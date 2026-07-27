"""Generate the 6cons catalog and named PyReact component factories."""

from __future__ import annotations

import argparse
import json
import keyword
import re
import xml.etree.ElementTree as ET
from pathlib import Path


SUPPORTED_NODES = {
    "circle",
    "ellipse",
    "line",
    "path",
    "polygon",
    "polyline",
    "rect",
}
KEBAB_PARTS = re.compile(r"[^a-zA-Z0-9]+")


def component_name(icon_name: str) -> str:
    """Convert a kebab-case Lucide name into a valid Python identifier."""
    result = "".join(
        part[:1].upper() + part[1:]
        for part in KEBAB_PARTS.split(icon_name)
        if part
    )
    if not result or result[0].isdigit() or keyword.iskeyword(result):
        result = f"Icon{result}"
    return result


def parse_icon(path: Path) -> list[list[object]]:
    """Parse and validate the drawable nodes from one Lucide SVG."""
    root = ET.parse(path).getroot()
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise ValueError(f"{path} does not contain an SVG root")

    nodes: list[list[object]] = []
    for child in root:
        tag = child.tag.rsplit("}", 1)[-1]
        if tag not in SUPPORTED_NODES:
            raise ValueError(f"Unsupported SVG node {tag!r} in {path}")
        nodes.append([tag, dict(sorted(child.attrib.items()))])
    if not nodes:
        raise ValueError(f"No drawable nodes found in {path}")
    return nodes


def generate(
    source: Path,
    package: Path,
    *,
    version: str,
    commit: str,
) -> int:
    """Generate deterministic JSON data and named component functions."""
    svg_paths = sorted(source.glob("*.svg"), key=lambda path: path.stem)
    if not svg_paths:
        raise ValueError(f"No SVG files found in {source}")

    catalog = {path.stem: parse_icon(path) for path in svg_paths}
    names: dict[str, str] = {}
    for icon_name in catalog:
        python_name = component_name(icon_name)
        if python_name in names:
            raise ValueError(
                f"Component collision: {icon_name!r} and {names[python_name]!r}"
            )
        names[python_name] = icon_name

    package.mkdir(parents=True, exist_ok=True)
    catalog_path = package / "_catalog.json"
    catalog_path.write_text(
        json.dumps(catalog, ensure_ascii=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    lines = [
        '"""Named PyReact components generated from Lucide.',
        "",
        f"Lucide version: {version}",
        f"Lucide commit: {commit}",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any, Mapping",
        "",
        "from pyreact import VNode",
        "",
        "from .core import icon as _icon",
        "",
        "",
        "def _component(",
        "    name: str,",
        "    props: Mapping[str, Any] | None,",
        "    attributes: dict[str, Any],",
        ") -> VNode:",
        "    return _icon(name, props, **attributes)",
        "",
        "",
    ]
    for python_name, icon_name in sorted(names.items()):
        lines.extend(
            [
                f"def {python_name}(",
                "    props: Mapping[str, Any] | None = None,",
                "    **attributes: Any,",
                ") -> VNode:",
                f'    """Render the ``{icon_name}`` Lucide icon."""',
                f'    return _component("{icon_name}", props, attributes)',
                "",
                "",
            ]
        )
    exported = ",\n    ".join(f'"{name}"' for name in sorted(names))
    lines.extend(["__all__ = [", f"    {exported}", "]", ""])
    (package / "icons.py").write_text("\n".join(lines), encoding="utf-8")
    return len(catalog)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument(
        "--package",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "src" / "sixcons",
    )
    args = parser.parse_args()
    count = generate(
        args.source.resolve(),
        args.package.resolve(),
        version=args.version,
        commit=args.commit,
    )
    print(f"Generated {count} PyReact icon components")


if __name__ == "__main__":
    main()
