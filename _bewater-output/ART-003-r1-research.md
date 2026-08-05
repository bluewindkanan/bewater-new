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
  - artifact:ART-002@1
  - assumption:A-001@1
  - assumption:A-002@1
  - assumption:A-003@1
  - assumption:A-004@1
signoffs: []
stale_reason: null
---

# Research · ART-003 r1 · 百度智能云 AI 硬件 token 业务

> Revision 1 仅含 Current Discover Plan；Latest Research Sprint 与 Research Sprint Debrief 在执行后随下一追加 revision 写入。

## Current Discover Plan

### 1. Discovery mission and decision

- **Core exploration question:** 在我们敢于对"以推理成本优势向 AI 眼镜/可穿戴 OEM 卖 token"这一方向下注（或否定它）之前，必须先搞清楚：OEM 今天到底是怎么解决模型推理的、真实痛点与可接受价格区间是什么，以及在不依赖 Apollo/小度既有生态杠杆的前提下，百度能否触达并说服这群客户？
- **Provisional proposition（待验）：** B2B 卖 token 给 AI 眼镜/可穿戴 OEM，押推理成本/基础设施优势。
- **Research boundary:** 仅做方向性的事前调查——澄清假设的可证伪证据需求与优先级，不在 Discover 阶段确定 SDK 形态、定价表、商业分成、签约客户、方案塑造。
- **Decision this research must inform:** G1（Strategy Gate）能否判定方向继续——具体地，A-001/A-002/A-003 这 3 条 Achilles Heel 是否能从 L1 上升到 L4+ 行为证据支撑；A-004（市场规模）是否成立。

### 2. Formal inputs and priorities

- **Charter head:** `artifact:ART-001@1`
- **Active root assumptions:** `assumption:A-001@1`, `A-002@1`, `A-003@1`, `A-004@1`
- **Advisory reference:** `artifact:ART-002@1`（Initial Assessment，**仅作 candidate，不构成 Fact / Evidence / Insight**）

**Risk priority order（impact × uncertainty + L4 义务）：**

| 优先级 | 假设 | 类型 | L4 义务 | 证伪信号 |
|---|---|---|---|---|
| P0 | A-001（OEM 普遍外采） | consumer / magic | durable | 头部 OEM 已自建或长期独家锁定友商 |
| P0 | A-002（成本优势构成可感知差异化） | commercial / money | durable | 同等条件下 OEM 不视价格为决策因素，或友商报价更低 |
| P0 | A-003（价格-成本结构双方可持续） | commercial / money | durable | OEM 接受报价但毛利低于底线，或为抢量被迫持续降价 |
| P1 | A-004（赛道出货量足以支撑独立业务） | commercial / money | — | 出货量持续低位、单品调用量不足 |

**Beliefs to challenge（来自 Charter + Assessment CI，均为 candidate）：**
- B1：AI 眼镜/可穿戴 OEM 普遍需要外采而非自建模型推理。（CI-1 反向质疑：是先有战略再选 greenfield 品类，pull 是否真实存在？）
- B2：百度云的成本优势在眼镜场景能被 OEM 可感知。（CI-3：消费侧免费化 + API 价格下行，单位毛利双向挤压。）
- B3：在不依赖 Apollo/小度的前提下百度能触达 AI 眼镜/可穿戴 OEM。（CI-2：第三方 token 供给的真实生态位可能是"非阵营 OEM 的备选推理源"，而非品类级基础设施。）

### 3. 4C coverage map

| C | 起始问题 | 优先级 | 覆盖状态 | 证据需求 | 接受的 gap |
|---|---|---|---|---|---|
| **Consumer**（OEM 决策人） | 谁在 OEM 内部决定采购 token 推理？他们的痛点、采购周期、自建/外采的真实原因？ | P0 | planned | 一手 OEM 访谈（产品/技术决策人）+ 二手案例 | "决策链与采购周期"暂接受为 Unknown，待 Sprint 后修订 |
| **Company**（百度） | 不依赖 Apollo/小度的前提下，百度能用什么触达这群客户？单位推理成本对 OEM 报价的可传导性？ | P0 | planned | 内部成本/产能数据 + 友商报价对照 | "现有 B 端商务对眼镜 OEM 的覆盖度"暂接受为 Unknown |
| **Category** | AI 眼镜/可穿戴 2026+ 出货量、单品 AI 调用量、自建 vs 外采比例、友商报价曲线？ | P1 | planned | IDC/Counterpoint 等二级数据 + 友商公开报价 | 国内 OEM 自建比例的精确数字可能不可得 |
| **Channel** | OEM 如何评估、集成、采购 token/API 推理供给？通过云市场、直客、方案商？ | P1 | planned | 二手流程案例 + 一手访谈 | 暂接受为 Unknown |

### 4. Evidence strategy

- **research_mode:** `secondary_first` —— 先用低成本二手证据快速收紧 P1（A-004 赛道规模）与 P0 中的可二手部分（友商报价曲线、自建/外采案例）；当二手无法回答 P0 的行为面（OEM 真实决策与可感知差异化）时，按 Primary Trigger 升级到一手研究。**Primary research is not mandatory**；每条 Primary Trigger 记录"何时该被点燃"以及"无主授权时不执行"。
- **Constraints:** 每条 evidence record 必须保留 `evidence_origin`（primary/secondary）+ `evidence_form`（behavior/self-report/expert-judgment/market-data/document）+ source 引用 + limitation；写入 `_bewater/evidence.yaml`（首次写入即创建 envelope）。**分析框架（competitive-positioning / five-forces / value-chain 等）只组织证据，本身不构成证据。**
- **Evidence targets:** 至少能分别给 A-001 / A-002 / A-003 提供一条 L2 secondary 以上的源；A-004 至少 2 条独立二手源三角验证。L4+ 行为证据（POC / 联合测价 / 一手访谈）作为 G1 前的 stretch goal，按 Primary Trigger 推进。
- **Evidence limitations:** 二手市场数据存在 recency/transferability 弱点；专家判断不等于行为证据；OEM 自报数据存在 desirability bias；任何 Assessment 引用、模型推断、self-report 在未获行为证据前保持 candidate 身份。
- **Primary Triggers:**
  - **PT-1（点燃条件：二手无法判定 A-001 的外采比例）→** 一手 OEM 访谈 ≥5 家代表性 AI 眼镜/可穿戴厂商（覆盖产品/技术决策人）。无主授权不执行。
  - **PT-2（点燃条件：A-002 在二手对照后仍无法判定 OEM 可感知差异）→** OEM 侧联合测价 / POC（百度 vs 友商 同等 token/延迟/SLA 条件下 OEM 偏好）。需要商务渠道授权。
  - **PT-3（点燃条件：A-003 内部数据可得性允许）→** 百度云单位推理成本曲线对 OEM 报价的可传导性测算（internal-document-review + 财务模型）。需要内部数据访问授权。

### 5. Research missions（next Sprint 候选）

> 下列 missions 均为 candidate；本 Plan 仅记录"证据需求—方法—预期—限制—停止条件"，不在本 revision 执行。执行后写入 ART-003 r2 的 Latest Research Sprint。

#### Mission M1 · 友商 token 报价 + SLA 横向对照

- **Question:** 在 AI 眼镜/可穿戴典型调用模式（多模态/低延迟/中等上下文）下，OpenAI / Anthropic / 智谱 / 月之暗面 / 阿里通义 / 腾讯混元 / 字节豆包 等友商的 token 报价与 SLA 处于什么位置？
- **Evidence need:** P0，A-002 / A-003。需要"同等条件下价格-性能对照"的市场数据。
- **Method / Framework:** `desk-research` (collection) + `competitive-positioning` (analysis framework)。
- **Execution need:** 公开报价页、官方文档、行业报价聚合（如 pricepertoken）。
- **Rationale:** 押"成本优势"成立与否，先要确认友商价格曲线在哪儿；这是二手能直接回答的部分。
- **Expected output:** 一张友商报价-延迟-上下文-多模态对照表；初判百度相对位置。
- **Limitation:** 公开报价不反映大客户真实成交价；SLA 承诺 ≠ 实际履约。
- **Owner / dependency:** Discover agent（无需用户主授权即可执行）。
- **Stop condition:** 收集到 ≥3 家国内外主流友商在可比 token 单位下的公开报价 + 至少 1 项 SLA 维度即可结束本 mission。

#### Mission M2 · AI 眼镜/可穿戴品类出货量 + 单品 AI 调用量三角验证

- **Question:** 2024-2027 全球与中国 AI 眼镜/可穿戴出货量预测？单品 AI 调用量量级（次/日/设备）？多模态占比？
- **Evidence need:** P1，A-004。三角验证赛道上限。
- **Method / Framework:** `desk-research` (collection) + `analogy-scan` (analysis framework，对照智能音箱/手机早期品类)。
- **Execution need:** IDC / Counterpoint / Strategy Analytics / Counterpoint / Yicai Global 等公开报告。
- **Rationale:** A-004 的 uncertainty 是 medium，二手可得性较高，是最便宜的 P1。
- **Expected output:** 出货量与调用量区间 + 单品 AI 调用量假设的三角验证结果。
- **Limitation:** 中国分品类数据稀缺；厂商未公开激活/调用数据，需要用类比+逆向推算。
- **Owner / dependency:** Discover agent。
- **Stop condition:** ≥2 家独立二手源 + 1 个类比品类交叉验证即可。

#### Mission M3 · OEM 自建 vs 外采现状（二手案例扫描）

- **Question:** Ray-Ban Meta、Google Glass、Apple Vision Pro、Rokid、雷鸟、INMO、Looktech、小度AI眼镜等代表性 OEM 当前在模型推理上是怎么做的？自建 / 友商独家 / 多源？
- **Evidence need:** P0，A-001。在 PT-1 点燃前，先用二手案例扫描把"自建 vs 外采"的现状摸清。
- **Method / Framework:** `desk-research` (collection) + `ecosystem-map` (analysis framework)。
- **Execution need:** 厂商公开资料、技术架构披露、行业会议演讲、第三方拆解报告。
- **Rationale:** 一手访谈门槛高，先看公开信息能否回答 A-001 的核心证伪信号（头部 OEM 普遍自建/锁定）。
- **Expected output:** 一张代表性 OEM × 推理供给来源的对照表；初判 A-001 证伪信号是否已部分显现。
- **Limitation:** 公开资料偏向头部厂商；中小厂商的私有合作不透明。
- **Owner / dependency:** Discover agent。
- **Stop condition:** ≥5 家代表性 OEM 的推理供给来源有公开证据或可信推断即可。

#### Mission M4 · 百度云 ERNIE 推理成本曲线与 OEM 报价的可传导性（preliminary，内部数据驱动）

- **Question:** ERNIE 主力模型在眼镜/可穿戴典型 token 量级下的单位推理成本大致量级？价格下行曲线？对 OEM 报价的可传导空间？
- **Evidence need:** P0，A-003（前置）。需要回答"价格-成本结构双方可持续"的成本侧。
- **Method / Framework:** `internal-document-review` (collection) + `value-chain` (analysis framework)。
- **Execution need:** 百度云公开报价页 + 内部成本/产能数据（需主授权）。
- **Rationale:** A-003 的成本侧一半在百度内部；先确认公开层面能算到哪儿，再决定 PT-3 是否点燃。
- **Expected output:** 单位推理成本量级估算 + 价格传导空间初步判断。
- **Limitation:** 内部数据未授权前只能用公开报价推算，存在 underdetermined。
- **Owner / dependency:** Discover agent（公开部分）+ 内部数据访问授权（PT-3 点燃后）。
- **Stop condition:** 公开层面能形成量级判断 + 标注内部数据缺口即可（不必精确到毛利数字）。

> **不在本 Sprint 执行：** PT-1 一手 OEM 访谈、PT-2 联合测价/POC——这两项需要用户主授权与商务渠道协同，由后续 Sprint 按触发条件推进。

---

*本 Plan 由 Discover capability 起草，未签 signoff，未达到 Insight / Fact / Evidence 身份。Revision 1 不含 Sprint 执行结果；执行后写入 ART-003 r2 的 Latest Research Sprint 与 Research Sprint Debrief。*
