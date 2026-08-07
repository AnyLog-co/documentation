#!/usr/bin/env python3
"""
Convert Markdown-style links [text](url) into HTML <a> tags with target="_blank",
recursively, across all .md files in a directory tree.

Usage:
    python3 convert_links.py /path/to/documentation           # apply changes
    python3 convert_links.py /path/to/documentation --dry-run # preview only
    python3 convert_links.py /path/to/documentation --ext .md,.mdx
"""

import argparse
import re
import sys
from pathlib import Path

# Matches [text](url) where text has no unescaped ']' and url has no whitespace/')'
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\((https?://[^\s)]+)\)')


def convert_line(line: str) -> str:
    return MD_LINK_RE.sub(
        r'<a href="\2" target="_blank">\1</a>',
        line
    )


def process_file(path: Path, dry_run: bool) -> int:
    """Returns number of links converted in this file."""
    original = path.read_text(encoding="utf-8")
    updated = MD_LINK_RE.sub(r'<a href="\2" target="_blank">\1</a>', original)

    count = len(MD_LINK_RE.findall(original))
    if count == 0:
        return 0

    if updated != original:
        if dry_run:
            print(f"[DRY RUN] {path} -> {count} link(s) would be converted")
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"{path} -> {count} link(s) converted")
    return count


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown links to HTML <a> tags.")
    parser.add_argument("root", help="Root directory to search recursively")
    parser.add_argument("--ext", default=".md", help="Comma-separated file extensions (default: .md)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    extensions = tuple(e.strip() if e.strip().startswith(".") else f".{e.strip()}"
                        for e in args.ext.split(","))

    total_files = 0
    total_links = 0
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix in extensions:
            n = process_file(path, args.dry_run)
            if n:
                total_files += 1
                total_links += n

    verb = "would be converted" if args.dry_run else "converted"
    print(f"\nDone: {total_links} link(s) across {total_files} file(s) {verb}.")


if __name__ == "__main__":
    main()