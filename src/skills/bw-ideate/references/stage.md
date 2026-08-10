# Ideate stage

Ideate runs an explicit concept lifecycle. Each opportunity area is diverged
into a `concept-seed-pool` (10–15 seeds); the human-confirmed seeds become
formal Concept Items in a single `concept-portfolio`, which is evaluated and
converged to a 2–4 selected handoff.

## Lifecycle

```
seeded -> shortlisted -> developed -> evaluated
                              ^            |
                              |            v
                       needs-revision <----+
                              |
                selected / killed / merged  (human only)
```

The AI proposes transitions and writes evaluation evidence; only the accountable
human records `selected`, `killed`, or `merged`. After two failed AI revision
proposals on one concept, the recommended action becomes `recycle-to-OA`, which
stops and routes through bw-backtrack (it never edits an OA or bypasses G1).

## Capabilities to route to

- **bw-concept-seed** — diverge 10–15 seeds per opportunity area (stable,
  pool-local `CS-` ids), cluster near-duplicates, keep every seed visible, and
  recommend a shortlist; stop for the human to confirm it.
- **bw-concept-development** — develop confirmed seeds into Concept Items
  (`CI-` ids) inside the portfolio, run hard/soft criteria and a bounded
  revision loop, then present one batch convergence view and stop before the
  human `select / revise / merge / kill` decision.

## Handoff to Shape (readiness check, no gate)

- the `concept-portfolio` carries 2–4 `selected` Concept Items
  (`exit.selected_concept_ids`), each with hard criteria passing;
- ≥2 provoke healthy anxiety (human judgment);
- all pass the locked-strategy filter.

Hand the exact portfolio revision to Shape (bw-shape router). Shape consumes the
portfolio and produces `solution` artifacts; it does not reselect concepts.
Lifecycle contract: `../_bw-shared/concept-lifecycle.md`.
