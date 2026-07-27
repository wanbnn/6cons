"""Lucide icons as native PyReact SVG components."""

from .core import (
    Icon,
    IconNotFoundError,
    get_icon_data,
    icon,
    icon_names,
    search_icons,
)

__version__ = "0.1.0"
__lucide_version__ = "1.27.0"
__lucide_commit__ = "4aec3f892fd6c23063bc2fead83c899b5d412b1c"

__all__ = [
    "Icon",
    "IconNotFoundError",
    "get_icon_data",
    "icon",
    "icon_names",
    "search_icons",
]
