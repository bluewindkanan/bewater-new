"""Fresh-context runner: spawns headless Codex in an isolated cwd/env."""
from __future__ import annotations
import json
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any


def _popen(cmd: list[str], **kw: Any) -> subprocess.Popen:
    """Wrapper around subprocess.Popen so tests can inject a fake."""
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)


def _resolve_codex_binary() -> str:
    """Resolve the real Codex binary, not a shell function."""
    path = shutil.which("codex")
    if path:
        return path
    # Fallback: resolve via bash -lc command -v
    try:
        result = subprocess.run(
            ["bash", "-lc", "command -v codex"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise RuntimeError("Cannot resolve codex binary")


def _thread_id(stdout: bytes) -> str | None:
    """Extract the Codex thread ID from its JSONL event stream."""
    for line in stdout.decode("utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            thread_id = event.get("thread_id")
            return str(thread_id) if thread_id else None
    return None


def run_once(prompt: str, sandbox: Any, model: str | None = None) -> dict[str, Any]:
    """Spawn headless Codex with isolated cwd/env and capture JSONL output.

    Args:
        prompt: The prompt to send to Codex.
        sandbox: Object with product_cwd (Path), temp_home (Path), env (dict).
        model: Optional model name to pass via --model.

    Returns:
        Dict with keys: returncode, stdout, transcript_path, fresh_context_id.
    """
    codex_path = _resolve_codex_binary()
    cmd = [
        codex_path, "--ask-for-approval", "never", "exec", "--json", "--ephemeral",
        "--skip-git-repo-check", "--sandbox", "workspace-write",
        "-C", str(sandbox.product_cwd),
    ]
    if model:
        cmd.extend(["--model", model])
    cmd.append(prompt)

    proc = _popen(
        cmd,
        cwd=sandbox.product_cwd,
        env=sandbox.env,
    )
    stdout_bytes, stderr_bytes = proc.communicate()

    # Persist transcript — uuid4 so two reps in the same millisecond never collide.
    transcript_path = sandbox.temp_home / f"transcript-{uuid.uuid4().hex}.json"
    transcript_path.write_bytes(stdout_bytes)

    fresh_context_id = _thread_id(stdout_bytes) if proc.returncode == 0 else None

    return {
        "returncode": proc.returncode,
        "stdout": stdout_bytes.decode("utf-8", errors="replace"),
        "stderr": stderr_bytes.decode("utf-8", errors="replace"),
        "transcript_path": str(transcript_path),
        "fresh_context_id": fresh_context_id,
    }
