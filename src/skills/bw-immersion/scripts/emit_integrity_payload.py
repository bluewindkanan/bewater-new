from __future__ import annotations

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        nargs=3,
        action="append",
        default=[],
        metavar=("ARTIFACT_ID", "REVISION", "SUPERSEDES_REVISION_OR_NULL"),
    )
    args = parser.parse_args()
    records = []
    for artifact_id, revision, supersedes in args.record:
        records.append(
            {
                "id": artifact_id,
                "revision": int(revision),
                "supersedes": None if supersedes == "null" else int(supersedes),
            }
        )
    print(json.dumps({"records": records}))


if __name__ == "__main__":
    main()
