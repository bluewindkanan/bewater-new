---
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: charter
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition:
      statement: "让企业创始人从「选题 + 策划 + 剪辑 + 运营发布」的短视频全流程时间与体力消耗中解放出来——录完即走，AI Agent 把短视频 IP 全流程搞定，创始人只做思考与出镜。"
      evidence_refs: []
    consumer_target:
      statement: "时间极度稀缺、又必须靠个人短视频 IP 获取品牌与流量的企业创始人；第一阶段就是工具作者自己（同时是 IP 创作者与代运营老兵，要求高、时间最稀缺），验证后再外溢给科技/传统企业创始人。"
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: "订阅 + 算力额度 + 增值服务三层收入；本地桌面部署让用户自担 GPU 算力、省去云端 GPU 成本；先自用做成案例（产品即营销），再向 T2 传统企业老板（利润主力）规模化。"
      evidence_refs: []
    leverageable_assets:
      statement: "创始人即用户（dogfooding 天然成立）+ 真实代运营服务沉淀的 know-how（业务认知差）+ 端到端产品力——功能可抄，认知不可抄。"
      evidence_refs: []
  tension:
    statement: "「让创始人只思考 + 出镜」的极致省事（Magic）与「创始人对质感 / 控制权的高要求」（制约全自动）相互拉扯——画布已用「审核后手动发布」「人机协作把控质量」做妥协；同时 self-first 先押效率 / 时间，但质感是 dogfooding 最敏感的信号，二者需平衡。"
  balance_choice: "起点押 self-first：先用作者自己验证「全流程串起来真省时间」（北极星 = 周均成片发布数），质感作为 dogfooding 敏感信号保留校验，验证通过后再外溢 T1/T2。"
derived_from: []
signoffs: []
stale_reason: null
---

### Intent trace

| Claim | Provenance | Basis / exact user context | Calibration status |
|---|---|---|---|
| 做创始人 IP 短视频 Agent，帮企业创始人做短视频以获得品牌和流量 | user-stated | 首句：「我要做创始人 IP 短视频 agent，用来帮这些企业创始人做短视频，从而获得品牌和流量」 | not-required |
| 作者自己就是 IP 创作者，且做过创始人代运营服务，痛点是实践中真实遇到的 | user-stated | 「本身就做过类似的代运营服务，同时我自己也在做 IP」 | not-required |
| 自己作为创始人没时间做选题/策划/剪辑/运营发布全流程，是第一痛点 | user-stated | 「作为一个创始人，你有没有时间…要做选题，要做策划，要剪辑，还要运营发布…但是我没时间」 | not-required |
| 想把原来偏人工、单点/单一交付的服务用 AI 标准化（语音"单云"推断为"单点"，未纠正） | user-stated | 「把原来偏人工服务…用 AI 做标准」 | not-required |
| 起点选 self-first：先自用、产品即案例、再外溢 T1/T2 | user-selected | 结构化选择中用户选定 | unchanged |
| 第一赌注押「全流程串起来真省时间」，北极星 = 周均成片发布数 | user-selected | 结构化选择中用户选定 | unchanged |
| founder 即用户 + 代运营 know-how = 真护城河，dogfooding 天然成立 | agent-interpretation | 由用户陈述与画布「不公平优势」综合推断 | unchanged |

### Original intent

- **User's own words:** 「我要做创始人 IP 短视频 agent，用来帮这些企业创始人做短视频，从而获得品牌和流量。」「作为一个创始人，你有没有时间去短视频啊……但是我没时间。」「想把原来偏人工服务用 AI 做标准。」
- **Trigger / why now:** 作者自己既是企业创始人、又是 IP 创作者，亲历选题/策划/剪辑/运营发布全流程的时间饥荒（每天 1–2 小时剪辑不可持续）；同时在运营代运营服务时积累了真实 know-how，想把人工、单点交付的服务用 AI 标准化、规模化——服务业务触到人工交付天花板，Agent 是杠杆。
- **Desired change:** 创始人不再被短视频全流程吞没时间——「录完即走」，只做思考与出镜，其余交给 AI Agent。

### Project definition

- **Challenge:** 企业创始人越来越依赖短视频个人 IP 获取品牌与流量，但全流程（选题文案 → 视频剪辑 → 运营分发）极度消耗时间；现有工具（剪映 / Descript / Opus Clip）只是「更好的锤子」，外包则效果失控、反复沟通比自剪还累。难点在于：如何让创始人「录完即走」、把全流程交给 AI Agent，同时不失质感与控制权。第一阶段以工具作者自己为第一个用户来验证。
- **Intent and outcome:** 做一个本地桌面 + 微信远程控制的「创始人 IP 短视频全流程 Agent」，覆盖选题文案、视频剪辑（核心）、运营分发三段；先用作者自己验证「全流程串起来真省时间」（每周稳定成片），产品即案例，再外溢给 T1 科技创始人 / T2 传统企业老板。
- **Target and situation:** 第一阶段 = 作者本人（既是创始人、又是 IP 创作者、还做过代运营，要求高、时间最稀缺）；后续 = 科技公司创始人（T1，品牌标杆，如追觅俞浩这类）与传统企业老板（T2，利润主力、基数大付费强）；个人 IP / 自媒体 / 投资人 / 知识 IP（T3）自然溢出。
- **Current behavior and alternatives:** 今天创始人自己硬剪（剪映等，1–2h/天不可持续）或外包给剪辑师（剪不出想要的质感、反复修改比直接剪还累）；工具仍是「锤子非木匠」——需坐在电脑前操作、学界面、手调细节。
- **Provisional solution hypothesis:** 本地桌面 Agent + 微信远程控制；创始人只思考 + 出镜，AI 做选题文案（画像/热点选题/对话式优化）→ 视频剪辑（自动去废片/智能字幕/素材叠加/画面智能切换+风格化/对话式修改）→ 运营分发（多平台审核后发布/数据采集分析看板/策略优化反哺选题）。（未验证方向）
- **Scope:** 包含：选题文案、视频剪辑（核心）、运营分发三段的「录完即走」全流程；本地桌面 + 微信远程控制形态。排除：全自动无人审核发布（保留人工审核关卡）；执行段（设计/开发/上线/增长）与 G3/G4 不在本工具范围，交下游交付系统。首周期边界：先 self-first——只做能让自己每周稳定成片的可用闭环，不先碰 T1/T2 规模化。
- **Constraints:** 创始人时间极度稀缺（工具本身必须省时，不能增加学习/操作负担）；Token / API 调用是核心成本，需通过算力额度定价转嫁给用户；创始人对质感与控制权高要求（不能全自动直发）；本地部署依赖用户自担 GPU 算力。
- **Success definition:** （定义，非已验证证据）self-first 阶段——作者自己每周稳定产出的成片数显著提升、单条视频处理时长显著下降、并愿意持续自用（产品即案例）；后续——T1/T2 创始人愿意付费订阅、北极星指标「周均成片发布数」持续上升。

### Money + Magic

- **Magic / consumer value proposition:** 把创始人从短视频全流程的时间与体力消耗中彻底解放——录完即走，只做思考 + 出镜，其余交给 AI Agent。
- **Magic / consumer target:** 时间极度稀缺、必须靠个人 IP 获品牌与流量的企业创始人；第一阶段就是作者自己（高要求、时间最稀缺），再外溢 T1/T2。
- **Money / commercial value proposition:** 订阅费 + 算力额度包 + 增值服务（高级模板 / 1 对 1 策略 / 代理白标）三层收入；本地桌面部署让用户自担 GPU、省云端 GPU 成本；自用阶段以「产品即案例」做内容营销获客。
- **Money / leverageable assets:** 创始人即用户（dogfooding 天然成立）+ 真实代运营服务沉淀的创始人 IP 业务 know-how（认知差壁垒）+ 端到端产品力；功能可抄，认知不可抄。
- **Tension and balance:** 极致省事（Magic）与质感 / 控制权高要求（制约全自动）相互拉扯；self-first 先押效率 / 时间，但质感是 dogfooding 最敏感信号——二者不可偏废，画布以「审核后手动发布」做妥协。

### Current knowledge state

| Type | Content |
|---|---|
| **Known** | [user-stated] 作者做过代运营、自己做 IP、痛点亲身；[user-stated] 创始人没时间做全流程、现有工具是「锤子非木匠」、外包效果失控与沟通成本高；[user-selected] 起点 self-first、第一赌注 = 全流程真省时间、北极星 = 周均成片发布数。（self-report 与选择，非验证证据） |
| **Believed** | [agent-interpretation] founder 即用户 + 代运营 know-how 构成真护城河、dogfooding 天然成立；[agent-interpretation] 订阅 + 算力 + 增值是可行商业模式、本地部署省云端 GPU；[agent-interpretation] 先自用做案例再外溢 T1/T2 的路径成立。 |
| **Unknown** | [unknown] T1 / T2 创始人的真实付费意愿与可接受定价区间；[unknown] 当前 AI 视频剪辑能力能否达到高要求 IP 创始人的质感门槛；[unknown] 创始人是否真愿「只思考 + 出镜」交出控制权（与「审核后手动发布」的张力如何解）；[unknown] self-first 第一版 scope 边界（三段全做 vs 先剪辑 + 选题）；[unknown] 本地桌面 + 微信远程控制的技术形态对快速验证是否过重；[unknown] self-first 成功的量化门槛（每周几条 / 省多少时间）。 |
| **Tensions** | 时间（效率）vs 质感（效果）：用户押效率，但质感是 dogfooding 最敏感信号；极致省事（Magic）vs 控制权 / 质感要求（制约全自动），画布以「审核后手动发布」妥协——全自动与人机协作的边界尚未定。 |
