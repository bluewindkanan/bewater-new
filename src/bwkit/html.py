"""Build self-contained HTML readers from BeWater Markdown documents."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from typing import Any

import markdown
import yaml

from .concept_visualization import render_concept_visualization

KNOWLEDGE_REF = re.compile(r"knowledge:(K-\d+)@(\d+)")
ARTIFACT_REF = re.compile(r"artifact:((?:ART|EXP)-\d+)@(\d+)")
H1_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
LEARNING_PLAN_RE = re.compile(
    r"## Learning Plan\s*\n```yaml\n(.*?)```",
    re.DOTALL,
)
RESEARCH_PROGRESS_RE = re.compile(
    r"## Research Progress\s*\n```yaml\n(.*?)```",
    re.DOTALL,
)
FENCED_YAML_RE = re.compile(r"```yaml\s*\n(.*?)```", re.DOTALL)
TYPED_REF_CODE_RE = re.compile(
    r"`((?:knowledge:K-\d+|artifact:(?:ART|EXP)-\d+)@\d+(?:#[\w-]+)?)`"
)
INTERNAL_TOKEN_RE = re.compile(
    r"(?<![\w:#])(?P<token>(?P<prefix>A|LP|RM|K|OA|CS|CI)-\d{3}(?:/\d{3})*(?:@\d+)?)"
    r"(?![\w/])"
)

FRONTMATTER_FIELDS = {
    "knowledge_id",
    "artifact_id",
    "title",
    "status",
    "document_status",
    "validation_status",
    "revision",
    "kind",
    "stage",
    "opportunity_areas",
    "review",
    "decisions",
    "concepts",
    "exit",
}

SECTION_MAP = {
    "Intent trace": "意图记录",
    "Original intent": "原始意图",
    "Project definition": "项目定义",
    "Current knowledge state": "当前认知",
    "Research Objective": "研究背景与边界",
    "Next Sprint": "下一步研究",
    "Sprint Decision": "研究结论",
    "Insight Ingredients and Insight Readiness": "洞察原料与就绪度",
    "Definition": "方案概览",
    "How It Works": "如何运作",
    "How To Implement": "实施路径",
    "How It Makes Money": "商业模式",
    "Validation": "验证重点",
    "Question or hypothesis": "研究问题",
    "Method and scope": "方法与范围",
    "Sources used": "资料来源",
    "Summary": "总结",
    "Conclusion": "结论",
    "Limitations and new questions": "局限与新问题",
    "1. Overall Preliminary Conclusion": "总体初步结论",
    "2. Professional Perspectives": "专业视角",
    "3. Material Risks & Unknowns (pre-mortem)": "主要风险与未知",
    "4. What to Inspect Next": "下一步需要查清",
    "5. Research Boundary & Sources": "研究边界与来源",
}

HEADING_PREFIX_MAP = {
    "选择与锁定": "最终战略选择",
    "短名单汇总": "入选创意",
    "推荐动作分布": "概念建议",
    "人工决策记录": "已选概念",
    "区域": "机会方向",
}

NAV_LABELS = {
    "charter": "项目命题",
    "initial-assessment": "初步判断",
    "research": "研究结论",
    "insights": "核心洞察",
    "directional-hypothesis": "战略假设",
    "strategy-statement": "战略选择",
    "opportunity": "机会方向",
    "idea-pool": "创意方向",
    "concept-portfolio": "概念筛选",
    "solution": "最终方案",
    "experiment": "关键实验",
}

NAV_GROUPS = (
    ("理解问题", {"charter", "initial-assessment"}),
    (
        "形成战略",
        {
            "research",
            "insights",
            "directional-hypothesis",
            "strategy-statement",
            "opportunity",
        },
    ),
    ("形成方案", {"idea-pool", "concept-portfolio", "solution"}),
    ("验证风险", {"experiment"}),
)

STATUS_LABELS = {
    "complete": "已完成",
    "final": "已定稿",
    "working": "进行中",
    "draft": "草案",
    "answered": "已回答",
    "partial": "部分确认",
    "gap-accepted": "暂无公开证据",
    "unknown": "待研究",
    "planned": "待研究",
}

FIELD_LABELS = {
    "name": "名称",
    "pithy_proposition": "一句话方案",
    "pithy_description": "一句话描述",
    "what_it_is": "方案说明",
    "who_its_for": "目标用户",
    "dual_sided": "双重价值",
    "money": "商业价值",
    "magic": "用户价值",
    "tension": "核心张力",
    "balance_choice": "取舍",
    "consumer_value_proposition": "用户价值主张",
    "commercial_value_proposition": "商业价值主张",
    "consumer_target": "目标用户",
    "leverageable_assets": "可积累资产",
    "dimensions": "关键维度",
    "path_to_market": "市场进入方式",
    "right_to_win": "获胜理由",
    "product_or_service_platform": "产品形态",
    "source_of_business": "收入来源",
    "product_or_service_design": "产品设计",
    "enabling_technology": "关键技术",
    "reason_to_believe": "可信理由",
    "branding": "品牌表达",
    "consumer_experience": "用户体验",
    "step": "步骤",
    "action": "行动",
    "consumer_benefit": "用户收益",
    "operational_benefit": "运营收益",
    "strategic_rationale": "战略理由",
    "legal_regulatory_rationale": "合规考虑",
    "phase": "阶段",
    "timing": "时间",
    "objective": "目标",
    "jobs_to_be_done": "要完成的工作",
    "capabilities_and_assets": "所需能力与资产",
    "owner": "负责人",
    "dependencies": "依赖",
    "risks": "风险",
    "open_questions": "待回答问题",
    "pilot_and_rollout": "试点与推广标准",
    "revenue_streams": "收入来源",
    "pricing_and_volume_logic": "定价与规模逻辑",
    "adoption_retention_frequency_assumptions": "采用与留存假设",
    "development_and_operating_costs": "开发与运营成本",
    "scenarios": "情景测算",
    "sensitivity": "敏感性",
    "unresolved_model_gaps": "尚未验证的缺口",
    "consumer_desire": "用户需求",
    "commercial_value": "商业价值",
    "claim": "当前主张",
    "assumption": "假设",
    "source": "依据",
    "method": "方法",
    "evidence_needed": "所需证据",
    "bounded_budget": "投入上限",
    "stop_condition": "停止条件",
    "expected_output": "预期产出",
    "limitation": "局限",
    "exclusions": "不包含",
    "method_source_bundle": "方法组合",
    "feasibility_and_implementation": "可行性与实施",
    "invalidated_claims": "已证伪主张",
    "base": "基准情景",
    "aggressive": "积极情景",
    "revenue": "营收",
    "margin": "毛利率",
    "earnings": "收益",
    "investment": "投入",
    "payback": "回收期",
    "current_answer": "当前判断",
    "remaining_gap": "还缺什么",
    "decision_relevance": "对决策的影响",
    "id": "记录编号",
    "priority": "优先级",
    "lens": "研究视角",
    "starting_state": "初始认知状态",
    "starting_view": "初始判断",
    "ledger_ref": "关联假设",
    "knowledge_refs": "支撑研究",
    "evidence_refs": "支撑证据",
    "design_refs": "来源概念",
}

SOLUTION_HIDDEN_FIELDS = {
    "方案概览": {
        "product_or_service_platform",
        "source_of_business",
        "product_or_service_design",
        "enabling_technology",
        "branding",
    },
    "如何运作": {
        "operational_benefit",
        "strategic_rationale",
        "legal_regulatory_rationale",
    },
    "实施路径": {
        "jobs_to_be_done",
        "capabilities_and_assets",
        "dependencies",
        "risks",
        "open_questions",
        "pilot_and_rollout",
    },
    "商业模式": {
        "adoption_retention_frequency_assumptions",
        "development_and_operating_costs",
        "scenarios",
        "sensitivity",
    },
}

EXPERIMENT_TERMS = (
    ("Van Westendorp", "价格敏感度测试"),
    ("guerrilla interview", "快速访谈"),
    ("related-worlds", "类比研究"),
    ("fake-website", "模拟订阅页"),
    ("dogfood", "自用验证"),
    ("demo", "演示"),
)

PROMOTED_SECTIONS = {
    "knowledge": ("结论", "总结"),
    "initial-assessment": ("总体初步结论", "主要风险与未知"),
    "research": ("研究结论", "洞察原料与就绪度", "关键问题与当前答案"),
    "strategy-statement": ("最终战略选择",),
    "opportunity": ("机会方向",),
    "idea-pool": ("入选创意",),
    "concept-portfolio": ("已选概念", "概念建议"),
    "solution": ("方案概览",),
}

FOLDED_SECTIONS = {
    "knowledge": ((2, "方法与范围"), (2, "资料来源")),
    "charter": ((3, "意图记录"), (3, "原始意图")),
    "initial-assessment": ((3, "专业视角"), (3, "研究边界与来源")),
    "research": ((2, "研究背景与边界"),),
    "strategy-statement": ((3, "候选"),),
    "idea-pool": ((2, "OA-"),),
    "solution": ((2, "实施路径"),),
}

MARKDOWN_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]


def parse_md(path: Path) -> tuple[dict[str, Any] | None, str]:
    """Return selected YAML frontmatter fields and the Markdown body."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text

    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return None, text

    loaded = yaml.safe_load(text[4:end])
    if not isinstance(loaded, dict):
        return None, text

    metadata = {
        key: value for key, value in loaded.items() if key in FRONTMATTER_FIELDS
    }
    return metadata, text[end + 5 :]


def _doc_id(item: dict[str, Any]) -> str:
    value = item.get("knowledge_id") or item.get("artifact_id") or ""
    return str(value)


def _revision(item: dict[str, Any]) -> int:
    value = item.get("revision", 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _plain_heading(text: str) -> str:
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*_`~]", "", text).strip()


def _normalize_document(
    metadata: dict[str, Any], body: str
) -> tuple[dict[str, Any], str]:
    normalized = dict(metadata)
    normalized["revision"] = _revision(normalized)

    h1 = H1_RE.search(body)
    h1_title = _plain_heading(h1.group(1)) if h1 else ""
    title = str(normalized.get("title") or "").strip()
    if not title and h1_title:
        normalized["title"] = h1_title
        title = h1_title

    if h1 and (not title or h1_title == title):
        body = f"{body[:h1.start()]}{body[h1.end():]}"

    return normalized, body.strip()


def clean_content(body: str, doc_type: str = "") -> str:
    """Translate standard section headings without flattening Markdown."""
    del doc_type
    for source, translated in SECTION_MAP.items():
        pattern = rf"^(#{{2,6}})\s+{re.escape(source)}\s*$"
        body = re.sub(
            pattern,
            lambda match, translated=translated: f"{match.group(1)} {translated}",
            body,
            flags=re.MULTILINE,
        )
    for source, translated in HEADING_PREFIX_MAP.items():
        pattern = rf"^(#{{2,6}})\s+{re.escape(source)}(?P<suffix>.*?)\s*$"
        body = re.sub(
            pattern,
            lambda match, translated=translated: (
                f"{match.group(1)} {translated}{match.group('suffix')}"
            ),
            body,
            flags=re.MULTILINE,
        )
    return body.strip()


def _safe_yaml(value: str) -> Any:
    try:
        return yaml.safe_load(value)
    except yaml.YAMLError:
        return None


def _is_technical_key(key: str) -> bool:
    return (
        key in {"id", "item_revision", "revision_attempts", "schema_version"}
        or key.endswith(("_id", "_ids", "_ref", "_refs"))
        or key.startswith(("source_", "derived_"))
    )


def _field_label(key: str) -> str:
    return FIELD_LABELS.get(key, key.replace("_", " ").strip().capitalize())


def _scalar_text(value: Any) -> str:
    if value is None:
        return "未设置"
    if isinstance(value, bool):
        return "是" if value else "否"
    text = str(value)
    return STATUS_LABELS.get(text, text)


def _render_structured_value(
    value: Any,
    *,
    show_technical: bool = False,
    hidden_keys: set[str] | None = None,
) -> str:
    hidden_keys = hidden_keys or set()
    if isinstance(value, dict):
        rows: list[str] = []
        technical: list[str] = []
        for raw_key, child in value.items():
            key = str(raw_key)
            target = (
                technical
                if (_is_technical_key(key) or key in hidden_keys) and not show_technical
                else rows
            )
            if isinstance(child, (dict, list)):
                target.append(
                    '<div class="structured-group">'
                    f'<h4>{escape(_field_label(key))}</h4>'
                    f'{_render_structured_value(child, show_technical=show_technical, hidden_keys=hidden_keys)}'
                    '</div>'
                )
            else:
                target.append(
                    '<div class="structured-row">'
                    f'<dt>{escape(_field_label(key))}</dt>'
                    f'<dd>{escape(_scalar_text(child))}</dd>'
                    '</div>'
                )
        public_html = f'<dl class="structured-data">{"".join(rows)}</dl>'
        if technical:
            public_html += (
                '<details class="technical-details">'
                '<summary>技术详情</summary>'
                f'<div class="technical-body">{"".join(technical)}</div>'
                '</details>'
            )
        return public_html
    if isinstance(value, list):
        if not value:
            return '<p class="empty-value">暂无</p>'
        items = "".join(
            f'<li>{_render_structured_value(item, show_technical=show_technical, hidden_keys=hidden_keys)}</li>'
            for item in value
        )
        return f'<ul class="structured-list">{items}</ul>'
    return f'<span>{escape(_scalar_text(value))}</span>'


def convert_yaml_blocks(body: str, doc_type: str = "") -> str:
    """Render structured YAML as scannable disclosure content instead of code."""

    def replace_yaml(match: re.Match[str]) -> str:
        loaded = _safe_yaml(match.group(1))
        if loaded is None:
            return match.group(0)
        preceding = body[:match.start()]
        headings = re.findall(r"^##\s+(.+?)\s*$", preceding, flags=re.MULTILINE)
        heading = headings[-1] if headings else ""
        hidden_keys = SOLUTION_HIDDEN_FIELDS.get(heading, set()) if doc_type == "solution" else set()
        return (
            '\n<div class="structured-block">'
            f'{_render_structured_value(loaded, hidden_keys=hidden_keys)}'
            '</div>\n'
        )

    return FENCED_YAML_RE.sub(replace_yaml, body)


def convert_research_agenda(body: str) -> str:
    """Merge Learning Plan intent and Research Progress into decision questions."""
    plan_match = LEARNING_PLAN_RE.search(body)
    if not plan_match:
        return body

    plan = _safe_yaml(plan_match.group(1))
    progress_match = RESEARCH_PROGRESS_RE.search(body)
    progress = _safe_yaml(progress_match.group(1)) if progress_match else []
    if not isinstance(plan, list):
        return body
    if progress_match and not isinstance(progress, list):
        return body

    plan_ids = [
        str(row.get("id") or "")
        for row in plan
        if isinstance(row, dict)
    ]
    progress_ids = [
        str(row.get("learning_ref") or "")
        for row in progress or []
        if isinstance(row, dict)
    ]
    if (
        len(plan_ids) != len(plan)
        or not all(plan_ids)
        or len(set(plan_ids)) != len(plan_ids)
        or len(progress_ids) != len(progress or [])
        or len(set(progress_ids)) != len(progress_ids)
        or any(item_id not in set(plan_ids) for item_id in progress_ids)
    ):
        return body

    progress_by_ref = {
        str(row.get("learning_ref")): row
        for row in progress or []
        if isinstance(row, dict) and row.get("learning_ref")
    }
    agenda_items: list[str] = []
    for row in plan:
        if not isinstance(row, dict):
            continue
        item_id = str(row.get("id") or "")
        answer = progress_by_ref.get(item_id, {})
        status = str(answer.get("answer_status") or "unknown")
        status_label = STATUS_LABELS.get(status, status)
        priority = "现在必须搞清楚" if row.get("priority") == "P1" else "随后验证"
        current_answer = answer.get("current_answer") or row.get("starting_view") or "尚无结论"
        gap = answer.get("remaining_gap") or "暂无显式缺口"
        technical = {
            "id": item_id,
            "priority": row.get("priority"),
            "lens": row.get("lens"),
            "starting_state": row.get("starting_state"),
            "starting_view": row.get("starting_view"),
            "ledger_ref": row.get("ledger_ref"),
            "knowledge_refs": answer.get("knowledge_refs"),
        }
        for key, value in row.items():
            if key not in {
                "id",
                "priority",
                "lens",
                "starting_state",
                "starting_view",
                "ledger_ref",
                "learning_objective",
                "decision_relevance",
            }:
                technical[key] = value
        for key, value in answer.items():
            if key not in {
                "learning_ref",
                "answer_status",
                "knowledge_refs",
                "current_answer",
                "remaining_gap",
            }:
                technical[key] = value
        agenda_items.append(
            '<article class="learning-item">'
            '<header class="learning-header">'
            f'<h3>{escape(str(row.get("learning_objective") or "待明确的问题"))}</h3>'
            '<div class="learning-status">'
            f'<span class="status-badge status-{escape(status, quote=True)}">{escape(status_label)}</span>'
            f'<span class="priority-label">{priority}</span>'
            '</div>'
            '</header>'
            '<dl class="decision-fields">'
            f'<div><dt>当前判断</dt><dd>{escape(str(current_answer))}</dd></div>'
            f'<div><dt>对决策的影响</dt><dd>{escape(str(row.get("decision_relevance") or "待明确"))}</dd></div>'
            f'<div><dt>还缺什么</dt><dd>{escape(str(gap))}</dd></div>'
            '</dl>'
            '<details class="technical-details">'
            '<summary>技术详情</summary>'
            f'{_render_structured_value(technical, show_technical=True)}'
            '</details>'
            '</article>'
        )

    replacement = (
        '\n<h2>关键问题与当前答案</h2>'
        '<div class="learning-agenda">'
        f'{"".join(agenda_items)}'
        '</div>\n'
    )
    body = LEARNING_PLAN_RE.sub(replacement, body, count=1)
    if progress_match:
        body = RESEARCH_PROGRESS_RE.sub("", body, count=1)
    return body


def convert_refs(body: str, page_kind: str) -> str:
    """Convert typed references to local or cross-reader links with citation styling."""

    def knowledge_link(match: re.Match[str]) -> str:
        doc_id, revision = match.groups()
        href = f"#{doc_id}" if page_kind == "knowledge" else f"knowledge.html#{doc_id}"
        short_id = doc_id.split("-")[1] if "-" in doc_id else doc_id
        return f'<a href="{href}" class="ref" title="{doc_id}@{revision}">[{short_id}]</a>'

    def artifact_link(match: re.Match[str]) -> str:
        doc_id, revision = match.groups()
        href = f"#{doc_id}" if page_kind == "artifact" else f"artifacts.html#{doc_id}"
        short_id = doc_id.split("-")[1] if "-" in doc_id else doc_id
        return f'<a href="{href}" class="ref" title="{doc_id}@{revision}">[{short_id}]</a>'

    body = KNOWLEDGE_REF.sub(knowledge_link, body)
    return ARTIFACT_REF.sub(artifact_link, body)


def convert_internal_tokens(body: str) -> str:
    """Replace visible workflow IDs with plain-language labels and keep IDs on hover."""
    labels = {
        "A": ("关键假设", "多个关键假设"),
        "LP": ("研究问题", "多个研究问题"),
        "RM": ("监控任务", "多个监控任务"),
        "K": ("相关研究", "多项相关研究"),
        "OA": ("机会方向", "多个机会方向"),
        "CS": ("创意方向", "多个创意方向"),
        "CI": ("概念方案", "多个概念方案"),
    }

    def replace(match: re.Match[str]) -> str:
        token = match.group("token")
        singular, plural = labels[match.group("prefix")]
        label = plural if "/" in token else singular
        return (
            f'<span class="internal-marker" title="{escape(token, quote=True)}">'
            f'{label}</span>'
        )

    return INTERNAL_TOKEN_RE.sub(replace, body)


def _render_markdown(body: str, page_kind: str, doc_type: str = "") -> str:
    body = convert_research_agenda(body)
    body = clean_content(body)
    body = convert_yaml_blocks(body, doc_type)
    body = TYPED_REF_CODE_RE.sub(r"\1", body)
    body = convert_internal_tokens(body)
    body = convert_refs(body, page_kind)
    return markdown.markdown(
        body,
        extensions=MARKDOWN_EXTENSIONS,
        output_format="html5",
    )


def _kind(item: dict[str, Any]) -> str:
    return str(item.get("kind") or ("knowledge" if item.get("knowledge_id") else ""))


def _subject_from_title(title: str) -> str:
    subject = re.sub(
        r"^(?:Charter|Initial Assessment|Research Plan|Insight Portfolio|"
        r"Directional Hypotheses|Strategy Statement|Opportunity Portfolio|"
        r"Idea Pool|Concept Portfolio)(?:\s+r\d+)?\s*·\s*",
        "",
        title,
        flags=re.IGNORECASE,
    )
    subject = re.sub(r"\s*（r\d+.*?）\s*$", "", subject)
    return subject.strip()


def _translate_experiment_terms(text: str) -> str:
    for source, translated in EXPERIMENT_TERMS:
        text = re.sub(re.escape(source), translated, text, flags=re.IGNORECASE)
    return text


def _display_title(item: dict[str, Any], *, compact: bool = False) -> str:
    title = str(item.get("title") or _doc_id(item))
    kind = _kind(item)
    if kind == "knowledge":
        return title
    if kind == "experiment":
        title = re.sub(r"^EXP-\d+(?:\s+r\d+)?\s*·\s*", "", title)
        title = re.sub(r"^Experiment\s*·\s*", "", title, flags=re.IGNORECASE)
        title = _translate_experiment_terms(title)
        title = re.sub(r"\bK-\d{3}\b", "外部基线", title)
        title = re.sub(r"\bRM-\d{3}\b", "常设监控", title)
        title = re.sub(r"（(?:真实使用行为|真实行为|行为信号).*?L4.*?）", "", title)
        return re.sub(r"（.*?）", "", title).strip() if compact else title.strip()
    if kind == "solution":
        return title
    label = NAV_LABELS.get(kind)
    if not label:
        return _subject_from_title(title)
    return label


def _toc_link(item: dict[str, Any]) -> str:
    doc_id = _doc_id(item)
    return "\n".join(
        [
            "          <li>",
            f'            <a href="#{escape(doc_id, quote=True)}">',
            f'              <span class="toc-item-title">{escape(_display_title(item, compact=True))}</span>',
            "            </a>",
            "          </li>",
        ]
    )


def render_toc(
    items: list[dict[str, Any]], title: str, *, include_journey: bool = False
) -> str:
    """Render a grouped decision journey without internal identifiers."""
    groups: list[str] = []
    if items and all(_kind(item) == "knowledge" for item in items):
        links = "\n".join(_toc_link(item) for item in items)
        groups.append(
            '<section class="toc-group">\n'
            '  <p class="toc-group-title">研究证据</p>\n'
            f'  <ol>\n{links}\n  </ol>\n'
            '</section>'
        )
    else:
        grouped_ids: set[str] = set()
        for group_title, kinds in NAV_GROUPS:
            group_items = [item for item in items if _kind(item) in kinds]
            if not group_items:
                continue
            grouped_ids.update(_doc_id(item) for item in group_items)
            links = "\n".join(_toc_link(item) for item in group_items)
            if kinds == {"experiment"}:
                groups.append(
                    '<details class="toc-group toc-group-collapsible">\n'
                    f'  <summary>{group_title}<span>{len(group_items)} 项</span></summary>\n'
                    f'  <ol>\n{links}\n  </ol>\n'
                    '</details>'
                )
            else:
                groups.append(
                    '<section class="toc-group">\n'
                    f'  <p class="toc-group-title">{group_title}</p>\n'
                    f'  <ol>\n{links}\n  </ol>\n'
                    '</section>'
                )
        ungrouped = [item for item in items if _doc_id(item) not in grouped_ids]
        if ungrouped:
            links = "\n".join(_toc_link(item) for item in ungrouped)
            groups.append(
                '<section class="toc-group">\n'
                '  <p class="toc-group-title">其他资料</p>\n'
                f'  <ol>\n{links}\n  </ol>\n'
                '</section>'
            )

    journey = []
    if include_journey:
        journey = [
            '<section class="toc-group toc-case-journey">',
            '  <ol><li><a href="#case-journey"><span class="toc-item-title">案例路径</span></a></li></ol>',
            '</section>',
        ]
    return "\n".join(
        [
            '<details class="toc" open>',
            "  <summary>",
            f'    <span class="toc-name">{escape(title)}</span>',
            f'    <span class="toc-count">{len(items)} 篇</span>',
            "  </summary>",
            f'  <nav aria-label="{escape(title)}目录">',
            *journey,
            *groups,
            "  </nav>",
            "</details>",
        ]
    )


def _render_case_journey(items: list[dict[str, Any]]) -> str:
    nodes: list[str] = []
    order = {
        "charter": 0,
        "initial-assessment": 1,
        "research": 2,
        "insights": 3,
        "directional-hypothesis": 4,
        "strategy-statement": 5,
        "opportunity": 6,
        "idea-pool": 7,
        "concept-portfolio": 8,
        "solution": 9,
        "experiment": 10,
    }
    ordered_items = sorted(
        items,
        key=lambda item: (order.get(_kind(item), 99), _doc_id(item)),
    )
    for item in ordered_items:
        kind = _kind(item)
        if not kind or kind == "knowledge":
            continue
        detail = ""
        status = str(item.get("document_status") or item.get("status") or "")
        if kind == "idea-pool":
            areas = item.get("opportunity_areas")
            typed_areas = [area for area in areas or [] if isinstance(area, dict)] if isinstance(areas, list) else []
            total = sum(
                len([seed for seed in area.get("seeds") or [] if isinstance(seed, dict)])
                for area in typed_areas
            )
            detail = f"{total} Ideas"
            reviews = [
                str(area["review"].get("status") or "legacy")
                if isinstance(area.get("review"), dict)
                else "legacy"
                for area in typed_areas
            ]
            status = (
                "needs-revision"
                if "needs-revision" in reviews
                else "ready"
                if reviews and all(value == "ready" for value in reviews)
                else "legacy"
            )
        elif kind == "concept-portfolio":
            concepts = [concept for concept in item.get("concepts") or [] if isinstance(concept, dict)]
            active = [concept for concept in concepts if not _concept_is_history(concept)]
            detail = f"{len(active)} active Concepts"
            review = item.get("review")
            status = (
                str(review.get("status") or "legacy")
                if isinstance(review, dict)
                else "legacy"
            )
        label = _display_title(item, compact=True)
        nodes.append(
            '<li class="journey-node">'
            f'<a href="#{escape(_doc_id(item), quote=True)}">'
            f'<span>{escape(label)}</span>'
            + (f'<strong>{escape(detail)}</strong>' if detail else "")
            + (f'<small>{escape(status)}</small>' if status else "")
            + "</a></li>"
        )
    return (
        '<section id="case-journey" class="doc-section" data-default="true">'
        '<article class="doc-article"><header class="doc-header">'
        '<p class="doc-context">项目全貌</p><h1 class="doc-title">案例路径</h1>'
        '</header><div class="doc-body"><ol class="case-journey">'
        + "".join(nodes)
        + "</ol></div></article></section>"
    )


def _metadata_pills(item: dict[str, Any]) -> str:
    status = item.get("status") or item.get("document_status")
    if not status:
        return ""

    classes = "meta-pill"
    if status in {"complete", "final"}:
        classes += " is-complete"
    elif status in {"working", "draft"}:
        classes += " is-working"

    label = STATUS_LABELS.get(str(status), str(status))
    pills = [f'<span class="{classes}">{escape(label)}</span>']
    validation = item.get("validation_status")
    if validation == "unvalidated":
        pills.append('<span class="meta-pill is-working">待验证</span>')
    elif validation == "supported":
        pills.append('<span class="meta-pill is-complete">已有证据支持</span>')
    return "".join(pills)


def _fold_html_sections(html: str, kind: str) -> str:
    for level, prefix in FOLDED_SECTIONS.get(kind, ()):
        stop = r"(?=<h2>|$)" if level == 2 else r"(?=<h[23]>|$)"
        pattern = re.compile(
            rf"<h{level}>(?P<title>[^<]+)</h{level}>(?P<body>.*?){stop}",
            re.DOTALL,
        )

        def fold(match: re.Match[str], prefix: str = prefix) -> str:
            title = match.group("title")
            if not title.startswith(prefix):
                return match.group(0)
            return (
                '<details class="detail-section">'
                f'<summary>{title}</summary>'
                f'<div class="detail-body">{match.group("body")}</div>'
                '</details>'
            )

        html = pattern.sub(fold, html)
    return html


def _promote_html_sections(html: str, kind: str) -> str:
    promoted: list[str] = []
    for prefix in PROMOTED_SECTIONS.get(kind, ()):
        pattern = re.compile(
            r"<h2>(?P<title>[^<]+)</h2>(?P<body>.*?)(?=<h2>|$)",
            re.DOTALL,
        )
        for match in pattern.finditer(html):
            if not match.group("title").startswith(prefix):
                continue
            promoted.append(
                '<section class="decision-lead">'
                f'<h2>{match.group("title")}</h2>{match.group("body")}'
                '</section>'
            )
            html = f"{html[:match.start()]}{html[match.end():]}"
            break
    return f'{"".join(promoted)}{html}'


def _shape_experiment_html(html: str) -> str:
    """Turn experiment checklists into a decision-facing validation brief."""
    section = re.compile(
        r"<h2>设计清单.*?</h2>\s*<ul>(?P<items>.*?)</ul>",
        re.DOTALL,
    )
    item = re.compile(
        r"<li><strong>(?P<label>[^<]+)</strong>[：:]\s*(?P<value>.*?)</li>",
        re.DOTALL,
    )
    technical_labels = {"目标假设", "方案修订", "证据采集路径"}
    label_map = {
        "目标证据级别": "证据标准",
        "Proceed 阈值": "达到什么就继续",
        "Kill 阈值": "什么情况就停止",
        "非结论性处理": "结果不明确时",
        "负责人 / 时间盒": "负责人和周期",
    }

    def replace(match: re.Match[str]) -> str:
        public_rows: list[str] = []
        technical_rows: list[str] = []
        for row in item.finditer(match.group("items")):
            label = row.group("label").strip()
            value = row.group("value")
            if label not in technical_labels:
                value = _translate_experiment_terms(value)
            rendered = (
                '<div class="structured-row">'
                f'<dt>{escape(label_map.get(label, label))}</dt>'
                f'<dd>{value}</dd>'
                '</div>'
            )
            (technical_rows if label in technical_labels else public_rows).append(rendered)
        if not public_rows and not technical_rows:
            return match.group(0)
        technical = ""
        if technical_rows:
            technical = (
                '<details class="technical-details">'
                '<summary>技术详情</summary>'
                f'<div class="technical-body">{"".join(technical_rows)}</div>'
                '</details>'
            )
        return (
            '<section class="experiment-brief">'
            '<h2>验证计划</h2>'
            f'<dl class="structured-data">{"".join(public_rows)}</dl>'
            f'{technical}'
            '</section>'
        )

    return section.sub(replace, html, count=1)


def _render_idea_pool_view(item: dict[str, Any]) -> str:
    areas = item.get("opportunity_areas")
    if not isinstance(areas, list) or not areas:
        return ""

    rendered_areas: list[str] = []
    review_states: list[str] = []
    for area in areas:
        if not isinstance(area, dict):
            continue
        oa_id = str(area.get("opportunity_area_id") or "未归类")
        seeds = [seed for seed in area.get("seeds") or [] if isinstance(seed, dict)]
        shortlist = area.get("shortlist") if isinstance(area.get("shortlist"), dict) else {}
        confirmed = {str(seed_id) for seed_id in shortlist.get("confirmed") or []}
        new_cuts = shortlist.get("recommended_cuts")
        legacy = not isinstance(new_cuts, list)
        cut_details: dict[str, dict[str, str]] = {}
        if isinstance(new_cuts, list):
            for entry in new_cuts:
                if not isinstance(entry, dict):
                    continue
                seed_id = str(entry.get("seed_id") or "")
                if seed_id:
                    cut_details[seed_id] = {
                        "reason": str(entry.get("reason") or ""),
                        "rationale": str(entry.get("rationale") or ""),
                    }
        else:
            for seed_id in shortlist.get("recommended") or []:
                cut_details[str(seed_id)] = {}

        review = area.get("review") if isinstance(area.get("review"), dict) else None
        review_status = str(review.get("status") or "") if review else "legacy"
        review_states.append(review_status)
        findings = review.get("findings") if review else []
        findings_html = ""
        if isinstance(findings, list) and findings:
            findings_html = (
                '<ul class="review-findings">'
                + "".join(f"<li>{escape(str(finding))}</li>" for finding in findings)
                + "</ul>"
            )

        rows: list[str] = []
        for seed in seeds:
            seed_id = str(seed.get("id") or "")
            recommendation = "cut" if seed_id in cut_details else "keep"
            confirmation = "confirmed" if seed_id in confirmed else "unconfirmed"
            detail = cut_details.get(seed_id, {})
            if recommendation == "cut":
                if legacy:
                    rationale = "<span>未提供结构化淘汰理由</span>"
                else:
                    reason = escape(detail.get("reason") or "未分类")
                    rationale_text = escape(detail.get("rationale") or "未提供结构化淘汰理由")
                    rationale = f"<span>{reason}</span><span>{rationale_text}</span>"
            else:
                rationale = '<span class="muted-value">—</span>'
            refs = seed.get("source_insight_refs")
            refs_text = "、".join(str(ref) for ref in refs) if isinstance(refs, list) else ""
            rows.append(
                f'<article class="idea-row" data-oa="{escape(oa_id, quote=True)}" '
                f'data-recommendation="{recommendation}" data-confirmation="{confirmation}">'
                '<header class="idea-row-header">'
                f'<code>{escape(seed_id)}</code><strong>{escape(str(seed.get("idea") or ""))}</strong>'
                "</header>"
                '<dl class="idea-row-fields">'
                f'<div><dt>来源 Insight</dt><dd>{escape(refs_text or "未设置")}</dd></div>'
                f'<div><dt>Cluster</dt><dd>{escape(str(seed.get("cluster_id") or "—"))}</dd></div>'
                f'<div><dt>Strategy fit</dt><dd>{escape(str(seed.get("strategy_filter") or "未设置"))}</dd></div>'
                f'<div><dt>AI 建议</dt><dd>{"建议淘汰" if recommendation == "cut" else "建议保留"}</dd></div>'
                f'<div><dt>依据</dt><dd>{rationale}</dd></div>'
                f'<div><dt>人工状态</dt><dd>{"已确认" if confirmation == "confirmed" else "待确认"}</dd></div>'
                "</dl></article>"
            )

        review_label = {
            "ready": "Review ready",
            "needs-revision": "Review needs-revision",
            "legacy": "未按新契约审查",
        }.get(review_status, review_status or "未设置")
        legacy_label = '<span class="legacy-label">旧版淘汰建议</span>' if legacy else ""
        rendered_areas.append(
            f'<section class="idea-oa" data-oa="{escape(oa_id, quote=True)}">'
            '<header class="idea-oa-header">'
            f'<h3>{escape(oa_id)}</h3>'
            f'<p>{len(seeds)} 个 Idea · 建议保留 {len(seeds) - len(cut_details)} · 已确认 {len(confirmed)}</p>'
            f'<p>{escape(review_label)} {legacy_label}</p>{findings_html}'
            "</header>"
            f'<div class="idea-rows">{"".join(rows)}</div></section>'
        )

    if not rendered_areas:
        return ""
    if review_states and all(state == "ready" for state in review_states):
        handoff = (
            '<p class="decision-handoff">'
            "请在对话中返回每个机会方向要确认的 5–8 个 CS- ID。"
            "</p>"
        )
    elif "needs-revision" in review_states:
        handoff = '<p class="decision-blocked">待修订，暂不进入人工确认。</p>'
    else:
        handoff = '<p class="decision-blocked">旧版记录仅供查看，未按新契约审查。</p>'
    return (
        '<section class="idea-pool-view">'
        '<header class="decision-view-header"><h2>Idea Pool 决策依据</h2>'
        '<div class="decision-filters" aria-label="Idea 筛选">'
        '<button type="button" data-idea-filter="all" aria-pressed="true">全部</button>'
        '<button type="button" data-idea-filter="keep" aria-pressed="false">建议保留</button>'
        '<button type="button" data-idea-filter="cut" aria-pressed="false">建议淘汰</button>'
        "</div></header>"
        + "".join(rendered_areas)
        + handoff
        + "</section>"
    )


_CONCEPT_HARD_LABELS = {
    "lineage": "血缘",
    "tension": "张力",
    "distinct_mechanism": "独特机制",
    "complete_blocks": "完整模块",
    "strategy_fit": "战略契合",
    "pretest_altitude": "可测高度",
    "concept_assumptions": "概念假设",
}

_CONCEPT_SOFT_LABELS = {
    "comprehension": "可理解",
    "credibility": "可信度",
    "appeal": "吸引力",
    "differentiation": "差异化",
    "naming": "命名",
    "visualization": "可视化",
    "design_principles": "设计原则",
    "money_magic": "双面",
    "altitude": "高度",
    "healthy_anxiety": "健康焦虑",
}


def _render_concept_cards(item: dict[str, Any]) -> str:
    """Render the Concept Portfolio's canonical comparison and cards."""
    concepts = item.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        return ""
    selected = set((item.get("exit") or {}).get("selected_concept_ids") or [])
    typed = [concept for concept in concepts if isinstance(concept, dict)]
    active = [concept for concept in typed if not _concept_is_history(concept)]
    history = [concept for concept in typed if _concept_is_history(concept)]
    if not typed:
        return ""

    review = item.get("review") if isinstance(item.get("review"), dict) else None
    review_status = str(review.get("status") or "") if review else "legacy"
    reviewed = review.get("reviewed_concept_ids") if review else []
    reviewed_count = len(reviewed) if isinstance(reviewed, list) else 0
    findings = review.get("portfolio_findings") if review else []
    findings = findings if isinstance(findings, list) else []
    finding_map: dict[str, list[dict[str, Any]]] = {}
    portfolio_findings: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        concept_ids = finding.get("concept_ids")
        if isinstance(concept_ids, list):
            for concept_id in concept_ids:
                finding_map.setdefault(str(concept_id), []).append(finding)
        portfolio_findings.append(_render_concept_finding(finding))

    review_label = {
        "ready": "Independent Review ready",
        "needs-revision": "Independent Review needs-revision",
        "legacy": "未按新契约独立 Review",
    }.get(review_status, review_status or "未设置")
    iterations = review.get("iterations") if review else None
    iteration_text = f" · {escape(str(iterations))} 轮" if iterations is not None else ""
    review_summary = (
        '<section class="concept-review-summary">'
        f'<h2>{escape(review_label)}{iteration_text}</h2>'
        f'<p>Reviewer 覆盖 {reviewed_count}/{len(active)} 个 active Concept</p>'
        + (
            '<ul class="review-findings">'
            + "".join(f"<li>{finding}</li>" for finding in portfolio_findings)
            + "</ul>"
            if portfolio_findings
            else ""
        )
        + "</section>"
    )

    oa_values = sorted({str(concept.get("opportunity_area_id") or "未归类") for concept in typed})
    action_values = sorted({_concept_action(concept) for concept in typed if _concept_action(concept)})
    filters = (
        '<div class="concept-filters" aria-label="Concept 筛选">'
        '<label>机会方向<select data-concept-filter="oa"><option value="all">全部</option>'
        + "".join(
            f'<option value="{escape(oa, quote=True)}">{escape(oa)}</option>' for oa in oa_values
        )
        + "</select></label>"
        '<label>Review 建议<select data-concept-filter="action"><option value="all">全部</option>'
        + "".join(
            f'<option value="{escape(action, quote=True)}">{escape(action)}</option>'
            for action in action_values
        )
        + "</select></label>"
        '<label>决策状态<select data-concept-filter="decision">'
        '<option value="all">全部 active</option><option value="selected">已选</option>'
        '<option value="killed">已砍</option><option value="merged">已合并</option>'
        "</select></label></div>"
    )

    comparison_groups: list[str] = []
    active_groups: list[str] = []
    for oa in sorted({str(concept.get("opportunity_area_id") or "未归类") for concept in active}):
        group = [
            concept
            for concept in active
            if str(concept.get("opportunity_area_id") or "未归类") == oa
        ]
        rows = "".join(_render_concept_comparison_row(concept, selected, finding_map) for concept in group)
        comparison_groups.append(
            f'<section class="concept-comparison-group" data-oa="{escape(oa, quote=True)}">'
            f'<h3>{escape(oa)}</h3><table><thead><tr><th>Concept</th><th>一句话</th>'
            '<th>独特机制</th><th>Consumer Magic</th><th>Commercial Money</th>'
            f'<th>Reviewer</th></tr></thead><tbody>{rows}</tbody></table></section>'
        )
        cards = "".join(
            _render_concept_card(
                concept,
                selected,
                status="active",
                findings=finding_map.get(str(concept.get("id") or ""), []),
            )
            for concept in group
        )
        active_groups.append(
            f'<section class="concept-card-group" data-oa="{escape(oa, quote=True)}">'
            f'<h3>{escape(oa)}</h3><div class="concept-cards">{cards}</div></section>'
        )

    history_html = ""
    if history:
        history_cards = "".join(
            _render_concept_card(
                concept,
                selected,
                status="history",
                findings=finding_map.get(str(concept.get("id") or ""), []),
            )
            for concept in history
        )
        history_html = (
            '<details class="concept-history"><summary>'
            f'历史 Concept（{len(history)}）</summary><div class="concept-cards">'
            f'{history_cards}</div></details>'
        )

    if review_status == "ready":
        handoff = (
            '<p class="decision-handoff">'
            "请在对话中返回跨全部机会方向最终选择的 2–4 个 CI- ID。"
            "</p>"
        )
    elif review_status == "needs-revision":
        handoff = '<p class="decision-blocked">待修订，暂不进入最终 Concept 选择。</p>'
    else:
        handoff = '<p class="decision-blocked">旧版记录仅供查看，未按新契约独立 Review。</p>'

    return (
        '<section class="concept-portfolio-view">'
        + review_summary
        + filters
        + '<h2>Concept 比较</h2><div class="concept-comparison">'
        + "".join(comparison_groups)
        + "</div>"
        + '<h2 class="concept-cards-heading">完整概念卡</h2>'
        + f'<p class="concept-cards-count">{len(active)} 个 active Concept</p>'
        + "".join(active_groups)
        + history_html
        + handoff
        + "</section>"
    )


def _concept_is_history(concept: dict[str, Any]) -> bool:
    return concept.get("decision") in {"killed", "merged"} or bool(concept.get("merge_into"))


def _concept_action(concept: dict[str, Any]) -> str:
    evaluation = concept.get("evaluation")
    if isinstance(evaluation, dict) and evaluation.get("recommended_action"):
        return str(evaluation["recommended_action"])
    return str(concept.get("recommended_action") or "")


def _concept_decision(concept: dict[str, Any], selected: set[str]) -> str:
    decision = str(concept.get("decision") or "")
    concept_id = str(concept.get("id") or "")
    if decision in {"killed", "merged"}:
        return decision
    if decision == "selected" or concept_id in selected:
        return "selected"
    return "active"


def _render_concept_finding(finding: dict[str, Any]) -> str:
    parts = [str(finding.get(key) or "") for key in ("issue", "recommendation")]
    return " → ".join(escape(part) for part in parts if part)


def _dual_statement(concept: dict[str, Any], side: str, field: str) -> str:
    dual = concept.get("dual_sided")
    side_value = dual.get(side) if isinstance(dual, dict) else None
    entry = side_value.get(field) if isinstance(side_value, dict) else None
    return str(entry.get("statement") or "") if isinstance(entry, dict) else ""


def _render_concept_comparison_row(
    concept: dict[str, Any],
    selected: set[str],
    finding_map: dict[str, list[dict[str, Any]]],
) -> str:
    concept_id = str(concept.get("id") or "")
    oa = str(concept.get("opportunity_area_id") or "未归类")
    action = _concept_action(concept)
    decision = _concept_decision(concept, selected)
    findings = "；".join(_render_concept_finding(finding) for finding in finding_map.get(concept_id, []))
    return (
        f'<tr data-concept-status="active" data-oa="{escape(oa, quote=True)}" '
        f'data-action="{escape(action, quote=True)}" data-decision="{escape(decision, quote=True)}">'
        f'<td><code>{escape(concept_id)}</code> {escape(str(concept.get("name") or ""))}</td>'
        f'<td>{escape(str(concept.get("pithy_description") or ""))}</td>'
        f'<td>{escape(str(concept.get("how_it_works") or ""))}</td>'
        f'<td>{escape(_dual_statement(concept, "magic", "consumer_value_proposition"))}</td>'
        f'<td>{escape(_dual_statement(concept, "money", "commercial_value_proposition"))}</td>'
        f'<td>{escape(action)}{(" · " + findings) if findings else ""}</td></tr>'
    )


def _render_concept_card(
    concept: dict[str, Any],
    selected: set[str],
    *,
    status: str = "active",
    findings: list[dict[str, Any]] | None = None,
) -> str:
    concept_id = str(concept.get("id") or "")
    name = str(concept.get("name") or concept_id)
    pithy = str(concept.get("pithy_description") or "")
    decision = concept.get("decision")
    badge = _concept_decision_badge(decision, concept_id in selected)

    header = (
        '<header class="concept-card-header">'
        f'<span class="concept-card-id">{escape(concept_id)}</span>'
        f'<h3 class="concept-card-name">{escape(name)}</h3>'
        f'<p class="concept-card-pithy">{escape(pithy)}</p>'
        f'{badge}'
        "</header>"
    )

    fields: list[str] = []
    for label, value in (
        ("消费者洞察", concept.get("consumer_insight")),
        ("商业洞察", concept.get("commercial_insight")),
        ("定义（What）", concept.get("idea_definition")),
        ("目标用户（Who）", concept.get("who_its_for")),
        ("机制（How）", concept.get("how_it_works")),
        ("替代什么", concept.get("what_it_replaces")),
        ("为什么大（Why big）", concept.get("why_big")),
    ):
        text = str(value or "").strip()
        if text:
            fields.append(_concept_field(label, text))

    body_parts: list[str] = []
    if fields:
        body_parts.append(
            '<dl class="concept-fields">' + "".join(fields) + "</dl>"
        )
    principles = concept.get("design_principles")
    if isinstance(principles, list) and principles:
        items = "".join(
            f"<li>{escape(str(principle))}</li>"
            for principle in principles
            if str(principle).strip()
        )
        if items:
            body_parts.append(
                '<div class="concept-principles"><h4>设计原则</h4>'
                f"<ul>{items}</ul></div>"
            )
    dual = _render_concept_dual_sided(concept.get("dual_sided"))
    if dual:
        body_parts.append(dual)
    visualization = _render_concept_visualization_block(concept)
    if visualization:
        body_parts.append(visualization)
    evaluation = _render_concept_evaluation(concept.get("evaluation"))
    if evaluation:
        body_parts.append(evaluation)
    action = _concept_action(concept)
    if action:
        body_parts.append(_concept_field("Reviewer 建议", action))
    assumption_refs = concept.get("assumption_refs")
    if isinstance(assumption_refs, list) and assumption_refs:
        body_parts.append(_concept_field("可证伪假设", "、".join(str(ref) for ref in assumption_refs)))
    if findings:
        body_parts.append(
            _concept_field(
                "Reviewer finding",
                "；".join(
                    re.sub(r"<[^>]+>", "", _render_concept_finding(finding))
                    for finding in findings
                ),
            )
        )

    oa = str(concept.get("opportunity_area_id") or "未归类")
    action = _concept_action(concept)
    decision_state = _concept_decision(concept, selected)

    return (
        f'<article class="concept-card" data-concept-status="{status}" '
        f'data-oa="{escape(oa, quote=True)}" data-action="{escape(action, quote=True)}" '
        f'data-decision="{escape(decision_state, quote=True)}">'
        f'{header}{"".join(body_parts)}'
        "</article>"
    )


def _concept_field(label: str, value: str) -> str:
    return (
        '<div class="concept-field">'
        f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>"
        "</div>"
    )


def _concept_decision_badge(decision: Any, selected: bool) -> str:
    if decision == "selected" or selected:
        return '<span class="concept-badge concept-selected">已选</span>'
    if decision == "killed":
        return '<span class="concept-badge concept-killed">已砍</span>'
    if decision == "merged":
        return '<span class="concept-badge concept-merged">已合并</span>'
    return ""


def _render_concept_dual_sided(dual: Any) -> str:
    if not isinstance(dual, dict):
        return ""
    magic = dual.get("magic") if isinstance(dual.get("magic"), dict) else {}
    money = dual.get("money") if isinstance(dual.get("money"), dict) else {}
    tension = dual.get("tension") if isinstance(dual.get("tension"), dict) else {}

    def statement(side: dict[str, Any], field: str) -> str:
        entry = side.get(field) if isinstance(side, dict) else None
        if not isinstance(entry, dict):
            return ""
        return str(entry.get("statement") or "").strip()

    rows: list[str] = []
    for label, text in (
        ("用户价值主张", statement(magic, "consumer_value_proposition")),
        ("目标用户", statement(magic, "consumer_target")),
        ("商业价值主张", statement(money, "commercial_value_proposition")),
        ("可积累资产", statement(money, "leverageable_assets")),
        ("核心张力", str(tension.get("statement") or "").strip()),
        ("取舍", str(dual.get("balance_choice") or "").strip()),
    ):
        if text:
            rows.append(_concept_field(label, text))
    if not rows:
        return ""
    return (
        '<div class="concept-dual"><h4>双面（Money+Magic）</h4>'
        '<dl class="concept-fields">' + "".join(rows) + "</dl></div>"
    )


def _render_concept_visualization_block(concept: dict[str, Any]) -> str:
    svg = render_concept_visualization(
        concept.get("visualization_spec"),
        caption=str(concept.get("name") or ""),
    )
    if svg:
        return f'<div class="concept-visualization"><h4>概念速写</h4>{svg}</div>'
    text = str(concept.get("visualization") or "").strip()
    if text:
        return (
            '<div class="concept-visualization concept-visualization-fallback">'
            f"<h4>概念速写</h4><p>{escape(text)}</p></div>"
        )
    return ""


def _render_concept_evaluation(evaluation: Any) -> str:
    if not isinstance(evaluation, dict):
        return ""
    parts: list[str] = []
    hard = evaluation.get("hard")
    if isinstance(hard, dict) and hard:
        chips = "".join(
            '<span class="chip '
            f'{"chip-ok" if value else "chip-no"}">'
            f'{escape(_CONCEPT_HARD_LABELS.get(key, key))}</span>'
            for key, value in hard.items()
        )
        parts.append(
            '<div class="concept-eval"><h4>硬标准</h4>'
            f'<div class="chips">{chips}</div></div>'
        )
    soft = evaluation.get("soft")
    if isinstance(soft, dict) and soft:
        chips = "".join(
            f'<span class="chip">{escape(_CONCEPT_SOFT_LABELS.get(key, key))} '
            f"{escape(str(value))}</span>"
            for key, value in soft.items()
        )
        parts.append(
            '<div class="concept-eval"><h4>软标准</h4>'
            f'<div class="chips">{chips}</div></div>'
        )
    return "".join(parts)


def render_doc(
    item: dict[str, Any], body: str, page_kind: str, *, active: bool = False
) -> str:
    """Render one latest-revision document as a semantic article."""
    doc_id = _doc_id(item)
    kind = _kind(item)
    title = _display_title(item)
    body_html = _render_markdown(body, page_kind, kind)
    if kind == "experiment":
        body_html = _shape_experiment_html(body_html)
    body_html = _fold_html_sections(body_html, kind)
    body_html = _promote_html_sections(body_html, kind)
    if kind == "idea-pool":
        body_html = _render_idea_pool_view(item) + body_html
    elif kind == "concept-portfolio":
        body_html = _render_concept_cards(item) + body_html
    meta_pills = _metadata_pills(item)
    meta_html = f"      <div class=\"doc-meta\" aria-label=\"文档元数据\">\n        {meta_pills}\n      </div>" if meta_pills else ""
    classes = "doc-section"
    hidden = "" if active else " hidden"
    default_attr = ' data-default="true"' if active else ""
    source_title = escape(str(item.get("title") or doc_id), quote=True)
    group_label = next(
        (label for label, kinds in NAV_GROUPS if kind in kinds),
        "研究证据" if kind == "knowledge" else "项目资料",
    )

    return f'''<section id="{escape(doc_id, quote=True)}" class="{classes}" data-source-title="{source_title}"{default_attr}{hidden}>
  <article class="doc-article">
    <header class="doc-header">
      <p class="doc-context">{escape(group_label)}</p>
      <h1 class="doc-title">{escape(title)}</h1>
{meta_html}
    </header>
    <div class="doc-body">
{body_html}
    </div>
  </article>
</section>'''


STYLES = """
    :root {
      --ink: #1d2927;
      --body: #46514e;
      --muted: #7b8480;
      --accent: #28665f;
      --accent-soft: #e4eee9;
      --surface: #fcfcfa;
      --sidebar: #f1f0eb;
      --rule: #dcded8;
      --code: #f2f4f1;
      --reader-width: 820px;
      --sidebar-width: 272px;
      --sans: "Avenir Next", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      --serif: "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", "Iowan Old Style", STSong, serif;
      --mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    }

    * { box-sizing: border-box; }

    html {
      scroll-behavior: smooth;
      scroll-padding-top: 2rem;
    }

    body {
      margin: 0;
      color: var(--ink);
      background: var(--surface);
      font-family: var(--sans);
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }

    .reader-shell {
      display: grid;
      grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
      min-height: 100vh;
    }

    .reader-sidebar {
      position: sticky;
      top: 0;
      align-self: start;
      height: 100vh;
      padding: 2rem 1.25rem;
      overflow: hidden;
      background: var(--sidebar);
      border-right: 1px solid var(--rule);
    }

    .toc {
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    .toc > summary {
      display: none;
    }

    .toc nav {
      min-height: 0;
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-width: thin;
    }

    .toc::before {
      content: "BEWATER / DOCS";
      display: block;
      margin: 0 .65rem 1.5rem;
      color: var(--accent);
      font-family: var(--serif);
      font-size: .82rem;
      font-weight: 700;
      letter-spacing: .09em;
    }

    .toc ol {
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .toc-group + .toc-group { margin-top: 1.25rem; }

    .toc-group-title,
    .toc-group > summary {
      margin: 0 .65rem .35rem;
      color: #7a827f;
      font-size: .7rem;
      font-weight: 700;
      letter-spacing: .08em;
    }

    .toc-group > summary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 2.75rem;
      cursor: pointer;
      list-style: none;
    }

    .toc-group > summary::-webkit-details-marker { display: none; }

    .toc-group > summary span {
      color: #969c99;
      font-weight: 500;
      letter-spacing: 0;
    }

    .toc li + li { margin-top: .2rem; }

    .toc a {
      display: flex;
      align-items: center;
      min-height: 2.75rem;
      padding: .6rem .65rem;
      color: #59625f;
      border-radius: 5px;
      text-decoration: none;
      transition: color 140ms ease, background 140ms ease;
    }

    .toc a:hover {
      color: var(--accent);
      background: rgba(255, 255, 255, .58);
    }

    .toc a.current,
    .toc a[aria-current="page"] {
      color: var(--accent);
      background: rgba(255, 255, 255, .58);
      box-shadow: inset 2px 0 0 var(--accent);
    }

    .toc-item-title {
      display: block;
      font-size: .83rem;
      font-weight: 600;
      line-height: 1.45;
    }

    .toc-item-meta {
      display: block;
      margin-top: .28rem;
      color: #8b918d;
      font-family: var(--mono);
      font-size: .68rem;
      letter-spacing: .02em;
    }

    .doc-section {
      display: none;
    }

    .doc-section.active { display: block; }
    .doc-section[data-default="true"] { display: block; }

    .reader-main {
      min-width: 0;
      padding: clamp(3rem, 7vw, 6.5rem) clamp(2rem, 7vw, 7rem) 8rem;
    }

    .docs {
      width: min(100%, var(--reader-width));
      margin: 0 auto;
    }

    .doc-section {
      scroll-margin-top: 2rem;
    }

    .doc-section + .doc-section {
      margin-top: 6rem;
      padding-top: 6rem;
      border-top: 1px solid var(--rule);
    }

    .doc-section:target .doc-title { color: var(--accent); }

    .doc-header { margin-bottom: 3.1rem; }

    .doc-context {
      margin: 0 0 .8rem;
      color: var(--accent);
      font-size: .76rem;
      font-weight: 700;
      letter-spacing: .08em;
    }

    .doc-kicker {
      margin: 0 0 .9rem;
      color: var(--accent);
      font-family: var(--mono);
      font-size: .76rem;
      font-weight: 650;
      letter-spacing: .08em;
    }

    .doc-title {
      margin: 0;
      color: var(--ink);
      font-family: var(--serif);
      font-size: clamp(2.15rem, 4vw, 3.2rem);
      font-weight: 700;
      letter-spacing: -.025em;
      line-height: 1.2;
      text-wrap: balance;
    }

    .doc-meta {
      display: flex;
      flex-wrap: wrap;
      gap: .45rem;
      margin-top: 1.4rem;
      padding-bottom: 1.55rem;
      border-bottom: 1px solid var(--rule);
    }

    .meta-pill {
      display: inline-flex;
      align-items: center;
      min-height: 1.7rem;
      padding: .24rem .62rem;
      color: #68716e;
      background: #f0f2ef;
      border: 1px solid #e1e4df;
      border-radius: 999px;
      font-family: var(--mono);
      font-size: .7rem;
      line-height: 1;
    }

    .meta-pill.is-complete {
      color: #256044;
      background: #e5f1e8;
      border-color: #cfe3d5;
    }

    .meta-pill.is-working {
      color: #765a22;
      background: #f6efdb;
      border-color: #eadfbf;
    }

    .doc-body {
      color: var(--body);
      font-size: 17px;
      line-height: 1.85;
      overflow-wrap: anywhere;
    }

    .doc-body h2,
    .doc-body h3,
    .doc-body h4,
    .doc-body h5,
    .doc-body h6 {
      color: #233b37;
      font-family: var(--serif);
      line-height: 1.4;
      text-wrap: balance;
    }

    .doc-body h2 {
      margin: 3.25rem 0 1rem;
      font-size: 1.55rem;
      letter-spacing: -.012em;
    }

    .doc-body h3 {
      margin: 2.5rem 0 .8rem;
      font-size: 1.28rem;
    }

    .doc-body h4,
    .doc-body h5,
    .doc-body h6 {
      margin: 2rem 0 .7rem;
      font-size: 1.08rem;
    }

    .doc-body p { margin: 0 0 1.15rem; }

    .decision-lead {
      margin: 0 0 3.25rem;
      padding: 1.6rem clamp(1.2rem, 3vw, 2rem);
      background: #eef3ef;
      border-top: 1px solid #d7e2dc;
      border-bottom: 1px solid #d7e2dc;
    }

    .decision-lead > h2:first-child {
      margin-top: 0;
    }

    .learning-agenda { margin: 0; }

    .learning-item {
      padding: 1.5rem 0 1.65rem;
      border-top: 1px solid var(--rule);
    }

    .learning-item:last-child { border-bottom: 1px solid var(--rule); }

    .learning-header {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 1rem;
      align-items: start;
    }

    .learning-header h3 {
      margin: 0;
      font-family: var(--sans);
      font-size: 1.08rem;
      line-height: 1.55;
    }

    .learning-status {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: .35rem;
    }

    .status-badge,
    .priority-label {
      white-space: nowrap;
      font-size: .72rem;
      line-height: 1.4;
    }

    .status-badge {
      padding: .2rem .5rem;
      color: #285d46;
      background: #e4efe8;
      border-radius: 999px;
      font-weight: 700;
    }

    .status-partial,
    .status-gap-accepted,
    .status-unknown { color: #73571e; background: #f4ecd6; }

    .priority-label { color: var(--muted); }

    .decision-fields {
      margin: 1.1rem 0 0;
    }

    .decision-fields > div {
      display: grid;
      grid-template-columns: 7rem minmax(0, 1fr);
      gap: .8rem;
      padding: .42rem 0;
    }

    .decision-fields dt,
    .structured-row dt {
      color: #334a45;
      font-weight: 700;
    }

    .decision-fields dd,
    .structured-row dd {
      min-width: 0;
      margin: 0;
    }

    .detail-section,
    .technical-details {
      margin: 1.5rem 0;
      border-top: 1px solid var(--rule);
      border-bottom: 1px solid var(--rule);
    }

    .detail-section > summary,
    .technical-details > summary {
      display: flex;
      align-items: center;
      min-height: 2.85rem;
      color: #35534d;
      cursor: pointer;
      font-weight: 700;
      list-style: none;
    }

    .detail-section > summary::after,
    .technical-details > summary::after {
      content: "+";
      margin-left: auto;
      color: var(--muted);
      font-size: 1.2rem;
      font-weight: 400;
    }

    .detail-section[open] > summary::after,
    .technical-details[open] > summary::after { content: "−"; }

    .detail-body,
    .technical-body { padding: .25rem 0 .8rem; }

    .technical-details {
      color: #66706d;
      font-size: .82rem;
    }

    .structured-block { margin: 1.35rem 0; }
    .structured-data { margin: 0; }

    .structured-row {
      display: grid;
      grid-template-columns: minmax(7.5rem, 28%) minmax(0, 1fr);
      gap: 1rem;
      padding: .65rem 0;
      border-top: 1px solid #e5e7e2;
    }

    .structured-group {
      padding: .8rem 0;
      border-top: 1px solid #e5e7e2;
    }

    .structured-group > h4 { margin: 0 0 .65rem; }

    .structured-list {
      margin: .35rem 0 1rem;
      padding-left: 1.2rem;
    }

    .structured-list > li + li {
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid #e5e7e2;
    }

    .experiment-brief > h2 { margin-top: 0; }

    .internal-marker {
      color: #52625e;
      border-bottom: 1px dotted #9ba7a3;
      cursor: help;
      white-space: nowrap;
    }

    .doc-body a {
      color: var(--accent);
      text-decoration-color: #9bb8b2;
      text-decoration-thickness: 1px;
      text-underline-offset: .18em;
    }

    /* 角标引用样式 */
    .doc-body .ref {
      display: inline-flex;
      align-items: baseline;
      vertical-align: super;
      color: var(--muted);
      font-family: var(--mono);
      font-size: 0.7em;
      font-weight: 600;
      text-decoration: none;
      white-space: nowrap;
      margin: 0 2px;
      cursor: help;
      transition: color 140ms ease;
    }

    .doc-body .ref:hover {
      color: var(--accent);
    }

    .doc-body .ref:focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 2px;
      border-radius: 2px;
    }

    .doc-body ul,
    .doc-body ol {
      margin: 0 0 1.35rem;
      padding-left: 1.55rem;
    }

    .doc-body li { padding-left: .22rem; }
    .doc-body li + li { margin-top: .38rem; }

    .doc-body blockquote {
      margin: 1.75rem 0;
      padding: .9rem 1.15rem .9rem 1.3rem;
      color: #36534e;
      background: #f1f5f1;
      border-left: 3px solid var(--accent);
    }

    .doc-body blockquote > :last-child { margin-bottom: 0; }

    .doc-body code {
      padding: .12em .34em;
      color: #7a3d2c;
      background: var(--code);
      border-radius: 3px;
      font-family: var(--mono);
      font-size: .86em;
    }

    .doc-body pre {
      max-width: 100%;
      margin: 1.6rem 0;
      padding: 1rem 1.15rem;
      overflow-x: auto;
      background: var(--code);
      border: 1px solid var(--rule);
      border-radius: 5px;
      line-height: 1.6;
    }

    .doc-body pre code {
      padding: 0;
      color: #34423f;
      background: transparent;
      white-space: pre;
    }

    .doc-body table {
      display: block;
      width: 100%;
      max-width: 100%;
      margin: 1.7rem 0;
      overflow-x: auto;
      border-collapse: collapse;
      font-size: .88em;
      line-height: 1.55;
      white-space: normal;
    }

    .doc-body th,
    .doc-body td {
      min-width: 8rem;
      padding: .68rem .75rem;
      text-align: left;
      vertical-align: top;
      border: 1px solid var(--rule);
    }

    .doc-body th {
      color: #294d47;
      background: #edf2ee;
      font-weight: 700;
    }

    .doc-body tr:nth-child(even) td { background: #f8f8f5; }

    .doc-body hr {
      margin: 2.8rem 0;
      border: 0;
      border-top: 1px solid var(--rule);
    }

    .doc-body img {
      max-width: 100%;
      height: auto;
    }

    a:focus-visible,
    summary:focus-visible {
      outline: 3px solid #77a79e;
      outline-offset: 3px;
    }

    @media (min-width: 961px) {
      .toc:not([open]) > nav { display: block; }
    }

    @media (max-width: 960px) {
      html { scroll-padding-top: 1rem; }

      .reader-shell { grid-template-columns: minmax(0, 1fr); }

      .reader-sidebar {
        position: relative;
        height: auto;
        padding: 1rem clamp(1rem, 5vw, 2.2rem);
        overflow: visible;
        border-right: 0;
        border-bottom: 1px solid var(--rule);
      }

      .toc { height: auto; }
      .toc::before { display: none; }

      .toc > summary {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        min-height: 2.5rem;
        color: var(--ink);
        cursor: pointer;
        list-style: none;
      }

      .toc > summary::-webkit-details-marker { display: none; }

      .toc-name {
        font-family: var(--serif);
        font-weight: 700;
      }

      .toc-count {
        color: var(--muted);
        font-size: .78rem;
      }

      .toc nav {
        max-height: 42vh;
        margin-top: .65rem;
        border-top: 1px solid var(--rule);
      }

      .toc ol { padding-top: .55rem; }

      .reader-main {
        padding: clamp(2.8rem, 8vw, 4.5rem) clamp(1.35rem, 6vw, 3.5rem) 6rem;
      }
    }

    @media (max-width: 640px) {
      .reader-main { padding-inline: 1.15rem; }
      .doc-header { margin-bottom: 2.4rem; }
      .doc-title { font-size: 2rem; }

      .doc-body {
        font-size: 16px;
        line-height: 1.8;
      }

      .doc-body h2 {
        margin-top: 2.6rem;
        font-size: 1.38rem;
      }

      .learning-header { grid-template-columns: minmax(0, 1fr); }
      .learning-status { align-items: flex-start; }

      .decision-fields > div,
      .structured-row {
        grid-template-columns: minmax(0, 1fr);
        gap: .18rem;
      }

      .doc-section + .doc-section {
        margin-top: 4.5rem;
        padding-top: 4.5rem;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      .toc a { transition: none; }
    }

    @media print {
      @page { margin: 1.8cm; }

      body {
        color: #000;
        background: #fff;
      }

      .reader-shell { display: block; }
      .reader-sidebar { display: none; }

      .reader-main {
        padding: 0;
      }

      .docs { width: 100%; }

      .doc-section {
        display: block !important;
      }

      .detail-section > :not(summary),
      .technical-details > :not(summary) {
        display: block !important;
      }

      .doc-section + .doc-section {
        margin-top: 0;
        padding-top: 0;
        border-top: 0;
        break-before: page;
      }

      .doc-body a {
        color: inherit;
        text-decoration: none;
      }

      .doc-body pre,
      .doc-body table,
      .doc-body blockquote {
        break-inside: avoid;
      }
    }

    .concept-cards-heading {
      margin: 2rem 0 .25rem;
      color: var(--accent);
      font-family: var(--serif);
    }
    .concept-cards-count {
      margin: 0 0 1rem;
      color: var(--muted);
      font-size: .85rem;
    }
    .concept-cards {
      display: grid;
      gap: 1.25rem;
    }
    .concept-card {
      border: 1px solid var(--rule);
      border-radius: 10px;
      background: #fff;
      overflow: hidden;
    }
    .concept-card-header {
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--rule);
      background: var(--accent-soft);
    }
    .concept-card-id {
      font-family: var(--mono);
      font-size: .78rem;
      color: var(--muted);
    }
    .concept-card-name {
      margin: .25rem 0 .35rem;
      font-family: var(--serif);
      font-size: 1.25rem;
      color: var(--ink);
    }
    .concept-card-pithy {
      margin: 0;
      color: var(--accent);
      font-weight: 600;
    }
    .concept-badge {
      display: inline-block;
      margin-top: .5rem;
      padding: .15rem .6rem;
      border-radius: 999px;
      font-size: .78rem;
      font-weight: 700;
    }
    .concept-selected { background: var(--accent); color: #fff; }
    .concept-killed { background: #f3d9d9; color: #8a2f2f; }
    .concept-merged { background: #e7e0c9; color: #6b5b1f; }
    .concept-fields {
      display: grid;
      gap: .55rem;
      margin: 0;
      padding: 1rem 1.25rem;
    }
    .concept-field {
      display: grid;
      grid-template-columns: 9rem minmax(0, 1fr);
      gap: .75rem;
    }
    .concept-field dt {
      color: var(--muted);
      font-weight: 600;
      font-size: .85rem;
      padding-top: .1rem;
    }
    .concept-field dd {
      margin: 0;
      color: var(--body);
    }
    .concept-card h4 {
      margin: 0 0 .5rem;
      color: var(--accent);
      font-size: .85rem;
      letter-spacing: .03em;
    }
    .concept-principles,
    .concept-dual,
    .concept-visualization,
    .concept-eval {
      padding: 1rem 1.25rem;
      border-top: 1px solid var(--rule);
    }
    .concept-principles ul {
      margin: 0;
      padding-left: 1.1rem;
    }
    .concept-principles li,
    .concept-dual dd {
      color: var(--body);
    }
    .concept-visualization svg {
      width: 100%;
      height: auto;
      max-width: 640px;
      display: block;
    }
    .concept-visualization-fallback p {
      margin: 0;
      color: var(--body);
      background: var(--code);
      border-left: 3px solid var(--accent);
      padding: .6rem .75rem;
      border-radius: 0 6px 6px 0;
    }
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: .4rem;
    }
    .chip {
      display: inline-block;
      padding: .15rem .55rem;
      border-radius: 6px;
      background: var(--code);
      color: var(--body);
      font-size: .78rem;
    }
    .chip-ok { background: var(--accent-soft); color: var(--accent); }
    .chip-no { background: #f3d9d9; color: #8a2f2f; }
    .case-journey,
    .idea-rows { display: grid; gap: .8rem; padding: 0; list-style: none; }
    .journey-node a,
    .idea-row,
    .concept-review-summary,
    .concept-history { border: 1px solid var(--rule); border-radius: 10px; background: var(--surface); }
    .journey-node a { display: grid; grid-template-columns: 1fr auto; gap: .25rem 1rem; padding: 1rem; color: inherit; text-decoration: none; }
    .journey-node strong { color: var(--accent); }
    .journey-node small { grid-column: 1 / -1; color: var(--muted); }
    .decision-view-header,
    .idea-oa-header,
    .concept-review-summary { margin: 1rem 0; padding: 1rem; }
    .decision-filters,
    .concept-filters { display: flex; flex-wrap: wrap; gap: .6rem; align-items: end; }
    .decision-filters button,
    .concept-filters select { border: 1px solid var(--rule); border-radius: 6px; background: var(--surface); padding: .4rem .65rem; color: var(--body); }
    .decision-filters button[aria-pressed="true"] { background: var(--accent); color: white; }
    .concept-filters label { display: grid; gap: .25rem; font-size: .8rem; color: var(--muted); }
    .idea-oa { margin: 1.5rem 0; }
    .idea-row { padding: 1rem; }
    .idea-row[data-recommendation="cut"] { opacity: .72; }
    .idea-row-header { display: grid; gap: .4rem; }
    .idea-row-fields { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: .6rem; }
    .idea-row-fields div { min-width: 0; }
    .idea-row-fields dt { color: var(--muted); font-size: .78rem; }
    .idea-row-fields dd { margin: .15rem 0 0; }
    .idea-row-fields dd span { display: block; }
    .legacy-label { display: inline-block; margin-left: .5rem; color: #6b5b1f; }
    .decision-handoff,
    .decision-blocked { border-left: 4px solid var(--accent); background: var(--accent-soft); padding: .8rem 1rem; }
    .decision-blocked { border-color: #9b6d24; background: #f4ecd9; }
    .concept-comparison { overflow-x: auto; }
    .concept-comparison table { min-width: 840px; }
    .concept-history { margin: 1.5rem 0; padding: 1rem; }
    .concept-history summary { cursor: pointer; font-weight: 700; }
    .review-findings { color: var(--body); }
    @media (max-width: 640px) {
      .concept-field { grid-template-columns: 1fr; gap: .15rem; }
    }
"""


def _default_document_id(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    if all(_kind(item) == "knowledge" for item in items):
        return _doc_id(items[0])
    priority = (
        "solution",
        "concept-portfolio",
        "opportunity",
        "strategy-statement",
        "insights",
        "research",
        "charter",
        "initial-assessment",
        "experiment",
    )
    for kind in priority:
        candidates = [item for item in items if _kind(item) == kind]
        if candidates:
            return _doc_id(candidates[-1])
    return _doc_id(items[0])


def generate_html(
    items: list[dict[str, Any]],
    bodies: dict[str, str],
    title: str,
    page_kind: str | None = None,
) -> str:
    """Generate one aggregated, self-contained HTML reader."""
    if page_kind is None:
        page_kind = "knowledge" if items and _doc_id(items[0]).startswith("K-") else "artifact"

    include_journey = page_kind == "artifact"
    toc = render_toc(items, title, include_journey=include_journey)
    default_id = "case-journey" if include_journey else _default_document_id(items)
    rendered_documents = "\n\n".join(
        render_doc(
            item,
            bodies.get(_doc_id(item), ""),
            page_kind,
            active=_doc_id(item) == default_id,
        )
        for item in items
    )
    documents = (
        f'{_render_case_journey(items)}\n\n{rendered_documents}'
        if include_journey
        else rendered_documents
    )
    safe_title = escape(title)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{safe_title}</title>
  <style>
{STYLES}  </style>
</head>
<body>
  <div class="reader-shell">
    <aside class="reader-sidebar">
{toc}
    </aside>
    <main class="reader-main">
      <div class="docs">
{documents}
      </div>
    </main>
  </div>
  <script>
    (() => {{
      const toc = document.querySelector(".toc");
      const desktop = window.matchMedia("(min-width: 961px)");
      const sections = [...document.querySelectorAll(".doc-section")];
      const tocLinks = [...document.querySelectorAll(".toc a")];
      const fallbackSection = document.querySelector(".doc-section[data-default]") || sections[0];
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

      const hashId = () => {{
        if (!location.hash) return "";
        try {{
          return decodeURIComponent(location.hash.slice(1));
        }} catch {{
          return "";
        }}
      }};

      const sectionById = (id) => {{
        const candidate = id ? document.getElementById(id) : null;
        return candidate?.classList.contains("doc-section") ? candidate : null;
      }};

      const showSection = (id, options = {{}}) => {{
        const target = sectionById(id) || fallbackSection;
        if (!target) return;

        sections.forEach((section) => {{
          const active = section === target;
          section.hidden = !active;
          section.classList.toggle("active", active);
          section.removeAttribute("data-default");
          section.setAttribute("aria-hidden", String(!active));
        }});

        tocLinks.forEach((link) => {{
          const active = link.getAttribute("href") === `#${{target.id}}`;
          link.classList.toggle("current", active);
          if (active) {{
            link.setAttribute("aria-current", "page");
            link.closest("details.toc-group")?.setAttribute("open", "");
          }} else {{
            link.removeAttribute("aria-current");
          }}
        }});

        if (options.push && location.hash !== `#${{target.id}}`) {{
          history.pushState(null, "", `#${{encodeURIComponent(target.id)}}`);
        }}
        if (options.scroll) {{
          window.scrollTo({{
            top: 0,
            behavior: reduceMotion.matches ? "auto" : "smooth",
          }});
        }}
        if (!desktop.matches && options.collapseNav) toc?.removeAttribute("open");
      }};

      const syncToc = (query) => toc.toggleAttribute("open", query.matches);
      syncToc(desktop);
      desktop.addEventListener("change", syncToc);

      tocLinks.forEach((link) => {{
        link.addEventListener("click", (event) => {{
          event.preventDefault();
          showSection(link.getAttribute("href").slice(1), {{
            push: true,
            scroll: true,
            collapseNav: true,
          }});
        }});
      }});

      const syncFromHistory = () => showSection(hashId(), {{ scroll: false }});
      window.addEventListener("hashchange", syncFromHistory);
      window.addEventListener("popstate", syncFromHistory);
      showSection(hashId(), {{ scroll: false }});

      document.querySelectorAll("[data-idea-filter]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const view = button.closest(".idea-pool-view");
          if (!view) return;
          const filter = button.dataset.ideaFilter;
          view.querySelectorAll("[data-idea-filter]").forEach((peer) =>
            peer.setAttribute("aria-pressed", String(peer === button))
          );
          view.querySelectorAll(".idea-row").forEach((row) => {{
            row.hidden = filter !== "all" && row.dataset.recommendation !== filter;
          }});
        }});
      }});

      document.querySelectorAll(".concept-portfolio-view").forEach((view) => {{
        const filters = [...view.querySelectorAll("[data-concept-filter]")];
        const applyFilters = () => {{
          const values = Object.fromEntries(
            filters.map((filter) => [filter.dataset.conceptFilter, filter.value])
          );
          view.querySelectorAll("[data-concept-status]").forEach((node) => {{
            const matchesOa = values.oa === "all" || node.dataset.oa === values.oa;
            const matchesAction = values.action === "all" || node.dataset.action === values.action;
            const requestedDecision = values.decision;
            const matchesDecision = requestedDecision === "all"
              ? node.dataset.conceptStatus === "active"
              : node.dataset.decision === requestedDecision;
            node.hidden = !(matchesOa && matchesAction && matchesDecision);
          }});
          const history = view.querySelector(".concept-history");
          if (history && ["killed", "merged"].includes(values.decision)) history.open = true;
        }};
        filters.forEach((filter) => filter.addEventListener("change", applyFilters));
      }});
    }})();
  </script>
</body>
</html>'''


def collect_docs(directory: Path) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Collect one latest revision per document ID from a directory."""
    if not directory.exists():
        return [], {}

    latest: dict[str, tuple[dict[str, Any], str]] = {}
    for md_file in sorted(directory.glob("*.md")):
        metadata, body = parse_md(md_file)
        if not metadata:
            continue
        doc_id = _doc_id(metadata)
        if not doc_id:
            continue

        metadata, body = _normalize_document(metadata, body)
        current = latest.get(doc_id)
        if current is None or _revision(metadata) > _revision(current[0]):
            latest[doc_id] = (metadata, body)

    ordered = sorted(latest.values(), key=lambda document: _doc_id(document[0]))
    items = [metadata for metadata, _ in ordered]
    bodies = {_doc_id(metadata): body for metadata, body in ordered}
    return items, bodies


def build_html(root: Path) -> dict[str, int | str]:
    """Build the Knowledge and Artifact readers under ``_bewater-output/html``."""
    html_dir = root / "_bewater-output" / "html"
    html_dir.mkdir(parents=True, exist_ok=True)

    knowledge_dir = root / "_bewater-output" / "knowledge"
    artifacts_dir = root / "_bewater-output" / "artifacts"

    knowledge_items, knowledge_bodies = collect_docs(knowledge_dir)
    if knowledge_items:
        output = generate_html(
            knowledge_items,
            knowledge_bodies,
            "Knowledge 工论文",
            "knowledge",
        )
        (html_dir / "knowledge.html").write_text(output, encoding="utf-8")

    artifact_items, artifact_bodies = collect_docs(artifacts_dir)
    if artifact_items:
        output = generate_html(
            artifact_items,
            artifact_bodies,
            "Artifacts",
            "artifact",
        )
        (html_dir / "artifacts.html").write_text(output, encoding="utf-8")

    return {
        "knowledge": len(knowledge_items),
        "artifacts": len(artifact_items),
        "output": str(html_dir),
    }
