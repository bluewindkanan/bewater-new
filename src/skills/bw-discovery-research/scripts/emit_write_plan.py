#!/usr/bin/env python3
"""Emit a validated resumable Research transaction plan."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_research_plan import validate_files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-id", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--artifact-path", required=True)
    parser.add_argument("--artifact-file", type=Path, required=True)
    parser.add_argument("--charter-file", type=Path, required=True)
    parser.add_argument("--ledger-before-file", type=Path, required=True)
    parser.add_argument("--ledger-file", type=Path, required=True)
    parser.add_argument("--cas-step", nargs=4, action="append", default=[])
    args = parser.parse_args()

    errors = validate_files(
        args.artifact_file, args.charter_file, args.ledger_before_file, args.ledger_file
    )
    ledger_changed = args.ledger_before_file.read_text() != args.ledger_file.read_text()
    ledger_steps = [step for step in args.cas_step if step[1] == "_bewater/ledger.yaml"]
    if ledger_changed and (
        len(ledger_steps) != 1 or Path(ledger_steps[0][3]).resolve() != args.ledger_file.resolve()
    ):
        errors.append("A changed staged ledger requires exactly one ledger CAS using --ledger-file.")
    if not ledger_changed and ledger_steps:
        errors.append("An unchanged staged ledger must omit the ledger CAS.")
    if errors:
        print("Research Plan validation failed; no write plan was emitted.", file=sys.stderr)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    steps = [{
        "step_id": "research-revision",
        "op": "write_new",
        "path": args.artifact_path,
        "new_text": args.artifact_file.read_text(),
    }]
    for step_id, path, expected, text_file in args.cas_step:
        steps.append({
            "step_id": step_id,
            "op": "cas_commit",
            "path": path,
            "expected_revision": int(expected),
            "new_text": Path(text_file).read_text(),
        })
    print(json.dumps({"action_id": args.action_id, "owner": args.owner, "steps": steps}))


if __name__ == "__main__":
    main()
