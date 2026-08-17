---
schema_version: 1
artifact_id: EXP-001
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-003@2
target_evidence_level: L4
proceed_threshold: P80 ≤ 40 分钟且 21 天完成率 ≥ 80%
kill_threshold: P80 > 60 分钟或完成率 < 50%
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-001 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-001 · dogfood（真实使用行为，L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-003@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：dogfood（真实使用行为，L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：作者自有账号连续 21 天日更；单条人工耗时 P80（会话内+会话外）
- **Proceed 阈值**：P80 ≤ 40 分钟且 21 天完成率 ≥ 80%
- **Kill 阈值**：P80 > 60 分钟或完成率 < 50%
- **非结论性处理**：重测：调整预处理管线后 2 周内复测一次
- **负责人 / 时间盒**：秋南Dylan（产品作者） / 3 周
- **证据采集路径**：_bewater/evidence.yaml 新增 E 记录：会话日志摘要+耗时统计
