"""TDD for the orchestrator. run_once is faked; no real LLM call."""
from __future__ import annotations
from pathlib import Path
import yaml
from evals._harness import orchestrator

REPO = Path(__file__).resolve().parents[1]


def _fake_runner(transcript_text):
    def _run(prompt, sandbox, model=None):
        t = sandbox.temp_home / "t.jsonl"
        t.write_text(transcript_text)
        return {"returncode": 0, "transcript_path": str(t), "fresh_context_id": "ctx"}
    return _run


def json_load(f):
    import json
    return json.loads(Path(f).read_text())


def test_run_scenario_green_writes_reps(tmp_path):
    m = {"scenario_id": "BWSH-S1", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [],  # No NL assertions to avoid needs-review
         "forbidden_behaviors": ["writes an artifact"],
         "repetition_count": 2,
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "bw-concept-gate"}}]}
    rs = orchestrator.run_scenario(tmp_path, REPO, m, mode="green", reps=2,
                                   run_once=_fake_runner("see bw-concept-gate next\n"))
    assert len(rs) == 2
    files = list((tmp_path / "evals" / "bw-shape" / "green").glob("BWSH-S1-r*.json"))
    assert len(files) == 2 and all(json_load(f)["verdict"] == "green" for f in files)


def test_run_scenario_red_must_fail_a_target_behavior(tmp_path):
    # RED = target absent; a well-formed RED transcript should miss the routing token
    # Note: NL assertions trigger needs-review per spec (no LLM-judging-LLM)
    m = {"scenario_id": "BWSH-R1", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [],  # No NL assertions to avoid needs-review
         "forbidden_behaviors": [],
         "repetition_count": 1,
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "bw-concept-gate"}}]}
    rs = orchestrator.run_scenario(tmp_path, REPO, m, mode="red", reps=1,
                                   run_once=_fake_runner("i do not know what to do\n"))
    assert rs[0]["verdict"] == "red"


def test_run_scenario_reps_override_manifest_default(tmp_path):
    # Verify explicit reps parameter overrides manifest repetition_count
    # Manifest says 3, we pass reps=2, should get 2 results
    m = {"scenario_id": "BWSH-S2", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [],
         "forbidden_behaviors": [],
         "repetition_count": 3,  # Manifest default
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "ok"}}]}
    rs = orchestrator.run_scenario(tmp_path, REPO, m, mode="green", reps=2,
                                   run_once=_fake_runner("ok\n"))
    assert len(rs) == 2
    files = list((tmp_path / "evals" / "bw-shape" / "green").glob("BWSH-S2-r*.json"))
    assert len(files) == 2


def test_run_skill_reps_override(tmp_path):
    # Verify run_skill passes reps through to run_scenario against the REAL
    # layout (evals/{skill}/scenarios/*.yaml) inside a tmp repo — no writes to
    # the live repo (M6 test isolation).
    m = {"scenario_id": "BWSH-S3", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [],
         "forbidden_behaviors": [],
         "repetition_count": 5,  # Manifest default
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "ok"}}]}

    repo = tmp_path / "repo"
    scenarios_dir = repo / "evals" / "bw-shape" / "scenarios"
    scenarios_dir.mkdir(parents=True)
    manifest_file = scenarios_dir / "BWSH-S3.yaml"
    manifest_file.write_text(yaml.dump(m))

    eval_root = tmp_path / "results"
    # Run with reps=2 override
    summary = orchestrator.run_skill(eval_root, repo, "bw-shape", mode="green", reps=2,
                                     run_once=_fake_runner("ok\n"))

    # Should get 2 results, not 5 (manifest default)
    assert summary["total_reps"] == 2
    assert len(summary["results"]) == 2
    files = list((eval_root / "evals" / "bw-shape" / "green").glob("BWSH-S3-r*.json"))
    assert len(files) == 2


def test_run_skill_discovers_real_layout_green_and_red(tmp_path):
    # C1: run_skill must discover manifests under the REAL layout
    # evals/{skill}/scenarios/*.yaml (GREEN) + evals/{skill}/red/*.yaml (RED).
    green = {"scenario_id": "BWSH-GA", "target_skill": "bw-shape", "prompt": "p",
             "required_assertions": [], "forbidden_behaviors": [],
             "repetition_count": 1,
             "checks": [{"id": "c", "type": "transcript_contains", "params": {"needle": "ok"}}]}
    red = {"scenario_id": "BWSH-RA", "target_skill": "bw-shape", "prompt": "p",
           "required_assertions": [], "forbidden_behaviors": [],
           "repetition_count": 1,
           "checks": [{"id": "c", "type": "transcript_contains", "params": {"needle": "ok"}}]}

    repo = tmp_path / "repo"
    gdir = repo / "evals" / "bw-shape" / "scenarios"; gdir.mkdir(parents=True)
    rdir = repo / "evals" / "bw-shape" / "red"; rdir.mkdir(parents=True)
    (gdir / "BWSH-GA.yaml").write_text(yaml.dump(green))
    (rdir / "BWSH-RA.yaml").write_text(yaml.dump(red))

    eval_root = tmp_path / "results"

    green_summary = orchestrator.run_skill(eval_root, repo, "bw-shape", mode="green",
                                           run_once=_fake_runner("ok\n"))
    assert green_summary["total_reps"] == 1
    assert green_summary["results"][0]["scenario_id"] == "BWSH-GA"
    assert green_summary["results"][0]["mode"] == "green"

    red_summary = orchestrator.run_skill(eval_root, repo, "bw-shape", mode="red",
                                         run_once=_fake_runner("not present\n"))
    assert red_summary["total_reps"] == 1
    assert red_summary["results"][0]["scenario_id"] == "BWSH-RA"
    assert red_summary["results"][0]["mode"] == "red"


def test_run_skill_installs_dependency_skills_in_sandbox(tmp_path):
    # C2: dependency skills declared under `installed_dependency_skills` must be
    # installed into the sandbox (read from the manifest key, not the old
    # `dependency_skills` key). GREEN also installs the target skill.
    repo = tmp_path / "repo"
    # Provide fake skill sources under repo/.claude/skills so isolation can copy them.
    skills_src = repo / ".claude" / "skills"
    for name in ("bw-shape", "bw-start", "bw-ideate"):
        d = skills_src / name; d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"# {name}\n")

    m = {"scenario_id": "BWSH-DEP", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [], "forbidden_behaviors": [],
         "installed_dependency_skills": ["bw-start", "bw-ideate"],
         "repetition_count": 1,
         "checks": []}
    (repo / "evals" / "bw-shape" / "scenarios").mkdir(parents=True)
    (repo / "evals" / "bw-shape" / "scenarios" / "BWSH-DEP.yaml").write_text(yaml.dump(m))

    installed = {}

    def capturing_runner(prompt, sandbox, model=None):
        installed["skills"] = list(sandbox.installed_skills or [])
        t = sandbox.temp_home / "t.jsonl"; t.write_text("ok\n")
        return {"returncode": 0, "transcript_path": str(t), "fresh_context_id": "ctx"}

    eval_root = tmp_path / "results"
    orchestrator.run_skill(eval_root, repo, "bw-shape", mode="green", run_once=capturing_runner)

    # Both declared deps + the target skill (GREEN) must be installed.
    assert "bw-start" in installed["skills"]
    assert "bw-ideate" in installed["skills"]
    assert "bw-shape" in installed["skills"]


def test_run_skill_dependency_key_legacy_is_ignored(tmp_path):
    # C2 regression guard: the old `dependency_skills` key must NOT install
    # skills (only `installed_dependency_skills` counts). No skills should be
    # copied beyond the target itself in GREEN.
    repo = tmp_path / "repo"
    skills_src = repo / ".claude" / "skills"
    for name in ("bw-shape", "bw-start"):
        d = skills_src / name; d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"# {name}\n")

    m = {"scenario_id": "BWSH-LEG", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [], "forbidden_behaviors": [],
         "dependency_skills": ["bw-start"],  # legacy key — must be ignored
         "repetition_count": 1,
         "checks": []}
    (repo / "evals" / "bw-shape" / "scenarios").mkdir(parents=True)
    (repo / "evals" / "bw-shape" / "scenarios" / "BWSH-LEG.yaml").write_text(yaml.dump(m))

    installed = {}

    def capturing_runner(prompt, sandbox, model=None):
        installed["skills"] = list(sandbox.installed_skills or [])
        return {"returncode": 0, "transcript_path": str(sandbox.temp_home / "t.jsonl"),
                "fresh_context_id": "ctx"}

    eval_root = tmp_path / "results"
    orchestrator.run_skill(eval_root, repo, "bw-shape", mode="green", run_once=capturing_runner)

    assert "bw-start" not in installed["skills"]
    assert installed["skills"] == ["bw-shape"]
