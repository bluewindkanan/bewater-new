---
schema_version: 1
artifact_id: EXP-006
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-020@2
- assumption:A-026@2
target_evidence_level: L4
proceed_threshold: 语境卡组转发率 ≥ 1.5×；动员组 4 周内达 100 真实转发
kill_threshold: 无显著差异或动员组人情消耗不可持续（退出率 >40%）
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-006 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-006 · 社交 A/B + 关系链动员（语境卡 vs 无语境卡；首 100 转发动员 vs 自然；行为 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-020@2, assumption:A-026@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：社交 A/B + 关系链动员（语境卡 vs 无语境卡；首 100 转发动员 vs 自然；行为 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：n≥30 条对照；转发率差异；动员组首 100 转发达成时间
- **Proceed 阈值**：语境卡组转发率 ≥ 1.5×；动员组 4 周内达 100 真实转发
- **Kill 阈值**：无显著差异或动员组人情消耗不可持续（退出率 >40%）
- **非结论性处理**：重测：缩小语境卡强制范围复测
- **负责人 / 时间盒**：运营 / 8 周
- **证据采集路径**：evidence.yaml E 记录：分组转发率+动员达成
