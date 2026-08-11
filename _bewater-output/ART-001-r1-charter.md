---
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: charter
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition:
      statement: "把'立项前先想明白'这件原本只有专业咨询才买得起的事，变成 AI agent 扛着、founder 自己跑得起的 SaaS 流程——立项开发前就有底，不再拍脑袋抄竞品。"
      evidence_refs: []
    consumer_target:
      statement: "AI 硬件创业 founder（如做儿童机器人那位）：凭'自己有娃 + 赛道热'进场，战略能力较弱、没时间/没精力/没能力、预算紧，想做系统决策但卡在'没能力做市场验证'。"
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: "B2B2C：孵化器/加速器/VC/硬件平台为 founder cohort 付费使用 hardso 全决策段（Immersion→G2），绕开 founder 价格敏感、触达'没意识到该做战略'的人群。"
      evidence_refs: []
    leverageable_assets:
      statement: "BeWater 方法论（已成型、agent-native、可编码进 SaaS）+ 用户作为 AI 硬件行业资深从业者的领域知识与可信度。"
      evidence_refs: []
  tension:
    statement: "Magic 要求 agent 深度扛方法以真正补 founder 能力差；Money 的 B2B2C 要求规模化与机构可重复交付——agent 产出质量若守不住 gate 严谨性，Magic 与 Money 同时崩。"
  balance_choice: "先用 AI 硬件首垂直 cohort 把 G1→G2 决策段跑通、证明 agent 产出可过 gate，再谈规模化与渠道铺开。"
derived_from: []
signoffs: []
stale_reason: null
---

### Original intent

- **User's own words:** "把 bewater 这个方法论，具象化成网站，做成 saas，让其他人可以直接用"；"hardso 主要就服务做 AI 硬件的产品创新"；这类 founder "通常都会卡在专业的方法上"、"核心是没有这个能力做市场验证"；"事先没有想明白，做好战略规划就开始开发产品，后面执行会非常痛苦"。
- **Trigger / why now:** ① AI 硬件正在爆发，战略能力不足的 founder 一批批涌入；② 用户作为行业资深从业者，深知"没想明白/没做好战略规划就开始开发，后面执行非常痛苦"。
- **Desired change:** 把"先开发后痛苦"换成"先想明白 / 先验证再开发"，且 founder 自己跑得动（不被专业方法吓退或卡住）。

### Structured interpretation

- **One-line proposition:** hardso 是把 BeWater 创新方法论具象化的 Agent 驱动 SaaS——AI agent 主导带 AI 硬件 founder 跑完立项前的战略决策段（Immersion→G2），founder 在 gate 上做决策。
- **Target and situation:** AI 硬件创业 founder（画像：儿童机器人 founder，因"自己有娃 + 赛道热"进场）；战略能力较弱、时间/精力/预算紧；想做系统决策但卡住。
- **Current behavior and alternatives:** 拍脑袋抄竞品；不做系统战略规划与需求定义；替代方案是"跳过验证直接立项开发"或"事后返工"，成本是开发后的痛苦与重资产浪费。
- **Provisional solution hypothesis:** 用 agent 驱动 SaaS 把 BeWater 全决策段交付给 founder（用户"怎么做"的假设；未验证）。
- **Success signals:** founder 在立项开发前先过 G1（乃至 G2）gate——可观测的行为改变（gate 记录），而非仅自述。
- **Scope:** In = 决策段 Immersion→G2、agent 驱动、AI 硬件垂直优先；Out = 执行段（Design/Build/Launch/Grow）与 G3/G4；hardso 不替 founder 做 gate 决策或签字；首周期边界 = AI 硬件首垂直 + G1→G2 决策段跑通。

### Money + Magic

- **Magic / consumer value proposition:** 把"立项前先想明白"从"专业咨询才买得起"变成"AI agent 扛着、founder 自己跑得起"——立项前就有底，不再拍脑袋抄竞品。
- **Magic / consumer target:** AI 硬件 founder（如儿童机器人那位）：凭个人需求 + 赛道热度进场，战略能力弱、资源紧，想做系统决策但"没能力做市场验证"。
- **Money / commercial value proposition:** B2B2C——孵化器/加速器/VC/硬件平台为 founder cohort 付费使用全决策段，绕开 founder 价格敏感、触达"没意识到"人群。
- **Money / leverageable assets:** BeWater 方法论（成型、agent-native、可编码进 SaaS）+ 用户在 AI 硬件行业的资深从业经验与领域可信度。
- **Tension and balance:** Magic 要求 agent 深度扛方法以真正补能力差；Money 的 B2B2C 要求规模化与机构可重复交付。balance_choice：先用 AI 硬件首垂直 cohort 跑通 G1→G2、证明 agent 产出可过 gate，再谈规模化。

### Intent trace

| Claim | Provenance | Basis / exact user context | Calibration status |
|---|---|---|---|
| 目标用户是 AI 硬件创业 founder（如儿童机器人 founder），凭"自己有娃 + 赛道热"进场，战略能力弱、预算紧 | user-stated | "一个做儿童机器人的创始人…主要是自己有了娃…还有儿童机器人比较热门…没有这个能力做市场验证" | unchanged |
| founder 现状是"拍脑袋抄竞品"、不做系统战略规划与需求定义，核心卡在"没能力做市场验证" | user-stated | "他实际上就是拍脑袋抄竞品，核心是没有这个能力做市场验证" | unchanged |
| why now：AI 硬件正在爆发、能力不足的 founder 一批批涌入 + 用户作为行业资深从业者深知"没想明白就开发→执行非常痛苦" | user-stated | "一批批的出现…一是 AI 硬件正在爆发，二是我作为一个行业资深从业者，深知事先没有想明白…后面执行会非常痛苦" | unchanged |
| hardso = BeWater 方法论具象化为 Agent 驱动 SaaS，AI agent 主导跑全决策段、founder 在 gate 决策 | user-selected | 形态结构化选择中选定 "Agent 驱动 SaaS" | unchanged |
| 交付终点 = G2（全决策段，含投资决策）；AI 硬件重资产使 G2 成命门 | user-selected | 交付终点结构化选择中选定 "投资决策 (G2)"；重资产推论为 agent-interpretation | unchanged |
| 收入路径 = B2B2C（孵化器/加速器/VC/硬件平台为 cohort 付费），绕开 founder 价格敏感并触达"没意识到"人群 | user-selected | 收入路径结构化选择中选定 "B2B2C 机构付费" | unchanged |
| 成功信号 = founder 立项开发前先过 G1/G2 gate（可观测行为改变）；垂直聚焦 AI 硬件 | user-selected | 成功信号与垂直范围结构化选择中选定推荐项 | unchanged |

### Current knowledge state

| Type | Content |
|---|---|
| **Known** | (user-stated) AI 硬件赛道正热；目标 founder 普遍战略能力弱、时间/精力/预算紧；现状行为是"拍脑袋抄竞品"。这些是用户作为行业资深从业者的观察，自报告 ≠ 验证。 |
| **Believed** | (user-selected / agent-interpretation) 机构（孵化器/VC）愿为 cohort 付费；agent 能把方法论扛到 founder 跑得动且产出有效；AI 硬件重资产使 G2 成命门。均为待证信念，非 Fact。 |
| **Unknown** | founder 真实付费意愿与转化；机构获客周期与渠道结构；agent 产出能否守住 gate 严谨性；哪些 AI 硬件细分是最佳首垂直；"没意识到"人群的真实可触达比例。 |
| **Tensions** | ① 目标 founder "没意识到该做战略" 与 hardso 需主动获客之间的矛盾（B2B2C 部分缓解）；② agent 主导与 gate 严谨性之间的矛盾；③ Magic 要"补能力差"与 SaaS 需"可规模化自驱"之间的矛盾。 |

### Discover handoff

#### Core exploration question

在能信任或重述 hardso 命题之前，必须先搞懂：那个"拍脑袋抄竞品"的 AI 硬件 founder，在真实的立项决策现场，究竟是被"没能力"卡住、还是被"没意识/没意愿"卡住——以及 agent 把方法论扛到他跑得动的程度，产出的到底是有效决策还是形式合规的填充？

#### Beliefs to challenge

- (candidate belief, user-stated) founder 真把"立项前想明白"当必须做的事——而非嘴上认同、实际仍抄竞品。
- (candidate belief, agent-interpretation) 卡点是"能力缺"而非"认知/意愿缺"——给方法+引导就能跑通。
- (candidate belief, user-selected) agent 能把方法论执行到可过 gate 的质量。
- (candidate belief, user-selected) 机构愿为 cohort 付费、且 ACV/续约支撑 SaaS。
- (candidate belief, agent-interpretation) AI 硬件重资产使 G2 成为命门、而非"对早期 founder 过重"。

#### Root assumption research map

| Assumption | 4C | Why it matters | Evidence needed | Disconfirming signal |
|---|---|---|---|---|
| A-001 | Consumer | 若 founder 嘴上认同、实际仍抄竞品先干，整个 Magic 命题空转 | 深度访谈 + 早期 cohort 观察：founder 是否愿投入时间走完验证流程而非跳过 | 有方法论引导下 founder 仍选择跳过验证、直接抄竞品立项 |
| A-002 | Consumer | 区分"能力缺"与"认知/意愿缺"决定产品该是 agent 工具还是教育/激励 | 对照：给"agent 引导方法论"组 vs "仅给模板"组，能否独立完成有效验证 | agent 全程引导下 founder 仍无法产出可过 gate 的验证 |
| A-003 | Company / Category | agent 产出质量是 hardso 形态成立的技术地基；守不住 gate 则 Magic 与 Money 同崩 | pilot agent 跑出的工件过 L1/L4 评审比例 + 专家盲评 agent 产出 vs 人类咨询师产出 | 专家盲评中 agent 产出系统性被判为"形式正确但决策无效" |
| A-004 | Company / Channel | 机构付费意愿与 ACV 决定 Money 模型是否成立 | 机构访谈 + 付费 pilot：付费意愿、ACV、续约/复购 | 机构普遍拒付费或只接受免费/单次，ACV 覆盖不了获客成本 |
| A-005 | Channel | B2B2C 触达与真实完成率决定"没意识到"人群能否被有效服务 | cohort 试点：触达规模、完成率、gate 通过率 | 机构采购后 cohort 完成率/gate 通过率极低、founder 不真用 |

#### Starting 4C questions

- **Consumer:** 在真实立项决策现场，是哪类 AI 硬件 founder、在什么情境下、为什么会选择"抄竞品先干"而非"先验证"？
- **Company:** BeWater 方法论的哪些环节最容易被 agent 编码、哪些环节仍依赖人类判断？我们的 AI 硬件领域知识与可信度能否转化为机构渠道的信任？
- **Category:** AI 硬件创新今天的主流方法论/替代方案是什么（咨询/加速器/内部 PM/拍脑袋）？它们在哪一步失效？
- **Channel:** 孵化器/加速器/VC/硬件平台今天如何帮助 founder 做战略决策？hardso 嵌入他们既有流程的接入点在哪？

#### Research boundary

Discover 应先查 A-001/A-002/A-003（人的真需求 + agent 可行性，是整个命题的地基），再查 A-004/A-005（机构渠道商业可行性）。不应在 agent 产出质量未被证明前就设计 SaaS 功能细节或锁定 UI；不应假设 founder 会自驱付费（需用 cohort 行为证据验证）。执行段（Design/Build/Launch/Grow）与 G3/G4 明确不在本研究范围。
