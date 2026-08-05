---
schema_version: 1
artifact_id: ART-003
revision: 3
supersedes_ref: artifact:ART-003@2
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

# Research · ART-003 r3 · 百度智能云 AI 硬件 token 业务

> r3 = r2 的 Current Discover Plan（更新）+ Latest Research Sprint（Sprint 2：PT 准备）+ Debrief。前次 Sprint（Sprint 1：M1~M4 desk-research）快照保存在 r2。

## Current Discover Plan（r3 更新）

### 1. Discovery mission and decision（不变）

详见 r1/r2。Core question 与 G1 决策不变。

### 2. Formal inputs and priorities（不变）

- **Charter head:** `artifact:ART-001@1`
- **Active root assumptions:** `assumption:A-001@1`、`A-002@1`、`A-003@1`、`A-004@1`（仍 L1 / untested）
- **Advisory:** `artifact:ART-002@1`
- **Risk priorities:** P0 = A-001/A-002/A-003；P1 = A-004。

### 3. 4C coverage map（r3 不变于 r2）

Consumer 部分 evidenced；Company 部分 evidenced；Category evidenced；Channel gap-accepted。详见 r2 §3。

### 4. Evidence strategy（r3 更新）

- **research_mode：** 仍 `secondary_first`，但 secondary 阶段已结束；**primary 阶段开启（PT-1/2/3 全部 triggered）**。
- **Primary Trigger 状态：**
  - **PT-1（OEM 一手访谈）：✅ triggered** —— 脚本已产出：`docs/discover/primary-triggers/PT-1-OEM访谈指南.md`。目标 ≥5 家 OEM，覆盖 3 类 sourcing 模式。
  - **PT-2（联合测价 / POC）：✅ triggered** —— 设计已产出：`docs/discover/primary-triggers/PT-2-POC设计方案.md`。目标 3-5 家 OEM 完成 4 阶段 POC。
  - **PT-3（内部成本/产能数据）：✅ triggered** —— 需求清单已产出：`docs/discover/primary-triggers/PT-3-内部数据需求清单.md`。P0 字段 D-001~005 必须，P1 字段 D-006~009 至少 3 项。
- **下一步执行模式：** 双轨并行。
  - **Track A（用户执行）：** 用户携脚本进入现场——访谈 OEM、推动 POC、申请内部数据。回收按各脚本末尾的 evidence 回收模板，由 Discover agent 结构化为新 evidence records（预计 ≥30 条新增 L3/L4 证据）。
  - **Track B（agent 执行）：** 基于现有 18 条 L2 secondary 证据，进入 `bw-insight-craft` 合成候选 Insight Portfolio；明确标注每条 Insight 的 evidence level 上限——凡依赖 PT-1/2/3 结果的 Insight，必须停在 L2/L3 候选态，不得直接进入 G1 Go。

### 5. Research missions（r3 状态）

| Mission | 状态 | 目标假设 | 关键证据 | 下一动作 |
|---|---|---|---|---|
| M1 友商 token 报价 + SLA | ✓ complete（r2） | A-002 | E-001~E-005 | 关闭 |
| M2 出货量 + 调用量 | ✓ complete（r2） | A-004 | E-006~E-008 | 关闭 |
| M3 OEM 自建 vs 外采 | ✓ complete（r2） | A-001 | E-009~E-015 | 关闭 |
| M4 ERNIE 成本曲线 | ✓ complete（r2） | A-003 | E-016~E-018 | 关闭 |
| **M5 PT-1 OEM 访谈** | 🔵 triggered-pending-execution | A-001、A-002（行为面） | 待回收 | 用户执行，预计 ≥5 家 |
| **M6 PT-2 联合测价/POC** | 🔵 triggered-pending-execution | A-002（核心 L4） | 待回收 | 用户执行，预计 3-5 家 |
| **M7 PT-3 内部成本数据** | 🔵 triggered-pending-execution | A-003（成本侧 L4） | 待回收 | 用户执行，预计 1-2 周拿 P0 |
| **M8（候选 deepen）多模态 token 权重** | ⚪ not-started | A-002 deepen#2 | — | 与 PT-3 D-003 合并 |

### 6. Stop rule（r3 决策）

**Next action（双轨）：**
- **Track B 立即：** 进入 `bw-insight-craft`，合成基于 18 条 L2 secondary 的候选 Insight Portfolio；标注 L4 缺口。
- **Track A 异步：** 用户携 PT-1/2/3 脚本进入现场；回收后由 Discover agent 把每条 claim 结构化为 evidence records，并视证据强度更新假设 validation_status。

**为什么并行：** Insight Craft 在 L2 上能产出有意义的候选判断（即便不能直接 Go），让用户在 PT 执行期间就能看到方向性轮廓；同时 PT 回收的证据可在 Insight Craft 之后通过 backtrack 或 Insight 修订并入。

## Latest Research Sprint（Sprint 2：PT 准备）

### Reviewed mission selection

Sprint 2 不采集证据，仅产出 PT 执行工具。等价于 "Sprint 0.5"——把 Plan 中标为 not-triggered 的 PT-1/2/3 转为 triggered，并把执行脚本交付给用户。

### Work actually executed

| 产出 | 路径 | 用途 |
|---|---|---|
| PT-1 OEM 访谈指南 | `docs/discover/primary-triggers/PT-1-OEM访谈指南.md` | 5 家 OEM × 产品/技术决策人 × A-001/A-002/A-003/Channel 问题清单 |
| PT-2 POC 设计方案 | `docs/discover/primary-triggers/PT-2-POC设计方案.md` | 3-5 家 OEM × 4 阶段 POC × 盲测+实测+模拟决策 |
| PT-3 内部数据需求清单 | `docs/discover/primary-triggers/PT-3-内部数据需求清单.md` | D-001~D-012 数据字段 × 4 条申请路径 × 量级目标 |

### Deviations from the Plan

无偏差——3 份脚本覆盖了 r2 Plan §5 中 M5/M6/M7 候选 mission 的全部证据需求。M8（多模态 token 权重 deepen）已并入 PT-3 的 D-003 字段。

## Research Sprint Debrief

### Learned（r3 新增）

1. PT-1/2/3 三条 trigger 的执行权完全在用户侧——agent 无法直接访谈 OEM 或访问百度内部数据；agent 的角色从"采集者"转为"工具产出者 + 回收结构化者"。
2. 3 份脚本合计 ~7000 字，覆盖候选 OEM 清单、问题清单、POC 4 阶段设计、12 个内部数据字段、3 套 evidence 回收模板——构成完整的 primary 执行链路。
3. 双轨并行的可行性：L2 证据足以 craft 候选 Insight（不能 Go），PT 回收后再升级——避免 PT 周期阻塞方向性判断。

### Unresolved（r3 新增）

1. PT-1 实际能访谈到几家 OEM 取决于用户渠道可达性；<5 家时记录 partial。
2. PT-2 POC 需要 BD 渠道协同 + token 费用减免预算；授权范围未明。
3. PT-3 D-004 毛利数据可能因敏感被拒；需备选路径（D-007~009 间接推算）。

### Deepen（r3 新增）

1. M8 多模态 token 权重已并入 PT-3 D-003，无需独立 deepen Sprint。
2. PT-1 访谈中若出现 Meta Muse Spark 开放给第三方的信号，需立即触发新 mission（M9 候选）。

### Drop

（无）

### New questions

- Q-NEW-5：百度智能云 BD 渠道对 AI 眼镜 OEM 的现有覆盖度如何？这决定 PT-2 POC 能否发起。
- Q-NEW-6：百度内部对"卖 token 给硬件"是否已有竞业/合规审查流程？

### Plan Delta

- **Primary Trigger status：** PT-1 / PT-2 / PT-3 全部从 not-triggered → **triggered-pending-execution**。
- **Mission changes：** 新增 M5/M6/M7（triggered）+ M8（合并入 PT-3）。
- **Execution mode：** 从单轨（agent desk-research）转为双轨（用户现场 + agent Insight Craft 并行）。
- **Evidence expectation：** PT 执行回收后预计新增 ≥30 条 evidence records（PT-1 ≥15 条 + PT-2 ≥10 条 + PT-3 ≥5 条），其中部分可达 L3/L4。

### Next action

**双轨启动：**
1. **Track B（立即）：** 路由到 `bw-insight-craft`，合成基于现有 18 条 L2 证据的候选 Insight Portfolio；明确标注每条 Insight 的 evidence level 上限与 L4 缺口。
2. **Track A（异步）：** 用户携 3 份 PT 脚本进入现场；回收按脚本末尾的 evidence 回收模板。回收后由 Discover agent 写入 `_bewater/evidence.yaml`，并通过 `bw-backtrack` 流程把新证据并入现有假设链路（如有假设需要 falsify 或记录 risk_history）。

---

*本 Sprint 仅产出执行工具与 Plan 更新；未采集新 evidence；未签 signoff；未升级任何 candidate；未修改 ledger 的 evidence_level / validation_status；未选择 gate exit。PT 脚本本身（位于 `docs/discover/primary-triggers/`）是工作产物，不是 BeWater 状态——可自由修改、补充、本地化，不影响 ART-003 链路完整性。*
