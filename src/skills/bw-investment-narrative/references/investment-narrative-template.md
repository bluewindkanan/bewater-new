# Investment-narrative template

The narrative is the shell the investment-decision level reads at G2. It wraps
one or two complete validated Solutions and never fills gaps that belong in
canonical Solution frontmatter. Goal: “make it impossible not to invest.” File:
`_bewater-output/ART-xxx-rN-investment-narrative.md` (append-only).

## The six parts

1. **Brief** — one-paragraph framing.
2. **Opportunity** — the consumer situation + desire (Magic) and the commercial opening (Money).
3. **Solution** — the complete validated dual-sided Solution; present its
   Definition/Dimensions, How It Works, How To Implement, How It Makes Money,
   and Validation without recreating canonical content.
4. **Why big** — the prize; why this is large.
5. **Financial Case** — sourced assumptions only (below).
6. **Roadmap** — phased plan (Exploratory → Product Design → Ops → Business Rules → Development →
   Pilot → Roll Out → Marketing), each phase with OBJECTIVE + Jobs To Be Done.

## Financial case — every assumption tagged with source + logic

Required lines, each citing a source and reasoning: user count · retention · pricing · adoption rate
· penetration · **CAC** · cost · year-by-year P&L · profitability timing. (Reference points: project
counts from comparable crowdfunding; success rate from industry ~36%.) Tie each to a ledger
assumption via `evidence_refs`; never assert a number without a source.

## Artifact frontmatter (kind: investment-narrative)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: investment-narrative
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition: {statement: "", evidence_refs: []}
    consumer_target: {statement: "", evidence_refs: []}
  money:
    commercial_value_proposition: {statement: "", evidence_refs: []}
    leverageable_assets: {statement: "", evidence_refs: []}
  tension: {statement: ""}
  balance_choice: ""
financial_assumption_refs: []   # ledger assumptions backing the Financial Case
derived_from: []                # the validated solution(s)
signoffs: []
stale_reason: null
```

Field semantics: `../_bw-shared/ledger-schema.md`.
