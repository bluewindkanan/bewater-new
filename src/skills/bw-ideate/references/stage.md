# Ideate stage

Ideate runs an explicit concept lifecycle. Each opportunity area is diverged
into a 10–15 Seed hard range, receives a lightweight Idea Pool review, and gets
explicit `recommended_cuts` whose complement is 5–8. The human confirms 5–8
Seeds per OA. Every confirmed Seed becomes one initial Concept in the single
`concept-portfolio`, which receives an independent Concept review before the
human converges it to a global 2–4 selected handoff.

## Lifecycle

```
seeded -> pool-reviewed -> human-confirmed -> developed -> independently-reviewed
                 ^                                  ^                 |
                 |                                  |                 v
           needs-revision                     needs-revision <--------+
                              |
                selected / killed / merged  (human only)
```

The Seed producer performs the lightweight batch check. A fresh-context
independent reviewer owns Concept evaluation evidence and recommendations; only
the accountable human records `selected`, `killed`, or `merged`. After at most
two review-and-revision cycles, unresolved material findings remain
`review.status: needs-revision`. `recycle-to-OA` stops and routes through
bw-backtrack; it never edits an OA or bypasses G1.

## Capabilities to route to

- **bw-concept-seed** — diverge 10–15 seeds per opportunity area (stable,
  pool-local `CS-` ids), cluster near-duplicates, keep every seed visible, and
  run the Idea Pool review; recommend explicit cuts with reason and rationale
  so 5–8 remain; stop for the human to confirm a valid 5–8.
- **bw-concept-development** — develop **all** confirmed seeds into Concept
  Items (`CI-` ids) inside the portfolio, obtain an independent Concept review
  and bounded verification, then present one batch convergence view only when
  `review.status: ready`; stop before the human decision.

## Handoff to Shape (readiness check, no gate)

- the `concept-portfolio` carries 2–4 `selected` Concept Items
  (`exit.selected_concept_ids`), each with hard criteria passing, and a
  new-contract Portfolio has `review.status: ready`;
- ≥2 provoke healthy anxiety (human judgment). Fewer than two is a soft blocker:
  stop, show the count, and require explicit human override before routing to Shape;
- all pass the locked-strategy filter.

Hand the exact portfolio revision to Shape (bw-shape router). Shape consumes the
portfolio and produces `solution` artifacts; it does not reselect concepts.
Legacy Portfolios whose exact Idea Pool uses `shortlist.recommended` remain
readable and are labelled not reviewed; do not infer findings or readiness that
the Artifact does not contain.
Lifecycle contract: `../_bw-shared/idea-concept-solution-lifecycle.md`.
