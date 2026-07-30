"""CLI for eval harness: run scenarios by skill or all (spec §11.1)."""
from __future__ import annotations

import argparse
from pathlib import Path

from evals._harness import orchestrator


def _parse_args():
    parser = argparse.ArgumentParser(description="Run BeWater eval harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run eval scenarios")
    run_parser.add_argument("--skill", required=True, help="Skill name to test")
    run_parser.add_argument("--mode", choices=["red", "green"], default="green",
                           help="Evaluation mode")
    run_parser.add_argument("--rep", type=int, default=None,
                           help="Repetition count (overrides manifest)")
    run_parser.add_argument("--all", dest="all_skills", action="store_true",
                           help="Run all skills (ignores --skill)")
    run_parser.add_argument("--model", default=None, help="Model name")

    return parser.parse_args()


def _print_summary(summary: dict) -> None:
    """Print a compact summary of eval results."""
    mode = summary.get("mode", "unknown")
    if summary.get("total_skills") is not None:
        # All-skills summary
        print(f"Mode: {mode}")
        print(f"Skills: {summary['total_skills']}")
        print(f"Scenarios: {summary['total_scenarios']}")
        print(f"Reps: {summary['total_reps']}")
    else:
        # Single-skill summary
        skill = summary.get("skill_name", "unknown")
        print(f"Skill: {skill}")
        print(f"Mode: {mode}")
        print(f"Scenarios: {summary['total_scenarios']}")
        print(f"Reps: {summary['total_reps']}")

    # Count verdicts
    results = summary.get("results", [])
    green = sum(1 for r in results if r.get("verdict") == "green")
    red = sum(1 for r in results if r.get("verdict") == "red")
    review = sum(1 for r in results if r.get("verdict") == "needs-review")
    print(f"Verdicts: GREEN={green}, RED={red}, NEEDS-REVIEW={review}")


def main():
    args = _parse_args()

    # Determine paths
    repo = Path.cwd()
    eval_root = repo

    if args.command == "run":
        if args.all_skills:
            summary = orchestrator.run_all(
                eval_root, repo, mode=args.mode, reps=args.rep, model=args.model
            )
        else:
            summary = orchestrator.run_skill(
                eval_root, repo, args.skill, mode=args.mode, reps=args.rep, model=args.model
            )
        _print_summary(summary)


if __name__ == "__main__":
    main()
