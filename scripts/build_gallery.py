"""Build the complete 6cons icon gallery with PyReact and UIKitPR."""

from __future__ import annotations

import html
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from pyreact import h  # noqa: E402
from pyreact.server import render_to_static_markup  # noqa: E402
from sixcons import (  # noqa: E402
    __lucide_commit__,
    __lucide_version__,
    __version__,
    get_icon_data,
    icon,
    icon_names,
)
from scripts.sync_lucide import component_name  # noqa: E402
from uikitpr import (  # noqa: E402
    Badge,
    Button,
    Card,
    Container,
    Heading,
    Stack,
    Text,
    UIProvider,
    stylesheet,
)


OUTPUT = ROOT / "_site"
SOURCE_ASSETS = ROOT / "site" / "assets"

CATEGORY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Arrows",
        (
            "arrow",
            "chevron",
            "corner-",
            "move-",
            "move",
            "undo",
            "redo",
            "reply",
            "forward",
            "iteration",
        ),
    ),
    (
        "Communication",
        (
            "mail",
            "message",
            "phone",
            "send",
            "inbox",
            "contact",
            "at-sign",
            "rss",
            "radio",
            "voicemail",
        ),
    ),
    (
        "Media",
        (
            "play",
            "pause",
            "skip",
            "volume",
            "audio",
            "music",
            "video",
            "camera",
            "image",
            "film",
            "mic",
            "headphone",
            "podcast",
        ),
    ),
    (
        "Files",
        (
            "file",
            "folder",
            "archive",
            "clipboard",
            "book",
            "notebook",
            "library",
            "newspaper",
            "scroll",
        ),
    ),
    (
        "Commerce",
        (
            "shopping",
            "cart",
            "store",
            "receipt",
            "wallet",
            "credit-card",
            "banknote",
            "badge-dollar",
            "package",
            "percent",
            "gift",
            "tag",
        ),
    ),
    (
        "People",
        (
            "user",
            "person",
            "contact",
            "baby",
            "accessibility",
            "hand",
            "footprints",
            "speech",
        ),
    ),
    (
        "Devices",
        (
            "monitor",
            "smartphone",
            "tablet",
            "laptop",
            "computer",
            "keyboard",
            "mouse",
            "printer",
            "watch",
            "headset",
            "router",
            "cpu",
        ),
    ),
    (
        "Maps",
        (
            "map",
            "pin",
            "compass",
            "globe",
            "navigation",
            "route",
            "milestone",
            "signpost",
            "locate",
        ),
    ),
    (
        "Weather",
        (
            "cloud",
            "sun",
            "moon",
            "snow",
            "wind",
            "rain",
            "rainbow",
            "thermometer",
            "umbrella",
            "tornado",
            "waves",
        ),
    ),
    (
        "Time",
        (
            "calendar",
            "clock",
            "timer",
            "alarm",
            "hourglass",
            "history",
            "watch",
        ),
    ),
    (
        "Development",
        (
            "code",
            "terminal",
            "git-",
            "braces",
            "brackets",
            "bug",
            "binary",
            "workflow",
            "database",
            "server",
            "webhook",
            "command",
            "regex",
            "github",
        ),
    ),
    (
        "Security",
        (
            "lock",
            "unlock",
            "key",
            "shield",
            "fingerprint",
            "scan",
            "badge-check",
            "badge-x",
            "siren",
        ),
    ),
    (
        "Status",
        (
            "check",
            "alert",
            "info",
            "help",
            "badge",
            "ban",
            "octagon-x",
            "circle-x",
            "circle-minus",
            "circle-plus",
        ),
    ),
    (
        "Interface",
        (
            "menu",
            "layout",
            "panel",
            "sidebar",
            "grid",
            "columns",
            "rows",
            "settings",
            "sliders",
            "filter",
            "search",
            "ellipsis",
            "more-",
            "maximize",
            "minimize",
            "fullscreen",
        ),
    ),
    (
        "Text",
        (
            "align-",
            "text",
            "type",
            "heading",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "indent",
            "list",
            "quote",
            "pilcrow",
            "case-",
        ),
    ),
    (
        "Shapes",
        (
            "circle",
            "square",
            "triangle",
            "diamond",
            "hexagon",
            "octagon",
            "pentagon",
            "rectangle",
            "squircle",
            "shapes",
        ),
    ),
)


def category_for(name: str) -> str:
    """Classify an icon using stable, human-readable name rules."""
    for category, needles in CATEGORY_RULES:
        if any(needle in name for needle in needles):
            return category
    return "Other"


def raw_svg(name: str) -> str:
    """Return a portable raw SVG string for copy and paste."""
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    ]
    for tag, attributes in get_icon_data(name):
        rendered = " ".join(
            f'{key}="{html.escape(str(value), quote=True)}"'
            for key, value in attributes.items()
        )
        parts.append(f"  <{tag} {rendered} />")
    parts.append("</svg>")
    return "\n".join(parts)


def copy_icon() -> object:
    return icon("copy", size=16, **{"aria-hidden": "true"})


def icon_card(name: str) -> object:
    category = category_for(name)
    python_name = component_name(name)
    component_code = (
        f"from sixcons.icons import {python_name}\n\n"
        f'{python_name}(size=24, label="{python_name}")'
    )
    dynamic_code = f'from sixcons import icon\n\nicon("{name}", size=24)'
    return Card(
        h(
            "div",
            {"className": "icon-preview"},
            icon(name, size=34, **{"aria-hidden": "true"}),
        ),
        h(
            "div",
            {"className": "icon-meta"},
            h("strong", {"title": name}, name),
            h("code", None, python_name),
        ),
        Button(
            copy_icon(),
            h("span", None, "Copy"),
            variant="outline",
            size="sm",
            class_name="card-copy",
            **{
                "data-copy-button": "true",
                "data-copy-component": component_code,
                "data-copy-dynamic": dynamic_code,
                "data-copy-svg": raw_svg(name),
                "aria-label": f"Copy {name}",
            },
        ),
        class_name="icon-card",
        **{
            "data-icon-card": "true",
            "data-icon-name": name,
            "data-category-name": category,
            "data-search": f"{name} {python_name} {category}".lower(),
        },
    )


def category_buttons(counts: Counter[str]) -> Iterable[object]:
    yield Button(
        "All",
        Badge(str(sum(counts.values())), pill=True),
        variant="primary",
        size="sm",
        class_name="category-chip is-active",
        **{"data-category": "All", "aria-pressed": "true"},
    )
    for name in sorted(counts):
        yield Button(
            name,
            Badge(str(counts[name]), pill=True),
            variant="outline",
            size="sm",
            class_name="category-chip",
            **{"data-category": name, "aria-pressed": "false"},
        )


def header() -> object:
    return h(
        "header",
        {"className": "site-header"},
        Container(
            h(
                "a",
                {"className": "brand", "href": "#top", "aria-label": "6cons home"},
                h("span", {"className": "brand-mark"}, icon("sparkles", size=21)),
                h("span", None, "6", h("strong", None, "cons")),
            ),
            h(
                "nav",
                {
                    "className": "header-links header-nav",
                    "aria-label": "Primary navigation",
                },
                h("a", {"href": "#icons"}, "Icons"),
                h("a", {"href": "https://pypi.org/project/6cons/"}, "PyPI"),
                h("a", {"href": "https://github.com/wanbnn/6cons"}, "GitHub"),
                Button(
                    icon("sun-moon", size=17),
                    h("span", {"className": "theme-label"}, "Theme"),
                    variant="ghost",
                    size="sm",
                    id="theme-toggle",
                    **{"aria-label": "Toggle color theme"},
                ),
            ),
            size="xl",
            class_name="header-inner",
        ),
    )


def hero(total: int) -> object:
    preview_names = ("search", "heart", "sparkles", "rocket", "code-xml", "palette")
    return h(
        "section",
        {"className": "hero", "id": "top"},
        Container(
            h(
                "div",
                {"className": "hero-copy"},
                Badge(
                    f"Lucide {__lucide_version__} · PyReact native",
                    tone="success",
                    pill=True,
                ),
                Heading(
                    "Every Lucide icon. Ready for Python.",
                    level=1,
                    class_name="hero-title",
                ),
                Text(
                    "Browse, search, and copy production-ready SVG components "
                    "built for PyReact and styled with UIKitPR.",
                    tone="muted",
                    class_name="hero-subtitle",
                ),
                h(
                    "div",
                    {"className": "install-command"},
                    h("span", {"aria-hidden": "true"}, "$"),
                    h("code", None, "prpm add 6cons"),
                    Button(
                        copy_icon(),
                        h("span", None, "Copy"),
                        variant="ghost",
                        size="sm",
                        id="copy-install",
                        **{"data-copy-value": "prpm add 6cons"},
                    ),
                ),
                h(
                    "div",
                    {"className": "hero-stats"},
                    h("span", None, h("strong", None, f"{total:,}"), " icons"),
                    h("span", None, h("strong", None, "0"), " JS dependencies"),
                    h("span", None, h("strong", None, "SSR"), " ready"),
                ),
            ),
            h(
                "div",
                {"className": "hero-visual", "aria-hidden": "true"},
                *[
                    h(
                        "span",
                        {"className": f"floating-icon floating-icon-{index + 1}"},
                        icon(name, size=34),
                    )
                    for index, name in enumerate(preview_names)
                ],
                h(
                    "div",
                    {"className": "hero-code-card"},
                    h("span", {"className": "code-caption"}, "app.py"),
                    h(
                        "pre",
                        None,
                        h(
                            "code",
                            None,
                            h("span", {"className": "syntax-keyword"}, "from"),
                            " sixcons.icons ",
                            h("span", {"className": "syntax-keyword"}, "import"),
                            " Rocket\n\n",
                            h("span", {"className": "syntax-call"}, "Rocket"),
                            "(size=32, color=",
                            h("span", {"className": "syntax-string"}, '"#7c5cff"'),
                            ")",
                        ),
                    ),
                ),
            ),
            size="xl",
            class_name="hero-grid",
        ),
    )


def controls(counts: Counter[str]) -> object:
    return h(
        "section",
        {"className": "catalog-controls", "aria-label": "Icon filters"},
        h(
            "div",
            {"className": "search-wrap"},
            icon("search", size=20, **{"aria-hidden": "true"}),
            h(
                "input",
                {
                    "id": "icon-search",
                    "type": "search",
                    "placeholder": "Search icons by name or component…",
                    "autocomplete": "off",
                    "spellcheck": "false",
                    "aria-label": "Search icons",
                },
            ),
            h("kbd", None, "/"),
            Button(
                icon("x", size=16),
                variant="ghost",
                size="sm",
                id="clear-search",
                class_name="clear-search",
                **{"aria-label": "Clear search", "hidden": True},
            ),
        ),
        h(
            "label",
            {"className": "copy-mode"},
            h("span", None, "Copy as"),
            h(
                "select",
                {"id": "copy-mode", "aria-label": "Copy format"},
                h("option", {"value": "component"}, "PyReact component"),
                h("option", {"value": "dynamic"}, "Dynamic lookup"),
                h("option", {"value": "svg"}, "Raw SVG"),
            ),
        ),
        h(
            "div",
            {"className": "category-scroll"},
            h(
                "div",
                {"className": "category-list", "role": "group", "aria-label": "Categories"},
                *category_buttons(counts),
            ),
        ),
    )


def catalog(names: tuple[str, ...], counts: Counter[str]) -> object:
    return h(
        "main",
        {"id": "icons", "className": "catalog-section"},
        Container(
            h(
                "div",
                {"className": "catalog-heading"},
                Stack(
                    Heading("Icon library", level=2, size="3xl"),
                    Text(
                        "Choose a copy format, then copy any icon directly into your project.",
                        tone="muted",
                    ),
                    gap=2,
                ),
                h(
                    "span",
                    {"id": "visible-count", "className": "result-count", "aria-live": "polite"},
                    f"Showing 180 of {len(names):,} icons",
                ),
            ),
            controls(counts),
            h(
                "div",
                {"id": "icon-grid", "className": "icon-grid"},
                *[icon_card(name) for name in names],
            ),
            h(
                "div",
                {"id": "empty-state", "className": "empty-state", "hidden": True},
                icon("search-x", size=42),
                Heading("No icons found", level=3),
                Text("Try a broader name or choose another category.", tone="muted"),
                Button("Clear filters", variant="outline", id="empty-clear"),
            ),
            h(
                "div",
                {"className": "load-more-wrap"},
                Button(
                    "Load more icons",
                    icon("chevron-down", size=17),
                    variant="outline",
                    id="load-more",
                ),
            ),
            size="xl",
        ),
    )


def footer(total: int) -> object:
    return h(
        "footer",
        {"className": "site-footer"},
        Container(
            h(
                "div",
                None,
                h("strong", None, "6cons"),
                Text(
                    f"{total:,} Lucide icons for PyReact · 6cons {__version__}",
                    tone="muted",
                    size="sm",
                ),
            ),
            h(
                "p",
                None,
                "Built with ",
                h("a", {"href": "https://github.com/wanbnn/pyreact"}, "PyReact"),
                " + ",
                h("a", {"href": "https://github.com/wanbnn/uikitpr"}, "UIKitPR"),
                ". Icons by ",
                h("a", {"href": "https://lucide.dev"}, "Lucide"),
                ".",
            ),
            size="xl",
            class_name="footer-inner",
        ),
    )


def page() -> str:
    names = icon_names()
    counts = Counter(category_for(name) for name in names)
    app = UIProvider(
        header(),
        hero(len(names)),
        catalog(names, counts),
        footer(len(names)),
        h(
            "div",
            {
                "id": "copy-toast",
                "className": "copy-toast",
                "role": "status",
                "aria-live": "polite",
            },
            icon("check", size=17),
            h("span", None, "Copied to clipboard"),
        ),
        theme="light",
        color_mode="light",
        with_styles=False,
        with_motion=False,
        full_height=True,
        id="app",
    )
    body = render_to_static_markup(app)
    metadata = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "6cons",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Any",
        "softwareVersion": __version__,
        "url": "https://wanbnn.github.io/6cons/",
        "codeRepository": "https://github.com/wanbnn/6cons",
    }
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "  <title>6cons — Lucide icons for PyReact</title>\n"
        '  <meta name="description" content="Search and copy all 1,756 Lucide icons as native PyReact SVG components.">\n'
        '  <meta name="theme-color" content="#6d4aff">\n'
        '  <meta property="og:title" content="6cons — Lucide icons for PyReact">\n'
        '  <meta property="og:description" content="The complete Lucide catalog, ready for Python.">\n'
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:url" content="https://wanbnn.github.io/6cons/">\n'
        '  <link rel="canonical" href="https://wanbnn.github.io/6cons/">\n'
        '  <link rel="stylesheet" href="./assets/uikitpr.css">\n'
        '  <link rel="stylesheet" href="./assets/gallery.css">\n'
        f'  <script type="application/ld+json">{json.dumps(metadata, separators=(",", ":"))}</script>\n'
        '  <script src="./assets/gallery.js" defer></script>\n'
        "</head>\n"
        f"<body>{body}</body>\n"
        "</html>\n"
    )


def build(output: Path = OUTPUT) -> Path:
    """Build the deployable GitHub Pages artifact."""
    if output.exists():
        shutil.rmtree(output)
    assets = output / "assets"
    assets.mkdir(parents=True)
    (output / "index.html").write_text(page(), encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    (assets / "uikitpr.css").write_text(
        stylesheet(minified=True),
        encoding="utf-8",
    )
    for asset in ("gallery.css", "gallery.js"):
        shutil.copy2(SOURCE_ASSETS / asset, assets / asset)
    return output


def main() -> None:
    output = build()
    print(
        f"Built {len(icon_names())} icons from Lucide {__lucide_version__} "
        f"({__lucide_commit__[:7]}) at {output}"
    )


if __name__ == "__main__":
    main()
