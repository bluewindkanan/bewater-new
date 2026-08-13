# BeWater 系统全景指南

> 一套"可预测的创新方法论"的可执行工具包：把一条 `Immersion → Discover → Define → G1 → Ideate → Shape → G2 → 交接` 的创新流水线，落地成 22 个 Claude Code skill + 一个确定性运行时（`bw` / `bwkit`）+ 一个新鲜上下文行为评测 harness。
>
> **一句话定位**：AI 负责发散与加速，人负责收敛与决策；工具包强制证据纪律与血缘可追溯，但**从不替人做决定、从不在门里选出口、从不签 F/P/E/T**。
>
> 版本：扫描于 2026-08-10（HEAD `8f8cd35`）。本文是**系统介绍与索引**，非方法论源文档；方法论源文档是 `bewater-methodology/bewater-core.md`（v1.4），技能源文档是 `src/skills/`（部署于 `.claude/skills/`）。

---

## 目录

- [0. 阅读地图](#0-阅读地图)
- [1. 架构总览](#1-架构总览)
- [2. 哲学内核：水的五重性 + 两世界](#2-哲学内核)
- [3. 核心模型与术语](#3-核心模型与术语)
- [4. 横切契约：系统的硬骨架](#4-横切契约)
- [5. 逐 Stage 创新流程 · 步骤 · 产出物（核心章节）](#5-逐-stage-创新流程)
  - [5.1 Immersion 目标对齐](#51-immersion-目标对齐)
  - [5.2 Discover 发现洞察](#52-discover-发现洞察)
  - [5.3 Define 战略定义（枢纽）](#53-define-战略定义枢纽)
  - [5.4 G1 战略门](#54-g1-战略门)
  - [5.5 Ideate 探索概念](#55-ideate-探索概念)
  - [5.6 Shape 方案定义](#56-shape-方案定义)
  - [5.7 G2 概念门 + 执行交接](#57-g2-概念门--执行交接)
  - [5.8 恢复与导航：bw-backtrack / bw-resume](#58-恢复与导航)
- [6. 确定性运行时（bw + bwkit + 状态模型）](#6-确定性运行时)
- [7. Eval Harness（新鲜上下文行为评测）](#7-eval-harness)
- [8. 设计原则与构建历史](#8-设计原则与构建历史)
- [9. 当前真实项目实例](#9-当前真实项目实例)
- [10. 方法论 vs 工具包：调和说明](#10-方法论-vs-工具包)
- [11. 已知开放差异与缺陷](#11-已知开放差异与缺陷)
- [附录 A：产物 ID 速查表](#附录-a产物-id-速查表)
- [附录 B：22 skill 角色速查表](#附录-b22-skill-角色速查表)
- [附录 C：命令速查](#附录-c命令速查)

---

<a id="0-阅读地图"></a>
## 0. 阅读地图

| 你想了解 | 直接看 |
|---|---|
| BeWater 是什么、整体长什么样 | §1 架构总览 |
| 为什么这样设计（哲学） | §2 + §8 |
| 每一步具体怎么做、产出什么 | **§5 逐 Stage**（本文核心） |
| 系统如何保证不被 AI 越权 / 数据不乱 | §4 横切契约 + §6 运行时 |
| 工具怎么跑、状态存在哪 | §6 运行时 |
| 怎么验证 skill 行为正确 | §7 Eval |
| 现在仓库里跑的真实项目 | §9 |
| 哪些是方法论写了但工具没实现的 | §10 + §11 |

> ⚠️ **范围分隔（最重要的一句话）**：本工具包**只实现决策段（管理不确定性）**，即 8 个 Stage 中的 5 个（Immersion / Discover / Define / Ideate / Shape），止于 **G2**。执行段（Design / Build / Launch / Grow）与 G3 / G4 **明确不在范围内、未实现**——不是"未来计划"，而是"刻意外移"给下游交付系统。G2 是本工具包的**终端边界**，也是**全流程最重的门**。

---

<a id="1-架构总览"></a>
## 1. 架构总览

### 1.1 三层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│ 哲学层  水的五重性：渗透(Money+Magic)·流动(假设驱动)·适应(Strategy=Choice)         │
│        ·分流(广发散窄收敛)·成势(归纳+消除法)  ＋  两世界认知开关                    │
├─────────────────────────────────────────────────────────────────────┤
│ 流程层  Start(Immersion) │ 决策段(Strategy+Concept) │ 执行段(外移)                  │
│        Immersion → Discover → Define ─G1─ Ideate → Shape ─G2─ 交接                │
│        4 门 × 5 出口 ＋ 3 种循环（小迭代 / 大回退 / 外环代际）                        │
├─────────────────────────────────────────────────────────────────────┤
│ 知识层  产物链血缘 · 假设账本（6 级证据）· 知识库留底 · 交接协议 · 双学习环           │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 决策段 vs 执行段（核心结构判据）

| | 决策段（Strategy + Concept） | 执行段（Realization + Operation） |
|---|---|---|
| **管理对象** | 不确定性（假设账本） | 确定性交付（范围 / 质量 / 进度） |
| **度量** | 假设验证速度 | 交付速度与质量 |
| **文化** | 推翻重来是常态，**Kill 是成功** | 反复摇摆战略是最大浪费 |
| **门性质** | G1 判断题 / G2 举证题 | G3 清单题 / G4 经营评审 |
| **本工具包** | ✅ 实现（Immersion→G2） | ❌ 外移（Design/Build/Launch/Grow + G3/G4） |

> 最常见的组织失配：**用执行段思维管决策段**（对探索工作要求排期与确定性）。两段管理逻辑必须分开——这是整个方法论的第一判据。

### 1.3 角色三分类（load-bearing，理解全系统的钥匙）

每个 skill 必属于且仅属于一种角色：

| 角色 | 职责 | 能做 | 不能做 | 例子 |
|---|---|---|---|---|
| **Router 导航** | 只读状态、报出路、路由到能力 | orient / resume / report / route | 产出任何工件、改任何状态、记任何决定 | `bw-immersion` `bw-discover` `bw-define` `bw-ideate` `bw-shape` `bw-resume` |
| **Capability 能力** | 产出可迭代草稿，列出候选，**点名人类决策者，停止** | 起草工件、自审、推荐、自动持久化 | 替人签字、锁策略、选概念、选出口、kill/proceed | `bw-project-charter` `bw-discovery-research` `bw-solution-shape` … |
| **Gate 门** | 聚证据、呈现方法论允许的出口、停止 | 装配证据、解析权限、写不可变决策记录、应用动作 | **选出口**、签 F/P/E/T、手写 `_bewater/` 状态 | `bw-strategy-gate`(G1) `bw-concept-gate`(G2) |
| **Recovery 恢复**（能力子类） | 假设被证伪 / 工件修订时，算影响、判循环大小、组装动作计划、停止 | 预分配 ID、写 BT-record + action plan | 静默改已确认基线、自动应用计划 | `bw-backtrack` |

### 1.4 4 门 × 5 出口

| 门 | 位置 | 决策问题 | 性质 | 决策人级别 |
|---|---|---|---|---|
| **G1 战略门** | Define → Ideate | 方向值得投入探索资源吗？ | 判断题（定性为主，容忍高不确定） | 产品负责人（product-owner） |
| **G2 概念门** | Shape → Design | 概念被验证到值得投入建设资源了吗？ | **举证题，全流程最重，本质是立项决策** | 投资决策级（**比 G1 高一级**） |
| G3 发布门 | Build → Launch | 达到进入市场标准了吗？ | 清单题 | （未实现，外移） |
| G4 经营评审 | Grow 段周期性 | 继续投入 / 维持收割 / 退役？ | 生命周期决策 | （未实现，外移） |

**统一五出口**（G1/G2 共享）：`Go · Conditional Go · Recycle · Pivot · Kill`。
- 门**呈现**方法论允许的出口，**人选**。任一阻塞判据失败 → `go` 被机械地从 `exit_allowed` 中剔除。
- **人坚持 Go 但硬判据未达标** → 得到一条 `methodology_deviation` 记录，**绝不**给 `exit:go`、绝不建基线、绝不交接。`L1–L3 自陈 + 人类坚持 ≠ Go`。

### 1.5 三种循环（线性骨架，迭代行为）

| 循环 | 范围 | 治理 | 触发 |
|---|---|---|---|
| **小循环 · 迭代** | 模块内 / 相邻 Stage（Ideate↔Shape、Design↔Build） | 不经过门，是工作节奏 | 常态 |
| **大循环 · 回退** | 跨模块向上游 | **必须过原门重裁** | 已验证前提失效（触基线） |
| **外环 · 代际** | Grow(vN) → Discover(vN+1) | 新一代立项 | 结构性增长洞察 |

**关键不变量**：小循环边界 = 已验证基线。怎么迭代都行，一旦触碰已被门确认的基线 → 性质升级为大循环，必须上报重裁。

---

<a id="2-哲学内核"></a>
## 2. 哲学内核

> 水的隐喻**只在概念层（§1–§2）点题**作记忆抓手；实操层（§3 起）一律用直白 Stage 名（v1.2 起"隐喻回撤"）。

### 2.1 水的五重性（第一性原则）

| 性 | 含义 | 方法论原则 | 落地 |
|---|---|---|---|
| **渗透 Permeate** | 水渗进每条缝隙；创新要浸润两面 | **Money + Magic 双面性**——单面倾斜是最常见死法 | 每个核心产物 schema 的 `dual_sided` 区块 + 每道门的双面检查 |
| **流动 Flow** | 活水长流，不是瀑布 | **假设驱动**——从"证明自己对"到"最快学到哪可能错" | 活的学习计划（每周四问）；边研究边综合 |
| **适应 Adapt** | 水随容器成形 | **Strategy = Choice**——策略是一组选择不是计划 | 策略陈述是"砍选择的刀，不是摘要" |
| **分流 Branch** | 一河分叉、下游汇聚 | **广发散、窄收敛、多支并行** | 一个 Idea Pool（10–15/域）→ Concept Portfolio → 2–4 选中 → 1–2 方案 |
| **成势 Momentum** | 水聚成势 | **归纳 + 消除法**——用证据排除选项、垒信心 | 致命弱点前置 + L4+ 行为证据；目标"让人无法不投" |

### 2.2 Money + Magic 双面性（编码进每个产物）

| | 是什么 | 问什么 |
|---|---|---|
| **Magic**（消费者共情） | 对用户处境与渴望的共情深度 | 你真懂这个用户吗？处境、痛、渴望？ |
| **Money**（商业敏锐） | 生意成不成、怎么赚 | 这生意成不成？怎么持续赚？ |

拆成 4 个可填要素（Charter `dual_sided` schema）：
- **Magic** = `consumer_value_proposition`（给用户什么）+ `consumer_target`（是谁、处境与渴望，⚠️不是"能解决问题"）
- **Money** = `commercial_value_proposition`（怎么成怎么赚）+ `leverageable_assets`（靠什么既有资产建护城河）
- + `tension`（双面在哪里相互制约/成就）+ `balance_choice`（配比权衡）

> ⚠️ **Magic 不是"用户愿不愿买单"**（那是下游验证），而是更上游的**共情深度**。"可杠杆资产"是把双面从口号变成护城河论证的关键。

### 2.3 两世界：创新的认知开关

人一次只能处在一个世界，**两世界错位是门治理冲突的根因**：

| | Creation World（创造世界） | Operational World（运营世界） |
|---|---|---|
| 追求 | 可能性、拥抱意外 | 确定性、避免失败 |
| 答案 | 没有标准答案 | 有对错 |
| 对应 | 决策段（Discover / Ideate / 发散） | 执行段（Build / Launch / 收敛交付） |

> 纪律：开会前先声明"今天在哪个世界"。拿创造世界的早期点子给运营世界的人评审——对方只会逐条证明你错。

---

<a id="3-核心模型与术语"></a>
## 3. 核心模型与术语

### 3.1 4 模块 × 8 Stage（一 Stage 只回答一个问题）

| 模块 | Stage | 核心问题 | 输入 | 输出（出口产物） | 工具包实现 |
|---|---|---|---|---|---|
| **Start** | Immersion | 命题/目标/约束是什么？ | 模糊命题 | 项目章程 + 初始假设 | ✅ |
| **Strategy** | Discover | 事实和洞察是什么？ | 命题 | 研究证据 + 洞察原料 | ✅ |
| | Define | 在哪赢、怎么聚焦？ | 洞察/假设 | 创新策略 + 机会域 | ✅ |
| **Concept** | Ideate | 有哪些可能方向？ | 策略+机会域 | 概念组合 | ✅ |
| | Shape | 哪个方案值得投？ | 概念组合 | 方案 + 商业案例 | ✅ |
| **Realization** | Design | 完整体验/架构长什么样？ | 已验证方案 | 方案规格 | ❌ 外移 |
| | Build | 怎么高质量造出来？ | 规格 | 可发布系统 | ❌ 外移 |
| **Operation** | Launch | 怎么进市场、建动能？ | 可发布系统 | 上线 + 初始动能 | ❌ 外移 |
| | Grow | 怎么形成飞轮并持续？ | 上线+市场数据 | 增长洞察 | ❌ 外移 |

> 一个 Stage 完成的标志不是"活动做完了"，而是**出口产物达到目标状态**。

### 3.2 假设账本 + 6 级证据 + 致命弱点（决策段的脊柱）

**假设账本**（`_bewater/ledger.yaml`）：全项目维护的一张活假设表。每条假设记录：`内容 / 层级 / 类别(category) / 双面(side) / 影响面(impact) / 不确定度(uncertainty) / 证据强度(evidence_level) / 验证状态(validation_status) / 状态(status) / 血缘(derived_from) / L4 义务状态(l4_obligation_status) / 历史(history)`。

**假设层级**（由根到叶）：`root → strategy → opportunity → concept → solution → feature`。回溯路由就按这个层级。

**6 级证据强度**（由低到高，rank-comparable 枚举）：

| 级别 | 类型 | 例子 |
|---|---|---|
| L1 | 主观判断 / 专家意见 | "我觉得用户会喜欢" |
| L2 | 二手数据 / 类比 | 行业报告、相似案例 |
| L3 | 自陈意图（问卷） | 问卷说"愿意买" |
| L4 | **行为信号（非真实交易）** | 假网站注册、广告 CTR |
| L5 | 真实行为 / 真实付费 | 众筹下单、试销购买 |
| L6 | 持续可重复结果 | 多轮实验稳定复现 |

**致命弱点（Achilles Heel）** = `impact=high AND uncertainty=high` 的假设——若错则击垮商业模式、且最没把握。
- `is_achilles_heel` 是**派生属性**（不是手设布尔），防博弈。
- 它触发一条**持久 L4 义务**：`has_durable_l4_obligation` 即使后来把 impact/uncertainty 调低也不会消除——只有 **L4+ 验证结论**或**人签的证据支持的重分类/证伪**才能关闭。
- 这是 `L1–L3 自陈 + 人类坚持 ≠ Go` 在代码层的执行机制：G2 Go 要求每个开放致命弱点 + 每条历史 L4 义务都有 **L4 行为级证据**结论。

### 3.3 Idea Seed → Concept → Solution 三态生命周期（冻结含义）

| 概念 | 冻结定义 | 出现 Stage | ID |
|---|---|---|---|
| **Idea Seed** | 一句话原始可能性，可错/不完整/不可行；血缘与过滤是元数据 | Ideate 发散 | `CS-NNN`（池级唯一） |
| **Concept** | 足以形成理解/可信/吸引/差异化/争论/测试的早期可研究命题——指明创新往哪走，但不是完整方案 | Ideate 发展 | `CI-NNN`（组合级唯一） |
| **Solution** | sharply-defined 的双面命题，含商业/运营/财务假设、证据、实施逻辑、叙事，足以支撑投资决策 | Shape | 无本地 ID |

**拓扑（一条分支全局唯一链）**：一个 Opportunity Portfolio（`OA-`）→ 一个分支全局 Idea Pool（`CS-`）→ 一个分支全局 Concept Portfolio（`CI-`）→ 1–2 个 Solution。

> ⚠️ **New Invention 治理禁令**：超出已选 Concept 边界的新发明**返回 Ideate**，不能绕过人收敛。概念→方案只有 4 条合法路径：`linear-refine / pivot / hybridize / scope-extend`（注意是 `scope-extend` 不是 `scope-expand`；`invent` 非法）。

### 3.4 核心术语速查

| 术语 | 定义 |
|---|---|
| **Fact vs Insight** | Fact=观察；Insight="一句非显而易见的话，为问题投下新光、帮生成方案"。逻辑链：facts → accepted beliefs → insights → hypotheses |
| **F/P/E/T** | 洞察四标准：Fresh(新鲜) / Potent(有力) / Energizing(激发) / Truth(真实) |
| **Accepted Belief** | 被默认、未检验的共识——**洞察的靶子** |
| **方向性假设** | "对创新策略可能是什么的有依据猜测"——By[手段]/We can[客户价值=Magic]/Resulting in[业务收益=Money] |
| **策略陈述** | 策略的"一句话把手"，代表核心选择——**砍选择的刀，不是摘要** |
| **机会域 OA** | 连接策略和概念的桥梁；2–4 个离散、不重叠、可滋生概念的创新方向 |
| **概念的海拔 altitude** | 概念的粒度；判断标准：什么高度对预测试最有用 |
| **健康焦虑** | 好概念应引发的焦虑感（够大吗？够大胆吗？搞得定吗？）；太安全=砍 |
| **假设地图** | 识别概念/方案背后关键假设并按 影响面×不确定度 排序 |
| **投资叙事** | 向决策层汇报的 6 部分外壳（Brief/Opportunity/Solution/Why big/Financial Case/Roadmap） |
| **已验证基线** | 已被门确认的前提集合；触基线=大循环 |
| **学习计划** | 动态研究计划，每周四问：已找到/未找到(灵魂)/待深挖/可放弃 |

**来源优先级**：原始 F212 培训材料 + 一手案例 > 派生的英文 BeWater 合同 > 当前技能/运行时/夹具/生成物。方法论资产汇自 **F212 + frog + 人本设计(IDEO)** 三条脉络，**去品牌化**呈现（`Frog:f212 General/` 与 `resources/` 为原始语料）。

---

<a id="4-横切契约"></a>
## 4. 横切契约：系统的硬骨架

这些是贯穿所有 skill / 运行时 / eval 的不变量，理解它们就理解了系统如何"防止 AI 越权、防止数据腐烂"。

### 4.1 ID 方案（稳定、永不全分支复用）

| 前缀 | 实体 | next_id 存于 |
|---|---|---|
| `BR-` | 分支 branch | `config.next_ids.branch` |
| `A-` | 假设 assumption | `ledger.next_id` |
| `ART-` | 工件 artifact | `config.next_ids.artifact` |
| `EXP-` | 实验 experiment | `config.next_ids.experiment` |
| `E-` | 证据 evidence | （就地条目，按分支） |
| `D-` | 门/回溯决策记录 | `config.next_ids.decision` |
| `B-` | 基线 baseline | `config.next_ids.baseline` |
| `BT-` | 回溯记录 backtrack | `config.next_ids.backtrack` |
| `ACT-` | 动作计划 action | `config.next_ids.action` |
| `C-` | 条件 condition | `conditions.next_id` |
| `OA-` / `CS-` / `CI-` | 机会域 / 种子 / 概念 | **工件本地**（不从 config.next_ids 分配） |

**类型化引用**：`artifact:ART-001@3`、`assumption:A-001@4`（`@n` 钉住可变 record revision）；`gate:D-001`、`baseline:B-001` 不可变（无 `@n`）。

### 4.2 四种版本模型（并存）

| 模型 | 用于 | 机制 |
|---|---|---|
| **就地 bump** | 假设 record_revision、conditions、evidence、config/ledger 信封 | bump `revision` 字段；假设额外把旧状态压入 `history[]` |
| **追加新文件** | 工件 `ART-001-r3-*.md`、证据 | 同 `artifact_id` + 下一 `revision`，`supersedes_ref` 链 |
| **跨文件不可变** | 基线 `B-002` 取代 `B-001` | 重新校验时**新建**决策+基线，动作计划切换 `active_baselines` 指针 |
| **跨文件版本化+文件内不可变** | 门决策 `D-` | 新 attempt → 新 `D-`；决策核心（到 exit）人定后不可变，仅操作字段 CAS 改 |

`supersedes_ref` 双语义：(a) 自修订前驱 (b) 跨实体替换——按自身 ID/类型与引用 ID/类型 比较消歧。

### 4.3 人机分工铁律

**核心原则：AI 负责 diverge（发散），人负责 converge（收敛）——converge = choice = 灵魂。**

人不可让渡的三件事：
1. **判断选择**（converge=choice）：选哪条策略、砍哪个概念、kill 还是 proceed、G4 裁决、选门出口。
2. **共情**（真人访谈）：真实用户处境理解。
3. **品味直觉**：感知健康焦虑、判断概念海拔、辨别"非显而易见"的洞察、体验/架构品味。

工具包层的硬执行：代码里的 `_is_human_actor` 检测拒绝 `ai/agent/system/assistant/model/bot` 名字的决策者——终结态（selected/killed/merged）、种子确认、Solution 校验、门出口，**必须有真人 actor**。

### 4.4 直接写状态禁令 + 唯一写路径

- **永不手写 `_bewater/` 状态**（CLAUDE.md 硬规则）。
- 工件持久化**唯一合法路径**：`PYTHONPATH=_bewater python3 -m bwkit plan apply .`（由各 skill 的 `emit_*.py` 生成 JSON 计划管道输入）。
- **禁用** Edit/Write/shell 重定向/heredoc/通用脚本直接改 `_bewater/` 或 `_bewater-output/`。
- `plan apply` 自带单写锁（acquire/release），不需要另调 `bwkit lock`。

### 4.5 写入顺序不变量（门 + 回溯）

预分配所有 ID → **先**写完整决策/BT-record + `action_status:pending`（在任何其他状态变更之前）→ 经 `bwkit plan apply` 应用（幂等：已完成=skipped，冲突=failed+停）→ 经 CAS commit 回写各步状态。冲突永不静默 pending → 走 `manual-repair`，阻塞后续状态变更 skill 直到人解决。

### 4.6 部署模型（install.sh）

```
src/skills/bw-*        →  <project>/.claude/skills/bw-*
src/skills/_bw-shared  →  <project>/.claude/skills/_bw-shared
src/bwkit              →  <project>/_bewater/bwkit        (原子替换，.bewater-managed 标记)
bwkit init             →  初始化 _bewater/{config,ledger,conditions}.yaml + records/ + _bewater-output/
```

- 首个工作流动作是 **Immersion**；`bw-resume` 可随时只读导航。
- 安装前 `bwkit init --check` 只读预检，**拒绝**向不兼容的既有生命周期状态部署（invalid 报错而非覆盖）。
- 原子部署（temp 暂存 + mv）+ marker 门控（绝不 rm -rf 未管理目标）；过时 managed skill 在全量安装时修剪（如重构后的 `bw-concept-card`）。

> ⚠️ **已知部署漂移**（见 §11）：当前 `src/skills/` 与 `.claude/skills/` 存在概念生命周期命名漂移——`.claude/skills/`（已部署、正确）用 `concept-lifecycle.md` + `concept-seed-pool-template.md`，而 `src/skills/`（源、未回填）仍是旧名 `idea-concept-solution-lifecycle.md` + `idea-pool-template.md`。**生命周期命名的权威以 `.claude/skills/` 为准**；从当前 `src` 跑下一次 `install.sh` 会回退已部署版本。

---

<a id="5-逐-stage-创新流程"></a>
## 5. 逐 Stage 创新流程 · 步骤 · 产出物

> 本章是全文核心。每个 Stage 用统一模板：**定位 / 角色(skill) / 创新流程(步骤) / 关键方法工具 / 产出物(ID+schema+修订) / 交接 / 判断标准 / 人机分工 / 真实样例**。
> 真实样例来自仓库内运行的「百度智能云 AI 硬件 token 业务」项目（见 §9）。

---

<a id="51-immersion-目标对齐"></a>
### 5.1 Immersion 目标对齐 —— 对齐命题，播下假设种子

**定位**：Start 模块入口。把用户模糊意图转成 Money+Magic 双面的 Charter + 3–5 条可证伪 root 假设 + 一份可选的源引用咨询报告。**只产草稿、不验证、不做门决策、不选是否继续。**

| skill | 角色 | 职责 |
|---|---|---|
| `bw-immersion` | Router | 只读报 Charter 头 + 精确 revision + 活跃 root 假设快照 + Assessment 状态(missing/failed/stale/current)，推荐唯一下一步并停 |
| `bw-project-charter` | Capability | 自适应访谈 → 起草 Charter + 3–5 root 假设 → 分级自审 → 自动持久化 |
| `bw-initial-assessment` | Capability | 新鲜上下文跑，对精确输入 revision 做 3–5 源轻量外部研究，产源引用咨询报告 |

**创新流程（bw-project-charter 的 Explore→Converge 自适应访谈）**：

1. 读活跃分支 + 当前 Charter + ledger 头；内部维护覆盖清单（why now/触发；具体人/处境/渴望/当前行为；替代方案+成本；命题+期望改变；Magic/Money/可杠杆资产；范围/约束/成功信号；Known/Believed/Unknown/Tension）。
2. **Explore（自由式，一次一问）**：在 4 个锚点齐备前（触发/why now + 具体人+处境 + 当前行为或显式 Unknown + 期望改变）——只问开放问题，**不给选项**，把推论标 `agent-interpretation`。丰富初始 prompt 可直接跳 Converge。
3. **Converge（结构化选择，一次一问）**：锚点齐备后，对框架/范围/优先级/权衡/Magic-Money 配比/成功信号用**宿主原生结构化选择**，每项含 `Uncertain` + Other（"都不准确—我想补充"）。推荐必须引述上下文 + 说明权衡（优化什么/牺牲什么/可信替代/什么会改变推荐）。
4. **每个高影响断言记 provenance**：`user-stated` / `user-selected` / `agent-interpretation` / `unknown`。`user-selected` 是 L1 输入，**永不**静默升格为 user-stated/Fact/证据。
5. 字段清楚/用户明确不知/该 Discover 查时停止追问。**Unknown 是合法结果**。
6. **Charter 起草 + 分级自审**（L0 确定性校验 via `validate_draft.py` → L1 同语境语义审计）→ 自动修可解问题 → 重跑。
7. **统一意图校准（L2）**：展示 4–7 条源标签断言镜像，问"哪一点最不准/最该用你自己的话？"——**开放修正机会，不是签字/审批/门**。
8. **持久化**：L0/L1 通过后**立即**持久化，无保存确认。`bwkit lock` + CAS 追加 Charter r1 + 3–5 root 假设。Charter 保持 `document_status:draft / validation_status:unvalidated`；假设 `evidence_level:L1 / untested`。**不写 signoff、不改 current_stage**。
9. **Assessment 交接**：Charter+假设提交后，把 `(分支, 精确 Charter revision, 精确 root 假设快照)` 传给 `bw-initial-assessment` 在**新鲜上下文**单独跑。

**产出物**：

| 产物 | ID | 关键字段 | 修订模型 |
|---|---|---|---|
| **Charter** | `ART-001` | `kind:charter, stage:immersion, document_status:draft, validation_status:unvalidated`；`dual_sided.{magic,money,tension,balance_choice}`；`derived_from:[]`；Body: Intent trace(Claim\|Provenance\|Basis\|Calibration) + Original intent + Structured interpretation(who-what-how-why/目标/现状/命题/成功信号/范围) + Money+Magic + Current knowledge state(Known/Believed/Unknown/Tensions) + **Discover handoff**(核心探索问题/待挑战信念/根假设研究图(Assumption\|4C\|Why it matters\|Evidence needed\|Disconfirming signal)/起始 4C 问题/研究边界) | 追加：`ART-001-r1`(supersedes:null) → r2 supersedes r1；重试时 Charter write_new 先于 counter CAS |
| **3–5 root 假设** | `A-001..A-005` | `layer:root, evidence_level:L1, validation_status:untested, status:active, derived_from:[artifact:ART-001@<rev>]`；`is_achilles_heel` 派生(impact=high AND uncertainty=high)→持久 L4 义务 | 就地 record_revision bump + `history[]` |
| **Initial Assessment** | `ART-002` | `kind:initial-assessment, stage:immersion`；`derived_from` **精确** = 当前 Charter revision + 完整活跃 root 假设快照；8 节(总体结论/专业视角 Magic\|Money\|Innovation/候选洞察 2–3/核心冲突/最有希望方向/关键风险≤3+证伪信号/Discover 任务/研究边界+源)；每条关键判断带五标签 trace(Charter basis→External signal→Assessment inference→Implication→What would change) | 追加；快照失配=stale，永不就地改旧文件 |

**关键方法/工具**：Explore→Converge 自适应访谈；Money+Magic 四要素；provenance 四标签；L0/L1/L2 分级自审（`validate_draft.py` 硬拒非法 provenance）；4C 透镜；CAS 事务写。

**交接**：精确 Charter revision + 完整活跃 root 假设快照（→ Assessment；→ bw-discover）。

**判断标准**：各方对命题与成功标准达成一致；初始假设 ≥3 条。（注意：**无 Charter 质量评分门**——方法论文档提的 L1–L4 Charter 成熟度/质量分**实现中刻意未采纳**，见 §10。）

**人机分工**：AI 起草章程/整理输入/自审/自动持久化；人锁定命题与成功标准（diverge=人自由作答，converge=AI 给结构化选择、人选）。**Charter 自动持久化 ≠ 决定继续**；阶段跃迁需人单独显式决定。

**真实样例**（`ART-001-r1-charter.md` + `A-001..A-005`）：
- 双面：Magic=`consumer_value_proposition`(端云协同+算力托管，比直接调 API 更优)、`consumer_target`(国内 AI 硬件品牌厂商/方案商)；Money=`commercial_value_proposition`(卖 token=卖算力+卖解决方案)、`leverageable_assets`(端云协同技术/算力托管/智能硬件经验)；`tension`(技术变现 vs 市场机会抢占)。
- Intent trace 13 行带 provenance，4 行 `unknown`（客户具体需求、核心差异化、端云协同 vs API 差异、具体成功指标）。
- 5 条 root 假设：A-001(Consumer/magic：OEM 普遍需外采推理)、A-002(Commercial/money：差异化是端云协同降低端侧硬件依赖，光学显示占 BOM 34%)、A-003(可持续报价区间)、A-004(市场进入大规模铺货)、A-005(Consumer：愿从纯 API 转向端云协同)。其中 A-001/A-002/A-004 为 Achilles（high×high）。

---

<a id="52-discover-发现洞察"></a>
### 5.2 Discover 发现洞察 —— 把事实炼成洞察

**定位**：Strategy 模块。用 4C 定向探索 + 自适应 Sprint 循环，把事实炼成洞察原料（Insight Ingredients），**绝不**产最终洞察、不签 F/P/E/T、不组方向性假设、不选出口。**洞察边界绝对**：研究只产原料，F/P/E/T 判断 + 人签字在 Define 的 `bw-insight-craft`。

| skill | 角色 | 职责 |
|---|---|---|
| `bw-discover` | Router | 只读：确认 discover、验正式输入(Charter revision + 完整 root 假设快照)、读匹配 Assessment（仅翻译 4 字段：候选洞察→待验证判断、核心冲突→优先挑战、最有希望方向→候选路径、关键风险→证伪问题）、报 4C 覆盖/Discover Plan/证据缺口，路由 research 或（洞察就绪时）define |
| `bw-discovery-research` | Capability | 单一 AI 研究能力：初始化/推进一个活 `kind:research` 工件，跑自适应多 Sprint 循环，组装最小互补 Method Bundle（33 法分层 Toolkit），有界并发研究，单写 Coordinator 扇入，洞察就绪时浮出 Insight Ingredients |
| `bw-insight-craft` | Capability（归 Define 路由） | 走认知阶梯 Facts→Accepted Beliefs→Insights，13 透镜 + Pearl/Code/Force 生成候选，F/P/E/T 判断，写 `kind:insights` 工件，**停给人签 F/P/E/T** |

**创新流程（bw-discovery-research 自适应 Sprint）**：

1. **Entry**：读当前 Charter revision + 完整活跃假设快照 + 创新挑战 + 研究边界 + 战略不确定性。
2. **Orient**：4C 罗盘 + 挑战特定扩展透镜(Technology/Regulation/Economics/Ecosystem/Future)扫盲点；折入 Research Frame + Living Learning Agenda（无单独 Orient 工件）。
3. **Plan 下一 Sprint**：起草 Frame + Agenda；对每个最高学习价值问题**先**推导证据需求**再**选方法，从分层 Toolkit 组最小互补 Method Bundle（按需加载，绝不整包注入）；解析各方法 `execution_need` 对照宿主工具。
4. **Plan 自审**（4 检查：占位/一致/范围/歧义）后持久化/执行；歧义则问一问停。
5. **Execute**：Coordinator 自选执行模式（顺序 / query 级并行 / mission 级并行 / 依赖波），**每波 ≤2–4 worker**（并发上限，非范围上限）；worker 只读，返回结构化 Research Packet。
6. **Fan-in**：Coordinator 单写——归一化 packet、按底层 origin 去重、查 claim-to-source 支持、对单边 claim 搜反证、保矛盾/替代、跑 10 点扇入质量审计；一次 commit 写归一证据 + 下一 revision。
7. **Sprint Synthesis**：每次有意义的 Sprint 后跑综合（learned/contradicted/belief changed/reframed/deepened/dropped/new questions/remaining gaps），按边际战略学习选转移(continue/deepen/redirect/synthesize/stop)，**无固定 Sprint 数**。
8. **Insight Readiness**（Coordinator 主题级判断，7 条）：关键不确定性已证据化或显式缺口；4C+扩展透镜已查；支持与反证都考虑；矛盾/替代可见；Sprint Synthesis 识别出 Insight Ingredients；边际学习不足以再开一 Sprint；剩余不确定性已带出。

**关键方法/工具**：
- **4C 覆盖罗盘**（Consumer/Company/Category/Channel + 5 扩展透镜）——是盲点检查，**不是**任务/章节/worker 划分。
- **33 法分层 Toolkit**（`research-toolkit.csv`）：采集 9 / 分析 11 / 验证 6 / 综合 7。种子库非白名单，按需加载。
- **Method Bundle**：每学习问题组最小互补集（跨层；一法只在提供独特证据形式/视角/推断/挑战/综合操作时才入选；不要求每层一法）。
- **认知四阶梯**：Facts → **Accepted Beliefs**（洞察的靶子）→ Insights → Hypotheses。
- **13 洞察透镜**：痛点挣扎/未满足向往/用词语言/趋势背后 why/跨类类比/文化消费/失效范式/无意识行为/品类空白/怪癖仪式/隐秘行为/补偿行为。
- **Pearl/Code/Force 三法**：Pearl(客观记意外)→Code(假设都为真，列 3–5 解释假设)→Force(归纳拼接成新洞察)。
- **F/P/E/T 四标准**：Fresh/Potent/Energizing/Truth。

**产出物**：

| 产物 | ID | 关键字段 | 修订模型 |
|---|---|---|---|
| **Research 工件（活）** | `ART-003` | `kind:research, stage:discover`；`derived_from`(精确 Charter rev + 各活跃假设 rev)；Body: Research Frame / Living Learning Agenda / Latest Research Sprint(执行后) / Sprint Synthesis & Plan Delta / **Insight Ingredients** & Insight Readiness / Remaining uncertainty | 追加链；r1=仅 Frame+Agenda（无空 Sprint 占位） |
| **Insight Ingredients**（交接载荷，非独立工件） | ART-003 的节 | patterns / tensions / anomalies / challenged Accepted Beliefs / reframe candidates / strategic relevance / limitations | 随 ART-003 revision 流入 insight-craft |
| Research Packet | （瞬态，非工件） | findings[claim, source_ref, source_title, source_date, source_location, source_family, independence_key, evidence_form, support, limitation] / contradictions / unanswered_questions / queries_attempted / stop_reason | 扇入归一化后丢弃 |
| **Insights 工件** | `ART-004`（Define 阶段写） | `kind:insights, stage:define`；`derived_from: artifact:ART-003@<rev>`；`signoffs[]: {insight(I/II/...), role, fpet{fresh,potent,energizing,truth}, status(retained 可选), signed_at}`；Body: Insight Portfolio | 追加；当前 revision 人签 F/P/E/T |

**交接**：方向性假设（→ Define）。原始素材进知识库留底。

**判断标准**：4C 不瘸腿；能区分 Fact/Accepted Belief/Insight；≥1 条洞察让人"意外但合理"；洞察过 F/P/E/T（人签）。

**人机分工**：AI 执行全部研究、综合、洞察就绪判断；**用户不被问研究模式/worker 数（自动+内部）**。会改变 mission/决策/优先级/范围/权限/资源的实质歧义 → 问一问停。研究里**永不签字**。F/P/E/T 由人签（`bw-insight-craft` 一次问"签哪几条"，如 `1,3,4`）。

**真实样例**：
- `ART-003-r2-research.md`：derived_from = ART-001@1 + A-001..A-005@1；Sprint 2 Method Bundle = desk-document-research + competitive-benchmarking-positioning + pricing-unit-economics + source-family-triangulation；**Sprint 1 断言"AI 算力稀缺"被 Sprint 2 发现"2025 大模型 API 价格战"证伪 → reframe 为"硬件成本优化路径"**（redirect 转移）。
- `ART-004-r1-insights.md`：4 条正式洞察——I"硬件成本优化 > API 成本优化"(光学显示占 34%, F/P/E/T 全 true, 已签)、II"品类聚焦 AI 眼镜"(全 true, 已签)、III"厂商积极实践端云协同"(**Energizing=false, status:retained**, 已签——示范部分 F/P/E/T 保留)、IV"竞争逻辑从价格转向差异化"(全 true, 已签)。
- `docs/discover/primary-triggers/`：BR-001 项目级人执行田野研究指南（PT-1 OEM 访谈 / PT-2 联合测价 POC / PT-3 内部成本数据清单），**刻意捕获 L4 行为证据**（过去 12 个月切换行为、真实 POC 参与而非自陈意愿）；这是项目文档，**非**技能级机制（技能级 Primary Trigger/research_mode 已删，见 §10）。

---

<a id="53-define-战略定义枢纽"></a>
### 5.3 Define 战略定义 —— 把洞察炼成选择（全方法枢纽）

**定位**：Strategy 模块，整个方法的**枢纽**。消费 Discover 的签名洞察，产出**且仅产出** G1 的 6 个就绪输入：签名洞察 / 2–5 方向性假设 / 锁定策略陈述 / 2–4 机会域 / 假设初始盘点+致命弱点象限 / Money+Magic 初判。G1 容忍高不确定，但要求连贯方向 + 可见风险（不要求 L4）。

| skill | 角色 | 职责 |
|---|---|---|
| `bw-define` | Router | 只读：报 Define 状态（6 个 G1 输入各自就绪？），按缺口路由到对应能力 |
| `bw-directional-hypothesis` | Capability | 从当前 revision 人签洞察碰撞出 2–5 候选方向性假设(By/We can/Resulting in + 4C 覆盖 + 双面)，停给人选哪几条关闭 |
| `bw-strategy-statement` | Capability | 起草"砍选择的刀"策略陈述候选（2 写法：捕捉 pivot insight / narrowed opportunity），跑刀口测试，停给人选/锁 |
| `bw-opportunity-area` | Capability | 定义一个 Opportunity Portfolio 修订链：2–4 离散/不重叠/可滋生概念的方向，停给人确认边界 |
| `bw-assumption-map` | Capability | 建/改假设账本，按 类别×影响面×不确定度 排布，识别致命弱点象限（持久 L4 义务），停给人重分类签字 |
| `bw-insight-craft` | Capability | （见 §5.2，归 Define 路由） |

**创新流程**：

- **方向性假设**：用 By[手段]/We can[客户价值=Magic]/Resulting in[业务收益=Money]，每子句引 ≥1 洞察且覆盖全部 4C（不瘸腿）。一工件持全部 2–5 候选（组合模式）。关闭=在当前 revision 加 per-candidate signoff（无需新 revision）。
- **策略陈述**：2 合法写法；跑"刀口测试"——能否砍掉至少一个候选方案？砍不掉=它是摘要不是策略。失败模式：术语堆砌、重述简报。锁=当前 revision 人签 `scope:locked`。
- **机会域**：4 种切法（消费者原型/业务支柱/消费者需求/旅程阶段）；2–4 个；互不重叠；是机会不是功能模块；每个能 spawn 多概念。`OA-NNN` ID 工件本地、跨链永不复用；**权威血缘在 canonical `opportunity_areas[]` frontmatter，Markdown 标题(OA-1)仅渲染**。
- **假设地图**：5 类(consumer/commercial/technical/distribution/regulatory) × 影响面 × 不确定度；致命弱点 = high×high → 派生 + 持久 L4 义务。

**产出物**：

| 产物 | ID | 关键字段 | 修订模型 |
|---|---|---|---|
| **方向性假设** | `ART-005` | `kind:directional-hypothesis, stage:define`；`derived_from`(签名洞察 revision)；`signoffs`(per-candidate: hypothesis#, role, dual_sided{magic/money/tension/balance}, signed_at) | 追加；候选就地关闭(加 signoff) |
| **策略陈述** | `ART-006` | `kind:strategy, stage:define`（⚠️ frontmatter `kind:strategy`，内容是 strategy-statement，见 §11 矛盾）；`dual_sided`；`signoffs`(strategy id, role:product-owner, scope:locked)；Body: 候选陈述 + 锁定陈述 + By/We can/Resulting in + **刀口(切掉什么)** + 双面 + 状态 | 追加；锁=当前 revision 签 `scope:locked` |
| **机会域** | `ART-007` | `kind:opportunity, stage:define`；`opportunity_areas[]`(id:OA-NNN, name, audience, opportunity, consumer_value, commercial_value, source_insight_refs)；Body: OA 节 + 切法说明 + 重叠声明 + 区域对比 | 追加；OA-NNN 工件本地、跨链不复用 |
| **假设账本记录** | `A-006..`(strategy/opportunity 层) | `layer:strategy\|opportunity, category, side, impact, uncertainty, evidence_level, derived_from, l4_obligation_status` | 就地 record_revision + history[] |

**判断标准（G1 6 输入）**：洞察经人签 F/P/E/T；2–5 方向性假设关闭且双面；策略陈述锁定过刀口测试；当前 Opportunity Portfolio `opportunity_areas[]` 含 2–4 稳定 OA；假设账本初始盘点 + 致命弱点象限已识别；Money+Magic 双面初判成立。

**人机分工**：AI 洞察碰撞/4C 填充/策略候选/绘假设图；人选哪个策略、签 F/P/E/T、重分类假设 L4 义务。

**真实样例**：
- `ART-005-r2`：3 候选——C1"硬件成本优化(端云协同作 BOM 降本杠杆)"+C2"品类聚焦"均 ✅已关闭(product-owner 签)，C3"差异化竞争"○未关闭。每条带 4C 覆盖(insight:ART-004@1:I/II/III/IV 引用) + 双面。
- `ART-006-r2`：S3"聚焦 AI 眼镜，且只以硬件降本为锚" ✅已锁定；**刀口(切掉什么)** 显式列出：✂️切掉泛 AI 硬件全品类平台 / ✂️切掉按 token 流量计费 / ✂️切掉 API 价格战低价竞争。
- `ART-007-r1`：3 个 OA 按消费者原型(厂商层级)切——OA-1 旗舰硬件降本+体验不降、OA-2 腰部/入门低成本进市场(白牌)、OA-3 传统眼镜/AR 品牌转型；明确重叠声明(OA-2↔OA-3 白牌 vs 白标轻微重叠、OA-1↔OA-2 技术交集但分服务高端/长尾)+共用底座说明；每个 OA 列"可滋生概念"。

---

<a id="54-g1-战略门"></a>
### 5.4 G1 战略门 —— 判断题：方向值得投入探索资源吗？

**定位**：Define → Ideate 的判断题门。聚 G1 证据、呈现 5 出口、停给产品负责人级决策人，再写+应用所选动作。**从不选出口。**

| skill | 角色 | 职责 |
|---|---|---|
| `bw-strategy-gate` | Gate | 解析分支+subject+决策人+触发；逐 G1 判据 pass/fail/unknown（数**一个**当前 Opportunity Portfolio 头里的 `opportunity_areas[]` 条目，**不数**独立 Opportunity 文件）；呈现允许出口；预分配 ID→写决策记录+action plan(pending)→`bwkit plan apply`→校验+diff→applied |

**判据清单**（`_bw-shared/gate-criteria.md`）：
- [ ] 洞察经人签当前 revision F/P/E/T
- [ ] 2–5 方向性假设关闭且双面(By/We can/Resulting in)
- [ ] 策略陈述锁定过"是刀不是摘要"测试
- [ ] 一个当前 `kind:opportunity` Portfolio 含 2–4 稳定 `OA-NNN`、互不重叠、各自能孵多概念
- [ ] 假设账本初始盘点 + 致命弱点象限已识别（**不要求已验证**）
- [ ] Money+Magic 双面初判成立

> G1 容忍高不确定：要连贯方向 + 可见风险，**不要** L4 验证。

**5 出口与状态动作**（`references/exits.md`）：
- **Go**：建不可变 `B-xxx` 基线（冻结 strategy_statement + opportunity_areas + assumption_inventory + money_magic_judgment）、推进 `current_stage:ideate`、设 `active_baselines.G1:B-xxx`。
- **Conditional Go**：写 `C-xxx` 条件、标记 conditional、推进 ideate、**无**已验证基线、下一门在后续 Go 取代前不合规。
- **Recycle**：建 `BT-xxx`、分支回更早 stage、保留证据。
- **Pivot**：先查活基线、建后继分支、按变更深度路由。
- **Kill**：失效门决策、清基线指针、关条件、**最后**标记 branch killed；保留全部工件。

**产出物**：`D-xxx`（决策记录，核心到 exit 人定后不可变）、`B-xxx`（Go 才建，冻结态）、`ACT-xxx`（动作计划，幂等应用）。

**人机分工**：AI 装配证据+解析权限+起草决策记录；**人选出口**。决策人 null/歧义/低于 product-owner → 只渲染就绪报告、**无决策记录**地停。坚持 Go 但硬判据失败 → `methodology_deviation` 记录，不给 Go/基线/交接。

**真实样例**：`_bewater/records/D-001-gate.md`（G1 Go, decision_maker=秋南Dylan product-owner, subject_refs=ART-006@2 strategy + ART-007@1 opportunity）；`B-001-baseline.yaml`（G1 基线，checklist 6 项全 pass：insights_fpet_signed / hypotheses_closed_dual_sided / strategy_locked / opportunity_areas_2_4 / achilles_quadrant_identified / money_magic_initial_judgment）。

---

<a id="55-ideate-探索概念"></a>
### 5.5 Ideate 探索概念 —— 一个池 → 一个组合 → 收敛

**定位**：Concept 模块。一条分支全局唯一生命周期：一个 Idea Pool（`CS-` 种子，每 OA 10–15）→ 人确认短名单 → 一个 Concept Portfolio（`CI-` 概念，精确 Opportunity/OA/Pool/Seed 血缘）→ 有界修订 → 全局 2–4 人选概念交 Shape。

| skill | 角色 | 职责 |
|---|---|---|
| `bw-ideate` | Router | 只读：报种子计数/短名单确认/概念生命周期态/修订阻塞/组合就绪，路由到 seed 或 development |
| `bw-concept-seed` | Capability（发散） | 创/改**一个**分支全局 Idea Pool，每 OA 发散 10–15 一句话 Seeds，推荐 OA 级短名单，**停给人确认** |
| `bw-concept-development` | Capability（发展+评估） | 仅消费**人确认**的 Seeds，在**一个**分支全局 Concept Portfolio 发展 `CI-` 概念，跑硬/软标准，有界修订（max 2 AI 提议），批量收敛视图后停给人 select/review/merge/kill |

**创新流程**：

**发散（bw-concept-seed）**：
1. 解析活跃分支 + 精确锁定策略 revision + 精确机会 revision；Portfolio 须暴露 2–4 `opportunity_areas[]` 稳定 `OA-NNN`。
2. 找分支既有 idea-pool 链；存在则**修订该链**（输入变了在下 revision 记新精确 refs），**永不**建第二条 Pool 链。**唯一键 = `branch_id`（非快照哈希）**。
3. 每 OA 用 brainstorm + "how might we" 发散 10–15 Seeds；`CS-NNN` 池级唯一、跨修订为同一种子保留、永不重派/复用。
4. 每个 Seed：唯一必填一句话 `idea` + `source_insight_refs`；`cluster_id`/`strategy_filter` 是系统元数据（非发展内容）。
5. 近重复聚类但**保留每个 Seed 可见**（含重复、过滤失败、未入选）——防 AI 藏点子。
6. 每 OA 单独推荐 `shortlist.recommended`，持久化 AI 推荐 revision，**停**。**不**填 `shortlist.confirmed`。
7. 人显式确认后，追下 revision，记 `decisions[]`(type:confirm-shortlist, seed_ids, decided_by:{type:human})。

**发展+评估（bw-concept-development）**：
1. 解析精确 idea-pool 头；要求人确认 Seeds；Portfolio 钉相同 strategy_ref + opportunity_ref。
2. 找既有 concept-portfolio 链；上游/概念变了则修订；**永不**建第二条链。
3. 把确认 Seeds 发展成 `concepts[]`（稳定 `CI-NNN`），记精确 `opportunity_area_id` + `source_seed_id`。拒绝 Seed 未确认或属别 OA 组的概念。
4. 填研究性命题字段，**不**展开成完整 Solution。`pithy_description` ≤5 词；`how_it_works` 保持机制级。
5. **硬标准**（全过才进人收敛）：精确血缘 / 一条未解决张力 / 机制独特 / Who-What-How-What it replaces-Why Big 完整 / 策略适配 / 可预测试海拔 / 概念级假设。
6. **软标准**（可见不阻塞，10 项）：理解/可信/吸引/差异化/命名/可视化/设计原则/Money∩Magic 分/海拔/**健康焦虑**。
7. 建概念层 ledger 假设（`source_concept_id` + 精确 Portfolio revision）。
8. 每概念推荐**恰好一个**有界动作：refine/pivot/split/merge/kill/recycle-to-OA。recycle-to-OA 经 `bw-backtrack`。merge 造**新** `CI-` 带**双亲** parent_ids（永不就地改亲）。**2 次 AI 修订提议后停**，除非人显式要再来一轮。
9. 批量收敛视图后**停**给人决策。人决策后追下 revision：仅显式人输入填 selected/killed/merged + 各概念终结字段；`exit.selected_concept_ids` 填 2–4 个。

**产出物**：

| 产物 | ID | 关键字段 | 修订模型 |
|---|---|---|---|
| **Idea Pool** | `ART-008`(模板) | `kind:idea-pool, stage:ideate`；`input_snapshot.{strategy_ref,opportunity_ref}`；`opportunity_areas[].{opportunity_area_id, seeds[](id:CS-NNN, idea, source_insight_refs, cluster_id, strategy_filter), shortlist.{recommended(AI), confirmed(human)}}`；`decisions[]`(confirm-shortlist, 人 actor) | 追加；唯一键=branch_id；CS-NNN 池级唯一、跨修订为同种子保留、移除/kill/merge/split/backtrack 后永不复用 |
| **Concept Portfolio** | `ART-009`(模板) | `kind:concept-portfolio`；`strategy_ref/opportunity_ref/idea_pool_ref`；`concepts[]`(id:CI-NNN, item_revision, opportunity_area_id, source_seed_id, parent_ids, name, pithy_description, consumer_insight, commercial_insight, idea_definition, who_its_for, how_it_works(机制级), what_it_replaces, why_big, visualization, design_principles[], dual_sided, evaluation{hard,soft,revision_attempts,recommended_action}, assumption_refs[assumption:A-NNN@record_revision], decision(null\|selected\|killed\|merged), merge_into)；`decisions[]`；`exit.selected_concept_ids`(2–4) | 追加；CI-NNN 组合级唯一；merge 造新 CI- 带双亲；AI 2 次修订后停 |

**确定性校验器**（`src/bw/concept_lifecycle.py`）：链唯一性 / ID 跨修订不重派 / 种子计数(≥10/OA) / CS-NNN 正则+池级唯一 / 确认短名单须有人 confirm-shortlist 决策 / Portfolio opportunity_ref 须=Pool 快照 / 概念 OA 须=源种子 OA 组 / 源种子须在 confirmed / 硬字段非空 / dual_sided 完整 / merge 完整性 / 终结决策须有人 actor / selected 须硬标准全 true / `exit.selected_concept_ids` 须 2–4 且=selected 集合。**接 `validate_all`**。

**交接**：`concept-portfolio` 精确 revision + 2–4 `selected_concept_ids`（→ bw-shape）。全部 Seeds/Concepts/修订可回溯。

**判断标准（概念收敛检查点，Ideate→Shape，轻量就绪检查，不设大门）**：含 2–4 选中概念、硬标准全过、≥2 引发健康焦虑（人工判断项，软阻塞——少于 2 个须人显式 override 才路由 Shape）、全过策略陈述过滤器。

**人机分工**：AI 发散种子/发展概念/跑硬软标准/起强名/推荐修订动作；人确认种子短名单、收敛选择(select/revise/merge/kill)、感知健康焦虑、定海拔。**selected/killed/merged 仅人记录**。

> 真实项目此阶段产物在 ledger 可见：`A-012..A-024` 概念层假设带 `source_concept_id: CI-001..CI-012`，引用 `artifact:ART-011@1`（概念组合头，⚠️ 当前 `_bewater-output/` 缺该工件文件 → `validate` 报 dangling-ref，见 §11）。

---

<a id="56-shape-方案定义"></a>
### 5.6 Shape 方案定义 —— 测致命弱点，做成"无法不投"

**定位**：Concept 模块，G2 前最后一段。消费 Ideate 组合交接（2–4 选中概念），发展成 1–2 个双面已验证 Solution（带源引用商业案例 + 投资叙事 + 每个致命弱点 L4+ 证据）。Shape 无自己的门，收敛进 G2。判据："**make it impossible not to invest**"。

| skill | 角色 | 职责 |
|---|---|---|
| `bw-shape` | Router | 只读：确认 shape、验 Ideate 组合交接（2–4 选中概念、硬标准过），缺失/越界/硬标准未过→回 `bw-ideate`（小循环），路由 solution-shape/experiment/investment-narrative/G2 |
| `bw-solution-shape` | Capability | 经恰好一条有界路径把选中概念发展成双面 Solution，填 5 规范区块，解致命弱点(L4+)，停给人 validation/Kill-Proceed |
| `bw-experiment` | Capability | 设计/记录假设驱动实验 + 人 Kill/Proceed；致命弱点实验**必须**目标 L4+ 行为证据 |
| `bw-investment-narrative` | Capability | 把 1–2 完整已验证 Solution 包进 6 部分叙事 + 源引用财务案例，停给人投资判断 |

**创新流程**：

- **概念→方案 4 路径**：`linear-refine` / `pivot` / `hybridize`(≥2 源概念) / `scope-extend`（每路径恰好 1 源概念，除 hybridize）；`invent` 非法——超边界新发明回 Ideate。
- **Solution 5 规范区块**（前置数据**唯一权威**，Markdown 正文是确定性投影 `render_solution_body(frontmatter)`；校验比归一化正文报 projection drift，**绝不**解析标题推断完整度）：
  1. `definition`（name, pithy_proposition, what_it_is, who_its_for, dual_sided, dimensions）
  2. `how_it_works`（端到端步骤；每步 action/消费者收益/运营收益/战略依据/法律监管依据/evidence_refs/design_refs）
  3. `how_to_implement`（阶段/时间/目标/JTBD/能力资产/owner/依赖/风险/开放问题/试点推广）
  4. `how_it_makes_money`（收入流/定价量/采纳留存频次/成本/Base+Aggressive 场景/收入利润投资回收期/源引用假设/敏感性/模型缺口）
  5. `validation`（消费者渴望/商业价值/可行性 各{claim,evidence_refs} + 钉 Achilles 假设 + 实验 + 证据 + 无效主张）
- **content_gaps vs applicability_exceptions**：未验证时缺项须精确列 `content_gaps`(field_path+reason) 或 `applicability_exceptions`(field_path+rationale)；**已验证 Solution 不得有 content gaps**；exception 不得豁免 `.source` 或 `validation.achilles_assumption_refs`。
- **假设驱动实验 4 步**：识别 → 聚焦致命弱点 → 真实行为测试 → 必要时重复。**Proceed/Kill 阈值在观察结果前固定**（预承诺赌注）。实验菜单：fake-website / social A/B(CTR~0.9%) / crowdfunding(L5) / mom-test(问"做过什么") / related-worlds / expert interview(L2) / Van Westendorp / guerrilla interview。
- **投资叙事 6 部分**：①Brief ②Opportunity ③Solution ④Why big ⑤Financial Case ⑥Roadmap。叙事**呈现**而非**重建**规范区块——**叙事不能替方案补缺**。

**产出物**：

| 产物 | ID | 关键字段 | 修订模型 |
|---|---|---|---|
| **Solution** | `ART-NNN` | `kind:solution, stage:shape`；`validation_status: unvalidated\|in-review\|validated\|invalidated`；`source_concepts.{portfolio_ref, concept_ids[CI-], path}`；5 区块 + `content_gaps` + `applicability_exceptions` + `signoffs`；**已验证须人签** `{scope:solution-validation, artifact_revision==revision}` | 追加；1–2 条独立链 |
| **Experiment** | `EXP-NNN` | `kind:experiment, stage:shape`；`solution_ref`(精确 Solution rev)；`target_assumption_refs`；`target_evidence_level:L4`；`proceed_threshold/kill_threshold`；`conclusion:supported\|falsified\|inconclusive` | 追加；EXP-id 从 `config.next_ids.experiment` |
| **证据条目** | `E-NNN` | `evidence:E-NNN@n` 就地条目（`_bewater/evidence.yaml`，⚠️当前工作树已删，见 §11） | 就地层 |
| **投资叙事** | `ART-NNN` | `kind:investment-narrative, stage:shape`；`dual_sided`；`financial_assumption_refs`；`derived_from:[validated solution(s)]` | 追加 |

**确定性校验器**（`src/bw/solution_contract.py`）：4 路径约束 / 5 区块齐 / 必填缺项分类(gap/exception/real gap) / 投影确定性 / **Achilles 并集**（=源概念开放持久 L4 义务 ∪ Solution 层义务，集合精确相等 + 钉 record_revision）/ 已验证须 Achilles 全 L4+closed+supported / Focused+Detailed+Persuasive 谓词 / 已验证须人 solution-validation 签字（拒机器名）。

**交接**：1–2 已验证 Solution + 投资叙事 + L4 证据 + 源引用财务假设（→ bw-concept-gate / G2）。

**判断标准**：方案三件事——**聚焦(Focused)/详尽(Detailed)/有说服力(Persuasive)**；未验证版本每个缺项有精确 content_gap；已验证无 gap、财务假设有源、全部致命弱点 L4+。

**人机分工**：AI 假设地图/实验设计/二手实验执行/财务建模/起草叙事；人一手实验、Kill/Proceed、Solution validation 签字、投资判断。

---

<a id="57-g2-概念门--执行交接"></a>
### 5.7 G2 概念门 + 执行交接 —— 举证题，全流程最重

**定位**：Shape → Design 的举证题门，本质是**立项决策**。决策人**投资决策级**（比 G1 高一级）。聚证据、呈现 5 出口、停给投资决策人。Go 解锁建设资源 + 冻结不可变基线 + 写执行交接。**L4+ 行为证据是硬地板。**

| skill | 角色 | 职责 |
|---|---|---|
| `bw-concept-gate` | Gate | 解析分支+subject(1–2 已验证 Solution+叙事)+投资决策人+触发；逐 G2 判据 pass/fail/unknown（复用 solution_contract 谓词，先跑 `bwkit check integrity`）；呈现允许出口；预分配 ID→写决策+action plan(pending)→`bwkit plan apply`→校验+diff→applied |

**判据清单**（全过才 Go）：
- [ ] 1–2 完整 `validated` Solution，各 derived from 精确选中 Concept ID
- [ ] 每个 Solution 5 区块齐、无 content_gaps、applicability_exceptions 有理由、无投影漂移、过 Focused/Detailed/Persuasive
- [ ] **每个当前致命弱点 + 每条开放历史 L4 义务 有 L4 行为证据结论**（自陈意图不算数）
- [ ] 每条财务假设挂源 + 逻辑
- [ ] 投资叙事 6 部分齐 + 双面
- [ ] 人解"make it impossible not to invest"判断
- [ ] 精确输入 revision 可成已验证基线

> 不可协商规则：**L1–L3 自陈 + 人类坚持 Go 永不给 Go、基线或交接**。坚持 Go 但硬判据失败 → `methodology_deviation` 记录。

**L4 门控状态（已机械化）**：`src/bw/gate_scan.py:179-190` 的 `_score_l4_obligations` 对每条开放致命弱点/L4 义务发**阻塞** `methodology-deviation` Criterion——所以"L4 硬门"是**真在代码里**，不是纸面。真正的现场差距是：当前活项目里 `bw gate-scan G2` 在 `io.load_ledger`(yaml 加载)处崩溃，且 G2 权限为 null，所以门**暂时跑不起来**（逻辑在，数据加载断），见 §11。

**5 出口与 G2 特性**：
- **Go**：建不可变 `B-xxx` 基线、推进 `current_stage:handoff-ready`、设 `active_baselines.G2`、写 `execution-handoff.md`、设 `active_execution_handoff=gate:D-xxx`。
- **Conditional Go**：仅写 `provisional-handoff-{decision-id}.md`（无基线、不占 active_execution_handoff）；不可用来把失败的 L4 硬判据洗成"已满足"；强制 closeout 后才下一门合规。
- **Recycle/Pivot/Kill**：同 G1 模型；Pivot 先查活基线定循环大小；Kill 保留全部证据。

**执行交接（execution-handoff）合同**（Go 才产，工具包终端交付物）：

| 字段 | 内容 |
|---|---|
| `source_g2_decision` | `gate:D-NNN` |
| `baseline_ref` | `baseline:B-NNN` |
| `validated_solutions[]` | 精确 Solution revision |
| `investment_narrative_ref` | 投资叙事 |
| `financial_case` | 财务案例 |
| `open_assumptions_to_monitor[]` | 上市后待观察假设 |
| `exact_source_revisions` | config / ledger 精确 revision |

> 每项目**恰好一个 active handoff**；取代前交接设 `supersedes_handoff_ref` + 归档前交接。Conditional Go 只产 provisional（非 active）。

**产出物**：`D-NNN`(决策)、`B-NNN`(Go 才建基线，冻结 validated_solutions+assumption_snapshot+open_observations+strategy_opportunity_lineage)、`execution-handoff.md`、`provisional-handoff-{decision-id}.md`(Conditional Go)。

**真实项目状态**：G2 权限 null、`active_baselines.G2:null`、24 条假设全 `untested` 且 L4 义务全 open → G2 Go 当前会被阻塞（符合设计）。

---

<a id="58-恢复与导航"></a>
### 5.8 恢复与导航：bw-backtrack / bw-resume

| skill | 角色 | 职责 |
|---|---|---|
| `bw-backtrack` | Recovery | 假设被证伪/工件修订时，4 类血缘边建影响图，按**是否触活基线**判循环大小，组装 BT-record + 有序动作计划，提议路由，**停给人**。永不静默改基线/自动应用 |
| `bw-resume` | Router（全局只读） | 任意时刻只读导航：报项目状态+下一人决策，安全时推荐唯一下游 skill。从不产工件/选出口/写状态/应用恢复 |

**回溯循环大小（baseline-first，非假设启发式）**：
- `ledger_ops._LAYER_LOOP`：feature/solution→(small, Shape)；concept→(small, Ideate)；opportunity/strategy→(large, Define)；root→(large, Discover)。
- **触任何活基线 → 升级 large + `must_repass_gate`**。大循环动作序：失效门决策 → 清基线指针 → 归档 handoff → 追 stale/invalidated 工件 revision → 改 stage → 调度门重跑。
- 被杀分支保留其已验证假设结论（继续服务其他分支）——kill 是分支状态变更，非数据删除。

**bw-resume 扫描序**：(1) 收集分支适用开放条件；(2) 验活 G1/G2 基线指针+源决策（失配=阻塞）；(3) 查门/回溯记录的 pending/manual-repair 动作计划，按所有权路由（root gate+G1→bw-strategy-gate；gate+G2→bw-concept-gate；backtrack record→bw-backtrack）；(4) 查生命周期头。未知 stage/损坏/冲突所有权 → fail closed。

---

<a id="6-确定性运行时"></a>
## 6. 确定性运行时（bw + bwkit + 状态模型）

确定性机器半。stdlib-only Python。`src/bw` 三重角色：**(1) oracle**（skill/门调 `bw validate`/`bw gate-scan` 读健康态）；**(2) helper 源**（schema dataclass/Enum 被技能与 bwkit 复用）；**(3) eval judge**（同套确定性校验器服务于 eval harness）。严格分层：`src/bw`=方法论感知 ops（import yaml、知 schema）；`src/bwkit`=schema 无关、YAML 无关、stdlib-only 状态工具（永不 import yaml 或 bw）。

### 6.1 `bw` CLI（`src/bw/cli.py`）

| 命令 | 作用 | 退出码 |
|---|---|---|
| `bw ledger add/update/validate/trace/backtrack/baseline` | 假设账本唯一写边界；trace 双向走血缘；backtrack 路由证伪假设；baseline 快照 | 0/1 |
| `bw validate` | `validate_all`：扫全树返回每条 Issue（不变量+引用完整性+双向无环+单面+missing-final+F/P/E/T+概念/Solution 血缘）。空=clean | 0/1 |
| `bw hash [--refresh-deps\|--stale]` | 正文(不含 frontmatter)sha256；刷新依赖哈希/报陈旧 | 0 |
| `bw gate-scan <G1\|G2>` | 数据驱动打分器打每判据 pass/fail + 算 `exit_allowed`；**不**决策 | 0(go 在内)/1/2(未实现门) |

### 6.2 `bwkit` CLI（`src/bwkit/cli.py`）

| 命令 | 作用 |
|---|---|
| `bwkit lock acquire/release/status` | 单写锁 `_bewater/.bw-lock`（pid 活性 + ttl 抢占，原子 os.replace） |
| `bwkit cas show/commit <path> --expected <rev>` | 文本级 revision CAS（永不 import yaml）；`CasConflict`/`BadRevisionBump`；轮转备份留 5 |
| `bwkit plan apply <root>` | 幂等可恢复动作计划（read stdin JSON）；acquire 全计划锁；write_new/cas_commit 两 op；重跑跳已应用步 |
| `bwkit check integrity` | 工件修订链健康（一头/工件、无重复/缺前驱/环）；读 stdin JSON |
| `bwkit scan impact` | 反向 BFS 算影响爆炸半径；读 stdin `{edges,roots}` |
| `bwkit init [--check]` | 三态分类(fresh/valid/invalid)；fresh 建 `_bewater/` 骨架；invalid 报错不覆盖 |

### 6.3 `_bewater/` 状态树

```
_bewater/
├── config.yaml          # 项目+分支{current_stage,status,active_baselines{G1,G2}}+decision_authority{G1,G2}
│                        #   +active_branch +active_execution_handoff +next_ids
├── ledger.yaml          # 假设 A-NNN（layer/category/side/impact/uncertainty/evidence_level/
│                        #   validation_status/status/derived_from/l4_obligation_status/history[]）+ next_id
├── conditions.yaml      # C-NNN 条件注册表（空：本项目未用过）
├── evidence.yaml        # 就地 E-NNN@n 证据条目（⚠️当前工作树已删，见 §11）
├── records/             # D-NNN-gate.md(决策) + B-NNN-baseline.yaml(基线) + BT-NNN-backtrack.yaml(回溯)
└── bwkit/               # 部署的运行时副本
_bewater-output/         # 追加只读工件 ART-NNN-rN-<kind>.md（用户语言保留）
```

**关键不变量**（`schema.Assumption.invariant_violations()` 单一源）：Achilles(impact=high AND uncertainty=high) 若 `validation_status==supported` 且 `evidence_level<L4` → 违反。`validate`/`ledger_ops`/`gate_scan` 全过此逻辑。`has_durable_l4_obligation` 查 risk_history+history → 义务**存续**于降风险之后。正文 only 哈希（不含 frontmatter）是陈旧检测的枢纽。

> ⚠️ **双账本加载器 caveat**：`bw validate`（`validate.validate_all`）在当前项目状态**能跑**（返回 50 条 issue，多为 dangling-ref 如 `artifact:ART-011@1`、`insight:ART-004@1:I`）；而 `bw gate-scan G2` 用**不同的** `io.load_ledger` 加载器，在活项目**会崩**于 yaml 加载处。这是真实运行时差异，非"validate 全崩"。

> ⚠️ **双基线格式 caveat**：`records/B-001-baseline.yaml` 用 `{baseline_id, gate, frozen{...}, checklist_result[]}`（门冻结记录）；而 `bw ledger baseline` 的 `ledger_ops.baseline()` 写 `{gate, snapshot:{assumptions,artifacts}}`（机器快照）。两者是**不同的东西**，勿混。

---

<a id="7-eval-harness"></a>
## 7. Eval Harness（§11.1 新鲜上下文行为评测）

**authoring-only**（不发布、非 bwkit、不被 install.sh 安装）。证明 skill 在**真实新鲜 LLM 上下文**里行为正确。位于 `evals/_harness/` + `tests/`。

**数据流**：manifest(loader) → Sandbox(isolation, 每 rep) → run_once(Codex) → judge(checks+oracle+NL→needs-review) → 持久 transcript → result.write_result → `evals/{skill}/{green|red}/{scenario_id}-r{rep}.json`。

| 组件 | 职责 |
|---|---|
| `isolation.py` | 每 rep 真隔离：repo 外 temp product cwd + temp HOME（无用户/全局 skill 泄漏）+ 依赖 skill 装入 + 目标 skill 仅 GREEN 装入；CODEX_HOME 透传保 auth；可选 DEEPSEEK→Anthropic base-URL 重映射 |
| `runner.py` | 每 rep spawn 一个 headless Codex（`codex exec --json --ephemeral --sandbox workspace-write`），捕获 JSONL event 流为 transcript，解析 fresh_context_id(thread.started 的 thread_id) |
| `judge.py` | 机械打分：结构化 checks(transcript_contains/regex/fs_no_new_files/fs_wrote_file_matching/oracle_validate_ok) + 只读 src/bw oracle；**每条 NL 断言独立成 needs-review 项**；forbidden 行为只机械检测"写工件"类，余下人审。**严格不让 LLM 评判 LLM** |
| `result.py` | §11.1 结果 schema；`derive_verdict` 单一源（caller verdict 被覆盖）：任一 needs-review→needs-review；否则全过且无 forbidden→green；否则 red |
| `orchestrator.py` | 串 isolation→runner→judge→result；rep 分层（manifest `repetition_count`）；CLI `python -m evals._harness run [--skill|--all] [--mode] [--rep] [--model]` |

**RED/GREEN 模型 + rep 分层**：GREEN=目标 skill 在，须过每条 check 且无 forbidden；RED=目标 skill 缺（对照），须失败 ≥1 目标行为。rep 默认 3；**安全关键门场景 5**（g1-go/g1-no-authority、g2-go/g2-no-authority/g2-conditional）——安全关键须 5/5。目标 skill 是**唯一实验变量**（cwd/model/prompt/依赖 skill/fixture 跨 RED/GREEN 固定）。

**覆盖**：24 个 `bw-*` suite 目录，22 个带 manifest（bw-start / bw-4c-research 无——路由入口/废弃槽）。GREEN ≈70 manifest（bw-project-charter 14、bw-discovery-research 12、bw-initial-assessment 10、bw-immersion 6 最多）。每 suite 有 `red/no-skill.yaml` RED 对照。

**已知现实**：461 条已提交结果 verdict=needs-review（因每条 NL 断言按设计是 needs-review）、3 条 red、3 个内层 check=pass（机械 GREEN 已证可行）。**§11.3 自动结果门当前缺失**——计划中的 `scripts/verify.py` 已删除/重构，现验证 = pytest `validate_skill_evals` + `bwkit check integrity`，无自动强制 RED 失败/GREEN 过/reviewer 身份。

---

<a id="8-设计原则与构建历史"></a>
## 8. 设计原则与构建历史

### 8.1 三条设计宪法

1. **最小化（minimal by default）**：每个元素须自证存在。一阶段/角色/工件一职责。一句够则不写两句；一个 skill 能做则不造两个。
2. **English-first**：方法论设计资源（SKILL.md、references、templates、design specs）全英文；用户面工件（Charter、Assessment 等）保留用户语言。
3. **自包含 + MECE**：runtime 最小化、自包含、互斥完备。

### 8.2 角色与规则

- **永不**选门出口；**永不**签 F/P/E/T；**永不**手写 `_bewater/` 状态。
- L4+ 行为证据是硬门判据——L1–L3 自陈 + 人类坚持 ≠ Go。
- 能力产草稿停止；门聚证据停止；人决定。
- 源变更永不手改已生成生命周期态；不兼容态需单独再生成授权。
- **Superpowers 政策**：只允许本地 `brainstorming` skill；不调用/推荐/转交任何其他 `superpowers:*`。

### 8.3 阶段构建史（TDD 先行）

| 阶段 | 内容 | 测试 |
|---|---|---|
| Phase 0 | bwkit/cas + 权威共享 schema + eval/installer 测试 harness | 168 passed |
| Phase 1a | G1 脊柱：3 router + project-charter/4c-research/insight-craft + 方向假设/策略陈述/机会域/假设地图 + installer | 208 |
| Phase 1b | G1 闭环：4 Define 能力 + bwkit applier + bw-strategy-gate(全 5 出口) | 231（**Phase 1 完成**） |
| Phase 2a | Ideate + helpers（bw-concept-card → 后被重构）+ integrity/lineage | 254 |
| Phase 2b | G2 闭环：Shape + bw-concept-gate(全 5 出口) + G2 基线 + execution-handoff + bw-backtrack（**20 skill**） | 272, cov 96% |
| Eval §11.1 | isolation+runner+judge+orchestrator+verify；T1–T6 pilot-ready | 311 |
| 研究质量+并发 | 源中性证据 + 自适应并发（5 提交） | — |
| insight-sprint 重设计 | 自适应 Sprint + 分层 33 法 Toolkit + Method Bundle + Insight Ingredients 边界 + 12 eval 场景（4 提交） | 428, cov 95% |
| 概念生命周期重构（2026-08-09） | concept-seed-pool + concept-portfolio 取代 concept-card；concept_lifecycle 校验器接 validate_all；bewater-core 统一数量合约 | 457, cov 95%（⚠️ memory 标"未提交"） |
| 方法论 skill review（2026-08-10） | 5 Critical + 10 Major；commit `8f8cd35` 开始修 P0–P1 | — |

**TDD 纪律**：每 skill ≥3 压力场景；行为塑造规则重复 ≥5 次；RED-then-GREEN 在新鲜隔离上下文；覆盖地板 80%（`pyproject` `fail_under=80`）；60 个 `test_*.py`。

---

<a id="9-当前真实项目实例"></a>
## 9. 当前真实项目实例

仓库 `_bewater/` 里跑着一个**真实**项目，完整演练了决策段管线：

- **项目**：百度智能云智能硬件 — AI 硬件 token 业务（BR-001）
- **当前阶段**：`shape`（已过 G1）
- **决策人**：G1 = 秋南Dylan（product-owner）；**G2 = null（未设）**
- **基线**：`active_baselines.G1 = B-001`；`G2 = null`
- **工件链**（`_bewater-output/`）：ART-001 Charter → ART-002 Assessment → ART-003 Research(r1/r2) → ART-004 Insights → ART-005 方向假设(r1/r2) → ART-006 策略(r1/r2) → ART-007 机会域 → （概念组合 ART-011 头，⚠️文件缺失→dangling）
- **假设账本**（`ledger.yaml`）：24 条 A-001..A-024，跨 root/strategy/opportunity/concept 层
  - root（A-001..A-005）：3 Achilles（A-001/A-002/A-004）
  - strategy（A-006..A-009）：A-002/A-003 已演进到 record_revision:2（A-002 从"单位推理成本优势"reframe 为"端云协同降低端侧硬件依赖（光学显示占 BOM 34%）"）
  - concept（A-012..A-024）：带 `source_concept_id: CI-001..CI-012`；**8 条 killed**（A-014/A-016/A-017/A-018/A-019/A-022/A-023/A-024）——概念收敛剪枝已发生
  - **全部 24 条 `validation_status: untested`，L4 义务全 open** → G2 Go 当前会被阻塞（符合设计）
- **门记录**：`D-001-gate.md`（G1 Go by 秋南Dylan）；`B-001-baseline.yaml`（G1 基线，6 checklist 全 pass）

> 这个实例既证明管线端到端能跑到 Shape，也暴露了 review 的关键缺口：全 untested 意味着 validate_all 在真实态会报 issue（已验证：50 条 dangling-ref），L4 义务全开意味着 S4 硬门是当前挡住过早 G2 Go 的唯一屏障。

---

<a id="10-方法论-vs-工具包"></a>
## 10. 方法论 vs 工具包：调和说明

方法论文档（`bewater-core.md`）描述的某些特性，在**实现中被刻意删除/重命名/替换**。读源文档时勿假设它们已实现：

| 方法论描述 | 实现现实 |
|---|---|
| Discover 田野方法包（AEIOU 观察网格 / 沉浸 / 极端用户 / 投射三件套 / 类比启发 / 资源流 / 同伴观察） | Toolkit 采集层用**不同方法名**（contextual-observation-diary-intercept-survey 等）；AEIOU 等词汇在 bw-discovery-research references **不存在**，仅存于 `bewater-core.md` 方法论层 |
| 综合流水线（每日 Download → Stories → Themes → Insight Statements → Frameworks） | 实际综合 = **Sprint Synthesis**（learned/contradicted/belief changed/reframed/deepened/dropped/new questions/remaining gaps）喂 Insight Ingredients |
| Charter L1–L4 成熟度 / 质量分 / 方向质量门 | 实现**刻意拒绝**：无 Charter 质量评分门、无成熟度分级；complete-draft 确认点已移除；仅 claim 级 provenance 保留 |
| Shape 5 路径（含 "New Invention"） | 实现 **4 路径**（linear-refine/pivot/hybridize/scope-extend），`invent` 非法；New Invention 治理禁令：超边界回 Ideate |
| 概念卡片（bw-concept-card，8 字段 + 7 硬标准） | 概念生命周期重构后**替换**为 concept-seed-pool + concept-portfolio（种子/概念/方案三态） |
| research_mode / Primary Trigger / primary-secondary 区分（技能级） | **已删**（2026-08-06 并发计划）；项目级 PT 文档（`docs/discover/primary-triggers/`）作为可选人执行上下文保留 |
| 知识库（跨流可查、留被杀分支结论、打标签） | 方法论层描述；运行时/技能层**无 Knowledge Base 工件或标签方案**——愿景未实现 |

---

<a id="11-已知开放差异与缺陷"></a>
## 11. 已知开放差异与缺陷

来源：2026-08-10 方法论 skill review + 完整性 critic 实测。commit `8f8cd35` 开始修 P0–P1。

**P0（会导致误读全系统）**：
1. **L4 门控状态**：`_score_l4_obligations` 已在 `gate_scan.py:179-190` 实现，发阻塞 `methodology-deviation`。真实差距是活项目 `bw gate-scan G2` 在 `io.load_ledger` 崩溃 + G2 权限 null（逻辑在，数据加载断），**非**"L4 门仅纸面"。
2. **validate vs gate-scan 加载器**：`bw validate` 能跑（50 issue，多为 dangling-ref）；`bw gate-scan G2` 用不同 loader 会崩。差距是**两个加载器**，非"validate 全崩"。
3. **src↔.claude/skills 漂移（确认 live）**：`.claude/skills/_bw-shared/concept-lifecycle.md` + `concept-seed-pool-template.md` 已部署（正确），但 `src/skills/` 仍是旧名 `idea-concept-solution-lifecycle.md` + `idea-pool-template.md`。**生命周期命名以 `.claude/skills/` 为准**；下次从 `src` 跑 `install.sh` 会回退。

**P1（覆盖不足 / 跨切契约不一致）**：
4. **概念组合工件缺失**：活 ledger 12 条概念层假设引用 `artifact:ART-011@1`（概念组合头），`_bewater-output/` 无该文件 → validate 报 dangling。
5. **evidence.yaml 删除**：工作树 `D _bewater/evidence.yaml`，但 shape/g2-recovery 合约依赖就地 `evidence:E-NNN@n` 条目。**工具包锁定的合约是就地层**（shape+g2-recovery+runtime 一致；discover 的"仅追加"描述已过时）。
6. **§11.3 结果门缺失**：计划中的 `scripts/verify.py` 自动强制（RED 失败/GREEN 过/reviewer 身份）已删；461 条 needs-review 无自动强制。
7. **知识库未实现**（见 §10）。

**P2（validator 矛盾，逐字标记未决）**：
8. `ART-006` frontmatter `kind: strategy` vs 内容/技能称 `strategy-statement`——别名还是不一致？
9. `backtrack()` 返回**单个** `must_repass_gate`（按门序取最新基线文件）vs 技能层引用 `gates_to_rerun` **列表**——多门重跑是否支持未决。
10. 概念组合 ID 不一致：Ideate 报告引 `ART-008/009/011/012` 作模板，活 ledger 引 `ART-011@1` 作概念组合头——夹具 vs 真实？
11. `scope-extend`（正确 token，`solution_contract.py:15`）vs 任务简报/他处 `scope-expand`——以 `scope-extend` 为准。
12. 条件注册表 `conditions.yaml` schema 完整但**从未在任何真实或 eval 项目演练过**（本项目空）——Conditional Go→closeout→Go 端到端无验证。

**bwkit 已知小缺陷（review minor）**：6 个 `.backup-*` 仍被 git 跟踪；3 个潜在 bug（lock TOCTOU、`keep_backups=0` 删全部、`acquire_lock` 无条件 mkdir `_bewater`）。

---

<a id="附录-a产物-id-速查表"></a>
## 附录 A：产物 ID 速查表

| ID | 实体 | 产出 Stage | 说明 |
|---|---|---|---|
| `ART-001` | Charter | Immersion | 项目章程 + Money/Magic 双面 + Discover handoff |
| `ART-002` | Initial Assessment | Immersion | 源引用咨询报告（advisory，非门） |
| `ART-003` | Research | Discover | 活研究工件 + Insight Ingredients |
| `ART-004` | Insights | Define | Insight Portfolio + F/P/E/T 签字 |
| `ART-005` | Directional Hypothesis | Define | 2–5 候选假设（By/We can/Resulting in） |
| `ART-006` | Strategy (Statement) | Define | 锁定策略陈述 + 刀口 |
| `ART-007` | Opportunity | Define | Opportunity Portfolio（OA-001..） |
| `ART-008/009` | idea-pool / concept-portfolio（模板） | Ideate | CS- 种子 / CI- 概念 |
| `ART-011` | concept-portfolio（真实头） | Ideate | ⚠️活 ledger 引用，文件缺失 |
| `ART-NNN` | solution / investment-narrative | Shape | 5 区块 / 6 部分叙事 |
| `EXP-NNN` | Experiment | Shape | 假设驱动实验 + Kill/Proceed |
| `E-NNN` | Evidence | Shape+ | 就地证据条目（evidence.yaml） |
| `A-NNN` | Assumption | 全程 | 假设账本（layer: root→feature） |
| `OA-/CS-/CI-` | 机会域/种子/概念 | Define/Ideate | 工件本地 ID |
| `B-NNN` | Baseline | G1/G2 | Go 才建，冻结态 |
| `D-NNN` | Decision | G1/G2 | 门决策记录 |
| `BT-NNN` | Backtrack | Recovery | 回溯记录 + 动作计划 |
| `C-NNN` | Condition | Conditional Go | 条件注册表 |
| `ACT-NNN` | Action | 全程 | 幂等动作计划 |

---

<a id="附录-b22-skill-角色速查表"></a>
## 附录 B：22 skill 角色速查表

| Stage | Router | Capability | Gate/Recovery |
|---|---|---|---|
| Immersion | `bw-immersion` | `bw-project-charter` `bw-initial-assessment` | — |
| Discover | `bw-discover` | `bw-discovery-research`（+ `bw-insight-craft` 归 Define 路由） | — |
| Define | `bw-define` | `bw-directional-hypothesis` `bw-strategy-statement` `bw-opportunity-area` `bw-assumption-map` | — |
| G1 | — | — | `bw-strategy-gate` |
| Ideate | `bw-ideate` | `bw-concept-seed` `bw-concept-development` | — |
| Shape | `bw-shape` | `bw-solution-shape` `bw-experiment` `bw-investment-narrative` | — |
| G2 | — | — | `bw-concept-gate` |
| 全局 | `bw-resume` | — | `bw-backtrack`（Recovery） |

---

<a id="附录-c命令速查"></a>
## 附录 C：命令速查

```bash
# 运行时（src/bw）
bw validate                              # 全树不变量扫描
bw gate-scan G1 .                        # G1 证据打分（不决策）
bw ledger add . --statement "..." --layer root --category consumer \
        --impact high --uncertainty high --branch BR-001
bw ledger trace A-002 --direction downstream
bw ledger backtrack A-002
bw hash _bewater-output/ART-001-r1-charter.md --stale

# 工具（src/bwkit）
bwkit lock acquire . --owner "$(whoami)"
bwkit cas commit <path> --expected <rev>          # stdin=新文本
bwkit plan apply <root> < plan.json               # 唯一合法状态写路径
bwkit check integrity                             # stdin=records JSON
echo '{"edges":[...],"roots":[...]}' | bwkit scan impact
bwkit init . [--check]

# 安装/部署
./install.sh                       # 全量：部署 skill + bwkit + 初始化状态
./install.sh --skills-only         # 仅更新 skill，不动 _bewater 状态

# 测试 / 评测
.venv/bin/python -m pytest         # ~457 passed, cov 95%（fail_under=80）
python -m evals._harness run --all --mode green --rep 3   # 新鲜上下文行为评测（成本 gated）
```

---

*BeWater：决策段管理不确定性（探索流向），执行段管理确定性交付（工程入海）。工具包实现决策段，止于 G2——全流程最重的立项门。AI 加速 diverge，converge 必须人亲自来。*
