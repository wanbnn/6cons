"""Tests for the PyReact icon factories."""

import pytest

from pyreact import h, render_to_static_markup
from sixcons import IconNotFoundError, get_icon_data, icon, icon_names, search_icons
from sixcons.icons import CircleCheck, Search


def test_catalog_contains_the_complete_pinned_lucide_release():
    names = icon_names()
    assert len(names) == 1756
    assert names == tuple(sorted(names))
    assert {"search", "circle-check", "house", "accessibility"} <= set(names)


def test_icon_returns_a_customizable_svg_vnode():
    node = Search(
        size=32,
        color="red",
        stroke_width=1.5,
        class_name="toolbar-icon",
        label="Search",
        id="search-icon",
    )

    assert node.type == "svg"
    assert node.props["width"] == 32
    assert node.props["height"] == 32
    assert node.props["stroke"] == "red"
    assert node.props["stroke-width"] == 1.5
    assert node.props["className"] == "lucide lucide-search toolbar-icon"
    assert node.props["aria-label"] == "Search"
    assert node.props["id"] == "search-icon"
    assert [child.type for child in node.children] == ["path", "circle"]


def test_decorative_icon_is_hidden_from_accessibility_tree():
    node = CircleCheck()
    assert node.props["aria-hidden"] == "true"
    assert "role" not in node.props


def test_named_component_works_through_h():
    html = render_to_static_markup(h(Search, {"size": 18, "label": "Find"}))
    assert html.startswith("<svg ")
    assert 'width="18"' in html
    assert 'aria-label="Find"' in html
    assert '<path d="m21 21-4.34-4.34"></path>' in html


def test_absolute_stroke_width_scales_from_the_24_pixel_grid():
    node = icon("search", size=48, stroke_width=2, absolute_stroke_width=True)
    assert node.props["stroke-width"] == 1.0


def test_dynamic_lookup_and_search():
    assert icon("circle_check").props["className"] == "lucide lucide-circle-check"
    assert search_icons("arrow", limit=3) == tuple(
        name for name in icon_names() if "arrow" in name
    )[:3]
    assert get_icon_data("search")[0][0] == "path"


def test_unknown_icon_has_a_helpful_error():
    with pytest.raises(IconNotFoundError, match="Unknown Lucide icon"):
        icon("not-a-real-lucide-icon")
