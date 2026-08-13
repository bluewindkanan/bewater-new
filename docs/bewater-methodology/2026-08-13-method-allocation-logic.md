# BeWater 研究方法分配逻辑

## 版本信息
- **版本**: 1.0
- **日期**: 2026-08-13
- **状态**: Draft

---

## 一、设计目标：让研究"足够扎实"

**扎实的定义**：
1. **覆盖全面**：不遗漏关键分析角度
2. **证据充分**：每个结论有足够证据支撑
3. **深度足够**：不止表面，触及因果机制
4. **质量可控**：证据可追溯、可验证

---

## 二、F212 的启发：4C × 一手/二手 矩阵

### F212 Discovery 阶段的方法组织

```
          一手                       二手
Consumer  Contextual Inquiry         Trends Reports
          Shop Along                 Blogs/Social
          Diary Study                Company Data
          Focus Group
          Intercept
          Survey

Category   Safaris                    Market Reports
          Expert Interviews          Competitive Audit
                                     Analogs

Channel    Immersive Safaris         Best-in-Class Scan
          Expert Interviews

Company    Stakeholder Interviews    Company Data
          Site Visits
          Working Sessions
```

**核心特点**：
- **二维矩阵**：分析对象（4C）× 数据来源（一手/二手）
- **方法菜单**：每个格子列出 2-6 种方法
- **非自动分配**：让人根据 Learning Plan 选择
- **覆盖保证**：确保从 4 个角度切入，每个角度都有多种方法可选

---

## 三、BeWater 的方法分配逻辑设计

### 3.1 核心原则：围绕 Learning Plan 的研究问题分配方法

```
Learning Plan 研究问题（LQ）
    ↓
问题分类（4C 分析对象 × 学习意图）
    ↓
方法矩阵选择（4C × functional_layer）
    ↓
最小互补组合（确保覆盖 + 深度）
    ↓
Sprint 执行
    ↓
质量检查（F/P/E/T + 覆盖度）
```

### 3.2 方法矩阵：4C × Functional Layer

```
                    Collection              Analysis                Validation              Synthesis
┌───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┐
│ Consumer          │ stakeholder           │ segmentation-        │ evidence-strength     │ pattern-anomaly      │
│                   │ interviews            │ decision-unit        │ transferability       │ detection            │
│                   │ contextual-           │ jtbd-journey         │ alternative-          │ tension-finding      │
│                   │ observation           │                      │ explanation-          │                      │
│                   │ diary-study           │                      │ testing               │                      │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ Category          │ desk-document         │ five-forces          │ source-family         │ trend-weak-signal    │
│                   │ literature-           │ competitive-         │ triangulation         │ scenario-analogy     │
│                   │ patent-search         │ benchmarking         │ negative-case         │                      │
│                   │ company-product-      │ value-chain-         │                      │                      │
│                   │ competitor-audit      │ profit-pool          │                      │                      │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ Channel           │ contextual-           │ ecosystem-           │ contradiction-        │ strategic-           │
│                   │ observation           │ channel-map          │ analysis              │ relevance-           │
│                   │                       │                      │                      │ mapping              │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ Company           │ internal-             │ pricing-             │ sensitivity-          │ belief-              │
│                   │ document-data         │ unit-economics       │ boundary-check        │ shift-mapping        │
│                   │ usability-demo        │                      │                      │                      │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 假设/实验         │ pretotyping           │ hypothesis-          │ assumption-           │ structural-          │
│                   │ mom-test              │ mapping              │ testing               │ reframe-             │
│                   │                       │                      │                      │ generation           │
└───────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

### 3.3 分配规则

#### 规则 1：覆盖度检查

每个 Learning Question 必须覆盖：
- **至少 1 个 C 维度**（Consumer/Category/Channel/Company）
- **至少 2 个 functional_layer**（Collection + Analysis 最小组合）
- **优先全流程**：Collection + Analysis + Validation（理想）

#### 规则 2：深度保证

根据问题深度要求：
- **浅层探索**：Collection + Analysis（如行业扫描）
- **中等深度**：Collection + Analysis + Validation（如竞争分析）
- **深度研究**：Collection + Analysis + Validation + Synthesis（如用户行为动机）

#### 规则 3：数据来源平衡

一手 vs 二手数据比例：
- **公开数据充足**：70% 二手 + 30% 一手（如行业研究）
- **需要行为洞察**：70% 一手 + 30% 二手（如用户研究）
- **快速验证**：100% 一手实验（如 Pretotype）

#### 规则 4：方法论流派适配

根据问题类型选择流派：
- **行业结构问题**：传统咨询（五力、战略群组）
- **用户行为问题**：设计研究（深访、观察）
- **概念验证问题**：创新方法论（Pretotype、实验）

---

## 四、执行流程

### Step 1：Learning Plan 研究问题分析

```yaml
learning_question: "用户为什么不愿意使用我们的 AI 助手？"

question_analysis:
  analysis_object: "Consumer"          # 主维度
  secondary_objects: ["Company"]      # 次要维度
  learning_intent: "explain"          # 学习意图
  depth_required: "medium"             # 深度要求
  data_availability:                   # 数据可用性
    internal_data: "some"              # 有一些客服记录
    primary_research: "feasible"       # 可以做访谈
```

### Step 2：方法矩阵定位

```yaml
matrix_positioning:
  primary_cell: "Consumer + Analysis"    # 主格子
  secondary_cells:                        # 辅助格子
    - "Consumer + Collection"
    - "Company + Analysis"

  candidate_methods:
    - consumer_segmentation_decision_unit
    - consumer_jtbd_journey
    - stakeholder_interviews
    - internal_document_data_review
```

### Step 3：最小互补组合

```yaml
method_bundle:
  collection:
    - stakeholder_interviews          # 一手：深访
    - internal_document_data_review    # 二手：客服记录

  analysis:
    - jtbd_journey                     # 用户旅程分析
    - segmentation_decision_unit       # 细分分析

  validation:
    - evidence_strength_transferability  # 迁移性检查
    - alternative_explanation_testing    # 排他解释测试

  synthesis:
    - pattern_anomaly_detection       # 模式识别
```

**为什么这个组合扎实？**
- ✅ 覆盖 Consumer 主维度（JTBD + 细分）
- ✅ 一手数据（深访）+ 二手数据（客服记录）
- ✅ 全流程：Collection → Analysis → Validation → Synthesis
- ✅ 质量检查：迁移性检查防止过度泛化
- ✅ 深度保证：JTBD 挖掘动机，不满足于表面描述

---

## 五、质量检查清单

### 检查 1：覆盖度

```yaml
coverage_check:
  - covered_dimensions: ["Consumer"]  # 至少 1 个 C
  - covered_layers: ["collection", "analysis", "validation", "synthesis"]  # 至少 2 个
  - data_source_balance:              # 一手/二手平衡
      primary: 50%
      secondary: 50%
```

### 检查 2：证据质量

```yaml
evidence_quality_check:
  - fp_e_t_rating: "≥ 3/5"           # F/P/E/T 评分
  - source_credibility: "high"        # 来源可信度
  - triangulation: "≥ 2 sources"     # 三角验证
```

### 检查 3：深度足够

```yaml
depth_check:
  - goes_beyond_surface: true         # 不止表面
  - causal_mechanism_identified: true # 找到因果机制
  - contradictions_preserved: true    # 保留矛盾证据
```

---

## 六、典型场景示例

### 场景 1：行业竞争格局（浅层探索）

**研究问题**：AI 硬件行业的竞争格局如何？

```yaml
method_bundle:
  collection:
    - desk_document_research          # 行业报告
    - literature_patent_search       # 专利分析

  analysis:
    - five_forces                     # 五力分析
    - competitive_benchmarking       # 竞争对标

  validation:
    - source_family_triangulation     # 三角验证

quality_check:
  depth: "shallow"
  coverage: ["Category"]
  layers: ["collection", "analysis", "validation"]
```

### 场景 2：用户行为动机（深度研究）

**研究问题**：为什么用户不愿意使用我们的 AI 助手？

```yaml
method_bundle:
  collection:
    - stakeholder_interviews          # 深访 8-12 人
    - contextual_observation          # 场景观察
    - internal_document_data_review  # 客服记录

  analysis:
    - jtbd_journey                     # JTBD 旅程
    - segmentation_decision_unit      # 细分 + 决策单元
    - code_cracking                    # 行为逻辑解码

  validation:
    - evidence_strength_transferability  # 迁移性
    - alternative_explanation_testing    # 排他解释
    - contradiction_analysis             # 矛盾保留

  synthesis:
    - pattern_anomaly_detection       # 模式/异常
    - tension_finding                # 张力识别
    - structural_reframe_generation   # 结构性重构

quality_check:
  depth: "deep"
  coverage: ["Consumer", "Company"]
  layers: ["collection", "analysis", "validation", "synthesis"]
  data_balance: {primary: 70%, secondary: 30%}
```

### 场景 3：概念快速验证（实验）

**研究问题**：这个 AI 健身教练概念是否值得开发？

```yaml
method_bundle:
  collection:
    - mom_test                        # 行为询问
    - pretotyping_landing_page        # 假页面测试

  analysis:
    - hypothesis_mapping              # 假设映射

  validation:
    - assumption_testing              # 假设测试
    - sensitivity_boundary_check      # 敏感性分析

quality_check:
  depth: "experiment"
  coverage: ["假设/实验"]
  layers: ["collection", "validation"]
  data_balance: {primary: 100%, secondary: 0%}
```

---

## 七、与 F212 的对比

| 维度 | F212 | BeWater 设计 |
|------|------|-------------|
| **组织方式** | 4C × 一手/二手 | 4C × Functional Layer |
| **分配逻辑** | 人工从矩阵选择 | 系统推荐 + 人工确认 |
| **覆盖保证** | 矩阵确保覆盖 4C | 覆盖度检查规则 |
| **深度保证** | Living Learning Plan | 深度分级（浅/中/深/实验） |
| **质量保证** | F/P/E/T 评判卡 | F/P/E/T + 覆盖度 + 深度检查 |

---

## 八、实现建议

### 8.1 方法矩阵数据结构

```yaml
# method-matrix.yaml
matrix:
  consumer:
    collection:
      - id: "stakeholder_interviews"
        data_source: "primary"
        depth: "medium"
        time_cost: "high"
      - id: "contextual_observation"
        data_source: "primary"
        depth: "deep"
        time_cost: "high"
    analysis:
      - id: "jtbd_journey"
        depth: "deep"
        complements: ["segmentation_decision_unit"]
      - id: "segmentation_decision_unit"
        depth: "medium"
    # ...

  category:
    collection:
      - id: "desk_document_research"
        data_source: "secondary"
        depth: "shallow"
        time_cost: "low"
    analysis:
      - id: "five_forces"
        depth: "medium"
        methodology_stream: "traditional_consulting"
    # ...
```

### 8.2 覆盖度检查算法

```python
def check_coverage(method_bundle, question_analysis):
    """
    检查方法组合的覆盖度
    """
    checks = {
        "covered_dimensions": check_dimensions(method_bundle, question_analysis),
        "covered_layers": check_layers(method_bundle),
        "data_balance": check_data_balance(method_bundle),
        "depth_adequacy": check_depth(method_bundle, question_analysis)
    }

    # 规则：
    # - 至少 1 个 C 维度
    # - 至少 2 个 functional_layer
    # - 数据来源平衡符合问题类型
    # - 深度符合 depth_required

    return checks

def suggest_improvements(checks, method_bundle):
    """
    建议改进
    """
    if not checks["covered_dimensions"]:
        return "建议增加 Consumer 维度方法"
    if not checks["covered_layers"]:
        return "建议增加 Analysis 层方法"
    # ...
```

---

## 九、关键原则总结

1. **围绕研究问题**：方法选择从 Learning Plan 的研究问题出发，而非相反
2. **覆盖全面**：确保 4C 维度 × Functional Layer 的覆盖
3. **深度适配**：根据问题深度要求选择方法的深度
4. **数据平衡**：一手/二手数据比例适配问题类型
5. **流派对齐**：传统咨询/设计研究/创新方法论用对场景
6. **质量可控**：F/P/E/T + 覆盖度 + 深度检查

---

**文档结束**
