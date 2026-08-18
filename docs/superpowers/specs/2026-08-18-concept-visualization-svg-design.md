# Concept Visualization → Deterministic SVG Wireframe + HTML Concept Cards

## Status

Approved 2026-08-18. Implements the brainstorm outcome: Idea Seeds stay one-line
text; Concepts must carry a real visual (not a text description). The chosen
medium is a **deterministic SVG wireframe** generated from a structured spec.

## Problem

1. F212's Concept Capture card field ⑧ ("速写草图" / sketch) is a *visual*.
   BeWater's `visualization` is a free-text string describing screens, so the
   F212 fidelity is lost.
2. `_bewater-output/html/artifacts.html` renders the Idea Pool's seed tables
   (they live in the Markdown body) but renders only the Concept Portfolio's
   *summary* — the 30 concept cards' fields live in YAML frontmatter and are
   never projected into readable HTML. A human cannot review/filter concepts in
   the reader.

## Decisions

- **Seed (Idea Pool)**: unchanged. One-line text is correct.
- **Concept**: `visualization` text is retained as the human alt/caption and as
  fallback for legacy data; a new optional structured `visualization_spec`
  drives a deterministic SVG wireframe.
- **SVG is a build-time projection, not stored content.** The artifact stays
  text-only, so CAS integrity, diff, and revision history are unaffected. This
  mirrors the existing Solution precedent
  (`src/bw/solution_contract.py::render_solution_body`).
- **The renderer is defensive**: missing or malformed `visualization_spec`
  yields no SVG; the card falls back to the `visualization` text. The live
  project's 30 concepts are therefore not broken and require no regeneration.

## Schema change

Concept card gains one optional field (documented in
`src/skills/bw-concept-development/references/concept-portfolio-template.md` and
`src/skills/_bw-shared/idea-concept-solution-lifecycle.md`):

```yaml
visualization: "每晚 21:00 手机弹会话；三屏：选题/文案/发布"   # retained: alt/caption + fallback
visualization_spec:                                          # new, optional: SVG input
  screens:
    - caption: "候选选题"
      bullets:
        - "3 个选题，各带一句理由"
        - "点选一个"
    - caption: "确认发布"
      bullets:
        - "顶部倒计时 30:00"
        - "确认发布按钮"
```

New Concepts SHOULD provide `visualization_spec` (instructed by
`bw-concept-development/SKILL.md`). It is intentionally **not** a hard validator
field: adding it to `_CONCEPT_REQUIRED_FIELDS` would flag the live portfolio's
legacy cards as content gaps. Enforcement is a skill principle, not a runtime
rule, consistent with "principles over rules".

## New module: `src/bw/concept_contract.py`

`render_concept_visualization(spec: dict | None, *, caption: str = "") -> str`

- Pure, deterministic, no external deps (stdlib `html.escape` only).
- Default style: a **phone-frame wireframe** (the active project is a mobile
  creator app). Each screen renders as a phone frame; the caption is the frame
  header and each bullet is an annotation row; consecutive screens are joined
  by an arrow.
- Returns `""` when `spec` is `None` or does not parse as
  `{screens: [{caption, bullets[]}]}`. Every output is safe (escaped text).

## HTML reader: `src/bwkit/html.py`

- Add `"concepts"` and `"exit"` to `FRONTMATTER_FIELDS` so `parse_md` carries
  the concept data (it currently whitelists only top-level scalar metadata).
- New `_render_concept_cards(item) -> str`: one `<article class="concept-card">`
  per concept, rendering `id`, `name`, `pithy_description`, `consumer_insight`,
  `commercial_insight`, `idea_definition` (What), `who_its_for` (Who),
  `how_it_works` (How), `what_it_replaces` (What it replaces), `why_big`,
  `design_principles`, `dual_sided` (magic/money/tension/balance), `evaluation`
  (hard/soft), `recommended_action`, `decision`, and the inline SVG wireframe.
- In `render_doc`, for `kind == "concept-portfolio"`, prepend the cards to the
  rendered body so cards lead and the existing summary/decision records follow.
- Add CSS for `.concept-card` and `.concept-wireframe` (responsive grid, phone
  frames, screen arrows).
- Import `render_concept_visualization` from `bw.concept_contract` (bwkit already
  imports `bw.*` elsewhere, e.g. `output_layout_migration.py`).

## Contract and skill updates

- `src/skills/_bw-shared/idea-concept-solution-lifecycle.md` — Concept section:
  document `visualization_spec` and state that the SVG is a deterministic
  projection (same authority posture as the Solution body).
- `src/skills/bw-concept-development/references/concept-portfolio-template.md` —
  add `visualization_spec` to the YAML template.
- `src/skills/bw-concept-development/SKILL.md` — instruct filling
  `visualization_spec` for each Concept.
- Deploy the three skill files to `.claude/skills/` and `.agents/skills/` via
  `install.sh --skills-only` (or equivalent sync).

## Validation and tests

- `tests/test_concept_contract.py`: SVG determinism (same spec → byte-stable
  output), fallback on `None`/malformed spec, caption/bullet escaping, arrow
  between multiple screens.
- `tests/test_bwkit_html.py`: concept-portfolio frontmatter renders concept
  cards (name + fields visible, SVG present when spec present, text fallback
  when spec absent).

## Out of scope

- Funnel/count tightening (Idea Seed confirmation ~5–8/OA and concept-layer
  convergence) — separate follow-up.
- AI-generated PNG sketches — deferred; SVG is the deterministic baseline.
- Regenerating the live `ART-009` cards with `visualization_spec` — requires
  separate authorization per AGENTS.md; legacy cards fall back to text.
