# Charter 迭代细化机制与质量审查系统

## 一、迭代细化机制 (Iterative Refinement Mechanism)

### 核心概念

**Charter 不是一次完成的文档，而是随着认知深化不断演进的活文档**。

### 当前问题

```yaml
# 当前模式：一次性完成
ART-001-r1-charter.md:  # 一次性产出，包含大量 Unknown
  unknowns:
    - "OEM 今天究竟怎么解决模型推理"
    - "OEM 决策链与购买周期"
    - "百度报价在 OEM 视角下是否构成差异化"
    # ... 8+ 个 Unknown
```

**问题**：
- Charter 变成"问题清单"而非"方向指南"
- Discover 需要填补太多空白，任务过重
- 质量门槛不清晰，什么 Charter 可以进入 Discover？

### 迭代细化机制

#### 1. Charter 成熟度分级

```yaml
maturity_levels:
  L1_draft:
    description: "初始方向，仅有核心命题和部分信息"
    criteria:
      - known_facts >= 1
      - core_bet_identified: true
      - readiness: "不可进入 Discover"

  L2_viable:
    description: "可行方向，核心假设已识别"
    criteria:
      - known_facts >= 3
      - root_assumptions >= 3
      - tensions_identified: true
      - readiness: "可以进入 Discover，但需补充信息"

  L3_discoverable:
    description: "可探索方向，核心未知已界定"
    criteria:
      - known_facts >= 5
      - root_assumptions >= 3
      - unknowns <= 5
      - each_assumption_has_disconfirming_signal: true
      - readiness: "可以进入 Discover"

  L4_ready:
    description: "就绪方向，初始证据已收集"
    criteria:
      - known_facts >= 5
      - root_assumptions >= 3
      - unknowns <= 3
      - initial_evidence_collected: true
      - readiness: "推荐进入 Discover"
```

#### 2. 迭代细化流程

```
初始输入 (L1_draft)
    ↓
[对话式探索]
    ↓
识别核心假设和张力 (L2_viable)
    ↓
[针对性研究/访谈]
    ↓
填补关键 Unknown (L3_discoverable)
    ↓
[初始证据收集]
    ↓
就绪进入 Discover (L4_ready)
```

#### 3. 细化触发条件

**自动触发**：
```python
def check_refinement_need(charter):
    triggers = []

    # Unknown 过多
    if len(charter.unknowns) > 8:
        triggers.append("too_many_unknowns")

    # 核心假设缺失证伪信号
    for assumption in charter.root_assumptions:
        if not assumption.disconfirming_signal:
            triggers.append("missing_disconfirming_signal")

    # Tension 识别但未细化
    if charter.tensions and not charter.balance_choice:
        triggers.append("unresolved_tension")

    # Known < Unknown
    if len(charter.known_facts) < len(charter.unknowns):
        triggers.append("unknown_exceeds_known")

    return triggers
```

**人工触发**：
- 用户主动要求深化 Charter
- Assessmen 建议补充信息
- Gate 判定 Charter 不足

#### 4. 细化路径

```python
refinement_paths = {
    "deepen_understanding": {
        "trigger": "核心假设有重大 Unknown",
        "action": "针对特定假设进行访谈/研究",
        "expected_output": "填补 1-2 个关键 Unknown",
        "time_cost": "2-4 小时"
    },
    "expand_scope": {
        "trigger": "发现新的重要维度",
        "action": "补充新的假设或边界",
        "expected_output": "新增 1-2 个 root assumptions",
        "time_cost": "30 分钟 - 1 小时"
    },
    "resolve_tension": {
        "trigger": "识别到 Tension 但未解决",
        "action": "探索 Tension 的含义和选择",
        "expected_output": "明确 balance_choice",
        "time_cost": "1-2 小时"
    },
    "collect_initial_evidence": {
        "trigger": "达到 L3_discoverable，想快速进入 Discover",
        "action": "对 1-2 个核心假设进行初始验证",
        "expected_output": "初步证据（L2-L3 级别）",
        "time_cost": "4-8 小时"
    }
}
```

#### 5. 细化模式的交互示例

```
AI: 我注意到你的 Charter 中有 8 个 Unknown，特别是关于 OEM 的真实解决路径
    和价格接受区间。在进入 Discover 之前，我建议先做一些针对性的细化。

    你有两个选择：

    1. **直接进入 Discover**：让 Discover 系统性地调查这些 Unknown
    2. **先快速细化**：花 1-2 小时对最关键的 1-2 个假设进行快速验证

    我的建议是选择 2，特别是针对"OEM 是否会外采推理"这个假设。因为如果
    这个假设不成立，整个命题就失效了。

    你想怎么做？

User: 那就先快速细化吧。我应该怎么做？

AI: 我建议做三件事：

    1. **访谈 2-3 家 AI 眼镜 OEM**：了解他们今天怎么解决推理问题
    2. **对照友商报价**：看看百度的价格是否真的有优势
    3. **更新 Charter**：将访谈结果作为 Known 加入，减少 Unknown

    预计耗时：1-2 小时

    要不要我帮你准备访谈提纲？
```

---

## 二、质量审查系统 (Quality Gate System)

### 核心概念

**不是所有 Charter 都能进入 Discover**。需要质量门槛确保 Charter 是"方向指南"而非"问题清单"。

### 质量审查的三个层次

#### 层次 1：自动质量检查

**在 Charter 自动持久化之前运行**（保留当前设计的自我审查）

```python
def auto_quality_check(charter):
    checks = {
        "structural_complete": check_structure(charter),
        "no_placeholders": check_placeholders(charter),
        "no_contradictions": check_contradictions(charter),
        "intent_fidelity": check_intent_fidelity(charter),
        "magic_money_completeness": check_magic_money(charter)
    }

    passed, failed = [], []
    for name, result in checks.items():
        if result.passed:
            passed.append(name)
        else:
            failed.append(f"{name}: {result.reason}")

    return {
        "passed": len(failed) == 0,
        "passed_checks": passed,
        "failed_checks": failed
    }
```

**问题**：这只是"文档完整性检查"，不是"方向质量检查"。

#### 层次 2：方向质量审查

**在决定是否进入 Discover 之前运行**（新增）

```python
def direction_quality_check(charter):
    """
    检查 Charter 是否有足够的信息质量进入 Discover
    """
    checks = {
        # 信息密度检查
        "known_density": {
            "check": len(charter.known_facts) >= 3,
            "reason": "需要至少 3 个已知事实作为基础"
        },

        # 未知数量控制
        "unknown_limit": {
            "check": len(charter.unknowns) <= 8,
            "reason": "Unknown 过多（>8）意味着 Charter 是问题清单而非方向指南"
        },

        # 假设完整性
        "assumption_completeness": {
            "check": all([
                len(charter.root_assumptions) >= 3,
                all(ass.disconfirming_signal for ass in charter.root_assumptions)
            ]),
            "reason": "每个假设都需要证伪信号"
        },

        # 张力识别
        "tension_identified": {
            "check": charter.tension is not None,
            "reason": "需要识别 Magic-Money 之间的张力"
        },

        # 边界清晰
        "boundary_clarity": {
            "check": all([
                charter.scope.included,
                charter.scope.excluded,
                charter.scope.first_cycle_boundary
            ]),
            "ready": "需要明确 in/out of scope 和第一周期边界"
        }
    }

    # 计算质量分数
    total_checks = len(checks)
    passed_checks = sum(1 for c in checks.values() if c["check"])

    quality_score = passed_checks / total_checks

    return {
        "score": quality_score,
        "checks": checks,
        "can_enter_discover": quality_score >= 0.6  # 60% 通过率
    }
```

#### 层次 3：适配性审查

**由 Assessment 或 Gate 执行**，检查 Charter 是否适合具体的上下文。

```python
def contextual_fitness_check(charter, context):
    """
    检查 Charter 是否适合当前的组织和市场上下文
    """
    checks = {
        "organization_fit": {
            "check": has_leverageable_assets(charter, context.org_assets),
            "reason": "命题需要与组织的实际杠杆资产匹配"
        },
        "market_timing": {
            "check": is_right_timing(charter, context.market_signals),
            "reason": "需要验证 market timing 是否合适"
        },
        "resource_feasibility": {
            "check": is_feasible_with_resources(charter, context.available_resources),
            "reason": "需要的资源是否在可承受范围内"
        }
    }

    return checks
```

### 质量审查的运作流程

```
Charter Draft (L1_draft)
    ↓
[自动质量检查] → 失败 → 返回细化
    ↓ 通过
方向质量审查
    ↓
├─ 质量分数 ≥ 80% (L3_discoverable) → 可以进入 Discover
├─ 质量分数 60-80% (L2_viable) → 建议细化后再进入
└─ 质量分数 < 60% → 必须细化
    ↓
[用户选择]
    ├─ 接受建议 → 细化 Charter
    └─ 坚持进入 → 记录风险，允许进入 Discover
```

### 质量审查的交互示例

```
AI: Charter 已完成自动质量检查并准备持久化。但在进入 Discover 之前，
    我想给你一个质量报告。

    **质量审查结果**：

    ✅ 通过的检查：
    - 结构完整
    - 无占位符
    - Magic-Money 完整
    - 张力已识别（生态错位 vs 成本差异化）

    ⚠️  未通过的检查：
    - Unknown 过多（9 个，建议 ≤5 个）
    - Known < Unknown（3 vs 9）
    - 关键假设 A-001 缺少证伪信号

    **质量分数**：55%（60% 以下）

    **我的建议**：

    这个 Charter 方向是有趣的，但信息密度不够。我建议先做一轮快速细化：

    1. 针对"OEM 是否会外采推理"（A-001）做 2-3 个快速访谈
    2. 对照友商报价，验证"成本优势"假设（A-002）
    3. 将访谈结果作为 Known 加入 Charter

    预计耗时：1-2 小时，预计质量分数提升到 70-80%

    **你的选择**：

    1. 接受建议，先细化 Charter
    2. 忽略建议，直接进入 Discover（会记录质量风险）

User: 我选择 2，直接进入 Discover。时间比较紧。

AI: 明白了。我会将 Charter 持久化，并在 ledger 中记录质量风险。
    Discover 的第一优先级将是验证这 9 个 Unknown。

    让我先记录这个决定...
```

---

## 三、两个机制的协同

### 迭代细化 + 质量审查

```
用户初始输入
    ↓
对话式探索（降低 Unknown，提高 Known）
    ↓
 Charter Draft (L1_draft)
    ↓
[自动质量检查]
    ↓
[方向质量审查]
    ↓
├─ 质量分数 ≥ 80% → 直接进入 Discover
├─ 质量分数 60-80% → 建议细化
└─ 质量分数 < 60% → 强烈建议细化
    ↓
[用户决策]
    ├─ 接受 → [迭代细化机制]
    │             ↓
    │         针对性补充信息
    │             ↓
    │         Charter Revision (L2/L3)
    │             ↓
    │         [重新质量审查]
    │
    └─ 拒绝 → 直接进入 Discover（记录质量风险）
```

### 与现有系统的集成

```yaml
# Charter artifact
maturity_level: "L1_draft|L2_viable|L3_discoverable|L4_ready"
quality_score: 0.55
quality_checks:
  passed: ["structural_complete", "tension_identified"]
  failed: ["unknown_limit", "known_density"]
last_refinement: null
refinement_history: []

# Ledger entry
event_type: "charter_quality_gate"
artifact_ref: "ART-001@1"
quality_score: 0.55
decision: "user_override"
risk_recorded: "high_unknown_count"
timestamp: "2026-08-05T12:00:00Z"
```

---

## 四、实施建议

### 短期（1-2 周）

1. **增加方向质量审查**：在 Charter 自动持久化后，但进入 Discover 前
2. **添加质量分数显示**：让用户看到 Charter 的信息质量
3. **记录质量风险**：当用户选择低质量 Charter 进入 Discover 时

### 中期（3-4 周）

1. **实现 Charter 成熟度分级**：L1-L4 分级系统
2. **实现细化路径建议**：针对不同的质量问题提供具体的细化建议
3. **集成到 Ledger**：记录质量审查和细化历史

### 长期（1-2 月）

1. **对话式交互**：从问卷式转向对话式
2. **自动细化触发**：系统自动识别 Charter 质量不足并建议细化
3. **细化工具集成**：提供访谈提纲、研究清单等细化工具

---

## 五、总结

**迭代细化机制**：
- Charter 是演进的活文档，不是一次性完成的
- 通过 L1-L4 成熟度分级管理 Charter 质量
- 提供多种细化路径（深化理解、扩大范围、解决张力、收集初始证据）

**质量审查系统**：
- 三个层次：自动检查、方向质量、适配性审查
- 质量分数量化 Charter 质量
- 建议而非强制：用户可以 override，但会记录风险

**协同**：
- 质量审查识别 Charter 的不足
- 迭代细化提供改进路径
- 两个机制协同确保 Charter 有足够质量进入 Discover

**核心原则**：
- 不是所有 Charter 都能进入 Discover
- Charter 是"方向指南"而非"问题清单"
- 质量比速度更重要：花时间细化 Charter，会在 Discover 阶段节省更多时间
