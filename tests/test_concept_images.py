from __future__ import annotations

import base64
import json
from pathlib import Path

from bwkit import html
from bwkit.concept_images import (
    IMAGE_MODEL,
    SVG_MODEL,
    AssetRef,
    concept_cache_key,
    concept_prompt,
    ensure_concept_images,
    validate_svg,
)

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="#28665f"/></svg>'


def _concept(concept_id: str = "CI-001", *, selected: bool = True) -> dict:
    return {
        "id": concept_id,
        "name": "30分钟选择会话",
        "pithy_description": "半小时日更",
        "opportunity_area_id": "OA-001",
        "decision": "selected" if selected else None,
        "who_its_for": "时间破产的老板",
        "idea_definition": "每天固定三十分钟完成选择与发布",
        "how_it_works": "会话外预处理，会话内只选择、拍板、发布",
        "visualization": "手机收到今晚会话提醒，依次展示候选、文案和发布确认",
        "design_principles": ["会话内只做选择", "人点发布"],
        "dual_sided": {
            "magic": {"consumer_value_proposition": {"statement": "每天三十分钟"}},
            "money": {"commercial_value_proposition": {"statement": "坚持即续费"}},
            "tension": {"statement": "纪律与状态波动"},
        },
    }


def _portfolio(*concepts: dict) -> dict:
    return {
        "artifact_id": "ART-009",
        "revision": 2,
        "exit": {"selected_concept_ids": ["CI-001"]},
        "concepts": list(concepts),
    }


class _Images:
    def __init__(self, payload: bytes = b"webp") -> None:
        self.calls = []
        self.payload = payload

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        return {"data": [{"b64_json": base64.b64encode(self.payload).decode()}]}


class _Responses:
    def __init__(self, text: str = SVG) -> None:
        self.calls = []
        self.text = text

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return {"output_text": self.text}


class _Client:
    def __init__(self, *, svg: str = SVG) -> None:
        self.images = _Images()
        self.responses = _Responses(svg)


def test_prompt_and_cache_key_are_stable() -> None:
    concept = _concept()
    assert concept_prompt(concept) == concept_prompt(concept)
    assert concept_cache_key(concept) == concept_cache_key(concept)
    assert IMAGE_MODEL in concept_cache_key(concept) or len(concept_cache_key(concept)) == 64


def test_selected_concept_uses_image_api_and_writes_manifest(tmp_path: Path) -> None:
    client = _Client()
    report = ensure_concept_images(tmp_path, _portfolio(_concept()), client=client)

    assert report.generated == 1
    assert report.assets["CI-001"].status == "gpt-image-2"
    assert report.assets["CI-001"].href.endswith(".webp")
    assert client.images.calls[0]["model"] == IMAGE_MODEL
    manifest = json.loads(
        (tmp_path / "_bewater-output/html/assets/concepts/manifest.json").read_text()
    )
    assert manifest["assets"]["ART-009:CI-001"]["model"] == IMAGE_MODEL


def test_cache_hit_does_not_call_client_again(tmp_path: Path) -> None:
    first = _Client()
    ensure_concept_images(tmp_path, _portfolio(_concept()), client=first)
    second = _Client()
    report = ensure_concept_images(tmp_path, _portfolio(_concept()), client=second)

    assert report.cached == 1
    assert second.images.calls == []


def test_image_failure_falls_back_to_validated_svg(tmp_path: Path) -> None:
    class FailingImages(_Images):
        def generate(self, **kwargs):
            raise RuntimeError("image model unavailable")

    client = _Client()
    client.images = FailingImages()
    report = ensure_concept_images(tmp_path, _portfolio(_concept()), client=client)

    assert report.svg_fallback == 1
    asset = report.assets["CI-001"]
    assert asset.status == "gpt-5.6-terra-svg"
    assert asset.href.endswith(".svg")
    assert validate_svg((tmp_path / "_bewater-output/html" / asset.href).read_text())
    assert client.responses.calls[0]["model"] == SVG_MODEL


def test_unsafe_svg_is_rejected() -> None:
    assert validate_svg('<svg><script>alert(1)</script></svg>') is False
    assert validate_svg('<svg><foreignObject /></svg>') is False
    assert validate_svg('<svg><image href="https://example.com/x.png" /></svg>') is False


def test_missing_key_continues_with_warning(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    report = ensure_concept_images(tmp_path, _portfolio(_concept()), client=None)

    assert report.missing == 1
    assert report.warnings
    assert report.assets["CI-001"].status == "missing"


def test_unselected_concepts_are_not_requested(tmp_path: Path) -> None:
    client = _Client()
    portfolio = _portfolio(_concept(), _concept("CI-002", selected=False))
    report = ensure_concept_images(tmp_path, portfolio, client=client)

    assert set(report.assets) == {"CI-001"}
    assert len(client.images.calls) == 1


def test_html_uses_cached_raster_asset_for_selected_concept() -> None:
    concept = _concept()
    item = _portfolio(concept)
    asset = AssetRef(
        concept_id="CI-001",
        href="assets/concepts/ART-009-CI-001.webp",
        status="gpt-image-2",
        cache_key="cache",
        alt="30分钟选择会话 概念故事板",
    )
    output = html.generate_html(
        [dict(item, artifact_id="ART-009", kind="concept-portfolio")],
        {"ART-009": "正文"},
        "Artifacts",
        "artifact",
        concept_images={"CI-001": asset},
    )

    assert 'class="concept-image"' in output
    assert "ART-009-CI-001.webp" in output
    assert "concept-wireframe" not in output
