# Method Map

This map routes one learning question to the smallest complementary Method Bundle. It is a set of
**recommended defaults, not a whitelist and not a menu to enforce**. The Toolkit
(`research-toolkit.csv`) is a seed library, not a whitelist: it lists proven methods and frameworks
across collection, analysis, validation, and synthesis, but the Coordinator loads it selectively for
each question, never wholesale, and may choose any method or framework it knows — including one not
listed here — when it answers the question better. Never let the table restrict the model's own
framework choice.

## Method, framework, tool

The Toolkit's four layers fold into three tiers, each answering one question:

- **Method** — *how evidence is produced or checked.* `collection_method` obtains evidence;
  `validation_method` checks it. A method earns its place only when it adds an evidence form the
  other methods do not provide.
- **Framework** — *how evidence is interpreted or organized.* `analysis_framework` and
  `synthesis_method` structure, explain, or reframe evidence already in hand. A framework is
  interpretation, never evidence; it never stands in for a collection method. A framework's standard
  dimensions are a reminder in `dimensions`, adaptable to the question — not a required schema.
- **Tool** — *what the host executes.* Tools are the host's native capabilities (web search, browser,
  file read, subagents) used directly at runtime. No tool library and no connector name is baked into
  the registry; the `input_requirements` field names what evidence a method consumes, not which tool
  to call.

Compose in that order and stop when the question is answered: choose the Method that produces or
checks the needed evidence, add a Framework only to interpret that evidence, and let the host tools
run the Method directly. Evidence need precedes all three tiers.

## Classify the question

Before matching, tag each selected learning question with two independent labels:

1. **question_kind** — `question` (an open inquiry) or `hypothesis` (a falsifiable claim that must
   survive disconfirmation).
2. **learning_intent** — one of `explore`, `describe`, `compare`, `explain`, `size`, `forecast`,
   `validate`, `reframe`.

A hypothesis is not just a question: it leads with the falsification layer. Map a hypothesis to
`validate` (or `reframe` when the whole frame is at stake), require at least one `validation_method`
— negative-case or disconfirming search — and, when the belief is a projected root, follow
`root-assumption-projection.md`. An open question leads with collection plus analysis and adds
validation only when its inference generalizes beyond the evidence in hand.

The rubric below maps `learning_intent` to the layers a bundle must lead with, may add, and should
treat as redundant. It is a default lead, not a quota: omit any layer that adds no distinct evidence
form or inference.

| learning_intent | intent answers | lead with | add when | redundant when |
|---|---|---|---|---|
| `explore` | What is out there? | collection | analysis to separate signal from noise | synthesis unless patterns surface |
| `describe` | What is the current state? | collection + analysis | validation to generalize | synthesis unless it reframes |
| `compare` | How do options differ? | collection + analysis (benchmark/positioning) | validation (source-family triangulation) | a second analysis framework on the same evidence |
| `explain` | Why does it happen? | collection + analysis (causal/journey) | validation (alternative-explanation) | synthesis unless the frame shifts |
| `size` | How big is it? | collection + analysis (sizing) | validation (sensitivity) | a second sizing framework on the same proxies |
| `forecast` | What is likely next? | collection + analysis (trend/scenario) | validation | synthesis unless signals collide into a reframe |
| `validate` | Is this claim true? | validation (negative-case + source-family) | collection only to obtain the evidence being checked | analysis frameworks that restate the claim |
| `reframe` | What is the better frame? | synthesis + validation on the prior frame | collection only if the new frame needs fresh evidence | analysis frameworks that re-derive the old frame |

## Selection sequence

For each selected learning question, classify it (above), then work top-down and stop as soon as the
bundle answers it:

1. **learning question** — the decision-relevant objective, drawn from the Learning Plan.
2. **learning intent** — explore, describe, compare, explain, size, forecast, validate, or reframe.
3. **desired evidence or inference** — the evidence form or inference that would actually move the
   strategic choice. Evidence need precedes method selection.
4. **smallest complementary Method Bundle** — the fewest methods and frameworks, across collection,
   analysis, validation, and synthesis, that together produce that evidence or inference. Use the
   routing table below as a **starting recommendation**, then override freely.
5. **tools** — host-native tools run the methods directly; no tool registry is consulted.
6. **evidence and limitations** — record what each method contributes and what it cannot prove.
7. **Sprint synthesis** — fold the bundle's outputs into patterns, tensions, anomalies, belief
   shifts, and reframe candidates for the Sprint Synthesis.

An analysis framework is interpretation, not evidence; choose it only to organize or challenge
evidence already in hand.

## Routing table — recommended defaults

Each row is a **recommended default bundle, not a requirement**. The Coordinator may override any
cell — replacing, dropping, or adding a method or framework the model knows fits better — as long as
the composition rules below hold and the override is recorded.

| question_type (analysis_object × learning_intent) | collection (method) | analysis (framework) | validation (method) | synthesis (framework) |
|---|---|---|---|---|
| external.industry × explain/compare | desk-document-research + company-product-competitor-audit | five-forces + strategic-group-analysis | source-family-triangulation | — |
| external.environment × forecast/explain | literature-patent-standards-regulatory-search + trend-weak-signal-structural | pestel + trend-weak-signal-structural | — | — |
| external.market × size | literature-patent-standards-regulatory-search + behavioral-transaction-data-review | market-sizing-triangulation | sensitivity-boundary-check | — |
| consumer (external.market) × explain/explore | social-review-discourse-analysis (+ user-provided notes) | jtbd-journey + segmentation-decision-unit | evidence-strength-transferability | tension-finding |
| internal.economics × explain | internal-document-data-review + pricing-unit-economics | pricing-unit-economics | sensitivity-boundary-check | — |
| hypothesis × validate | targeted collection | — | negative-case-disconfirming-search + alternative-explanation-testing | — |

The method-to-framework pairing lives inside each row — the framework consumes the evidence the
method produced — so method and framework are one table, not two.

## Composition rules

Only these four are constraints; everything else in the map is a recommendation:

1. **Evidence need precedes method selection.** Define the evidence that would move the choice
   before choosing any method or framework.
2. **A framework is interpretation, not evidence.** It cannot stand in for a collection method, and
   it must not be treated as a newly gathered fact.
3. **Smallest complementary, no redundancy.** Select the fewest methods and frameworks that add a
   distinct evidence form, perspective, inference, challenge, or synthesis operation. Omit any layer
   that adds no value; do not require exactly one method from every layer. Reject redundant
   frameworks that consume the same evidence to make the same inference (see `conflicts` on each
   Toolkit row; e.g. `five-forces` and `value-chain-profit-pool` both describe industry structure
   from the same evidence).
4. **Open-world override, recorded.** The Coordinator may use any method or framework — from its own
   knowledge or outside the Toolkit — when it fits the question better. Record why selected, the
   evidence it should yield, what it cannot prove, and its key limitation. An ad-hoc method or
   ad-hoc framework is allowed the same way and is not automatically promoted into the Toolkit.

Validity-relevant limitations are persisted in the Research artifact; the rest is transient.

## Framework execution — one breath

To execute a framework from evidence: (1) read its `dimensions` as a reminder and adapt them to the
question; (2) fill each dimension with evidence plus an exact source reference; (3) record a
limitation for any dimension the evidence cannot fill — leave the gap visible, never fabricate;
(4) state the aggregate conclusion with confidence. Keep the detailed framework output in a Source
file only when it improves auditability; the Knowledge workpaper summarizes.

## Out-of-band and out-of-scope

- **Offline field research** — live interviews, field observation (AEIOU, immersion, shop-along),
  usability or experiment with real users — is **out-of-band human work**, not part of this online
  toolkit. User-provided documents (interview notes, internal reports) enter as optional context
  sources; the human's live field work itself is never auto-executed and is never reported as
  AI-executed evidence. Its absence is a recorded limitation, not a blocking stage.
- **Portfolio and strategy matrices** — BCG, Ansoff, GE-McKinsey, Portfolio Curation, and the
  Money∩Magic / 8-criteria scoring — belong to Define/Ideate/Shape (see `bw-ideate`, `bw-shape`),
  not to Discover research. Discover references them as downstream tools; it does not apply them.

## Bundle examples (illustrative, not recipes)

These illustrate complementary selection and redundancy avoidance. They are defaults, not
requirements.

- **Industry structure:** `desk-document-research` + `company-product-competitor-audit` (collection),
  `five-forces` (analysis), `source-family-triangulation` (validation). A redundant addition is
  `value-chain-profit-pool` when the question is only industry structure — it restates structure from
  the same evidence.
- **Consumer unmet need:** `social-review-discourse-analysis` + user-provided notes (collection),
  `jtbd-journey` (analysis), `evidence-strength-transferability` (validation), `tension-finding`
  (synthesis if competing needs collide).
- **Market size and economics:** `market-sizing-triangulation` (analysis) with
  `sensitivity-boundary-check` (validation); a second sizing framework on the same proxies adds no
  new inference.
- **Macro environment:** `literature-patent-standards-regulatory-search` (collection) + `pestel`
  (analysis) + `trend-weak-signal-structural` (analysis) for forward uncertainty.

## Bundles revise with the question

A Method Bundle is for one Sprint. When the Sprint Synthesis changes the question — a belief shift,
a contradiction, a reframe — the next Sprint recomposes the bundle from the question's new evidence
need, not from the previous Sprint's method list.
