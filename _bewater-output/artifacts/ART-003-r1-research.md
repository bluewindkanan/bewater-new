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
derived_from: ["artifact:ART-001@1"]
signoffs: []
stale_reason: null
---

# Research Plan · 创始人 IP 短视频放大器（r1 · Sprint 1 计划）

## Research Objective

- **Charter 修订**：`artifact:ART-001@1`（本计划唯一正式输入；Initial Assessment 不作为证据，其 inspect-next 项仅作候选种子问题）
- **创新挑战（源自 Charter Challenge）**：中小企业老板做创始人 IP 短视频的三重困境——全部自己干则粗糙且耗时（剪辑最重）、找代运营则成本高且照样占用创始人时间、多数人随便发发没流量。如何以放大器模式（AI 干程序化工序 + 人做选择，覆盖选题/文案/剪辑/运营）把创始人的时间成本压到每天约 30 分钟工具互动并改善流量结果——未经验证。
- **研究边界（源自 Charter Scope + Constraints）**：范围内 = 面向四环节 copilot 的市场/用户/竞争/平台研究；首发人群 = 粗糙自干派中小企业老板；首发平台 = 微信视频号；素材输入 = 每周批量真人拍摄。范围外 = 全托管服务、代运营服务包、数字人替代真人、多平台矩阵（首发不锁定）。约束 = 产品作者个人时间与自有方法论起步、平台规则与接口的外部限制、AI 能力的现实水平。
- **战略不确定性（源自 Charter Unknown + Tensions）**：
  - U1 粗糙自干派的付费意愿与价位带
  - U2 放大器模式下"没流量"的实际改善幅度（方法论有效性）
  - U3 "每天 30 分钟"行为承诺的现实性
  - U4 AI 剪辑可达到的质感天花板
  - U5 自有方法论能否显性化、产品化
  - T1 流量是结果但订阅续费取决于结果（承诺边界 vs 商业可持续）
  - T2 "让他选择" vs 选择本身即创始人最贵时间（总决策量可能不降反升）
  - T3 日更节奏 vs 每周批量拍摄的时序错位
  - T4 订阅自助获客 vs 目标人群恰恰没时间
- **研究可能影响的未来战略选择**（尚未作出任何战略决策）：首发环节楔形（四环节先攻哪个 / 是否全流程一步到位）；目标人群校准（自干派是否真有预算与习惯）；平台策略（视频号首发是否成立）；商业化形态（订阅价位与结构）；方法论产品化路径（自有显性化优先 vs 数据闭环优先）；是否具备进入 Define 阶段提炼洞察的条件。

## Learning Plan

```yaml
- id: LP-001
  learning_objective: 粗糙自干派的真实工作流与成本基线——单条选题→发布实际投入、现有工具链、卡点
  starting_state: think-known
  starting_view: 用户自述三流派画像（自干粗糙 / 代运营贵且仍费时 / 随便发发），self-report 非验证
  decision_relevance: 校准 Magic 命中与 A-002 人群真实性
  lens: Consumer
  priority: P1
- id: LP-002
  learning_objective: 自干派对工具的付费意愿与价位带——现有付费行为、代运营报价对照
  starting_state: unknown
  starting_view: 未验证；Charter 显式 Unknown
  decision_relevance: A-002 直接检验；定价与商业化形态
  lens: Consumer
  priority: P1
  ledger_ref: assumption:A-002@1
- id: LP-003
  learning_objective: AI 短视频工具赛道格局——竞品按环节覆盖×定价×目标用户分组，端到端空缺是否真实
  starting_state: think-known
  starting_view: Assessment 线索：资本确认（OpusClip/Captions），端到端位置存疑（候选非证据）
  decision_relevance: wedge 选择；差异化定位
  lens: Category
  priority: P1
- id: LP-004
  learning_objective: 默认工具吞噬风险——剪映及官方工具的 AI 能力路线、面向企业主的免费全流程能力信号（kill signal）
  starting_state: unknown
  starting_view: Assessment 判断"剪映 All in AI"为 top 风险（候选非证据）
  decision_relevance: A-003 可行性；产品存续 kill signal 基线
  lens: Technology
  priority: P1
  ledger_ref: assumption:A-003@1
- id: LP-005
  learning_objective: 视频号生态与运营可行性——企业主 IP 流量机制、第三方发布/数据接口政策、AI 内容规则
  starting_state: unknown
  starting_view: 未验证；Charter 显式 Unknown
  decision_relevance: 运营环节可自动化程度与合规风险；平台策略校准
  lens: Channel
  priority: P1
- id: LP-006
  learning_objective: 方法论可显性化的外部基准——业界创始人 IP 内容方法论资源能否支撑"选得更准"承诺
  starting_state: unknown
  starting_view: 作者自有 know-how 存在但未显性化（self-report）
  decision_relevance: A-001 直接检验；方法论产品化路径
  lens: Company
  priority: P2
  ledger_ref: assumption:A-001@1
- id: LP-007
  learning_objective: 「每天 30 分钟」行为预算可行性——创作者时间投入基准、同类工具实际使用时长证据
  starting_state: unknown
  starting_view: 理想态为用户期望（user-stated），无行为证据
  decision_relevance: A-003 / T2 / T3；日更承诺可信度
  lens: Consumer
  priority: P2
- id: LP-008
  learning_objective: 订阅经济性——AI 生成成本对订阅定价的约束、竞品 credit 定价教训
  starting_state: unknown
  starting_view: Assessment 线索：竞品 $15-69/mo、credit-cap 陷阱（候选非证据）
  decision_relevance: T1；定价结构设计
  lens: Economics
  priority: P2
```

**4C 盲点图**：Consumer（LP-001/002/007，planned）、Company（LP-006，planned）、Category（LP-003，planned）、Channel（LP-005，planned）；material 扩展镜头：Technology（LP-004）、Economics（LP-008）、Ecosystem（并入 LP-005）；Regulation 并入 LP-005 平台规则，Future 并入 LP-004 路线追踪。**已接受缺口**：① LP-006 作者侧 know-how 显性化本体是 out-of-band 人工工作，本研究只建外部基准——后果 = A-001 只能侧面检验，L4 留给 dogfood；② LP-007 公开一手时间投入统计可能不存在，预期 gap-accepted → dogfood 行为日志（L4）承接。

**已投影根假设**（本修订引入，derived_from = artifact:ART-003@1，均 impact=high × uncertainty=high → Achilles Heel，L4 durable obligation 即刻打开，行为证据由 dogfood 承接、与 Charter 首个成功信号一致）：

- **A-001**（magic/consumer）："产品作者的自有方法论（选题/文案/结构）能够显著改善粗糙自干派内容的流量结果——放大器承诺的核心。"证伪信号：外部证据显示企业主 IP 流量结果主要由人设/赛道/投放等非方法论因素决定，或同等方法论能力已被免费默认工具内置。
- **A-002**（money/commercial）："粗糙自干派中小企业老板对'每天 30 分钟全流程'放大器工具存在真实付费意愿，足以支撑订阅制 SaaS。"证伪信号：该人群工具付费率极低且付费集中于代运营服务而非工具，或价位带证据不成立。
- **A-003**（both/technical）："当前 AI 能力已足以把选题→文案→剪辑→发布的程序化工序压缩到每天约 30 分钟的真人互动内。"证伪信号：竞品/官方能力盘点显示关键工序（尤其剪辑质感）仍需大量人工，或单条生成成本使订阅经济不可行。

## Next Sprint

Sprint 1 = RM-001..RM-003，三个任务源空间相互独立；协调者按用户既有偏好**顺序内联执行**（不派并行 worker）。

```yaml
- id: RM-001
  learning_refs: [LP-003, LP-004]
  evidence_needed: 竞品功能与定价事实、官方公告文本、公开能力评测（中英文）
  method_source_bundle: desk-document-research + company-product-competitor-audit（collection）→ strategic-group-analysis（analysis，按环节覆盖×定价×目标用户分组；不用 five-forces，因问题只需分组定位而非行业结构）→ source-family-triangulation + negative-case-disconfirming-search（validation，对"吞噬"信号找正反两面）
  exclusions: 不做账号实测；不展开消费者娱乐剪辑 App 的非企业主功能细节
  dependencies: []
  owner: coordinator
  bounded_budget: 约 6-8 次检索
  stop_condition: 主要竞品分组覆盖且吞噬信号获得正/反明确证据或确认无公开信号
  expected_output: Research Packet（原子 claim + 精确来源）
  limitation: 公开信息无法验证实际生成质量；路线图非承诺
- id: RM-002
  learning_refs: [LP-005]
  evidence_needed: 微信/视频号官方文档与公告文本、接口服务商现状、平台规则原文
  method_source_bundle: official-document-search（collection，ad-hoc：官方文档优先）→ platform-policy mapping（analysis，ad-hoc 三栏：机会/限制/成本）→ 官方来源三角（validation）
  exclusions: 不做账号实测；不做多平台横向对比（Sprint 2 视需要扩展）
  dependencies: []
  owner: coordinator
  bounded_budget: 约 4-6 次检索
  stop_condition: 接口政策与 AI 内容规则获得官方文本锚点，或确认无公开文本（记录为 gap）
  expected_output: Research Packet
  limitation: 成文规则与实际执行可能不一致；政策有时效风险
- id: RM-003
  learning_refs: [LP-001, LP-002]
  evidence_needed: 老板自述（社区/评论区/访谈转载）、代运营报价对照、工具会员付费行为证据
  method_source_bundle: social-review-discourse-analysis（collection）→ jtbd-journey（analysis，从"想做一条"到"发出去"的真实旅程与卡点）→ evidence-strength-transferability（validation）→ tension-finding（synthesis，仅当付费意愿信号冲突时）
  exclusions: live 访谈为 out-of-band 人工工作（记录为 limitation 与 gap）；不覆盖海外创作者
  dependencies: []
  owner: coordinator
  bounded_budget: 约 6-8 次检索
  stop_condition: 出现稳定的工作流/成本模式，且付费信号有方向（含保留矛盾）
  expected_output: Research Packet
  limitation: 自述样本存在偏差与幸存者问题；付费意愿是态度信号而非行为验证（L4 缺口显式保留）
```

LP-006/007/008 为 Sprint 2 候选：LP-006 依赖作者侧 out-of-band 显性化工作的外部基准盘点；LP-007 预期公开数据缺失；LP-008 的竞品定价事实由 RM-001 顺带部分覆盖，深化留待 Sprint 2 按 Sprint Decision 决定。

## Research Progress

```yaml
- learning_ref: LP-001
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 自干派工作流与成本基线（Sprint 1 · RM-003）
- learning_ref: LP-002
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 付费意愿与价位带（Sprint 1 · RM-003；L4 行为验证缺口）
- learning_ref: LP-003
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 赛道分组与端到端空缺（Sprint 1 · RM-001）
- learning_ref: LP-004
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 默认工具吞噬信号基线（Sprint 1 · RM-001；持续追踪项）
- learning_ref: LP-005
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 视频号接口政策与 AI 内容规则（Sprint 1 · RM-002）
- learning_ref: LP-006
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 方法论外部基准（Sprint 2 候选；作者侧显性化为 out-of-band）
- learning_ref: LP-007
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 30 分钟行为预算（Sprint 2 候选；预期 gap → dogfood L4）
- learning_ref: LP-008
  answer_status: not-researched
  knowledge_refs: []
  current_answer: Not researched
  remaining_gap: 订阅经济性（Sprint 2 候选；定价事实部分由 RM-001 顺带）
```
