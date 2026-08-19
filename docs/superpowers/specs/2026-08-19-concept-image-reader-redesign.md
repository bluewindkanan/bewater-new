# Concept Image Pipeline and Artifacts Reader Redesign

## Status

Approved in chat on 2026-08-19. This document records the approved design
before implementation. The implementation remains bounded to the derived
Artifacts HTML reader and selected Concept image projection; it does not alter
Artifact Markdown, lifecycle state, or `_bewater/` state.

## Problem

The current Concept Portfolio reader renders a deterministic phone-frame SVG
from a long free-text `visualization` field. The SVG displays only one
truncated bullet, so it is not a useful concept visual. The current page also
renders a wide comparison table followed by a full, expanded card for every
Concept. The active portfolio is therefore difficult to compare on desktop,
uncomfortable on mobile, and unnecessarily long.

## Goals and non-goals

Goals:

- Generate useful product concept storyboards for the human-selected Concepts.
- Prefer GPT Image 2 for raster generation and use a language-model SVG as the
  fallback when GPT Image 2 is unavailable.
- Keep HTML builds cacheable, resilient to missing credentials, and safe for
  local/offline reuse after assets exist.
- Make the Artifacts reader comfortable for desktop decision review while
  keeping mobile content readable without page-level horizontal scrolling.
- Preserve canonical Artifact content and existing revision/lineage behavior.

Non-goals:

- No writes to `_bewater/` or manual edits to Artifact Markdown.
- No lifecycle, gate, or Concept schema change.
- No image generation for unselected or historical Concepts in the first
  implementation.
- No replacement of the single `artifacts.html` delivery with a multi-page
  application.

## Decisions

### Selection and generation

The only source of image selection is the current Concept Portfolio's
`exit.selected_concept_ids`. The current case selects CI-001, CI-010, CI-019,
and CI-021. A Concept that is absent from that list is not sent to an image
model, even if it has `decision: selected` elsewhere.

Each selected Concept is represented by a prompt assembled from its name,
pithy description, Who/What/How fields, `visualization`, design principles,
and Money/Magic/tension content. The prompt requests a 16:9 product concept
storyboard with two or three interface states, a restrained BeWater palette,
and minimal large text or numbered panels. Full Chinese explanations remain
in HTML because small generated text is unreliable.

The primary call uses the Image API with `gpt-image-2`, 1536×1024, medium
quality, and WebP output. A content hash includes the normalized Concept
inputs, model, size, quality, and prompt version. A cache hit does not call the
API. Assets are stored under `_bewater-output/html/assets/concepts/` and are
referenced from HTML by relative paths.

If the GPT Image 2 call fails, the fallback uses the Responses API with
`gpt-5.6-terra` and a strict request for a single SVG payload. The SVG is
accepted only after XML parsing and safety validation. The validator rejects
DOCTYPE, scripts, `foreignObject`, event attributes, animations, external
URLs, and oversized output. The asset is written only after validation.

Calls are sequential. 429 and 5xx responses may be retried once, respecting
`Retry-After`; other errors proceed directly to the fallback. The API key is
read only from `OPENAI_API_KEY` and is never logged.

### Cache and failure behavior

A manifest records the Artifact revision, Concept ID, content hash, prompt
version, model, output format, timestamp, file path, and status. Manifest and
asset writes use temporary files followed by atomic replacement. Old assets
are retained; no automatic deletion is performed.

If both models fail, an existing asset for the same Concept may be used as
`stale`. If no asset exists, HTML displays the original `visualization` text
and a visible “image not generated” status. The build continues successfully
and reports per-Concept warnings plus a summary of generated, cached, SVG,
stale, and missing results. A build with complete cache can run without a
network or API key.

### Artifacts reader information architecture

The existing single-file reader and left-side case navigation remain. The
Artifacts reader gains a page-kind marker so its layout changes do not alter
the Knowledge reader unintentionally.

Normal prose uses a comfortable 720–760px measure. Decision views can use a
maximum width near 1180px. Header whitespace is reduced and typography,
status pills, tables, callouts, and paragraph rhythm are made consistent.

The Concept Portfolio view is ordered as:

1. Overview and review status.
2. OA-grouped candidate comparison.
3. Selected Concept deep dives.
4. Collapsed Artifact source and decision records.

Candidate comparison uses responsive rows/cards rather than a six-column table
that is forced into a phone viewport. It shows Concept identity, mechanism,
Consumer Magic, Commercial Money, and Reviewer result. Filters remain
read-only and operate on OA, review recommendation, and decision state.

All candidate details remain accessible, but unselected details are collapsed
by default. Selected Concepts are placed first and expanded by default. Each
selected deep dive prioritizes the storyboard, thesis, Who/What/How, Money,
Magic, and tension. Principles, evaluation, assumptions, evidence, and the
raw Markdown record are secondary collapsible content. The original
`visualization` remains the figure caption.

The Idea Pool and Concept Portfolio structured views appear before their raw
Markdown body. The raw body is collapsed to avoid repeating the same facts,
while remaining available for audit and context.

### Interfaces

The existing `python -m bwkit html [root]` command remains the public entry
point. `build_html()` gains image-generation report fields but still returns
success when image generation is unavailable and HTML itself is written.

The image implementation exposes an injectable client boundary for tests:

```text
ensure_concept_images(root, portfolio) -> ImageBuildReport
ImageBuildReport.assets: concept_id -> AssetRef
ImageBuildReport.generated, cached, svg_fallback, stale, missing, warnings
```

The HTML renderer accepts the asset map as optional context, so existing unit
callers that do not provide images remain valid. No Artifact metadata is
mutated to carry derived asset paths.

## Failure modes and safety

- Missing `OPENAI_API_KEY`: skip network calls, use cache if available, and
  otherwise emit a missing-image warning.
- Organization verification or model-access failure: use the SVG fallback,
  then stale/text fallback.
- Rate limit or transient server error: one bounded retry, then fallback.
- Invalid or unsafe SVG: discard it and report a fallback warning.
- Missing selected Concept: render the available selection and report the
  missing ID; do not invent content.
- Missing asset referenced by the manifest: treat the cache as invalid and
  regenerate when credentials are available.

## Validation

Unit tests cover selection, prompt/hash stability, cache hits and invalidation,
mocked GPT Image 2 success, retry behavior, SVG fallback and rejection,
stale/missing behavior, HTML asset bindings, selected/unselected disclosure,
and raw-record folding. The full test suite and coverage target remain at
least 80%.

Visual QA checks the current ART-009 at 1440×1000 and 390×844. Desktop must
support comparison and selected-Concept deep reading. Mobile must have no
page-level horizontal scrolling. The default view must not expand all 26
Concept cards.

## Assumptions

- The current selected set is CI-001, CI-010, CI-019, and CI-021.
- GPT Image 2 and the SVG fallback are both optional at build time; a valid
  `OPENAI_API_KEY` is required only when a cache miss needs generation.
- The current uncommitted HTML/SVG/test changes are user work and must be
  preserved and merged intentionally.
