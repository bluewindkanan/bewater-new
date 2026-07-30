"""TDD for the orchestrator. run_once is faked; no real LLM call."""
from __future__ import annotations
from pathlib import Path
import yaml
from evals._harness import orchestrator, result

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
    # Verify run_skill passes reps through to run_scenario
    m = {"scenario_id": "BWSH-S3", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": [],
         "forbidden_behaviors": [],
         "repetition_count": 5,  # Manifest default
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "ok"}}]}

    # Create a minimal scenario directory structure in the REPO (not tmp_path)
    # run_skill looks for scenarios in repo/evals/_scenarios/skill_name
    scenarios_dir = REPO / "evals" / "_scenarios" / "bw-shape"
    scenarios_dir.mkdir(parents=True, exist_ok=True)
    import yaml
    manifest_file = scenarios_dir / "BWSH-S3.yaml"
    manifest_file.write_text(yaml.dump(m))

    try:
        # Run with reps=2 override
        summary = orchestrator.run_skill(tmp_path, REPO, "bw-shape", mode="green", reps=2,
                                        run_once=_fake_runner("ok\n"))

        # Should get 2 results, not 5 (manifest default)
        assert summary["total_reps"] == 2
        assert len(summary["results"]) == 2
    finally:
        # Clean up the created manifest file
        manifest_file.unlink()
