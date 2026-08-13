# Method Bundles

A Method Bundle is the small complementary set of Toolkit methods the Coordinator composes for one
learning question in one Sprint. The Toolkit (`research-toolkit.csv`) is a seed library, not a
whitelist: it lists proven methods across collection, analysis, validation, and synthesis, but the
Coordinator must load the toolkit selectively for each question, never wholesale. The seed library
grows the available option space; it does not auto-fill a Sprint.

## Selection sequence

For each selected learning question, work top-down and stop as soon as the bundle answers it:

1. **learning question** — the decision-relevant objective, drawn from the Learning Plan.
2. **learning intent** — explore, describe, compare, explain, size, forecast, validate, or reframe.
3. **desired evidence or inference** — the evidence form or inference that would actually move the
   strategic choice.
4. **smallest complementary Method Bundle** — the fewest methods, across collection, analysis,
   validation, and synthesis, that together produce that evidence or inference.
5. **available execution tools** — the Coordinator resolves each method's `execution_need` against
   tools actually available in the current host; no method registry hardcodes a connector name.
6. **evidence and limitations** — record what each method contributes and what it cannot prove.
7. **Sprint synthesis** — fold the bundle's outputs into patterns, tensions, anomalies, belief
   shifts, and reframe candidates for the Sprint Synthesis.

Evidence need precedes method selection. An analysis framework is interpretation, not evidence;
choose it only to organize or challenge evidence already in hand.

## Composition rules

- Select the **smallest complementary** set. A method earns its place by adding a distinct evidence
  form, perspective, inference, challenge, or synthesis operation that the other methods do not
  provide.
- **Omit any layer that adds no value.** A question may need only collection, only analysis plus
  validation, or only synthesis on prior evidence. Do not require exactly one method from every
  layer.
- **Reject redundant** frameworks that consume the same evidence to make the same inference. Two
  positioning maps from the same competitor page count as one, not two.
- Record, for the bundle, each method's contribution and key limitation, plus any access fallback
  used. Validity-relevant limitations are persisted in the Research artifact; the rest is transient.
- The Coordinator resolves `execution_need against tools available in the current host`. It picks the
  concrete tool (document store, internal system, interview channel, data pipeline, verification
  pass) from what the host actually provides, not from a name baked into the registry.

## Ad-hoc methods

A learning question may need a method the seed library does not list. An ad-hoc method is allowed
only when the Research Plan records why selected, the evidence it should yield, what it cannot
prove, its key limitation, and its execution need. An ad-hoc method is **not automatically**
promoted into the Toolkit; it stays a local, validity-relevant choice until a later review decides
otherwise.

## Bundle examples (non-prescriptive)

These examples illustrate complementary selection and redundancy avoidance. They are not recipes and
do not require exactly one method from every layer.

### Broad industry orientation

- collection: `desk-document-research` plus `internal-document-data-review` for existing context;
- analysis: `trend-weak-signal-structural` to separate signal from noise;
- synthesis: `pattern-anomaly-detection` to surface where the consensus story frays.

Why complementary: documents establish context, the structural trend lens separates cyclical from
durable change, and pattern detection surfaces weak signals worth a follow-up Sprint. A redundant
addition would be a full `five-forces` here — it consumes the same public documents to restate
industry structure the trend scan already covers. Add it only when industry structure is itself the
question.

### Customer behavior and unmet need

- collection: `stakeholder-expert-consumer-interviews` and
  `contextual-observation-diary-intercept-survey` for stated and observed behavior;
- analysis: `jtbd-journey` to interpret progress, friction, and unmet need;
- validation: `evidence-strength-transferability` before generalizing beyond the small sample.

Why complementary: self-report and observation cross-check each other, JTBD organizes both into
unmet progress, and transferability checks stop a vivid interview from becoming an over-broad claim.
A redundant addition would be `journey` mapping as a second framework beside JTBD — they draw the
same touchpoint evidence and answer the same question, so one suffices.

### Competitive and value-chain structure

- collection: `company-product-competitor-audit` of visible offers;
- analysis: `competitive-benchmarking-positioning` and `value-chain-profit-pool`;
- validation: `source-family-triangulation` so repeated pages from one analyst count as one source.

Why complementary: the audit supplies the raw offer data, positioning interprets differentiation, the
value chain locates where profit actually accrues, and triangulation keeps the structure claim
honest. A redundant addition would be `five-forces` as well as `value-chain-profit-pool` when the
question is specifically where value is captured — both describe industry structure and would lean on
the same evidence.

### Market sizing and economics

- collection: `literature-patent-standards-regulatory-search` and `behavioral-transaction-data-review`
  for category and proxy data;
- analysis: `market-sizing-triangulation` and `pricing-unit-economics`;
- validation: `sensitivity-boundary-check` on the key volume and cost assumptions.

Why complementary: triangulation converges a sized estimate from independent angles, unit economics
checks whether the size converts to profit, and sensitivity exposes which assumption drives the
number. A redundant addition would be a second sizing framework on the same proxy data — if the
evidence is identical, a different model does not add a new inference.

### Emerging technology, regulation, and future signals

- collection: `literature-patent-standards-regulatory-search`;
- analysis: `technology-maturity-capability` and `scenario-analogy-causal`;
- synthesis: `structural-reframe-generation` when the signals collide.

Why complementary: the search assembles evidence across literature, patent, and regulatory records,
maturity maps what is technically possible, scenarios hold multiple futures open rather than picking
one, and reframe generation turns a collision of lenses into a candidate reframe. A redundant
addition would be `trend-weak-signal-structural` alongside `scenario-analogy-causal` when both serve
only to restate the same forward uncertainty — keep them only if each changes the inference.

### Validating whether a cost advantage becomes customer value

- collection: `usability-demo-experiment-poc` and `social-review-discourse-analysis` for observed
  and stated response to price and value;
- analysis: `pricing-unit-economics` for the cost-to-price gap;
- validation: `alternative-explanation-testing` to separate price-driven adoption from confounders;
- synthesis: `tension-finding` if the cost story and the customer-value story diverge.

Why complementary: demos and discourse show how customers actually respond, unit economics states
whether the cost gap survives pricing, alternative-explanation testing rules out confounders, and
tension finding preserves the gap if the two stories collide. A redundant addition would be
`market-sizing-triangulation` here — it answers how big the prize is, not whether customers value
the advantage, so it adds no inference to this specific question.

## Bundles revise with the question

A Method Bundle is for one Sprint. When the Sprint Synthesis changes the question — a belief shift,
a contradiction, a reframe — the next Sprint recomposes the bundle from the question's new evidence
need, not from the previous Sprint's method list.
