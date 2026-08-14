---
schema_version: 1
knowledge_id: K-003
revision: 1
branch_id: BR-001
title: Unit economics for AI short-video editing - per-clip cost versus pricing models
research_ref: artifact:ART-003@1
learning_refs: [LP-003]
source_refs:
  - url: https://www.opus.pro/pricing
  - url: https://playcut.ai/blog/opus-clip-alternatives/
  - url: https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026
  - url: https://www.layer3labs.io/guides/descript-pricing
  - url: https://checkthat.ai/brands/opusclip/pricing
  - url: https://kgabeci.medium.com/i-compared-the-cost-of-every-ai-video-api-heres-what-each-clip-actually-costs-3984ef6553e9
  - url: https://ai.google.dev/gemini-api/docs/pricing
  - url: https://www.together.ai/pricing
  - url: https://www.forbes.com/sites/metronome/2025/10/01/using-credit-based-pricing-in-ai-powered-saas-what-works-and-what-doesnt/
  - url: https://getlago.com/blog/usage-based-pricing-examples
  - url: https://userpilot.com/blog/saas-pricing-models/
knowledge_refs: []
evidence_refs: []
status: complete
---

## Question or hypothesis

What are the unit economics — token/GPU cost per published clip versus viable subscription or compute-quota pricing — and does the credit-cap unpredictability trap apply?

## Method and scope

Pricing and unit-economics analysis from competitor pricing pages, AI video-generation API cost proxies, and GPU rental rates (2025-2026); sensitivity boundary check on cost-to-price spreads; review of credit-based SaaS pricing dynamics. Exclusions: proving customers will adopt a price; full market sizing. Single wave.

## Sources used

- Opus Clip official pricing (opus.pro) — vendor.
- Playcut, "7 Best Opus Clip Alternatives (Real Cost-Per-Clip Math)" — independent-industry.
- Reap.video, "State of Top AI Video Clipping Tools 2026" — independent-industry.
- Layer3 Labs, "Descript Pricing 2026 Guide" — independent-industry.
- CheckThat.ai, "OpusClip Pricing 2026" — independent-industry.
- kgabeci (Medium), "I Compared the Cost of Every AI Video API" — independent-industry.
- Google, "Gemini Developer API pricing" — vendor.
- Together AI, "Pricing" (H100 GPU) — vendor.
- Forbes/Metronome, "Using Credit-Based Pricing in AI-Powered SaaS" (Oct 2025) — independent-industry.
- Lago, "10 Usage-Based Pricing Examples" — independent-industry.
- Userpilot, "SaaS Pricing Models" — independent-industry.

## Summary

Competitor pricing is subscription-plus-credit and structurally unpredictable: Opus Clip runs a free 60-credit tier to roughly USD 15-29/mo Pro (about 300 credits, one credit per source-minute, sub-one-minute clips rounded up), and "credit gaps and unpublished refill costs make total expenses hard to predict" (CheckThat.ai); Submagic's API lands at USD 69/mo with 100 included minutes then USD 0.10-0.15/min and a 30-minute-per-clip cap (Reap.video); Descript spans USD 16-50/mo by tier (Layer3 Labs). On the cost side, AI video-generation APIs run roughly USD 5-50 per generated minute (kgabeci), Gemini 720p video about USD 6/min via token accounting, and H100 GPU rental USD 2.01-7.25/hr (Together AI; Fireworks serverless cheaper). The credit-cap trap is real but contingent: Forbes/Metronome finds "credits buy time at the start, but they're rarely the end state" as enterprise AI moves to usage or hybrid pricing, yet Lago reports that fairly priced usage-based models can actually reduce churn because users scale down instead of canceling. Credit-model companies grew 126% year-on-year in 2025 (Userpilot).

## Conclusion

Partial. A bounded per-clip cost-to-price band is visible: incumbent consumer pricing is roughly USD 15-69/mo credit-capped (unpredictable per-clip), while the underlying generation cost is roughly USD 3-50 per generated minute plus editing compute. The credit-cap unpredictability trap applies to naive credit pricing, but a transparent, predictable compute-quota or fair usage-based model is both viable and a differentiator that can lower churn rather than raise it. Willingness-to-pay for the T1/T2 founder segments remains a gap. Confidence: medium on the cost and price bands; the WTP gap is unaddressed.

## Limitations and new questions

Pricing pages change frequently and vendor pages carry commercial framing; token/GPU costs are proxies, not measured for this product's actual pipeline; local-desktop GPU is borne by the user, which shifts the cost model but is unquantified here. New questions: what is the real token/compute cost of one end-to-end run on this product's pipeline (measured in dogfooding), and what T1/T2 price band clears both cost and the control-quality bar — both need behavioral and internal data, not public sources.
