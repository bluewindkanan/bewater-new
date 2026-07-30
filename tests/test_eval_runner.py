"""TDD for the fresh-context runner. Subprocess is faked; the real claude run is the pilot (T7)."""
from __future__ import annotations
from pathlib import Path
from evals._harness import runner


class _FakeSandbox:
    def __init__(self, tmp_path: Path):
        self.product_cwd = tmp_path / "prod"; self.product_cwd.mkdir()
        self.temp_home = tmp_path / "home"; self.temp_home.mkdir()
        self.env = {"HOME": str(self.temp_home), "ANTHROPIC_API_KEY": "k", "PATH": "/usr/bin"}


def test_run_once_invokes_headless_claude_with_cwd_and_env(tmp_path, monkeypatch):
    captured = {}
    def fake_popen(cmd, **kw):
        captured["cmd"] = cmd
        captured["cwd"] = kw.get("cwd")
        captured["env"] = kw.get("env")
        class R:
            returncode = 0
            def communicate(self): return (b'{"result":"hi","session_id":"s1"}', b"")
        return R()
    monkeypatch.setattr(runner, "_popen", fake_popen)
    sb = _FakeSandbox(tmp_path)
    out = runner.run_once("Status please", sb, model="claude-test")
    assert "claude" in captured["cmd"][0] or captured["cmd"][0].endswith("claude")
    assert "-p" in captured["cmd"]
    assert captured["cwd"] == sb.product_cwd
    assert captured["env"]["HOME"] == sb.env["HOME"]
    assert out["returncode"] == 0
    assert out["fresh_context_id"] == "s1"


def test_run_once_records_nonzero_exit(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "_popen", lambda cmd, **kw:
                        type("R", (), {"returncode": 1, "communicate": lambda self: (b"", b"boom")})())
    out = runner.run_once("p", _FakeSandbox(tmp_path))
    assert out["returncode"] == 1 and out["fresh_context_id"] is None


def test_run_once_surfaces_stderr(tmp_path, monkeypatch):
    # M1: stderr is surfaced for pilot diagnostics, not discarded.
    monkeypatch.setattr(runner, "_popen", lambda cmd, **kw:
                        type("R", (), {"returncode": 1,
                                       "communicate": lambda self: (b"", b"kaput")})())
    out = runner.run_once("p", _FakeSandbox(tmp_path))
    assert out["stderr"] == "kaput"


def test_run_once_transcript_names_are_unique(tmp_path, monkeypatch):
    # I2: two reps in the same millisecond must not overwrite each other's
    # transcript (uuid-based naming).
    def fake_popen(cmd, **kw):
        class R:
            returncode = 0
            def communicate(self): return (b'{"session_id":"s"}', b"")
        return R()
    monkeypatch.setattr(runner, "_popen", fake_popen)
    sb = _FakeSandbox(tmp_path)
    out1 = runner.run_once("p", sb)
    out2 = runner.run_once("p", sb)
    assert out1["transcript_path"] != out2["transcript_path"]
