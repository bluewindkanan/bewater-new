from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_draft import validate_files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-id", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--artifact-path", required=True)
    parser.add_argument("--artifact-file", type=Path, required=True)
    parser.add_argument("--ledger-file", type=Path, required=True)
    parser.add_argument(
        "--cas-step",
        nargs=4,
        action="append",
        default=[],
        metavar=("STEP_ID", "PATH", "EXPECTED_REVISION", "TEXT_FILE"),
    )
    args = parser.parse_args()

    errors = validate_files(args.artifact_file, args.ledger_file)
    ledger_steps = [
        step for step in args.cas_step
        if step[1] == "_bewater/ledger.yaml"
    ]
    if not ledger_steps or any(Path(step[3]).resolve() != args.ledger_file.resolve() for step in ledger_steps):
        errors.append("The validated --ledger-file must be the staged text for _bewater/ledger.yaml.")
    if errors:
        print("Draft validation failed; no write plan was emitted.", file=sys.stderr)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    steps = [
        {
            "step_id": "charter-revision",
            "op": "write_new",
            "path": args.artifact_path,
            "new_text": args.artifact_file.read_text(),
        }
    ]
    for step_id, path, expected, text_file in args.cas_step:
        steps.append(
            {
                "step_id": step_id,
                "op": "cas_commit",
                "path": path,
                "expected_revision": int(expected),
                "new_text": Path(text_file).read_text(),
            }
        )
    print(json.dumps({"action_id": args.action_id, "owner": args.owner, "steps": steps}))


if __name__ == "__main__":
    main()
