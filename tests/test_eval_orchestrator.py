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
    # Provide fake source skills so isolation can deploy them.
    skills_src = repo / "src" / "skills"
    for name in ("bw-shape", "bw-resume", "bw-ideate"):
        d = skills_src / name; d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"# {name}\n")

    m = {"scenario_id": "BWSH-DEP", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [], "forbidden_behaviors": [],
         "installed_dependency_skills": ["bw-resume", "bw-ideate"],
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
    assert "bw-resume" in installed["skills"]
    assert "bw-ideate" in installed["skills"]
    assert "bw-shape" in installed["skills"]


def test_run_skill_dependency_key_legacy_is_ignored(tmp_path):
    # C2 regression guard: the old `dependency_skills` key must NOT install
    # skills (only `installed_dependency_skills` counts). No skills should be
    # copied beyond the target itself in GREEN.
    repo = tmp_path / "repo"
    skills_src = repo / "src" / "skills"
    for name in ("bw-shape", "bw-resume"):
        d = skills_src / name; d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"# {name}\n")

    m = {"scenario_id": "BWSH-LEG", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [], "forbidden_behaviors": [],
         "dependency_skills": ["bw-resume"],  # legacy key — must be ignored
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

    assert "bw-resume" not in installed["skills"]
    assert installed["skills"] == ["bw-shape"]


def test_active_eval_manifests_do_not_reference_bw_start():
    manifests = [
        *REPO.glob("evals/*/scenarios/*.yaml"),
        *REPO.glob("evals/*/red/*.yaml"),
    ]

    references = [path for path in manifests if "bw-start" in path.read_text()]

    assert references == []


def test_run_scenario_applies_declared_fixture_overlay(tmp_path):
    repo = tmp_path / "repo"
    skill = repo / "src" / "skills" / "bw-resume"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# resume\n")
    fixture = repo / "evals" / "fixtures" / "pending-g1"
    record = fixture / "_bewater" / "records" / "D-001-g1.yaml"
    record.parent.mkdir(parents=True)
    record.write_text("gate: G1\naction_plan:\n  action_status: pending\n")
    manifest = {
        "scenario_id": "BWRESUME-FIXTURE",
        "target_skill": "bw-resume",
        "prompt": "resume",
        "fixture_refs": ["evals/fixtures/pending-g1"],
        "required_assertions": [],
        "forbidden_behaviors": [],
        "repetition_count": 1,
        "checks": [],
    }

    def assert_fixture(_prompt, sandbox, _model=None):
        deployed = sandbox.product_cwd / "_bewater" / "records" / record.name
        assert deployed.read_text() == record.read_text()
        transcript = sandbox.temp_home / "t.jsonl"
        transcript.write_text("ok\n")
        return {"returncode": 0, "transcript_path": str(transcript), "fresh_context_id": "ctx"}

    result = orchestrator.run_scenario(
        tmp_path / "results", repo, manifest, mode="green", run_once=assert_fixture
    )
    assert len(result) == 1


def test_run_scenario_persists_durable_transcript_after_sandbox_exits(tmp_path):
    # Pilot gap F1: the runner writes the transcript into sandbox.temp_home, but
    # Sandbox.__exit__ removes temp dirs -> the stored transcript_path dangles and
    # needs-review items become unreviewable. After run_scenario completes (and the
    # Sandbox has exited), the durable transcript file at the result's
    # transcript_path MUST still exist (the in-temp-home copy is gone).
    import json

    m = {"scenario_id": "BWSH-F1", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [], "forbidden_behaviors": [],
         "repetition_count": 1,
         "checks": [{"id": "c", "type": "transcript_contains", "params": {"needle": "ok"}}]}

    eval_root = tmp_path / "results"
    rs = orchestrator.run_scenario(eval_root, REPO, m, mode="green", reps=1,
                                   run_once=_fake_runner("ok\n"))

    transcript_path = Path(rs[0]["transcript_path"])

    # The durable transcript survives Sandbox cleanup.
    assert transcript_path.exists(), f"durable transcript missing at {transcript_path}"
    assert transcript_path.read_text() == "ok\n"
    # Durable layout: evals/{skill}/{mode}/transcript-{scenario_id}-r{rep}.json
    assert transcript_path.parent == eval_root / "evals" / "bw-shape" / "green"
    assert transcript_path.name == "transcript-BWSH-F1-r1.json"

    # The written result record points at the durable path.
    result_file = eval_root / "evals" / "bw-shape" / "green" / "BWSH-F1-r1.json"
    record = json.loads(result_file.read_text())
    assert record["transcript_path"] == str(transcript_path)
