---
schema_version: 1
source_concepts:
  portfolio_ref: artifact:ART-009@2
  concept_ids:
  - CI-001
  - CI-010
  - CI-019
  - CI-021
  path: hybridize
definition:
  name: 视频号创始人IP日更放大器
  pithy_proposition: 每天 30 分钟，自己握方向盘的视频号日更，回报信号以天计
  what_it_is: 一个把『坚持』做成产品的订阅工作台：AI 在会话外备好选题/文案/粗剪（转发值选题引擎供候选并评分排序），老板每晚固定 30 分钟只做选择与拍板（人点发布、AI
    标识内建），全流程每步可见可改可回滚（透明工作台），次日清晨收到天级战报与明日建议；按服务替代锚定价（¥3000+/月档，按条/周产出计价）
  who_its_for: 粗糙自干派中小企业老板（视频号×真人 IP）：时间破产（单条 3-8 小时、等不起 200-300 条）、已为 IP 结果持续付费、被代运营/陪跑黑箱交付伤过、拒绝全托管但不愿从零创作
  dual_sided:
    money:
      commercial_value_proposition: 服务替代锚订阅（¥3000+/月，对标全案 ¥1.5万/月分数档），单条边际成本 ¥1-10，毛利结构支撑独立
        SaaS
      leverageable_assets: 方法论×私有数据闭环（转发值评分、归因、留痕）越用越准不可迁移；平台政策壁垒的产品化入口
    magic:
      consumer_value_proposition: 每天 30 分钟维持日更、回报信号以天计、方向盘在自己手里——把『等不起』变成『每天看到信号』
      consumer_target: 粗糙自干派、时间破产、被黑箱交付伤过但持续为结果付费的中小企业老板
    tension: 窄而深（坚持装置+服务替代）与获客规模天然冲突；不承诺流量与续费依赖流量结果并存
    balance_choice: Magic 侧——先证明坚持装置与转发命中，定价强度随后
  dimensions:
    path_to_market: 迁移包承接『被代运营/陪跑伤过但不敢裸退』的存量老板（K-005 三层价位带上层）——低 CAC 进入机制；信任型 onboarding（外部基线
      K-006 先行）降低『再赌一次』恐惧；全案对比工具作为临门说服
    right_to_win: 平台博弈空位（insight II：视频号×真人×copilot 大厂进不来）+ 方法论×私有数据闭环（insight III）+
      信任缺口上的服务替代形态（insight IV）三重复合——占住没有大厂工具的位置
    product_or_service_platform: 订阅制 SaaS 工作台（会话容器 + 内容引擎 + 透明流水线），服务替代形态而非工具
    source_of_business: 订阅续费（坚持装置成立=续费成立）；进线量/转发命中作为『内容带来客户』的商业信号
    product_or_service_design: 30 分钟硬上限的拍板仪式为核心容器；会话外全预处理；透明流水线可改可回滚；AI 只备选、人拍板
    enabling_technology: AI 文本/剪辑预处理管线 + 账号私有数据回流（转发值评分、归因引擎、天级战报）+ 合规发布闸口（AI 标识内建、人点发布）
    reason_to_believe: K-004（时间破产基线）、K-005（三层价位带+陪跑信任崩塌）、K-006（方法论外部基线）、K-007（单条成本
      ¥1-10）——外部证据锚点齐全；作者本人 dogfood 可作首条 L4 行为证据
    branding: 『坚持装置』叙事（反效率竞赛）+ 『方向盘在你手里』（反全托管）+ 『服务替代』（反黑箱）——三种叙事指向同一形态
    consumer_experience: 每晚 21:00 的 30 分钟仪式：3-5 个带理由的选题 → 拍板 → 确认发布 → 次日清晨战报；每步可见可改；断更时被救援而非被责备
how_it_works:
- step: 1
  action: 会话外备料：AI 消费账号私有数据（历史命中率、行业、日历）生成选题池（转发值评分排序）+ 文案稿 + 粗剪
  consumer_benefit: 打开会话即有 3-5 个带『谁会转给谁、为什么』理由的候选，零创作负担
  operational_benefit: 单条人工耗时从 3-8 小时压向 30 分钟以内；预处理在会话外异步完成
  strategic_rationale: 私有数据闭环入口——候选越贴账号越用越准，切换成本累积
  legal_regulatory_rationale: AI 生成内容标识在生成环节自动附加（K-003 合规要求）
  evidence_refs:
  - knowledge:K-004@1
  - knowledge:K-007@1
  - assumption:A-010@2
  - assumption:A-019@2
  design_refs:
  - artifact:ART-009@2#CI-001
  - artifact:ART-009@2#CI-010
  - artifact:ART-009@2#CI-006
- step: 2
  action: 30 分钟选择会话：固定时段的拍板仪式（选选题→微调文案→确认发布），倒计时硬约束，超时自动收束
  consumer_benefit: 方向盘在自己手里：每关键步老板拍板、AI 只给备选与理由；每天只付 30 分钟
  operational_benefit: 会话节律产生每日行为数据（决策留痕），坚持与否被量化
  strategic_rationale: 『坚持成立=续费成立』的因果链在每次会话中被验证——产品只卖坚持本身
  legal_regulatory_rationale: 人点发布闸口不可绕过（无发布 API 下的合规半自动）
  evidence_refs:
  - assumption:A-010@2
  - assumption:A-031@2
  design_refs:
  - artifact:ART-009@2#CI-001
  - artifact:ART-009@2#CI-022
- step: 3
  action: 透明工作台：五段流水线（选题→文案→剪辑→发布→数据）每步产物可见可改可回滚，效果归因到具体决策
  consumer_benefit: 看得见自己买的内容生产线——黑箱被移除，信任重建
  operational_benefit: 修改向后联动重算；归因口径固定可查，杜绝玄学
  strategic_rationale: 服务替代形态的第一性体验（信息差溢价被结构性移除）
  legal_regulatory_rationale: 归因与承诺不构成流量承诺（Charter 红线：不承诺流量）
  evidence_refs:
  - assumption:A-028@2
  - assumption:A-029@2
  design_refs:
  - artifact:ART-009@2#CI-019
  - artifact:ART-009@2#CI-020
- step: 4
  action: 天级战报 + 明日建议：次日清晨 3 个信号（曝光/点赞/私域进线）+ 近 7 天对比 + 一句话『明天该调什么』
  consumer_benefit: 回报信号以天计——不再赌 200-300 条后的爆发；信号直接转成明天的行动
  operational_benefit: 信号→行动闭环（建议-采纳-结果回流），内容迭代自动化
  strategic_rationale: 消灭『断更作为理性选择』的动机；建议采纳数据成为私有资产
  legal_regulatory_rationale: 建议是解释与选项而非指令，越权即产品失败
  evidence_refs:
  - assumption:A-011@2
  - assumption:A-017@2
  design_refs:
  - artifact:ART-009@2#CI-002
  - artifact:ART-009@2#CI-008
- step: 5
  action: 断更救援 + 坚持资产：缺席触发梯度救援（提醒→降载→代拟），streak/里程碑可视化
  consumer_benefit: 状态差也有 10 分钟轻载日——坚持不因状态波动中断；断更被事前拦截而非事后悔恨
  operational_benefit: 断更拦截直接保护 LTV（流失第一原因被产品化处理）
  strategic_rationale: 坚持装置必须容错；轻载/救援数据揭示个体脆弱点，越用越懂用户何时会放弃
  legal_regulatory_rationale: 救援永不自动发布——发布闸门永远是真人
  evidence_refs:
  - assumption:A-012@2
  - assumption:A-016@2
  - assumption:A-014@2
  design_refs:
  - artifact:ART-009@2#CI-003
  - artifact:ART-009@2#CI-007
  - artifact:ART-009@2#CI-005
how_to_implement:
- phase: P0 dogfood
  timing: 第 1-2 周
  objective: 作者自有 IP 跑通 30 分钟会话全流程，产出首条 L4 行为证据
  jobs_to_be_done:
  - 作者账号连续 21 天日更
  - 单条人工耗时压至 40 分钟内
  - 记录会话完成率与发布率
  capabilities_and_assets:
  - 作者自有方法论
  - 自有账号数据
  - AI 预处理管线 v0
  owner: 秋南Dylan（产品作者）
  dependencies:
  - AI 文本/剪辑管线可用
  risks:
  - dogfood 与真实用户行为偏差
  open_questions:
  - 30 分钟是否真实可维持
  pilot_and_rollout: 作者账号先行，数据作为 A-010 首条 L4 证据
- phase: P1 MVP
  timing: 第 1-2 月
  objective: 会话+战报+透明工作台 v0 上线，10-15 位种子老板（迁移包承接）
  jobs_to_be_done:
  - 30 分钟会话最小闭环
  - 天级战报
  - 透明工作台 v0
  - 迁移包 v0
  capabilities_and_assets:
  - P0 沉淀的会话模板
  - 合规发布闸口
  owner: 产品+工程（2 人）
  dependencies:
  - P0 完成
  risks:
  - 种子用户断更
  - 迁移摩擦
  open_questions:
  - 坚持率基线
  pilot_and_rollout: 种子池 30 天坚持率 ≥80% 为 P1 验收
- phase: P2 内容引擎+定价
  timing: 第 3-4 月
  objective: 转发值选题 v1 + 服务替代定价页上线，A-030/A-019 的 L4 实验启动
  jobs_to_be_done:
  - 转发值评分 v1
  - 服务替代定价页
  - 价格接受度实验（A-030）
  - 转发命中实验（A-019）
  capabilities_and_assets:
  - 账号历史数据回流
  - 定价页组件
  owner: 产品+工程+运营（3 人）
  dependencies:
  - P1 数据积累
  risks:
  - 价格接受度不达预期
  - 转发命中不可检出
  open_questions:
  - ¥3000+/月档真实转化率
  pilot_and_rollout: 付费转化 ≥25% 为 P2 验收
- phase: P3 数据闭环+实验规模化
  timing: 第 5-6 月
  objective: 归因面板、结构变体实验（承接 CI-030），15 条 Achilles 中关键 6 条 L4 结论
  jobs_to_be_done:
  - 归因面板 v1
  - 结构变体实验
  - Achilles L4 实验矩阵执行
  - 投资叙事与财务案例
  capabilities_and_assets:
  - 归因引擎
  - 实验框架
  - 数据闭环
  owner: 全员（3-4 人）
  dependencies:
  - P2 实验数据
  risks:
  - L4 样本不足
  - 归因不可信
  open_questions:
  - G2 就绪度
  pilot_and_rollout: G2 前每条 Achilles 有 L4 结论或显式例外
how_it_makes_money:
  revenue_streams:
  - 服务替代订阅 ¥3,980/月档（按产出单位条/周计价，对标全案 ¥1.5万/月分数档）
  - 进阶档（结构实验/归因深度功能，后续版本）
  pricing_and_volume_logic: 定价锚定代运营服务而非工具：¥3,980/月 ≈ 全案 26% 档位；按条/周计价使『续费=坚持』可度量；目标客群为三层价位带上层（K-005），窄而深定位下的可寻址规模受获客渠道约束（A-006）
  adoption_retention_frequency_assumptions:
  - assumption: 试用→付费转化率 ≥25%（迁移包承接存量受伤老板，自带付费预算）
    source: assumption:A-024@2（基线先行）+ K-005
  - assumption: 月续费率 ≥95%（坚持装置成立=续费成立）
    source: assumption:A-010@2 + A-002
  - assumption: 每日会话参与率 ≥80%（30 天窗口）
    source: assumption:A-010@2
  - assumption: 获客 CAC ≤ ¥3,000（窄深定位触达成本可承受）
    source: assumption:A-006
  development_and_operating_costs:
  - assumption: 单条 AI 程序化工序边际成本 ¥1-10（真人素材+文本驱动架构）
    source: knowledge:K-007@1
  - assumption: 单用户月基础设施成本 ¥30-300
    source: knowledge:K-007@1
  - assumption: 3-4 人团队年成本约 ¥80-120 万（seed 阶段）
    source: 市场基准估算
  - assumption: 迁移/合规/工具类一次性投入约 ¥30 万
    source: 估算（P1-P2 清单）
  scenarios:
    base:
      revenue: 1430
      margin: 0.7
      earnings: 300
      investment: 150
      payback: 12-18 个月
    aggressive:
      revenue: 3800
      margin: 0.75
      earnings: 1300
      investment: 300
      payback: 9 个月
  sensitivity:
  - 转化率 ±10pp → 首年营收 ±¥250 万（base 场景）
  - 月续费率 95%→90% → LTV 缩短约 30%
  - CAC ±¥1000 → 单位经济敏感性中等（客单价 ¥3980/月支撑）
  unresolved_model_gaps:
  - ¥3000+/月档真实接受度未 L4 验证（A-030）
  - 转化率/获客渠道无实测（A-006）
  - 窄深定位的 TAM 边界未量化
validation:
  consumer_desire:
    claim: 时间破产+信任缺口的老板会为『每天 30 分钟、自己握方向盘的日更能力』付费并坚持——对手是等不起不是不会剪
    evidence_refs:
    - knowledge:K-004@1
    - knowledge:K-005@1
    - artifact:ART-004@2
  commercial_value:
    claim: 服务替代锚定价（¥3000+/月）配合单条边际成本 ¥1-10 的毛利结构支撑独立 SaaS
    evidence_refs:
    - knowledge:K-005@1
    - knowledge:K-007@1
    - assumption:A-030@2
  feasibility_and_implementation:
    claim: AI 预处理+30 分钟会话+人点发布在现有技术下可交付，合规（AI 标识/真人出镜）可内建
    evidence_refs:
    - knowledge:K-007@1
    - knowledge:K-003@1
    - assumption:A-003
  achilles_assumption_refs:
  - assumption:A-019@2
  experiment_refs: []
  evidence_refs: []
  invalidated_claims: []
content_gaps:
- field_path: validation.evidence_refs
  reason: 尚无机器证据记录（_bewater/evidence.yaml 未建立）；Achilles 实验产出 L4 行为证据后由 bw-experiment
    回填
- field_path: validation.experiment_refs
  reason: Achilles L4 实验尚未设计执行；由 bw-experiment 设计并记录 EXP 后回填
applicability_exceptions: []
hash: ac2f164c7eeda9c2800965fb336e57f1998b5c7490d1c6afa7a946bab23463f8
artifact_id: ART-010
kind: solution
stage: shape
revision: 1
document_status: final
validation_status: unvalidated
branch_id: BR-001
locked: false
signoffs: []
dual_sided:
  magic:
    consumer_value_proposition:
      statement: 每天 30 分钟、自己握方向盘的视频号日更能力——回报信号以天计（不再赌 200-300 条后的爆发）
      evidence_refs:
      - artifact:ART-004@2
    consumer_target:
      statement: 粗糙自干派中小企业老板（视频号×真人 IP，时间破产但为结果持续付费、被代运营/陪跑伤过）
      evidence_refs:
      - artifact:ART-004@2
  money:
    commercial_value_proposition:
      statement: 服务替代锚订阅（对标 ¥1.5万/月全案的分数档 ¥3000+/月），单条边际成本 ¥1-10、月成本 ¥30-300，毛利结构支撑独立
        SaaS
      evidence_refs:
      - knowledge:K-005@1
      - knowledge:K-007@1
    leverageable_assets:
      statement: 作者自有方法论×账号私有数据闭环（转发值评分、归因数据、决策留痕）——越用越准、不可迁移
      evidence_refs:
      - artifact:ART-004@2
  tension:
    statement: 坚持装置价值锚（Magic）与服务替代高位定价（Money）都要求窄而深，但窄而深与获客规模天然冲突；且不承诺流量与续费依赖流量结果并存
  balance_choice: Magic 侧（先证明坚持装置与转发命中，定价强度随后）
derived_from:
- artifact:ART-009@2
last_validated_against: []
---
# 视频号创始人IP日更放大器

## Definition

```yaml
name: 视频号创始人IP日更放大器
pithy_proposition: 每天 30 分钟，自己握方向盘的视频号日更，回报信号以天计
what_it_is: 一个把『坚持』做成产品的订阅工作台：AI 在会话外备好选题/文案/粗剪（转发值选题引擎供候选并评分排序），老板每晚固定 30 分钟只做选择与拍板（人点发布、AI
  标识内建），全流程每步可见可改可回滚（透明工作台），次日清晨收到天级战报与明日建议；按服务替代锚定价（¥3000+/月档，按条/周产出计价）
who_its_for: 粗糙自干派中小企业老板（视频号×真人 IP）：时间破产（单条 3-8 小时、等不起 200-300 条）、已为 IP 结果持续付费、被代运营/陪跑黑箱交付伤过、拒绝全托管但不愿从零创作
dual_sided:
  money:
    commercial_value_proposition: 服务替代锚订阅（¥3000+/月，对标全案 ¥1.5万/月分数档），单条边际成本 ¥1-10，毛利结构支撑独立
      SaaS
    leverageable_assets: 方法论×私有数据闭环（转发值评分、归因、留痕）越用越准不可迁移；平台政策壁垒的产品化入口
  magic:
    consumer_value_proposition: 每天 30 分钟维持日更、回报信号以天计、方向盘在自己手里——把『等不起』变成『每天看到信号』
    consumer_target: 粗糙自干派、时间破产、被黑箱交付伤过但持续为结果付费的中小企业老板
  tension: 窄而深（坚持装置+服务替代）与获客规模天然冲突；不承诺流量与续费依赖流量结果并存
  balance_choice: Magic 侧——先证明坚持装置与转发命中，定价强度随后
dimensions:
  path_to_market: 迁移包承接『被代运营/陪跑伤过但不敢裸退』的存量老板（K-005 三层价位带上层）——低 CAC 进入机制；信任型 onboarding（外部基线
    K-006 先行）降低『再赌一次』恐惧；全案对比工具作为临门说服
  right_to_win: 平台博弈空位（insight II：视频号×真人×copilot 大厂进不来）+ 方法论×私有数据闭环（insight III）+
    信任缺口上的服务替代形态（insight IV）三重复合——占住没有大厂工具的位置
  product_or_service_platform: 订阅制 SaaS 工作台（会话容器 + 内容引擎 + 透明流水线），服务替代形态而非工具
  source_of_business: 订阅续费（坚持装置成立=续费成立）；进线量/转发命中作为『内容带来客户』的商业信号
  product_or_service_design: 30 分钟硬上限的拍板仪式为核心容器；会话外全预处理；透明流水线可改可回滚；AI 只备选、人拍板
  enabling_technology: AI 文本/剪辑预处理管线 + 账号私有数据回流（转发值评分、归因引擎、天级战报）+ 合规发布闸口（AI 标识内建、人点发布）
  reason_to_believe: K-004（时间破产基线）、K-005（三层价位带+陪跑信任崩塌）、K-006（方法论外部基线）、K-007（单条成本 ¥1-10）——外部证据锚点齐全；作者本人
    dogfood 可作首条 L4 行为证据
  branding: 『坚持装置』叙事（反效率竞赛）+ 『方向盘在你手里』（反全托管）+ 『服务替代』（反黑箱）——三种叙事指向同一形态
  consumer_experience: 每晚 21:00 的 30 分钟仪式：3-5 个带理由的选题 → 拍板 → 确认发布 → 次日清晨战报；每步可见可改；断更时被救援而非被责备
```

## How It Works

```yaml
- step: 1
  action: 会话外备料：AI 消费账号私有数据（历史命中率、行业、日历）生成选题池（转发值评分排序）+ 文案稿 + 粗剪
  consumer_benefit: 打开会话即有 3-5 个带『谁会转给谁、为什么』理由的候选，零创作负担
  operational_benefit: 单条人工耗时从 3-8 小时压向 30 分钟以内；预处理在会话外异步完成
  strategic_rationale: 私有数据闭环入口——候选越贴账号越用越准，切换成本累积
  legal_regulatory_rationale: AI 生成内容标识在生成环节自动附加（K-003 合规要求）
  evidence_refs:
  - knowledge:K-004@1
  - knowledge:K-007@1
  - assumption:A-010@2
  - assumption:A-019@2
  design_refs:
  - artifact:ART-009@2#CI-001
  - artifact:ART-009@2#CI-010
  - artifact:ART-009@2#CI-006
- step: 2
  action: 30 分钟选择会话：固定时段的拍板仪式（选选题→微调文案→确认发布），倒计时硬约束，超时自动收束
  consumer_benefit: 方向盘在自己手里：每关键步老板拍板、AI 只给备选与理由；每天只付 30 分钟
  operational_benefit: 会话节律产生每日行为数据（决策留痕），坚持与否被量化
  strategic_rationale: 『坚持成立=续费成立』的因果链在每次会话中被验证——产品只卖坚持本身
  legal_regulatory_rationale: 人点发布闸口不可绕过（无发布 API 下的合规半自动）
  evidence_refs:
  - assumption:A-010@2
  - assumption:A-031@2
  design_refs:
  - artifact:ART-009@2#CI-001
  - artifact:ART-009@2#CI-022
- step: 3
  action: 透明工作台：五段流水线（选题→文案→剪辑→发布→数据）每步产物可见可改可回滚，效果归因到具体决策
  consumer_benefit: 看得见自己买的内容生产线——黑箱被移除，信任重建
  operational_benefit: 修改向后联动重算；归因口径固定可查，杜绝玄学
  strategic_rationale: 服务替代形态的第一性体验（信息差溢价被结构性移除）
  legal_regulatory_rationale: 归因与承诺不构成流量承诺（Charter 红线：不承诺流量）
  evidence_refs:
  - assumption:A-028@2
  - assumption:A-029@2
  design_refs:
  - artifact:ART-009@2#CI-019
  - artifact:ART-009@2#CI-020
- step: 4
  action: 天级战报 + 明日建议：次日清晨 3 个信号（曝光/点赞/私域进线）+ 近 7 天对比 + 一句话『明天该调什么』
  consumer_benefit: 回报信号以天计——不再赌 200-300 条后的爆发；信号直接转成明天的行动
  operational_benefit: 信号→行动闭环（建议-采纳-结果回流），内容迭代自动化
  strategic_rationale: 消灭『断更作为理性选择』的动机；建议采纳数据成为私有资产
  legal_regulatory_rationale: 建议是解释与选项而非指令，越权即产品失败
  evidence_refs:
  - assumption:A-011@2
  - assumption:A-017@2
  design_refs:
  - artifact:ART-009@2#CI-002
  - artifact:ART-009@2#CI-008
- step: 5
  action: 断更救援 + 坚持资产：缺席触发梯度救援（提醒→降载→代拟），streak/里程碑可视化
  consumer_benefit: 状态差也有 10 分钟轻载日——坚持不因状态波动中断；断更被事前拦截而非事后悔恨
  operational_benefit: 断更拦截直接保护 LTV（流失第一原因被产品化处理）
  strategic_rationale: 坚持装置必须容错；轻载/救援数据揭示个体脆弱点，越用越懂用户何时会放弃
  legal_regulatory_rationale: 救援永不自动发布——发布闸门永远是真人
  evidence_refs:
  - assumption:A-012@2
  - assumption:A-016@2
  - assumption:A-014@2
  design_refs:
  - artifact:ART-009@2#CI-003
  - artifact:ART-009@2#CI-007
  - artifact:ART-009@2#CI-005
```

## How To Implement

```yaml
- phase: P0 dogfood
  timing: 第 1-2 周
  objective: 作者自有 IP 跑通 30 分钟会话全流程，产出首条 L4 行为证据
  jobs_to_be_done:
  - 作者账号连续 21 天日更
  - 单条人工耗时压至 40 分钟内
  - 记录会话完成率与发布率
  capabilities_and_assets:
  - 作者自有方法论
  - 自有账号数据
  - AI 预处理管线 v0
  owner: 秋南Dylan（产品作者）
  dependencies:
  - AI 文本/剪辑管线可用
  risks:
  - dogfood 与真实用户行为偏差
  open_questions:
  - 30 分钟是否真实可维持
  pilot_and_rollout: 作者账号先行，数据作为 A-010 首条 L4 证据
- phase: P1 MVP
  timing: 第 1-2 月
  objective: 会话+战报+透明工作台 v0 上线，10-15 位种子老板（迁移包承接）
  jobs_to_be_done:
  - 30 分钟会话最小闭环
  - 天级战报
  - 透明工作台 v0
  - 迁移包 v0
  capabilities_and_assets:
  - P0 沉淀的会话模板
  - 合规发布闸口
  owner: 产品+工程（2 人）
  dependencies:
  - P0 完成
  risks:
  - 种子用户断更
  - 迁移摩擦
  open_questions:
  - 坚持率基线
  pilot_and_rollout: 种子池 30 天坚持率 ≥80% 为 P1 验收
- phase: P2 内容引擎+定价
  timing: 第 3-4 月
  objective: 转发值选题 v1 + 服务替代定价页上线，A-030/A-019 的 L4 实验启动
  jobs_to_be_done:
  - 转发值评分 v1
  - 服务替代定价页
  - 价格接受度实验（A-030）
  - 转发命中实验（A-019）
  capabilities_and_assets:
  - 账号历史数据回流
  - 定价页组件
  owner: 产品+工程+运营（3 人）
  dependencies:
  - P1 数据积累
  risks:
  - 价格接受度不达预期
  - 转发命中不可检出
  open_questions:
  - ¥3000+/月档真实转化率
  pilot_and_rollout: 付费转化 ≥25% 为 P2 验收
- phase: P3 数据闭环+实验规模化
  timing: 第 5-6 月
  objective: 归因面板、结构变体实验（承接 CI-030），15 条 Achilles 中关键 6 条 L4 结论
  jobs_to_be_done:
  - 归因面板 v1
  - 结构变体实验
  - Achilles L4 实验矩阵执行
  - 投资叙事与财务案例
  capabilities_and_assets:
  - 归因引擎
  - 实验框架
  - 数据闭环
  owner: 全员（3-4 人）
  dependencies:
  - P2 实验数据
  risks:
  - L4 样本不足
  - 归因不可信
  open_questions:
  - G2 就绪度
  pilot_and_rollout: G2 前每条 Achilles 有 L4 结论或显式例外
```

## How It Makes Money

```yaml
revenue_streams:
- 服务替代订阅 ¥3,980/月档（按产出单位条/周计价，对标全案 ¥1.5万/月分数档）
- 进阶档（结构实验/归因深度功能，后续版本）
pricing_and_volume_logic: 定价锚定代运营服务而非工具：¥3,980/月 ≈ 全案 26% 档位；按条/周计价使『续费=坚持』可度量；目标客群为三层价位带上层（K-005），窄而深定位下的可寻址规模受获客渠道约束（A-006）
adoption_retention_frequency_assumptions:
- assumption: 试用→付费转化率 ≥25%（迁移包承接存量受伤老板，自带付费预算）
  source: assumption:A-024@2（基线先行）+ K-005
- assumption: 月续费率 ≥95%（坚持装置成立=续费成立）
  source: assumption:A-010@2 + A-002
- assumption: 每日会话参与率 ≥80%（30 天窗口）
  source: assumption:A-010@2
- assumption: 获客 CAC ≤ ¥3,000（窄深定位触达成本可承受）
  source: assumption:A-006
development_and_operating_costs:
- assumption: 单条 AI 程序化工序边际成本 ¥1-10（真人素材+文本驱动架构）
  source: knowledge:K-007@1
- assumption: 单用户月基础设施成本 ¥30-300
  source: knowledge:K-007@1
- assumption: 3-4 人团队年成本约 ¥80-120 万（seed 阶段）
  source: 市场基准估算
- assumption: 迁移/合规/工具类一次性投入约 ¥30 万
  source: 估算（P1-P2 清单）
scenarios:
  base:
    revenue: 1430
    margin: 0.7
    earnings: 300
    investment: 150
    payback: 12-18 个月
  aggressive:
    revenue: 3800
    margin: 0.75
    earnings: 1300
    investment: 300
    payback: 9 个月
sensitivity:
- 转化率 ±10pp → 首年营收 ±¥250 万（base 场景）
- 月续费率 95%→90% → LTV 缩短约 30%
- CAC ±¥1000 → 单位经济敏感性中等（客单价 ¥3980/月支撑）
unresolved_model_gaps:
- ¥3000+/月档真实接受度未 L4 验证（A-030）
- 转化率/获客渠道无实测（A-006）
- 窄深定位的 TAM 边界未量化
```

## Validation

```yaml
consumer_desire:
  claim: 时间破产+信任缺口的老板会为『每天 30 分钟、自己握方向盘的日更能力』付费并坚持——对手是等不起不是不会剪
  evidence_refs:
  - knowledge:K-004@1
  - knowledge:K-005@1
  - artifact:ART-004@2
commercial_value:
  claim: 服务替代锚定价（¥3000+/月）配合单条边际成本 ¥1-10 的毛利结构支撑独立 SaaS
  evidence_refs:
  - knowledge:K-005@1
  - knowledge:K-007@1
  - assumption:A-030@2
feasibility_and_implementation:
  claim: AI 预处理+30 分钟会话+人点发布在现有技术下可交付，合规（AI 标识/真人出镜）可内建
  evidence_refs:
  - knowledge:K-007@1
  - knowledge:K-003@1
  - assumption:A-003
achilles_assumption_refs:
- assumption:A-019@2
experiment_refs: []
evidence_refs: []
invalidated_claims: []
```
