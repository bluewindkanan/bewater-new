# Charter interaction and review rubric

Use this rubric when reviewing saved interactive transcripts. Run each scenario three times and
record `pass` or `fail` for every assertion; `needs-review` is not evidence of a passing behavior.

| Dimension | Pass condition |
| --- | --- |
| Conversational focus | Each turn is clear, focused, and natural: it helps the user see the current most worthwhile point to think about and leads into the next step. When the question is complex, it supplies enough context, reasoning, or comparison to advance shared understanding. |
| Explore | Before all grounding anchors are collected or explicitly Unknown, the assistant stays open-ended and offers no recommended or structured option. It uses mirroring or a clearly-labelled sensemaking observation when that helps the user understand the emerging situation. |
| Explore challenge | When it sees ambiguity, an implicit assumption, opinion without behavior, or a contradiction, the assistant can name the relevant tension gently as `agent-interpretation` and invite reflection, helping the user develop their own view. |
| Converge | A recommendation is restricted to a bounded decision and serves as an aid to thinking, not an answer. It provides the context needed to see what it optimizes and sacrifices, identifies an Unknown that would change it, and retains a credible alternative, Uncertain, and Other route. |
| Provenance | User wording is `user-stated`; accepted options remain `user-selected`; synthesis is `agent-interpretation`; absence of knowledge is `unknown`. |
| Review | L0 blocks deterministic draft defects. L1 checks semantic consistency and causal-chain exits. After any revision, both run again. |
| Intent calibration (L2) | After the draft and L0/L1 review, high-impact selected or interpreted claims are presented once in a concise source-labelled mirror, not as a full-document approval. A user correction replaces the prior claim before persistence. |
| Persistence | Once L0/L1 pass and any L2 correction is incorporated, the Charter saves automatically. The assistant reports the revision, major choices, Unknowns, and Discover starting points; it does not ask for save approval. |

The reviewer must reject a transcript that treats an AI candidate or observation as user fact, asks
for full-document or save approval, chooses a Converge option for the user, omits the recommendation's
decision logic, or persists a draft after a failed L0/L1 check.
