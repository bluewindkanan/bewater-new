"""Cached Concept image generation with a safe SVG fallback."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

IMAGE_MODEL = "gpt-image-2"
SVG_MODEL = "gpt-5.6-terra"
IMAGE_SIZE = "1536x1024"
IMAGE_QUALITY = "medium"
PROMPT_VERSION = "concept-storyboard-v1"
MAX_SVG_BYTES = 512_000
_MANIFEST_NAME = "manifest.json"
_EXTERNAL_URL_RE = re.compile(r"(?:https?:|data:|//)", re.IGNORECASE)
_DISALLOWED_TAGS = {"script", "foreignobject", "animate", "animatemotion", "set"}


@dataclass(frozen=True)
class AssetRef:
    concept_id: str
    href: str
    status: str
    cache_key: str
    alt: str


@dataclass
class ImageBuildReport:
    assets: dict[str, AssetRef] = field(default_factory=dict)
    generated: int = 0
    cached: int = 0
    svg_fallback: int = 0
    stale: int = 0
    missing: int = 0
    warnings: list[str] = field(default_factory=list)


def _selected_ids(portfolio: dict[str, Any]) -> list[str]:
    exit_data = portfolio.get("exit")
    if not isinstance(exit_data, dict):
        return []
    values = exit_data.get("selected_concept_ids")
    return [str(value) for value in values if str(value).strip()] if isinstance(values, list) else []


def _text(value: Any) -> str:
    return str(value or "").strip()


def _dual_statement(concept: dict[str, Any], side: str, field: str) -> str:
    dual = concept.get("dual_sided")
    side_data = dual.get(side) if isinstance(dual, dict) else None
    entry = side_data.get(field) if isinstance(side_data, dict) else None
    return _text(entry.get("statement")) if isinstance(entry, dict) else ""


def _prompt_payload(concept: dict[str, Any]) -> dict[str, Any]:
    principles = concept.get("design_principles")
    return {
        "id": _text(concept.get("id")),
        "name": _text(concept.get("name")),
        "pithy": _text(concept.get("pithy_description")),
        "who": _text(concept.get("who_its_for")),
        "what": _text(concept.get("idea_definition")),
        "how": _text(concept.get("how_it_works")),
        "visualization": _text(concept.get("visualization")),
        "principles": [_text(item) for item in principles if _text(item)]
        if isinstance(principles, list)
        else [],
        "magic": _dual_statement(concept, "magic", "consumer_value_proposition"),
        "money": _dual_statement(concept, "money", "commercial_value_proposition"),
        "tension": _text(
            (concept.get("dual_sided") or {}).get("tension", {}).get("statement")
            if isinstance(concept.get("dual_sided"), dict)
            else ""
        ),
    }


def concept_prompt(concept: dict[str, Any]) -> str:
    payload = _prompt_payload(concept)
    return (
        "Create a polished product concept storyboard for a Chinese creator-business app. "
        "Use a restrained BeWater palette: warm ivory, charcoal ink, muted teal, and soft sage. "
        "Show two or three interface states in a clear 16:9 landscape composition, with generous "
        "spacing and realistic mobile/web UI surfaces. Use panel numbers and only a few large, "
        "legible labels; do not fill the image with tiny Chinese copy, logos, or decorative text. "
        "The image must communicate the mechanism and user flow, not a generic stock illustration. "
        "Do not include a title card or watermark. Concept facts:\n"
        + json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
    )


def concept_cache_key(concept: dict[str, Any]) -> str:
    payload = {
        "prompt_version": PROMPT_VERSION,
        "model": IMAGE_MODEL,
        "size": IMAGE_SIZE,
        "quality": IMAGE_QUALITY,
        "prompt": concept_prompt(concept),
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _asset_root(root: Path) -> Path:
    return root / "_bewater-output" / "html" / "assets" / "concepts"


def _manifest_path(root: Path) -> Path:
    return _asset_root(root) / _MANIFEST_NAME


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"version": 1, "assets": {}}
    return value if isinstance(value, dict) and isinstance(value.get("assets"), dict) else {"version": 1, "assets": {}}


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def _manifest_save(path: Path, manifest: dict[str, Any]) -> None:
    payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    _atomic_write(path, payload)


def _response_value(response: Any, key: str) -> Any:
    if isinstance(response, dict):
        return response.get(key)
    return getattr(response, key, None)


def _first_image_b64(response: Any) -> str:
    data = _response_value(response, "data")
    if not isinstance(data, list) or not data:
        return ""
    first = data[0]
    value = _response_value(first, "b64_json")
    return _text(value)


def _response_text(response: Any) -> str:
    value = _response_value(response, "output_text")
    if value:
        return _text(value)
    output = _response_value(response, "output")
    if isinstance(output, list):
        parts: list[str] = []
        for item in output:
            content = _response_value(item, "content")
            if isinstance(content, list):
                for part in content:
                    text = _response_value(part, "text")
                    if text:
                        parts.append(_text(text))
        return "".join(parts)
    return ""


def _status_code(error: Exception) -> int | None:
    value = getattr(error, "status_code", None)
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _call_once(callable_obj, *, attempts: int = 2):
    for attempt in range(attempts):
        try:
            return callable_obj()
        except Exception as error:
            code = _status_code(error)
            transient = code == 429 or code is not None and 500 <= code < 600
            if attempt + 1 >= attempts or not transient:
                raise
            time.sleep(min(2**attempt, 2))
    raise RuntimeError("unreachable")


def _openai_client() -> Any | None:
    if not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from openai import OpenAI
    except ImportError:
        return None
    return OpenAI()


def _extract_svg(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:xml|svg)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"<svg\b[\s\S]*?</svg>", cleaned, flags=re.IGNORECASE)
    return match.group(0).strip() if match else ""


def validate_svg(svg: str) -> bool:
    if not svg or len(svg.encode("utf-8")) > MAX_SVG_BYTES:
        return False
    if re.search(r"<!DOCTYPE|<script\b|<foreignObject\b|on[a-z]+\s*=|javascript:", svg, re.IGNORECASE):
        return False
    try:
        root = ElementTree.fromstring(svg)
    except ElementTree.ParseError:
        return False
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        return False
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1].lower() if isinstance(element.tag, str) else ""
        if tag in _DISALLOWED_TAGS:
            return False
        for name, value in element.attrib.items():
            lower_name = name.lower()
            if lower_name in {"xmlns", "xmlns:xlink"}:
                continue
            if lower_name.startswith("on") or _EXTERNAL_URL_RE.search(value):
                return False
            if "url(" in value.lower():
                return False
    return True


def _asset_ref(concept: dict[str, Any], href: str, status: str, cache_key: str) -> AssetRef:
    concept_id = _text(concept.get("id"))
    return AssetRef(
        concept_id=concept_id,
        href=href,
        status=status,
        cache_key=cache_key,
        alt=f"{_text(concept.get('name') or concept_id)} 概念故事板",
    )


def _existing_asset(root: Path, entry: dict[str, Any] | None) -> tuple[Path, str] | None:
    if not isinstance(entry, dict):
        return None
    relative = _text(entry.get("path"))
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        return None
    path = root / "_bewater-output" / "html" / relative
    return (path, relative) if path.is_file() else None


def ensure_concept_images(
    root: Path,
    portfolio: dict[str, Any],
    *,
    client: Any | None = None,
) -> ImageBuildReport:
    """Ensure cached images for the selected Concepts in one portfolio."""
    report = ImageBuildReport()
    typed = [item for item in portfolio.get("concepts") or [] if isinstance(item, dict)]
    by_id = {_text(item.get("id")): item for item in typed if _text(item.get("id"))}
    selected = _selected_ids(portfolio)
    if not selected:
        return report

    asset_root = _asset_root(root)
    manifest_path = _manifest_path(root)
    manifest = _load_manifest(manifest_path)
    assets = manifest.setdefault("assets", {})
    artifact_id = _text(portfolio.get("artifact_id") or "portfolio")
    revision = portfolio.get("revision")
    if client is None and os.getenv("OPENAI_API_KEY"):
        client = _openai_client()

    for concept_id in selected:
        concept = by_id.get(concept_id)
        if concept is None:
            report.missing += 1
            report.warnings.append(f"selected Concept {concept_id} is missing from the portfolio")
            continue
        cache_key = concept_cache_key(concept)
        manifest_key = f"{artifact_id}:{concept_id}"
        entry = assets.get(manifest_key)
        current = _existing_asset(root, entry)
        if isinstance(entry, dict) and entry.get("cache_key") == cache_key and current:
            _, href = current
            ref = _asset_ref(concept, href, "cached", cache_key)
            report.assets[concept_id] = ref
            report.cached += 1
            continue

        stale = current
        if client is None:
            if stale:
                _, href = stale
                report.assets[concept_id] = _asset_ref(concept, href, "stale", cache_key)
                report.stale += 1
            else:
                report.assets[concept_id] = _asset_ref(concept, "", "missing", cache_key)
                report.missing += 1
            report.warnings.append(f"{concept_id}: OPENAI_API_KEY or openai SDK unavailable")
            continue

        prompt = concept_prompt(concept)
        generated_ref: AssetRef | None = None
        try:
            response = _call_once(
                lambda prompt=prompt: client.images.generate(
                    model=IMAGE_MODEL,
                    prompt=prompt,
                    size=IMAGE_SIZE,
                    quality=IMAGE_QUALITY,
                    output_format="webp",
                )
            )
            data = base64.b64decode(_first_image_b64(response), validate=True)
            filename = f"{artifact_id}-{concept_id}-{cache_key[:12]}.webp"
            path = asset_root / filename
            _atomic_write(path, data)
            generated_ref = _asset_ref(concept, f"assets/concepts/{filename}", "gpt-image-2", cache_key)
            report.generated += 1
        except Exception as image_error:  # noqa: BLE001 - provider failures must trigger fallback
            report.warnings.append(f"{concept_id}: GPT Image 2 failed ({type(image_error).__name__})")
            try:
                response = _call_once(
                    lambda prompt=prompt: client.responses.create(
                        model=SVG_MODEL,
                        input=(
                            "Return only one safe standalone SVG, no markdown fences. "
                            "Create a clean 16:9 product storyboard with two or three panels, "
                            "minimal large labels, no external resources, scripts, or animations.\n"
                            + prompt
                        ),
                    )
                )
                svg = _extract_svg(_response_text(response))
                if not validate_svg(svg):
                    raise ValueError("fallback SVG failed safety validation")
                filename = f"{artifact_id}-{concept_id}-{cache_key[:12]}.svg"
                path = asset_root / filename
                _atomic_write(path, svg.encode("utf-8"))
                generated_ref = _asset_ref(concept, f"assets/concepts/{filename}", "gpt-5.6-terra-svg", cache_key)
                report.svg_fallback += 1
            except Exception as svg_error:  # noqa: BLE001 - fallback must not abort HTML build
                report.warnings.append(f"{concept_id}: SVG fallback failed ({type(svg_error).__name__})")

        if generated_ref:
            report.assets[concept_id] = generated_ref
            assets[manifest_key] = {
                "artifact_id": artifact_id,
                "revision": revision,
                "concept_id": concept_id,
                "cache_key": cache_key,
                "model": generated_ref.status,
                "format": Path(generated_ref.href).suffix.lstrip("."),
                "path": generated_ref.href,
                "alt": generated_ref.alt,
                "prompt_version": PROMPT_VERSION,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            _manifest_save(manifest_path, manifest)
        elif stale:
            _, href = stale
            report.assets[concept_id] = _asset_ref(concept, href, "stale", cache_key)
            report.stale += 1
        else:
            report.assets[concept_id] = _asset_ref(concept, "", "missing", cache_key)
            report.missing += 1

    return report
