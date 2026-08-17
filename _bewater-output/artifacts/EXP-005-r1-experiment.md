---
schema_version: 1
artifact_id: EXP-005
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-008@2
- assumption:A-019@2
target_evidence_level: L4
proceed_threshold: 转发值组均值转发率 ≥ 1.5× 对照组
kill_threshold: 无显著差异（p≥0.1 且效应 <1.2×）
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-005 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-005 · 社交 A/B（同账号同选题，转发值排序 vs 热度排序；行为信号 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-008@2, assumption:A-019@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：社交 A/B（同账号同选题，转发值排序 vs 热度排序；行为信号 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：n≥40 条对照；转发率差异（p<0.1 双侧）
- **Proceed 阈值**：转发值组均值转发率 ≥ 1.5× 对照组
- **Kill 阈值**：无显著差异（p≥0.1 且效应 <1.2×）
- **非结论性处理**：重测：换选题域复测；连续两次无差异视为 falsified（触发 bw-backtrack）
- **负责人 / 时间盒**：产品+数据 / 8 周
- **证据采集路径**：evidence.yaml E 记录：分组转发率+统计量
