# Charter review contract

Charter review has distinct responsibilities. No layer upgrades user intent into validation evidence.

## L0 — deterministic draft validation

Before any persistence plan is emitted, run `scripts/validate_draft.py` against the staged Charter.
It fails closed when any of these are missing or invalid:

- Charter frontmatter and required body sections;
- complete Magic/Money statements, draft/unvalidated status, and empty signoffs;
- an Intent trace table whose claims use only `user-stated`, `user-selected`,
  `agent-interpretation`, or `unknown` provenance labels;
- a complete project definition covering challenge, intent and outcome, scope, constraints, and
  success definition;
- a Current knowledge state that preserves explicit Unknowns.

L0 only checks document consistency. It does not determine whether the user's intent is
accurate, whether a claim is true, or whether evidence is strong enough for a Gate.

## L1 — same-context semantic audit

The capability checks claim traceability, frontmatter/body contradictions, scope drift,
Known/Believed/Unknown classification, and gaps in the project definition. Record each material
finding as `claim → issue → correction or explicit Unknown`; revise it, then run L0 + L1 again. L1 is a same-context draft
audit, not evidence that the user agrees or that the claim is true.

## L2 — final unified intent calibration

Show a compact source-labelled 4–7 claim mirror and ask which claim is least accurate or needs the
user's own words. It consolidates high-impact `user-selected` and `agent-interpretation` claims,
while retaining `user-stated` and `unknown` labels. Apply a correction before the final L0/L1 loop.
This is an intent correction, not a signoff, not an approval, and not a Gate. Once the final L0/L1
loop passes, persist immediately; do not request a save confirmation.

## L3 — reality checking

Initial Assessment may reality-check the Charter for the user; Discover owns Research Planning,
Evidence, and selective assumption projection. A
Charter remains `draft` and `unvalidated` regardless of passing L0 or L1.
