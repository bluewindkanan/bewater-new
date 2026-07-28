import argparse, sys

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bw", description="bewater decision-phase deterministic runtime")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="scaffold _bewater/")
    sub.add_parser("ledger", help="assumption ledger add/update/validate/trace/backtrack/baseline")
    sub.add_parser("validate", help="check ledger + artifacts (invariants, refs, dual-sided, acyclic)")
    sub.add_parser("hash", help="content-hash an artifact; refresh dependency hashes")
    sub.add_parser("gate-scan", help="compute gate evidence pass/fail (G1)")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    print(f"bw: '{args.cmd}' not yet implemented")  # replaced task-by-task
    return 0

if __name__ == "__main__":
    sys.exit(main())
