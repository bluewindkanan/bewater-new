# Research persistence plan

All mutation uses one resumable `bwkit plan apply` transaction after deterministic validation. Emit
the immutable Research revision first, optional ledger CAS only when assumptions change, and config
CAS when allocating an artifact ID. Persist revision 1 before executing the first Sprint.

Pass the exact Charter file as `--charter-file`; validation checks `kind: charter`, branch identity,
and the Research Plan's exact pinned `artifact:ART-NNN@n` revision before emitting any step.

For zero projection, before and after ledger texts are identical and the ledger CAS is omitted. A
Sprint transaction writes the next Research revision, real Evidence, and affected ledger revisions
together. Never create `evidence.yaml` before a real finding exists.
