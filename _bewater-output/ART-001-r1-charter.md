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
      statement: "向 AI 眼镜/可穿戴 OEM 提供按量、稳定、低门槛的大模型推理供给（token），让 OEM 不必自建模型与推理基础设施即可上线 AI 功能。"
      evidence_refs: []
    consumer_target:
      statement: "正在或即将量产 AI 眼镜、AI 耳机、可穿戴设备的硬件厂商的产品/技术决策人；他们的渴望是用最低集成成本与可控边际成本，把对话式/多模态 AI 能力塞进受限于功耗、体积、算力的设备里。"
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: "百度智能云智能硬件业务以 token 计量向 OEM 出售模型推理配额/API 调用，按设备激活量或调用量计费；收益来自推理规模与百度云基础设施的成本优势之间的差。"
      evidence_refs: []
    leverageable_assets:
      statement: "ERNIE/文心 模型族、百度云推理基础设施（算力与单位推理成本）、既有 B 端商务与硬件客户关系。明确不押：Apollo 车载生态、小度音箱自有渠道（与目标品类无直接重叠）。"
      evidence_refs: []
  tension:
    statement: "Magic 与 Money 在『押推理成本/基础设施』这一选择上相互约束：要给 OEM 极低门槛的集成体验，就需要把价格、SDK、计费颗粒度做到 OEM 友好；而百度云的成本优势是否能传导到 OEM 可感知的价格点，且这一价格点是否仍能产生可持续毛利，尚未被验证。此外，百度智能硬件 BU 的天然生态杠杆（车载/音箱）与本次选定的目标品类（AI 眼镜/可穿戴）不重合，意味着这是一次以基础设施成本为主要卖点的 greenfield 销售尝试，而非生态延伸。"
  balance_choice: "暂时押 Money 侧——以推理成本/基础设施优势作为差异化主卖点；Magic 侧的 OEM 体验设计留待 Discover/Shape 阶段细化。"
derived_from: []
signoffs: []
stale_reason: null
---

# Charter · ART-001 r1 · 百度智能云智能硬件业务 — AI 硬件 token 业务

## Original intent

- **User's own words:** "百度智能云智能硬件业务，要做给 AI 硬件卖 token 的业务。"
- **Trigger / why now:** 内部战略推动——智能硬件 BU 寻找第二曲线 / 提高 ARPU / 战略转型。本次启动为 push 驱动，**尚无具体大客户落地**。
- **Desired change:** 让百度智能云智能硬件业务从原本的硬件相关业务，长出一个面向 AI 硬件厂商、按 token 计费的模型推理供给业务。

## Structured interpretation

- **One-line proposition:** 向 AI 眼镜/可穿戴 OEM 厂商，按 token 计量出售百度模型推理配额/API，押注百度云的推理成本与基础设施优势。
- **Target and situation:** AI 眼镜、AI 耳机、可穿戴设备厂商的产品/技术决策人，受限于端侧算力/功耗/体积，需要在云侧完成大模型推理并按量采购。
- **Current behavior and alternatives:** *Unknown*——OEM 今天究竟怎么解决模型推理（自建/友商采购/调海外 API/灰色转售）以及每种替代的真实成本与痛点，尚未由用户提供，亦无证据支撑。这是 Discover 的首要调查面。
- **Provisional solution hypothesis（用户当前 how，未验证）:** 以 ERNIE/百度云推理为供给底座，向 OEM 提供按量 token API，主卖点为价格/性价比与基础设施稳定性。
- **Success signals:** *待 Discover 后细化*。暂列候选：OEM 签约数、激活设备数、月活调用量、单设备 ARPU、续约率。所有候选拟在 Shape/投资叙事阶段指标化，不在此处承诺阈值。
- **Scope:**
  - **Included:** AI 眼镜/可穿戴 OEM 的 B2B token/API 供给；推理成本/基础设施为差异化主轴。
  - **Excluded:** 不以车载/智能座舱、机器人/具身智能、智能家居（音箱/学习机/家电）为本次目标品类；不押自有硬件渠道分发；不在本 Charter 阶段承诺 SDK 形态、价格表、商业分成的具体数字。
  - **First-cycle boundary:** 在 Discover 完成对 AI 眼镜/可穿戴 OEM 真实现状与付费意愿的调查之前，不进入方向性假设与方案塑造。

## Money + Magic

- **Magic / consumer value proposition:** 让 OEM 用低门槛、可计量的方式获得大模型推理能力，无需自建模型团队/推理基础设施。
- **Magic / consumer target:** AI 眼镜/可穿戴设备的产品/技术决策人；他们当前的渴望与痛点是 *Unknown*——明确知道客户"类型"，但不知道"情境"。
- **Money / commercial value proposition:** 按 token/API 调用量计费的 B2B 推理供给；商业可行性取决于百度云单位推理成本 vs. OEM 可接受报价 vs. 调用规模三者之交集。
- **Money / leverageable assets:** ERNIE 模型、百度云推理基础设施、既有 B 端商务能力。明确**不**计入杠杆：Apollo、小度自有渠道（与目标品类无重叠）。
- **Tension and balance:**
  1. **生态错位 tension：** 智能硬件 BU 的天然生态杠杆（车载/音箱）与本次押注的目标品类（AI 眼镜/可穿戴）不重合，"内部战略推动"与"押推理成本"之间的因果链尚未成立——是先有战略再选了 greenfield 品类，还是先识别到眼镜机会再倒推战略？这一动因方向的缺失影响所有下游假设。
  2. **价格-毛利 tension：** 押成本优势即隐含承诺"低于友商的可感知报价"，但 OEM 端的可接受价格区间与百度云的单位推理成本曲线关系未量化，存在"压价抢量但毛利撑不住"的风险。
  3. **Magic-Money 断层：** Money 主卖点（成本/基础设施）与 Magic 主诉求（OEM 集成体验、生态贴合）之间尚未形成相互强化的故事——客户可能不只为便宜而买。

## Current knowledge state

| 类型 | 内容 |
|---|---|
| **Known** | 命题方向：B2B 卖 token 给 AI 眼镜/可穿戴 OEM（用户选定）；启动动因：内部战略推动（用户选定）；主卖点选择：押推理成本/基础设施（用户选定）；杠杆资产清单：ERNIE、百度云推理设施、B 端商务能力（用户确认）。 |
| **Believed** | AI 眼镜/可穿戴 OEM 普遍需要云侧大模型推理；百度云的单位推理成本相对友商具有可感知优势；按 token 计量是此类业务可落地的计费形态。 |
| **Unknown** | OEM 今天的真实解决路径与痛点；OEM 决策链与购买周期；OEM 对推理单价、延迟、稳定性的真实可接受区间；目标品类的实际出货量与单品调用量；百度报价在 OEM 视角下是否构成差异化；在不依赖现有生态杠杆的情况下销售如何触达 OEM；ERNIE 在眼镜/可穿戴多模态/低延迟场景下的适配成熟度。 |
| **Tensions** | 生态错位（押推理成本 ≠ 押生态杠杆）；价格-毛利未量化；Magic-Money 故事尚未相互强化；push 启动 vs. pull 验证的先后关系未定。 |

## Discover handoff

### Core exploration question

> 在我们敢于对"以推理成本优势向 AI 眼镜/可穿戴 OEM 卖 token"这一方向下注之前，必须先搞清楚：OEM 今天是怎么解决的、真实痛点与可接受价格区间是什么，以及在不依赖既有生态杠杆的前提下，百度能否触达并说服这群客户？

### Beliefs to challenge

- B1（candidate belief）：AI 眼镜/可穿戴 OEM 普遍需要外采而非自建模型推理。
- B2（candidate belief）：百度云的单位推理成本足以构成对 OEM 可感知的差异化。
- B3（candidate belief）：OEM 在百度可承受的报价下仍能形成可持续毛利。
- B4（candidate belief）：AI 眼镜/可穿戴品类出货量足以支撑独立 token 业务。
- B5（candidate belief）：在不依赖 Apollo/小度生态的情况下，百度能触达 AI 眼镜/可穿戴 OEM。

以上均为 candidate belief，**不是 Fact**。每一条都需要 Discover 提供 L4+ 行为证据后才能进入 Go 判断。

### Root assumption research map

| Assumption | 4C | Why it matters | Evidence needed | Disconfirming signal |
|---|---|---|---|---|
| A-001 | Consumer（OEM）/ Channel | 若 OEM 不外采，整个命题失效 | 一手访谈 OEM 技术/产品负责人；二级市场研报对自建 vs. 外采比例 | 头部 AI 眼镜/可穿戴 OEM 普遍已自建或长期独家锁定友商 |
| A-002 | Company / Category | "押成本优势"是否真的可感知 | OEM 侧联合测价/POC；百度与友商在同等 token/延迟条件下的报价对照 | 同等条件下 OEM 不视价格为决策因素，或友商报价比百度更低 |
| A-003 | Category / Company | 决定业务是否挣钱而非只走量 | OEM 预算与毛利结构访谈；百度云单位推理成本曲线 | 即便 OEM 接受报价，毛利仍低于内部底线，或为抢量被迫持续降价 |
| A-004 | Category | 决定赛道上限 | 出货量预测（IDC/Counterpoint/Strategy Analytics 等）；AI 眼镜品类 2024-2026 出货量与渗透率 | 出货量持续低位、单品调用量不足以摊薄基础设施投入 |

### Starting 4C questions

- **Consumer（OEM）：** 谁（具体角色/公司类型）会决定采购 token 推理？他们所在公司的产品节奏、出货量量级、技术能力是什么？
- **Company：** 在不依赖 Apollo/小度的前提下，百度智能云智能硬件业务靠什么触达这群客户？现有 B 端商务覆盖了哪些 OEM？
- **Category：** AI 眼镜/可穿戴品类在 2026+ 的实际出货量、单品 AI 调用量、定价区间是什么？替代方案（自建、友商 API、海外 API）的真实成本与体验差距是什么？
- **Channel：** OEM 评估与采购 token/API 推理供给的决策与集成路径是什么？通过云市场、直客、设备方案商还是方案商集成？

### Research boundary

- **应先做：** 一手 OEM 访谈（≥5 家代表性 AI 眼镜/可穿戴厂商，覆盖产品/技术决策人）；友商 token 报价与 SLA 横向对照；目标品类出货量与单品 AI 调用量的二手数据三角验证；百度云单位推理成本对 OEM 报价的可传导性测算。
- **不应假定 / 不应优化：** 不假定 OEM 一定外采；不假定具体价格数字；不在 Discover 阶段设计 SDK、签订客户、写商业模型数字、做方案塑造。SDK 形态、定价表、商业分成结构留给 Shape 阶段。
