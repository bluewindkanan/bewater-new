# BeWater Toolkit 工具分类与边界

> **SUPERSEDED** — 历史草稿，已按 `2026-08-14-toolkit-implementation-decision.md` 实现。仅供回溯，不是实现设计。

## 版本信息
- **版本**: 1.0
- **日期**: 2026-08-14
- **状态**: Draft

---

## 一、什么是"研究方法工具"？

### 定义

**研究方法工具** = 用来获取、分析、验证证据，或综合洞察的具体操作或框架。

**关键特征**：
1. **有输入**：需要特定类型的证据或数据
2. **有输出**：产生特定类型的证据、分析或洞察
3. **可执行**：有明确的执行步骤或分析方法
4. **可重复**：不同人/时间使用相同方法可产生类似结果

---

## 二、当前 35 个方法的分类与用途

### 2.1 证据收集

| 工具 | 用途 | 什么时候用 | 输入 | 输出 |
|------|------|-----------|------|------|
| desk-document-research | 从公开文档建立背景 | 需要行业/竞品信息 | 文档 | 文档发现 |
| internal-document-data-review | 审查内部能力/约束 | 需要了解内部情况 | 内部文档 | 内部证据 |
| company-product-competitor-audit | 审计公司和竞品 offer | 需要竞争情报 | 产品/服务 | offer 清单 |
| literature-patent-standards-search | 搜索文献/专利/标准 | 需要技术/监管信息 | 数据库 | 文档证据 |
| behavioral-transaction-data-review | 分析行为/交易数据 | 有用户行为数据 | 数据日志 | 行为模式 |
| social-review-discourse-analysis | 分析评论/话语 | 需要用户反馈 | 社交媒体 | 话语证据 |
| stakeholder-interviews | 通过访谈学习/测试 | 需要一手信息 | 访谈对象 | 访谈记录 |
| contextual-observation | 捕获情境观察 | 需要看真实使用场景 | 场景 | 观察记录 |
| usability-demo-experiment-poc | 检查可用性/演示/实验 | 有产品可用性证据 | 产品 | 可用性发现 |

**是否应该在 Toolkit？** ✅ 是，这些都是标准的数据收集方法

---

### 2.2 证据分析

| 工具 | 用途 | 什么时候用 | 输入 | 输出 |
|------|------|-----------|------|------|
| market-sizing-triangulation | 从多角度市场估算 | 需要市场规模 | 多个数据源 | 规模估算 |
| segmentation-decision-unit | 细分+决策单元分析 | 需要理解客户 | 用户数据 | 细分模型 |
| competitive-benchmarking | 竞争对标和定位 | 需要竞争定位 | 竞品信息 | 定位图 |
| five-forces | 五力评估行业结构 | 需要行业吸引力分析 | 行业信息 | 五力模型 |
| value-chain-profit-pool | 价值链+利润池映射 | 需要知道价值在哪 | 公司数据 | 价值链图 |
| ecosystem-channel-map | 生态系统和渠道映射 | 需要理解生态 | 生态信息 | 生态图 |
| jtbd-journey | JTBD+旅程分析 | 需要理解用户需求 | 用户研究 | JTBD 模型 |
| pricing-unit-economics | 定价和单位经济分析 | 需要商业可行性 | 成本/价格数据 | 经济模型 |
| trend-weak-signal-structural | 趋势/弱信号/结构分析 | 需要预测未来 | 趋势数据 | 趋势图 |
| technology-maturity-capability | 技术成熟度和能力评估 | 需要技术分析 | 技术信息 | 成熟度图 |
| scenario-analogy-causal | 构建场景/类比/因果模型 | 需要预测多种未来 | 趋势/数据 | 场景模型 |

**是否应该在 Toolkit？** ✅ 是，这些都是标准的分析框架

---

### 2.3 假设验证

| 工具 | 用途 | 什么时候用 | 输入 | 输出 |
|------|------|-----------|------|------|
| source-family-triangulation | 跨独立来源三角验证 | 需要验证证据可靠性 | 多个来源 | 验证状态 |
| negative-case-search | 反例/证伪搜索 | 需要挑战假设 | 假设+数据 | 反例 |
| contradiction-analysis | 矛盾分析（保留冲突） | 发现证据冲突 | 冲突证据 | 矛盾清单 |
| sensitivity-boundary-check | 敏感性和边界检查 | 需要测试假设健壮性 | 假设+参数 | 敏感度 |
| alternative-explanation-testing | 排他解释测试 | 需要验证因果 | 推断+数据 | 解释清单 |
| evidence-strength-transferability | 证据强度和迁移性检查 | 需要判断证据质量 | 证据 | 质量评分 |

**是否应该在 Toolkit？** ✅ 是，这些都是标准的验证方法

---

### 2.4 洞察综合

| 工具 | 用途 | 什么时候用 | 输入 | 输出 |
|------|------|-----------|------|------|
| pattern-anomaly-detection | 模式和异常检测 | 需要从证据找模式 | 证据集合 | 模式/异常 |
| accepted-belief-challenge | 挑战未检验的共识 | 需要发现盲点 | 共识 | 被挑战的信念 |
| belief-shift-mapping | 信念迁移映射 | 需要理解变化 | 前后证据 | 迁移图 |
| tension-finding | 张力发现（竞争证据） | 需要发现矛盾 | 证据集合 | 张力清单 |
| structural-reframe-generation | 结构性重构生成 | 需要重构框架 | 多个 lens | 重构候选 |
| cross-lens-collision | 跨 lens 碰撞（4C+扩展） | 需要多角度碰撞 | 多 lens | 碰撞发现 |
| strategic-relevance-mapping | 战略相关性映射 | 需要关联未来选择 | 证据+战略 | 相关性图 |

**是否应该在 Toolkit？** ✅ 是，这些都是标准的综合方法

---

## 三、什么不是"研究方法工具"？

### 3.1 流程 / 程序

❌ **不应该作为 Toolkit 条目，但应该作为研究流程的一部分**：

| 名称 | 用途 | 为什么不是工具 |
|------|------|--------------|
| Living Learning Plan | 迭代研究问题 | 是流程，不是具体方法 |
| Sprint | 研究 Sprint 循环 | 是时间盒，不是方法 |
| Daily Debrief | 每日简报 | 是仪式，不是方法 |
| Research Debrief | 研究简报 | 是仪式，不是方法 |
| Diverge & Converge | 发散和收敛节奏 | 是流程模式，不是方法 |

**正确位置**：应该在 Research Plan / Sprint 流程中说明，不在 Toolkit 中

---

### 3.2 模板 / 表格

❌ **不应该作为 Toolkit 条目，但应该作为模板提供**：

| 名称 | 用途 | 为什么不是工具 |
|------|------|--------------|
| Money+Magic 双面定义 | 定义项目 | 是模板，不是方法 |
| 4C 研究框架 | 4 导航问题 | 是框架模板，不是方法 |
| Strategic Hypothesis 模板 | By/We can/Resulting in | 是模板，不是方法 |
| Strategy Statement 模板 | 捕捉策略 | 是模板，不是方法 |
| Notion Capture Template | 8 字段捕获 Notion | 是模板，不是方法 |
| Investment Narrative 模板 | 6 部分叙事 | 是模板，不是方法 |

**正确位置**：应该在 `references/templates/` 中，不在 Toolkit 中

---

### 3.3 评判标准 / 质量检查

❌ **不应该作为 Toolkit 条目，但应该作为质量标准使用**：

| 名称 | 用途 | 为什么不是工具 |
|------|------|--------------|
| F/P/E/T 评判卡 | 评判 Insight 质量 | 是评分标准，不是方法 |
| Notion 8 条标准 | 评判 Notion 质量 | 是评分标准，不是方法 |
| Portfolio Curation 矩阵 | 评判组合质量 | 是评分标准，不是方法 |

**正确位置**：应该在 `references/quality-standards/` 中，不在 Toolkit 中

---

### 3.4 输出物 / 交付物

❌ **不应该作为 Toolkit 条目**：

| 名称 | 用途 | 为什么不是工具 |
|------|------|--------------|
| Opportunity Areas | 机会领域 | 是输出物，不是方法 |
| Notions Portfolio | Notion 组合 | 是输出物，不是方法 |
| Solutions | 解决方案 | 是输出物，不是方法 |
| Investment Narrative | 投资叙事 | 是输出物，不是方法 |

**正确位置**：是研究过程的产出，不在 Toolkit 中

---

## 四、F212 的工具清单（参考）

### F212 Discovery 阶段的方法菜单

```
          一手                        二手
┌─────────┼─────────────────────────┼──────────────────────────┐
│ Consumer│ Contextual Inquiry       │ Trends Reports           │
│         │ Shop Along               │ Blogs/Social             │
│         │ Diary Study              │ Company Data             │
│         │ Focus Group              │                          │
├─────────┼─────────────────────────┼──────────────────────────┤
│ Category│ Safaris                  │ Market Reports           │
│         │ Expert Interviews        │ Competitive Audit        │
│         │                          │ Analogs                  │
├─────────┼─────────────────────────┼──────────────────────────┤
│ Channel │ Immersive Safaris        │ Best-in-Class Scan       │
│         │ Expert Interviews        │                          │
├─────────┼─────────────────────────┼──────────────────────────┤
│ Company │ Stakeholder Interviews   │ Company Data             │
│         │ Site Visits              │                          │
│         │ Working Sessions          │                          │
└─────────┴─────────────────────────┴──────────────────────────┘
```

**F212 实验方法菜单**（§7.12）：
- Fake Website（测 sign-up）
- Social Media A-B（CTR 基准 0.9%）
- Crowdfunding（测 WTP）
- Mom test（问行为）
- Related Worlds（类比）
- Expert Interviews
- Van Westendorp（价格）
- Guerilla Interviews
- 原则：Keep it simple + Define metrics

**观察**：
- F212 只列出**具体的研究方法**
- 模板、标准、流程都在其他地方说明
- Toolkit 纯粹是"方法菜单"

---

## 五、BeWater Toolkit 应该包含什么？

### 应该包含 ✅

```yaml
toolkit_should_include:
  evidence_collection:
    - 访谈（深访、专家访谈）
    - 观察（Contextual Inquiry、Diary Study）
    - 文档研究（Desk Research、内部文档）
    - 数据分析（行为数据、交易数据）
    - 实验（Pretotype、A/B Test）

  evidence_analysis:
    - 行业分析（五力、战略群组、PEST）
    - 竞争分析（对标、定位）
    - 用户分析（JTBD、细分、旅程）
    - 财务分析（单位经济、定价）
    - 趋势分析（弱信号、场景）

  hypothesis_validation:
    - 三角验证
    - 反例搜索
    - 矛盾分析
    - 敏感性分析
    - 排他解释

  insight_synthesis:
    - 模式识别
    - 张力发现
    - 重构生成
    - 跨 lens 碰撞
```

### 不应该包含 ❌

```yaml
toolkit_should_NOT_include:
  processes:
    - Living Learning Plan
    - Sprint 流程
    - Daily Debrief

  templates:
    - Money+Magic 定义
    - Strategic Hypothesis 模板
    - Notion Capture Template
    - Investment Narrative 模板

  quality_standards:
    - F/P/E/T 评判卡
    - Notion 8 条标准
    - Portfolio Curation 矩阵

  outputs:
    - Opportunity Areas
    - Notions Portfolio
    - Solutions
```

---

## 六、总结：Toolkit 边界

### 判断标准：是不是"研究方法工具"？

```
                    ┌─────────────┐
                    │  有输入吗？ │
                    └──────┬──────┘
                           │ 是
                    ┌──────▼──────┐
                    │  有输出吗？ │
                    └──────┬──────┘
                           │ 是
                    ┌──────▼──────┐
                    │  可执行吗？ │
                    └──────┬──────┘
                           │ 是
                    ┌──────▼──────┐
                    │  可重复吗？ │
                    └──────┬──────┘
                           │ 是
                        ✅ 在 Toolkit

任何一个"否" → ❌ 不在 Toolkit
```

### 当前 35 个方法的检查

| 类别 | 数量 | 是否应该在 Toolkit |
|------|------|-------------------|
| 证据收集 | 9 | ✅ 全部是 |
| 证据分析 | 11 | ✅ 全部是 |
| 假设验证 | 6 | ✅ 全部是 |
| 洞察综合 | 7 | ✅ 全部是 |

**结论**：当前 35 个方法都是真正的"研究方法工具"，应该都在 Toolkit 中。

---

## 七、扩展：60 方法建议

### 新增传统咨询方法（~15）

| 方法 | 用途 | 放入理由 |
|------|------|---------|
| PESTEL | 宏观环境分析 | 标准咨询工具 |
| SWOT | 内外部优势劣势 | 标准咨询工具 |
| BCG Matrix | 业务组合分析 | 标准咨询工具 |
| GE-McKinsey Matrix | 业务组合评估 | 标准咨询工具 |
| Core Competency | 核心竞争力分析 | 标准咨询工具 |
| Financial Ratios | 财务比率分析 | 标准咨询工具 |
| Break-even Analysis | 盈亏平衡分析 | 标准咨询工具 |
| ROI/NPV | 投资回报分析 | 标准咨询工具 |
| Decision Tree | 决策树分析 | 标准咨询工具 |
| Game Theory | 博弈论分析 | 竞争策略工具 |

### 新增设计研究方法（~10）

| 方法 | 用途 | 放入理由 |
|------|------|---------|
| Pearl Finding | 盲点挖掘 | F212 核心方法 |
| Code Cracking | 行为逻辑解码 | F212 核心方法 |
| Force Fitting | 归纳推理工具 | F212 核心方法 |
| Card Sorting | 信息架构研究 | 标准设计研究 |
| Experience Mapping | 体验地图 | 标准设计研究 |
| Persona Development | 用户画像 | 标准设计研究 |
| Insight Generation (8 维) | 洞察生成 | F212 核心方法 |

### 新增创新方法论（~5）

| 方法 | 用途 | 放入理由 |
|------|------|---------|
| Pretotyping | 快速概念验证 | Lean Startup 工具 |
| Mom Test | 行为询问法 | Lean Startup 工具 |
| Lean Experiment | 精益实验 | Lean Startup 工具 |
| Landing Page Experiment | 落地页实验 | 标准验证工具 |
| Crowdfunding Test | 众筹验证 | 标准验证工具 |

---

**文档结束**
