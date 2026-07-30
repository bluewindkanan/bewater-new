"""Fresh-context runner: spawns headless claude in isolated cwd/env, captures JSON output."""
from __future__ import annotations
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


def _popen(cmd: list[str], **kw: Any) -> subprocess.Popen:
    """Wrapper around subprocess.Popen so tests can inject a fake."""
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)


def _resolve_claude_binary() -> str:
    """Resolve the real claude binary, not a shell function."""
    path = shutil.which("claude")
    if path:
        return path
    # Fallback: resolve via bash -lc command -v
    try:
        result = subprocess.run(
            ["bash", "-lc", "command -v claude"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise RuntimeError("Cannot resolve claude binary")


def run_once(prompt: str, sandbox: Any, model: str | None = None) -> dict[str, Any]:
    """Spawn headless claude with isolated cwd/env, capture JSON output.

    Args:
        prompt: The prompt to send to claude.
        sandbox: Object with product_cwd (Path), temp_home (Path), env (dict).
        model: Optional model name to pass via --model.

    Returns:
        Dict with keys: returncode, stdout, transcript_path, fresh_context_id.
    """
    claude_path = _resolve_claude_binary()
    cmd = [claude_path, "-p", prompt, "--output-format", "json"]
    if model:
        cmd.extend(["--model", model])

    proc = _popen(
        cmd,
        cwd=sandbox.product_cwd,
        env=sandbox.env,
    )
    stdout_bytes, stderr_bytes = proc.communicate()

    # Persist transcript
    timestamp = int(time.time() * 1000)
    transcript_path = sandbox.temp_home / f"transcript-{timestamp}.json"
    transcript_path.write_bytes(stdout_bytes)

    # Extract session_id as fresh_context_id
    fresh_context_id = None
    if proc.returncode == 0:
        try:
            data = json.loads(stdout_bytes.decode("utf-8"))
            fresh_context_id = data.get("session_id")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    return {
        "returncode": proc.returncode,
        "stdout": stdout_bytes.decode("utf-8", errors="replace"),
        "transcript_path": str(transcript_path),
        "fresh_context_id": fresh_context_id,
    }
