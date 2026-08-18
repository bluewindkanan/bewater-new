"""Deterministic Concept visualization projection for standalone bwkit."""

from __future__ import annotations

from html import escape
from typing import Any

_PHONE_W = 150
_PHONE_H = 240
_PAD = 20
_ARROW_W = 34
_GAP = 10
_HEADER_H = 30
_BULLET_H = 22
_MAX_BULLETS = 6
_CAPTION_MAX = 12
_BULLET_MAX = 16

_STROKE = "#28665f"
_INK = "#1d2927"
_BODY = "#46514e"
_MUTED = "#7b8480"
_FRAME_FILL = "#fcfcfa"
_FONT = "'Avenir Next','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif"


def render_concept_visualization(
    spec: dict[str, Any] | None,
    *,
    caption: str = "",
    fallback_text: str = "",
) -> str:
    """Return a deterministic SVG wireframe for ``spec``, or ``""``."""
    screens = _parse_screens(spec)
    if not screens and fallback_text.strip():
        screens = [(caption.strip(), [fallback_text.strip()])]
    if not screens:
        return ""

    count = len(screens)
    width = _PAD * 2 + count * _PHONE_W + (count - 1) * (_ARROW_W + 2 * _GAP)
    height = _PAD * 2 + _PHONE_H
    parts = [
        (
            f'<svg class="concept-wireframe" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" '
            f'aria-label="{escape(caption or "concept wireframe", quote=True)}">'
        )
    ]
    for index, (screen_caption, bullets) in enumerate(screens):
        x = _PAD + index * (_PHONE_W + _ARROW_W + 2 * _GAP)
        parts.append(_phone_frame(x, _PAD, screen_caption, bullets))
        if index < count - 1:
            parts.append(_arrow(x + _PHONE_W + _GAP, _PAD + _PHONE_H // 2))
    parts.append("</svg>")
    return "".join(parts)


def _parse_screens(spec: dict[str, Any] | None) -> list[tuple[str, list[str]]]:
    if not isinstance(spec, dict):
        return []
    raw = spec.get("screens")
    if not isinstance(raw, list) or not raw:
        return []
    screens: list[tuple[str, list[str]]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        caption = _text(entry.get("caption"))
        raw_bullets = entry.get("bullets")
        bullets = (
            [text for bullet in raw_bullets if (text := _text(bullet))]
            if isinstance(raw_bullets, list)
            else []
        )
        if caption or bullets:
            screens.append((caption, bullets))
    return screens


def _phone_frame(x: int, y: int, caption: str, bullets: list[str]) -> str:
    center_x = x + _PHONE_W // 2
    parts = [
        "<g>",
        (
            f'<rect x="{x}" y="{y}" width="{_PHONE_W}" height="{_PHONE_H}" rx="12" '
            f'fill="{_FRAME_FILL}" stroke="{_STROKE}" stroke-width="2"/>'
        ),
        (
            f'<rect x="{center_x - 16}" y="{y + 7}" width="32" height="6" rx="3" '
            f'fill="{_MUTED}"/>'
        ),
        (
            f'<text x="{center_x}" y="{y + 24}" text-anchor="middle" '
            f'font-family="{_FONT}" font-size="12" font-weight="700" fill="{_INK}">'
            f'{escape(_truncate(caption, _CAPTION_MAX))}</text>'
        ),
        (
            f'<line x1="{x + 8}" y1="{y + _HEADER_H}" x2="{x + _PHONE_W - 8}" '
            f'y2="{y + _HEADER_H}" stroke="{_MUTED}" stroke-width="1"/>'
        ),
    ]
    text_y = y + _HEADER_H + 16
    for bullet in bullets[:_MAX_BULLETS]:
        parts.append(
            f'<text x="{x + 12}" y="{text_y}" text-anchor="start" '
            f'font-family="{_FONT}" font-size="10" fill="{_BODY}">'
            f'• {escape(_truncate(bullet, _BULLET_MAX))}</text>'
        )
        text_y += _BULLET_H
    parts.append("</g>")
    return "".join(parts)


def _arrow(x: int, y: int) -> str:
    tip = x + _ARROW_W
    return (
        f'<line x1="{x}" y1="{y}" x2="{tip - 7}" y2="{y}" '
        f'stroke="{_STROKE}" stroke-width="2"/>'
        f'<path d="M {tip} {y} L {tip - 8} {y - 5} L {tip - 8} {y + 5} Z" '
        f'fill="{_STROKE}"/>'
    )


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(0, limit - 1)] + "…"
