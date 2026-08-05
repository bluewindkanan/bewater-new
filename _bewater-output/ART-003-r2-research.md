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
  - artifact:ART-002@1
  - assumption:A-001@1
  - assumption:A-002@1
  - assumption:A-003@1
  - assumption:A-004@1
signoffs: []
stale_reason: null
---

# Research · ART-003 r2 · 百度智能云 AI 硬件 token 业务

> r2 = r1 的 Current Discover Plan（更新）+ Latest Research Sprint（M1~M4 执行结果）+ Research Sprint Debrief（含 Plan Delta）。旧 Plan 快照保存在 r1。

## Current Discover Plan（r2 更新）

### 1. Discovery mission and decision

- **Core exploration question（不变）：** 在我们敢于对"以推理成本优势向 AI 眼镜/可穿戴 OEM 卖 token"这一方向下注（或否定它）之前，必须先搞清楚：OEM 今天到底是怎么解决模型推理的、真实痛点与可接受价格区间是什么，以及在不依赖 Apollo/小度既有生态杠杆的前提下，百度能否触达并说服这群客户？
- **Decision（不变）：** G1（Strategy Gate）能否判定方向继续——具体地，A-001/A-002/A-003 三条 Achilles Heel 是否能从 L1 上升到 L4+ 行为证据支撑；A-004（市场规模）是否成立。

### 2. Formal inputs and priorities（不变）

- **Charter head:** `artifact:ART-001@1`
- **Active root assumptions:** `assumption:A-001@1`、`A-002@1`、`A-003@1`、`A-004@1`（**validation_status 仍为 untested；本 Sprint 不修改 ledger**）
- **Advisory:** `artifact:ART-002@1`（仅 candidate）

**Risk priority order（不变）：** P0 = A-001 / A-002 / A-003（durable L4 义务）；P1 = A-004。

### 3. 4C coverage map（r2 更新）

| C | 起始问题 | 优先级 | 覆盖状态（r1 → r2） | 主要证据 | 接受的 gap |
|---|---|---|---|---|---|
| **Consumer**（OEM 决策人） | 谁决定采购 token 推理？痛点？自建/外采原因？ | P0 | planned → **部分 evidenced**（sourcing 模式清晰，transacted price 未知） | E-009~E-015（7 家 OEM 的 sourcing 路径） | 决策链细节、成交价、采购周期 — Unknown，待 primary |
| **Company**（百度） | ERNIE 单位推理成本曲线？OEM 报价可传导空间？ | P0 | planned → **部分 evidenced**（公开刊例价 + 价格曲线可得；内部成本/毛利仍未知） | E-016~E-018（ERNIE 定价 + 价格战） | 内部成本/产能数据 — 需 PT-3 授权 |
| **Category** | 出货量？单品调用量？自建 vs 外采比例？ | P1 | planned → **evidenced**（出货量与增长曲线由 IDC + Counterpoint 三角验证） | E-006、E-007（IDC、Counterpoint） | 单品 AI 调用量无公开数据；类比锚点（智能音箱 Alexa+）仅作量级 |
| **Channel** | OEM 如何评估/集成/采购 token 推理？ | P1 | planned → **gap-accepted** | （本轮未单独采集） | 公开案例稀缺；sourcing 路径已在 Consumer 项下部分覆盖 |

### 4. Evidence strategy（r2 更新）

- **research_mode：** `secondary_first` → **本轮结束于 secondary 阶段；下一步建议 synthesize**，若 Insight Craft 后仍有未答 P0 行为面，则点燃 PT-1/PT-2。
- **Evidence targets 完成情况：**
  - A-001：≥1 条 L2 secondary ✓（7 家 OEM sourcing 案例）
  - A-002：≥1 条 L2 secondary ✓（5 条友商 + ERNIE 报价）
  - A-003：≥1 条 L2 secondary ✓（ERNIE 定价 + 价格战曲线）
  - A-004：≥2 条独立 secondary 三角验证 ✓（IDC + Counterpoint + Amazon 类比）
- **L4+ 行为证据：** 本轮未采集（PT-1/2/3 均未触发）；Achilles Heel 的 L4 义务仍未关闭。
- **Primary Triggers 状态：**
  - PT-1（OEM 一手访谈）：**not-triggered**（二手已能部分回答，但 transacted price 与决策链细节仍需 PT-1）。
  - PT-2（联合测价 / POC）：**not-triggered**（A-002 的"可感知差异化"在二手层面无法判定，需 OEM 侧行为证据）。
  - PT-3（百度云内部成本数据）：**not-triggered**（公开刊例价可得，内部单位成本/产能数据需主授权）。

### 5. Research missions（r2 状态）

| Mission | 状态 | 目标假设 | 关键证据 | 下一动作 |
|---|---|---|---|---|
| M1 友商 token 报价 + SLA 对照 | ✓ complete | A-002 | E-001~E-005 | 关闭；细分多模态 token 权重留作 deepen |
| M2 出货量 + 调用量三角验证 | ✓ complete | A-004 | E-006~E-008 | 关闭；单品调用量无二手数据，进入 unresolved |
| M3 OEM 自建 vs 外采现状 | ✓ complete | A-001 | E-009~E-015 | 关闭；transacted price 进入 unresolved → 候选 PT-1 |
| M4 ERNIE 成本曲线 + 可传导性 | ✓ complete | A-003 | E-016~E-018 | 关闭；内部成本数据进入 unresolved → 候选 PT-3 |

**新增 / 候选 mission（不在本轮执行）：**
- M5（候选，需主授权）：5 家 targeted OEM 的 procurement/BD 访谈 → 回答 transacted price、决策链、采购周期；点燃即关闭 PT-1。
- M6（候选，需商务渠道授权）：OEM 侧联合测价 / POC → 回答 A-002 的"可感知差异化"；点燃即关闭 PT-2。
- M7（候选， deepen）：多模态 token（图/视频/音频）在眼镜场景的计费权重与最优路由策略 → 回答 deepen#2 与 Q-NEW-4。

### 6. Stop rule（r2 决策）

**Next action: `synthesize`。** 4 个 secondary mission 全部 stop condition 达成，4 个 assumption 均有 ≥1 条 L2 secondary 证据覆盖；继续 desk-research 边际收益降低，主要缺口需 primary 才能闭合。建议下一步进入 `bw-insight-craft`，将 18 条 candidate evidence 合成为候选 Insight Portfolio；同时向用户呈现 PT-1/PT-2/PT-3 的点燃选项，由用户决定是否在 Insight Craft 之前/之中授权一手研究。

## Latest Research Sprint（Sprint 1）

### Reviewed mission selection

执行了 r1 Plan 中全部 4 个 candidate missions（M1~M4），全部为 secondary desk-research，无需主授权。

### Work actually executed

| Mission | 工具 | 主要来源数 | Stop condition |
|---|---|---|---|
| M1 | WebSearch + WebFetch | 5（OpenAI / Anthropic / Google / 智谱 / OpenAI Scale Tier） | ✓ ≥3 vendor + ≥1 SLA 维度 |
| M2 | WebSearch + WebFetch | 3（Counterpoint / IDC / Amazon Alexa+） | ✓ ≥2 独立源 + 1 类比 |
| M3 | WebSearch + WebFetch | 7（UploadVR / Apple ML / 财联社 / 中国网 / Fibocom / 百度官方 / YouTube） | ✓ ≥5 OEM |
| M4 | WebSearch + WebFetch | 3（百度千帆 ×2 / 新浪财经） | ✓ ≥1 ERNIE 型号 + 价格曲线 + 量级 |

**总计 18 条 evidence records（E-001~E-018）写入 `_bewater/evidence.yaml`。**

### Evidence references（按 mission）

- M1（A-002）：`evidence:E-001@1`、`E-002@1`、`E-003@1`、`E-004@1`、`E-005@1`
- M2（A-004）：`evidence:E-006@1`、`E-007@1`、`E-008@1`
- M3（A-001）：`evidence:E-009@1`、`E-010@1`、`E-011@1`、`E-012@1`、`E-013@1`、`E-014@1`、`E-015@1`
- M4（A-003）：`evidence:E-016@1`、`E-017@1`、`E-018@1`

### Deviations from the Plan

- **M1：** 混合 USD/CNY 报价，仅在单位 token 层面可比；多模态 token 计费权重未深入（留作 deepen）。
- **M2：** 单品 AI 眼镜日均调用次数 + 多模态 token 占比无公开二手数据；以智能音箱（Alexa+）作类比锚点。

## Research Sprint Debrief

### Learned

1. 海外 Tier-A 模型（GPT-4o $2.50/$10、Sonnet $3/$15、Gemini 2.5 Pro $1.25/$10）单位价格约为国内 ERNIE/GLM 刊例价的 6-30 倍；纯价格竞争对百度有利。
2. 国内 AI 眼镜 OEM 普遍选择"合作接入"而非自建；仅 Meta、Apple 全栈自建，Rokid 走多源混合路线。
3. 5 家代表性 OEM（Ray-Ban Meta / 小度 / 雷鸟 / INMO / Rokid）覆盖了三种 sourcing 模式（自建 / 独家绑定 / 多源），Meta 占全球 >70% 份额主导。
4. IDC 与 Counterpoint 两个独立源对 2024-2025 AI 眼镜增长量级一致（+110% / +167% YoY），AI 占比从 46% 升至 78%，赛道增长真实。
5. ERNIE Speed/Lite 免费 + 4.0 Turbo 2025-03 降价 85% → 百万台设备年成本可压至数十万元量级，OEM pass-through 空间充足。

### Unresolved

1. 单品 AI 眼镜日均调用次数 + 多模态 token 占比无公开二手数据 → 必须 primary。
2. Gemini 在中国大陆对 OEM 的可用性 / 合规路径未澄清。
3. Meta Muse Spark 取代 Llama 的具体性能/成本差异尚无公开数据。
4. ERNIE 免费 tier 是否有调用频次 / 速率限制未公开。
5. Apple Vision Pro 与纯 AI 眼镜架构类比的有效边界需进一步界定。

### Deepen（下一 Sprint 候选）

1. OEM 付费给大模型厂商的实际 transacted price（非刊例价）→ 需访谈或招标文件 → 即 PT-1。
2. 多模态 token（图/视频/音频）在眼镜场景下的实际计费权重 vs 文本。
3. Meta Muse Spark 的公开定价/性能 spec → 对国内 OEM 可对比基准。

### Drop

（无）

### New questions

- Q-NEW-1：眼镜 OEM 若多源混合（Rokid 模式），跨厂商路由的延迟/成本最优点在哪？
- Q-NEW-2：国内 OEM 对 ERNIE 免费 tier 的依赖度多高？百度若回调价格，代际切换成本？
- Q-NEW-3：Meta Muse Spark 若开放给第三方 OEM，是否会改变国内 sourcing 格局？
- Q-NEW-4：多模态（摄像头帧 + 音频流）在眼镜场景对 token bill 的真实倍数？

### Plan Delta

- **Priority changes：** P0/P1 排序不变；但 P0 的执行瓶颈已从"缺二手证据"转移到"缺一手行为证据"。
- **4C gap changes：** Consumer 部分 evidenced（sourcing 模式）+ Company 部分 evidenced（公开刊例价）+ Category evidenced（出货量）+ Channel 仍 gap-accepted。
- **Evidence strategy changes：** secondary 阶段告一段落；下一步若需进一步闭合 P0，必须点燃 PT-1（OEM 访谈）/ PT-2（联合测价）/ PT-3（内部成本数据）中的至少一条。
- **Mission changes：** M1~M4 关闭；新增候选 M5（targeted OEM 访谈）/ M6（POC）/ M7（多模态权重 deepen）。
- **Primary Trigger status：** PT-1/2/3 均 not-triggered；交由用户在 Insight Craft 前决定是否授权点燃。

### Next action

**`synthesize` → 建议路由到 `bw-insight-craft`。**

**Reason：** 4 个 secondary mission 全部达成 stop condition；18 条独立二手证据对 4 个 assumption 均形成 L2 secondary 支撑；继续 desk-research 边际收益递减，未答项必须靠 primary 闭合。Insight Craft 阶段应基于现有证据合成候选 Insight Portfolio，并明确标注哪些 Insight 因缺 L4 行为证据而只能停在 L2/L3（不可直接进入 G1 Go）。

---

*本 Sprint 仅产出 candidate evidence；未签 signoff；未升级任何 candidate 为 Fact / Accepted Belief / Insight；未修改 ledger 的 evidence_level / validation_status；未选择 gate exit。Insight Portfolio 的合成留给 `bw-insight-craft`。*
