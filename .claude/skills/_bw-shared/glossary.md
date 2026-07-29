---
contract_id: bw-glossary
contract_version: 1
source_sections: spec §0–§8
---

# BeWater Glossary (authoritative)

- **Decision phase**: Immersion → Discover → Define → G1 → Ideate → Shape → G2 → execution handoff.
- **G1 / Strategy Gate**: convergence gate after Define; product-owner authority.
- **G2 / Concept Gate**: investment gate after Shape; investment-decision authority.
- **Money + Magic**: dual-sided reasoning (commercial leverage vs consumer value).
- **Assumption ledger**: revisioned record of assumptions with evidence levels.
- **Evidence level (L1–L6)**: must point to evidence, not be asserted. L4+ = behavioral.
- **Achilles Heel**: assumption with impact=high AND uncertainty=high → durable L4 obligation.
- **Baseline**: immutable snapshot created by a Go; governs loop size (touching it = large loop).
- **Execution handoff**: derived output of a G2 Go; one active per project.
- **Conditional Go**: bounded gap with conditions; mandatory closeout before the next gate.
- **Five exits**: Go, Conditional Go, Recycle, Pivot, Kill (§6.4).
- **Direct-write protocol**: §5.7 — announce, single-writer lock, read, backup, modify, CAS check, bump, diff, verify.
- **bwkit**: narrow stdlib-only helper (single-writer lock + revision CAS); no gate authority (§12). Invoked as `python -m bwkit` (tool repo) or via `_bw-shared/bwkit/` (installed).
- **Contract reference**: a shared file under `_bw-shared/` with contract_id/contract_version (§2.3).
- **revision vs record_revision**: file-level envelope `revision` vs per-record `record_revision` (assumption/condition). bwkit's CAS bumps via the caller; bwkit verifies.
