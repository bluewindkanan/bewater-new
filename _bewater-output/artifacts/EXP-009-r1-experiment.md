---
schema_version: 1
artifact_id: EXP-009
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-009@2
- assumption:A-029@2
- assumption:A-036@2
target_evidence_level: L4
proceed_threshold: 体验后意向显著提升（配对检验 p<0.1）且退款组转化 ≥ 1.5×
kill_threshold: 无显著差异
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-009 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-009 · fake-website 工作台 demo + 退款条款 A/B（行为信号 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-009@2, assumption:A-029@2, assumption:A-036@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：fake-website 工作台 demo + 退款条款 A/B（行为信号 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：样本老板 n≥30 体验透明工作台 demo；信任意向 + 退款组 vs 对照组转化
- **Proceed 阈值**：体验后意向显著提升（配对检验 p<0.1）且退款组转化 ≥ 1.5×
- **Kill 阈值**：无显著差异
- **非结论性处理**：重测：demo 迭代后复测一次
- **负责人 / 时间盒**：产品 / 6 周
- **证据采集路径**：evidence.yaml E 记录：意向分+分组转化
