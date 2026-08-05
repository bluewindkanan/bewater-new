---
schema_version: 1
artifact_id: ART-004
revision: 1
supersedes_ref: null
kind: insights
stage: discover
branch_id: BR-001
document_status: draft
validation_status: unvalidated
derived_from:
  - artifact:ART-001@1
  - artifact:ART-002@1
  - artifact:ART-003@1
  - artifact:ART-003@2
  - assumption:A-001@1
  - assumption:A-002@1
  - assumption:A-003@1
  - assumption:A-004@1
signoffs: []
stale_reason: null
---

# Insights · ART-004 r1 · 百度智能云 AI 硬件 token 业务

> 候选 Insight Portfolio，基于 Sprint 1 的 18 条 L2 secondary 证据。**所有 candidate 均未经人类 F/P/E/T 签署**；多数 T 维度因缺 L4 行为证据而停留在 candidate 态，需 PT-1/2/3 回收后升级。

## 1. Cognitive ladder

### Facts（直接观察，evidence_refs 见 §5）

- ERNIE 4.0 Turbo 刊例 30/60 元/1M（2025-03 降 85%）；Speed/Lite 自 2024-05 全面免费。（E-016、E-017）
- 海外 Tier-A 单位价格约为国内 ERNIE/GLM 刊例价 6-30 倍。（E-001~004）
- 2024 H2-2025 国内大模型价格战后段，超 7 成厂商回调涨价。（E-018）
- IDC + Counterpoint 三角验证：H1 2025 全球智能眼镜 +110% YoY，AI 占比 46%→78%，Meta >70% 份额。（E-006、E-007）
- 7 家代表性 OEM 中，仅 Meta、Apple 全栈自建；雷鸟独家通义、Rokid 多源、XREAL 双线、INMO 双模型、小度文心自建。（E-009~015）
- 文心 2024 日均调用 16.5 亿次。（M4 finding）

### Accepted Beliefs（Charter 与团队默认共识，待 challenge）

| AB | 内容 | 来源 |
|---|---|---|
| **AB-1** | 国内 AI 眼镜 OEM 普遍需要外采大模型推理（命题前提） | Charter A-001 |
| **AB-2** | 百度云推理成本优势构成 OEM 可感知差异化（核心押点） | Charter A-002、dual_sided.money |
| **AB-3** | 存在可持续毛利的 token 报价区间 | Charter A-003 |
| **AB-4** | AI 眼镜品类爆发支撑独立 token 业务 | Charter A-004 |
| **AB-5** | "卖 token" 是一个可独立计价的业务模型 | Charter 隐含 |

## 2. Candidate Insights

### IC-1 · 中国 OEM 选"外采"不是因"价格便宜"，而是因"自建不可承担"

> **针对 AB-1 / AB-2 的 challenge。**

Meta、Apple 全栈自建（端侧+云侧+模型+OS+硬件）是美元/硬件高端市场的特权；中国 OEM 即使年出货百万级也无法承担自建成本结构（人才 + 算力 + 多模态数据飞轮）。因此，**百度"押推理成本优势"的押点偏了**：真正的杠杆不是"我的 token 比友商便宜"，而是"中国 OEM 没有自建这条路可走"。竞争位的真正对手不是友商 token 价，是 OEM 的"自建冲动"——一旦 OEM 走自建（如小度走文心自建），任何 token 价都 irrelevant。

**F/P/E/T 评估：**

| 维度 | 评分 | 说明 |
|---|---|---|
| F（Fresh） | 强 | 把"外采需求"重新归因到"自建门槛"，而非 Charter 默认的"价格" |
| P（Potent） | 强 | 命中 A-001 的真正因果；重新定义竞争位与差异化方向 |
| E（Energizing） | 强 | 打开"中国 OEM 自建门槛"为锚点的产品策略（如降低切换成本、绑定硬件规格、阻止 OEM 自建） |
| T（Truth） | **candidate / L2-ceiling** | F-009/010 vs F-011~015 直接对照支持；但 OEM 视角的真实动机需 PT-1 L4 验证 |

**evidence_level：** L2 secondary ceiling；T 升级到 G1 ready 必须有 PT-1 OEM 访谈的行为证据。

---

### IC-2 · AI 眼镜 OEM 把"多源混合"作为对冲"未来被锁定"的默认策略

> **针对 AB-3 的 challenge；命中 distribution / 单 OEM 量级天花板。**

即使 ERNIE Speed/Lite 免费、4.0 Turbo 大幅降价，OEM 仍接入通义/智谱/豆包多源——因为它们预期百度价格会回调（事实上 2025 已回调，E-018）。多源不是临时方案，而是 OEM 的稳定运营哲学。**这意味着"独家绑定"（雷鸟模式）反而是 OEM 视角的脆弱结构**；任何"卖 token"业务必须接受 OEM 永远多源的现实，单 OEM 的 token 量天花板被多源结构天然限制。

**F/P/E/T 评估：**

| 维度 | 评分 | 说明 |
|---|---|---|
| F | 强 | 揭示"独家绑定"是供应商视角的幻觉，OEM 视角完全相反 |
| P | 强 | 重新定义 sales/forecast 模型——单 OEM 配额无法独占；多源编排放进产品策略 |
| E | 中-强 | 触发具体产品方向（多模型编排层、跨厂商路由）而非独家绑定产品 |
| T | **candidate / L2-strong** | E-010/012/013/015 多 OEM 直接行为证据；动机层面仍需 PT-1 确认 |

**evidence_level：** L2 secondary-strong（行为面证据密度最高）；PT-1 主要确认动机细节，不改变核心结论。

---

### IC-3 · "卖 token 给硬件"的真正终局是"硬件生态绑定"，不是"token 单价毛利"

> **针对 AB-3 / AB-5 的 challenge；合并 IC-window-closing + IC-analogy 的 Force Fitting。**

三股力量共同把"token 单价毛利"压缩到接近 0：
1. ERNIE Speed/Lite 已免费 + 4.0 Turbo 降 85%（E-016、E-017）
2. 国内价格战后段 7 成厂商涨价（E-018）——证明纯 token 商品化的死亡螺旋已显现，不可持续
3. OEM 多源避险（E-010、E-012、E-013、E-015）——价格不再是切换触发

历史类比坐标系：**地图 API（Apple Maps / 高德）、支付 API（微信支付 / Stripe）、推送 API（Firebase / 个推）都走完了同一条路**——从"按调用计费商品"演化为"平台免费 + 生态绑定"。百度的真正终局不是"卖更多 token"，而是"成为 AI 眼镜品类的默认推理基础设施 + 与头部 OEM 共建产品/渠道/数据/品牌"，**利润从生态 LTV 中产生，不从 token 单价中产生**。

**F/P/E/T 评估：**

| 维度 | 评分 | 说明 |
|---|---|---|
| F | 强 | 颠覆 Charter 的"卖 token"核心命题；类比视角打破现有框架 |
| P | 强 | 重新定义 G2 投资逻辑——看生态 LTV 而非 token 毛利 |
| E | 强 | 触发战略级 idea：与头部 OEM 共建、IP 共享、芯片层合作、数据飞轮共享 |
| T | **candidate / L2-medium** | 类比证据 + 价格战证据；但"终局"是预测性论断，需 PT-2 POC 验证 OEM 在生态绑定方案下的真实偏好 |

**evidence_level：** L2 medium；T 升级需要 PT-2 的"模拟决策"数据（OEM 在"纯 token 报价"vs"生态绑定方案"下的偏好）。

---

### IC-4 · AI 眼镜品类真正的产品空白是"端云协同推理栈 + OEM 友好的计费颗粒度"

> **针对 Charter Magic 侧的 challenge；填补 Assessment 的 "Most Promising Direction"。**

M3 的 7 家 OEM 案例显示：所有 OEM 都在解决"端侧算力/功耗约束 × 云侧多模态/低延迟"的协同问题，但没有一家把端云协同推理栈本身做成差异化（都在拼模型能力或商务条款）。**真正的产品空白不是"再做一个模型"，而是"贴合眼镜形态的端云协同推理栈 + OEM 友好计费颗粒度"**——这个空白没有任何厂商占领。ERNIE 的轻量化版本（如 ERNIE Speed）+ 百度云基础设施 + 多模态能力，组合起来正是占领这个空白的基础；但 Charter 把它定成"卖 token"反而掩盖了这个真正机会。

**F/P/E/T 评估：**

| 维度 | 评分 | 说明 |
|---|---|---|
| F | 强 | 重新框定产品机会——从"卖 token"到"卖端云协同栈" |
| P | 强 | 命中 Charter 的 Magic 缺口 + 拓展 Money 侧差异化 |
| E | 强 | 触发具体产品方向：端云模型编排、眼镜形态 SDK、按设备/按场景计费 |
| T | **candidate / L2-medium** | M3 案例显示空白存在；但 OEM 是否真愿为此付费需 PT-1 + PT-2 验证 |

**evidence_level：** L2 medium；T 升级需要 PT-1 第 8-9 题（非价格差异化）+ PT-2 盲测/集成人时数据。

## 3. F/P/E/T 汇总

| ID | F | P | E | T | 状态 | 升级 G1 所需 |
|---|---|---|---|---|---|---|
| IC-1 | ✓ | ✓ | ✓ | L2 ceiling | candidate | PT-1 OEM 访谈（自建门槛视角） |
| IC-2 | ✓ | ✓ | ✓- | L2 strong | candidate（最接近 ready） | PT-1 OEM 访谈（动机细节） |
| IC-3 | ✓ | ✓ | ✓ | L2 medium | candidate | PT-2 POC（生态绑定模拟决策） |
| IC-4 | ✓ | ✓ | ✓ | L2 medium | candidate | PT-1 第 8-9 题 + PT-2 集成人时数据 |

**所有 candidate 当前 evidence_level 上限 = L2 secondary**；任何一条要进入 G1 Go 判断，必须由 PT-1/PT-2 回收的 L3/L4 行为证据升级 T 维度，并由人类 F/P/E/T signoff。

## 4. 降级与未入选

| 候选 | 处理 | 原因 |
|---|---|---|
| "AI 眼镜品类爆发" | 降级为 Fact（AB-4） | F 失败——已是行业共识 |
| "百度单位成本全球领先" | 降级为 Fact（待证） | F 失败——已是 Charter 押点；需 PT-3 内部数据升级 |
| "文心 16.5 亿次/日 内外部结构未公开" | 转为 Open Question | 不是 insight，是 critical Unknown——影响起点判断 |
| "Meta Muse Spark 开放给第三方会改变格局" | 转为 Watchlist | 条件性 insight——若发生再激活 |

## 5. Evidence refs 映射

| IC | 关键证据 |
|---|---|
| IC-1 | E-009、E-010（自建案例） + E-011~015（合作接入案例） |
| IC-2 | E-010（Rokid 多源） + E-012（Rokid/小度） + E-013（XREAL 双线） + E-015（INMO 双模型） + E-018（价格回调） |
| IC-3 | E-016、E-017（ERNIE 免费/降价） + E-018（价格战反转） + E-001~004（海外 vs 国内价格对照） |
| IC-4 | E-009~015（7 OEM 案例显示端云协同栈未被差异化） + E-017（Speed 轻量化适配端侧） |

## 6. Open Questions（待 PT/后续 Discover 解答）

- **OQ-1：** 百度文心 16.5 亿次/日 调用中，外部分发 vs 内部循环（搜索/小度/Ernie Bot）的结构比例？这决定"卖 token 给硬件"是从已有外部基础扩展，还是从零建外部销售能力。
- **OQ-2：** Meta Muse Spark 是否会开放给第三方 AI 眼镜 OEM？若开放，对国内 sourcing 格局的冲击？
- **OQ-3：** 百度智能云现有 BD 渠道对 AI 眼镜 OEM 的覆盖度？决定 PT-2 POC 能否真正发起。

## 7. Human decision authority

**F/P/E/T signoff 权属于：G1 strategy-gate 的 accountable person（当前 `decision_authority.G1.accountable_person: null`，需在 G1 前明确）。**

候选 Insights 现处于"draft / unvalidated"状态，**未签 signoff**。任何 candidate 在 G1 Go 判断前必须：
1. 由 PT-1/PT-2/PT-3 回收的 L3/L4 证据升级 T 维度
2. 由 G1 accountable person 在当前 revision 上 F/P/E/T signoff

本 capability 在此前停止。

---

*本 artifact 是 candidate Insights 草案；未签 signoff；未升级任何 Fact / Accepted Belief 为 Insight；未修改 ledger 的 evidence_level / validation_status；未生成 directional hypothesis（属于 Define 阶段）；未选择 gate exit。下一步路由：用户决策——执行 PT-1/2/3 升级证据后回到 Insight Craft 修订 r2，或先进入 Define 起 directional hypothesis（但需接受当前 Insights 仍 L2 的限制）。*
