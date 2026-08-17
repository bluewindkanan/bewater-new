# Discover Research Toolkit — Implementation Decision

- **Date**: 2026-08-14
- **Status**: Implemented
- **Scope**: `bw-discovery-research` method/framework routing only

This records the final decisions behind the Discover research toolkit rework. It supersedes the
five earlier drafts listed at the end; those drafts are kept for history and are **not** the
implemented design.

## Decisions

1. **One registry + one routing table, not three libraries.** `research-toolkit.csv` is the single
   registry of methods and frameworks; `method-map.md` is the single routing table. A `kind` column
   (`method` | `framework`) distinguishes the two. The "tool" tier is **not a registry entry**: tools
   are the host's native capabilities used directly at runtime.
2. **Online-only.** The registry holds only methods and frameworks the AI can execute online over
   public sources plus user-provided documents. `run_mode` and `execution_need` were dropped. Live
   field research (interviews, observation, usability with real users) is **out-of-band human work**,
   noted in `method-map.md`, never auto-executed, never reported as AI-executed evidence.
3. **Recommendation, not restriction.** The registry is a seed library (open-world) and the routing
   table is a set of recommended defaults, not a whitelist and not a menu. The model may override any
   cell with a framework or method it knows fits better, recording why selected, what it cannot prove,
   and its limitation. Ad-hoc methods and frameworks are symmetric and are never auto-promoted.
4. **One table for method↔framework matching, not two.** Method and framework are joined by the
   evidence need (the framework consumes the method's evidence), so each routing-table row carries a
   full method→framework bundle.
5. **Portfolio matrices stay out of Discover.** BCG / Ansoff / GE-McKinsey / Portfolio Curation /
   Money∩Magic / 8-criteria scoring belong to Define/Ideate/Shape and are cross-referenced as a
   pointer, not merged. Stages stay independent; there is **no global framework table**.
6. **CSV stays the registry format.** Frameworks carry a compact `dimensions` reminder column (not a
   per-framework document); a short execution contract lives in `method-map.md`.

## Registry schema (15 columns)

`id, kind, layer, methodology_stream, analysis_object, lens_fit, learning_intent, use_when,
avoid_when, evidence_or_output, input_requirements, dimensions, complements, conflicts, key_limitation`

`kind` folds from `layer`: `collection_method`/`validation_method` → `method`;
`analysis_framework`/`synthesis_method` → `framework`.

## Superseded drafts

- `2026-08-13-toolkit-redesign.md`
- `2026-08-13-method-allocation-logic.md`
- `2026-08-14-toolkit-categorization.md`
- `2026-08-14-research-tools-complete.md`
- `2026-08-14-research-means-complete-v2.md`
