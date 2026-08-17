---
schema_version: 1
artifact_id: EXP-007
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@1
target_assumption_refs:
- assumption:A-005@2
target_evidence_level: L4
proceed_threshold: 12 个月窗口内空位保持（无 kill signal 触发）置信高
kill_threshold: kill signal 触发（如字节系工具进入视频号、发布 API 开放）
conclusion: null
derived_from:
- artifact:ART-010@1
signoffs:
- what: design-approval
  who: 秋南Dylan
  role: product-owner
  when: '2026-08-17T09:30:00Z'
  scope: EXP-007 设计+阈值固定（proceed/kill/inconclusive/owner/timebox/证据路径）
stale_reason: null
---
# EXP-007 · related-worlds（字节系/大厂进入垂直平台的历史行为模式）+ 官方政策文本监测（RM-006）

## 设计清单（执行前固定，等待人工审批）

- **目标假设**：assumption:A-005@2
- **方案修订**：artifact:ART-010@1（solution_ref）
- **方法**：related-worlds（字节系/大厂进入垂直平台的历史行为模式）+ 官方政策文本监测（RM-006）
- **目标证据级别**：L4（行为证据）
- **指标与基线**：kill signal 清单状态（字节系进入/API 开放/政策转向）+ 历史类比
- **Proceed 阈值**：12 个月窗口内空位保持（无 kill signal 触发）置信高
- **Kill 阈值**：kill signal 触发（如字节系工具进入视频号、发布 API 开放）
- **非结论性处理**：监管/平台类假设证据特殊性：行为证据不可得，用真实市场事件与政策文本作为 L4 级代理——由人工审批裁决可接受性
- **负责人 / 时间盒**：产品（监控组件） / 持续 12 周（滚动）
- **证据采集路径**：evidence.yaml E 记录：信号清单快照
