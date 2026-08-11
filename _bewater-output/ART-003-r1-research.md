---
schema_version: 1
artifact_id: ART-003
revision: 1
supersedes_ref: null
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
- Advisory context: `ART-002@1`; it supplies candidate judgments only and is not evidence.

### Innovation challenge

在真实的 AI 硬件立项现场，判断 founder 的关键阻力究竟是能力与可用性不足，还是认知、意愿与行为优先级不足；同时判断 Agent 主导的方法论能否产生真正改善决策的结果，而非形式合规的填充。

### Research boundary

- In scope: AI 硬件 founder 的立项前行为；Agent 执行战略与需求验证方法的有效性；机构型 B2B2C 渠道；首个 cohort 的可验证机制；相关品类、生态与经济约束。
- Out of scope: SaaS UI 和功能细节、定价套餐设计、执行段 Design/Build/Launch/Grow、G3/G4，以及任何既定战略或投资结论。
- Available evidence: 可信公共来源，以及用户后续明确提供的文档。
- Current access limitation: 暂无目标 founder 访谈、现场观察、内部 cohort 数据、交易数据或可运行产品试点；公共来源不能替代这些行为证据。

### Strategic uncertainties

| ID | Uncertainty | Why it matters |
|---|---|---|
| SU-01 | founder 是“不能做”还是“不愿/不知道要做”？ | 决定 hardso 更像能力工具、教育/激励机制，还是两者组合。 |
| SU-02 | Agent 能否维持 Gate 所需的判断深度，而不只满足文档结构？ | 这是 Magic 与 Money 共同的单点风险。 |
| SU-03 | 孵化器、加速器、VC 或硬件平台是否愿为决策质量付费，并能推动 founder 真正完成流程？ | 决定 B2B2C 是否同时成立为收入渠道和验证渠道。 |
| SU-04 | AI 硬件是否足够同质，能作为一个首垂直，还是必须进一步收窄到具体子赛道与 founder 情境？ | 决定研究的可迁移边界和首个 cohort 的可比性。 |
| SU-05 | 哪些生态、技术与经济约束会使 Agent 驱动的决策服务无法规模化？ | 防止只研究需求而遗漏交付、责任与单位经济。 |

### Future strategic choice relevance

本研究可为以下未来选择提供输入，但不代表这些选择已经做出：

- 能力工具、教育/激励产品或混合机制；
- 机构嵌入式 cohort 服务或 founder 自助式 SaaS；
- AI 硬件广泛垂直或更窄的首个子赛道；
- Agent 自动化深度与人类专家介入边界；
- 首个验证 cohort 应优先证明需求行为、产出质量还是机构付费。

## Living Learning Agenda

### Candidate beliefs to challenge

| Belief | Status | Disconfirming direction |
|---|---|---|
| founder 真把“立项前先想明白”当作必须完成的工作。 | Candidate belief; L1 self-report only | 有方法和引导时仍跳过验证、直接开发。 |
| founder 的核心障碍是能力缺口，而非认知或意愿缺口。 | Candidate belief | 已理解方法且获得支持后仍不投入时间或改变行为。 |
| Agent 能把 BeWater 执行到决策有效、可过 Gate 的质量。 | Candidate belief | 专家盲评显示产物形式正确但决策无效。 |
| 机构愿为 founder cohort 的决策质量付费。 | Candidate belief | 机构只愿购买导师服务，或把软件视为免费附属品。 |
| 机构渠道能够让 founder 真正完成流程。 | Candidate belief | 采购后参与率、完成率或 Gate 通过率持续偏低。 |

### Open learning questions

| ID | Priority | Learning question | Evidence need | Dependencies |
|---|---|---|---|---|
| LQ-01 | Critical | AI 硬件 founder 在立项前何时选择验证、何时直接抄竞品或开工，真实约束是什么？ | 多个独立来源中的行为、失败复盘与具体决策情境；同时寻找意愿而非能力导致跳过验证的反例。 | None |
| LQ-02 | Critical | Agent 辅助复杂战略判断的已知能力边界是什么，怎样区分结构合规与决策有效？ | 直接评测、实验或同行评议研究；任务定义、比较基线、失败模式与适用边界。 | None |
| LQ-03 | High | 哪类机构今天为 founder 的战略/验证能力投入预算，购买对象和成功指标是什么？ | 机构公开项目结构、采购/合作模式、预算或价格代理、结果衡量方式；避免把投资条款误当工具付费。 | None |
| LQ-04 | High | B2B2C cohort 能否同时产生真实参与行为和可用验证证据？ | cohort 参与、完成、留存与结果机制；寻找“机构买了但 founder 不用”的反例。 | LQ-03 |
| LQ-05 | Medium | 当前替代方案如何解决同一问题，hardso 的可验证差异在哪里？ | 咨询、加速器、模板/课程、AI 创业工具的可见服务边界与交付方式。 | LQ-01, LQ-03 |
| LQ-06 | Medium | AI 硬件内部哪些子赛道和 founder 情境最适合首个可比 cohort？ | 开发资本强度、验证周期、监管/安全、渠道和用户反馈可得性的差异证据。 | LQ-01 |

### 4C and extended-lens coverage

| Lens | Material question | Priority | Status | Evidence needed |
|---|---|---|---|---|
| Consumer | 谁在什么决策情境下挣扎、切换或坚持原行为？ | Critical | planned | 决策行为、失败复盘、反例与情境边界。 |
| Company | BeWater + Agent 的真实能力、限制和必要人工介入是什么？ | Critical | planned | 直接评测、专家比较与失败模式。 |
| Category | 咨询、加速器、课程、模板与 AI 工具如何界定和交付价值？ | High | planned | 独立品类证据与可见产品/项目审计。 |
| Channel | 哪类机构掌握目标 founder、为何采购、如何推动完成？ | High | planned | 机构项目、采购代理、参与和结果机制。 |
| Technology | 当前 Agent 在长链战略任务上的成熟度与可靠性边界是什么？ | Critical | planned | 原始研究、公开评测和方法透明的实验。 |
| Ecosystem | founder、机构、导师、投资人和平台之间如何交换价值与承担责任？ | High | planned | 角色、激励、流程和责任边界。 |
| Economics | 机构付费与高质量人工介入能否形成可持续交付单元？ | Medium | planned | 可核验价格/成本代理及敏感性边界。 |
| Regulation | 哪些 AI 硬件子赛道的安全或合规要求会改变首个 cohort？ | Medium | planned | 官方规则与标准，仅在子赛道比较时进入。 |

### Accepted gaps for this revision

| Gap | Why accepted now | Possible strategic consequence | Future research path |
|---|---|---|---|
| 无目标 founder 的一手访谈和现场行为。 | 当前环境只能执行公共来源研究。 | 无法确认 capability-vs-willingness，也不能形成 L4 行为结论。 | 后续由人类组织访谈、观察或 cohort。 |
| 无 hardso 原型和 Agent 产出盲评。 | 尚无可运行试点输入。 | 无法验证 A-003 或确定人工介入边界。 | 用同一案例比较 Agent、模板与专家产物。 |
| 无机构采购、合同或交易数据。 | 未提供内部材料，公开价格只能作为代理。 | 无法确认真实 WTP、ACV 或续约。 | 机构访谈与付费 pilot。 |
| 无 cohort 完成率和 Gate 通过率。 | 尚未运行 cohort。 | 无法判断 B2B2C 是否产生真实使用行为。 | 记录邀请、激活、完成、Gate 与后续决策。 |
