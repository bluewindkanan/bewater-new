---
schema_version: 1
artifact_id: EXP-002
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-001@2
target_evidence_level: L4
proceed_threshold: 中位数 ≥ 外部基线 P50
kill_threshold: 中位数 ≤ 外部基线 P25
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-002 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-002 · dogfood + 外部基线对照（K-006，真实行为 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-001@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：dogfood + 外部基线对照（K-006，真实行为 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：作者账号 21 天日更的曝光/点赞/进线 vs K-006 同规模账号基线分布
- **Proceed 阈值**：中位数 ≥ 外部基线 P50
- **Kill 阈值**：中位数 ≤ 外部基线 P25
- **非结论性处理**：重测：延长至 42 天窗口
- **负责人 / 时间盒**：秋南Dylan / 4 周
- **证据采集路径**：evidence.yaml E 记录：天级指标 vs 基线分位数
