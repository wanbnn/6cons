from pathlib import Path

from scripts.build_gallery import build, category_for, raw_svg
from sixcons import icon_names


def test_category_classification() -> None:
    assert category_for("arrow-left") == "Arrows"
    assert category_for("message-circle") == "Communication"
    assert category_for("file-text") == "Files"
    assert category_for("shopping-cart") == "Commerce"
    assert category_for("github") == "Development"


def test_raw_svg_uses_catalog_content() -> None:
    svg = raw_svg("rocket")

    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert 'width="24"' in svg
    assert 'stroke-width="2"' in svg
    assert svg.endswith("</svg>")


def test_build_creates_complete_static_gallery(tmp_path: Path) -> None:
    output_dir = tmp_path / "_site"

    built_dir = build(output_dir)
    html = (built_dir / "index.html").read_text(encoding="utf-8")

    assert html.count('data-icon-card="true"') == len(icon_names()) == 1756
    assert 'id="icon-search"' in html
    assert 'class="category-list"' in html
    assert 'data-copy-component=' in html
    assert 'data-copy-dynamic=' in html
    assert 'data-copy-svg=' in html
    assert "Built with " in html
    assert ">PyReact</a>" in html
    assert ">UIKitPR</a>" in html
    assert (output_dir / ".nojekyll").exists()
    assert (output_dir / "assets" / "uikitpr.css").is_file()
    assert (output_dir / "assets" / "gallery.css").is_file()
    assert (output_dir / "assets" / "gallery.js").is_file()
