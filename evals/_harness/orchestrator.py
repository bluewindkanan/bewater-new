"""Eval orchestrator: per-scenario RED/GREEN loop, rep tiering (spec §11.1)."""
from __future__ import annotations

import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from evals._harness import isolation, judge, loader, result, runner


def _persist_transcript(
    eval_root: Path, skill: str, mode: str, scenario_id: str, rep: int, src_transcript: str
) -> str | None:
    """Copy the in-temp-home transcript to a durable location so it survives
    Sandbox cleanup. Returns the durable path (or the original path if no source
    file exists). Spec §11.1 — the result payload's transcript_path must point at
    a file the human reviewer can still open after the run.

    Durable layout: <eval_root>/<skill>/<mode>/transcript-<scenario_id>-r<rep>.json
    """
    if not src_transcript:
        return src_transcript
    src = Path(src_transcript)
    if not src.exists():
        # Nothing to copy (e.g. faked run without a transcript); leave as-is.
        return src_transcript
    dst_dir = eval_root / "evals" / skill / mode
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f"transcript-{scenario_id}-r{rep}.json"
    shutil.copyfile(src, dst)
    return str(dst)


def run_scenario(
    eval_root: Path,
    repo: Path,
    manifest: dict,
    mode: str,
    reps: int | None = None,
    model: str | None = None,
    run_once: Callable[[str, Any, str | None], dict] = runner.run_once,
) -> list[dict]:
    """Run a single scenario multiple times, returning one result per rep.

    Args:
        eval_root: Root directory for eval results (writes go here)
        repo: Source repository path (skills are read from here)
        manifest: Scenario manifest dict (from loader.load_manifest)
        mode: "green" or "red"
        reps: Number of repetitions (defaults to manifest["repetition_count"])
        model: Optional model name to pass to runner
        run_once: Injectable runner function (for testing)

    Returns:
        List of result dicts, one per repetition
    """
    if reps is None:
        reps = manifest.get("repetition_count", 1)

    target_skill = manifest.get("target_skill", "unknown")
    scenario_id = manifest.get("scenario_id", "unknown")
    dependency_skills = manifest.get("installed_dependency_skills", [])

    results = []

    for rep in range(1, reps + 1):
        with tempfile.TemporaryDirectory(prefix="sandbox-product-") as product_temp:  # noqa: SIM117
            with tempfile.TemporaryDirectory(prefix="sandbox-home-") as home_temp:
                # Build sandbox
                sandbox = isolation.Sandbox(
                    repo=repo,
                    product_root=Path(product_temp),
                    home_root=Path(home_temp),
                    target_skill=target_skill,
                    dependency_skills=dependency_skills,
                    mode=mode,
                    fixture_refs=manifest.get("fixture_refs", []),
                )
                with sandbox:
                    # Run the prompt
                    prompt = manifest.get("prompt", "")
                    run_artifact = run_once(prompt, sandbox, model)

                    # Judge the result
                    judgment = judge.judge(manifest, run_artifact, sandbox)

                    # Persist the transcript to a durable location BEFORE the
                    # Sandbox exits and removes temp_home — the in-temp-home
                    # transcript is otherwise lost, leaving needs-review items
                    # unreviewable (pilot gap F1).
                    durable_transcript = _persist_transcript(
                        eval_root, target_skill, mode, scenario_id, rep,
                        run_artifact.get("transcript_path"),
                    )

                    # Assemble result payload
                    payload = {
                        "scenario_id": scenario_id,
                        "target_skill": target_skill,
                        "mode": mode,
                        "repetition": rep,
                        "fresh_context_id": run_artifact.get("fresh_context_id"),
                        "cwd": str(sandbox.product_cwd),
                        "temp_home": str(sandbox.temp_home),
                        "project_local_skills": sandbox.installed_skills or [],
                        "global_skills": [],
                        "model": model,
                        "transcript_path": durable_transcript,
                        "checks": judgment.get("checks", []),
                        "forbidden_triggered": judgment.get("forbidden_triggered", []),
                        "verdict": judgment.get("verdict"),  # Will be re-derived by write_result
                        "reviewer": judgment.get("reviewer"),
                    }

                    # Write result
                    result.write_result(
                        eval_root, target_skill, mode, scenario_id, rep, payload
                    )

                    # Return with the derived verdict
                    payload["verdict"] = result.derive_verdict(payload)
                    results.append(payload)

    return results


def run_skill(
    eval_root: Path,
    repo: Path,
    skill_name: str,
    mode: str = "green",
    model: str | None = None,
    reps: int | None = None,
    run_once: Callable[[str, Any, str | None], dict] = runner.run_once,
) -> dict:
    """Run all scenarios for a given skill.

    Args:
        eval_root: Root directory for eval results
        repo: Source repository path
        skill_name: Name of the skill to test
        mode: "green" or "red"
        model: Optional model name
        reps: Optional repetition count (overrides manifest defaults)
        run_once: Injectable runner function

    Returns:
        Summary dict with skill_name, mode, total_scenarios, total_reps, results
    """
    # Discover all scenario manifests for this skill under the REAL layout:
    # GREEN -> evals/{skill}/scenarios/*.yaml, RED -> evals/{skill}/red/*.yaml
    # (matches scripts/verify.py::list_eval_scenarios).
    bucket = "scenarios" if mode == "green" else "red"
    scenarios_dir = repo / "evals" / skill_name / bucket
    if not scenarios_dir.exists():
        return {
            "skill_name": skill_name,
            "mode": mode,
            "total_scenarios": 0,
            "total_reps": 0,
            "results": [],
        }

    all_results = []
    for manifest_file in sorted(scenarios_dir.glob("*.yaml")):
        manifest = loader.load_manifest(manifest_file)
        scenario_results = run_scenario(
            eval_root, repo, manifest, mode, reps=reps, model=model, run_once=run_once
        )
        all_results.extend(scenario_results)

    return {
        "skill_name": skill_name,
        "mode": mode,
        "total_scenarios": len(all_results),
        "total_reps": len(all_results),  # Each result is one rep
        "results": all_results,
    }


def run_all(
    eval_root: Path,
    repo: Path,
    mode: str = "green",
    model: str | None = None,
    reps: int | None = None,
    run_once: Callable[[str, Any, str | None], dict] = runner.run_once,
) -> dict:
    """Run all scenario manifests across all skills.

    Args:
        eval_root: Root directory for eval results
        repo: Source repository path
        mode: "green" or "red"
        model: Optional model name
        reps: Optional repetition count (overrides manifest defaults)
        run_once: Injectable runner function

    Returns:
        Summary dict with all skills combined
    """
    # Discover all skill directories under the REAL layout: evals/bw-*/...
    # A skill is a candidate if evals/{skill}/ exists (matches verify.py).
    evals_root = repo / "evals"
    if not evals_root.exists():
        return {
            "mode": mode,
            "total_skills": 0,
            "total_scenarios": 0,
            "total_reps": 0,
            "results": [],
        }

    all_results = []
    skill_count = 0

    for skills_dir in sorted(evals_root.iterdir()):
        if not skills_dir.is_dir() or not skills_dir.name.startswith("bw-"):
            continue
        skill_name = skills_dir.name
        skill_summary = run_skill(
            eval_root, repo, skill_name, mode=mode, reps=reps, model=model, run_once=run_once
        )
        if skill_summary["total_scenarios"] > 0:
            skill_count += 1
            all_results.extend(skill_summary["results"])

    return {
        "mode": mode,
        "total_skills": skill_count,
        "total_scenarios": len(all_results),
        "total_reps": len(all_results),
        "results": all_results,
    }
