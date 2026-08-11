"""``bw`` — bewater decision-phase deterministic runtime CLI.

Each subcommand parses args, calls the matching ops-layer function, prints a
concise result, and returns an exit code: ``0`` on success / clean state,
``1`` on validation issues or errors. ``gate-scan`` returns ``2`` for an
unimplemented gate (so it reports cleanly rather than crashing).
"""
import argparse
import sys
from pathlib import Path

from . import gate_scan, hashing, ledger_ops, paths, schema, validate
from .errors import ValidationError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bw", description="bewater decision-phase deterministic runtime")
    sub = p.add_subparsers(dest="cmd", required=True)

    # --- ledger ---
    p_ledger = sub.add_parser("ledger", help="assumption ledger add/update/validate/trace/backtrack/baseline")
    lsub = p_ledger.add_subparsers(dest="ledger_cmd", required=True)

    lp = lsub.add_parser("add", help="append a new assumption")
    lp.add_argument("project", nargs="?", default=".", help="project root path")
    lp.add_argument("--statement", required=True)
    lp.add_argument("--layer", required=True, choices=[layer.value for layer in schema.Layer])
    lp.add_argument("--category", required=True, choices=["consumer", "commercial", "technical", "distribution", "regulatory"])
    lp.add_argument("--impact", required=True, choices=["low", "medium", "high"])
    lp.add_argument("--uncertainty", required=True, choices=["low", "medium", "high"])
    lp.add_argument("--branch", required=True)
    lp.add_argument("--evidence-level", default="L1", dest="evidence_level")
    lp.add_argument(
        "--validation-status",
        default="untested",
        choices=[status.value for status in schema.AssumptionValidationStatus],
        dest="validation_status",
    )
    lp.add_argument("--status", default="active", choices=[status.value for status in schema.AssumptionStatus])
    lp.add_argument("--evidence-ref", default="", dest="evidence_ref")
    lp.add_argument("--derived-from", nargs="*", default=[], dest="derived_from")
    lp.add_argument("--affects", nargs="*", default=[])
    lp.add_argument("--id", default=None)

    lp = lsub.add_parser("update", help="apply changes to an assumption")
    lp.add_argument("project", nargs="?", default=".", help="project root path")
    lp.add_argument("id", help="assumption id, e.g. A-001")
    lp.add_argument("--set", action="append", default=[], metavar="KEY=VAL", dest="set_items",
                    help="field override(s); --set statement=... --set status=killed")
    lp.add_argument("--statement")
    lp.add_argument("--layer", choices=[layer.value for layer in schema.Layer])
    lp.add_argument("--category", choices=["consumer", "commercial", "technical", "distribution", "regulatory"])
    lp.add_argument("--impact", choices=["low", "medium", "high"])
    lp.add_argument("--uncertainty", choices=["low", "medium", "high"])
    lp.add_argument("--evidence-level", dest="evidence_level")
    lp.add_argument(
        "--validation-status",
        choices=[status.value for status in schema.AssumptionValidationStatus],
        dest="validation_status",
    )
    lp.add_argument("--status", choices=[status.value for status in schema.AssumptionStatus])
    lp.add_argument("--evidence-ref", dest="evidence_ref")
    lp.add_argument("--branch")
    lp.add_argument("--derived-from", nargs="*", default=None, dest="derived_from")
    lp.add_argument("--affects", nargs="*", default=None)

    lp = lsub.add_parser("validate", help="report invariant violations for one assumption")
    lp.add_argument("project", nargs="?", default=".", help="project root path")
    lp.add_argument("id", help="assumption id, e.g. A-001")

    lp = lsub.add_parser("trace", help="walk the lineage of an assumption")
    lp.add_argument("project", nargs="?", default=".", help="project root path")
    lp.add_argument("id", help="assumption id, e.g. A-001")
    lp.add_argument("--direction", default="upstream", choices=["upstream", "downstream"])

    lp = lsub.add_parser("backtrack", help="route a falsified assumption to its upstream stage")
    lp.add_argument("project", nargs="?", default=".", help="project root path")
    lp.add_argument("id", help="falsified assumption id")

    lp = lsub.add_parser("baseline", help="snapshot state and stamp a gate label")
    lp.add_argument("project", nargs="?", default=".", help="project root path")
    lp.add_argument("--label", default="G2")

    # --- validate ---
    p_val = sub.add_parser("validate", help="check ledger + artifacts (invariants, refs, dual-sided, acyclic)")
    p_val.add_argument("project", nargs="?", default=".", help="project root path")

    # --- hash ---
    p_hash = sub.add_parser("hash", help="content-hash an artifact; refresh dependency hashes")
    p_hash.add_argument("path", help="artifact file to hash")
    hash_mode = p_hash.add_mutually_exclusive_group()
    hash_mode.add_argument("--refresh-deps", action="store_true",
                           help="refresh dependents' last_validated_against hashes")
    hash_mode.add_argument("--stale", action="store_true",
                           help="report whether the given artifact has stale deps")

    # --- gate-scan ---
    p_gate = sub.add_parser("gate-scan", help="compute gate evidence pass/fail (G1)")
    p_gate.add_argument("gate", help="gate label, e.g. G1 or G2")
    p_gate.add_argument("project", nargs="?", default=".", help="project root path")
    p_gate.add_argument("--subject", default=None, help="solution-branch id to scope assumption scoring")

    return p


def _kv_pairs(items: list[str]) -> dict:
    out: dict = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"bw update: --set expects KEY=VAL, got {item!r}")
        k, v = item.split("=", 1)
        out[k.strip()] = v
    return out


# --- subcommand handlers --------------------------------------------------

def _cmd_ledger(args) -> int:
    root = Path(args.project)
    if args.ledger_cmd == "add":
        fields = {
            "id": args.id,
            "statement": args.statement,
            "layer": args.layer,
            "category": args.category,
            "impact": args.impact,
            "uncertainty": args.uncertainty,
            "branch_id": args.branch,
            "evidence_level": args.evidence_level,
            "validation_status": args.validation_status,
            "status": args.status,
            "evidence_refs": [args.evidence_ref] if args.evidence_ref else [],
            "derived_from": args.derived_from,
            "affects": args.affects,
        }
        a = ledger_ops.add(root, fields)
        print(f"bw ledger add: {a.id}  {a.statement}  (layer={a.layer.value}, branch={a.branch_id})")
        return 0

    if args.ledger_cmd == "update":
        changes = _kv_pairs(args.set_items)
        for attr in ("statement", "layer", "category", "impact", "uncertainty",
                     "evidence_level", "validation_status", "status",
                     "evidence_ref", "branch", "derived_from", "affects"):
            val = getattr(args, attr)
            if val is not None:
                if attr == "branch":
                    changes["branch_id"] = val
                elif attr == "evidence_ref":
                    changes["evidence_refs"] = [val] if val else []
                else:
                    changes[attr] = val
        try:
            a = ledger_ops.update(root, args.id, changes)
        except (KeyError, ValidationError) as exc:
            print(f"bw ledger update: {args.id} — {exc}")
            return 1
        print(f"bw ledger update: {a.id} updated")
        return 0

    if args.ledger_cmd == "validate":
        try:
            violations = ledger_ops.validate_one(root, args.id)
        except KeyError:
            print(f"bw ledger validate: {args.id} not found")
            return 1
        if not violations:
            print(f"bw ledger validate: {args.id} OK (no invariant violations)")
            return 0
        for msg in violations:
            print(f"bw ledger validate: {msg}")
        return 1

    if args.ledger_cmd == "trace":
        try:
            order = ledger_ops.trace(root, args.id, direction=args.direction)
        except ValidationError as exc:
            print(f"bw ledger trace: {exc}")
            return 1
        label = "upstream" if args.direction == "upstream" else "downstream"
        if not order:
            print(f"bw ledger trace: {args.id} has no {label} lineage")
        else:
            print(f"bw ledger trace ({label}): " + " -> ".join([args.id, *order]))
        return 0

    if args.ledger_cmd == "backtrack":
        try:
            result = ledger_ops.backtrack(root, args.id)
        except KeyError:
            print(f"bw ledger backtrack: {args.id} not found")
            return 1
        print(f"bw ledger backtrack: {args.id} -> {result.loop_type} loop to {result.depth_target}")
        if result.affected_ids:
            print("  affected: " + ", ".join(result.affected_ids))
        if result.must_repass_gate:
            print(f"  must re-pass gate: {result.must_repass_gate}")
        return 0

    if args.ledger_cmd == "baseline":
        snap = ledger_ops.baseline(root, label=args.label)
        n_assum = len(snap.get("assumptions", {}))
        n_art = len(snap.get("artifacts", {}))
        print(f"bw ledger baseline: stamped {args.label} ({n_assum} assumptions, {n_art} artifacts)")
        return 0

    return 1  # unreachable: subparser is required


def _cmd_validate(args) -> int:
    issues = validate.validate_all(Path(args.project))
    if not issues:
        print(f"bw validate: {Path(args.project).resolve()} clean (no issues)")
        return 0
    print(f"bw validate: {len(issues)} issue(s) in {Path(args.project).resolve()}")
    for iss in issues:
        print(f"  [{iss.kind}] {iss.scope}: {iss.message}")
    return 1


def _cmd_hash(args) -> int:
    artifact = Path(args.path)
    if args.stale:
        root = paths.find_project_root(artifact.parent)
        stale = hashing.is_stale(root, artifact)
        print(f"bw hash: {artifact} is {'STALE' if stale else 'fresh'}")
        return 0
    # Hash the body FIRST so refresh_deps (if requested) captures the NEW hash;
    # doing it in the other order leaves dependents recording the stale hash.
    h = hashing.hash_artifact(artifact)
    print(f"bw hash: {artifact} hash={h}")
    if args.refresh_deps:
        root = paths.find_project_root(artifact.parent)
        hashing.refresh_deps(root, artifact)
        print("  (deps refreshed)")
    return 0


def _cmd_gate_scan(args) -> int:
    root = Path(args.project)
    try:
        result = gate_scan.scan(root, gate=args.gate, subject=args.subject)
    except NotImplementedError:
        print(f"bw gate-scan: {args.gate} not implemented")
        return 2
    print(f"bw gate-scan {args.gate}: allowed exits = {', '.join(result.exit_allowed)}")
    for c in result.criteria:
        flag = "PASS" if c.passed else "FAIL"
        blk = " (blocking)" if (c.blocking and not c.passed) else ""
        note = f"  — {c.note}" if c.note else ""
        print(f"  [{flag}] {c.name}{blk}{note}")
    return 0 if "go" in result.exit_allowed else 1


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "ledger":
        return _cmd_ledger(args)
    if args.cmd == "validate":
        return _cmd_validate(args)
    if args.cmd == "hash":
        return _cmd_hash(args)
    if args.cmd == "gate-scan":
        return _cmd_gate_scan(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
