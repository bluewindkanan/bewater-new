---
schema_version: 1
artifact_id: EXP-008
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-006@2
target_evidence_level: L4
proceed_threshold: 注册率 ≥ 2% 且 CAC ≤ ¥3,000
kill_threshold: 注册率 < 0.5%
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-008 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-008 · guerrilla interview + fake-website 获客实验（真实注册行为 L4）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-006@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：guerrilla interview + fake-website 获客实验（真实注册行为 L4）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：目标人群渠道触达 n≥200；注册率 + CAC 估算
- **Proceed 阈值**：注册率 ≥ 2% 且 CAC ≤ ¥3,000
- **Kill 阈值**：注册率 < 0.5%
- **非结论性处理**：重测：换渠道组合复测一次
- **负责人 / 时间盒**：运营 / 6 周
- **证据采集路径**：evidence.yaml E 记录：注册率+CAC 分渠道
