---
schema_version: 1
artifact_id: ART-003
revision: 3
supersedes_ref: "artifact:ART-003@2"
kind: research
stage: discover
branch_id: BR-001
document_status: final
validation_status: unvalidated
derived_from: ["artifact:ART-001@1"]
signoffs: []
stale_reason: null
---

# Research Plan · 创始人 IP 短视频放大器（r3 · Sprint 2 综合 + Insight Readiness）

## Research Objective

- **Charter 修订**：`artifact:ART-001@1`（本计划唯一正式输入；Initial Assessment 不作为证据，其 inspect-next 项仅作候选种子问题）
- **创新挑战（源自 Charter Challenge）**：中小企业老板做创始人 IP 短视频的三重困境——全部自己干则粗糙且耗时（剪辑最重）、找代运营则成本高且照样占用创始人时间、多数人随便发发没流量。如何以放大器模式（AI 干程序化工序 + 人做选择，覆盖选题/文案/剪辑/运营）把创始人的时间成本压到每天约 30 分钟工具互动并改善流量结果——未经验证。
- **研究边界（源自 Charter Scope + Constraints）**：范围内 = 面向四环节 copilot 的市场/用户/竞争/平台研究；首发人群 = 粗糙自干派中小企业老板；首发平台 = 微信视频号；素材输入 = 每周批量真人拍摄。范围外 = 全托管服务、代运营服务包、数字人替代真人、多平台矩阵（首发不锁定）。约束 = 产品作者个人时间与自有方法论起步、平台规则与接口的外部限制、AI 能力的现实水平。
- **战略不确定性（源自 Charter Unknown + Tensions）**：
  - U1 粗糙自干派的付费意愿与价位带
  - U2 放大器模式下"没流量"的实际改善幅度（方法论有效性）
  - U3 "每天 30 分钟"行为承诺的现实性
  - U4 AI 剪辑可达到的质感天花板
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

**已投影根假设**（r1 引入，derived_from = artifact:ART-003@1，均 impact=high × uncertainty=high → Achilles Heel，L4 durable obligation 即刻打开，行为证据由 dogfood 承接、与 Charter 首个成功信号一致）：

- **A-001**（magic/consumer）："产品作者的自有方法论（选题/文案/结构）能够显著改善粗糙自干派内容的流量结果——放大器承诺的核心。"证伪信号：外部证据显示企业主 IP 流量结果主要由人设/赛道/投放等非方法论因素决定，或同等方法论能力已被免费默认工具内置。
- **A-002**（money/commercial）："粗糙自干派中小企业老板对'每天 30 分钟全流程'放大器工具存在真实付费意愿，足以支撑订阅制 SaaS。"证伪信号：该人群工具付费率极低且付费集中于代运营服务而非工具，或价位带证据不成立。
- **A-003**（both/technical）："当前 AI 能力已足以把选题→文案→剪辑→发布的程序化工序压缩到每天约 30 分钟的真人互动内。"证伪信号：竞品/官方能力盘点显示关键工序（尤其剪辑质感）仍需大量人工，或单条生成成本使订阅经济不可行。

## Next Sprint

Sprint 2 后研究进入综合态：八个 Learning Objective 全部达到 answered / partial-with-explicit-gap / gap-accepted，desk 研究的边际战略学习已耗尽。剩余唯一活动为常设监控任务（非新 Sprint）：

```yaml
- id: RM-006
  learning_refs: [LP-004]
  evidence_needed: 即创/剪映/视频号官方能力与发布公告、新竞品进入"视频号×真人IP×全流程"组合的证据
  method_source_bundle: signal-monitoring（collection，ad-hoc：官方公告定向复查，每次 1-2 次检索）
  exclusions: 不做全面竞品复盘；不扩展新赛道扫描
  dependencies: []
  owner: coordinator
  bounded_budget: 每双周 1-2 次检索，持续 3 个月
  stop_condition: 出现"官方全流程能力进入视频号"或"新竞品占位组合空缺"信号即升级为 kill/竞争评估并回写本计划；3 个月无信号则降频
  expected_output: 简短信号备注（追加到 K-002 修订）
  limitation: 监控非穷尽；stealth 产品不可见
```

## Research Progress

```yaml
- learning_ref: LP-001
  answer_status: partial
  knowledge_refs: ["knowledge:K-004@1"]
  current_answer: 自干派瓶颈=全流程时间总和超预算数倍 × 正反馈延迟断更；单条新手 3-8h/熟练 1-2h 为综述值；老板对"AI 全包"期望已存在
  remaining_gap: 一手计时数据缺失（dogfood L4 承接）；无 live 访谈（out-of-band）
- learning_ref: LP-002
  answer_status: partial
  knowledge_refs: ["knowledge:K-005@1"]
  current_answer: 三层价位带结构（工具 ¥599-9800/年 × 服务 ¥1.5-3万/月 × 陪跑信任崩塌）；付费意愿存在但定价与定位强耦合
  remaining_gap: 付费行为验证（L4）；锚点选择=定位决策移交 Define
- learning_ref: LP-003
  answer_status: answered
  knowledge_refs: ["knowledge:K-001@1"]
  current_answer: 六组战略格局建立；空缺为组合空缺（视频号 × 创始人真人 IP × 全流程 copilot 无人占位）而非功能空缺
  remaining_gap: RM-006 常设监控承接
- learning_ref: LP-004
  answer_status: partial
  knowledge_refs: ["knowledge:K-002@1"]
  current_answer: kill signal 未触发但半触发：字节系（即创）全流程能力已存在、未进视频号；官方一条龙全部平台绑定且数字人导向
  remaining_gap: RM-006 双周×3 月监控
- learning_ref: LP-005
  answer_status: answered
  knowledge_refs: ["knowledge:K-003@1"]
  current_answer: 视频号无第三方发布 API（不可合规全自动发布）；AI 标识 2025-09 起强制；数字人受限/真人被鼓励；双推荐引擎社交裂变优先
  remaining_gap: 政策时效随 RM-006 一并观察
- learning_ref: LP-006
  answer_status: answered
  knowledge_refs: ["knowledge:K-006@1"]
  current_answer: 五类组件（结构/选题/拆解/视频号社交特化/AI×方法论先例）公开可组合=工程可行；但组件商品化→A-001 弱侧面支持+边界收窄（价值在组合×数据闭环，不在组件）
  remaining_gap: 组件效果无公开数据；A-001 本体验证=dogfood L4
- learning_ref: LP-007
  answer_status: gap-accepted
  knowledge_refs: []
  current_answer: 公开源确认不存在一手时间投入统计与同类工具使用时长数据；行为可行性验证移交 dogfood L4（Charter 首个成功信号即承接载体）
  remaining_gap: dogfood 行为日志（环外，L4 durable obligation）
- learning_ref: LP-008
  answer_status: answered
  knowledge_refs: ["knowledge:K-007@1"]
  current_answer: 真人素材架构单条边际成本 ¥1-10、日更月成本 ¥30-300，工具锚价位带内毛利率充足；"成本使订阅不可行"证伪信号不触发；OpusClip 教训=按产出单位计价
  remaining_gap: 架构定型后精算；多轮交互 token 膨胀由 dogfood 顺带测量
```

## Sprint Decision

**Learned**：

- 方法论五类组件公开、结构化、可组合 → 产品化工程可行性高；"AI 找选题+人选择"哲学有公开先例（knowledge:K-006@1）
- 组件商品化（蝉妈妈 AI 拆解/SkillHub 文案/剪映模板）→ 通用方法论组件不构成差异化，护城河论证必须转向"组合调优 × 视频号社交特化 × 数据闭环"（knowledge:K-006@1）
- 单条边际成本量级 ¥1-10、日更月成本 ¥30-300：真人素材架构下订阅经济成立，架构约束与经济约束同向锁定真人路线（knowledge:K-007@1）

**Resolved（Sprint 1 保留矛盾的收敛）**：K-005 的"订阅 SaaS ↔ 工具低锚点"矛盾，经 K-007 排除经济不可行解释后，**收敛为纯定位选择**（工具锚 ¥50-800/月 vs 服务替代锚更高位定价）——这是 Define 阶段的战略选择输入，不再属于研究可裁决项。

**Reframed**：

- A-001 边界收窄：从"自有方法论有效吗"到"组合×数据闭环能否跑赢商品化组件"（knowledge:K-006@1）
- A-003 半验证态：能力面（官方一条龙存在、程序化工序可压缩，knowledge:K-001@1/knowledge:K-002@1）+ 成本面（可行，knowledge:K-007@1）已清；唯行为面（30min 真人互动）留 dogfood L4（LP-007 gap-accepted）

**Decision**: `synthesize`——desk 研究边际学习耗尽（4C+Technology+Economics 全镜头处置完毕，剩余不确定性全部为 L4 行为证据或 Define 阶段战略选择），Insight Readiness 达成，研究循环收口；仅保留 RM-006 常设监控。

## Insight Ingredients and Insight Readiness

**Insight Readiness 判定：达成**（8/8 Learning Objective 处置：answered ×4、partial-with-explicit-gap ×2、gap-accepted ×1；根假设 A-001 弱侧面+收窄、A-002 方向+矛盾定位化、A-003 能力/成本面已清行为面留 L4；剩余不确定性均不可由 desk 研究消解）。以下为移交 `bw-define` 的 Insight Ingredients（候选原料，非结论）：

- **Patterns（证据支持的 pattern）**：组合空缺——"视频号×创始人真人IP×全流程copilot"无人占位，功能链本身已被大厂填满（knowledge:K-001@1）；信任缺口——服务付费意愿高但对人力交付信任崩塌，"AI 程序化+人选择"恰好落在缺口上（knowledge:K-005@1）；断更主因——瓶颈是时间总和×正反馈延迟，非单点技能（knowledge:K-004@1）
- **Tensions（张力）**：定价锚两极（工具锚 ¥50-800/月 vs 服务替代锚 ¥3000+/月）（knowledge:K-005@1, knowledge:K-007@1）；"人点发布"硬约束 vs 运营自动化承诺（knowledge:K-003@1）；"让他选择"vs 选择即最贵时间（Charter T2，行为面未证，LP-007 gap）
- **Anomalies（反常）**：陪跑信任崩塌与代运营混乱并存，但老板仍在为 IP 结果持续付大钱（knowledge:K-005@1）；视频号 API 缺失同时是竞品护城河与自身自动化枷锁（knowledge:K-002@1, knowledge:K-003@1）
- **Challenged beliefs（被挑战的既有认知）："端到端功能空缺"→实为组合空缺（knowledge:K-001@1）；"自干派缺技能"→缺时间预算与正反馈（knowledge:K-004@1）；"自有方法论=护城河"→组件已商品化，壁垒在组合×数据（knowledge:K-006@1）
- **Reframe candidates（重构候选）**：放大器=断更解药而非效率工具；运营环节=合规半自动+社交裂变设计（面向"值得点赞"而非算法）；定价=服务替代逻辑对标全案 1/5-1/3（knowledge:K-003@1, knowledge:K-004@1, knowledge:K-005@1）
- **Strategic relevance（战略相关性）**：wedge 候选=组合空缺位（视频号首发成立，kill signal 半触发需 RM-006 监控）；商业化候选=按产出单位计价的订阅，锚点选择待 Define；方法论产品化候选=垂直组合+数据闭环优先（knowledge:K-001@1, knowledge:K-002@1, knowledge:K-006@1, knowledge:K-007@1）
- **Remaining uncertainty（移交的剩余不确定性）**：L4 行为证据三缺口（30min 互动时长、dogfood 流量改善、付费行为）；RM-006 吞噬监控；政策时效（knowledge:K-003@1）
