"""argparse glue over bwkit.cas. Thin router; no business logic."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import cas, integrity


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bwkit", description="bewater narrow helpers (lock, revision CAS)")
    sub = p.add_subparsers(dest="cmd", required=True)

    lock = sub.add_parser("lock", help="single-writer lock")
    lsub = lock.add_subparsers(dest="lock_cmd", required=True)
    a = lsub.add_parser("acquire")
    a.add_argument("root")
    a.add_argument("--owner", required=True)
    a.add_argument("--ttl", type=int, default=3600)
    rel = lsub.add_parser("release")
    rel.add_argument("root")
    rel.add_argument("--owner", required=True)
    st = lsub.add_parser("status")
    st.add_argument("root")

    c = sub.add_parser("cas", help="text-level revision CAS")
    csub = c.add_subparsers(dest="cas_cmd", required=True)
    show = csub.add_parser("show")
    show.add_argument("path")
    com = csub.add_parser("commit")
    com.add_argument("path")
    com.add_argument("--expected", type=int, required=True)

    pl = sub.add_parser("plan", help="action-plan applier (idempotent, resumable)")
    plsub = pl.add_subparsers(dest="plan_cmd", required=True)
    apl = plsub.add_parser("apply")
    apl.add_argument("root")

    check = sub.add_parser("check", help="schema-agnostic integrity checks")
    check_sub = check.add_subparsers(dest="check_cmd", required=True)
    check_sub.add_parser("integrity")
    return p


def main(argv=None, *, _stdin=None) -> int:
    args = build_parser().parse_args(argv)
    stdin = _stdin if _stdin is not None else sys.stdin

    if args.cmd == "lock":
        root = Path(args.root)
        if args.lock_cmd == "acquire":
            info = cas.acquire_lock(root, args.owner, args.ttl)
            print(f"acquired owner={info['owner']} pid={info['pid']}")
            return 0
        if args.lock_cmd == "release":
            cas.release_lock(root, args.owner)
            print("released")
            return 0
        if args.lock_cmd == "status":
            st = cas.lock_status(root)
            print("unlocked" if st is None else f"owner={st['owner']} pid={st['pid']}")
            return 0

    if args.cmd == "cas":
        path = Path(args.path)
        if args.cas_cmd == "show":
            rev = cas.read_revision(path)
            print(f"revision={rev} hash={cas.content_hash(path.read_text())}")
            return 0
        if args.cas_cmd == "commit":
            new_text = stdin.read()
            try:
                r = cas.commit(path, new_text, args.expected)
            except (cas.CasConflict, cas.BadRevisionBump) as e:
                print(f"error: {e}", file=sys.stderr)
                return 1
            print(f"committed revision={r['revision']} hash={r['hash']}")
            return 0

    if args.cmd == "plan":
        from . import applier
        if args.plan_cmd == "apply":
            try:
                plan = json.loads(stdin.read())
                result = applier.apply_plan(Path(args.root), plan)
            except (applier.PlanError, cas.LockError) as e:
                print(f"error: {e}", file=sys.stderr)
                return 1
            print(json.dumps(result))
            return 0 if result["action_status"] == "applied" else 1

    if args.cmd == "check" and args.check_cmd == "integrity":
        payload = json.loads(stdin.read())
        result = integrity.check_artifacts(payload.get("records", []))
        print(json.dumps(result))
        return 0 if result["ok"] else 1
    return 2
