# Research persistence plan

All canonical Sprint mutation uses one validated, resumable `bwkit plan apply` action. Always pass
the repository as `--project-root`; omission is invalid. Prepare
candidate UTF-8 state files in a caller-supplied `mktemp` directory. Host tools prepare Source bytes
separately under `_bewater-output/sources/`; the emitter validates their paths and SHA-256 through the
Knowledge validator but emits no Source step and never decodes binary material as text.

Validate the complete candidate state before emitting:

1. the exact current Research head and immutable successor;
2. every new or revised stable-path Knowledge workpaper, including Source digests, branch, authorizing
   Research revision, exact Learning refs, current synthesis closure, and required content;
3. Research Progress against the candidate current Knowledge revisions;
4. optional Evidence and Ledger state when a decision-critical claim changes;
5. config allocation from `next_ids.knowledge` only for new K IDs.

Emit steps in recovery order: new Knowledge `write_new` and Knowledge CAS revisions first; the new
Research Artifact `write_new` next; optional Evidence and Ledger CAS steps after it; config CAS last
when IDs were allocated. A later K revision uses CAS on exactly the same path and does not advance the
counter. Evidence and Ledger steps are omitted when no decision-critical claim changes.

This order intentionally permits a temporary Knowledge/Research head mismatch after interruption.
Retry the identical action: already-applied identical steps skip, then the missing Research revision
and counter complete. An occupied new-K path with identical bytes is the same resumable allocation;
different bytes fail closed. A stale config revision, stale Research head, stale K CAS, missing ref,
branch mismatch, Source mismatch, or `RM-NNN` in a typed ref emits no plan.

Never persist `config-after-sprint*.yaml`, another staged candidate, a CAS backup, or any Source file
as canonical project state. Git owns historical Knowledge text; CAS backups are short-term recovery
only.
