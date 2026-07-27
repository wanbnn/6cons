<div align="center">

# 6cons

Lucide icons as native PyReact SVG components.

[![PyPI](https://img.shields.io/pypi/v/6cons?logo=pypi&logoColor=white)](https://pypi.org/project/6cons/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyReact](https://img.shields.io/badge/PyReact-1.0.5%2B-6D4AFF)](https://github.com/wanbnn/pyreact)
[![Lucide](https://img.shields.io/badge/Lucide-1.27.0-F56565)](https://lucide.dev)
[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE)

</div>

`6cons` adapts the complete Lucide icon catalog to PyReact. Every icon is a
Python function that returns an SVG `VNode`, so it works with composition,
events, SSR, accessibility attributes, and UIKitPR utility classes without a
JavaScript runtime.

This project is an independent community port. It is not affiliated with or
endorsed by the Lucide maintainers.

## Installation with PRPM

```bash
prpm add 6cons
```

Installation with pip is also supported:

```bash
python -m pip install 6cons
```

The distribution is named `6cons`; the Python import package is `sixcons`
because Python identifiers cannot start with a digit.

## Quick start

```python
from sixcons.icons import CircleCheck, Search


def Toolbar(props):
    return Search(
        size=20,
        color="currentColor",
        stroke_width=1.75,
        class_name="text-primary",
        label="Search",
    )


status = CircleCheck(size=24, color="#16a34a")
```

Use any icon by its Lucide name when a dynamic lookup is more convenient:

```python
from sixcons import icon

settings_icon = icon("settings", size=18)
```

Named components also work through PyReact's `h()`:

```python
from pyreact import h
from sixcons.icons import Bell

node = h(Bell, {"size": 20, "label": "Notifications"})
```

## API

### `icon(name, props=None, **attributes)`

Creates an SVG VNode for a kebab-case Lucide icon name.

Common options:

| Option | Default | Description |
| --- | --- | --- |
| `size` | `24` | SVG width and height |
| `color` | `"currentColor"` | Stroke color |
| `stroke_width` | `2` | Stroke width |
| `absolute_stroke_width` | `False` | Keep the visual stroke constant when resizing |
| `class_name` / `className` | — | Additional CSS classes |
| `label` | — | Accessible label; otherwise the icon is decorative |

All other attributes, including events, `data-*`, `aria-*`, and `style`, are
forwarded to the root SVG VNode.

### Catalog helpers

```python
from sixcons import get_icon_data, icon_names, search_icons

all_names = icon_names()
matches = search_icons("arrow")
nodes = get_icon_data("search")
```

## Server-side rendering

```python
from pyreact import render_to_static_markup
from sixcons.icons import Heart

html = render_to_static_markup(Heart(size=32, color="red", label="Favorite"))
```

## Updating from Lucide

The generated catalog is pinned to Lucide `1.27.0` at commit
`4aec3f892fd6c23063bc2fead83c899b5d412b1c`.

To regenerate from a local Lucide checkout:

```bash
python scripts/sync_lucide.py \
  --source ../lucide/icons \
  --version 1.27.0 \
  --commit 4aec3f892fd6c23063bc2fead83c899b5d412b1c
```

The generator validates every SVG and produces deterministic catalog and
component modules.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m build
python -m twine check dist/*
```

## License and attribution

The icon data is derived from [Lucide](https://lucide.dev), released under the
ISC License. Icons inherited from Feather are covered by the MIT License. The
complete upstream notices are preserved in [LICENSE](LICENSE).
