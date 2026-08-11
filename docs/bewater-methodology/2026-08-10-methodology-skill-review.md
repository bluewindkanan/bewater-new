# BeWater 方法论 & Skill 设计评审报告

- **日期**：2026-08-10
- **范围**：`bewater-methodology/bewater-core.md` 方法论 + `src/skills/bw-*` 全部 skill + `src/bw`/`src/bwkit` 运行时 + `evals/` 评估体系 + `_bewater/` 状态层
- **方法**：4 个子代理并行深挖（bwkit 实现 / skill 架构 / 方法论忠实度 / 状态层与 eval），关键发现已逐条用 `diff`/`grep`/读源码人工复核
- **结论速览**：方法论本身成熟自洽；问题集中在「方法论承诺」与「skill/bwkit 实现」之间的落差，其中 4 项会直接阻塞系统正确运行

---

## 评审覆盖图（pipeline 实现度）

| 方法论阶段/门 (§) | 实现？ | Skill |
|---|---|---|
| Immersion (§5.0) | 是 | bw-immersion, bw-project-charter, bw-initial-assessment |
| Discover (§5.1.1) | 部分 | bw-discover, bw-discovery-research（仅桌面研究，缺田野方法包） |
| Define (§5.1.2) | 是 | bw-define, bw-insight-craft, bw-directional-hypothesis, bw-strategy-statement, bw-opportunity-area, bw-assumption-map |
| **G1** (§6.1) | 是 | bw-strategy-gate |
| Ideate (§5.2.1) | 是（src 侧术语漂移） | bw-ideate, bw-concept-seed, bw-concept-development |
| 概念收敛检查点 | 声明未强制 | 仅显示，无硬停止 |
| Shape (§5.2.2) | 是（src 侧契约不符） | bw-shape, bw-solution-shape, bw-experiment, bw-investment-narrative |
| **G2** (§6.1) | 是 | bw-concept-gate |
| Design (§5.3.1) | **缺** | — |
| Build (§5.3.2) | **缺** | — |
| **G3** (§6.1) | **缺** | — |
| Launch (§5.4.1) | **缺** | — |
| Grow (§5.4.2) | **缺** | — |
| **G4** (§6.1) | **缺** | — |
| handoff (Shape→Design) | 占位 | 仅作为 bw-backtrack 可归档目标存在 |
| 回溯 (§6.2) | 是 | bw-backtrack |
| 恢复 | 是 | bw-resume |

工具链实现 8 阶段中的 5 个（Immersion→G2），在 G2 截断。执行段（Design/Build/Launch/Grow）与 G3/G4 完全未实现。

---

## 严重（阻塞正确运行，须立即修）

| # | 问题 | 证据 | 影响 | 修复 |
|---|---|---|---|---|
| S1 | **`src/skills` 与部署版 `.claude/skills` 严重漂移，重部署会回退系统** | `.claude/skills/` 被 `.gitignore:25` 忽略；`diff` 确认 `bw-ideate`/`bw-shape`/`bw-solution-shape` 三处 SKILL.md 均不一致；6 个 src 文件残留旧词汇 | 下次 `install.sh` 用 src 覆盖正确部署，把系统打回重构前 | 把 2026-08-09 concept 重构从部署版回填到 src 并提交；加 CI 门 `diff -r src/skills .claude/skills` |
| S2 | **Ideate→Shape 移交契约在 src 里是断的** | src 版引用幽灵 skill `bw-idea-seed`/`bw-notion-development`、幽灵契约 `idea-notion-solution-lifecycle.md`、`notion-portfolio`/`NT-` id；真实能力产出 `concept-portfolio`/`CI-`（见 `_bw-shared/concept-lifecycle.md`） | 新上下文按 src 的 SKILL.md 执行时路由到不存在的 skill、读不到移交工件 | 同 S1 一并回填；补「移交字段名一致」断言测试 |
| S3 | **`validation_status` 枚举三处分叉，唯一门控 oracle 在真实态崩溃** | `schema.py:72`=`{open,testing,validated,falsified,superseded}`；`ledger-schema.md:53`=`{untested,testing,supported,falsified,inconclusive}`；真实 `ledger.yaml` 24 条全是 `untested` | `bw.validate.validate_all('.')` 加载真实状态即抛 `ValueError`，所有机械化门控保证（Achilles L4/F-P-E-T/引用完整性）只在 fixture 上跑过，从不在真项目上跑 | 统一枚举（建议用文档的 `untested/testing/supported/falsified`），三处对齐；加「加载真实 ledger 不崩」回归测试 |
| S4 | **L4+ 硬门控纯纸面，从未被机械化强制** | `gate_scan.py` 完全不引用 `L4`/`evidence_level`/`l4_obligation`；`schema.py:184` 暴露 `l4_obligation_open` 但无人消费它阻断 Go；`schema.py:187` 的 L4 断言只在 `validation_status==validated` 时触发，而真实态全是 `untested`，永不触发 | CLAUDE.md 反复强调的「L4+ behavioral evidence is a hard gate criterion」「L1-L3 self-report + human insistence ≠ Go」实际无法生效——缺 L4 的 Achilles 也能过 G2 | 在 `gate_scan` 加阻断性准则：任何 `l4_obligation_open==True` 的 Achilles → 禁止 Go，只发 `methodology_deviation`；加 eval 断言 |
| S5 | **F/P/E/T 签署检查过脆，产生假阴性** | `gate_scan.py:124` 只接受字面串 `"F/P/E/T"`；写成 4 条独立 signoff 或 `"... signed"` 都判失败 | 合法洞察工件被错判缺签，阻塞 Go、逼人手工覆盖 | 抽 `has_fpet_signoff()` 辅助函数，接受全匹配/4 条独立/结构化 dict，gate 与 validator 共用 |

---

## 主要（设计 / 覆盖缺口）

| # | 问题 | 证据 | 建议 |
|---|---|---|---|
| M1 | **执行段全缺且未诚实标注 scope** | 无 `bw-design`/`bw-build`/`bw-launch`/`bw-grow`/G3/G4；`gate-criteria.md` 只覆盖 G1/G2；CLAUDE.md 路由表止于「G2→handoff」但未声明后半有意排除 | 若有意只做决策段：CLAUDE.md 显式写「本工具包仅覆盖决策段（Immersion→G2），执行段交下游交付系统」；否则列路线图 |
| M2 | **Discover 缺整套田野方法包，且把访谈缺失当非阻塞** | `bw-discovery-research` 只跑桌面研究；`research-toolkit.csv` 9 法全是二手/访谈/问卷；无 AEIOU/沉浸/极端用户/投射/资源流（§5.1.1(b)）。skill 自述「研究不等待缺失的访谈」——与方法论「真人访谈是人的不可让渡动作」矛盾 | 要么工具包补田野方法 + 人工主导共情步骤；要么诚实把 capability 限定为「二手/桌面研究」，一手田野标注为 out-of-band 人工输入工件 |
| M3 | **eval 真实结果几乎全 `needs-review`，门控准则无机械化断言** | 47 个真结果 25 个 needs-review / 22 解析差异，**0 个 green**；`oracle_validate_ok` 检查存在但 **0 个场景使用**；90 个场景仅 2 个带结构化 `checks:` | 给每个 gate/capability 场景加机器可验证 checks（工件写入模式 + `transcript_regex_absent` 捕捉 gate 说「Go」/「Kill」+ gate 的 `oracle_validate_ok`） |
| M4 | **最新两个能力 skill 无 eval 场景** | `bw-concept-development`、`bw-concept-seed` 在 eval 表里是 0 场景——恰是 2026-08-09 重构新引入的两个 | 补 eval 场景，接回回归网 |
| M5 | **概念收敛「≥2 健康焦虑」只显示不强制** | `concept-development` 仅在批处理视图列显示；`gate-criteria.md` 列为定性属性；无任何 Ideate→Shape 路由阻塞 | 健康焦虑属不可让渡的人判断（§8.2），AI 不能判——但路由器可：人按概念记录的 `healthy_anxiety` 计数 <2 时软阻断，需人显式覆盖 |
| M6 | **`bw-backtrack` 角色分类错** | CLAUDE.md 路由表把 backtrack 与 router 并列；但它预分配 id、写 BT-record + action plan（`SKILL.md:8` 自述「capability」） | 从 router 行移出，单列「恢复能力」角色；注明所有 router 只读 |
| M7 | **backup 文件进 git** | `git ls-files` 仍有 6 个 `_bewater/.backup-*` 被追踪；`.gitignore` 未排除 `.backup-*`/`.bw-lock`/`.tmp-*` | 加进 `.gitignore`，`git rm --cached` 清已追踪备份；考虑加 >7d 过期清理 |
| M8 | **bwkit 锁抢占有 TOCTOU 竞争** | `cas.py:46-53` 「读判定 stale→replace」之间有窗口，两进程可同时自认持锁 | 改 `fcntl.flock`（进程死自动释放），或抢占后重读确认自己是持锁者，否则重试 |
| M9 | **bwkit `keep_backups=0` 反而保留全部备份** | `cas.py:150` `backups[:-0]`==`backups[:0]`==空 | `extras = backups if keep_backups==0 else backups[:-keep_backups]` |
| M10 | **`acquire_lock` 有副作用：无条件 `mkdir _bewater`** | `cas.py:40-41` | 缺 `_bewater/` 应抛 `LockError`，引导只由 `bwkit init` 做 |

---

## 次要（清理 / 一致性）

- **dead state**：`Ledger.next_id` 写而不读（`ledger_ops.py` 用 `_max_suffix` 重算）；`Assumption.affects` 全项目省略，下游追踪实际只走反向 `derived_from`——两个都是陷阱字段，建议删。
- **baseline 最新启发式对多位数 gate 错**：`ledger_ops.py:258` 按文件名字典序取最后，`G1<G10<G2`。按 gate 数值或 mtime 排。
- **`validate_all` 循环检测 O(N²)**：每节点调一次 `trace`，改单次染色 DFS 降到 O(V+E)。
- **`action-plan.md` 在两个 gate 重复且未抽到 `_bw-shared/`**：把 `bwkit plan apply` 机制抽成 `gate-action-application.md`，gate 各自只留载荷差异。
- **router 选择 UX 约定不一致**：6 个 router 里只有 bw-discover 命名 `AskUserQuestion`+fallback，其余只说「呈现选择」。把约定提到 `_bw-shared/router-selection.md`。
- **`EXP-NNN` 版本模型在 `ledger-schema.md` 未文档化**（append-only chain + `experiment:EXP-001@n` 引用）。
- **bewater 大小写不一致**：5 处 frontmatter 写 `bewater`，其余 17 处 `BeWater`。
- **`bw-immersion/SKILL.md:47-49` 有冗余病句**（「从不改变阶段；换句话说，它从不改变阶段」）。
- **stdin JSON 解析错误未捕获**：`check`/`scan`/`plan` 收到坏 JSON 直接抛栈，应返回 exit 1 + 清晰错误。
- **`conditions.yaml` 模式完整但全项目空跑**：无真实/eval 项目实践过 conditional-go 条件追踪，模式可能潜在有缺陷。
- **`read_revision` 接受 `revision: 0`** 但 `init._valid_state_file` 拒绝——两处正则不一致。
- **`io.read_artifact` 缺结束 fence 抛晦涩 `substring not found`**：改 `text.find` + 自描述错误。
- **`lineage.transitive_dependents` 对缺 key 的边抛未捕获 `KeyError`**：跳过格式错误的边或抛带索引的清晰错误。

---

## 方法论本身可商榷 3 点

1. **概念生命周期对「最小化」原则是张力**。`concept-lifecycle.md` + 8 字段卡 + 7 硬标准 + 软标准 + 有界修订(2 次)+ recycle-to-OA + 三去向，是全工具包最重的契约。对真实小团队（§11 一页纸流程）门槛偏高。建议保留这套为「正式模式」，另给一个「轻量模式」退化路径，与方法论 FAQ Q3「小团队跑得起」呼应。
2. **L4+ 在 G2 的刚性**：现实里许多内部/企业场景确实只能拿到 L3 问卷证据。方法论已用 `Conditional Go` 缓冲（未闭环 condition 阻塞下一门），设计是对的——但建议在 §6.1 显式写「L3 可走 Conditional Go，不可走 Go」，避免读者把 L4 理解为「做不到就卡死」。
3. **两世界理论（Creation/Operational）漂亮但工具未体现**：§2.6/§10.1 强调「开会前先声明在哪个世界」，但工具链没有 mode 标记。可考虑在 stage/state 挂 `world: creation|operational` 字段，让 Build/Launch 期越界改战略时自动提示大循环。

---

## 建议修复顺序

| 优先级 | 动作 | 工作量 |
|---|---|---|
| **P0（半天）** | S1+S2 回填 concept 重构到 src 并提交；S3 统一 `validation_status` 枚举；M7 `.gitignore` 排除 backup + 清已追踪 | 小，纯对齐 |
| **P1（1-2 天）** | S4 L4 硬门控机械化 + eval 断言；S5 F/P/E/T 辅助函数；M4 两个 concept skill 补 eval | 中，含测试 |
| **P2** | M1 scope 诚实声明；M2 Discover 田野方法标注/补全；M5 健康焦虑路由软阻断；M6 backtrack 角色纠偏 | 中 |
| **P3** | M8/M9/M10 bwkit 锁与 backup 修复；次要清理批量 | 中 |

---

## 评审方法说明

- 4 路并行子代理：bwkit 实现质量 / skill 架构一致性 / 方法论→skill 忠实度 / 状态层与 eval 体系。
- 每条 Critical/Major 发现均经人工二次验证（`diff`、`grep`、读源码），证据栏的文件/行号已核对。
- 方法论侧（`bewater-core.md`）的术语、五性、双面、门治理、人机分工理论设计未发现硬伤；问题一律在实现层。

---

*本报告为评审记录，未含可执行步骤。修复实施须基于 P0→P3 顺序另起 TDD 计划。*
