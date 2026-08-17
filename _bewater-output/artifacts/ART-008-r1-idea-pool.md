---
schema_version: 1
input_snapshot:
  strategy_ref: artifact:ART-006@2
  opportunity_ref: artifact:ART-007@1
opportunity_areas:
- opportunity_area_id: OA-001
  seeds:
  - id: CS-001
    idea: 30 分钟日更会话——每晚固定 30 分钟"选择会话"，AI 在会话外做完全部预处理，老板在会话内只做选择与拍板
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: cl-1
    strategy_filter: pass
  - id: CS-002
    idea: 天级回报信号仪表盘——当日曝光/点赞/私域进线天级回流，把"200-300 条后的爆发"变成"每天看到信号"
    source_insight_refs:
    - insight:ART-004@2:I
    - insight:ART-004@2:III
    cluster_id: cl-2
    strategy_filter: pass
  - id: CS-003
    idea: 断更预警与救援——连续 N 天未进入会话时主动干预（提醒/降载/代拟），把断更从事后悔恨变成事前拦截
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: cl-4
    strategy_filter: pass
  - id: CS-004
    idea: 产出节奏计价——按产出单位（条/周）而非素材时长计价，反向设计惩罚轻度使用=惩罚坚持的工具锚逻辑
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: null
    strategy_filter: pass
  - id: CS-005
    idea: 坚持契约与进度可视化——日更 streak、里程碑可视化，把坚持变成可感知、可展示的进度资产
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: cl-3
    strategy_filter: pass
  - id: CS-006
    idea: 会话外 AI 预处理管线——选题池/文案稿/粗剪全部在会话外生成，会话内零创作负担（不推高决策频率与决策量）
    source_insight_refs:
    - insight:ART-004@2:I
    - insight:ART-004@2:III
    cluster_id: cl-1
    strategy_filter: pass
  - id: CS-007
    idea: 轻载日模式——状态差的日子提供 10 分钟"最低可持续日"模板，让坚持不因状态波动中断
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: null
    strategy_filter: pass
  - id: CS-008
    idea: 回报信号解释器——把天级数据转译成"明天该调什么"的一句话建议，完成信号→行动闭环
    source_insight_refs:
    - insight:ART-004@2:I
    - insight:ART-004@2:III
    cluster_id: cl-2
    strategy_filter: pass
  - id: CS-009
    idea: 断更数据追溯——用账号历史断更模式校准提醒时机（越用越准的坚持层，I3 数据闭环在坚持维度的应用）
    source_insight_refs:
    - insight:ART-004@2:III
    cluster_id: cl-4
    strategy_filter: pass
  - id: CS-010
    idea: 家庭/团队监督侧——让老板的拍档或团队看到坚持进度，把外部责任变成坚持装置的一部分
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: null
    strategy_filter: partial
  - id: CS-011
    idea: 复利叙事——把"第 100 条 vs 第 300 条"的资产累积可视化为坚持回报，对抗延迟正反馈
    source_insight_refs:
    - insight:ART-004@2:I
    cluster_id: cl-3
    strategy_filter: pass
  shortlist:
    recommended:
    - CS-009
    - CS-011
    confirmed: []
- opportunity_area_id: OA-002
  seeds:
  - id: CS-012
    idea: 社交推荐选题引擎——按"值得点赞/转发"而非完播率选题：选题评分含转发语境与点赞理由
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: cl-7
    strategy_filter: pass
  - id: CS-013
    idea: 转发语境设计——每条内容内置"一个具体的人转发给另一个具体的人"的语境（谁会给谁转、为什么转）
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: null
    strategy_filter: pass
  - id: CS-014
    idea: 私域钩子工作台——内容尾部私域进线设计（好友申请理由、进线路径），私域约 1:1 撬公域推流
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: null
    strategy_filter: pass
  - id: CS-015
    idea: 真人出镜合规工作流——AI 标识内建、数字人规避、人点发布，政策圈出的结构性位置的产品化
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: cl-5
    strategy_filter: pass
  - id: CS-016
    idea: 结构变体 A/B——同一选题多结构变体（钩子/顺序）并行发布，回流命中率调优
    source_insight_refs:
    - insight:ART-004@2:II
    - insight:ART-004@2:III
    cluster_id: null
    strategy_filter: pass
  - id: CS-017
    idea: 视频号生态监控——kill signal 半触发监控（字节系能力/平台策略变化），平台押注的风险对冲仪表
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: cl-6
    strategy_filter: partial
  - id: CS-018
    idea: 社交货币钩子库——按行业/人群的"值得转发"钩子模板（点赞理由分类），内容资产的视频号特化
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: cl-7
    strategy_filter: pass
  - id: CS-019
    idea: 关系链冷启动——老板微信关系链的"首 100 次转发"设计，私域导入公域的启动机制
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: null
    strategy_filter: pass
  - id: CS-020
    idea: 平台原生素材适配——视频号竖屏/沉浸/评论互动原生设计，不为抖音逻辑迁就
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: null
    strategy_filter: partial
  - id: CS-021
    idea: 合规发布审批流——半自动生成+人点发布的人审环节（AI 标识 + 发布前人工确认）
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: cl-5
    strategy_filter: pass
  - id: CS-022
    idea: 政策变动预警——官方政策文本监控，AI 标识/数字人规则变化即时预警
    source_insight_refs:
    - insight:ART-004@2:II
    cluster_id: cl-6
    strategy_filter: partial
  shortlist:
    recommended:
    - CS-021
    - CS-022
    confirmed: []
- opportunity_area_id: OA-003
  seeds:
  - id: CS-023
    idea: 透明工作台——选题→文案→剪辑→发布全流程每步可见可改，不再是黑箱
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: cl-9
    strategy_filter: pass
  - id: CS-024
    idea: 效果归因面板——每条内容的流量结果归因到具体决策（选题/结构/发布时间），效果归因可见
    source_insight_refs:
    - insight:ART-004@2:IV
    - insight:ART-004@2:III
    cluster_id: cl-8
    strategy_filter: pass
  - id: CS-025
    idea: 服务替代订阅定价——¥3000+/月档订阅（对标全案 ¥1.5万/月 的分数价），服务替代锚定价
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: null
    strategy_filter: pass
  - id: CS-026
    idea: 方向盘产品化——每步"人做选择"的拍板界面：老板握方向盘、AI 只提供备选
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: null
    strategy_filter: pass
  - id: CS-027
    idea: 陪跑迁移包——从代运营/陪跑迁移的导入流程（账号/数据/期望管理），承接信任崩塌后的存量需求
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: null
    strategy_filter: pass
  - id: CS-028
    idea: 信任型 onboarding——前 30 天"结果基线"：先展示方法论外部基线（K-006）再承诺，付费前先给确定性
    source_insight_refs:
    - insight:ART-004@2:IV
    - insight:ART-004@2:III
    cluster_id: null
    strategy_filter: pass
  - id: CS-029
    idea: 月成本透明账单——单条成本 ¥1-10、月成本 ¥30-300 的可视化账单，成本余量支撑透明承诺
    source_insight_refs:
    - insight:ART-004@2:III
    - insight:ART-004@2:IV
    cluster_id: null
    strategy_filter: pass
  - id: CS-030
    idea: 效果周报（老板视角）——每周一页的结果归因+下周建议，把"服务感"产品化
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: cl-8
    strategy_filter: pass
  - id: CS-031
    idea: 全案对比工具——与代运营全案（¥1.5万/月）的 ROI 对比器，服务替代定价的叙事武器
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: null
    strategy_filter: pass
  - id: CS-032
    idea: 退款承诺机制——有条件结果承诺/退款条款设计，信任重建的硬机制（注意与"不承诺流量"张力的边界）
    source_insight_refs:
    - insight:ART-004@2:IV
    cluster_id: null
    strategy_filter: partial
  - id: CS-033
    idea: 决策留痕——每次选择会话的决策记录可回放（我做过什么选择→结果如何），控制感的长期资产
    source_insight_refs:
    - insight:ART-004@2:IV
    - insight:ART-004@2:III
    cluster_id: cl-9
    strategy_filter: pass
  shortlist:
    recommended:
    - CS-030
    confirmed: []
decisions: []
hash: e26a4cf19feb02c29d803a5e6faa271787406068800d260833df30d9241f4b5f
artifact_id: ART-008
kind: idea-pool
stage: ideate
revision: 1
document_status: draft
validation_status: unvalidated
branch_id: BR-001
locked: false
signoffs: []
derived_from:
- artifact:ART-007@1
last_validated_against: []
---

# Idea Pool r1 · 创始人 IP 短视频放大器

分支全局唯一 Idea Pool。输入快照：战略 `artifact:ART-006@2`（复合刀）· 机会组合 `artifact:ART-007@1`（OA-001..003）。33 条种子（每 OA 11 条 ≥ 10 硬下限），`CS-001..CS-033` 池级唯一，跨修订永不重号。

**战略过滤器（复合刀）**：视频号 × 每天 30 分钟真人选择会话 × 服务替代定价——凡不服务于『坚持』与『方向盘在老板手里』的功能一律不做。

## OA-001 坚持装置 · 断更解药（11 条种子）

| ID | 种子 | 来源 | 簇 | 过滤器 |
|---|---|---|---|---|
| CS-001 | 30 分钟日更会话（会话内只选择） | I | cl-1 | pass |
| CS-002 | 天级回报信号仪表盘 | I, III | cl-2 | pass |
| CS-003 | 断更预警与救援 | I | cl-4 | pass |
| CS-004 | 产出节奏计价 | I | – | pass |
| CS-005 | 坚持契约与进度可视化 | I | cl-3 | pass |
| CS-006 | 会话外 AI 预处理管线 | I, III | cl-1 | pass |
| CS-007 | 轻载日模式（10 分钟最低可持续日） | I | – | pass |
| CS-008 | 回报信号解释器 | I, III | cl-2 | pass |
| CS-009 | 断更数据追溯 | III | cl-4 | pass |
| CS-010 | 家庭/团队监督侧 | I | – | partial |
| CS-011 | 复利叙事 | I | cl-3 | pass |

**短名单建议（elimination，默认保留）**：
- 砍 **CS-009**（cl-4 与 CS-003 近重复——数据追溯是预警的校准机制，并入 CS-003）
- 砍 **CS-011**（cl-3 与 CS-005 近重复——且复利叙事依赖延迟正反馈叙事，正是战略要对抗的）
- 保留 9 条；CS-010 标 partial（外部监督改变单人产品形态），按"拿不准就保留"不砍

## OA-002 视频号原生内容 · 为关系链而发（11 条种子）

| ID | 种子 | 来源 | 簇 | 过滤器 |
|---|---|---|---|---|
| CS-012 | 社交推荐选题引擎 | II | cl-7 | pass |
| CS-013 | 转发语境设计 | II | – | pass |
| CS-014 | 私域钩子工作台 | II | – | pass |
| CS-015 | 真人出镜合规工作流 | II | cl-5 | pass |
| CS-016 | 结构变体 A/B | II, III | – | pass |
| CS-017 | 视频号生态监控 | II | cl-6 | partial |
| CS-018 | 社交货币钩子库 | II | cl-7 | pass |
| CS-019 | 关系链冷启动 | II | – | pass |
| CS-020 | 平台原生素材适配 | II | – | partial |
| CS-021 | 合规发布审批流 | II | cl-5 | pass |
| CS-022 | 政策变动预警 | II | cl-6 | partial |

**短名单建议（elimination，默认保留）**：
- 砍 **CS-021**（cl-5 与 CS-015 近重复——发布审批是合规工作流的一环）
- 砍 **CS-022**（cl-6 与 CS-017 近重复——政策预警并入生态监控）
- 保留 9 条；CS-017/CS-022 标 partial（风险对冲配套而非功能），CS-020 标 partial（设计原则性强、独立概念弱）

## OA-003 结果可控 · 服务替代（11 条种子）

| ID | 种子 | 来源 | 簇 | 过滤器 |
|---|---|---|---|---|
| CS-023 | 透明工作台 | IV | cl-9 | pass |
| CS-024 | 效果归因面板 | IV, III | cl-8 | pass |
| CS-025 | 服务替代订阅定价 | IV | – | pass |
| CS-026 | 方向盘产品化 | IV | – | pass |
| CS-027 | 陪跑迁移包 | IV | – | pass |
| CS-028 | 信任型 onboarding | IV, III | – | pass |
| CS-029 | 月成本透明账单 | III, IV | – | pass |
| CS-030 | 效果周报 | IV | cl-8 | pass |
| CS-031 | 全案对比工具 | IV | – | pass |
| CS-032 | 退款承诺机制 | IV | – | partial |
| CS-033 | 决策留痕 | IV, III | cl-9 | pass |

**短名单建议（elimination，默认保留）**：
- 砍 **CS-030**（cl-8 与 CS-024 近重复——周报是归因面板的呈现形态）
- 保留 10 条；CS-032 标 partial（退款承诺与 Charter"不承诺流量"的张力边界需人工裁决）

## 短名单汇总（AI 推荐，等人工确认）

| OA | 种子数 | 推荐砍 | 建议确认 |
|---|---|---|---|
| OA-001 | 11 | CS-009, CS-011 | CS-001..008, CS-010（9 条） |
| OA-002 | 11 | CS-021, CS-022 | CS-012..020（9 条） |
| OA-003 | 11 | CS-030 | CS-023..029, CS-031..033（10 条） |

确认原则：拿不准就保留，只砍明确死项/近重复/偏离战略；`decisions[]` 保持为空直到人工确认（本修订仅记录 AI 推荐，不代填 `shortlist.confirmed`）。确认后每条保留种子全部进入 bw-concept-development 的概念发展（无草稿中间层）。
