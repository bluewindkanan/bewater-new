---
schema_version: 1
artifact_id: ART-002
revision: 1
supersedes_ref: null
kind: initial-assessment
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
derived_from:
  - artifact:ART-001@1
  - assumption:A-001@1
  - assumption:A-002@1
  - assumption:A-003@1
  - assumption:A-004@1
signoffs: []
stale_reason: null
---

# Initial Assessment · ART-002 r1 · 百度智能云 AI 硬件 token 业务

## 1. Overall Preliminary Conclusion

百度面向 AI 眼镜/可穿戴 OEM 的 B2B token 供给，是一个**方向合理、动因可疑、毛利未证实的 greenfield 机会**：云侧推理确为该品类的硬需求，但"内部战略推动 + 押成本优势"的因果链尚未成立，且百度智能硬件 BU 的天然生态杠杆与本品类错位，最大未知是**OEM 是否会在百度可承受报价下持续外采**。

> **Charter basis:** ART-001 押 Money 侧，以"推理成本/基础设施优势"为主卖点。 → **External signal:** 全球 AI 眼镜出货 2025 ≈ 870 万台、2026 预测 ≈ 1360 万台（IDC）；Ray-Ban Meta 采用"端-云混合"架构，云侧推理为硬需求（ZenML/Meta）。 → **Assessment inference:** 品类增量真实存在，且结构性依赖云侧推理，外采命题的方向性成立。 → **Implication:** Discover 应优先证伪 A-001/A-002 而非重新论证赛道。 → **What would change this view:** 头部 OEM 普遍自建推理或被友商长期独家锁定（A-001 证伪信号）。

## 2. Professional Perspectives

- **Magic：** 让 OEM 跳过自建模型/推理团队即可上线 AI 功能——价值真实，但 Meta/Google 已示范"自有生态 + 自有推理"路径，第三方 token 供给只是**若干可行选项之一**，而非默认选项。
- **Money：** ERNIE 4.5 21B A3B 报价约 $0.06–0.22 / 百万 token（pricepertoken），价格工具齐全；但消费侧 Ernie Bot 已于 2025-04 起免费，API 价格曲线持续下行，**单位毛利被双向挤压**，"低成本优势可传导为可感知差异化"未被任何源证实。
- **Innovation：** 真正差异化的机制不是"卖 token"，而是**给眼镜品类提供贴合场景的多模态/低延迟推理 + OEM 友好的计费颗粒度**——Charter 暂未押此层。

## 3. Candidate Insights

1. **CI-1：** 百度智能硬件 BU 选"AI 眼镜/可穿戴"更像先有战略再选 greenfield 品类，而非先识别到 OEM 真实 pull——动因方向倒置会使所有下游假设系统性偏乐观。
2. **CI-2：** 在 Meta/Google/Apple 都把"眼镜 + 自有推理生态"做成默认路径的市场里，第三方 token 供给的**真实生态位是"非阵营 OEM 的备选推理源"**，而非品类级基础设施。
3. **CI-3：** 价格曲线下行（消费侧已免费、企业 API 持续降价）意味着**"压价抢量"几乎必然，可持续毛利只能来自百度云单位推理成本的长期结构性领先**——这是 A-002 与 A-003 的真正交汇点。

## 4. Core Conflict / Tension

**生态错位 vs. 成本差异化：** 智能硬件 BU 的天然杠杆（车载、小度）与目标品类不重合，使本命题成为一次**只凭"成本优势"打开 greenfield OEM 的纯销售尝试**；而消费侧 token 已免费、企业 API 持续降价，"成本优势"作为差异化主轴的护城河宽度未被任何源证实。

> **Charter basis:** Tension 章节明确生态错位与价格-毛利 tension。 → **External signal:** Ernie Bot 2025-04 起免费（Yicai）；ERNIE API 多档报价区间公开（pricepertoken/ZenMux）。 → **Assessment inference:** 价格工具虽齐全，但行业单价整体下行，单凭报价难以构成 OEM 决策差异。 → **Implication:** 必须把"差异化"从价格拓宽到 SLA/集成/场景适配。 → **What would change this view:** 出现 OEM 把"百度单位推理成本显著低于友商"列为采购主因的实测证据。

## 5. Most Promising Direction

**优先方向：** "非阵营 AI 眼镜/可穿戴 OEM 的备选云侧推理供给"——服务那些**未被 Meta/Google/Apple 阵营锁定、又无力自建**的腰部厂商。
**备选方向 A：** 面向中国本土眼镜/耳机 OEM 的多模态低延迟推理 + OEM 友好计费（贴近百度既有 B 端商务覆盖）。
**备选方向 B：** 以单位推理成本结构性优势为锚的可持续毛利定价模型（与 A-002/A-003 同向）。

## 6. Key Risks

- **R-1（生态错位）：** 无既有生态杠杆，纯靠成本打开 OEM。 → **What would change this view:** 百度在眼镜/可穿戴品类获得非成本型合作证据（场景共建、SDK 共担）。
- **R-2（价格-毛利）：** 消费侧免费、企业 API 持续降价，可持续毛利假设脆弱。 → **What would change this view:** 拿到 OEM 联合测价/POC 中百度仍保持内部毛利底线的实测数据。
- **R-3（赛道上限）：** 出货量与单品调用量是否足以摊薄基础设施投入，二手数据口径分歧大（2026 市场规模 $3.2B–$12.5B）。 → **What would change this view:** 出货量与单品调用量的三角验证收敛到一致量级。

## 7. Discover Mission

- **优先任务：** 一手访谈 ≥5 家非阵营 AI 眼镜/可穿戴 OEM 的产品/技术决策人，弄清他们**今天怎么解决推理、真实可接受报价区间、决策链**。
- **两个关键问题：** (1) OEM 在什么条件下会**持续外采**而非自建或投奔阵营？(2) 在同等 SLA 下，百度报价是否构成 OEM 决策因素？
- **本轮不优化：** SDK 形态、定价表、商业分成结构（留给 Shape）。

## 8. Research Boundary & Sources

**研究边界：** 仅做了 4 次公开网检，得到 4 类可信源（二手市场预测、一手 API 报价、架构分析、消费侧免费公告）。**未做**一手 OEM 访谈、未拿到百度云单位推理成本曲线、未做友商 SLA 横向对照。"外采比例""OEM 决策权重""百度毛利结构"在公开源中**未建立**，相关推断均为 Assessment inference。源之间在 2026 市场规模（$3.2B vs $12.5B）与 ERNIE 报价（$0.06 vs $2.65 / 百万 token，不同型号）存在显著分歧，已保留为风险 R-3 而非选择有利源。

**Sources:**

1. IDC — *Smart Glasses Surge: XR Market Rewriting Its Own Rules*（2026 预测 ≈13.6M 台、≈$5.1B）。https://www.idc.com/resource-center/blog/smart-glasses-surge-the-xr-market-is-rewriting-its-own-rules/
2. pricepertoken.com — *Baidu API Pricing (Updated 2026) – All Models*（ERNIE 多档报价）。https://pricepertoken.com/pricing-page/provider/baidu
3. ZenML LLMOps Database — *Meta / Ray-Ban: Edge AI Architecture for Wearable Smart Glasses*（端-云混合架构）。https://www.zenml.io/llmops-database/edge-ai-architecture-for-wearable-smart-glasses-with-real-time-multimodal-processing
4. Yicai Global — *Baidu to Turn AI Model Ernie Bot Free-of-Charge From April 1*（2025-04-01）。https://www.yicaiglobal.com/news/baidu-to-turn-ai-model-ernie-bot-free-of-charge-from-april-1

*本报告为初步咨询性判断，非 Insight、非 Gate、不含评分/红黄绿 readiness 标签，不决定是否投资或是否进入 Discover。*
