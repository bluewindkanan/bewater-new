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
