# BeWater 决策段落地形态：bw- 原生 agent/skill 生态

## Context

`bewater-methodology`（v1.3，`bewater-core.md`，943 行）已是一套成熟、自洽的「可预测的创新方法论」——三层架构、4模块×8阶段、4门5出口、3循环、假设账本+证据六级、14 个字段级模板都齐备。它**不缺方法论内核**，缺的是**可执行的落地形态**。

现有仓库曾有一套落地形态（`bw-*` stage router + 借用 `bmad-*` 专家能力），但有两个根本缺陷：
1. **决策段是空的**——`bw-1discover`/`bw-2define` 路由到的全是 `bmad-*`（domain/market/technical-research、cis-innovation-strategy），这些是泛化能力，没有承载 bewater 的核心机制（假设账本、证据六级、双面性、门、回溯）。
2. **bmad 的模型承载不了 bewater**——bmad 是 "agent persona + 能力菜单" 的单层模型，为「执行工作」设计；而 bewater 决策段的本质是「管理不确定性」，需要一套**贯穿全流程的活状态层**。

当前工作树已清空所有旧资产（`.agents/`、`.claude/`、`_bmad/`、`docs/`、`dist/`、`bw-*`、`bmad-*` 全部 deleted），磁盘只剩 `bewater-methodology/` 正文 + `resources/` submodules。这是一个干净的重做起点。

**目标**：基于 bewater-methodology 忠实落地，聚焦**决策段**（Immersion→Discover→Define→Ideate→Shape + G1/G2 门），全新设计一套 `bw-` 原生的 agent/skill 生态，**原生承载** bewater 的全部独特机制（假设账本+证据六级+门治理、Money+Magic 双面性硬约束、大小循环+回溯治理、两世界声明+工作坊操作法）。执行段不在本次范围，仅预留 Shape→Design 衔接出口。

**与 bmad 的根本差异**（这是设计的核心洞察）：把 bewater 独有的**状态层**（假设账本+血缘+回溯）作为最底层引擎，门做成「判据可机器核验（扫账本）、五出口决策不可让渡（强制人工）」的节点。bmad 没有、也无法表达这一层。

---

## 1. 设计概览：四层架构

```
┌─────────────────────────────────────────────────────────────┐
│ L4 路由层   stage router（bw-immersion/discover/define/      │
│            ideate/shape）+ 工作坊（bw-world-switch 等）       │
│            扫描状态 → 路由到能力/门；最轻量                    │
├─────────────────────────────────────────────────────────────┤
│ L3 能力层   每个 Stage 的具体工作 skill                       │
│            （bw-insight-craft / bw-strategy-statement / ...） │
│            执行 §9 模板的字段级工作；读写状态层                 │
├─────────────────────────────────────────────────────────────┤
│ L2 门层     G1/G2（bw-g1-strategy-gate / bw-g2-concept-gate）│
│            判据机器核验 + 五出口人工决策；G2 后基线化账本       │
├─────────────────────────────────────────────────────────────┤
│ L1 状态层   bw-assumption-ledger / bw-lineage-trace /         │  ← bewater 独有引擎
│            bw-backtrack                                       │     bmad 完全没有
│            假设账本 + 产物血缘 + 失效传播 + 回溯路由            │
└─────────────────────────────────────────────────────────────┘
```

**交互方式**：L4 router 扫描 L1 状态 + 产物 → 路由到 L3 能力 或 L2 门；L3 能力执行时读写 L1 账本；L2 门读取 L1 账本核验判据、输出五出口、决策后回写 L1（基线化）；失效发生时 L1 的 `bw-backtrack` 判定回溯深度，路由回对应门重裁。

**为什么这样分层**：bewater 决策段的「产物」不是孤立文档，而是一条**带血缘的假设链**——每个产物 derived_from 上游、affects 下游，假设被证伪时失效要沿链传播。这条链必须有独立的状态层来维护，否则血缘、回溯、门判据全都无处附着。把状态层独立出来，门和能力才能保持轻薄（只管核验/执行），这是 bewater「收敛物 handoff + 血缘 + 知识库留底」（§7.1）机制的直接落地。

---

## 2. 命名空间与目录结构

**命名规范**：统一前缀 `bw-`（= bewater 缩写），**不加子前缀**，靠 skill 名语义 + frontmatter `layer` 字段区分层次。

```yaml
# 每个 SKILL.md frontmatter 统一加 layer 字段
---
name: bw-assumption-ledger
description: "..."
layer: state          # state | gate | capability | stage | workshop
stage: discover        # 所属 stage（state/gate 跨 stage 时留空）
---
```

**目录结构**（仿 `_bmad` 模式，bewater 原生）：

```
bewater-explore/
├── bewater-methodology/bewater-core.md     # 方法论正文（已存在，只读权威源，不动）
│
├── .claude/skills/bw-*/SKILL.md            # Claude 平台 skill（主副本）
├── .agents/skills/bw-*/SKILL.md            # Codex/OpenAI 镜像（与 .claude byte-identical）
│   └── 每个 skill 可含 templates/、references/（惰性加载）
│
├── _bewater/                               # 决策段运行时根（活状态机）
│   ├── config.yaml                         # 项目配置（project_name / output paths）
│   ├── state/                              # L1 状态层文件
│   │   ├── assumption-ledger.yaml          #   假设账本（决策段 source of truth）
│   │   └── gates/                          #   门决策记录
│   │       ├── g1-strategy-gate-<date>.md
│   │       └── g2-concept-gate-<date>.md
│   ├── artifacts/                          # 阶段产物（统一 frontmatter）
│   │   ├── immersion/project-charter.md
│   │   ├── discover/{research/*, insights.md, directional-hypotheses.md}
│   │   ├── define/{strategy.md, opportunity-areas.md}
│   │   ├── ideate/concepts/*.md
│   │   └── shape/{solutions/*.md, investment-narrative.md}
│   └── knowledge-base/                     # 原始素材留底（录音/笔记/报告，可回查）
│
└── docs/                                   # 背景文档（哲学/设计决策/skill writing standard）
```

**两平台副本**：保留 `.claude/skills/` + `.agents/skills/` byte-identical 约定（仓库既有规范，bw-* 要求 cmp 校验）。这是仓库已验证的工程实践，不改。

**MVP 不做 `dist/` 分发层**（build-runtime.js / install.sh）：先聚焦决策段方法论落地本身，目录预留，后续需要分发时再引入。

---

## 3. 核心状态文件 Schema（字段级）

### 3.1 假设账本 `_bwater/state/assumption-ledger.yaml`（L1 核心）

决策段的 source of truth。依据 §7.2（账本字段）+ §9.8（假设地图/致命弱点）+ §6.2（回溯深度=假设层级）。

```yaml
project: <project-name>
last_baselined_at: null        # G2 过门后置为 G2；之后判断"战略前提是否被市场推翻"的参照物
assumptions:
  - id: A-001
    statement: "目标用户愿意为 X 持续付费"
    layer: concept              # root(根前提) | strategy(策略) | opportunity(机会域) | concept(概念) | feature(功能)
    category: consumer          # consumer | commercial | technical | distribution | regulatory（§9.8）
    impact: high                # low | medium | high
    uncertainty: high           # low | medium | high
    is_achilles_heel: true      # high×high = 致命弱点，须最先测、证据须 L4+（§9.8/§7.2）
    evidence_level: L3          # L1 主观 | L2 二手 | L3 自陈意图 | L4 行为信号 | L5 真实付费 | L6 可重复（§7.2）
    validation_status: open     # open | testing | validated | falsified | superseded
    evidence_ref: knowledge-base/<path>   # 证据产物路径（空则未验证）
    derived_from: [C-002]       # 上游血缘（产物/假设 id）
    affects: [S-001, A-004]     # 下游影响（失效传播目标）
    updated_at: 2026-07-27
```

**不变量**（由 `bw-assumption-ledger` skill 强制）：
- `is_achilles_heel=true` ⟺ `impact=high && uncertainty=high`。
- `is_achilles_heel=true` 且 `validation_status=validated` 时，`evidence_level` 必须 ≥ L4（否则账本校验失败，G2 阻塞）。
- `layer` 决定回溯深度（§6.2）：root→回 Discover，strategy/opportunity→回 Define，concept/feature→段内 reframe。

### 3.2 产物统一 frontmatter（所有 `artifacts/**/*.md`）

依据 §7.1（血缘/收敛物 handoff）+ bw-1discover 的 Artifact Evidence 规则 + §9.1（双面四要素）。

```yaml
---
artifact_id: <unique-id>           # 全局唯一，被 assumption-ledger / 其他产物引用
kind: charter                       # charter | directional-hypothesis | strategy | opportunity-area
                                    #  | concept | solution | investment-narrative | research | insights
stage: immersion                    # immersion|discover|define|ideate|shape
status: draft                       # draft | final | superseded | unknown
                                    # 规则：只有 final + 非空 body 满足门；unknown/invalid 视为缺失
dual_sided:                         # Money+Magic 双面性硬约束（§9.1，kind 为 hypothesis/concept/solution 时必填）
  money:
    commercial_value_proposition: "..."
    leverageable_assets: "..."
  magic:
    consumer_value_proposition: "..."
    consumer_target: "..."          # 写"处境与渴望"，不是"能解决问题"
  tension: "..."                    # 双面张力点
derived_from: [<artifact-id>]       # 上游血缘
last_validated_against: [<artifact-id>]  # 依赖快照；不再匹配时产物标记 stale
created_at: 2026-07-27
updated_at: 2026-07-27
---
```

**门核验规则**（机器可扫，依据 bw-1discover Artifact Evidence）：
- `status` 优先于文件存在；`status: final` + 非空 body 才满足门。
- `draft` 是可恢复输入，非完成证据；`superseded` 不计入完成（除非为解释血缘）。
- `last_validated_against` 不再匹配依赖 ⟹ 标记 stale ⟹ 阻塞下游门。
- 双面区块：`kind` 为 hypothesis/concept/solution 时，`dual_sided.money.*` 与 `dual_sided.magic.*` 四要素任一为空 ⟹ 双面校验失败（§6.3 反模式 5）。

### 3.3 门决策记录 `_bwater/state/gates/g2-concept-gate-<date>.md`（L2 输出）

依据 §3.2（门统一五要素）+ §6.1（G2 判据清单）。

```yaml
---
gate: G2
position: shape→design
decision_date: 2026-07-27
decision_maker: <name>             # 单一 accountable 决策人（必须是人，不可让渡 §8.2）
exit: go                           # go | conditional-go | recycle | pivot | kill（五出口）
---

## 决策问题
概念被验证到值得投入建设资源了吗？（本质：立项决策）

## 证据核验（机器扫描 assumption-ledger + 产物）
- [ ] 方案 artifacts/shape/solutions/<id>.md status: final
- [ ] 致命弱点（is_achilles_heel=true）全部 validation_status: validated，evidence_level >= L4
- [ ] 财务案例每条假设挂 evidence_ref（非空）
- [ ] 投资叙事 6 部分齐备
- [ ] dual_sided money+magic 双成立

## 决策后动作
- [ ] assumption-ledger.last_baselined_at = G2（基线化）
- [ ] exit=go ⟹ 解锁建设资源，交接给 Design（执行段出口）
- [ ] exit=conditional-go ⟹ 未闭环 condition 阻塞下一门准入（§6.3 反模式 4）
- [ ] exit=recycle/pivot ⟹ 触发 bw-backtrack，回溯到对应深度过原门重裁
```

---

## 4. Skill 清单（决策段完整，共 24 个）

| layer | stage | name | 职责（一句话） | 关键依据 |
|---|---|---|---|---|
| **state** | — | `bw-assumption-ledger` | 假设账本增删改查：调证据强度、标致命弱点、校验不变量 | §7.2 §9.8 |
| **state** | — | `bw-lineage-trace` | 给定产物/假设，追溯 derived_from 上游与 affects 下游 | §7.1 §6.2 |
| **state** | — | `bw-backtrack` | 失效发生时按假设 layer 判定回溯深度，路由到对应门重裁 | §6.2 §3.3 |
| **gate** | define→ideate | `bw-g1-strategy-gate` | G1 判断题：核验策略陈述/机会域/账本初始盘点/双面初判，五出口 | §6.1 G1 |
| **gate** | shape→design | `bw-g2-concept-gate` | G2 举证题：致命弱点 L4+/财务挂证据/叙事齐/双面成立，五出口，基线化 | §6.1 G2 |
| **capability** | immersion | `bw-project-charter` | 项目章程（who/what/how/why + 范围/约束/成功标准）+ 双面四要素 + 播种初始假设 | §5.0 §9.1 |
| **capability** | discover | `bw-4c-research` | 4C 四问研究矩阵 + 学习计划四问（每周迭代） | §5.1.1 §9.2 |
| **capability** | discover | `bw-insight-craft` | 洞察生成：认知四阶梯 + 13 透镜 + Pearl/Code/Force 三法 + F/P/E/T 评判 | §5.1.1 §9.3 |
| **capability** | discover | `bw-directional-hypothesis` | 方向性假设（By/We can/Resulting in + 4C 各一条支撑） | §9.4 |
| **capability** | define | `bw-strategy-statement` | 策略陈述（砍选择的刀，两种写法 + 反例检测） | §9.5 |
| **capability** | define | `bw-opportunity-area` | 机会域组织战术（4 种切法，2-4 个互不重叠） | §9.6 |
| **capability** | ideate | `bw-concept-card` | 概念卡 8 字段 + 8 标准 + Money/Magic 评分卡 | §5.2.1 §9.7 |
| **capability** | shape | `bw-assumption-map` | 假设分类 + 影响面×不确定度排序 + 识别致命弱点，写入账本 | §9.8 |
| **capability** | shape | `bw-experiment-design` | 实验方法菜单 8 法 + 成功指标/基准定义（kill/proceed 判据前置） | §9.9 |
| **capability** | shape | `bw-investment-narrative` | 投资叙事 6 部分 + Solutions 三段式 + 假设逐条披露 | §9.10 |
| **stage** | immersion | `bw-immersion` | router：扫描章程/初始假设 → 路由 | §5.0 |
| **stage** | discover | `bw-discover` | router：扫描 research/insights/hypothesis → 路由能力或 G1 | §5.1.1 |
| **stage** | define | `bw-define` | router：扫描 strategy/opportunity-area → 路由 G1 | §5.1.2 |
| **stage** | ideate | `bw-ideate` | router：扫描 concepts → 收敛检查点 → 路由 | §5.2.1 |
| **stage** | shape | `bw-shape` | router：扫描 solutions/账本致命弱点 → 路由 G2 | §5.2.2 |
| **workshop** | — | `bw-world-switch` | 两世界声明（Creation/Operational 认知开关） | §2.6 §10.1 |
| **workshop** | — | `bw-creative-meeting` | 创意会议 9 步法 + 三角色（Problem Owner/Facilitator/Creative Resources） | §10.2 §10.3 |
| **workshop** | — | `bw-dual-sided-check` | Money+Magic 双面性校验（产物 schema 强制双面区块非空） | §2.1 §9.1 |
| **stage** | — | `bw-start` | 项目初始化 + 状态总览 + 推荐下一步（入口/导航） | §11 |

**人机分工铁律**（编码进每个 capability skill 的 frontmatter 或正文，依据 §8）：AI 负责 diverge（生成候选/聚类/填卡/实验设计），人负责 converge（选策略/砍概念/kill-proceed/G2 裁决）。收敛类动作 capability skill 必须以「呈现候选 + 停下等人决策」收尾，禁止 AI 代为 converge。

---

## 5. 关键 Skill 内容草案（4 个，遵循 Skill Writing Standard）

> 标准：concise imperative；checklist/routing table/allowed values/exact paths；every paragraph changes routing or defines artifact/gate/failure/format；无哲学/motivation。

### 5.1 `bw-assumption-ledger`（L1 状态层核心）

```markdown
---
name: bw-assumption-ledger
description: "BeWater 假设账本读写。新增/更新假设、调整证据强度、标记致命弱点、校验不变量。决策段 source of truth。"
layer: state
---

# bw-assumption-ledger

## Ledger Location
Canonical path: `_bwater/state/assumption-ledger.yaml`. Create with header (`project`, `last_baselined_at: null`, `assumptions: []`) if missing.

## Allowed Values
- `layer`: root | strategy | opportunity | concept | feature
- `category`: consumer | commercial | technical | distribution | regulatory
- `impact` / `uncertainty`: low | medium | high
- `evidence_level`: L1 | L2 | L3 | L4 | L5 | L6
- `validation_status`: open | testing | validated | falsified | superseded

## Operations
- `add`: append entry with new `id` (A-NNN, max+1). Required fields: statement, layer, category, impact, uncertainty. Default `validation_status: open`, `evidence_level: L1`, `derived_from: []`, `affects: []`.
- `update`: change field(s) on existing id. Recompute `is_achilles_heel` after any impact/uncertainty change.
- `validate`: set `validation_status` + `evidence_level` + `evidence_ref`.
- `baseline`: set `last_baselined_at` (called only by G2 gate on exit=go).

## Invariants (reject write on violation)
- `is_achilles_heel` ⟺ `impact=high && uncertainty=high`.
- If `is_achilles_heel=true && validation_status=validated` ⟹ `evidence_level >= L4` (else error: "致命弱点须 L4+ 真实行为证据，§7.2").
- `derived_from` / `affects` ids must exist in ledger or artifacts frontmatter.
- On `validation_status: falsified` ⟹ trigger `bw-backtrack` with the assumption id.

## Backtrack Routing (on falsified)
Read `layer` of falsified assumption ⟹ determine backtrack target:
- root ⟹ Discover (大循环, 过 G1 重裁)
- strategy | opportunity ⟹ Define (大循环, 过 G1 重裁)
- concept | feature ⟹ current stage reframe (小循环)

Output: backtrack target stage + affected downstream ids (from `affects` chain via `bw-lineage-trace`).

## Output Format
After every operation, print: changed assumption(s) summary table (id | layer | impact×uncertainty | achilles_heel | evidence_level | status) + any triggered routing.
```

### 5.2 `bw-g2-concept-gate`（L2，全流程最重的门）

```markdown
---
name: bw-g2-concept-gate
description: "BeWater G2 概念门（举证题，全流程最重）。核验致命弱点 L4+/财务挂证据/投资叙事齐/双面成立，输出五出口，go 时基线化账本。"
layer: gate
stage: shape
---

# bw-g2-concept-gate

## Position
Shape → Design. 本质：立项决策（是否投入建设资源）。

## Decision Maker
单一 accountable 决策人（必须是人，不可让渡，§8.2）。本 skill 只核验证据 + 呈现五出口，**不替人决策**。

## Evidence Check (machine-scan `_bwater/state/assumption-ledger.yaml` + `artifacts/shape/**`)
Scan and report pass/fail per item; do not auto-pass:
- [ ] solution artifact `kind: solution` with `status: final` + non-empty body
- [ ] all `is_achilles_heel=true` assumptions: `validation_status: validated` AND `evidence_level >= L4`
- [ ] financial case: every assumption referenced has non-empty `evidence_ref`
- [ ] investment narrative artifact: 6 sections present (Brief/Opportunity/Solution/Why big/Financial Case/Roadmap)
- [ ] solution `dual_sided`: money.* and magic.* all non-empty

## Blocking Reasons (canonical)
- `missing artifact` — solution or narrative not final
- `achilles heel under-evidenced` — fatal assumption < L4 or not validated
- `unbacked financial assumption` — financial assumption lacks evidence_ref
- `single-sided` — dual_sided block incomplete
- `stale artifact` — solution.last_validated_against no longer matches upstream

## Five Exits (present to decision maker, await selection)
- `go` — unlock build resources; run `bw-assumption-ledger baseline G2`; hand off to Design (执行段出口)
- `conditional-go` — record open conditions; conditions block next gate admission until closed (§6.3 #4)
- `recycle` — trigger `bw-backtrack` to concept/feature layer (小循环)
- `pivot` — trigger `bw-backtrack` to opportunity/strategy layer (大循环, 过 G1 重裁)
- `kill` — mark solution `status: superseded`; validated assumptions stay in ledger (serve other branches, §7.3)

## Decision Record
Write `_bwater/state/gates/g2-concept-gate-<date>.md` using §3.3 schema. On `go`: set `assumption-ledger.last_baselined_at = G2`.

## Failure Routing
- Any blocking reason non-empty ⟹ do not offer `go`; present only conditional-go/recycle/pivot/kill + the blocking reason.
- Decision maker absent ⟹ stop, do not auto-decide.
```

### 5.3 `bw-discover`（L4 stage router 代表）

```markdown
---
name: bw-discover
description: "BeWater Discover stage entry. 扫描 research/insights/directional-hypothesis 状态，路由到能力 skill 或 G1。"
layer: stage
stage: discover
---

# bw-discover

## Stage Responsibility
Discover (发现洞察) is a Strategy stage. 把事实炼成洞察，收口为方向性假设（§5.1.1）。Router only — 不执行研究本身。

## Input Scan (on activation)
Inspect target project for:
- `artifacts/discover/research/**` (4C 研究产物)
- `artifacts/discover/insights.md` (洞察, status)
- `artifacts/discover/directional-hypotheses.md` (方向性假设, status)
- upstream `artifacts/immersion/project-charter.md` (status: final required)

## Artifact Evidence
- Prefer frontmatter `status` over file presence.
- Only `status: final` + non-empty body satisfies a gate.
- `draft` = resumable input, not completion.
- `last_validated_against` mismatch ⟹ stale ⟹ blocking.

## Routing Order
1. charter missing/not final ⟹ `bw-immersion`.
2. 4C research missing any C (consumer/company/category/channel each < 3 facts) ⟹ `bw-4c-research`.
3. research final but insights missing/not final ⟹ `bw-insight-craft`.
4. insights final but directional hypotheses missing ⟹ `bw-directional-hypothesis`.
5. directional hypotheses final + dual_sided complete ⟹ `bw-g1-strategy-gate`.

## Routing State (always present, canonical labels)
current_stage | detected_artifacts | missing_artifacts | recommended_next_action | blocking_reason

blocking_reason allowed: `missing artifact` | `stale artifact` | `single-sided` | `4c incomplete`

## Failure Routing
- charter exists but dual_sided incomplete ⟹ `bw-project-charter` (single-sided, §6.3 #5).
- conflicting research conclusions ⟹ stop with `blocking_reason: artifact conflict`, ask user to resolve.
```

### 5.4 `bw-backtrack`（L1 回溯治理）

```markdown
---
name: bw-backtrack
description: "BeWater 回溯治理。假设证伪时按 layer 判定回溯深度，追溯失效传播，路由到对应门重裁。"
layer: state
---

# bw-backtrack

## Trigger
Called by `bw-assumption-ledger` on `validation_status: falsified`, or by G2 exit=recycle/pivot, or by human reporting a failed validation.

## Step 1 — Determine Backtrack Depth
Read falsified assumption `layer`:
- feature | concept ⟹ 小循环 (current stage reframe, 不经过门)
- opportunity | strategy ⟹ 大循环 (回 Define, 过 G1 重裁)
- root ⟹ 大循环 (回 Discover, 过 G1 重裁)

## Step 2 — Trace Failure Propagation
Run `bw-lineage-trace --id <falsified-id> --direction downstream` to enumerate all artifacts/assumptions in `affects` chain. Mark each `status: stale` (set `last_validated_against` mismatch).

## Step 3 — Check Baseline Boundary
If any stale artifact was part of `last_baselined_at` baseline (post-G2) ⟹ upgrade to 大循环, must re-pass original gate (§6.2). Report: "触碰已验证基线，升级大循环".

## Step 4 — Route
- 小循环 ⟹ current stage router (e.g. `bw-shape`) with stale artifacts listed for reframe.
- 大循环 ⟹ target stage router (`bw-discover` for root, `bw-define` for strategy/opportunity) + flag "过 G1 重裁".

## Output Format
falsified_id | layer | backtrack_type (小循环/大循环) | depth_target (stage) | affected_ids[] | must_repass_gate (G1/none)

## Invariant
回溯深度 = 假设错的深度（§6.2）。宁早回溯（成本低），不可一条错路走到底。
```

---

## 6. 实施步骤

### Step 0 — 处理 git 起点
```bash
git add -A
git commit -m "chore: clear legacy bw-*/bmad-* assets, fresh start for bewater-native decision-stage runtime"
```
工作树清空状态作为干净的新项目起点，历史保留在 git 可回查。

### Step 1 — 搭骨架（MVP，跑通最小闭环）
目标：用一个真实命题跑通 Immersion → Discover → G1 最小链路，验证状态层 + 门的设计成立。
1. 建 `_bwater/` 目录结构（config.yaml / state/assumption-ledger.yaml 空壳 / artifacts/ 各 stage 子目录 / knowledge-base/）。
2. 实现 3 个 L1 状态层 skill：`bw-assumption-ledger`、`bw-lineage-trace`、`bw-backtrack`。
3. 实现 G1 门：`bw-g1-strategy-gate`。
4. 实现 2 个 stage router：`bw-immersion`、`bw-discover`。
5. 实现 3 个能力 skill：`bw-project-charter`、`bw-insight-craft`、`bw-directional-hypothesis`。
6. 双平台副本：`.claude/skills/` + `.agents/skills/` byte-identical。
7. 写 `docs/skill-writing-standard.md`（迁移 spec 里的标准）+ `docs/architecture.md`（四层架构说明）。

### Step 2 — 补齐决策段（Define / Ideate / Shape + G2）
8. 实现 G2 门：`bw-g2-concept-gate`。
9. stage router：`bw-define`、`bw-ideate`、`bw-shape`。
10. 能力 skill：`bw-4c-research`、`bw-strategy-statement`、`bw-opportunity-area`、`bw-concept-card`、`bw-assumption-map`、`bw-experiment-design`、`bw-investment-narrative`。
11. workshop skill：`bw-world-switch`、`bw-creative-meeting`、`bw-dual-sided-check`。

### Step 3 — 入口 + 文档
12. `bw-start`（项目初始化 + 状态总览 + 推荐下一步）。
13. 更新 `README.md` / `AGENTS.md` / `CLAUDE.md`（决策段 Stage Map：bw-immersion→...→bw-shape→G2→Design 出口）。

### Step 4 —（后续，非本次）分发层 + 执行段衔接
14. 引入 `dist/` 分发层（build-runtime.js / install.sh），按需。
15. Shape→Design 衔接出口：G2 exit=go 后产出方案规格交接给执行段（执行段实现另行规划）。

---

## 7. 验证方法

**端到端跑一个真实命题**（§11 一页纸的最小流程为脚本）：
1. 选一个真实命题（非 toy example），用 `bw-start` 初始化。
2. 跑 `bw-immersion` → `bw-project-charter`：产出章程 + ≥3 条初始假设入账本。
3. 跑 `bw-discover` → `bw-4c-research` + `bw-insight-craft` + `bw-directional-hypothesis`：产出洞察（过 F/P/E/T）+ 方向性假设（双面完整）。
4. 跑 `bw-g1-strategy-gate`：验证门能正确核验 + 输出五出口。
5. **故意制造一次假设证伪**（在账本里标一条 falsified），验证 `bw-backtrack` 正确判定回溯深度 + 标记下游 stale。
6. **故意制造单面倾斜**（删掉产物的 magic 区块），验证 `bw-dual-sided-check` / 门的双面校验阻塞。

**通过判据**：
- 门能在证据不足时正确阻塞（不给 go）。
- 假设证伪能沿血缘传播到正确深度。
- 双面缺失能被拦截。
- 人机分工：所有 converge 动作（选策略/砍概念/G2 裁决）由人完成，AI 只呈现候选。

**单元校验**（可脚本化）：
- assumption-ledger 不变量校验脚本（致命弱点 L4+ 等）。
- 产物 frontmatter status / dual_sided / derived_from 校验脚本。
- `.claude/skills` 与 `.agents/skills` byte-identical（cmp）。

---

## 8. 关键决策权衡

1. **四层架构 vs bmad 单层 agent 菜单**：bewater 决策段是「管理不确定性」不是「执行工作」，必须有独立状态层承载假设链+血缘+回溯。这是和 bmad 的根本差异，也是本方案的核心价值。**状态层独立**让门和能力保持轻薄。
2. **统一 `bw-` 前缀 + frontmatter `layer` 字段**：bewater 缩写名正言顺；不加子前缀保持简洁；`layer` 字段提供结构化分层标识，便于 router 扫描和文档生成。
3. **假设账本单文件 canonical + 产物分散 md + 统一 frontmatter**：账本集中（source of truth，门/回溯单点读取），产物分散（按 stage 组织，handoff 清晰），frontmatter 双向血缘（derived_from/affects）连接两者。仿 `build-plan.yaml` 模式。
4. **决策段不引入 bmad 强 persona**：bewater 强调人机分工（AI diverge / 人 converge），强 persona 会模糊「收敛必须人来」的铁律。工作坊三角色（Problem Owner/Facilitator/Creative Resources）映射为 `bw-creative-meeting` skill 的角色指引，其中 Problem Owner/Facilitator 明确标注「必须是人」。
5. **门 = skill，判据机器核验 + 五出口人工决策**：门的「证据核验」可机器扫账本（确定性），但「五出口决策」是资源分配，必须人拍板（不可让渡）。门 skill 不替人决策，只核验+呈现。
6. **MVP 不做 dist 分发层**：先验证决策段方法论落地本身有效，分发是工程优化，后续按需引入，目录预留。
7. **保留两平台 byte-identical 副本**：仓库既有约定（cmp 校验），已验证的工程实践，不改。
