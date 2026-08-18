"""Behavioral tests for the self-contained bwkit HTML reader."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from bwkit import cli, html


class _DocsStructureParser(HTMLParser):
    void_tags = frozenset(
        {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }
    )

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, dict[str, str | None]]] = []
        self.docs_depth: int | None = None
        self.errors: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if self.docs_depth is not None and len(self.stack) == self.docs_depth:
            classes = set((attributes.get("class") or "").split())
            if tag != "section" or "doc-section" not in classes:
                self.errors.append(f"unexpected .docs child: {tag}.{'.'.join(classes)}")
        if tag not in self.void_tags:
            self.stack.append((tag, attributes))
        if tag == "div" and "docs" in (attributes.get("class") or "").split():
            self.docs_depth = len(self.stack)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1][0] != tag:
            current = self.stack[-1][0] if self.stack else "nothing"
            self.errors.append(f"closing {tag} while {current} is open")
            return
        if self.docs_depth == len(self.stack) and tag == "div":
            self.docs_depth = None
        self.stack.pop()


def _write_doc(
    directory: Path,
    filename: str,
    *,
    doc_id: str,
    revision: int,
    body: str,
    title: str | None = None,
    status: str | None = None,
    kind: str | None = None,
    stage: str | None = None,
) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    id_key = "knowledge_id" if doc_id.startswith("K-") else "artifact_id"
    fields = [f"{id_key}: {doc_id}", f"revision: {revision}"]
    if title is not None:
        fields.append(f'title: "{title}"')
    if status is not None:
        status_key = "status" if doc_id.startswith("K-") else "document_status"
        fields.append(f"{status_key}: {status}")
    if kind is not None:
        fields.append(f"kind: {kind}")
    if stage is not None:
        fields.append(f"stage: {stage}")
    path = directory / filename
    frontmatter = "\n".join(fields)
    path.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
    return path


def test_parse_md_loads_typed_reader_metadata(tmp_path: Path) -> None:
    path = _write_doc(
        tmp_path,
        "ART-001-r2-charter.md",
        doc_id="ART-001",
        revision=2,
        body="# Charter\n",
        title="Strategy: first cut",
        status="final",
        kind="charter",
        stage="immersion",
    )

    metadata, body = html.parse_md(path)

    assert metadata == {
        "artifact_id": "ART-001",
        "revision": 2,
        "title": "Strategy: first cut",
        "document_status": "final",
        "kind": "charter",
        "stage": "immersion",
    }
    assert body == "# Charter\n"


def test_collect_docs_keeps_latest_revision_and_derives_h1_title(tmp_path: Path) -> None:
    _write_doc(
        tmp_path,
        "ART-003-r1-research.md",
        doc_id="ART-003",
        revision=1,
        body="# Research · old\n\nOld body\n",
    )
    _write_doc(
        tmp_path,
        "ART-003-r2-research.md",
        doc_id="ART-003",
        revision=2,
        body="# Research · current\n\nCurrent body\n",
    )

    items, bodies = html.collect_docs(tmp_path)

    assert len(items) == 1
    assert items[0]["artifact_id"] == "ART-003"
    assert items[0]["revision"] == 2
    assert items[0]["title"] == "Research · current"
    assert bodies == {"ART-003": "Current body"}


def test_generate_html_preserves_markdown_semantics_and_translates_sections() -> None:
    items = [
        {
            "knowledge_id": "K-001",
            "revision": 3,
            "title": "Reader semantics",
            "status": "complete",
        }
    ]
    bodies = {
        "K-001": """## Question or hypothesis

Paragraph with **strong text** and `inline_code`.

- first item
- second item

> quoted finding

```python
print("hello")
```

| Signal | Result |
|---|---|
| Demand | Confirmed |
"""
    }

    output = html.generate_html(items, bodies, "Knowledge 工论文", "knowledge")

    assert "<h2>研究问题</h2>" in output
    assert "<strong>strong text</strong>" in output
    assert "<code>inline_code</code>" in output
    assert "<ul>" in output and "<li>first item</li>" in output
    assert "<blockquote>" in output
    assert '<code class="language-python">' in output
    assert "<table>" in output and "<th>Signal</th>" in output
    assert "<p><table>" not in output


def test_generate_html_routes_local_and_cross_page_revision_refs() -> None:
    items = [{"knowledge_id": "K-001", "revision": 1, "title": "References"}]
    bodies = {
        "K-001": (
            "See knowledge:K-002@3, artifact:ART-004@2, "
            "and artifact:EXP-007@1."
        )
    }

    output = html.generate_html(items, bodies, "Knowledge 工论文", "knowledge")

    # Check for new citation format with title attribute
    assert '<a href="#K-002" class="ref" title="K-002@3">[002]</a>' in output
    assert '<a href="artifacts.html#ART-004" class="ref" title="ART-004@2">[004]</a>' in output
    assert '<a href="artifacts.html#EXP-007" class="ref" title="EXP-007@1">[007]</a>' in output

    artifact_output = html.generate_html(
        [{"artifact_id": "ART-004", "revision": 2, "title": "Artifact refs"}],
        {"ART-004": "See knowledge:K-002@3 and artifact:EXP-007@1."},
        "Artifacts",
        "artifact",
    )
    assert (
        '<a href="knowledge.html#K-002" class="ref" title="K-002@3">[002]</a>'
        in artifact_output
    )
    assert '<a href="#EXP-007" class="ref" title="EXP-007@1">[007]</a>' in artifact_output


def test_generate_html_escapes_metadata_and_builds_reader_shell() -> None:
    items = [
        {
            "artifact_id": "ART-001",
            "revision": 4,
            "title": '<script>alert("title")</script>',
            "document_status": "final",
            "kind": "charter",
            "stage": "immersion",
        }
    ]

    output = html.generate_html(items, {"ART-001": "## Scope\n\nBody"}, "Artifacts", "artifact")

    assert '<script>alert("title")</script>' not in output
    assert "&lt;script&gt;alert(&quot;" in output
    assert '<div class="reader-shell">' in output
    assert '<aside class="reader-sidebar">' in output
    assert '<details class="toc" open>' in output
    assert '<main class="reader-main">' in output
    assert '<article class="doc-article">' in output
    assert 'class="meta-pill is-complete">已定稿</span>' in output
    # 简化元数据后不再显示 revision/kind/stage
    assert "r4</span>" not in output and "charter</span>" not in output and "immersion</span>" not in output
    assert "--reader-width: 820px" in output
    assert "line-height: 1.85" in output
    assert "@media (max-width: 960px)" in output
    assert "@media (max-width: 640px)" in output
    assert "@media print" in output
    assert 'window.matchMedia("(min-width: 961px)")' in output
    assert "https://" not in output


def test_build_html_handles_empty_and_single_collection_projects(tmp_path: Path) -> None:
    empty_result = html.build_html(tmp_path)
    html_dir = tmp_path / "_bewater-output" / "html"
    assert empty_result == {"knowledge": 0, "artifacts": 0, "output": str(html_dir)}
    assert html_dir.is_dir()
    assert not (html_dir / "knowledge.html").exists()
    assert not (html_dir / "artifacts.html").exists()

    _write_doc(
        tmp_path / "_bewater-output" / "knowledge",
        "K-001-reader.md",
        doc_id="K-001",
        revision=1,
        title="Only knowledge",
        status="complete",
        body="## Summary\n\nReadable body.\n",
    )

    result = html.build_html(tmp_path)

    assert result["knowledge"] == 1
    assert result["artifacts"] == 0
    assert (html_dir / "knowledge.html").exists()
    assert not (html_dir / "artifacts.html").exists()


def test_html_cli_reports_unique_latest_documents(tmp_path: Path, capsys) -> None:
    artifact_dir = tmp_path / "_bewater-output" / "artifacts"
    _write_doc(
        artifact_dir,
        "ART-001-r1-charter.md",
        doc_id="ART-001",
        revision=1,
        body="# Old charter\n",
    )
    _write_doc(
        artifact_dir,
        "ART-001-r2-charter.md",
        doc_id="ART-001",
        revision=2,
        body="# Current charter\n",
    )

    assert cli.main(["html", str(tmp_path)]) == 0

    stdout = capsys.readouterr().out
    assert "generated 0 knowledge documents, 1 artifacts" in stdout
    generated = tmp_path / "_bewater-output" / "html" / "artifacts.html"
    assert generated.exists()
    assert generated.read_text(encoding="utf-8").count('id="ART-001"') == 1


def test_artifact_toc_groups_decision_stages_and_hides_internal_title_noise() -> None:
    items = [
        {
            "artifact_id": "ART-008",
            "revision": 2,
            "title": "ART-008 r2 · Idea Pool · 创意方向",
            "kind": "idea-pool",
            "stage": "ideate",
        },
        {
            "artifact_id": "EXP-001",
            "revision": 4,
            "title": "EXP-001 r4 · Experiment · 真实使用行为",
            "kind": "experiment",
            "stage": "shape",
        },
        {
            "artifact_id": "ART-004",
            "revision": 3,
            "title": "ART-004 r3 · Insight Portfolio · 核心洞察",
            "kind": "insights",
            "stage": "define",
        },
        {
            "artifact_id": "ART-001",
            "revision": 5,
            "title": "ART-001 r5 · Charter · 项目命题",
            "kind": "charter",
            "stage": "immersion",
        },
    ]
    bodies = {_id: "正文" for _id in ("ART-008", "EXP-001", "ART-004", "ART-001")}

    output = html.generate_html(items, bodies, "Artifacts", "artifact")

    expected_reader_order = [
        "理解问题",
        "项目命题",
        "形成战略",
        "核心洞察",
        "形成方案",
        "创意方向",
        "验证风险",
        "真实使用行为",
    ]
    positions = [output.index(label) for label in expected_reader_order]
    assert positions == sorted(positions)

    toc_titles = re.findall(r'<span class="toc-item-title">([^<]+)</span>', output)
    doc_titles = re.findall(r'<h1 class="doc-title">([^<]+)</h1>', output)
    assert toc_titles == ["案例路径", "项目命题", "核心洞察", "创意方向", "真实使用行为"]
    assert sorted(doc_titles) == sorted(
        ["案例路径", "项目命题", "核心洞察", "创意方向", "真实使用行为"]
    )
    for reader_title in toc_titles + doc_titles:
        assert not re.search(r"(?:ART|EXP)-\d+|\br\d+\b", reader_title)
        assert not re.search(
            r"Charter|Insight Portfolio|Idea Pool|Experiment", reader_title
        )


def test_experiment_brief_translates_visible_method_terms() -> None:
    body = """## 设计清单（执行前固定，等待人工审批）

- **方法**：dogfood + fake-website demo + guerrilla interview + related-worlds
- **目标证据级别**：L4（行为证据）
"""
    output = html.generate_html(
        [
            {
                "artifact_id": "EXP-001",
                "revision": 1,
                "title": "Experiment · dogfood",
                "kind": "experiment",
            }
        ],
        {"EXP-001": body},
        "Artifacts",
        "artifact",
    )

    assert "自用验证 + 模拟订阅页 演示 + 快速访谈 + 类比研究" in output
    visible_brief = re.search(
        r'<section class="experiment-brief">.*?</section>', output, re.DOTALL
    )
    assert visible_brief is not None
    assert not re.search(
        r"dogfood|fake-website|guerrilla interview|related-worlds|\bdemo\b",
        visible_brief.group(0),
        re.IGNORECASE,
    )


def test_reader_has_no_show_all_toggle() -> None:
    output = html.generate_html(
        [
            {"artifact_id": "ART-001", "revision": 1, "title": "项目命题"},
            {"artifact_id": "ART-002", "revision": 1, "title": "初步判断"},
        ],
        {"ART-001": "第一篇", "ART-002": "第二篇"},
        "Artifacts",
        "artifact",
    )

    assert "查看全部" not in output
    assert "单页模式" not in output
    assert "toc-toggle" not in output
    assert 'data-mode="all"' not in output


def test_reader_routes_one_document_from_hash_and_browser_history() -> None:
    output = html.generate_html(
        [
            {"artifact_id": "ART-001", "revision": 1, "title": "项目命题"},
            {"artifact_id": "ART-002", "revision": 1, "title": "初步判断"},
        ],
        {"ART-001": "第一篇", "ART-002": "第二篇"},
        "Artifacts",
        "artifact",
    )

    assert output.count('class="doc-section"') == 3
    assert re.search(r"\.doc-section\s*\{[^}]*display:\s*none", output, re.DOTALL)
    assert re.search(
        r"\.doc-section\.active\s*\{[^}]*display:\s*block", output, re.DOTALL
    )
    assert "location.hash" in output
    assert 'window.addEventListener("hashchange"' in output
    assert "history.pushState" in output
    assert 'window.addEventListener("popstate"' in output
    assert "sections[0]" in output


def test_learning_plan_and_progress_merge_into_decision_reader_cards() -> None:
    body = """## Learning Plan

```yaml
- id: LP-002
  learning_objective: 用户是否愿意为结果付费？
  decision_relevance: 决定采用低价工具模式还是服务替代模式
  lens: Consumer
  priority: P1
  ledger_ref: assumption:A-002@1
```

## Research Progress

```yaml
- learning_ref: LP-002
  answer_status: partial
  knowledge_refs: ["knowledge:K-005@1"]
  current_answer: 用户愿意为结果付费，但工具定价与服务定价差异很大
  remaining_gap: 真实付费行为验证
```
"""

    output = html.generate_html(
        [
            {
                "artifact_id": "ART-003",
                "revision": 3,
                "title": "研究结论",
                "kind": "research",
                "stage": "discover",
            }
        ],
        {"ART-003": body},
        "Artifacts",
        "artifact",
    )

    assert "Learning Plan" not in output
    assert "Research Progress" not in output
    assert "关键问题与当前答案" in output
    assert "用户是否愿意为结果付费？" in output
    assert "当前判断" in output
    assert "用户愿意为结果付费，但工具定价与服务定价差异很大" in output
    assert "对决策的影响" in output
    assert "决定采用低价工具模式还是服务替代模式" in output
    assert "还缺什么" in output
    assert "真实付费行为验证" in output
    assert "部分确认" in output

    technical_label = output.index("技术详情")
    details_start = output.rfind("<details", 0, technical_label)
    details_end = output.find("</details>", technical_label)
    learning_id = output.index("LP-002")
    assert details_start != -1 and details_end != -1
    assert details_start < learning_id < details_end
    assert output.count("LP-002") == 1


def test_research_agenda_keeps_every_document_inside_its_doc_section() -> None:
    research = """## Learning Plan

```yaml
- id: LP-001
  learning_objective: 哪个问题最重要？
  decision_relevance: 决定是否继续
```

## Research Progress

```yaml
- learning_ref: LP-001
  answer_status: answered
  current_answer: 已找到答案
```

## Next Sprint

只属于研究文档的下一步。
"""
    output = html.generate_html(
        [
            {
                "artifact_id": "ART-003",
                "revision": 1,
                "title": "研究结论",
                "kind": "research",
            },
            {
                "artifact_id": "ART-010",
                "revision": 1,
                "title": "最终方案",
                "kind": "solution",
            },
        ],
        {"ART-003": research, "ART-010": "方案正文"},
        "Artifacts",
        "artifact",
    )

    parser = _DocsStructureParser()
    parser.feed(output)

    assert parser.errors == []
    research_section = output[output.index('<section id="ART-003"') :]
    research_section = research_section[: research_section.index('<section id="ART-010"')]
    assert "只属于研究文档的下一步。" in research_section


def test_visible_internal_id_sequences_become_plain_language_markers() -> None:
    output = html.generate_html(
        [
            {
                "artifact_id": "ART-003",
                "revision": 3,
                "title": "研究结论",
                "kind": "research",
                "stage": "discover",
            }
        ],
        {
            "ART-003": (
                "正文关联 LP-001/002/007，并由 K-004 和 A-003 支撑；"
                "最终流向 OA-001、CS-002 与 CI-003。"
            )
        },
        "Artifacts",
        "artifact",
    )

    assert ">多个研究问题</span>" in output
    assert ">相关研究</span>" in output
    assert ">关键假设</span>" in output
    assert ">机会方向</span>" in output
    assert ">创意方向</span>" in output
    assert ">概念方案</span>" in output
    assert "LP-001/002/007" in output
    assert "LP-001/002/007，并" not in output
    assert "OA-001、" not in output
    assert "CS-002 与" not in output
    assert "CI-003。" not in output


def test_print_styles_reveal_every_document() -> None:
    output = html.generate_html(
        [
            {"artifact_id": "ART-001", "revision": 1, "title": "项目命题"},
            {"artifact_id": "ART-002", "revision": 1, "title": "初步判断"},
        ],
        {"ART-001": "第一篇", "ART-002": "第二篇"},
        "Artifacts",
        "artifact",
    )

    print_styles = output.split("@media print", maxsplit=1)[1].split(
        "</style>", maxsplit=1
    )[0]
    assert re.search(
        r"\.doc-section\s*\{[^}]*display:\s*block\s*!important",
        print_styles,
        re.DOTALL,
    )


def test_solution_yaml_sections_render_as_readable_fields_with_refs_folded() -> None:
    body = """## Definition

```yaml
name: 日更放大器
pithy_proposition: 每天 30 分钟完成一条视频
what_it_is: AI 预先备料、用户只做关键选择的工作台
who_its_for: 时间有限但希望自己掌握方向的中小企业老板
evidence_refs: ["knowledge:K-004@1"]
```

## How It Works

```yaml
- step: 1
  action: AI 在会话外准备选题、文案和粗剪
  consumer_benefit: 打开工作台即可选择
  design_refs: ["artifact:ART-009@2#CI-001"]
```

## How To Implement

```yaml
- phase: P0 dogfood
  timing: 第 1-2 周
  objective: 跑通完整流程
  dependencies: ["artifact:EXP-001@1"]
```

## How It Makes Money

```yaml
revenue_streams:
  - 服务替代订阅 ¥3,980/月
pricing_and_volume_logic: 按产出单位计价，对标代运营服务
unresolved_model_gaps:
  - 真实价格接受度尚未验证
```

## Validation

```yaml
consumer_desire:
  claim: 用户会为每天 30 分钟的日更能力付费并坚持
  evidence_refs: ["knowledge:K-005@1"]
achilles_assumption_refs: ["assumption:A-030@2"]
experiment_refs: ["artifact:EXP-003@1"]
```
"""

    output = html.generate_html(
        [
            {
                "artifact_id": "ART-010",
                "revision": 1,
                "title": "视频号创始人 IP 日更放大器",
                "kind": "solution",
                "stage": "shape",
            }
        ],
        {"ART-010": body},
        "Artifacts",
        "artifact",
    )

    assert 'class="language-yaml"' not in output
    assert "<pre>" not in output
    assert "<pre><code" not in output
    for visible_text in (
        "方案概览",
        "一句话方案",
        "每天 30 分钟完成一条视频",
        "目标用户",
        "时间有限但希望自己掌握方向的中小企业老板",
        "如何运作",
        "步骤",
        "AI 在会话外准备选题、文案和粗剪",
        "实施路径",
        "阶段",
        "P0 dogfood",
        "商业模式",
        "定价与规模逻辑",
        "按产出单位计价，对标代运营服务",
        "验证重点",
        "当前主张",
        "用户会为每天 30 分钟的日更能力付费并坚持",
    ):
        assert visible_text in output

    technical_details = re.findall(
        r'<details class="technical-details">.*?</details>', output, re.DOTALL
    )
    assert technical_details
    public_output = re.sub(
        r'<details class="technical-details">.*?</details>', "", output, flags=re.DOTALL
    )
    for internal_ref in ("K-004", "ART-009", "EXP-001", "K-005", "A-030", "EXP-003"):
        assert internal_ref in "".join(technical_details)
        assert internal_ref not in public_output


def test_document_and_validation_status_are_both_shown_in_plain_chinese() -> None:
    output = html.generate_html(
        [
            {
                "artifact_id": "ART-010",
                "revision": 1,
                "title": "最终方案",
                "kind": "solution",
                "stage": "shape",
                "document_status": "final",
                "validation_status": "unvalidated",
            }
        ],
        {"ART-010": "方案正文"},
        "Artifacts",
        "artifact",
    )

    metadata = re.search(
        r'<div class="doc-meta" aria-label="文档元数据">(?P<body>.*?)</div>',
        output,
        re.DOTALL,
    )
    assert metadata is not None
    assert '<span class="meta-pill is-complete">已定稿</span>' in metadata.group("body")
    assert '<span class="meta-pill is-working">待验证</span>' in metadata.group("body")


def test_artifact_server_markup_defaults_to_case_journey_and_hides_documents() -> None:
    output = html.generate_html(
        [
            {
                "artifact_id": "ART-001",
                "revision": 1,
                "title": "项目命题",
                "kind": "charter",
                "stage": "immersion",
            },
            {
                "artifact_id": "ART-010",
                "revision": 1,
                "title": "最终方案",
                "kind": "solution",
                "stage": "shape",
            },
            {
                "artifact_id": "ART-003",
                "revision": 1,
                "title": "研究结论",
                "kind": "research",
                "stage": "discover",
            },
        ],
        {"ART-001": "命题", "ART-010": "方案", "ART-003": "结论"},
        "Artifacts",
        "artifact",
    )

    section_attrs = dict(
        re.findall(r'<section id="([^"]+)" class="doc-section"([^>]*)>', output)
    )
    assert set(section_attrs) == {"case-journey", "ART-001", "ART-003", "ART-010"}
    assert (
        sum('data-default="true"' in attrs for attrs in section_attrs.values()) == 1
    )
    assert 'data-default="true"' in section_attrs["case-journey"]
    assert " hidden" not in section_attrs["case-journey"]
    assert " hidden" in section_attrs["ART-010"]
    assert " hidden" in section_attrs["ART-001"]
    assert " hidden" in section_attrs["ART-003"]


def test_concept_portfolio_renders_cards_and_svg_wireframe() -> None:
    items = [
        {
            "artifact_id": "ART-009",
            "revision": 2,
            "title": "Concept Portfolio · 概念筛选",
            "kind": "concept-portfolio",
            "stage": "ideate",
            "concepts": [
                {
                    "id": "CI-001",
                    "name": "30分钟选择会话",
                    "pithy_description": "半小时日更",
                    "consumer_insight": "时间破产",
                    "commercial_insight": "续费闭环",
                    "idea_definition": "每晚 30 分钟选择会话",
                    "who_its_for": "老板",
                    "how_it_works": "会话外预处理",
                    "what_it_replaces": "3-8 小时自剪",
                    "why_big": "把日更改成流程问题",
                    "visualization": "三屏：选题/文案/发布",
                    "visualization_spec": {
                        "screens": [
                            {"caption": "候选选题", "bullets": ["3 个选题"]},
                            {"caption": "确认发布", "bullets": ["倒计时"]},
                        ]
                    },
                    "design_principles": ["只选择不创作"],
                    "dual_sided": {
                        "magic": {
                            "consumer_value_proposition": {"statement": "30 分钟拍板"},
                            "consumer_target": {"statement": "老板"},
                        },
                        "money": {
                            "commercial_value_proposition": {"statement": "续费载体"},
                            "leverageable_assets": {"statement": "行为数据"},
                        },
                        "tension": {"statement": "纪律 vs 波动"},
                        "balance_choice": "magic",
                    },
                    "evaluation": {
                        "hard": {"lineage": True, "tension": True},
                        "soft": {"comprehension": "4/5"},
                    },
                    "recommended_action": "refine",
                    "decision": "selected",
                },
            ],
            "exit": {"selected_concept_ids": ["CI-001"]},
        }
    ]
    output = html.generate_html(
        items, {"ART-009": "## 推荐动作分布\n\nrefine 1 条"}, "Artifacts", "artifact"
    )

    assert "概念卡" in output
    assert "30分钟选择会话" in output
    assert "时间破产" in output
    assert 'class="concept-wireframe"' in output
    assert "候选选题" in output
    assert "已选" in output
    assert "双面（Money+Magic）" in output
    assert "硬标准" in output


def test_concept_portfolio_projects_visualization_text_to_svg_without_spec() -> None:
    items = [
        {
            "artifact_id": "ART-009",
            "revision": 2,
            "title": "Concept Portfolio · 概念筛选",
            "kind": "concept-portfolio",
            "concepts": [
                {
                    "id": "CI-002",
                    "name": "天级战报",
                    "visualization": "次日清晨一条战报",
                }
            ],
        }
    ]
    output = html.generate_html(items, {"ART-009": "正文"}, "Artifacts", "artifact")

    assert "天级战报" in output
    assert "次日清晨一条战报" in output
    assert 'class="concept-wireframe"' in output
    assert "concept-visualization-fallback" not in output


def _seed(seed_id: str, *, idea: str | None = None) -> dict:
    return {
        "id": seed_id,
        "idea": idea or f"Idea {seed_id}",
        "source_insight_refs": [f"insight:ART-004@2:{seed_id}"],
        "cluster_id": "cluster-a",
        "strategy_filter": "pass",
    }


def test_parse_md_keeps_canonical_ideate_decision_fields(tmp_path: Path) -> None:
    path = tmp_path / "ART-008-r1-idea-pool.md"
    path.write_text(
        """---
artifact_id: ART-008
revision: 1
kind: idea-pool
opportunity_areas:
  - opportunity_area_id: OA-001
    seeds: [{id: CS-001, idea: Canonical Idea}]
review: {status: ready}
decisions: [{type: confirm-shortlist}]
html_projection: {rationale: SHADOW CONTENT}
---
Body
""",
        encoding="utf-8",
    )

    metadata, _ = html.parse_md(path)

    assert metadata is not None
    assert metadata["opportunity_areas"][0]["seeds"][0]["idea"] == "Canonical Idea"
    assert metadata["review"] == {"status": "ready"}
    assert metadata["decisions"] == [{"type": "confirm-shortlist"}]
    assert "html_projection" not in metadata


def test_idea_pool_renders_complete_oa_decision_evidence_and_read_only_filters() -> None:
    seeds = [_seed(f"CS-{index:03d}") for index in range(1, 11)]
    item = {
        "artifact_id": "ART-008",
        "revision": 3,
        "kind": "idea-pool",
        "opportunity_areas": [
            {
                "opportunity_area_id": "OA-001",
                "seeds": seeds,
                "review": {
                    "status": "ready",
                    "iterations": 1,
                    "findings": ["机制覆盖足够"],
                },
                "shortlist": {
                    "recommended_cuts": [
                        {
                            "seed_id": "CS-009",
                            "reason": "duplicate",
                            "rationale": "与 CS-003 使用同一机制",
                        },
                        {
                            "seed_id": "CS-010",
                            "reason": "weak-distinctiveness",
                            "rationale": "更像设计原则",
                        },
                    ],
                    "confirmed": [
                        "CS-001",
                        "CS-002",
                        "CS-003",
                        "CS-004",
                        "CS-005",
                    ],
                },
            }
        ],
    }

    output = html.generate_html([item], {"ART-008": "说明正文"}, "Artifacts", "artifact")

    assert 'class="idea-pool-view"' in output
    assert 'data-oa="OA-001"' in output
    assert "10 个 Idea" in output
    assert "建议保留 8" in output
    assert "已确认 5" in output
    assert "机制覆盖足够" in output
    assert "与 CS-003 使用同一机制" in output
    assert "duplicate" in output
    for seed in seeds:
        assert seed["id"] in output
        assert seed["idea"] in output
    assert output.count('data-recommendation="keep"') == 8
    assert output.count('<article class="idea-row" data-oa="OA-001" data-recommendation="cut"') == 2
    assert 'data-confirmation="confirmed"' in output
    assert 'data-idea-filter="all"' in output
    assert 'data-idea-filter="keep"' in output
    assert 'data-idea-filter="cut"' in output
    assert "请在对话中返回每个机会方向要确认的 5–8 个 CS- ID" in output


def test_idea_pool_projects_existing_elimination_without_legacy_display() -> None:
    item = {
        "artifact_id": "ART-008",
        "revision": 2,
        "kind": "idea-pool",
        "opportunity_areas": [
            {
                "opportunity_area_id": "OA-001",
                "seeds": [_seed("CS-001"), _seed("CS-002")],
                "shortlist": {
                    "recommended": ["CS-002"],
                    "confirmed": ["CS-001", "CS-002"],
                },
            }
        ],
    }

    output = html.generate_html([item], {"ART-008": "Artifact 正文理由"}, "Artifacts", "artifact")

    assert "旧版" not in output
    assert "未按新契约" not in output
    assert 'data-recommendation="cut"' in output
    assert "Artifact 未提供结构化淘汰理由" in output
    assert "请在对话中返回每个机会方向" in output


def test_needs_revision_idea_pool_does_not_present_confirmation_handoff() -> None:
    item = {
        "artifact_id": "ART-008",
        "revision": 1,
        "kind": "idea-pool",
        "opportunity_areas": [
            {
                "opportunity_area_id": "OA-001",
                "seeds": [_seed("CS-001")],
                "review": {"status": "needs-revision", "findings": ["创意重复"]},
                "shortlist": {"recommended_cuts": [], "confirmed": []},
            }
        ],
    }

    output = html.generate_html([item], {"ART-008": "正文"}, "Artifacts", "artifact")

    assert "待修订，暂不进入人工确认" in output
    assert "请在对话中返回每个机会方向" not in output


def _concept(
    concept_id: str,
    oa: str,
    *,
    decision: str | None = None,
    merge_into: str | None = None,
    action: str = "refine",
) -> dict:
    return {
        "id": concept_id,
        "opportunity_area_id": oa,
        "source_seed_id": concept_id.replace("CI", "CS"),
        "name": f"Concept {concept_id}",
        "pithy_description": f"Pithy {concept_id}",
        "consumer_insight": f"Consumer {concept_id}",
        "commercial_insight": f"Commercial {concept_id}",
        "idea_definition": f"What {concept_id}",
        "who_its_for": f"Who {concept_id}",
        "how_it_works": f"Mechanism {concept_id}",
        "what_it_replaces": f"Replace {concept_id}",
        "why_big": f"Big {concept_id}",
        "dual_sided": {
            "magic": {
                "consumer_value_proposition": {"statement": f"Magic {concept_id}"}
            },
            "money": {
                "commercial_value_proposition": {"statement": f"Money {concept_id}"}
            },
            "tension": {"statement": f"Tension {concept_id}"},
        },
        "evaluation": {
            "hard": {"lineage": True},
            "soft": {"comprehension": "4/5"},
            "recommended_action": action,
        },
        "assumption_refs": [f"assumption:A-{concept_id[-3:]}@1"],
        "decision": decision,
        "merge_into": merge_into,
    }


def test_concept_portfolio_groups_comparison_and_separates_active_history() -> None:
    concepts = [
        _concept("CI-001", "OA-001", decision="selected"),
        _concept("CI-002", "OA-002", action="pivot"),
        _concept("CI-003", "OA-002", decision="merged", merge_into="CI-004"),
        _concept("CI-004", "OA-002"),
    ]
    item = {
        "artifact_id": "ART-009",
        "revision": 3,
        "kind": "concept-portfolio",
        "review": {
            "status": "ready",
            "iterations": 2,
            "reviewed_concept_ids": ["CI-001", "CI-002", "CI-004"],
            "portfolio_findings": [
                {
                    "concept_ids": ["CI-002", "CI-003"],
                    "issue": "mechanism-overlap",
                    "recommendation": "merge",
                }
            ],
        },
        "concepts": concepts,
        "exit": {"selected_concept_ids": ["CI-001"]},
    }

    output = html.generate_html([item], {"ART-009": "说明正文"}, "Artifacts", "artifact")

    assert 'class="concept-comparison"' in output
    assert "OA-001" in output and "OA-002" in output
    assert "Mechanism CI-002" in output
    assert "Magic CI-002" in output
    assert "Money CI-002" in output
    assert "mechanism-overlap" in output
    assert "pivot" in output
    assert "assumption:A-002@1" in output
    assert output.count('data-concept-status="active"') >= 3
    assert output.count('data-concept-status="history"') >= 1
    assert '<details class="concept-history">' in output
    comparison = re.search(
        r'<div class="concept-comparison">(?P<body>.*?)</div>', output, re.DOTALL
    )
    assert comparison is not None
    assert "Concept CI-001" in comparison.group("body")
    assert "Concept CI-002" in comparison.group("body")
    assert "Concept CI-004" in comparison.group("body")
    assert "Concept CI-003" not in comparison.group("body")
    assert 'data-concept-filter="oa"' in output
    assert 'data-concept-filter="action"' in output
    assert 'data-concept-filter="decision"' in output
    assert "请在对话中返回跨全部机会方向最终选择的 2–4 个 CI- ID" in output


def test_concept_portfolio_existing_evaluation_and_needs_revision_handoffs() -> None:
    existing = {
        "artifact_id": "ART-009",
        "revision": 1,
        "kind": "concept-portfolio",
        "concepts": [_concept("CI-001", "OA-001")],
        "exit": {"selected_concept_ids": []},
    }
    needs_revision = {
        **existing,
        "artifact_id": "ART-010",
        "review": {"status": "needs-revision", "portfolio_findings": []},
    }

    output = html.generate_html(
        [existing, needs_revision],
        {"ART-009": "现有评价", "ART-010": "待修订"},
        "Artifacts",
        "artifact",
    )

    existing_section = output[output.index('<section id="ART-009"') : output.index('<section id="ART-010"')]
    needs_section = output[output.index('<section id="ART-010"') :]
    assert "旧版" not in existing_section
    assert "未按新契约" not in existing_section
    assert "请在对话中返回跨全部机会方向" in existing_section
    assert "待修订，暂不进入最终 Concept 选择" in needs_section
    assert "请在对话中返回跨全部机会方向" not in needs_section


def test_artifact_reader_defaults_to_derived_case_journey() -> None:
    items = [
        {"artifact_id": "ART-010", "revision": 1, "kind": "solution", "stage": "shape"},
        {
            "artifact_id": "ART-008",
            "revision": 2,
            "kind": "idea-pool",
            "stage": "ideate",
            "opportunity_areas": [
                {
                    "opportunity_area_id": "OA-001",
                    "seeds": [_seed("CS-001"), _seed("CS-002")],
                    "shortlist": {"recommended": ["CS-002"], "confirmed": ["CS-001"]},
                }
            ],
        },
        {
            "artifact_id": "ART-009",
            "revision": 2,
            "kind": "concept-portfolio",
            "stage": "ideate",
            "concepts": [_concept("CI-001", "OA-001", decision="selected")],
            "exit": {"selected_concept_ids": ["CI-001"]},
        },
    ]

    output = html.generate_html(
        items,
        {"ART-008": "Ideas", "ART-009": "Concepts", "ART-010": "Solution"},
        "Artifacts",
        "artifact",
    )

    assert '<section id="case-journey" class="doc-section"' in output
    journey_attrs = re.search(
        r'<section id="case-journey" class="doc-section"(?P<attrs>[^>]*)>', output
    )
    assert journey_attrs is not None
    assert 'data-default="true"' in journey_attrs.group("attrs")
    assert 'href="#case-journey"' in output
    assert 'href="#ART-008"' in output and 'href="#ART-009"' in output
    assert "2 Ideas" in output
    assert "1 active Concepts" in output
    journey_start = output.index('<section id="case-journey"')
    journey = output[journey_start : output.index('</section>', journey_start)]
    assert journey.index('href="#ART-008"') < journey.index('href="#ART-009"')
    assert journey.index('href="#ART-009"') < journey.index('href="#ART-010"')
    solution = re.search(r'<section id="ART-010" class="doc-section"(?P<attrs>[^>]*)>', output)
    assert solution is not None and " hidden" in solution.group("attrs")


def test_case_journey_projects_missing_review_without_legacy_status() -> None:
    item = {
        "artifact_id": "ART-008",
        "revision": 1,
        "kind": "idea-pool",
        "opportunity_areas": [
            {
                "opportunity_area_id": "OA-001",
                "seeds": [_seed("CS-001")],
                "review": {"status": "ready"},
            },
            {
                "opportunity_area_id": "OA-002",
                "seeds": [_seed("CS-002")],
            },
        ],
    }

    output = html.generate_html([item], {"ART-008": "正文"}, "Artifacts", "artifact")
    journey_start = output.index('<section id="case-journey"')
    journey = output[journey_start : output.index('</section>', journey_start)]

    assert "legacy" not in journey
    assert "<small>artifact</small>" in journey
    assert "<small>ready</small>" not in journey


def test_decision_views_only_use_artifact_markdown_as_business_source(tmp_path: Path) -> None:
    artifacts = tmp_path / "_bewater-output" / "artifacts"
    artifacts.mkdir(parents=True)
    (artifacts / "ART-008-r1-idea-pool.md").write_text(
        """---
artifact_id: ART-008
revision: 1
kind: idea-pool
opportunity_areas:
  - opportunity_area_id: OA-001
    seeds:
      - id: CS-001
        idea: CANONICAL FRONTMATTER IDEA
    shortlist:
      recommended: [CS-001]
      confirmed: []
html_projection:
  rationale: FABRICATED SHADOW RATIONALE
---
# Idea Pool

BODY EXPLANATORY NOTE
""",
        encoding="utf-8",
    )

    html.build_html(tmp_path)
    output = (tmp_path / "_bewater-output" / "html" / "artifacts.html").read_text(
        encoding="utf-8"
    )

    assert "CANONICAL FRONTMATTER IDEA" in output
    assert "BODY EXPLANATORY NOTE" in output
    assert "FABRICATED SHADOW RATIONALE" not in output
    assert "未提供结构化淘汰理由" in output
    assert "fetch(" not in output
    assert "localStorage" not in output
