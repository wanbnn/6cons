"""Tests for deterministic Lucide catalog generation."""

from pathlib import Path

import pytest

from scripts.sync_lucide import component_name, generate


def test_component_name_creates_valid_identifiers():
    assert component_name("circle-check") == "CircleCheck"
    assert component_name("a-arrow-down") == "AArrowDown"
    assert component_name("360") == "Icon360"


def test_generate_creates_catalog_and_components(tmp_path: Path):
    source = tmp_path / "icons"
    package = tmp_path / "sixcons"
    source.mkdir()
    (source / "sample-icon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<path d="M1 2" /><circle cx="3" cy="4" r="2" />'
        "</svg>",
        encoding="utf-8",
    )

    count = generate(source, package, version="1.0.0", commit="abc123")

    assert count == 1
    assert '"sample-icon":[["path",{"d":"M1 2"}]' in (
        package / "_catalog.json"
    ).read_text(encoding="utf-8")
    generated = (package / "icons.py").read_text(encoding="utf-8")
    assert "def SampleIcon(" in generated
    assert 'return _component("sample-icon", props, attributes)' in generated


def test_generate_rejects_unsupported_svg_nodes(tmp_path: Path):
    source = tmp_path / "icons"
    source.mkdir()
    (source / "bad.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><g /></svg>',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported SVG node"):
        generate(source, tmp_path / "package", version="1", commit="abc")
