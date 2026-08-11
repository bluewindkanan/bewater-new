---
schema_version: 1
artifact_id: ART-003
revision: 2
supersedes_ref: artifact:ART-003@1
kind: research
stage: discover
branch_id: BR-001
document_status: draft
validation_status: unvalidated
derived_from:
  - artifact:ART-001@1
  - assumption:A-001@1
  - assumption:A-002@1
  - assumption:A-003@1
  - assumption:A-004@1
  - assumption:A-005@1
signoffs: []
stale_reason: null
---

# Discover Research — hardso

## Research Frame

### Formal input snapshot

- Charter: `ART-001@1`
- Active root assumptions: `A-001@1`, `A-002@1`, `A-003@1`, `A-004@1`, `A-005@1`
- Advisory context: `ART-002@1`; it supplied candidate judgments only and was not treated as evidence.

### Innovation challenge

在真实的 AI 硬件立项现场，判断 founder 的关键阻力究竟是能力与可用性不足，还是认知、意愿与行为优先级不足；同时判断 Agent 主导的方法论能否产生真正改善决策的结果，而非形式合规的填充。

### Research boundary

- In scope: AI 硬件 founder 的立项前行为；Agent 执行战略与需求验证方法的有效性边界；机构型 B2B2C 渠道；cohort 参与机制；相关品类、生态与经济约束。
- Out of scope: SaaS UI 和功能细节、定价套餐、执行段、G3/G4，以及任何既定战略或投资结论。
- Evidence used: 14 条来源级原子证据，来自创业行为研究、Agent 原始评测、官方平台规则和政府项目评估。
- Access limitation: 暂无中国 AI 硬件 founder 的现场观察、hardso 原型盲评、机构采购记录或 cohort 遥测；因此不形成 L4 行为结论，也不验证任何根假设。

### Strategic uncertainties

| ID | Current research position | Strategic consequence |
|---|---|---|
| SU-01 | capability-vs-willingness 的二分被证据否定；更合理的结构是“优先级/身份防御 × 方法能力 × 有效样本可得性 × 硬件阶段约束”。 | hardso 不能只补方法，也要暴露投入、反证采纳、样本质量和不可逆承诺。 |
| SU-02 | 通用 Agent 证据表明格式、动作、状态、重复可靠性与整体可采用质量是不同层级；BeWater 实际质量仍未测试。 | Gate 质量必须以多层结果评测和人工签核验证，不能以文档完成率代理。 |
| SU-03 | 机构确实为管理训练、customer discovery 和软件采用投入资源；但公开证据不证明其会采购 hardso，且补贴/入选不保证使用。 | B2B2C 仍是候选路径，首个 pilot 必须同时测采购与 founder 行为。 |
| SU-04 | 硬件“先做原型”有时是获得有效市场信号的制度前提；公开资料不足以选择 AI 硬件首子赛道。 | 必须区分可逆实验性 prototype 与不可逆量产承诺，再选择可比 cohort。 |
| SU-05 | 高质量交付可能依赖行为里程碑、cohort accountability、人工审核和样本招募支持。 | 单纯 self-serve SaaS 的规模化假设仍无证据。 |

### Future strategic choice relevance

研究为以下未来选择提供输入，但没有替人做选择：

- 能力工具、行为约束机制或两者结合；
- self-serve SaaS、机构 cohort workflow 或 human-in-the-loop 服务；
- Agent 自动化深度与人工检查点；
- 首个 cohort 的子赛道、可逆验证边界和成功指标；
- 机构采购、founder 参与和 Gate 质量是否应在同一 pilot 中同时验证。

## Living Learning Agenda

### Belief status after Sprint 1

| Belief | Sprint status | Evidence basis | Remaining test |
|---|---|---|---|
| founder 真把“立项前先想明白”当作必须工作。 | challenged | `E-001@1`, `E-002@1`, `E-005@1` | 目标 founder 是否投入时间、接受反证并在不可逆量产前行动。 |
| 核心障碍是能力缺，而非认知/意愿缺。 | contradicted as a single-cause frame | `E-001@1`–`E-005@1` | 在同一 cohort 中分离能力、优先级、身份、样本与硬件阶段机制。 |
| Agent 能产出可过 Gate 的有效决策。 | unresolved; evaluation frame deepened | `E-006@1`–`E-009@1` | 同案比较 Agent、模板和专家，重复运行并盲评整体可采用性。 |
| 机构愿为 cohort 付费。 | weakly supported for adjacent programs only | `E-010@1`, `E-012@1` | hardso 的真实机构采购、预算科目、ACV、审批和续约。 |
| 机构渠道能推动 founder 真走完流程。 | challenged | `E-011@1`–`E-014@1` | 邀请、激活、里程碑、深度支持、Gate 与后续决策的漏斗遥测。 |

### Updated learning questions

| ID | Priority | Current answer | Next evidence need |
|---|---|---|---|
| LQ-01 | Critical | 二分不成立；至少四类机制共同作用。 | 中国 AI 硬件 founder 的纵向行为与具体决策日志。 |
| LQ-02 | Critical | Agent 质量至少含协议、状态、重复可靠性、整体采用和恢复五层。 | hardso 工件的专家盲评、重复运行和实际决策后果。 |
| LQ-03 | High | 机构投入相邻能力项目，但不等于采购 SaaS。 | 采购人、预算、合同、付费 pilot 和续约门槛。 |
| LQ-04 | High | cohort 与补贴不能自动产生深度参与。 | 产品级活跃、里程碑完成、mentor 使用、Gate 与退出原因。 |
| LQ-05 | Medium | 高接触训练、强制 customer discovery、软件补贴和自助工具是不同机制。 | 首个 pilot 需要比较的最小可信替代方案。 |
| LQ-06 | Medium | 暂无足够公开证据选择 AI 硬件首子赛道。 | 按 prototype 成本、反馈周期、监管与渠道可得性比较候选子赛道。 |

### 4C and extended-lens coverage

| Lens | Status | Sprint evidence and limitation |
|---|---|---|
| Consumer | evidenced with target-population gap | 创业探索、反馈抵抗、方法训练和样本偏差已有证据；不是中国 AI 硬件现场行为。 |
| Company | evidenced for evaluation boundary; gap for hardso | Agent 评测边界清楚；hardso/BeWater 自身尚无 prototype 盲评。 |
| Category | evidenced at adjacent-category level | 结构化训练、customer discovery cohort、软件补贴和 Agent 工具代表不同替代机制；未完成全市场产品清单。 |
| Channel | evidenced with procurement gap | 机构投入与参与漏斗已有官方数据；没有 hardso 类 SaaS 合同和续约。 |
| Technology | evidenced with fast-change limitation | 通用 Agent 的长链、重复可靠性和整体质量边界已有原始评测；绝对能力需持续复测。 |
| Ecosystem | evidenced | 机构、business school、mentor、平台和 founder 的角色及 accountability 机制可见。 |
| Economics | evidenced by proxies; material gap retained | 有参与费、补贴和项目预算代理；没有 hardso 单位经济或机构 ACV。 |
| Regulation | gap-accepted | 只有在首个硬件子赛道被选定后，具体安全/合规要求才会改变 cohort 设计；当前不阻塞核心重构。 |

## Latest Research Sprint — Sprint 1

### Selected learning questions

- M1 / LQ-01: founder 何时探索、接受反证或直接 build，capability-vs-willingness 是否成立。
- M2 / LQ-02: Agent 的结构合规、结果有效、重复可靠性和整体采用如何区分。
- M3 / LQ-03–04: 机构如何投入资源，什么机制推动参与，以及“机构出钱但不使用”的反证。

### Method Bundles

| Mission | Smallest complementary bundle | Contribution | Limitation |
|---|---|---|---|
| M1 | desk/document research + evidence-strength/transferability + negative-case search + tension finding | 结合行为研究、RCT、平台规则和反例，避免把先 prototype 自动解释为拒绝验证。 | 公开资料不能替代目标 founder 现场观察。 |
| M2 | primary benchmark research + source-family triangulation + contradiction analysis + holistic-evaluation comparison | 区分多层 Agent 质量，并保留快速进步和任务迁移的反证。 | 基准多来自软件、API 和仿真任务。 |
| M3 | official programme evaluation + ecosystem/channel mapping + alternative-explanation testing + tension finding | 区分项目预算、参与费、软件补贴、投资条款和实际使用。 | 公开项目不是 hardso 采购，也缺产品级留存。 |

### Work executed

- M1 normalized evidence: `E-001@1`–`E-005@1`
- M2 normalized evidence: `E-006@1`–`E-009@1`
- M3 normalized evidence: `E-010@1`–`E-014@1`
- Duplicate pages from the same study or programme were assigned one `independence_key` and not counted as independent confirmations.
- Supporting and disconfirming evidence were both retained; no Assessment claim was promoted to evidence.

### Material deviations and fallbacks

- 未找到 AI 硬件 founder 的目标人群现场行为研究；采用广义创业行为、硬件渠道规则与实验质量研究，并明确限制迁移。
- 未找到机构为 founder strategy workflow 统一采购 SaaS 的可核验合同；采用相邻训练项目、软件补贴和 cohort 评估作为代理，不将其写成 hardso WTP。
- 未找到直接测战略决策有效性的 Agent RCT；采用状态评测、重复可靠性、长链边界和 holistic review 形成评测约束，不将 benchmark 分数等同商业有效。

## Sprint Synthesis and Plan Delta

### Learned

1. founder 的障碍不是“能力”与“意愿”二选一。最低成本探索不足、身份防御、方法可教性、样本偏差和硬件 prototype 规则共同构成因果结构。
2. 对硬件而言，关键不是“是否先 build”，而是 build 是否仍为可逆实验，以及 founder 是否在不可逆量产承诺前获得高质量反证。
3. 方法训练可以改变终止与 pivot 行为，但现有有效干预含导师、高支持和参与者筛选，不能直接推出 Agent 可独立复现。
4. Agent 质量不能用文档完成率或单次自动测试表示；至少需要协议合法、外部状态、无副作用、重复可靠性、整体可采用性和人工修复成本。
5. 机构会为管理训练、customer discovery 和软件采用投入资源，但培训参与费、政府补贴、SAFE 投资和 SaaS 采购是不同经济对象。
6. 机构背书、补贴和 cohort enrolment 均不能保证深度使用；行为里程碑、时间承诺、公开进展和人工支持可能是关键机制。
7. 满意度、完成率、自报能力、软件兑换、Gate 通过和最终业务结果必须分层，不能互相代理。

### Contradicted

- `A-002` 的 capability-only 结构被反证；它仍可作为一项机制，但不能排除意愿、身份、样本和硬件阶段约束。
- “机构购买或补贴后 founder 就会使用”被相邻项目数据反证；这削弱 `A-005` 的自动触达与完成逻辑。

### Belief changed

- `A-001`: 从“是否口头认为重要”转为“是否投入时间、采纳反证，并在不可逆承诺前完成有效验证”。
- `A-003`: 从单一“能否过 Gate”转为可检验的多层质量模型；根假设仍 untested。
- `A-004`: 从泛化的“机构有预算”收窄为“相邻项目存在投入和 stated WTP，但 hardso 采购与续约未知”。
- `A-005`: 从渠道触达假设收窄为“渠道必须和行为机制、实施支持、漏斗遥测共同成立”。

### Reframed

原问题：

> founder 是被“没能力”卡住，还是被“没意识/没意愿”卡住？

研究后的候选 reframe：

> 在硬件 founder 走向不可逆投入之前，哪些机制能让他投入真实时间、接触正确样本、采纳反证并改变决策；Agent、cohort accountability 与人工审核分别承担哪一层？

### Deepened

- Agent 评测标准从结构合规扩展到多层结果可靠性。
- B2B2C 从“分销渠道”扩展为采购、参与行为、证据生产和 accountability 的组合系统。
- 硬件验证从“先想后做”深化为可逆 prototype 与不可逆量产承诺的边界。

### Dropped

- 不再继续寻找一个公开统计来证明所有 AI 硬件 founder 都因单一原因跳过验证。
- 不再把 accelerator 投资额、政府计划总预算或 completer stated WTP 当作 hardso 软件收入证据。
- 不再用单一 benchmark 或文档完成率判断 Agent 决策有效。

### New questions

1. 中国 AI 硬件 founder 的真实立项顺序、不可逆承诺点和反证采纳行为是什么？
2. 同一案例下，模板、Agent、Agent+cohort 和人类专家的开始率、完成率、盲评质量与决策变化分别如何？
3. 哪些人工检查点带来净质量增益，哪些只增加审批成本？
4. 机构采购人的预算科目、审批周期、单 cohort 可接受价格和续约阈值是什么？
5. 哪个 AI 硬件子赛道能以最低 prototype 成本获得最快、最可信的行为信号？
6. Gate 通过后，哪些后续行为可证明决定被采纳，而非只完成文档？

### Remaining gaps

- 无中国 AI 硬件 founder 的 L4 行为证据。
- 无 hardso/BeWater Agent 的重复运行、专家盲评和实际决策后果。
- 无机构采购合同、真实 ACV、续约或 cohort 产品遥测。
- 无首子赛道比较所需的本地渠道、监管和 prototype 成本数据。
- 无 human-in-the-loop 检查点的因果比较。

### Plan Delta and transition

- Priorities move from broad desk discovery to two future empirical tracks: founder behavior cohort and Agent quality blind evaluation.
- The next transition is `synthesize`.
- Rationale: additional general public-source search is now unlikely to resolve the remaining critical uncertainty; the next meaningful evidence requires field access, a runnable hardso case, institution interviews or a paid pilot.
- Stop rule: do not run another desk-research Sprint unless new internal material, a named target subsegment, a prototype, or institution access changes the evidence boundary.

## Insight Ingredients and Insight Readiness

### Evidence-backed patterns

- **Multi-mechanism barrier:** founder inaction and weak validation arise from interacting behavioral, capability, sample-access and hardware-stage mechanisms, not a single deficit.
- **Reversible-before-irreversible:** hardware prototype activity is not the problem by itself; the strategic boundary is whether evidence is gathered before irreversible scale commitments.
- **Layered Agent validity:** format and task completion are necessary but far from sufficient; repeated state success, no collateral damage, holistic adoption quality and repair cost matter.
- **Channel-behavior coupling:** institutional distribution only creates value when procurement, founder activation, behavior milestones, deep support and outcome measurement all connect.

### Tensions

- 更严格的 Agent Gate 质量需要人工审核和重复评测，但 SaaS 规模化要求低边际交付成本。
- founder 最需要帮助时可能也最缺乏发现、进入和坚持流程的能力；补贴本身不能解决这一点。
- 硬件需要 prototype 才能获得强信号，但 prototype 又容易升级为沉没成本和身份依附。
- 机构重视 cohort 完成和满意度，而 hardso 需要证明的是反证采纳和决策变化。

### Anomalies

- 结构化方法能增加终止弱想法，而常见创新项目指标往往偏好“更多项目继续”。
- 已完成高质量 cohort 的参与者愿付更多，但高价值 mentoring 模块的完整使用率仍低。
- 软件补贴已获批者中仍有 40% 不兑换，说明价格不是唯一障碍。
- 自动测试通过的 Agent 成果仍可能全部无法直接采用。

### Challenged Accepted Beliefs

- “给方法就会做”缺乏支持。
- “机构买了就会用”有直接相邻反证。
- “文档过 Gate 就代表决策有效”必须改为多层、重复和后果导向的验证。
- “先 build 就是拒绝验证”在硬件路径上过度简化。

### Reframe candidate

> hardso 的核心不应被研究成“替 founder 填完一套方法”，而应被检验为一个在不可逆投入前制造真实承诺、正确样本、反证采纳和可审计决策变化的系统；Agent 负责可重复的认知与流程劳动，机构/cohort 提供 accountability，人类保留高风险判断和 Gate 决策。

这是研究候选，不是最终 Insight、策略或产品决定。

### Strategic relevance

- 若后续行为研究支持该 reframe，首个 pilot 应同时测 founder 行为、Agent 整体质量和机构参与机制，而非先做完整 SaaS。
- Agent 的成功指标应从 completion rate 改为分层质量与后续决策行为。
- 机构价值主张应指向可审计的 cohort 决策质量，而不是内容、模板或席位数量。
- 首子赛道应按“可逆验证成本 × 行为信号速度 × 不可逆投入风险”选择，而非只按赛道热度。

### Insight Readiness judgment

**Met for handoff, with explicit material gaps.**

- Critical uncertainties are evidenced where public sources can answer them, or retained as explicit material gaps.
- Consumer, Company, Category and Channel were checked; Technology, Ecosystem and Economics were material and checked; Regulation is an accepted, consequence-labelled gap.
- Supporting and disconfirming evidence are both present.
- Contradictions and alternative explanations remain visible.
- Evidence-backed patterns, tensions, anomalies and a reframe candidate are available.
- Additional general desk research has low marginal strategic learning value under current access constraints.
- This is not a Gate, score, fact quota, F/P/E/T signoff, directional hypothesis or strategy decision.

## Remaining uncertainty

| Gap | What it may change | Future research path |
|---|---|---|
| Target founder behavior | 是否需要能力工具、行为机制或教育/筛选 | 中国 AI 硬件 founder 纵向访谈、观察和 cohort telemetry |
| Agent whole-task quality | 自动化深度、人工检查点和 Gate 可信度 | 同案重复运行、专家盲评、修复成本与后续决策跟踪 |
| Institution procurement | B2B2C 是否成立、价格与销售周期 | 机构采购访谈、付费 pilot、合同和续约 |
| First subsegment | cohort 可比性、验证周期和监管负担 | prototype 成本、渠道、反馈速度与规则对比 |
| L4 behavior | G2 最终是否可能满足硬门槛 | 真实完成、付费、反证采纳、决策改变和不可逆投入前后行为 |
