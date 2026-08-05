# Discover Plan

The Discover Plan is the forward-looking planning section of the branch's living `research`
artifact. Revision 1 contains a reviewed Current Discover Plan. A Research Sprint first uses that
snapshot, then writes the next append-only revision of the same artifact ID using `supersedes_ref`.
That next revision carries the updated Current Discover Plan, Latest Research Sprint, and Research
Sprint Debrief. Older revisions preserve history; do not duplicate every prior Sprint in the
current revision.

## Artifact layout

### Current Discover Plan — required sections

1. **Discovery mission and decision** — the core exploration question, provisional proposition,
   research boundary, and the decision this research must inform.
2. **Formal inputs and priorities** — exact Charter and active root-assumption revisions; the
   assumptions, risk priorities, and beliefs to challenge in priority order.
3. **4C coverage map** — the four learning questions, priority, coverage status, and accepted gaps.
4. **Evidence strategy** — `research_mode` (`secondary_only`, `secondary_first`, or `mixed`),
   constraints, evidence targets, evidence limitations, and Primary Triggers. Each new evidence
   record is appended as an entry in `_bewater/evidence.yaml`, preserving `evidence_origin:
   primary | secondary` and `evidence_form: behavior | self-report | expert-judgment | market-data |
   document`.
5. **Research missions** — for each mission: question, evidence need, selected method/framework,
   execution need, rationale, expected output, limitation, owner or dependency, and stop condition.

### Latest Research Sprint — after execution only

Record the reviewed mission, work actually executed, evidence references, deviations from the
Plan, and limitations. Revision 1 has no Latest Research Sprint or Research Sprint Debrief section:
omit them rather than adding empty placeholders.

### Research Sprint Debrief and Plan Delta — after execution only

Record **learned**, **unresolved**, **deepen**, **drop**, and **new questions**. Then choose
`continue`, `deepen`, `synthesize`, or `stop` with a reason and stop rule based on marginal
learning. The Research Debrief records the Plan Delta: which priorities, 4C gaps, evidence
strategy, or missions changed for the next Sprint. It is the decision edge for another Sprint, not
a human Gate.

## Plan self-review

Run one in-context self-review after drafting or changing the Current Discover Plan and before
persistence or execution. Use the same four checks as the brainstorming self-review, adapted to
research:

1. **Placeholder scan** — remove temporary or incomplete placeholders, incomplete required
   sections, and vague mission fields.
2. **Internal consistency** — align the mission and decision with formal inputs, risk priorities,
   4C coverage, evidence need, method, expected output, limitation, and stop condition.
3. **Scope check** — keep the next Sprint bounded and compatible with available time, authority,
   access, owner, and dependency; do not turn Discover into a fixed research programme.
4. **Ambiguity check** — make the evidence need, expected output, limitation, owner/dependency, and
   stop condition unambiguous. Define evidence need before method, and never call an analysis
   framework evidence.

Also confirm that an Initial Assessment, self-report, or model inference remains a candidate rather
than a Fact. Automatically repair a problem when the current context resolves it. Explicit Unknowns
are valid when the Plan names a research path. If an unresolved ambiguity would change the mission,
decision, priority, scope, authority, or resource commitment, ask one question and stop before
writing or executing. The self-review itself produces no artifact, state, signoff, checklist result,
or user confirmation.

Research is flow, not waterfall. Secondary research may be sufficient for Discover, but its
limitations and unresolved validation needs remain visible. Do not wait for every possible fact;
do not hide an evidence gap by calling it resolved. The toolkit is a seed library, not a whitelist:
an ad-hoc method records why selected, what it cannot prove, and is not automatically promoted.
