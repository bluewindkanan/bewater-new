"""Eval judge: structured checks + src/bw oracle + needs-review (spec §11.1).

No LLM-judging-LLM: NL ``required_assertions`` / ``forbidden_behaviors`` that
lack a matching structured ``check`` are surfaced as ``needs-review`` for a
human reviewer rather than graded by an LLM.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from evals._harness import result

# Checks that signal an artifact/side-effect write on disk. NL forbidden
# behaviors matching these heuristics map to filesystem probes rather than a
# needs-review review item.
_FORBIDDEN_ARTIFACT_HINTS = (
    "writes an artifact",
    "writes artifact",
    "artifact write",
    "writes a file",
    "writes files",
    "new file",
    "creates an artifact",
)

# Product-side directories where a fresh file means an artifact/side-effect was
# produced by the run.
_PRODUCT_WRITE_DIRS = ("_bewater-output", "_bewater/records")


def _read_transcript(run_artifact: dict) -> str:
    """Best-effort read of the transcript file; empty string if unreadable."""
    path = run_artifact.get("transcript_path")
    if not path:
        return ""
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _check_transcript_contains(check: dict, transcript: str) -> dict:
    needle = str(check.get("params", {}).get("needle", ""))
    verdict = "pass" if needle and needle in transcript else "red"
    return {"id": check.get("id"), "type": "transcript_contains",
            "verdict": verdict, "detail": f"needle={needle!r} found={verdict == 'pass'}"}


def _check_transcript_regex_present(check: dict, transcript: str) -> dict:
    pattern = str(check.get("params", {}).get("pattern", ""))
    try:
        found = bool(re.search(pattern, transcript))
        verdict = "pass" if found else "red"
        detail = f"pattern={pattern!r} matched={found}"
    except re.error as exc:
        verdict, detail = "needs-review", f"invalid regex {pattern!r}: {exc}"
    return {"id": check.get("id"), "type": "transcript_regex_present",
            "verdict": verdict, "detail": detail}


def _check_transcript_regex_absent(check: dict, transcript: str) -> dict:
    pattern = str(check.get("params", {}).get("pattern", ""))
    try:
        found = bool(re.search(pattern, transcript))
        verdict = "pass" if not found else "red"
        detail = f"pattern={pattern!r} present={found}"
    except re.error as exc:
        verdict, detail = "needs-review", f"invalid regex {pattern!r}: {exc}"
    return {"id": check.get("id"), "type": "transcript_regex_absent",
            "verdict": verdict, "detail": detail}


def _glob_files(cwd: Path, paths: list[str]) -> list[Path]:
    """Resolve a list of glob patterns / dir roots under cwd to concrete files."""
    out: list[Path] = []
    for raw in paths or []:
        p = Path(raw)
        base = p if p.is_absolute() else (cwd / p)
        if base.is_dir():
            out.extend(sorted(base.rglob("*")))
        else:
            out.extend(sorted(cwd.glob(raw)) if not p.is_absolute() else sorted(Path("/").glob(str(p))))
    # Keep only files
    return [f for f in out if f.is_file()]


def _check_fs_no_new_files(check: dict, cwd: Path) -> dict:
    params = check.get("params", {})
    paths = params.get("paths") or list(_PRODUCT_WRITE_DIRS)
    files = _glob_files(cwd, paths)
    verdict = "pass" if not files else "red"
    return {"id": check.get("id"), "type": "fs_no_new_files",
            "verdict": verdict,
            "detail": f"{len(files)} file(s) under {paths}: {[str(f.relative_to(cwd)) for f in files[:5]]}"}


def _check_fs_wrote_file_matching(check: dict, cwd: Path) -> dict:
    pattern = str(check.get("params", {}).get("pattern", "*"))
    matches = sorted(cwd.glob(pattern))
    matches = [m for m in matches if m.is_file()]
    verdict = "pass" if matches else "red"
    return {"id": check.get("id"), "type": "fs_wrote_file_matching",
            "verdict": verdict,
            "detail": f"pattern={pattern!r} matched={len(matches)} file(s)"}


def _check_oracle_validate_ok(check: dict, cwd: Path) -> dict:
    """Run src/bw legacy validate/gate_scan read-only; never crash the harness.

    The legacy runtime is known-drifted vs v5 (memory §10.5). ANY import
    error, schema mismatch, or exception → needs-review with a note; the judge
    must never crash the harness over oracle drift.
    """
    gate = str(check.get("params", {}).get("gate", "G1"))
    try:
        from bw import (  # noqa: WPS433 (lazy: keep drift out of import-time)
            gate_scan,
            validate,
        )
    except Exception as exc:  # noqa: BLE001 — drift must not crash harness
        return {"id": check.get("id"), "type": "oracle_validate_ok",
                "verdict": "needs-review",
                "detail": f"oracle unavailable (import failed): {exc}"}

    try:
        issues = list(validate.validate_all(cwd))
        scan = gate_scan.scan(cwd, gate=gate)
        blocked = bool(getattr(scan, "blocked", False))
        verdict = "pass" if not issues and not blocked else "red"
        detail = f"validate_all={len(issues)} issue(s); gate={gate} blocked={blocked}"
        if issues:
            detail += f"; e.g. {issues[0].kind}: {issues[0].message}"
    except Exception as exc:  # noqa: BLE001 — drift must not crash harness
        return {"id": check.get("id"), "type": "oracle_validate_ok",
                "verdict": "needs-review",
                "detail": f"oracle drifted/unavailable: {type(exc).__name__}: {exc}"}
    return {"id": check.get("id"), "type": "oracle_validate_ok",
            "verdict": verdict, "detail": detail}


_DISPATCH = {
    "transcript_contains": lambda c, t, cwd: _check_transcript_contains(c, t),
    "transcript_regex_present": lambda c, t, cwd: _check_transcript_regex_present(c, t),
    "transcript_regex_absent": lambda c, t, cwd: _check_transcript_regex_absent(c, t),
    "fs_no_new_files": lambda c, t, cwd: _check_fs_no_new_files(c, cwd),
    "fs_wrote_file_matching": lambda c, t, cwd: _check_fs_wrote_file_matching(c, cwd),
    "oracle_validate_ok": lambda c, t, cwd: _check_oracle_validate_ok(c, cwd),
}


def _eval_structured_check(check: dict, transcript: str, cwd: Path) -> dict:
    fn = _DISPATCH.get(check.get("type"))
    if fn is None:
        return {"id": check.get("id"), "type": check.get("type"),
                "verdict": "needs-review",
                "detail": f"unknown check type {check.get('type')!r}"}
    return fn(check, transcript, cwd)


def _looks_like_artifact_write(text: str) -> bool:
    low = text.lower()
    return any(h in low for h in _FORBIDDEN_ARTIFACT_HINTS)


def _forbidden_triggered(forbidden: list[str], cwd: Path) -> tuple[list[str], list[dict]]:
    """Map NL forbidden behaviors to fs/transcript probes where possible.

    Returns (triggered_list, review_items). Behaviors that can be mapped to a
    concrete filesystem probe and DID fire are added to triggered_list; ones we
    cannot mechanically detect become needs-review review items.
    """
    triggered: list[str] = []
    review_items: list[dict] = []
    wrote = bool(_glob_files(cwd, list(_PRODUCT_WRITE_DIRS)))

    for behavior in forbidden or []:
        if _looks_like_artifact_write(behavior):
            if wrote:
                triggered.append(behavior)
            # If no write happened, the forbidden behavior did not fire → not triggered, no review item.
            continue
        review_items.append({
            "id": f"forbidden:{behavior}",
            "type": "nl_forbidden_behavior",
            "verdict": "needs-review",
            "detail": f"no structured check maps to forbidden behavior {behavior!r}",
        })
    return triggered, review_items


def judge(manifest: dict, run_artifact: dict, sandbox: Any) -> dict:
    """Grade a single run against the manifest.

    Returns ``{checks, forbidden_triggered, verdict, reviewer: None}``.
    Verdict: needs-review if any check/review-item is needs-review; green if
    every check passes and no forbidden behavior triggered; red otherwise.
    """
    cwd = Path(getattr(sandbox, "product_cwd", "."))
    transcript = _read_transcript(run_artifact)

    checks: list[dict] = []
    for c in manifest.get("checks", []) or []:
        checks.append(_eval_structured_check(c, transcript, cwd))

    # NL assertions without a matching structured check → needs-review review
    # items (§11.1: no LLM-judging-LLM). We have no machine mapping from NL
    # prose to a check id, so an assertion is "covered" only when the scenario
    # declares at least one structured check; otherwise it is surfaced for a
    # human reviewer.
    has_structured = bool(manifest.get("checks"))
    for assertion in manifest.get("required_assertions", []) or []:
        verdict = "pass" if has_structured else "needs-review"
        checks.append({
            "id": f"assertion:{assertion}",
            "type": "nl_required_assertion",
            "verdict": verdict,
            "detail": "NL assertion; verified only via accompanying structured check"
                      if has_structured
                      else "NL assertion without a matching structured check; needs human review",
        })

    forbidden_triggered, forbidden_review = _forbidden_triggered(
        manifest.get("forbidden_behaviors", []) or [], cwd)
    checks.extend(forbidden_review)

    verdict = result.derive_verdict({"checks": checks, "forbidden_triggered": forbidden_triggered})
    return {
        "checks": checks,
        "forbidden_triggered": forbidden_triggered,
        "verdict": verdict,
        "reviewer": None,
    }
