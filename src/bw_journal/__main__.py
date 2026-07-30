"""``bw-journal`` — CLI entry point.

Commands:
    init        scaffold a new decision journal in CWD
    log         log an assumption with auto-categorization
    status      show a concise snapshot of open assumptions
    diff        show what changed since the last checkpoint

Each command delegates to the ``bw`` runtime underneath.
"""
import argparse
import sys
from pathlib import Path

from . import __version__
from . import commands as cmds


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="bw-journal",
        description="Your personal decision journal — git for decisions.",
    )
    p.add_argument("--version", action="version", version=f"bw-journal {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    # --- init ---
    p_init = sub.add_parser("init", help="scaffold a new decision journal")
    p_init.add_argument("project", nargs="?", default=".", help="journal root directory")

    # --- log ---
    p_log = sub.add_parser("log", help="log a new assumption / decision entry")
    p_log.add_argument("project", nargs="?", default=".", help="journal root directory")
    p_log.add_argument("statement", help="what you are assuming or deciding")
    p_log.add_argument("--impact", choices=["low", "medium", "high"], default="medium")
    p_log.add_argument("--uncertainty", choices=["low", "medium", "high"], default="medium")
    p_log.add_argument("--category", choices=["consumer", "commercial", "technical", "distribution", "regulatory"], default="consumer")
    p_log.add_argument("--side", choices=["magic", "money", "both"], default="both")
    p_log.add_argument("--branch", default="main", help="journal branch label")
    p_log.add_argument("--no-telemetry", action="store_true", help="skip anonymous usage ping")

    # --- status ---
    p_status = sub.add_parser("status", help="show open assumptions summary")
    p_status.add_argument("project", nargs="?", default=".", help="journal root directory")
    p_status.add_argument("--no-telemetry", action="store_true", help="skip anonymous usage ping")

    # --- diff ---
    p_diff = sub.add_parser("diff", help="show changes since last checkpoint")
    p_diff.add_argument("project", nargs="?", default=".", help="journal root directory")

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.cmd == "init":
        return cmds.cmd_init(Path(args.project))

    if args.cmd == "log":
        return cmds.cmd_log(
            project=Path(args.project),
            statement=args.statement,
            impact=args.impact,
            uncertainty=args.uncertainty,
            category=args.category,
            side=args.side,
            branch=args.branch,
            telemetry=not args.no_telemetry,
        )

    if args.cmd == "status":
        return cmds.cmd_status(Path(args.project), telemetry=not args.no_telemetry)

    if args.cmd == "diff":
        return cmds.cmd_diff(Path(args.project))

    return 1


if __name__ == "__main__":
    sys.exit(main())
