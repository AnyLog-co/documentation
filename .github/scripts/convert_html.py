#!/usr/bin/env python3
"""
Convert Markdown links and/or images to HTML/JSX tags, recursively across a
directory tree (or a single file).

  --url   [text](url)              ->  <a href="url" target="_blank">text</a>
  --img   ![alt]({path})           ->  <img src={path} alt="alt" />
          ![alt](images/pic.png)   ->  <img src="images/pic.png" alt="alt" />

Rule for image `src`: if the path in the parens is already a `{...}`
expression (e.g. an imported image variable, common in MDX/JSX docs), it's
kept as an unquoted JSX expression: `src={path}`. Anything else (a plain
string path or URL) is emitted as a quoted JSX string.

Fenced code blocks (```...```) are always left untouched, so example syntax
written inside a code fence isn't rewritten. Image syntax (![...]) is never
mistaken for a link even when --url is on.

At least one of --url / --img must be given.

Usage:
    python3 convert_md.py /path/to/docs --url                   # links only
    python3 convert_md.py /path/to/docs --img                   # images only
    python3 convert_md.py /path/to/docs --url --img              # both
    python3 convert_md.py /path/to/docs --url --img --dry-run    # preview only
    python3 convert_md.py /path/to/docs --url --ext .md,.mdx
    python3 convert_md.py somefile.md --url --img                # single file works too
"""

import argparse
import re
import sys
from pathlib import Path

# [text](url) -- but not ![text](url) (that's an image).
MD_LINK_RE = re.compile(r'(?<!!)\[([^\]]+)\]\((\S+?)\)')

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
    """Escape a value for safe placement inside a double-quoted attribute."""
    return value.replace("&", "&amp;").replace('"', "&quot;")


def convert_links(line: str, converted: list) -> str:
    def repl(m):
        text, url = m.group(1), m.group(2)
        new = f'<a href="{url}" target="_blank">{text}</a>'
        converted.append((m.group(0), new))
        return new

    return MD_LINK_RE.sub(repl, line)


def convert_images(line: str, converted: list) -> str:
    def repl(m):
        alt, src, title_dq, title_sq = m.group(1), m.group(2), m.group(3), m.group(4)
        title = title_dq if title_dq is not None else title_sq

        if src.startswith("{") and src.endswith("}"):
            src_attr = f"src={src}"
        else:
            src_attr = f'src="{escape_attr(src)}"'

        attrs = f'{src_attr} alt="{escape_attr(alt)}"'
        if title:
            attrs += f' title="{escape_attr(title)}"'
        new = f"<img {attrs} />"
        converted.append((m.group(0), new))
        return new

    return IMAGE_RE.sub(repl, line)


def process_file(path: Path, dry_run: bool, do_url: bool, do_img: bool) -> int:
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
        # Images first, so ![alt](src) isn't ever partially matched as a link.
        if do_img:
            line = convert_images(line, converted)
        if do_url:
            line = convert_links(line, converted)
        new_lines.append(line)

    trailing = "\n" if text.endswith("\n") else ""
    updated_text = "\n".join(new_lines) + trailing

    changed = updated_text != text
    if changed:
        if dry_run:
            print(f"[DRY RUN] {path} -> {len(converted)} conversion(s) would be made")
        else:
            out_bytes = updated_text.replace("\n", newline.decode("ascii")).encode("utf-8")
            path.write_bytes(out_bytes)
            print(f"{path} -> {len(converted)} conversion(s) made")
        for old, new in converted:
            print(f"  - {old} -> {new}")
    return len(converted)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown links and/or images to HTML/JSX tags."
    )
    parser.add_argument("root", help="Root directory (or single file) to process")
    parser.add_argument("--url", action="store_true", help="Convert [text](url) links to <a target=\"_blank\">")
    parser.add_argument("--img", action="store_true", help="Convert ![alt](src) images to JSX <img />")
    parser.add_argument("--ext", default=".md", help="Comma-separated file extensions (default: .md)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    args = parser.parse_args()

    if not args.url and not args.img:
        parser.error("must specify --url and/or --img")

    root = Path(args.root)
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    extensions = tuple(e.strip() if e.strip().startswith(".") else f".{e.strip()}"
                        for e in args.ext.split(","))

    paths = [root] if root.is_file() else sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix in extensions
    )

    total_files = 0
    total_conversions = 0
    for path in paths:
        n = process_file(path, args.dry_run, args.url, args.img)
        if n:
            total_files += 1
            total_conversions += n

    verb = "would be made" if args.dry_run else "made"
    print(f"\nDone: {total_conversions} conversion(s) across {total_files} file(s) {verb}.")


if __name__ == "__main__":
    main()