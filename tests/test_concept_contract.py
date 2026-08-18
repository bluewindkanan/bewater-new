"""Tests for the deterministic Concept visualization projection."""

from __future__ import annotations

from bw.concept_contract import render_concept_visualization


def _spec() -> dict:
    return {
        "screens": [
            {"caption": "候选选题", "bullets": ["3 个选题", "点选一个"]},
            {"caption": "确认发布", "bullets": ["倒计时 30:00"]},
        ]
    }


def test_render_is_deterministic_for_identical_spec() -> None:
    first = render_concept_visualization(_spec(), caption="概念")
    second = render_concept_visualization(_spec(), caption="概念")
    assert first == second
    assert first


def test_render_returns_empty_for_missing_or_malformed_spec() -> None:
    assert render_concept_visualization(None) == ""
    assert render_concept_visualization({}) == ""
    assert render_concept_visualization({"screens": "nope"}) == ""
    assert render_concept_visualization({"screens": []}) == ""
    assert (
        render_concept_visualization(
            {"screens": [{"caption": "", "bullets": []}]}
        )
        == ""
    )


def test_render_projects_fallback_text_to_a_wireframe() -> None:
    output = render_concept_visualization(
        None,
        caption="天级战报",
        fallback_text="次日清晨显示曝光、点赞和私域进线",
    )

    assert 'class="concept-wireframe"' in output
    assert 'aria-label="天级战报"' in output
    assert "次日清晨显示曝光、点赞" in output


def test_render_includes_captions_bullets_and_arrow() -> None:
    output = render_concept_visualization(_spec(), caption="概念")
    assert "<svg" in output and "</svg>" in output
    assert "候选选题" in output
    assert "确认发布" in output
    assert "• 3 个选题" in output
    assert "倒计时 30:00" in output
    # two screens -> one connector path
    assert "<path" in output


def test_render_escapes_markup_in_spec_text() -> None:
    output = render_concept_visualization(
        {"screens": [{"caption": "<script>", "bullets": ["a & b"]}]}
    )
    assert "<script>" not in output
    assert "&lt;script&gt;" in output
    assert "a &amp; b" in output


def test_bullets_are_capped_and_truncated() -> None:
    spec = {
        "screens": [
            {
                "caption": "A" * 40,
                "bullets": [f"b{index}" for index in range(10)] + ["x" * 40],
            }
        ]
    }
    output = render_concept_visualization(spec)
    assert output.count("• ") == 6
    assert "…" in output
