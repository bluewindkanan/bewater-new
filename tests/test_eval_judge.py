"""TDD for the judge: structured checks + oracle + needs-review (§11.1 no LLM-judging-LLM)."""
from __future__ import annotations

from evals._harness import judge


def _manifest(checks, assertions=None, forbidden=None):
    return {"scenario_id": "S", "target_skill": "bw-start", "prompt": "p",
            "required_assertions": assertions or [], "forbidden_behaviors": forbidden or [],
            "repetition_count": 1, "checks": checks}


def test_transcript_regex_present_pass(tmp_path):
    t = tmp_path / "t.jsonl"; t.write_text('the gate presents Go and Kill exits\n')
    m = _manifest([{"id": "exits", "type": "transcript_regex_present",
                    "params": {"pattern": r"\b(Go|Kill)\b"}}])
    out = judge.judge(m, {"transcript_path": str(t)}, type("SB", (), {"product_cwd": tmp_path})())
    assert out["checks"][0]["verdict"] == "pass" and out["verdict"] == "green"


def test_fs_no_new_files_detects_a_write(tmp_path):
    (tmp_path / "_bewater-output").mkdir()
    (tmp_path / "_bewater-output" / "ART-1.md").write_text("x")  # forbidden artifact write
    m = _manifest([], forbidden=["writes an artifact"])
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")},
                      type("SB", (), {"product_cwd": tmp_path})())
    assert "writes an artifact" in out["forbidden_triggered"]


def test_nl_assertion_without_check_is_needs_review(tmp_path):
    m = _manifest([], assertions=["presents the five permitted exits"])  # no structured check
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")},
                      type("SB", (), {"product_cwd": tmp_path})())
    assert out["verdict"] == "needs-review"
    assert any(c["verdict"] == "needs-review" for c in out["checks"])


def _sb(tmp_path):
    return type("SB", (), {"product_cwd": tmp_path})()


def test_transcript_contains_and_regex_absent(tmp_path):
    t = tmp_path / "t.jsonl"; t.write_text("hello world\n")
    m = _manifest([
        {"id": "c1", "type": "transcript_contains", "params": {"needle": "hello"}},
        {"id": "c2", "type": "transcript_contains", "params": {"needle": "missing"}},
        {"id": "c3", "type": "transcript_regex_absent",
         "params": {"pattern": r"forbidden\d+"}},
    ])
    out = judge.judge(m, {"transcript_path": str(t)}, _sb(tmp_path))
    verdicts = {c["id"]: c["verdict"] for c in out["checks"]}
    assert verdicts == {"c1": "pass", "c2": "red", "c3": "pass"}
    assert out["verdict"] == "red"


def test_fs_wrote_file_matching(tmp_path):
    (tmp_path / "ART-7.md").write_text("x")
    m = _manifest([{"id": "w", "type": "fs_wrote_file_matching",
                    "params": {"pattern": "ART-*.md"}}])
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")}, _sb(tmp_path))
    assert out["checks"][0]["verdict"] == "pass"
    assert out["verdict"] == "green"


def test_oracle_validate_ok_drift_is_needs_review(tmp_path):
    # No _bewater/ state under cwd → legacy oracle errors/raises → needs-review, never crashes.
    m = _manifest([{"id": "o", "type": "oracle_validate_ok", "params": {"gate": "G1"}}])
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")}, _sb(tmp_path))
    assert out["checks"][0]["verdict"] == "needs-review"
    assert out["verdict"] == "needs-review"
    assert out["reviewer"] is None


def test_oracle_validate_ok_blocked_gate_forces_red(tmp_path):
    # I1 regression: a blocking gate failure (go withheld) must force the oracle
    # check red even when validate_all is clean. The check reads the REAL
    # GateScanResult signal (exit_allowed lacks "go"), not a non-existent
    # `blocked` attr.
    import sys
    import types
    from typing import ClassVar

    class _Scan:
        # go withheld → blocked. Mirrors GateScanResult when a blocking
        # criterion fails (exit_allowed == the 4 non-go exits).
        exit_allowed: ClassVar[list[str]] = ["conditional-go", "recycle", "pivot", "kill"]

    fake_bw = types.ModuleType("bw")
    fake_validate = types.ModuleType("bw.validate")
    fake_validate.validate_all = lambda cwd: iter(())  # no issues
    fake_gate_scan = types.ModuleType("bw.gate_scan")
    fake_gate_scan.scan = lambda cwd, gate="G1": _Scan()
    fake_bw.validate = fake_validate
    fake_bw.gate_scan = fake_gate_scan

    real_bw = sys.modules.get("bw")
    real_validate = sys.modules.get("bw.validate")
    real_gate_scan = sys.modules.get("bw.gate_scan")
    sys.modules["bw"] = fake_bw
    sys.modules["bw.validate"] = fake_validate
    sys.modules["bw.gate_scan"] = fake_gate_scan
    try:
        m = _manifest([{"id": "o", "type": "oracle_validate_ok", "params": {"gate": "G1"}}])
        out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")}, _sb(tmp_path))
        assert out["checks"][0]["verdict"] == "red"
        assert out["verdict"] == "red"
        assert "blocked=True" in out["checks"][0]["detail"]
    finally:
        for key, mod in (("bw", real_bw), ("bw.validate", real_validate),
                         ("bw.gate_scan", real_gate_scan)):
            if mod is None:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = mod


def test_unknown_check_type_is_needs_review(tmp_path):
    m = _manifest([{"id": "u", "type": "no_such_type", "params": {}}])
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")}, _sb(tmp_path))
    assert out["checks"][0]["verdict"] == "needs-review"


def test_forbidden_artifact_write_when_clean_is_not_triggered(tmp_path):
    # No files under product write dirs → forbidden behavior did not fire.
    m = _manifest([], forbidden=["writes an artifact"])
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")}, _sb(tmp_path))
    assert out["forbidden_triggered"] == []
    assert out["verdict"] == "green"


def test_nl_assertion_with_unrelated_passing_check_is_needs_review(tmp_path):
    # Regression (§11.1): a passing structured check must NOT auto-cover an
    # UNRELATED NL required_assertion. The NL assertion is its own needs-review
    # item, and the overall verdict is needs-review (NOT green).
    t = tmp_path / "t.jsonl"; t.write_text("hello world\n")
    m = _manifest(
        [{"id": "c1", "type": "transcript_contains", "params": {"needle": "hello"}}],
        assertions=["presents the five permitted exits"],  # unrelated to the check
    )
    out = judge.judge(m, {"transcript_path": str(t)}, _sb(tmp_path))
    nl_items = [c for c in out["checks"] if c["id"].startswith("nl-assertion-")]
    assert len(nl_items) == 1
    assert nl_items[0]["verdict"] == "needs-review"
    assert nl_items[0]["detail"] == "presents the five permitted exits"
    assert out["verdict"] == "needs-review"
