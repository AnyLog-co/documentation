#!/usr/bin/env python3
"""
Convert Markdown image syntax to raw HTML <img> tags in Jekyll (kramdown) docs.

kramdown/markdown renders
    ![alt text](path/to/image.png "optional title")
fine on its own, but some doc pipelines need the equivalent explicit HTML so
attributes (classes, sizing, lazy-loading, etc.) can be added later, or so
markdown and HTML image usage in a repo is consistent. This script rewrites
every Markdown image reference in a file into:
    <img src="path/to/image.png" alt="alt text">
preserving a "title" attribute when the source included one.

Fenced code blocks are left untouched, since image syntax written as a
documentation example inside a code fence shouldn't be rewritten.

Usage:
    python3 convert_images.py /path/to/documentation             # apply changes
    python3 convert_images.py /path/to/documentation --dry-run   # preview only
    python3 convert_images.py /path/to/documentation --ext .md,.mdx
"""

import argparse
import re
import sys
from pathlib import Path

# ![alt](src)  or  ![alt](src "title")  or  ![alt](src 'title')
IMAGE_RE = re.compile(
    r'!\[([^\]]*)\]\('
    r'(\S+?)'
    r'(?:\s+(?:"([^"]*)"|\'([^\']*)\'))?'
    r'\)'
)

# Fenced code blocks shouldn't have their contents touched.
FENCE_RE = re.compile(r'^\s*```')


def escape_attr(value: str) -> str:
    """Escape a value for safe placement inside a double-quoted HTML attribute."""
    return value.replace("&", "&amp;").replace('"', "&quot;")


def convert_line(line: str, converted: list) -> str:
    def repl(m):
        alt, src, title_dq, title_sq = m.group(1), m.group(2), m.group(3), m.group(4)
        title = title_dq if title_dq is not None else title_sq
        attrs = f'src="{escape_attr(src)}" alt="{escape_attr(alt)}"'
        if title:
            attrs += f' title="{escape_attr(title)}"'
        converted.append((m.group(0), f"<img {attrs}>"))
        return f"<img {attrs}>"

    return IMAGE_RE.sub(repl, line)


def process_file(path: Path, dry_run: bool):
    raw = path.read_bytes()
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")
    lines = text.splitlines()

    converted = []
    in_fence = False
    new_lines = []
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            new_lines.append(line)
            continue
        if in_fence:
            new_lines.append(line)
            continue
        new_lines.append(convert_line(line, converted))

    trailing = "\n" if text.endswith("\n") else ""
    updated_text = "\n".join(new_lines) + trailing

    changed = updated_text != text
    if changed:
        if dry_run:
            print(f"[DRY RUN] {path}")
        else:
            out_bytes = updated_text.replace("\n", newline.decode("ascii")).encode("utf-8")
            path.write_bytes(out_bytes)
            print(f"{path}")
        for old, new in converted:
            print(f"  - {old} -> {new}")

    return len(converted)


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown image syntax to HTML <img> tags in Jekyll docs.")
    parser.add_argument("root", help="Root directory (or single file) to process")
    parser.add_argument("--ext", default=".md", help="Comma-separated file extensions (default: .md)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    extensions = tuple(e.strip() if e.strip().startswith(".") else f".{e.strip()}"
                        for e in args.ext.split(","))

    paths = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in extensions)

    total_files = 0
    total_fixes = 0
    for path in paths:
        n = process_file(path, args.dry_run)
        if n:
            total_files += 1
            total_fixes += n

    verb = "would be made" if args.dry_run else "made"
    print(f"\nDone: {total_fixes} conversion(s) across {total_files} file(s) {verb}.")


if __name__ == "__main__":
    main()