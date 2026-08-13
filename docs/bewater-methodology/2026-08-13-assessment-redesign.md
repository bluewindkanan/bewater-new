# BeWater Initial Assessment 重设计计划

**日期**：2026-08-13
**范围**：`initial-assessment-template.md` + `bw-immersion/SKILL.md` 判断契约（纯方法论文档改动，无代码）
**方法**：基于外部调研证据的契约调整；回归靠 eval 断言核查（无 TDD 对象，断言语义不变）

---

## 背景与设计依据

用户提出的 Assessment 定位假设（经确认）：
- 核心 = 让用户快速获得初步判断 + 抓住用户；是**快速直觉判断**，不是深度评估报告
- 来源数量（3 vs 5）无意义
- **最核心产出 = Inspect Next**（传给下游做 research 的信号）

网络调研 6 组，4 类相似产品，三条证据结论：

| 结论 | 证据 | 对本设计的含义 |
|---|---|---|
| "具体下一步"是工具分水岭 | AI 验证工具批判共识：可执行行动清单 = horoscope→diagnosis 的区别；好工具赢在下一步而非分数 | Inspect Next 应升格为 core deliverable，且每条必须可执行 |
| 初筛 = 过滤器，不是判决 | 天使投资人 first-pass 分桶（Advance/Monitor/Pass）；Stage-Gate Gate 1 金融指标故意不进第一屏 | Assessment"非 Gate、无 score"定位正确，不动 |
| 数量无用，纪律有用 | 商业验证工具死于 feel-good scoring（每个想法 90 分、无来源归因、"reflect the internet, not customers"） | 来源**数量**不设目标，但**归因/权威纪律 + 消证信号**是反谄媚护栏，必须保留 |

两个直接可借鉴：
- **Pre-mortem**（Klein 实证）：前瞻性后见比"什么会出问题"多识别 ~30% 失败原因
- **Stage-Gate must-meet**：一票否决式淘汰条件，给"快速判断"一个明确边界

## 设计决策

**总则**：把"初步判断"从一段描述变成**带校准边界的快判断**；锋利点从风险罗列移到**可执行的下一步清单**；反谄媚护栏（5 标签溯源、零来源不产、隔离墙、非 Gate）全部不动。

5 处改动（A–E）+ 明确不改什么（§"不改变项"）。

---

## 改动任务

### T1: 模板 §3 Material Risks → Pre-mortem 框架

**位置**：`src/skills/bw-immersion/references/initial-assessment-template.md` §3（L61-64）

**现状**：
```
List at most three risks. For each, include a disconfirming signal under **What would change this
view**. Preserve material Charter Unknowns and distinguish them from externally surfaced risks.
```

**改成**：
```
### 3. Material Risks & Unknowns (pre-mortem)

Assume the direction proved fruitless within ~90 days of exploration, then state the most likely
reasons — prospective hindsight surfaces ~30% more failure causes than "what could go wrong"
(Klein). List at most three, ranked by how quickly a disconfirming signal could settle each. For
each, state the concrete observation under **What would change this view** that would prove the
risk wrong. Preserve material Charter Unknowns and distinguish them from externally surfaced
risks.
```

**验证**：§3 仍至多 3 风险、仍带消证信号；§1-5 五个 heading 结构不变。

**工作量**：0.25 小时

---

### T2: 模板 §1 结论 → 方向级 kill signal

**位置**：模板 §1（L49-53）

**现状**：
```
### 1. Overall Preliminary Conclusion

- One-sentence preliminary judgment.
- Why the space is worth further exploration.
- The largest unknown.
```

**改成**：
```
### 1. Overall Preliminary Conclusion

- One-sentence calibrated preliminary judgment that names what would flip it, not a generic
  "worth exploring".
- Why the space is worth further exploration.
- The largest unknown.
- **Direction-level kill signal:** the single external observation whose appearance flips the
  conclusion to "not worth exploring". Pre-registered knockout criterion (Stage-Gate must-meet
  logic); not a Gate decision and no score.
```

**验证**：结论可被单个观察翻转（校准边界）；非 Gate 语义保留。

**工作量**：0.25 小时

---

### T3: 模板 §4 Inspect Next → core deliverable + 可执行标准

**位置**：模板 §4（L66-69）

**现状**：
```
### 4. What to Inspect Next

Give the user a short inspection checklist grounded in the Charter and external reality check. Do
not turn it into a Research Design, Discover Mission, priority direction, or downstream handoff.
```

**改成**：
```
### 4. What to Inspect Next (core deliverable)

This checklist is the report's core output — a verdict becomes useful only through its next
action. Give a short inspection checklist grounded in the Charter and external reality check;
each item must be specific enough to act on: what to observe, whom to ask, how many cases, over
what period. Do not turn it into a Research Design, Discover Mission, priority direction, or
downstream handoff. Discover may reuse each item only as a candidate seed question with
independent source verification.
```

**验证**：隔离墙措辞保留（candidate seed + independent verification）；可执行性标准新增。

**工作量**：0.25 小时

---

### T4: 模板 §5 来源 → 数量不设目标

**位置**：模板 §5（L74-75）

**现状**：
```
Charter basis, External signal, and Assessment inference. List the 1–5 sources actually used with
exact title, publisher, date when available, and exact retrieved URL.
```

**改成**：
```
Charter basis, External signal, and Assessment inference. List only the sources actually used,
each with exact title, publisher, date when available, and exact retrieved URL. The count is not
a target: fewer well-attributed sources beat padded ones, and a visibly source-sparse report is
preferred to a padded one. Every External signal must resolve to a listed source; anything
unsourced is labeled **Assessment inference**.
```

**验证**：`1–5` 数量约束移除；归因纪律 + sparse 诚实标签保留。

**工作量**：0.25 小时

---

### T5: SKILL.md 同步（与 T4 成对，避免模板/技能矛盾）

**位置**：`src/skills/bw-immersion/SKILL.md`（L147-156 外部研究 + L164-168 pre-write audit）

**现状 L147-156**：
```
Search for 3–5 credible public sources, preferring primary research, ...
Source availability controls the outcome: 3–5 credible sources yield the normal report; 1–2 yield
a visibly source-sparse report narrowing every conclusion; zero credible sources, an unavailable
search tool, or a failed search produce no Assessment — preserve the Charter and report a
concrete retry reason.
```

**改成 L147-156**：固定数量目标去掉，保留 sparse/zero 行为：
```
Search for credible public sources — primary research, official data, regulatory material, and
authoritative industry sources — with no fixed count target. Preserve exact source titles and
URLs returned by the research tool; never invent or repair a citation. ... Source availability
controls the outcome: sufficient credible sources yield the normal report; only 1–2 yield a
visibly source-sparse report narrowing every conclusion; zero credible sources, an unavailable
search tool, or a failed search produce no Assessment — preserve the Charter and report a
concrete retry reason.
```

**现状 L164-168（pre-write audit）**：
```
...a compact five-label trace for every key judgment, at most three risks each with a
disconfirming signal, and an explicit research boundary with only the sources actually retrieved.
```

**改成**：
```
...a compact five-label trace for every key judgment, a direction-level kill signal in the
conclusion, at most three pre-mortem risks each with a disconfirming signal, an inspect-next
checklist whose items are actionable, and an explicit research boundary with only the sources
actually retrieved.
```

**验证**：SKILL.md 与模板措辞一致；`grep -n "3–5"` SKILL.md 应无残留（Assessment 段）。

**工作量**：0.5 小时

---

## 不改变项（反谄媚护栏）

网络证据最强警告：商业验证工具死于"快 + 抓用户 + 浅"。以下全部保留，不因本计划触碰：

- ✅ 5 标签溯源（Charter basis → External signal → Assessment inference → Implication → What would change this view）
- ✅ 零来源 / 搜索工具不可用 → 不产 Assessment、不 fabricate、报 retry 原因
- ✅ 隔离墙：Inspect Next 只作候选种子问题（独立源验证后提升）；Material Risks 与判断不流入 Research
- ✅ 非 Gate、无 score、无 readiness 标签；不改 Charter/assumption/current_stage/Evidence
- ✅ 60-second read / 1–2 屏 / 600–900 词硬上限
- ✅ 5 个 heading 结构不变

## 执行顺序

```
T1 → T2 → T3 → T4 → T5 → [提交]
```

单文件模板编辑（T1-T4 同文件顺序改）+ SKILL.md（T5），共 2 文件，无需 Agent 协作。

## 回归门

```bash
# 1. 结构与措辞核查
grep -n "3–5" src/skills/bw-immersion/SKILL.md          # Assessment 段应无残留
grep -c "^### " src/skills/bw-immersion/references/initial-assessment-template.md   # 仍为 5 个 heading

# 2. eval 断言语义核查（不改场景，确认仍成立）
# BWIAS-S2 zero-sources : 不产 Assessment、不 fabricate        → 新规则下成立
# BWIAS-S3 sparse-sources : 收窄结论、标局限、不 padding        → 新规则下成立（1-2 来源仍 sparse）
# BWIAS-S7 reassess : fresh research、同 ID、derived_from 精确 → 不受影响

# 3. 全量测试（无代码改动，应全过）
python -m pytest tests/ -x -q
```

**总工作量**：1.5 小时
