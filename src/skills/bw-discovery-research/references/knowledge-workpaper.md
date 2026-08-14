# Knowledge workpaper

Use one living Knowledge workpaper for each bounded research question or hypothesis. A primary
workpaper keeps `knowledge_refs: []`; a Sprint summary uses the same contract, records
`method: synthesis` under Method and scope, and pins each contributing `knowledge:K-NNN@n`.

Path: `_bewater-output/knowledge/K-NNN-<short-title>.md`. There is one stable file per K-NNN. A
revision updates that path in place through CAS; never create `K-NNN-rN` files. The filename remains
stable if the title changes.

```yaml
---
schema_version: 1
knowledge_id: K-001
revision: 1
branch_id: BR-001
title: Bounded research question
research_ref: artifact:ART-003@1
learning_refs: [LP-001]
source_refs:
  - path: _bewater-output/sources/interviews.docx
    sha256: <lowercase SHA-256 of the exact bytes>
  - url: <exact retrieved URL>
knowledge_refs: []
evidence_refs: []
status: working
---
```

Required body headings are Question or hypothesis, Method and scope, Sources used, Summary,
Conclusion, and Limitations and new questions. A complete Knowledge workpaper has a non-empty
Summary, direct Conclusion with confidence, and material limitations. Keep detailed analysis in a
Source file only when it improves auditability or reuse; the Research Plan contains neither full
analysis nor source inventories.

The validator checks local Source existence and Source SHA-256 from bytes only. It never parses,
executes, copies, or writes a DOCX, PDF, spreadsheet, or other Source. URLs are preserved exactly and
are never invented or repaired. Host tools prepare Sources before canonical persistence.

`research_ref` remains the exact plan revision that authorized the work; it does not chase a newly
appended Research head. Runtime resolution is current-head only: the current Research head pins the
current revision of each same-branch workpaper it reads. A synthesis workpaper also pins the current
revision of every input. Historical Research revisions retain audit pins and are not re-resolved.
Git preserves historical Knowledge text; CAS backups are recovery files only.
