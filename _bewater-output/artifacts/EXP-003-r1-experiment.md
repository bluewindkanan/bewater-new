---
schema_version: 1
artifact_id: EXP-003
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-002@2
- assumption:A-004@2
target_evidence_level: L4
proceed_threshold: 接受带覆盖 ¥3,980 且意向 CTR ≥ 3%
kill_threshold: 接受带上限 < ¥2,000 或 CTR < 1%
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-003 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-003 · Van Westendorp 价格带 + fake-website 订阅页点击（行为信号 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-002@2, assumption:A-004@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：Van Westendorp 价格带 + fake-website 订阅页点击（行为信号 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：目标老板样本 n≥30；价格接受带 + 订阅页意向 CTR
- **Proceed 阈值**：接受带覆盖 ¥3,980 且意向 CTR ≥ 3%
- **Kill 阈值**：接受带上限 < ¥2,000 或 CTR < 1%
- **非结论性处理**：重测：换样本渠道复测一次；若仍低于 kill 阈值视为 falsified
- **负责人 / 时间盒**：运营（秋南Dylan 协办） / 4 周
- **证据采集路径**：evidence.yaml E 记录：价格带数据+CTR
