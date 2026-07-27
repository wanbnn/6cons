"""Command-line catalog browser for 6cons."""

from __future__ import annotations

import argparse

from . import __lucide_version__, __version__, icon_names, search_icons


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="6cons",
        description="Browse the Lucide catalog bundled for PyReact.",
    )
    parser.add_argument("--version", action="store_true")
    parser.add_argument("query", nargs="?")
    parser.add_argument("--limit", type=int, default=25)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.version:
        print(f"6cons {__version__} (Lucide {__lucide_version__})")
        return 0

    names = (
        search_icons(args.query, limit=args.limit)
        if args.query
        else icon_names()[: max(0, args.limit)]
    )
    print("\n".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
