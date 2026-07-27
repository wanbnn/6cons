"""PyReact VNode factories for the generated Lucide catalog."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from importlib.resources import files
from typing import Any, Mapping

from pyreact import VNode, h


_NORMALIZE = re.compile(r"[\s_]+")


class IconNotFoundError(KeyError):
    """Raised when an icon name is not part of the bundled catalog."""


@lru_cache(maxsize=1)
def _catalog() -> dict[str, list[list[Any]]]:
    resource = files("sixcons").joinpath("_catalog.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def _normalize_name(name: str) -> str:
    return _NORMALIZE.sub("-", name.strip().lower())


def icon_names() -> tuple[str, ...]:
    """Return every bundled Lucide icon name in deterministic order."""
    return tuple(_catalog())


def search_icons(query: str, *, limit: int | None = None) -> tuple[str, ...]:
    """Find icon names containing the normalized query."""
    normalized = _normalize_name(query)
    matches = tuple(name for name in _catalog() if normalized in name)
    return matches if limit is None else matches[: max(0, limit)]


def get_icon_data(name: str) -> tuple[tuple[str, dict[str, str]], ...]:
    """Return an immutable copy of an icon's SVG node definitions."""
    normalized = _normalize_name(name)
    try:
        nodes = _catalog()[normalized]
    except KeyError as exc:
        raise IconNotFoundError(
            f"Unknown Lucide icon {name!r}. Use search_icons() or icon_names()."
        ) from exc
    return tuple((tag, dict(attributes)) for tag, attributes in nodes)


def _stroke_width(
    value: int | float | str,
    size: int | float | str,
    absolute: bool,
) -> int | float | str:
    if not absolute:
        return value
    try:
        return float(value) * 24 / float(size)
    except (TypeError, ValueError, ZeroDivisionError):
        return value


def icon(
    name: str,
    props: Mapping[str, Any] | None = None,
    **attributes: Any,
) -> VNode:
    """Create a PyReact SVG VNode for a Lucide icon."""
    options = dict(props or {})
    options.update(attributes)

    size = options.pop("size", 24)
    color = options.pop("color", "currentColor")
    stroke_width = options.pop(
        "stroke_width",
        options.pop("strokeWidth", 2),
    )
    absolute = bool(
        options.pop(
            "absolute_stroke_width",
            options.pop("absoluteStrokeWidth", False),
        )
    )
    label = options.pop("label", None)

    normalized = _normalize_name(name)
    nodes = get_icon_data(normalized)

    supplied_class = options.pop("class_name", options.pop("className", ""))
    classes = f"lucide lucide-{normalized}"
    if supplied_class:
        classes = f"{classes} {supplied_class}"

    svg_props: dict[str, Any] = {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": size,
        "height": size,
        "viewBox": "0 0 24 24",
        "fill": "none",
        "stroke": color,
        "stroke-width": _stroke_width(stroke_width, size, absolute),
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "className": classes,
        "focusable": "false",
    }
    if label:
        svg_props.update({"role": "img", "aria-label": label})
    else:
        svg_props["aria-hidden"] = "true"
    svg_props.update(options)

    children = [h(tag, node_attributes) for tag, node_attributes in nodes]
    return h("svg", svg_props, *children)


Icon = icon
