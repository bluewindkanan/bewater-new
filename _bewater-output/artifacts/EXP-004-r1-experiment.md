---
schema_version: 1
artifact_id: EXP-004
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-007@2
- assumption:A-011@2
target_evidence_level: L4
proceed_threshold: 坚持率 ≥ 80%
kill_threshold: 坚持率 ≤ 50%
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-004 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-004 · 种子用户 30 天行为记录（真实行为 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-007@2, assumption:A-011@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：种子用户 30 天行为记录（真实行为 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：10-15 位种子老板 30 天日更坚持率（进入会话并发布）
- **Proceed 阈值**：坚持率 ≥ 80%
- **Kill 阈值**：坚持率 ≤ 50%
- **非结论性处理**：重测：轻载/救援机制上线后复测
- **负责人 / 时间盒**：产品（秋南Dylan） / 5 周
- **证据采集路径**：evidence.yaml E 记录：坚持率+断更模式
