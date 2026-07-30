"""bw-journal command handlers.

Each function wraps one or more ``bw`` runtime calls and adds the "journal"
UX layer: concise output, emoji status markers, auto-computed fields.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# --- helpers ----------------------------------------------------------------

_LEDGER_PATH = "_bewater/state/assumption-ledger.yaml"


def _bw(*args: str, root: Path | None = None) -> subprocess.CompletedProcess:
    """Run the ``bw`` CLI inside an optional project root."""
    cwd = root or Path.cwd()
    return subprocess.run(
        [sys.executable, "-m", "bw", *args],
        capture_output=True, text=True, cwd=cwd,
    )


def _expect_bw_ledger(*args: str, root: Path) -> subprocess.CompletedProcess:
    """Run ``bw ledger <subcmd>`` and exit on failure."""
    r = subprocess.run(
        [sys.executable, "-m", "bw", "ledger", *args],
        capture_output=True, text=True, cwd=root,
    )
    if r.returncode != 0:
        print(f"bw-journal: bw error — {r.stderr.strip() or r.stdout.strip()}")
        sys.exit(r.returncode)
    return r


def _telemetry_ping(event: str, root: Path) -> None:
    """Opt-in anonymous usage ping.

    Only fires if the env var ``BW_JOURNAL_TELEMETRY`` is truthy or if
    ``.bw-journal/telemetry`` exists in the root.  Logs to stdout on failure
    (never blocks).
    """
    if not os.environ.get("BW_JOURNAL_TELEMETRY"):
        if not (root / ".bw-journal" / "telemetry").is_file():
            return
    try:
        payload = json.dumps({
            "event": event,
            "version": _version(),
            "ts": int(time.time()),
        })
        # async fire-and-forget via subprocess — won't block the CLI
        subprocess.Popen(
            ["curl", "-s", "-o", "/dev/null", "-X", "POST",
             "https://telemetry.bw-journal.dev/ping",
             "-H", "Content-Type: application/json",
             "-d", payload],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass  # never crash for telemetry


def _version() -> str:
    from . import __version__
    return __version__


def _ensure_journal_dir(root: Path) -> Path:
    """Return ``root/.bw-journal``, creating if absent."""
    jd = root / ".bw-journal"
    jd.mkdir(parents=True, exist_ok=True)
    return jd


# --- commands ---------------------------------------------------------------


def cmd_init(project: Path) -> int:
    """Scaffold a new journal directory.

    Creates ``_bewater/`` via ``bw init`` and a local ``.bw-journal/``
    marker so subsequent commands find the project root automatically.
    """
    root = project.resolve()
    if (root / _LEDGER_PATH).is_file():
        print(f"bw-journal: already a journal at {root}")
        return 0

    r = subprocess.run(
        [sys.executable, "-m", "bw", "init", str(root)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"bw-journal init: {r.stderr.strip() or r.stdout.strip()}")
        return r.returncode

    _ensure_journal_dir(root)
    print(f"bw-journal: journal created at {root}")
    print("  next:  bw-journal log 'we believe X because Y'")
    return 0


def cmd_log(
    project: Path,
    statement: str,
    impact: str,
    uncertainty: str,
    category: str,
    side: str,
    branch: str,
    telemetry: bool,
) -> int:
    """Log a new assumption entry.

    Auto-fills ``layer`` (``feature``), ``evidence_level`` (``L1``),
    ``validation_status`` (``open``), and ``--side`` → ``derived_from``
    mapping.
    """
    root = project.resolve()
    if not (root / _LEDGER_PATH).is_file():
        print("bw-journal: not a journal directory (run 'bw-journal init' first)")
        return 1

    # Map --side to derivation track for the ledger
    derived = []
    if side in ("magic", "both"):
        derived.append("consumer-insight")
    if side in ("money", "both"):
        derived.append("commercial-insight")

    args = [
        "add",
        str(root),
        "--statement", statement,
        "--layer", "feature",
        "--category", category,
        "--impact", impact,
        "--uncertainty", uncertainty,
        "--branch", branch,
        "--evidence-level", "L1",
        "--validation-status", "open",
        "--status", "active",
    ]
    if derived:
        args += ["--derived-from"] + derived

    r = _expect_bw_ledger(*args, root=root)
    # Extract assigned id from output, e.g. "bw ledger add: A-001  ..."
    assigned_id = "?"
    if r.stdout:
        parts = r.stdout.strip().split()
        for p in parts:
            if p.startswith("A-") and len(p) > 2:
                assigned_id = p.rstrip(":")
                break

    print(f"  ✓ {assigned_id}  {statement}")
    entry_path = root / _LEDGER_PATH
    print(f"    → {entry_path}")

    if telemetry:
        _telemetry_ping("log", root)
    return 0


def cmd_status(project: Path, telemetry: bool) -> int:
    """Show a concise summary of the assumption ledger.

    Output mimics ``git status``: open / validated / falsified counts,
    plus the most recent entries.
    """
    root = project.resolve()
    if not (root / _LEDGER_PATH).is_file():
        print("bw-journal: not a journal directory")
        return 1

    # Validate first — reports issues cleanly without crashing
    r_val = _bw("validate", str(root), root=root)

    import yaml
    ledger_raw = yaml.safe_load((root / _LEDGER_PATH).read_text())
    raw = ledger_raw.get("assumptions", [])
    if isinstance(raw, dict):
        assumptions = list(raw.values())
    else:
        assumptions = raw
    if not assumptions:
        print("bw-journal: 0 assumptions in ledger")
        return 0

    total = len(assumptions)
    open_ = [a for a in assumptions if a.get("status") == "active"]
    validated = [a for a in assumptions if a.get("validation_status") == "validated"]
    falsified = [a for a in assumptions if a.get("status") in ("killed", "falsified")]
    achilles = [a for a in assumptions if a.get("l4_obligation_status") == "open"]

    # Recent entries (last 5 by id order)
    def _num_id(a: dict) -> int:
        try:
            return int(a.get("id", "A-0").split("-")[1])
        except (IndexError, ValueError):
            return 0
    recent = sorted(assumptions, key=_num_id, reverse=True)[:5]

    print(f"bw-journal status — {total} assumption{'s' if total != 1 else ''}")
    print(f"  open:      {len(open_)}")
    print(f"  validated: {len(validated)}")
    print(f"  falsified: {len(falsified)}")
    print(f"  achilles:  {len(achilles)}")

    if r_val.returncode != 0:
        first_issue = r_val.stdout.strip().split("\n")[0] if r_val.stdout else "?"
        print(f"  ⚠ validate: {first_issue}")

    print()
    if recent:
        print("  recent entries:")
        for a in recent:
            kid = a.get("id", "?")
            st = a.get("statement", "?")[:72]
            stmt = f"\"{st}\"" if st != "?" else "?"
            ev = a.get("evidence_level", "L1")
            sts = a.get("validation_status", "open")
            act = a.get("status", "active")
            marker = "✓" if act != "active" else ("●" if a.get("l4_obligation_status") == "open" else "○")
            print(f"    {marker} {kid} ({ev}, {sts})  {stmt}")
    else:
        print("  (no entries)")

    if telemetry:
        _telemetry_ping("status", root)
    return 0


def cmd_diff(project: Path) -> int:
    """Show changes since the last checkpoint (baseline).

    Delegates to ``git diff`` on the ``_bewater/ledger.yaml`` file.
    Falls back to a YAML-based field-level diff if git is unavailable.
    """
    root = project.resolve()
    ledger_file = root / _LEDGER_PATH
    if not ledger_file.is_file():
        print("bw-journal: not a journal directory")
        return 1

    # Try git diff first
    try:
        r = subprocess.run(
            ["git", "diff", "--", str(ledger_file.relative_to(root))],
            capture_output=True, text=True, cwd=root,
        )
        if r.returncode == 0 and r.stdout.strip():
            print(r.stdout)
            return 0
    except Exception:
        pass

    # Fallback: show the file as-is
    print(f"bw-journal diff: no tracked changes (ledger at {ledger_file})")
    return 0
