---
contract_id: bw-ledger-schema
contract_version: 1
---

# BeWater State Schema (authoritative)

Use this shared contract for state fields and reference formats.

## ID prefixes (stable, never reused)
BR-001 branch · A-001 assumption · ART-001 artifact · EXP-001 experiment ·
D-001 decision · B-001 baseline · BT-001 backtrack · ACT-001 action ·
C-001 condition · E-001 evidence.

## Typed references
artifact:ART-001@3 · assumption:A-001@4 · experiment:EXP-001@2 ·
evidence:E-001@1 · gate:D-001 · baseline:B-001. The `@n` pins a mutable
record revision; gate/baseline refs are immutable (no `@n`).

## supersedes_ref (two semantics)
(a) self-revision — new revision of the same entity → its predecessor
(`artifact:ART-001@3` supersedes `artifact:ART-001@2`). (b) cross-entity
replacement — a new entity replaces a different entity's revision
(branch-local `assumption:A-002` → `assumption:A-001@4`). Disambiguate by
comparing own ID/type vs the referenced ID/type. `supersedes_handoff_ref`
(action_plan) is the one named exception → the gate decision whose handoff a
Go replaces.

## Versioning models
In-place bump (one file): assumptions (`record_revision`), conditions
(`record_revision`), config/ledger/conditions envelopes (`revision`).
Append-only (new file per revision): artifacts (`ART-001-r3-…`), evidence.
Cross-file versioned, in-file immutable: baselines (`B-002` supersedes
`B-001`), gate decisions (new attempt → new `D-…`).

Every revisioned file carries `schema_version`; a writer declares the
schema_version it supports and fails closed on a higher version.

## config.yaml (selected)
schema_version, revision, next_ids{branch,artifact,experiment,decision,
baseline,backtrack,action,evidence}, active_branch, active_execution_handoff,
branches{BR-nn: status,current_stage,parent_ids,merged_into,gate_due_at,
inherited_assumption_refs, excluded_assumption_refs, inherited_condition_ids,
needs_rebase_refs, active_baselines{G1,G2}}. Branch status: active, merged,
killed, pivoted, deviated. A gate cannot record a decision when its single
accountable person is missing or ambiguous.

## ledger.yaml (assumption record)
record_revision, statement, branch_id, layer{root,strategy,opportunity,
concept,feature}, category{consumer,commercial,technical,distribution,
regulatory}, side{money,magic,both}, impact, uncertainty, evidence_level{L1–L6},
validation_status{untested,testing,supported,falsified,inconclusive},
status{active,killed,merged}, evidence_refs[], derived_from[], supersedes_ref,
risk_history[], l4_obligation_status, history[]. `is_achilles_heel` =
impact=high AND uncertainty=high (derived). An Achilles Heel raises a durable
L4 obligation that survives lowering impact/uncertainty; it closes only with
L4+ validation or evidence-backed human signoff. ledger.yaml also carries the
assumption `next_id` (canonical source for A-NNN).

## conditions.yaml (condition record)
record_revision, origin_decision_id, branch_id, statement, owner, due_at,
status{open,satisfied,waived,cancelled,superseded}, required_evidence,
evidence_refs[], resolution_ref, resolved_at/by, waiver_rationale,
close_reason, close_authority. Edits bump in-place `record_revision` under a
stable C-NNN ID (never a new ID); conditions.yaml also carries the condition
`next_id`. waived hard G2 evidence still does not qualify for Go. cancelled
and superseded require close_reason and close_authority.

## artifact frontmatter (selected)
schema_version, artifact_id, revision, supersedes_ref, kind, stage, branch_id,
document_status{draft,final,superseded}, validation_status{unvalidated,
in-review,validated,invalidated}, dual_sided{magic,money,tension,balance_choice},
derived_from[], signoffs[{person,role,scope,artifact_revision,signed_at}],
stale_reason. final + non-empty body is document-presence only, never
readiness. Artifact files are append-only revisions in the flat output dir:
`ART-001-r3-solution.md` supersedes `ART-001-r2-solution.md`. The resolver
requires exactly one head per revision chain; a duplicate, missing
predecessor, cycle, or two heads is corruption.

## evidence wrapper
evidence_id, revision, supersedes_ref, effect_on_prior{supplements,supersedes,
invalidates}, validity{active,invalidated}, correction_reason, source_type,
captured_at, content_sha256, source_path_or_user_provided_url. Corrections
create the next immutable revision and trigger dependent stale/invalidation.
A user-provided URL is preserved exactly; skills never invent or repair URLs.
