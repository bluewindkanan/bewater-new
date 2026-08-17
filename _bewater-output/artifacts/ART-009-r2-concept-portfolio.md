---
schema_version: 1
strategy_ref: artifact:ART-006@2
opportunity_ref: artifact:ART-007@1
idea_pool_ref: artifact:ART-008@2
concepts:
- id: CI-001
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-001
  parent_ids: []
  name: 30分钟选择会话
  pithy_description: 半小时日更
  consumer_insight: 自干派老板放弃 IP 不是因为缺技能，而是正反馈延迟下的时间破产——单条 3-8 小时投入要在 200-300 条后才可能兑现，对手是'等不起'不是'不会剪'；他缺的不是更强的创作能力，而是一个把日更成本压到时间破产线以下的交付容器。
  commercial_insight: 30 分钟会话是'坚持装置'的实物载体——坚持成立=续费成立的因果链在每次会话中被验证；会话节律产生每日行为数据，进入'方法论×私有数据'越用越准的闭环，构成可防御资产。
  idea_definition: 每晚固定 30 分钟的'选择会话'是产品的核心容器：AI 在会话外完成选题、文案、粗剪全部预处理，会话内老板只做三件事——选选题、微调拍板、确认发布。会话被设计为
    30 分钟硬上限的仪式，把日更从 3-8 小时的重体力劳动改写为每日 30 分钟的低负荷决策；人点发布与 AI 标识内建，方向盘始终在老板手里，产品只卖'坚持'本身。
  who_its_for: 时间破产但愿意为结果持续付费、已确认真人出镜的中小企业老板（粗糙自干派）——尤其是有私域盘、把 IP 当资产而非爱好的那批人。
  how_it_works: 以'固定时长的选择仪式'为机制：会话外预处理好候选，会话内仅保留 选择→拍板→发布 三个低负荷动作，时长用倒计时硬约束；发布动作永远由老板触发。
  what_it_replaces: 替代'每晚自己花 3-8 小时剪一条'的自干流程，也替代外包代运营的'全托管'——前者太重、后者交出方向盘。
  why_big: 把日更从'技能问题'改写为'流程问题'，是唯一能规模化服务'时间破产'人群的形态；30 分钟会话同时是续费的实物载体与行为数据的采集器，商业与留存同源。
  visualization: 每晚 21:00 手机弹出'今晚 30 分钟会话已就绪'；会话页只有三屏：①今日候选选题 3 个（各带一句话理由）②选中文案稿可微调
    ③确认发布；顶部倒计时 30:00。
  design_principles:
  - 会话内只做选择与拍板，不做创作
  - 会话时长硬上限 30 分钟，倒计时可见
  - 拍板即发布，不设二次确认拖累
  - 固定时段形成节律，节律即产品
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每天 30 分钟拍板，日更不再需要 3-8 小时——把时间破产线以下的坚持变成可能
        evidence_refs:
        - artifact:ART-004@2#I
      consumer_target:
        statement: 时间破产但愿意为结果持续付费、已确认真人出镜的粗糙自干派老板
        evidence_refs:
        - artifact:ART-004@2#I
    money:
      commercial_value_proposition:
        statement: 以 30 分钟会话为续费实物载体——坚持成立=续费成立的因果链在每次会话中被验证
        evidence_refs: []
      leverageable_assets:
        statement: 每日会话行为数据进入私有闭环，越用越准，构成方法论×数据的可防御资产
        evidence_refs:
        - artifact:ART-004@2#III
    tension:
      statement: 会话纪律要求老板每天固定时间出现，而时间破产恰恰是其常态——纪律刚性 vs 状态波动，谁来兜底？
    balance_choice: magic——会话内只做选择，用轻载与救援选项吸收状态波动，纪律服务于坚持而非考核
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-010@2
  decision: selected
  merge_into: null
- id: CI-002
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-002
  parent_ids: []
  name: 天级战报
  pithy_description: 每天见信号
  consumer_insight: 老板放弃 IP 不是因为不想，而是正反馈延迟下的时间破产——单条 3-8 小时投入要在 200-300 条后才可能兑现，对手是'等不起'不是'不会剪'；他需要的不是更复杂的分析，而是'今天有回报'的可感知证据。
  commercial_insight: 天级回流构成留存机制——续费不再赌内容爆发，而赌每日信号习惯的养成；信号与行为数据同时是'方法论×私有数据'闭环的输入，越用越准。
  idea_definition: 当日曝光/点赞/私域进线在次日清晨以极简'战报'回流，只呈现 3 个数字与近 7 天对比，不做实时、不做复杂分析；把'200-300
    条后才可能兑现'的延迟正反馈改写为'每天都能看到信号'的即时反馈，从根上消灭'断更作为理性选择'的动机。
  who_its_for: 已开始日更但看不到回报信号、正处在'等不起'边缘的老板——尤其是有私域进线诉求、每天会忍不住刷数据的那批人。
  how_it_works: 以'天级回流+极简呈现'为机制：每天固定时间把前一日行为与回报数据压缩成 3 个信号与一条趋势线，只呈现、不排名、不惩罚，把反馈周期从'条数级（200-300
    条）'压缩到'天级'。
  what_it_replaces: 替代'发完就看一眼、凭感觉判断'的无反馈状态，也替代抖音式复杂数据后台与周报/月报的延迟反馈。
  why_big: 天级信号把'赌 200-300 条后的爆发'改写为每天可验证的进程——这是消灭断更理性动机的机制本身；每日信号习惯一旦养成，留存与续费不依赖内容运气。
  visualization: 次日清晨一条'昨日战报'：曝光、点赞、私域进线 3 个数字 + 与近 7 天对比的迷你折线；整屏只有这些，点击才展开。
  design_principles:
  - 数据以天为单位回流，不做实时
  - 只呈现与坚持/回报相关的信号，指标不超过 3 个
  - 数字是燃料不是裁判——不排名、不惩罚、不制造焦虑
  - 战报绑定次日会话，看完即进入行动
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每天清晨看到曝光/点赞/进线信号——'200-300 条后的爆发'被改写为每日可验证的进程
        evidence_refs:
        - artifact:ART-004@2#I
      consumer_target:
        statement: 已开始日更但看不到回报信号、正在'等不起'边缘徘徊的老板
        evidence_refs:
        - artifact:ART-004@2#I
    money:
      commercial_value_proposition:
        statement: 天级数据回流构成留存机制——续费不赌内容爆发，而赌每日信号习惯
        evidence_refs: []
      leverageable_assets:
        statement: 天级行为与表现数据是私有闭环的输入，越用越准
        evidence_refs:
        - artifact:ART-004@2#III
    tension:
      statement: 天级数字多是噪声——小样本波动可能诱发数据焦虑与短视优化（为点赞调内容），反而动摇坚持
    balance_choice: magic——数字是燃料不是裁判，只呈现不惩罚，坚持优先于指标
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-011@2
  decision: null
  merge_into: null
- id: CI-003
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-003
  parent_ids: []
  name: 断更救援
  pithy_description: 断更前救援
  consumer_insight: 断更往往不是一个决定，而是'今天没空'累积成'算了'；时间破产的老板缺的不是意志，而是一个在他动摇时出手的机制——对手是'等不起'不是'不会剪'。
  commercial_insight: 断更是订阅流失的第一原因——把断更拦截产品化，就是直接保护 LTV；救援中的降载与代拟成本可控，换来的是续费链条不断。
  idea_definition: 系统监测'是否进入会话'这一行为信号，连续 N 天未进入时按梯度主动干预：先提醒（轻触），再降载（自动收缩本周产出目标），最后代拟（生成候选内容供老板拍板）；把断更从事后悔恨变成事前拦截；救援永不自动发布，红线在人点发布与
    AI 标识内。
  who_its_for: 有断更史（近 3 个月断更 2 次及以上）或工作节奏不可控、常徘徊在'算了'边缘的老板。
  how_it_works: 以'缺席触发+梯度救援'为机制：以'是否进入会话'为行为信号，N 天未进入触发 提醒→降载→代拟 的递增干预，干预终点永远是'老板在会话内拍板'。
  what_it_replaces: 替代'断更后的悔恨与重启成本'（重新捡起需要更大决心），也替代日历提醒这类无差别、无递减策略的提醒。
  why_big: 断更拦截直接作用于留存第一杀手；救援过程产生的行为数据揭示每个用户坚持的脆弱点，反哺降载与提醒设计——越用越懂'他什么时候会放弃'。
  visualization: 第 2 天没进会话，晚间收到'明天补一次还是轻载？'；第 3 天 AI 主动降载：'这周只剩 2 条，我拟好了 3 个选题等你拍板'；第
    5 天可选地同步提醒合伙人。
  design_principles:
  - 干预按 提醒→降载→代拟 梯度递增，先轻后重
  - 救援永不自动发布，发布永远由老板触发
  - 救援动作可被老板一键关闭
  - 每次救援留痕，解释'为什么现在提醒你'
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 连续 N 天未进会话时主动救援——断更从事后悔恨变成事前拦截
        evidence_refs:
        - artifact:ART-004@2#I
      consumer_target:
        statement: 有断更史或工作节奏不可控、常在'算了'边缘的老板
        evidence_refs: []
    money:
      commercial_value_proposition:
        statement: 断更拦截直接保护 LTV——流失第一原因被产品化处理
        evidence_refs: []
      leverageable_assets:
        statement: 救援触发数据揭示坚持脆弱点，反哺降载与提醒设计
        evidence_refs: []
    tension:
      statement: 救援力度与'方向盘在老板手里'的边界——代拟到什么程度仍算'老板的选择'，而不是'AI 在替你坚持'？
    balance_choice: magic——救援只到'候选+拍板'，永不自动发布，红线在人点发布与 AI 标识内
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-012@2
  decision: null
  merge_into: null
- id: CI-004
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-004
  parent_ids: []
  name: 按产出计价
  pithy_description: 按条数计费
  consumer_insight: 老板不为工具付费，为'有人替我产出结果'付费；他对代运营的数千至数万/月报价有认知，对 50-800 元/月工具费无感——锚点决定付费意愿。
  commercial_insight: 计价即定位——按产出单位计价把价格锚定到'服务替代'而非'工具'，客单价空间高一个量级；且'续费=坚持'的因果链变得可度量：停用才损失产出。
  idea_definition: 按'条/周'的产出单位而非素材时长或功能数量计价，价格锚定代运营服务；反向设计'轻度使用=惩罚坚持'的工具锚逻辑——用得越久越便宜、停用才产生真实损失；计价的产出下限以'可坚持的最小日更节奏'为约束，防止低价档稀释坚持目标。
  who_its_for: 对代运营报价有认知、按结果付费意愿高、把 IP 当资产而非工具的中小企业老板。
  how_it_works: 以'计价单位=产出单元'为机制：价格与'条/周'绑定而非时长/功能，续费页以'本周已产出 N 条'为履约证据，把使用强度直接翻译为金钱得失。
  what_it_replaces: 替代'按素材时长/条数打包的工具订阅'与'按条高价外包的代运营'两种既有计价——前者与坚持脱钩，后者贵到不可持续。
  why_big: 计价是定位本身——服务替代定价打开比工具锚高一个量级的客单价；产出即履约证据，每一条都是续费理由与口碑素材，商业模型与坚持机制同构。
  visualization: 报价页只有一档：'每周 3 条起，¥X/周'，旁边并排代运营'¥XXXX/月'作参照；续费页显示'本周已产出 3 条，连续坚持 21
    天'。
  design_principles:
  - 按条/周计价，与素材时长彻底解耦
  - 价格锚定代运营服务，而非工具
  - 计价下限不得低于'可坚持'的最小产出
  - 产出即履约证据，续费页呈现坚持成果
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 按产出单位付费——为'坚持'付钱，而不是为素材时长/功能付钱
        evidence_refs: []
      consumer_target:
        statement: 对代运营报价有认知、按结果付费意愿高、对工具锚无感的老板
        evidence_refs: []
    money:
      commercial_value_proposition:
        statement: 服务替代定价打开比工具锚高一个量级的客单价；续费=坚持的因果链可度量
        evidence_refs: []
      leverageable_assets:
        statement: 产出数据即履约证据——每一条都是续费理由与口碑素材
        evidence_refs: []
    tension:
      statement: 按条计价若设最低档，用户倾向选最低档→周产出下滑，与日更目标冲突；设高下限又吓退时间破产用户
    balance_choice: money——但计价下限以'可坚持的最小产出'为约束，商业机制必须服务于坚持目标
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 3/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-013@2
  decision: null
  merge_into: null
- id: CI-005
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-005
  parent_ids: []
  name: 坚持链与契约
  pithy_description: 坚持可见化
  consumer_insight: 自干派老板有展示欲与竞争心，但'坚持'不可见就无法自我证明、也无法被辜负——把坚持变成看得见的资产，才有断不得的约束力。
  commercial_insight: 进度资产化创造切换成本——streak 越久，离开的心理代价越高；里程碑分享是零成本获客素材，把坚持本身变成传播内容。
  idea_definition: 把'坚持'变成可感知、可展示的进度资产：日更 streak 链、里程碑节点与可分享的坚持卡片；以正激励的可视化为主，可选叠加契约（对赌/承诺）作为进阶附件；让坚持从内心想法变成看得见、断不得、舍不得的资产。
  who_its_for: 有竞争心/展示欲、需要自我证明的老板——如习惯在朋友圈立 flag、自诩自律的那批人。
  how_it_works: 以'行为连续性资产化'为机制：把每天'进入会话并发布'编码为一条只增不减的链，中断即重置；里程碑自动生成分享物，让连续性与中断代价都可见。
  what_it_replaces: 替代'坚持只是内心想法'的不可见状态，也替代健身 App 式通用打卡——这里的链绑定真实发布行为。
  why_big: streak 是心理学上最强的习惯机制之一；进度资产化创造天然切换成本，且分享卡片让'坚持'成为获客内容——坚持本身开始自我复制。
  visualization: 个人页一根'坚持链'：每一天一个圆点，连续不断；到'第 30 条·坚持一个月'自动生成可分享卡片，卡面上是老板真人出镜与连续天数。
  design_principles:
  - 可视化正激励为主，契约惩罚仅为可选附件
  - streak 只增不减，绑定真实发布而非打卡
  - 里程碑由老板自定义，分享物默认带上产品印记
  - 中断即重置，但轻载日不破链
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 把坚持变成看得见、断不得的进度资产——streak 与里程碑
        evidence_refs: []
      consumer_target:
        statement: 有展示欲/竞争心、需要自我证明的自干派老板
        evidence_refs: []
    money:
      commercial_value_proposition:
        statement: 进度资产化创造切换成本——streak 越久越难离开；里程碑分享是零成本获客
        evidence_refs: []
      leverageable_assets:
        statement: 可分享的坚持卡片形成口碑传播面，坚持本身成为获客内容
        evidence_refs: []
    tension:
      statement: 契约（对赌/惩罚）越强越有效也越劝退——与时间破产人群对额外压力的厌恶冲突，弱契约又形同虚设
    balance_choice: magic——可视化正激励为主，契约仅作可选附件，绝不让坚持变成负担
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 3/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: split
  assumption_refs:
  - assumption:A-014@2
  decision: null
  merge_into: null
- id: CI-006
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-006
  parent_ids: []
  name: 会话外备料
  pithy_description: 会话外备料
  consumer_insight: 老板的创作负担集中在会话外——想选题、写文案、剪片子，这才是单条 3-8 小时的来源；会话内轻松的前提是会话外有人把活干完，而'等不起'的人没有时间在会话外自学技能。
  commercial_insight: 预处理管线是'方法论×私有数据'闭环的载体——选题采纳率、素材表现随使用回流，越用越准，构成不可复制的资产；'有方法论'本身已商品化，可防御位置只剩方法论×私有数据。
  idea_definition: 选题池、文案稿、粗剪全部在会话外异步生成：AI 基于历史表现、老板偏好与日历等私有数据产出候选与理由，会话内零创作负担——只呈现候选、只做选择，不推高决策频率与决策量；预处理结果可追溯、可解释，老板始终知道'为什么推荐这个'。
  who_its_for: 技能薄弱（不会剪、不会写、不会选题）但坚持真人出镜的纯自干派老板。
  how_it_works: 以'场外异步预处理'为机制：管线在会话外消费私有数据产出候选集，会话内只消费候选——创作负担全部外移，决策量被压缩到选择层。
  what_it_replaces: 替代'从选题到成片全在晚上自己做'的创作流程，也替代'现学现剪'的技能补课路径。
  why_big: 预处理是私有数据闭环的入口——使用越久，候选越贴个体，切换成本越高；它是'越用越准的部分才是资产'的物理载体，也是把日更从 3-8 小时压到
    30 分钟的关键。
  visualization: 会话外，AI 依据上周数据与老板日历产出 5 个选题、2 版文案与粗剪草稿；老板打开会话时看到的是'已备好的菜'，只需挑选，每道菜带一句'为什么推荐'。
  design_principles:
  - 预处理全部在会话外完成，会话内零创作负担
  - 只呈现候选与理由，不推高决策频率与决策量
  - 预处理可追溯可解释，老板知道推荐依据
  - 产出仍由人点发布，AI 标识内建
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 会话外全部预处理，会话内零创作负担——单条总投入从 3-8 小时压到 30 分钟
        evidence_refs:
        - artifact:ART-004@2#I
      consumer_target:
        statement: 技能薄弱但坚持真人出镜的纯自干派老板
        evidence_refs:
        - artifact:ART-004@2#I
    money:
      commercial_value_proposition:
        statement: 预处理管线是'方法论×私有数据'闭环的载体——越用越准的部分才是资产
        evidence_refs:
        - artifact:ART-004@2#III
      leverageable_assets:
        statement: 选题采纳率、素材表现等私有数据随使用累积，构成可防御位置
        evidence_refs:
        - artifact:ART-004@2#III
    tension:
      statement: 预处理越充分，会话越轻松，但老板对内容的掌控越间接——真实感/掌控感可能被稀释，'这是 AI 的号还是我的号'？
    balance_choice: magic——预处理只到'候选+理由'，拍板与微调权永远留在会话内
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-015@2
  decision: null
  merge_into: null
- id: CI-007
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-007
  parent_ids: []
  name: 轻载日
  pithy_description: 轻载保日更
  consumer_insight: 大量断更不是'不想做'而是'那天没状态'——时间破产人群的状态波动是常态，他们需要的不是'再坚持一下'，而是一个状态差时也能完成的降载选项。
  commercial_insight: 把最大断更诱因（状态波动）变成产品功能，直接扩大可服务人群；轻载日保住 streak，也就保住了续费因果链——坚持装置必须容错。
  idea_definition: 状态差的日子提供 10 分钟'最低可持续日'模板：1 个选题、一段口播提示词、一键粗剪，仍产出并发布一条；把'状态波动→断更'的二元选择改写为'状态波动→降载但仍日更'，坚持不因状态中断。
  who_its_for: 出差/应酬/状态波动频繁、断更多因'那天没状态'而非'不想做'的老板。
  how_it_works: 以'状态自适应降载'为机制：会话内提供轻载入口，把当天决策量降到最低可持续水平（1 选题/1 稿/一键粗剪），产出仍为真发布，链不断。
  what_it_replaces: 替代'状态差就直接断更'的二元选择，也替代'状态差硬撑 3 小时'的消耗式坚持。
  why_big: 状态波动是断更的第一诱因——把它产品化等于给坚持装置装了减震；轻载日同时是流失风险的提前泄压阀，扩展可服务人群。
  visualization: 会话页底部一个'今天没状态'按钮→进入 10 分钟轻载模式：只有 1 个选题、一段口播提示词、一键粗剪；仍产出并发布一条，坚持链不中断。
  design_principles:
  - 10 分钟最低可持续日，轻载不等于断更
  - 状态自评触发，不预设失败、不惩罚轻载
  - 轻载日仍真发布，链不断
  - 轻载频率可见，用于识别长期疲惫而非追责
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 状态差也有 10 分钟最低可持续日——坚持不因状态波动中断
        evidence_refs:
        - artifact:ART-004@2#I
      consumer_target:
        statement: 出差/应酬/状态波动频繁、断更多因'那天没状态'的老板
        evidence_refs: []
    money:
      commercial_value_proposition:
        statement: 把最大断更诱因变成产品功能，扩大可服务人群并保住 streak=保住续费链
        evidence_refs: []
      leverageable_assets:
        statement: 轻载使用数据揭示个体脆弱模式，反哺降载与救援设计
        evidence_refs: []
    tension:
      statement: 轻载日内容质量低——为保连续而发低质内容，是否损害账号权重与粉丝期待，反而伤害长期回报？
    balance_choice: magic——连续性优先，轻载模板守住基本盘，质量由正常日补回
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-016@2
  decision: null
  merge_into: null
- id: CI-008
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-008
  parent_ids: []
  name: 明天调什么
  pithy_description: 明天调什么
  consumer_insight: '''数据看了不知道怎么办''是数据回流断在行动前的常见死因——老板要的不是报表，而是''明天干什么''；没有行动的反馈等于没有反馈。'
  commercial_insight: 信号→行动闭环让天级回流真正作用于内容迭代，是坚持装置从'看信号'升级为'会进化'的关键；建议-采纳-结果三元组构成方法论×数据的核心私有资产。
  idea_definition: 把天级数据转译成'明天该调什么'的一句话建议，绑定在次日会话中呈现：建议基于近 7 天数据对比生成，是解释与选项而非指令，老板可'采纳/换一个'；完成信号→行动闭环，让每天的信号直接作用于明天的那一条。
  who_its_for: 看不懂数据、或看了不知道怎么办的老板——需要'有人告诉我明天干嘛'的那批人。
  how_it_works: 以'信号→行动转译'为机制：把回流数据与历史表现比对，压缩为一条可执行建议，在次日会话内作为选项呈现，采纳权在老板；建议-采纳-结果闭环回流为私有数据。
  what_it_replaces: 替代'数据看完不知道干嘛'的无效反馈，也替代找付费教练/顾问看数据的昂贵路径。
  why_big: 建议采纳数据随使用累积为'方法论×数据'的私有资产；闭环一旦成立，产品从反馈仪表变成会调优的坚持教练，不可复制。
  visualization: 战报末尾一行：'明天建议：把开头 3 秒换成结果预告试试——同类开头近 7 天均值高出 20%'；附带'采纳/换一个'两个按钮，采纳结果在下次战报回显。
  design_principles:
  - 一句话建议，不多于一句
  - 建议是解释与选项，不是指令，方向盘在老板
  - 建议绑定次日会话呈现，不单独推送骚扰
  - 采纳结果回流，闭环可见
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 把天级数据转译成'明天该调什么'的一句话建议——信号→行动闭环
        evidence_refs: []
      consumer_target:
        statement: 看不懂数据、看了不知道怎么办的老板
        evidence_refs: []
    money:
      commercial_value_proposition:
        statement: 建议采纳数据构成私有闭环，产品从'看信号'进化到'会调优'——不可复制
        evidence_refs:
        - artifact:ART-004@2#III
      leverageable_assets:
        statement: 建议-采纳-结果三元组随使用累积，是方法论×数据的核心资产
        evidence_refs:
        - artifact:ART-004@2#III
    tension:
      statement: 自动建议可能从'解释与选项'滑向'AI 在开车'——建议越具体越有用，也越接近替老板做决定
    balance_choice: magic——建议绑定次日会话、采纳权永远在老板，越权即产品失败
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-017@2
  decision: null
  merge_into: null
- id: CI-009
  item_revision: 1
  opportunity_area_id: OA-001
  source_seed_id: CS-010
  parent_ids: []
  name: 拍档监督侧
  pithy_description: 有人盯着我
  consumer_insight: 一部分老板'为自己坚持不动、为他人坚持得动'——外部眼睛是现成的责任杠杆；拍档/团队本就关心 IP 进展，只是没有一个不打扰的视角。
  commercial_insight: 引入外部责任人把坚持的稳定性从单人意志转移到多人网络，降低单点流失；监督侧只是只读链接，成本极低，却把家庭/团队变成续费同盟。
  idea_definition: 让老板的拍档或团队以只读方式看到坚持进度（streak 与发布记录，看不到数据明细与草稿）：暴露范围由老板自选，外部人看到的是'他还在坚持'而非'他的数据'；把外部责任变成坚持装置的一部分，为'为自己坚持不动、为他人坚持得动'的人群提供杠杆。
  who_its_for: 有配偶/合伙人/小团队在场、在意他人评价的老板——尤其是'怕丢脸'胜过'怕亏钱'的那批人。
  how_it_works: 以'外部责任回路'为机制：老板授权后生成只读进度视图，外部人可查看不可干预；责任主体从自我转移到他人，坚持的违约成本外部化。
  what_it_replaces: 替代'独自坚持无人知晓'的孤立状态，也替代朋友圈立 flag 这种不可持续、无反馈的自我监督。
  why_big: 社会问责是行为改变最强的机制之一；把老板身边现成的人变成监督者，等于零成本扩充坚持装置的约束力，触及纯自我驱动覆盖不了的人群。
  visualization: 设置页'让谁看到我的坚持链'：勾选合伙人/团队；对方收到只读链接，看到 streak 与最近发布，看不到数据明细与草稿；对方页面只有一句话：'他还在坚持'。
  design_principles:
  - 暴露范围与内容边界由老板自选
  - 外部人看到进度而非数据，只读不干预
  - 责任回路只增不减老板的控制权
  - 外部人退出机制随时可用
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 让拍档/团队看到坚持进度——外部眼睛把坚持从单人意志变成多人责任
        evidence_refs: []
      consumer_target:
        statement: '''为自己坚持不动、为他人坚持得动''、有配偶/合伙人/小团队在场的老板'
        evidence_refs: []
    money:
      commercial_value_proposition:
        statement: 外部责任回路降低单点流失——坚持稳定性从个人意志转移到多人网络
        evidence_refs: []
      leverageable_assets:
        statement: 只读监督链接成本极低，却把家庭/团队变成续费同盟与口碑传播者
        evidence_refs: []
    tension:
      statement: 把坚持失败暴露给拍档/团队——面子与隐私风险，可能只有少数老板愿意开启，且外部人参与度不可控
    balance_choice: magic——暴露范围与边界由老板自选，责任回路服务于坚持，绝不反向施加压力
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 3/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 3/5
      altitude: 4/5
      healthy_anxiety: 2/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-018@2
  decision: null
  merge_into: null
- id: CI-010
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-012
  parent_ids: []
  name: 转发值选题引擎
  pithy_description: 转发值选题
  consumer_insight: 视频号社交推荐占分发 C 位（F7：51% 的用户因好友点赞激发观看、私域约 1:1 撬公域），按抖音热度/完播率逻辑选题在此是系统性错配（insight
    II）；自干派老板时间破产（insight I），每一条『发出去没人转』的内容都是浪费——选题是内容成败的第一决策点，却从未被按『社交价值』产品化。
  commercial_insight: 选题方法论组件已被商品化（insight III），通用选题工具给所有人同样的爆款列表、无账号级私有数据；把『转发值』做成可随天级回流自校准的账号私有评分模型，『越用越准』的部分才是资产。
  idea_definition: 一档把『值得点赞/转发』做成可打分、可排序的选题机制：会话外 AI 预处理出候选选题池，每条输出转发语境评分（谁会转、转给谁、为什么转）与点赞理由评分，替代热度/完播率逻辑；评分权重随账号历史命中率回流自校准。社交推荐机制为候选前提（insight
    5 未签，作为开放假设）。
  who_its_for: 主阵地在视频号、每天只有 30 分钟、不知道明天发什么的粗糙自干派老板——尤其按抖音热门逻辑选题却屡发不转的那些。
  how_it_works: 机制=选题层的数据闭环：对候选选题池按社交价值两维度（可转发性：是否存在具体转发对与理由；点赞理由强度：是否给出可被认同引用的具体理由）打分排序，账号历史高转发条目的共同特征回流为评分权重——只做选题层的选择与校准，不涉及成片与发布。
  what_it_replaces: 替代『看抖音热门/抄爆款选题』的做法与通用选题拆解工具（蝉妈妈类）——从『什么火发什么』换成『谁会给谁转什么』。
  why_big: 选题是每条内容的第一决策点，而视频号社交推荐占 C 位（F7）；所有抖音系工具按完播率选题（insight II 的结构性空位），一个为转发而选题的引擎正好占住大厂进不来的位置。
  visualization: 每晚 30 分钟会话的第一屏：3-5 条候选选题，每条一行理由——『转发评分 82｜采购总监会转给质检负责人：避坑清单』；老板点选或调整，评分随昨日回流数据实时跳动。
  design_principles:
  - 评分可解释——每条选题必须给出『谁会转给谁、为什么』的一行理由，禁止黑箱分数
  - 数据回流优先于专家规则——评分权重随账号命中率自校准，不写死方法论
  - 会话内零创作负担——候选池会话外生成，会话内只做选择
  - 不为完播率优化——任何提高完播率但降低转发值的维度不进评分
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 选题从『赌什么火』变成『选哪条值得被转发』——每条选题都有可解释的转发理由支撑，转发命中以天级可见。
        evidence_refs:
        - knowledge:K-006@1
        - knowledge:K-003@1
        - insight:ART-004@2:II
      consumer_target:
        statement: 视频号真人创始人 IP 中按社交价值而非完播率选题的粗糙自干派老板。
        evidence_refs:
        - insight:ART-004@2:I
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 转发值评分随账号数据回流自校准——选题引擎是私有数据闭环的第一入口，构成越用越准的切换成本与续费理由。
        evidence_refs:
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 作者自有选题方法论作为初始评分组合，叠加账号历史命中率数据持续校准。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 转发值评分依赖『社交推荐机制』这一未签候选前提（insight 5）——若社交推荐实际权重低于假设，评分维度整体失真，而完播率维度又已被战略砍掉，选题引擎失去基准。
    balance_choice: Magic 侧——先证明转发值选题带来可感知的转发命中，再谈评分模型的数据资产化。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5 依赖未签的社交货币机制
      appeal: 4/5
      differentiation: 5/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5 整个引擎建立在未签 insight 5 上
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-019@2
  decision: selected
  merge_into: null
- id: CI-011
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-013
  parent_ids: []
  name: 转发语境卡
  pithy_description: 谁转给谁
  consumer_insight: 视频号内容为『一个具体的人转发给另一个具体的人』而设计（F7），但老板的内容常常『内容对、没人转』——因为没有给转发者一个现成的『转给谁、附什么话』的理由；自干派老板发一条已耗尽精力（insight
    I），无力再做语境设计。
  commercial_insight: 语境卡是『为关系链而发』的最小可交付单元：每个具体转发对的命中都是一次社交推荐分发（1:1 撬公域），命中数据按行业/人群沉淀为私有转发语境资产——方法论×私有数据的可防御位置（insight
    III）。
  idea_definition: 每条内容在会话内强制产出一张转发语境卡：明确的转发者画像、接收者画像、转发理由、转发时附带的一句话；语境卡作为脚本生成的结构约束（钩子与埋点从语境推导），让内容天然携带『某人转给某人的理由』。
  who_its_for: 发过内容但转发惨淡、希望内容在微信关系链里被主动转走的视频号真人创始人 IP。
  how_it_works: 机制=会话内一个强制的语境化步骤：每选中一条内容，先填『谁→谁→为什么→附什么话』四格，脚本结构（钩子、埋点、结尾）从语境推导而非事后包装——语境是生成约束，不是可选优化。
  what_it_replaces: 替代面向算法写内容、转发听天由命的做法，以及代运营/陪跑靠经验『蹭热点』的选题方式。
  why_big: 转发是视频号社交推荐引擎的分发货币（F7）——给每条内容装上具体转发对是平台机制下最直接的杠杆；这一层没有大厂工具做（insight II），语境命中数据随时间沉淀为行业/人群私有的转发语境资产。
  visualization: 会话中内容页下方四格卡片：转发者『采购总监』→接收者『质检负责人』→理由『避坑清单，防踩供应商的坑』→附言『老规矩，转给下个要签合同的人』；脚本区标注语境埋点位置。
  design_principles:
  - 语境先于文案——先有转发对，才有脚本结构
  - 具体优先——禁止『受众/用户』抽象画像，必须是可指认的角色
  - 一条一卡——语境卡是每条内容的强制交付物
  - 附言可复制——转发者转的时候能直接复制一句话，降低转发成本
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每条内容自带『谁转给谁、为什么转、附什么话』——转发不再靠运气，而是被设计出来的动作。
        evidence_refs:
        - knowledge:K-006@1
        - knowledge:K-003@1
      consumer_target:
        statement: 有内容产出但转发率低、想让内容在微信关系链里流动的真人创始人 IP。
        evidence_refs:
        - insight:ART-004@2:I
    money:
      commercial_value_proposition:
        statement: 语境命中数据按行业/人群沉淀为私有转发语境资产，越用越准构成续费与切换成本。
        evidence_refs:
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 作者代运营经验中的转发语境 know-how 作为初始模板组合。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 语境卡为理想转发对精确设计，可能窄化内容对算法推荐池的广谱吸引力——精确定位 vs 广谱曝光，二者可能互斥。
    balance_choice: Magic 侧——先验证带语境卡的内容转发率显著更高，再决定是否牺牲广谱曝光。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 3/5 依赖社交货币假设
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5 同样依赖未签 insight 5 的社交推荐机制
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-020@2
  decision: null
  merge_into: null
- id: CI-012
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-014
  parent_ids: []
  name: 私域钩子工作台
  pithy_description: 私域进线
  consumer_insight: F7：私域导入约 1:1 撬公域推流；老板的微信关系链与私域是他唯一带得走的资产，但内容尾部常常没有进线设计——看完即走，公域流量无法沉淀；时间破产（insight
    I）下每条内容都要最大化回收，进线是唯一可量化、可归因的回收。
  commercial_insight: 私域进线量是可天级回流、可归因到单条内容的硬指标——同时服务坚持（OA-001 回报信号）与内容精度（OA-002 命中率），是数据闭环里最干净的商业信号；私域资产增值直接支撑服务替代定价。
  idea_definition: 内容尾部的进线设计工作台：为每条内容生成好友申请理由（加好友时的一句话）、进线路径（企微/个微/群）与进线话术，进线量按条归因并天级回流，反哺选题与语境设计。
  who_its_for: 已有或愿意建私域、把视频号当获客入口的创始人 IP——『公域涨粉是虚荣、私域进线是真金』的老板。
  how_it_works: 机制=在内容尾部把『看完』转成『申请加好友』：进线理由由内容主题推导（不是『交个朋友』而是『领取那份清单』），进线量按条归因回流，成为选题/语境层的校准信号——收口设计与数据回流的耦合。
  what_it_replaces: 替代内容尾部『关注引导/点赞引导』的泛流量做法与需要专人的客服式私域运营，以及代运营的涨粉 KPI 叙事。
  why_big: 1:1 撬公域（F7）意味着进线既是沉淀又是分发杠杆；私域是老板唯一可控的资产，进线工作台把『内容→客户』链路产品化——这是绑定自家投放生态的大厂工具与无微信私域语境的抖音方法论都做不了的（insight
    II）。
  visualization: 会话末尾一步：系统给出尾部方案——结尾 8 秒『评论区扣 1，或直接加我，领《供应商避坑清单》』；好友申请自动带『领清单』备注；次日进线数按条显示在数据页。
  design_principles:
  - 理由先于路径——先设计为什么加，再设计怎么加
  - 进线可归因——每条内容的进线量单独统计，不打混
  - 钩子即承诺——进线理由必须对应内容里真实交付的东西
  - 不刷量——只设计真实进线，不做假加粉
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 内容尾部不再是求关注，而是带走一个具体好处——每条内容都有可量化的私域回收。
        evidence_refs:
        - knowledge:K-006@1
        - knowledge:K-003@1
      consumer_target:
        statement: 把视频号当获客入口、愿意经营微信私域的创始人 IP。
        evidence_refs:
        - insight:ART-004@2:I
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 进线量是唯一可归因到单条内容的硬商业信号——支撑『内容带来客户』的服务替代叙事与续费。
        evidence_refs:
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 私域进线数据沉淀为账号私有资产，回流到选题与语境。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 尾部进线设计越强，内容越像广告、越伤害为关系链而发的真诚人设——进线效率 vs 信任感。
    balance_choice: Magic 侧——先保证内容本身值得转发，进线设计以不伤害人设为上限。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5 1:1 撬公域有机制文本但无拆分数据
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 5/5
      altitude: 4/5
      healthy_anxiety: 3/5 钩子过强伤害人设的边界需实测
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-021@2
  decision: null
  merge_into: null
- id: CI-013
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-015
  parent_ids: []
  name: 真人合规工作流
  pithy_description: 真人合规流
  consumer_insight: insight II：视频号用政策（压制数字人、鼓励真人）加封闭接口（无发布 API）圈出真人 IP 场；K-003：AI
    生成内容 2025-09 起强制标识、数字人直播违规、违规处罚对依赖社交推荐的账号近乎致命——老板既没能力也没意愿搞懂这些红线，一条违规内容可能废掉整个账号。
  commercial_insight: 合规不是成本而是壁垒的产品化：政策本身就是大厂进不来的护城河（insight II），把真人出镜+AI 标识内建+人点发布做成产品内强制管线，等于把政策红利变成可交付的服务承诺——代运营与通用工具都覆盖不了这个位置。
  idea_definition: 把视频号合规红线做成产品内强制工作流：所有 AI 生成内容自动附带显式+隐式标识；素材入管线前做数字人/非真人检测拦截；发布环节设计为『人手指确认』（无发布
    API 下的合规半自动）——老板在会话内的每一步都走在合规护栏里，违规风险从用户身上移走。
  who_its_for: 真人出镜、不想研究平台规则、害怕违规封号的视频号创始人 IP——尤其是被数字人工具坑过、被全自动发布骗过的老板。
  how_it_works: 机制=合规作为管线约束而非用户义务：生成环节自动加标识、入管线环节自动检测拦截、发布环节强制人工确认——三个强制闸口把『用户自行担责』变成『产品内建护栏』；合规规则随政策文本更新（与
    CI-015 的监控机制联动）。
  what_it_replaces: 替代裸奔式自剪自发的违规风险、数字人工具（已违规风险）与 RPA 全自动发布（运营规范风险）——把违规风险从用户身上移走。
  why_big: 合规是视频号的结构性闸口（K-003），谁把合规做成顺滑的产品体验，谁就独占真人 IP 场的入口；AI 内容只会更多、政策只会更严，合规能力是随时间增值的资产（insight
    II）。
  visualization: 发布前最后一步：预览页顶部绿色横幅『已含 AI 标识 ✓ 真人检测通过 ✓ 待你确认发布』，老板点确认完成今日第 1 条；任何 AI
    素材缺标识时流程直接卡住并提示补标识。
  design_principles:
  - 合规内建而非提醒——违规动作在管线里被物理拦截
  - 标识零负担——AI 标识自动附加，老板不需要理解规则
  - 人点发布不可绕过——发布闸门永远是真人
  - 政策变化即产品变化——合规规则随政策更新，不写死
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 老板在不可能违规的护栏里做内容——合规不再是他的知识负担。
        evidence_refs:
        - knowledge:K-003@1
        - insight:ART-004@2:II
      consumer_target:
        statement: 真人出镜、怕违规怕封号的视频号创始人 IP。
        evidence_refs:
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 合规管线是政策壁垒的产品化——独占真人 IP 场入口，且随时间增值。
        evidence_refs:
        - insight:ART-004@2:II
        - knowledge:K-003@1
      leverageable_assets:
        statement: 政策文本监控与合规规则库作为持续更新的私有 know-how。
        evidence_refs:
        - insight:ART-004@2:II
    tension:
      statement: 合规闸口（人点发布、标识检查）增加每步摩擦 vs 30 分钟会话纪律要求顺畅——护栏 vs 顺滑。
    balance_choice: Magic 侧——先保证合规零负担（摩擦被会话设计吸收），再谈合规作为卖点。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 5/5 政策文本锚点齐全
      appeal: 3/5 属底线价值而非增长价值
      differentiation: 5/5 独占位
      naming: 3/5
      visualization: 4/5
      design_principles: 5/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5 摩擦拖累坚持率是真实风险
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-022@2
  decision: merged
  merge_into: CI-029
- id: CI-014
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-016
  parent_ids: []
  name: 结构变体 A/B
  pithy_description: 结构变体
  consumer_insight: insight I：同一选题，怎么说决定成败，但自干派老板没有余力做多版本试错（单条 3-8 小时）；insight III：方法论商品化后，只有组合调优×账号私有数据可防御——结构变体的命中率回流正是账号级私有数据的积累方式。
  commercial_insight: 结构变体实验是越用越准的最小闭环：每条内容的多版本+命中率回流，构成账号私有内容参数模型（insight III 的数据资产）；通用工具给所有人同样的结构模板，这里给每个账号自己的结构参数。
  idea_definition: 同一选题由会话外 AI 生成多个结构变体（不同钩子/信息顺序），老板在会话内选 1-2 个发布；发布后天级回流（转发/点赞/进线）比较变体命中率，命中率回传为结构生成参数的校准信号。原生格式规则（CI-018）作为结构参数空间的维度一并验证。
  who_its_for: 已能稳定日更、想从『发了』进阶到『发得准』的视频号创始人 IP——结构调优是坚持之后的第二台阶。
  how_it_works: 机制=结构参数空间（钩子类型、信息顺序、语境埋点位置）× 天级命中率回流的调优闭环：变体在会话外生成（不增加会话内决策量），命中率在账号内比较并回传参数权重——账号私有的实验循环。
  what_it_replaces: 替代同一句话反复发的碰运气式日更，以及陪跑服务里靠人的标题/结构 A/B 测试（成本高、样本慢）。
  why_big: 它是数据闭环（insight III）在内容层的落地形态——每个账号的命中率数据随使用增值、不可迁移，是切换成本与续费的核心壁垒；变体并行发布天然适配视频号值得转发的社交推荐。
  visualization: 会话内一条选题下方两三个结构卡片：版本 A 避坑清单式开头 / 版本 B 行业真相式开头，每版标注预测转发理由；次日数据页显示 A
    转发 12、B 转发 3，参数权重随之上调 A 类开头。
  design_principles:
  - 变体在会话外生成——会话内决策量不增加
  - 命中率按条归因——数据干净，不打混
  - 参数可解释——权重变化能说清为什么下次多给 A 类
  - 不为了实验而实验——变体差异必须来自语境/结构，不是换皮
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 同一个选题，用最可能被转发的结构发出去——内容命中率随账号数据自我调优。
        evidence_refs:
        - insight:ART-004@2:III
        - insight:ART-004@2:I
      consumer_target:
        statement: 已稳定日更、追求内容命中率的视频号创始人 IP。
        evidence_refs:
        - insight:ART-004@2:I
    money:
      commercial_value_proposition:
        statement: 账号私有结构参数模型随使用增值、不可迁移——切换成本与续费壁垒。
        evidence_refs:
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 作者自有结构方法论作为初始参数组合，账号数据持续校准。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 同日多版本并行发布稀释单条注意力、可能被关系链视为营销号刷内容——实验需求 vs 关系链信任。
    balance_choice: Magic 侧——先以单条更准证明价值，并行发布频次以不伤信任为上限。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 3/5 命中率差异检出性需账号数据验证
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5 并行发布伤信任+命中差异可能过小检不出
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-023@2
  decision: merged
  merge_into: CI-030
- id: CI-015
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-017
  parent_ids: []
  name: 生态风险监控仪
  pithy_description: 杀机雷达
  consumer_insight: 整条战略押注视频号×真人×copilot 的结构性空位（insight II），该位置依赖平台政策与接口现状（K-003）——一旦字节系能力进入视频号、发布
    API 开放或政策转向，押注的根基动摇；老板把日更押在这个平台上，也需要感知平台风向。
  commercial_insight: 单平台押注的已知代价是 kill signal 半触发（ART-005@2 C2 已签：balance Money 侧，接受平台押注风险，以
    RM-006 监控对冲）——监控本身是战略的风险管理组件，不是面向用户的独立卖点。
  idea_definition: 对视频号生态关键变量的常设监控：字节系能力进入信号、发布 API 开放动向、AI 标识/数字人政策变化、社交推荐机制调整——半触发式告警（达到阈值才动作），为产品方向与老板的押注提供提前量。
  who_its_for: 内部产品团队为主；对外面向重度依赖视频号平台的老板——以风险等级而非原始情报呈现。
  how_it_works: 机制=对少数关键信号（政策文本、接口开放、竞品动作）做低频结构化监控，触发阈值才升级告警并联动预案（如 API 开放后的自动化接管、政策转向后的内容策略切换）——半触发，不制造噪音。
  what_it_replaces: 替代人工盯平台公告、靠行业群消息的被动反应，以及老板对平台风险的裸奔式感知。
  why_big: 它是单平台押注战略的刹车与转向灯——不是增长引擎，但押注越大越需要；对老板的价值是平台风向的提前感知这一信任点。
  visualization: 内部仪表：三个信号灯（平台接口/政策/竞品），常态绿灯，任一信号触发阈值亮黄并附预案链接；老板侧仅收到季度级平台风向简报。
  design_principles:
  - 半触发——阈值内不打扰，触发才升级
  - 信号少而关键——只盯能改变押注判断的变量
  - 联动预案——告警必须带可执行动作，不制造焦虑
  - 内外分离——内部高频仪表，对外低频简报
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 把平台风向变成可感知的风险等级——老板知道自己押注的平台在什么位置。
        evidence_refs:
        - insight:ART-004@2:II
        - knowledge:K-003@1
      consumer_target:
        statement: 依赖视频号平台的重度创始人 IP 与内部产品团队。
        evidence_refs:
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 平台押注的风险对冲组件——降低单平台战略的尾部风险，本身不作为独立收费项。
        evidence_refs:
        - insight:ART-004@2:II
      leverageable_assets:
        statement: 政策文本监控与预案库作为合规管线（CI-013）的持续输入。
        evidence_refs:
        - insight:ART-004@2:II
    tension:
      statement: 监控的价值取决于检出后能否来得及调——若信号检出即已晚（如 API 突然开放），监控成本白付；监控强度 vs 对冲有效性。
    balance_choice: Money 侧——它是战略押注的风险管理成本，按最小必要强度运行，不因它膨胀产品。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: false
      pretest_altitude: false
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5 平台变化不可控，监控有效性存疑
      appeal: 2/5 安抚价值而非增长价值
      differentiation: 2/5 无竞品做，但正因为不是用户买点
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 2/5 无独立商业逻辑——是成本项
      altitude: 2/5 工具/能力而非命题
      healthy_anxiety: 3/5 单平台押注的焦虑真实，监控是对冲
    revision_attempts: 0
    recommended_action: merge
  assumption_refs:
  - assumption:A-024@2
  decision: merged
  merge_into: CI-029
- id: CI-016
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-018
  parent_ids: []
  name: 社交货币钩子库
  pithy_description: 转发钩子库
  consumer_insight: 视频号内容为转发而设计（F7），但什么开头值得被转发对自干派老板是不可复用的个人灵感（insight I）；按行业/人群沉淀的点赞理由钩子（避坑清单、行业真相、给同行的建议）解决第一条
    3 秒里给对方一个转发的理由。
  commercial_insight: 钩子库本身是易商品化的方法论组件（insight III 警告），单靠库不构成壁垒——壁垒在库×账号命中率回流：同一钩子在不同账号的表现数据按行业/人群私有化排序，越用越准；且社交货币特化正好站在战略砍除项（TikTok
    式模板库）的边界内侧。
  idea_definition: 按行业×人群×点赞理由分类的『值得转发』钩子资产库：每个钩子带适用语境与示例，随账号天级回流数据按命中率重排；库只服务『让第一条
    3 秒值得被转发』，不服务完播率。
  who_its_for: 已日更但开头不抓人、转发靠运气的视频号创始人 IP——需要现成可选的钩子而非方法论学习。
  how_it_works: 机制=分类资产库+命中率反馈排序：钩子按点赞理由分类组织（社交货币分类法），账号发布后的转发/点赞数据按钩子归因并重排库内排序——库是活的，排序是账号私有的。
  what_it_replaces: 替代个人收藏的爆款开头、抖音式黄金三秒模板库（被战略砍除）与陪跑里靠人传授的钩子经验。
  why_big: 钩子是每条内容的第一决策点，而值得转发的开头在视频号社交推荐机制下是分发杠杆（F7）；全行业钩子库都是算法逻辑（完播率导向），社交货币特化+私有命中率排序占住差异化位。
  visualization: 会话内选题确定后，钩子库按本账号历史命中率弹出 3 个候选开头：避坑清单式（你行业命中率 34%）——老板点选，示例展开为 3 秒口播稿。
  design_principles:
  - 按点赞理由分类，不按格式分类——防止滑向被砍的模板库
  - 命中率排序优先——库的排序是账号数据的产物
  - 钩子即承诺——开头承诺的东西必须在内容里兑现
  - 可解释——每个钩子标注为什么这条会被转发
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 3 秒开头直接给关系链一个转发的理由——开头不靠灵感，靠命中率排序过的资产库。
        evidence_refs:
        - knowledge:K-006@1
        - insight:ART-004@2:II
      consumer_target:
        statement: 已日更但开头转化差的视频号真人创始人 IP。
        evidence_refs:
        - insight:ART-004@2:I
    money:
      commercial_value_proposition:
        statement: 库×账号命中率数据构成私有资产——通用钩子人人可得，私有排序不可迁移。
        evidence_refs:
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 作者代运营经验中的社交货币钩子 know-how 作为库的初始分类与种子内容。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 钩子库一旦规模化商品化，就滑向战略明确砍掉的 TikTok 式模板库——社交货币特化 vs 通用模板化，边界极薄。
    balance_choice: Magic 侧——先证明点赞理由分类的钩子带来更高转发，用数据守住与模板库的边界。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5 依赖社交货币机制（未签）+钩子有效性无公开数据
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5 稍学术
      visualization: 4/5
      design_principles: 4/5
      money_magic: 3/5 库本身商品化风险 vs 私有排序资产
      altitude: 4/5
      healthy_anxiety: 2/5 与模板库边界极薄+insight III 商品化警告
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-025@2
  decision: null
  merge_into: null
- id: CI-017
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-019
  parent_ids: []
  name: 关系链冷启动
  pithy_description: 首百次转发
  consumer_insight: 新号冷启动在视频号社交推荐机制下（F7）依赖初始社交互动，但老板没有粉丝基础；他唯一现成的社交资产是多年经营的微信关系链（老客户、同行、员工、供应商）——冷启动不是算法赌博，而是把已有关系链动员起来（insight
    II：真人 IP 场的结构性位置，真人=老板本人可信）。
  commercial_insight: 冷启动是订阅的第一道坎——前 30 天没有信号，坚持装置（OA-001）与续费都无从谈起；把首 100 次转发做成可执行程序，等于把
    churn 风险最高的窗口期产品化，且动员中积累的转发命中数据直接进入数据闭环（insight III）。
  idea_definition: 面向老板微信关系链的首 100 次转发启动程序：前 N 条内容定向设计为关系链会转的形态（给老客户/同行/员工的具体内容），配合私域触点（朋友圈、群、1:1
    话术）逐条动员真实转发，撬动社交推荐引擎初始分发。
  who_its_for: 从零开始的视频号真人创始人 IP——有微信关系链但账号零粉丝、不知如何启动的老板。
  how_it_works: 机制=把冷启动从等待算法分发改为用老板已有社交图做种子：启动期内每条内容先回答这条给关系链里的谁、为什么他会转，再通过最小动员动作（发圈话术、1:1
    转发请求模板）把前 100 次真实转发做出来，命中数据回流校准后续选题。
  what_it_replaces: 替代买粉/互关/蹭热点的冷启动套路与发了等算法的被动策略，以及陪跑服务的涨粉承诺。
  why_big: 冷启动是视频号社交推荐模型的启动开关（F7 机制），而老板的微信关系链是别人拿不走、大厂工具够不到的资产（insight II）——把关系链动员产品化，是把结构性位置从内容层延伸到启动层。
  visualization: 启动期会话多一栏今日转发任务：目标对象『王总（老客户，做餐饮）』、内容『给他转这条《餐饮老板避坑清单》』、附言模板一句；进度条显示第
    47/100 次转发。
  design_principles:
  - 真实转发优先——只动员真实关系链，不做假量（平台风险）
  - 人情有预算——动员动作有额度上限，不消耗老板长期人情
  - 内容为人而做——启动期内容按关系链里具体的人设计
  - 命中即回流——每次转发的后续互动进入数据闭环
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 冷启动从赌算法变成动员老关系——老板用自己已有的信任资产启动账号。
        evidence_refs:
        - knowledge:K-006@1
        - knowledge:K-003@1
        - insight:ART-004@2:II
      consumer_target:
        statement: 零粉丝但有微信关系链的视频号创始人 IP。
        evidence_refs:
        - insight:ART-004@2:I
    money:
      commercial_value_proposition:
        statement: 冷启动窗口期是订阅 churn 最高风险段——把启动做成程序直接保护留存与续费。
        evidence_refs:
        - insight:ART-004@2:I
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 老板微信关系链本身作为不可替代的启动资产，产品提供动员设计。
        evidence_refs:
        - insight:ART-004@2:II
    tension:
      statement: 动员关系链转发消耗老板人情资本、密集转发可能被平台判定刷量——启动速度 vs 人情与合规风险。
    balance_choice: Magic 侧——先证明首 100 次真实转发能显著改变初始分发，人情消耗控制在可持续额度内。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 3/5 动员有效性无拆分数据
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 3/5 依赖社交货币机制+刷量误判风险
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-026@2
  decision: null
  merge_into: null
- id: CI-018
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-020
  parent_ids: []
  name: 原生格式适配
  pithy_description: 视频号原生
  consumer_insight: 视频号是沉浸式竖屏+评论互动+社交推荐（F7/K-003），与抖音的强钩子快节奏逻辑不同；自干派老板通常从抖音模板学格式（黄金三秒、快切、完播率导向），在视频号上系统性错配（insight
    II）。
  commercial_insight: 平台原生不是功能而是默认设计约束——它没有独立卖点，但所有内容概念的产出物都必须满足它；作为独立概念会与各内容概念重叠，作为
    CI-014 结构参数空间的组成部分则能被数据验证（insight III：组合调优才有壁垒）。
  idea_definition: 视频号原生格式规则集：竖屏沉浸构图、信息密度适配、评论互动设计——作为所有生成内容的格式约束，并作为结构变体 A/B 的参数维度被数据验证。
  who_its_for: 从抖音迁移过来、把视频号当第二个抖音发的创始人 IP——需要格式上的去抖音化。
  how_it_works: 机制=格式规则作为生成约束+实验参数：原生规则集（构图/密度/互动设计）内建到素材生成管线，同时作为 CI-014 结构实验的一个参数维度，用命中率数据验证哪些原生规则真实生效。
  what_it_replaces: 替代抖音式模板（黄金三秒快切、强钩子完播率结构）在视频号上的误用，以及一稿多发的跨平台迁就。
  why_big: 单独看是设计原则而非增长引擎（partial 判定成立）；但作为 CI-014 的参数维度，它是平台特化组合调优的一部分，是数据闭环验证的对象而非空洞原则。
  visualization: 生成预览统一为 9:16 沉浸竖屏，信息密度/互动位标注在时间轴上；会话内切换原生/抖音式对比预览，次日数据页显示原生版互动命中。
  design_principles:
  - 默认原生——格式约束内建，不提供抖音式选项
  - 规则可验证——每条原生规则都是 A/B 参数，不靠信仰
  - 沉浸不牺牲转发——原生格式同样服务于值得转发
  - 不做跨平台迁就——不为抖音逻辑保留格式分支
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每条内容生来就是视频号的样子——沉浸竖屏、评论可互动、为关系链而发。
        evidence_refs:
        - knowledge:K-003@1
        - knowledge:K-006@1
      consumer_target:
        statement: 从抖音迁移、需要去抖音化格式的视频号创始人 IP。
        evidence_refs:
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 作为 CI-014 结构参数维度被数据验证——平台特化组合调优是数据闭环资产的一部分。
        evidence_refs:
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 原生格式规则集作为生成管线的内建约束与实验参数库。
        evidence_refs:
        - insight:ART-004@2:II
        - insight:ART-004@2:III
    tension:
      statement: 原生格式一旦固化成规则模板，就可能滑向被战略砍除的模板库；而完全不做规则化又退化为空洞原则——规则化 vs 模板化。
    balance_choice: Magic 侧——以数据验证的原生参数而非固定模板落地，守住边界。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: false
      complete_blocks: true
      strategy_fit: false
      pretest_altitude: false
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5 平台原生=好但缺可证效果数据
      appeal: 2/5 无独立用户买点
      differentiation: 3/5 反抖音迁移定位清晰，但作为概念不独立成立
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 2/5 无独立商业逻辑
      altitude: 2/5 设计原则高度而非命题高度
      healthy_anxiety: 3/5 原生很容易变成信仰而非假设
    revision_attempts: 0
    recommended_action: merge
  assumption_refs:
  - assumption:A-027@2
  decision: merged
  merge_into: CI-030
- id: CI-019
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-023
  parent_ids: []
  name: 透明工作台
  pithy_description: 全流程透明
  consumer_insight: 被代运营/陪跑伤过的老板，痛感核心不是『没人干活』而是『看不见在干什么』——钱花在哪、内容怎么做、能不能改，全是黑箱（IV
    信任缺口）。他们要的不是更多服务，而是看清并掌控自己买的东西。
  commercial_insight: 透明不是功能而是服务替代的载体——当全流程每步可见可改，人工代运营的『信息差溢价』被结构性移除，订阅才站得住 ¥3000+
    档；同时流程产物本身沉淀为方法论×私有数据闭环的输入（III）。
  idea_definition: 把选题→文案→剪辑→发布的全流程拆成可见的流水线环节，每个环节的产物（选题清单、文案稿、剪辑稿、发布设置）随时可查看、可修改、可回滚，老板花
    30 分钟检查并拍板即可，彻底告别『交了钱只能看结果』的黑箱体验。
  who_its_for: 为 IP 付过大钱、被代运营/陪跑『黑箱交付』伤害过、仍在为内容结果持续付费的 SME 老板（OA-003 三层价位带上层）。
  how_it_works: 机制＝分步流水线透明化：每一环节的中间产物以可见对象呈现，任一环节可原地修改并向后联动重算，修改记录可回滚；所有可见性都服务于 30
    分钟会话内的『检查-拍板』节奏，而不是无限可配置。
  what_it_replaces: 取代代运营/陪跑的黑箱交付（只给成品、不给过程、不可干预），以及普通剪辑工具的单点工具形态。
  why_big: 信任崩塌后市场留下的缺口是『结果可控、自己握方向盘』的形态（IV）；全流程透明是这种形态的第一性体验——它把外包 IP 运营重构为『自己的生产线』，可服务全案客户降级下来的整个存量市场。
  visualization: 打开工作台是一根五段流水线（选题→文案→剪辑→发布→数据），每段下方挂着可展开的中间产物卡片；点开文案卡片直接改字，旁边立刻显示『已改
    2 处，下游剪辑稿待更新』，右上角一个『今天已检查 3/5 环节』的进度环。
  design_principles:
  - 透明优先于美观：中间产物以原始形态呈现，不做包装
  - 可改是承诺：每个可见对象都可改，不可改的环节必须明示原因
  - 30 分钟纪律：可见性服务拍板节奏，不为浏览设计无限层级
  - 回滚免惊扰：修改不丢历史，随时可退
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 全流程每步可见可改，老板第一次能看清自己买的内容生产线并随时干预。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 被代运营黑箱伤害、仍在为 IP 结果持续付费的 SME 老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 以透明工作台为载体支撑 ¥3000+/月服务替代订阅，信息差溢价被移除后仍以方法论×数据闭环留出毛利。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 每步可见的流程产物沉淀为方法论×私有数据闭环的输入，越用越准的部分成为资产。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 全流程透明可能带来『环节越多越要检查』的负担，与 30 分钟会话纪律冲突——透明如何不变成新的时间黑洞。
    balance_choice: 偏向 magic：透明是信任重建的第一性体验，效率负担由『默认可信＋按需检查』的设计消化。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 3/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-028@2
  decision: selected
  merge_into: null
- id: CI-020
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-024
  parent_ids: []
  name: 效果归因面板
  pithy_description: 归因到决策
  consumer_insight: 老板付大钱买 IP 结果却说不清『结果怎么来的、下次该改什么』——归因不可见让每次投入都像赌博（IV）。他们要的不是玄学建议，而是『这个结果是由我的哪个决策造成的』的可解释答案。
  commercial_insight: 归因面板把效果解释权从服务商手里夺回给用户，是服务替代的信任基础设施；归因数据本身是方法论×私有数据闭环的核心资产（III）——越用越准。
  idea_definition: 每条内容的流量结果被分解归因到具体决策维度（选题、结构、发布时间等），以可解释的归因视图呈现『这个结果主要来自哪个决策』，而不是黑箱评分或玄学总结；归因用于复盘下次选择，不用于承诺流量。
  who_its_for: 已为 IP 付过大钱、要求『钱花得明白』、会复盘数据但缺乏归因工具的中上层价位老板。
  how_it_works: 机制＝决策维度归因引擎：把单条内容的结果按预先定义的决策维度做可解释分解（哪一维贡献了主要差异），呈现『决策→结果』的对应关系；归因口径固定且可展开查看计算依据，杜绝玄学。
  what_it_replaces: 取代代运营的总结报告话术（只给结论不给因果）和老板自己拍脑袋的复盘；也取代只看单指标（播放/点赞）的浅层数据工具。
  why_big: 效果归因可见是『结果可控』的第二支柱（第一支柱是流程透明）——它把『赌服务商』变成『看得懂自己的决策系统』，是信任缺口（IV）上可规模化的解释层，构成订阅的长期留存理由。
  visualization: 数据页顶部是『最近 30 条内容』的散点，点开一条：一条横轴把播放结果拆成『选题贡献 52%、结构 30%、发布时间 12%、随机
    6%』，每段可点开看计算口径；旁边一行小字『归因用于复盘，不构成流量承诺』。
  design_principles:
  - 可解释优先于精确：归因必须能看懂，看不懂的归因不如不给
  - 口径固定透明：计算依据随时可查，杜绝黑箱算法
  - 复盘定位：归因服务于下一次选择，不做流量承诺
  - 随机性诚实：无法归因的部分如实标注随机
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每条内容的结果归因到具体决策，老板第一次能看懂『我的选择如何决定结果』。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 会复盘数据、要求钱花得明白的中上层价位老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 归因解释层构成订阅的长期留存理由，归因数据沉淀为越用越准的私有数据闭环资产。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 跨内容积累的『决策×结果』归因数据是方法论商品化的私有数据部分。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 单条短视频流量含大量外部随机性，归因的因果可信度天然有限——可解释的简化归因可能误导决策，如何在不承诺流量与给出有用因果之间取边界。
    balance_choice: 偏向 magic：归因以看得懂为先，宁可如实标注随机也不做精确但不可信的承诺。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 3/5
      credibility: 4/5
      appeal: 3/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 3/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-029@2
  decision: null
  merge_into: null
- id: CI-021
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-025
  parent_ids: []
  name: 服务替代订阅定价
  pithy_description: 服务替代锚
  consumer_insight: 老板对按人头、按月收 ¥1.5万 的代运营价格已麻木但心有不甘——他们接受为结果付钱，拒绝为黑箱付钱；一个对标全案但只收分数价、且按产出单位计价的价格结构，是把『我付得起也看得懂』还给老板。
  commercial_insight: 定价即叙事：锚定 ¥1.5万/月全案的分数档（¥3000+/月），配合单条边际成本 ¥1-10 的毛利结构，让 SaaS
    单位经济成立；服务替代锚定价同时天然过滤工具锚（¥50-800）的价格敏感客群，筛选出愿为结果可控付费的上层客群。
  idea_definition: 以代运营全案（¥1.5万/月）为价格锚、按产出单位（条/会话）计价的服务替代订阅档（¥3000+/月），把『我付的是结果可控与方向盘』而非『我买的是工具』讲成价格语言。
  who_its_for: 已为 IP 付过大钱、预算在 ¥3000-15000/月区间、被工具锚产品伤过（买了没用）的中上层价位老板。
  how_it_works: 机制＝服务替代锚定价：价格锚定对标服务的分数档，计价单位绑定可数产出（条/会话/月），并配价格档位说明『全案 ¥1.5万 vs 本档
    ¥3000+，省下的钱来自 AI 干程序化』；定价结构同时内置向上/向下的档位迁移路径。
  what_it_replaces: 取代 ¥1.5万/月全案＋服务商黑箱的代运营付费结构，也取代 ¥50-800 工具订阅的低价工具锚心智。
  why_big: 三层价位带的上层存在『付得起、被伤过、拒绝再赌』的存量市场（IV）；服务替代锚定价是唯一能把该客群付费意愿和 SaaS 毛利结构同时接住的定价形态，是独立
    SaaS 商业成立的前提。
  visualization: 定价页左侧竖排三档价格锚：『代运营全案 ¥15,000/月』打上斜线，右侧本档『¥3,980/月 · 约 30 条 · 含 30
    分钟会话』；下方一行自动算好的『单条成本 ¥1-10，你为结果可控和方向盘付费，不为人力时薪付费』。
  design_principles:
  - 锚定可见：价格页永远并排展示全案锚
  - 单位可数：计价绑定条/会话产出，不按时长
  - 档位清晰：向上/向下迁移路径明确，不设免费增值漏斗
  - 价格即叙事：每个价格点都回答贵在全案哪里、省在 AI 哪里
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 对标全案分数档、按产出单位计价的订阅，让『结果可控』有清晰的价格语言。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 预算 ¥3000-15000/月、被工具锚伤过的上层价位老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 服务替代锚订阅 ¥3000+/月，单条边际成本 ¥1-10、月成本 ¥30-300，毛利结构支撑独立 SaaS。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 服务替代锚定价本身是叙事资产，价格即差异化声明。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 定价锚定服务（¥3000+）与用户对软件工具的价格心智（¥50-800）之间隔着价值感知鸿沟——不靠流量承诺，靠什么让老板信服这个价差。
    balance_choice: 偏向 money：定价是商业成立的硬条件，magic 侧的价值感知由 CI-019/020/024 等概念供给。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 3/5
      appeal: 3/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-030@2
  decision: selected
  merge_into: null
- id: CI-022
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-026
  parent_ids: []
  name: 方向盘产品化
  pithy_description: 每步人拍板
  consumer_insight: 老板被托管伤过的核心是『方向盘被拿走』——不是不愿干活，而是不愿当甩手掌柜却背黑锅；他们要的是『每一关键步我自己拍板、AI
    只是备选』的控制感（IV）。
  commercial_insight: 『人做选择』是战略哲学的落点，也是与全托管服务商区分的结构性差异——AI 干程序化＋人拍板的形态同时保证低边际成本（AI
    备选）与高决策黏性（人的投入），形成留存飞轮。
  idea_definition: 把内容生产的关键节点结构化为『拍板会话』：每个节点 AI 只给出备选集与推荐理由，老板做唯一决策（选、改或弃），30 分钟内完成当日全部拍板——方向盘以界面形式产品化。
  who_its_for: 被代运营夺走控制权、明确拒绝全托管、愿意每天付出 30 分钟但不愿超过的 SME 老板。
  how_it_works: 机制＝结构化拍板协议：决策点被预先定义为有限集合（选题定夺、文案确认、发布设置确认等），每个决策点呈现『AI 备选 n 项＋每项理由＋默认推荐』，老板一拍即定；决策点数量与顺序固定，超出即触发会话超时保护。
  what_it_replaces: 取代全托管代运营（无人拍板）和从零创作（无备选、无结构）两种极端，把老板从干活的或甩手的变成拍板的。
  why_big: 『方向盘在老板手里』是锁定战略里唯一不可外包的价值主张；把它产品化为可复用的拍板协议，就是把这个主张变成可交付、可定价、可留存的界面——服务替代形态的灵魂机制。
  visualization: 手机端拍板界面：顶部『今日 7 个拍板点，剩 12 分钟』；第一个卡片『选题：AI 给了 5 个备选，各附一句理由』，老板左滑弃、右滑选、点开改；全部拍完出现『今日方向盘已握完』的动画。
  design_principles:
  - 决策点固定：拍板点数量与顺序可预期，不随内容浮动
  - AI 只备选：AI 永不替老板做决定，推荐必须有理由
  - 超时保护：30 分钟到点自动收束，防止选择疲劳
  - 拍板即记录：每次拍板自动进入留痕（联动 CI-028）
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每一关键步老板拍板、AI 只提供备选与理由，方向盘以界面形式回到手里。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 拒绝全托管、愿付 30 分钟/天换控制权的 SME 老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 人拍板＋AI 备选使边际成本保持极低（AI 干活），同时人的投入产生高黏性，支撑订阅留存。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 拍板协议本身是方法论商品化的载体，决策数据沉淀为私有数据闭环（III）。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 拍板点的粒度是双刃——决策点太少不像握方向盘，太多则拖垮 30 分钟纪律；『拍板感』与『会话时长』的最优平衡未解。
    balance_choice: 偏向 magic：先保证方向盘感真实，时长约束用超时保护兜底，再迭代粒度。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 4/5
      appeal: 5/5
      differentiation: 5/5
      naming: 4/5
      visualization: 5/5
      design_principles: 5/5
      money_magic: 3/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-031@2
  decision: null
  merge_into: null
- id: CI-023
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-027
  parent_ids: []
  name: 陪跑迁移包
  pithy_description: 代运营迁移
  consumer_insight: 大批老板正处在『对陪跑/代运营失望但不敢裸退』的状态——沉没成本、账号资产、内容节奏都在别人手里；他们要的不是又一个服务商，而是一条体面、无损的退出与接管路径（IV）。
  commercial_insight: 信任崩塌后的存量需求是现成的获客池——迁移包是进入机制而非功能，它把竞品的存量客户变成我们的新用户，且迁移过程中沉淀的账号数据直接成为私有数据闭环的种子。
  idea_definition: 一套从代运营/陪跑迁移过来的导入流程：账号权限接管、历史内容与数据导入、期望管理（明确『我们从基线开始、不承诺流量』）、前 30
    天过渡会话——让老板带着全部历史资产换到自握方向盘的新形态。
  who_its_for: 正在或刚退出代运营/陪跑、账号与内容资产还在服务商手里、犹豫『换船』成本的中上层价位老板。
  how_it_works: 机制＝存量迁移协议：分三步——资产导入（账号/内容/数据一键接管清单）、期望校准（用外部基线 K-006 重设预期，明确新形态的承诺边界）、过渡会话（前
    30 天每日会话由迁移模板驱动，逐步建立新节奏）。
  what_it_replaces: 取代『续费不划算、裸退又不敢』的两难——替代继续续约代运营的惯性行为，也替代老板自己 DIY 迁移的混乱过程。
  why_big: 代运营/陪跑行业持续制造受伤的存量用户（IV），迁移包把每个竞品的退订事件变成我们的获客事件——这是服务替代形态最顺滑的流量入口，且迁移者天然带着付费预算。
  visualization: 迁移页像一份搬家清单：第 1 步『账号接管：3 个平台、2 年内容、1.2 万粉丝数据已就位』，第 2 步『期望校准：你的账号基线将按
    K-006 外部基线建立』，第 3 步『第 1 天过渡会话已排好』，顶部一行『你的历史资产，一样不丢』。
  design_principles:
  - 无损迁移：历史内容/数据/账号权限完整接管，一样不丢
  - 期望先于承诺：迁移即重设预期，明确不承诺流量
  - 过渡有模板：前 30 天由迁移模板驱动，不要求老板立刻上手
  - 退出体面：不贬低原服务商，只展示你现在可以自己握方向盘
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 带着全部历史资产体面退出代运营，无损迁移到自握方向盘的新形态。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 对陪跑/代运营失望但不敢裸退、账号资产在服务商手里的老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 迁移包把竞品退订事件变成获客事件，迁移者自带付费预算，是低 CAC 的进入机制。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 迁移导入的历史账号数据成为方法论×私有数据闭环的种子数据。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 迁移做浅了接不住『体面退出』的期望，做深了滑向人工代运营交接（重人力、高成本）——迁移的自动化程度与服务化滑移的边界未解。
    balance_choice: 偏向 money：迁移包首先是获客机制，自动化边界以『不新增人工服务』为红线。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-032@2
  decision: null
  merge_into: null
- id: CI-024
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-028
  parent_ids: []
  name: 信任型 onboarding
  pithy_description: 基线先行
  consumer_insight: 受伤老板的付费门槛不是价格而是『又赌一次』的恐惧——他们需要先看到确定性的证据（这个方法论对别人的账号是什么基线），再决定是否把钱包交出来（IV）；付费前先给确定性，是信任重建的第一步。
  commercial_insight: 把确定性前置到付费之前，是把获客成本从销售说服转移到方法论证据——外部基线 K-006 是可复用、可规模化的信任资产，每多一个账号的基线数据，信任资产越厚（III
    数据闭环）。
  idea_definition: 前 30 天『结果基线』onboarding：注册后先展示方法论的外部基线（K-006：同规模账号在坚持＋方向纪律下的典型结果分布），再用
    30 天建立『你这个账号的基线』；承诺一律基于基线区间表达（在你的基线上方改善），而非绝对流量数字。
  who_its_for: 对『再交钱给任何服务』都警惕、需要先被证明再付费的犹豫型老板（OA-003 上层的典型心理状态）。
  how_it_works: 机制＝基线校准承诺：外部基线先行（K-006 数据公开可查）→ 个人基线建立（30 天会话采集本账号数据）→ 承诺客体锚定基线区间；所有对外表述都引用基线区间而非单点结果，从结构上杜绝流量承诺。
  what_it_replaces: 取代先吹结果再收钱的传统销售话术（陪跑/代运营的成交惯例），也取代免费试用功能的工具式 onboarding（免费增值漏斗被砍后需要新的确定性入口）。
  why_big: 信任缺口（IV）决定获客的关键不是流量而是确定性证据；基线先行把『敢不敢信』变成『数据说话』，是可规模化的信任引擎——每多一个账号，基线样本与说服力同时增长。
  visualization: onboarding 第三天晚上，老板收到一张图：『外部基线（K-006）：同规模账号 30 天坚持率的典型分布』；第 30 天换成『你的基线已建立，和外部基线对比在这里』；全程没有一句绝对流量承诺，只有区间与对比。
  design_principles:
  - 证据先于承诺：任何承诺都引用基线区间
  - 30 天纪律内建：基线期就是每日会话的磨合期
  - 不承诺流量：表述结构上只能出现区间与对比
  - 确定性可带走：基线报告是老板自己的资产，离开也带走
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 付费前先用外部基线＋30 天个人基线给出确定性，把『又赌一次』变成『数据说话』。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 对任何服务都警惕、需要先被证明的犹豫型老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 获客从销售说服转向方法论证据，基线数据随账号增长而增厚，降低 CAC 并强化定价底气。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: K-006 外部基线＋个人基线样本构成可复用的信任资产与数据闭环。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 30 天基线期意味着付费后置、现金流后移，且基线期若被当作免费期消耗，转化路径会被拉长——确定性供给与商业化节奏的平衡未解。
    balance_choice: 偏向 magic：信任重建优先，商业化节奏靠『基线期即高价值磨合』的设计对冲。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 5/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 5/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-033@2
  decision: null
  merge_into: null
- id: CI-025
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-029
  parent_ids: []
  name: 月成本透明账单
  pithy_description: 月成本可见
  consumer_insight: 老板对代运营账单的怨气不仅是贵，更是『钱去哪了说不清』——一笔 ¥1.5万 的月费背后是看不见的人力成本；一张把单条成本摊到
    ¥1-10、月成本摊到 ¥30-300 的透明账单，把『我为什么只该付这些』讲清楚。
  commercial_insight: 成本透明是服务替代定价（CI-021）的可信度底座——低单位成本不是廉价信号而是 AI 杠杆的证据；同时透明账单反向约束内部成本结构，形成『必须保持单条成本
    ¥1-10』的组织纪律。
  idea_definition: 每月一张成本可视化账单：单条内容成本（¥1-10）、月度总成本（¥30-300）、每项成本构成（AI 算力/会话时间/存储），与代运营人力成本的并排对照——用数字证明『AI
    干程序化＋人做选择』的成本结构。
  who_its_for: 对价格敏感但拒绝廉价工具、想确认订阅费到底买了什么的上层价位老板。
  how_it_works: 机制＝成本核算可视化：系统按实际用量实时核算单条/月成本并分项展示，账单页同时并排展示对标人力成本估算；成本数字随用量实时变化，老板能看到每一分钱对应的产出。
  what_it_replaces: 取代代运营一口价/按人头的模糊账单，也取代工具订阅只收钱不解释成本的沉默定价。
  why_big: 透明账单把『便宜』重新定义为『AI 杠杆』而非『低价值』，是服务替代叙事里最有说服力的数字证据；它同时是组织内部成本纪律的仪表盘——商业可信度与运营效率双收。
  visualization: 月底账单页：大数字『本月 31 条 × 均 ¥2.3 ＝ ¥71.3』；下方拆成三段『AI 算力 ¥38 · 会话时长 ¥21 ·
    存储 ¥12』，最下面一行灰字『对照：同类全案代运营人力成本估算 ¥15,000』。
  design_principles:
  - 数字即证据：成本数字实时核算，不造假不估算
  - 对照常驻：永远并排展示人力成本对照
  - 分项可查：每项成本可点开看构成
  - 成本即纪律：账单反过来约束内部成本结构
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 单条 ¥1-10、月成本 ¥30-300 的透明账单，让老板看懂每一分钱买了什么。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 想确认订阅费买什么、拒绝模糊账单的上层价位老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 成本透明为 ¥3000+ 订阅提供可信度底座，同时账单约束内部单条成本纪律，毛利结构自我强化。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 实时成本核算数据是定价与叙事的可信资产。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 把成本亮到 ¥30-300/月可能反噬价值感知——『这么便宜是不是不值 ¥3000』；低成本数字如何被解读为杠杆而非廉价，是未解张力。
    balance_choice: 偏向 magic：透明是信任的硬承诺，价值感知由对照叙事（CI-026）与结果可见（CI-020）托底。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 4/5
      appeal: 3/5
      differentiation: 4/5
      naming: 4/5
      visualization: 5/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-034@2
  decision: null
  merge_into: null
- id: CI-026
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-031
  parent_ids: []
  name: 全案对比工具
  pithy_description: 全案对比器
  consumer_insight: 受伤老板在决策时真正在比较的是『再赌一次代运营 vs 试试这个新东西』——他们需要一个可信的对比框架，把价格、控制权、透明度这些维度摆在同一张桌上（IV）；对比不是营销话术而是决策工具。
  commercial_insight: 对比工具是服务替代定价（CI-021）的叙事武器——它把『¥1.5万 vs ¥3000+』的价差从广告语变成用户自己算出来的结论；且对比维度（价格/控制权/透明度）都可验证，不依赖流量承诺，规避
    Charter 风险。
  idea_definition: 一个与代运营全案（¥1.5万/月）的 ROI 对比器：输入自己的账号规模与内容目标，从价格、控制权、透明度、可退出性等可验证维度生成『全案
    vs 订阅』对比报告；对比只使用可验证事实维度，不含预测流量。
  who_its_for: 正处在『续约代运营 or 换形态』决策点、需要理性对比框架来下决心的上层价位老板。
  how_it_works: 机制＝对比叙事生成器：基于可验证维度（价格、决策权归属、流程可见性、迁移成本）的固定对比模板，输入账号参数后生成个性化对比报告；维度全部可验证，预测类维度（流量/涨粉）被结构性地排除在外。
  what_it_replaces: 取代凭感觉比价的决策方式和代运营的销售对比话术（口头贬低竞品）；把对比从口头叙事变成可保存、可转发的决策文件。
  why_big: 对比工具是获客临门一脚的标准化武器——它把服务替代的商业逻辑压缩成一个用户自己算出来的结论，转化效率高且叙事可复制；同时它是『不承诺流量』边界下的少数合规说服手段。
  visualization: 输入『月发 30 条、粉丝 5 万』后生成双栏报告：左栏『代运营全案 ¥15,000/月：决策权-服务商、流程-黑箱、退出-困难』；右栏『本订阅
    ¥3,980/月：决策权-你、流程-全透明、退出-随时』；底部一行『本报告不包含任何流量预测』。
  design_principles:
  - 只比可验证：对比维度全部可验证，排除预测
  - 用户自己算：结论由用户输入生成，不是广告文案
  - 边界内建：报告结构上排除流量/涨粉承诺
  - 可带走：对比报告是用户资产，可保存可转发
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 一个可验证的对比框架，把『再赌代运营还是换形态』变成用户自己算出的理性结论。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 处于续约/换形态决策点、需要理性框架的老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 对比器把服务替代价差变成用户自算结论，标准化获客叙事，降低转化成本。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 对比模板与维度库是方法论商品化的可复制部分。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 对比工具若引入『省下的钱能买多少结果』之类的换算，就悄悄滑向结果/流量暗示——可验证维度与说服力之间的边界未解。
    balance_choice: 偏向 money：对比器是销售武器，说服力必须始终锚定可验证维度。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 5/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 5/5
      design_principles: 5/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-035@2
  decision: null
  merge_into: null
- id: CI-027
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-032
  parent_ids: []
  name: 退款承诺机制
  pithy_description: 过程可退
  consumer_insight: 受伤老板的最后一道心理防线是『万一又赌输了呢』——退款条款是信任重建的硬机制，它把『风险由用户承担』翻转成『风险由我们承担一部分』（IV）；但老板真正需要的是『可退』背后的确定性逻辑，而非一句营销口号。
  commercial_insight: 退款承诺是有成本的信任信号——它把『我们相信自己交付了什么』变成可验证的承诺；关键是把承诺客体设计在我们可完全控制的对象上（过程/交付/参与支持），使退款率可预测、可管理，而不是赌不可控的流量结果。
  idea_definition: 一套退款条款设计：承诺客体锚定『我们可控的交付』（每日会话素材完整交付、每步可改可回放、30 天会话纪律支持），而非流量/结果；若我方交付未达标，按比例退款——用条款结构把『不承诺流量』与『敢退款』同时立住。
  who_its_for: 处于『想信但不敢再赌』状态、退款条款是最后决策变量的犹豫型老板。
  how_it_works: 机制＝承诺客体设计：把可承诺对象限定在我方完全可控的交付项（交付完整率、会话支持、素材质量通过检查清单），退款条件绑定这些可验证交付项；不可控对象（流量、涨粉、转化）在条款中显式排除，并写明本产品不承诺流量。
  what_it_replaces: 取代代运营口头承诺结果、出事推诿的隐性风险转移，也取代先款后货、无任何保障的行业惯例。
  why_big: 退款条款是把信任重建从口号变成合同的唯一硬机制（IV）——在信任缺口市场上，『敢退款』本身是稀缺信号；且承诺客体限定在可控交付上，使该机制可规模化而不被退款率击穿。
  visualization: 签约页的退款条款以承诺清单呈现：绿勾项『每日素材交付完整率 ≥ 98%』『每一步可改可回放』；灰字项『本产品不承诺播放量、涨粉、转化等外部结果』；旁边一行小字『退款条件：我方交付未达标，按未达标比例退还』。
  design_principles:
  - 客体可控：只承诺我方完全可控的交付项
  - 排除显式：流量/结果类承诺在条款中显式排除
  - 条件可验证：退款条件绑定可核验的交付记录
  - 比例而非全退：按未达标比例退款，避免滥用
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 退款条款把『风险由用户承担』翻转成『交付未达标可退』，信任重建有了合同级硬机制。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 想信但不敢再赌、退款条款是最后决策变量的老板。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 承诺客体限定可控交付使退款率可预测，信任信号成本可控；敢退款是稀缺获客信号。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 交付记录系统（与 CI-028 决策留痕联动）成为退款核验的可信基础设施。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 退款机制的原生形态是结果承诺——若承诺客体滑向流量/结果，将直接违反 Charter『不承诺流量』；承诺客体如何始终钉在可控交付上，是未解且必须守住的边界。
    balance_choice: 偏向 magic：退款是信任机制，但设计上以『可控交付客体』守住 money 侧不崩（退款率可控）。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 5/5
      appeal: 4/5
      differentiation: 4/5
      naming: 3/5
      visualization: 4/5
      design_principles: 5/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 5/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-036@2
  decision: null
  merge_into: null
- id: CI-028
  item_revision: 1
  opportunity_area_id: OA-003
  source_seed_id: CS-033
  parent_ids: []
  name: 决策留痕
  pithy_description: 决策可回放
  consumer_insight: 老板要的不仅是『这次选得对』，更是『我在变好』的掌控感证据——把每次会话的选择记录下来并与结果关联，『我做过什么选择→结果如何』的回放能力把控制感变成可积累的长期资产（IV）。
  commercial_insight: 决策留痕是『方法论×私有数据闭环』（III）的用户侧形态——每次拍板都是私有数据的一行，回放界面让用户看见数据在积累，形成『越用越准、越用越离不开』的留存飞轮。
  idea_definition: 每次选择会话的决策被自动记录成可回放的时间线：我选了哪个选题、改了哪句文案、几点发布，并在后续与结果数据关联；老板随时回放『我的决策史』，看到自己的判断如何随时间演变、与结果如何对应。
  who_its_for: 愿意为掌控感长期付费、看重复盘与自我提升的深度用户（留存型客群，非首次转化客群）。
  how_it_works: 机制＝决策时间线回放：每次拍板自动生成带时间戳的决策记录，按会话/周/月组织成可回放的时间线，并与结果数据（CI-020 归因）关联；回放是只读的、自动的，不增加会话负担。
  what_it_replaces: 取代老板自己记笔记/凭记忆复盘的习惯，也取代代运营成果汇报式的外部记录（那是服务商的历史，不是老板的决策史）。
  why_big: 留痕把方向盘从一次性的功能变成可积累的资产——资产越厚，迁移成本越高，留存越强；它是数据闭环（III）的用户可见形态，是『越用越准』叙事的直接证据。
  visualization: 『我的决策史』时间线：3 月 3 日『选了选题 C（结构类）→ 发布 18:00』，3 月 10 日『改了 2 句文案 → 发布
    12:00』，每条末端挂着结果标签『该条归因：选题贡献 52%』；顶部『你已累计 214 次拍板，决策风格正在形成』。
  design_principles:
  - 自动留痕：记录零操作成本，不打断会话
  - 只读回放：历史不可篡改，回放即证据
  - 结果关联：每条决策与后续归因结果挂钩
  - 资产归属：决策史是老板的资产，离开可带走
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 每次选择自动留痕、可回放、与结果关联，『我做过什么选择→结果如何』成为可积累的掌控感资产。
        evidence_refs:
        - artifact:ART-004@2
      consumer_target:
        statement: 看重复盘与自我提升、愿为掌控感长期付费的深度用户。
        evidence_refs:
        - artifact:ART-004@2
    money:
      commercial_value_proposition:
        statement: 决策时间线是私有数据闭环的用户可见形态，资产越厚留存越强、迁移成本越高。
        evidence_refs:
        - artifact:ART-004@2
      leverageable_assets:
        statement: 每次拍板沉淀为私有数据的一行，『越用越准』由用户亲眼可见。
        evidence_refs:
        - artifact:ART-004@2
    tension:
      statement: 留痕的长期价值依赖结果关联（CI-020 归因）成立——若归因不可信，留痕退化为日记；留痕的独立价值与对归因的依赖关系未解。
    balance_choice: 偏向 magic：留痕首先服务掌控感（无需归因也成立），结果关联作为增值层渐进接入。
  evaluation:
    hard:
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft:
      comprehension: 4/5
      credibility: 4/5
      appeal: 4/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 5/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-037@2
  decision: null
  merge_into: null
- id: CI-029
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-015
  parent_ids:
  - CI-013
  - CI-015
  name: 合规与生态护栏
  pithy_description: 护栏雷达
  consumer_insight: 老板既怕违规封号也怕平台变天——合规红线（AI 标识强制、数字人压制）与生态风向（发布 API、字节系进入）都是押注视频号的致命外部变量，单靠个人盯不动（insight
    II；K-003）。
  commercial_insight: 政策壁垒的产品化＋单平台押注的风险对冲：护栏独占真人 IP 场入口（大厂工具跨不进、通用工具不管合规），雷达是 C2 已签接受的押注风险对冲组件；两者共享同一套政策文本监控与规则库。
  idea_definition: 合规作为产品内强制管线（AI 标识内建、数字人/非真人检测拦截、人点发布三闸口）＋生态关键变量半触发监控（字节系能力进入/发布
    API 开放/政策转向）——护栏让老板每一步都在安全区，雷达为押注提供提前量；监控输出直接驱动护栏规则更新。
  who_its_for: 真人出镜、怕违规怕封号、不想研究平台规则的视频号创始人 IP；以及依赖视频号平台、需要风险感知的重度用户。
  how_it_works: 机制＝合规管线约束＋低频信号监控的双层护栏：三闸口把违规动作在管线内物理拦截；少数关键信号阈值触发告警并联动预案（API 开放→自动化接管、政策转向→内容策略切换）；半触发，不制造噪音。
  what_it_replaces: 替代裸奔式自剪自发的违规风险、数字人工具（已违规风险）、RPA 全自动发布（运营规范风险）；替代人工盯公告、靠行业群消息的被动平台风险感知。
  why_big: 合规是视频号的结构性闸口（K-003），护栏独占真人 IP 场入口且随政策收紧而增值；雷达保护整个单平台押注的尾部——入口价值与风险保护合为平台押注的完整风控面。
  visualization: 发布前预览页绿色横幅『已含 AI 标识 ✓ 真人检测通过 ✓ 待你确认发布』；内部信号灯仪表（接口/政策/竞品三灯），常态绿灯，任一触发阈值亮黄并附预案链接。
  design_principles:
  - 合规内建而非提醒——违规动作在管线里被物理拦截
  - 半触发——阈值内不打扰，触发才升级
  - 监控联动预案——告警必须带可执行动作
  - 人点发布不可绕过——发布闸门永远是真人
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 老板在不可能违规的护栏里做内容、平台风向以风险等级可感知——合规与生态都不是他的知识负担。
        evidence_refs:
        - insight:ART-004@2:II
      consumer_target:
        statement: 真人出镜、怕违规怕封号、依赖视频号平台的重度创始人 IP。
        evidence_refs:
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 政策壁垒的产品化独占真人 IP 场入口，同时降低单平台押注的尾部风险——护栏与雷达构成平台押注的完整风控面。
        evidence_refs:
        - insight:ART-004@2:II
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 政策文本监控与合规规则库作为持续更新的私有 know-how，监控输出即护栏规则更新源。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 护栏摩擦（人点发布、标识检查）与雷达运行成本 vs 30 分钟会话顺畅与产品克制——兜底强度与用户体验的平衡未解。
    balance_choice: magic 侧——护栏零负担优先（摩擦被会话设计吸收），雷达按最小必要强度运行，不因风控膨胀产品。
  evaluation:
    hard: &id001
      lineage: true
      tension: true
      distinct_mechanism: true
      complete_blocks: true
      strategy_fit: true
      pretest_altitude: true
      concept_assumptions: true
    soft: &id002
      comprehension: 4/5
      credibility: 4/5
      appeal: 3/5
      differentiation: 4/5
      naming: 4/5
      visualization: 4/5
      design_principles: 4/5
      money_magic: 4/5
      altitude: 4/5
      healthy_anxiety: 4/5
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-038@2
  decision: null
  merge_into: null
- id: CI-030
  item_revision: 1
  opportunity_area_id: OA-002
  source_seed_id: CS-016
  parent_ids:
  - CI-014
  - CI-018
  name: 原生结构变体实验
  pithy_description: 原生结构实验
  consumer_insight: 同一选题怎么说决定成败，但自干派老板没有余力多版本试错（单条 3-8 小时，insight I）；且视频号原生格式（沉浸竖屏/评论互动/社交推荐）与抖音快节奏错配（insight
    II）——发得准需要结构实验，实验必须在原生格式约束下做。
  commercial_insight: 结构参数空间×天级命中率回流构成账号私有内容参数模型（insight III）——越用越准、不可迁移，是切换成本与续费壁垒；原生格式作为参数维度被数据验证而非信仰，守住与战略砍除项（模板库）的边界。
  idea_definition: 同一选题由会话外生成多个结构变体（钩子/信息顺序/语境埋点），老板会话内选 1-2 发布；原生格式规则（竖屏沉浸构图、信息密度、评论互动设计）内建为生成约束并作为变体的参数维度；天级命中率回流校准参数权重——账号私有的原生实验循环。
  who_its_for: 已稳定日更、想从『发了』进阶到『发得准』、且从抖音迁移需要去抖音化格式的视频号创始人 IP。
  how_it_works: 机制＝结构参数空间×天级命中率回流实验闭环：变体在会话外生成（不增加会话内决策量），原生规则作为参数维度参与变体差异生成，命中率按条归因回传权重——每条原生规则都是可验证的
    A/B 参数。
  what_it_replaces: 替代同一句话反复发的碰运气式日更、陪跑服务的人肉标题/结构 A/B 测试、以及抖音式格式模板（黄金三秒/快切）在视频号的系统性误用。
  why_big: 数据闭环（insight III）在内容层的落地形态——账号私有参数模型随使用增值、不可迁移；原生特化让实验始终站在模板库边界内侧，是平台特化组合调优的唯一可防御形态。
  visualization: 会话内选题下方结构卡片：版本 A 避坑清单式开头 / 版本 B 行业真相式开头，均为原生竖屏预览并标注预测转发理由；次日数据页 A
    转发 12 vs B 3，参数权重上调 A 类，原生规则命中与否随参数回显。
  design_principles:
  - 变体在会话外生成——会话内决策量不增加
  - 命中率按条归因——数据干净，不打混
  - 原生规则可验证——每条规则都是 A/B 参数，不靠信仰
  - 不为实验而实验——变体差异必须来自语境/结构
  dual_sided:
    magic:
      consumer_value_proposition:
        statement: 同一个选题，用最可能被转发的原生结构发出去——内容命中率随账号数据自我调优，且生来就是视频号的样子。
        evidence_refs:
        - insight:ART-004@2:II
      consumer_target:
        statement: 已稳定日更、追求内容命中率、需要去抖音化格式的视频号创始人 IP。
        evidence_refs:
        - insight:ART-004@2:II
    money:
      commercial_value_proposition:
        statement: 账号私有结构参数模型随使用增值、不可迁移——切换成本与续费壁垒；原生参数化守住与模板库的边界。
        evidence_refs:
        - insight:ART-004@2:II
        - insight:ART-004@2:III
      leverageable_assets:
        statement: 原生格式规则集作为生成管线的内建约束与实验参数库，命中率数据持续校准参数权重。
        evidence_refs:
        - insight:ART-004@2:III
    tension:
      statement: 多版本并行发布稀释单条注意力、可能被关系链视为营销号刷内容，且原生规则一旦固化就滑向被战略砍除的模板库——实验需求、关系链信任与战略边界的三角张力未解。
    balance_choice: magic 侧——并行频次以不伤信任为上限，规则以数据验证落地而非固定模板。
  evaluation:
    hard: *id001
    soft: *id002
    revision_attempts: 0
    recommended_action: refine
  assumption_refs:
  - assumption:A-039@2
  decision: null
  merge_into: null
decisions:
- type: select
  concept_ids:
  - CI-001
  - CI-010
  - CI-019
  - CI-021
  decided_by:
    name: 秋南Dylan
    role: product-owner
    type: human
  decided_at: '2026-08-17T08:45:00Z'
- type: merge
  concept_ids:
  - CI-013
  - CI-015
  decided_by:
    name: 秋南Dylan
    role: product-owner
    type: human
  decided_at: '2026-08-17T08:45:00Z'
- type: merge
  concept_ids:
  - CI-014
  - CI-018
  decided_by:
    name: 秋南Dylan
    role: product-owner
    type: human
  decided_at: '2026-08-17T08:45:00Z'
- type: split
  concept_ids:
  - CI-005
  decided_by:
    name: 秋南Dylan
    role: product-owner
    type: human
  decided_at: '2026-08-17T08:45:00Z'
exit:
  selected_concept_ids:
  - CI-001
  - CI-010
  - CI-019
  - CI-021
hash: e395ae625817300d55ff3c0d89b96329509f1d59d053562e0e43bf873c6b5917
supersedes_ref: artifact:ART-009@1
artifact_id: ART-009
kind: concept-portfolio
stage: ideate
revision: 2
document_status: final
validation_status: unvalidated
branch_id: BR-001
locked: false
signoffs: []
derived_from: []
last_validated_against: []
---
# Concept Portfolio r1 · 创始人 IP 短视频放大器

由 Idea Pool `artifact:ART-008@2`（28 条人工确认种子）发展的 28 个 Concept Items（CI-001..CI-028），
锁定战略 `artifact:ART-006@2`，机会组合 `artifact:ART-007@1`。每条概念携带双面命题、硬/软评估、一条可证伪的 Concept 假设
（ledger A-010..A-037，layer: concept，source_concept_id 校验）。

## 推荐动作分布（AI 建议，等待人工决策）

- **refine**：24 条（CI-001..014, 016..017, 019..028）
- **split**：CI-005（内部捆绑『契约约束』与『连续性反馈』两个可分离机制）
- **merge**：CI-015（生态风险监控仪 → 并入 CI-013 真人合规工作流）、CI-018（原生格式适配 → 并入 CI-014 结构变体 A/B）

## 诚实标注的硬标准缺口（AI 自评，非阻塞）

- CI-015：`strategy_fit: false`（风险对冲配套而非用户功能）、`pretest_altitude: false`（能力而非命题）→ 推荐 merge
- CI-018：`distinct_mechanism: false`、`strategy_fit: false`、`pretest_altitude: false`（设计原则而非独立机制）→ 推荐 merge
- OA-002 的 CI-010/011/016/017 依赖未签的 insight 5（社交货币机制）——已作为开放假设显式标注在 Concept 假设与 healthy_anxiety

## 人工决策（本修订未做，等待）

- 每个 Concept 的 `selected / killed / merged`（AI 只能推荐，不能填）
- 合并若被接受：CI-015 → CI-013、CI-018 → CI-014 创建新 CI 携带双 parent
- 最终 `exit.selected_concept_ids` 2–4 条 → 移交 bw-shape


## 人工决策记录（r2 · 2026-08-17 · 秋南Dylan product-owner）

- **selected（4，进入 Shape）**：CI-001 30分钟选择会话 · CI-010 转发值选题引擎 · CI-019 透明工作台 · CI-021 服务替代订阅定价
- **merge**：CI-013 + CI-015 → **CI-029 合规与生态护栏**（双 parent，父项不删除）；CI-014 + CI-018 → **CI-030 原生结构变体实验**
- **split（接受推荐，非终态字段）**：CI-005 坚持链与契约——streak 可视化与契约约束按两个可分离机制对待，Shape 阶段分别承接
- 未选概念（decision: null）保留于组合，可作未来回溯/扩展资源
- **Ideate → Shape 移交**：exact portfolio 修订 `artifact:ART-009@2`，2–4 条 selected 满足就绪检查
