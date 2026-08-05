from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-id", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--artifact-path", required=True)
    parser.add_argument("--artifact-file", type=Path, required=True)
    parser.add_argument(
        "--cas-step",
        nargs=4,
        action="append",
        default=[],
        metavar=("STEP_ID", "PATH", "EXPECTED_REVISION", "TEXT_FILE"),
    )
    args = parser.parse_args()

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
