#!/usr/bin/env python3
"""
Clean up mixed HTML/Markdown anchor IDs in Jekyll (kramdown) docs.

kramdown auto-generates an id for every heading by lowercasing the heading
text and replacing runs of non-alphanumeric characters with a single hyphen
(duplicate headings get -1, -2, ... appended). That means a manual
    <a id="bucket-file-upload"></a>
    ### Bucket File Upload
is redundant (and produces a duplicate id in the rendered HTML) whenever the
explicit id exactly matches the slug kramdown would generate anyway.

This script, for every heading in a file:
  1. Computes the kramdown auto-slug (handling duplicate-heading suffixes).
  2. If a `<a id="...">`/`<a name="...">` tag sits directly above (or on) the
     heading line and its id matches the auto-slug, the tag is removed as
     redundant.
  3. If the explicit id does NOT match the auto-slug (a genuinely custom
     anchor), it's left alone and reported, since removing it could break
     links elsewhere.
  4. Rewrites in-file link references [text](#Some-Anchor) whose casing
     doesn't match the real slug, so links that are silently broken (e.g.
     #Get-All-Bucket-Names vs the real get-all-bucket-names) start working.

Usage:
    python3 fix_anchors.py /path/to/documentation             # apply changes
    python3 fix_anchors.py /path/to/documentation --dry-run   # preview only
    python3 fix_anchors.py /path/to/documentation --ext .md,.mdx
"""

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
ANCHOR_TAG_RE = re.compile(r'^\s*<a\s+(?:id|name)\s*=\s*"([^"]+)"\s*>\s*</a>\s*$', re.IGNORECASE)
LINK_RE = re.compile(r'\[([^\]]*)\]\(#([^\s)]+)\)')

# Fenced code blocks shouldn't have their contents touched.
FENCE_RE = re.compile(r'^\s*```')


def kramdown_slug(text: str) -> str:
    """Approximate kramdown's auto-generated heading id algorithm."""
    # Strip markdown emphasis/code/link markup that wouldn't count toward the id text
    stripped = re.sub(r'[`*_]', '', text)
    stripped = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', stripped)
    slug = stripped.strip().lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-{2,}', '-', slug)
    slug = slug.strip('-')
    return slug


def compute_heading_slugs(lines):
    """
    Walk the file (skipping fenced code blocks) and return, for each heading
    line index, its final kramdown slug (accounting for -1, -2 dedup suffixes).
    Returns dict: line_index -> slug
    """
    seen = {}
    result = {}
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = kramdown_slug(m.group(2))
        if base in seen:
            seen[base] += 1
            slug = f"{base}-{seen[base]}"
        else:
            seen[base] = 0
            slug = base
        result[i] = slug
    return result


def process_file(path: Path, dry_run: bool):
    raw = path.read_bytes()
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")
    lines = text.splitlines()

    heading_slugs = compute_heading_slugs(lines)
    removed_anchors = []
    custom_anchors = []

    # Step 1: find <a id="..."> lines immediately preceding a heading line
    # (allowing a single blank line between), and drop them if redundant.
    to_delete = set()
    for i, line in enumerate(lines):
        am = ANCHOR_TAG_RE.match(line)
        if not am:
            continue
        anchor_id = am.group(1)

        # look ahead for the next non-blank line
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and j in heading_slugs:
            if heading_slugs[j] == anchor_id:
                to_delete.add(i)
                removed_anchors.append(anchor_id)
                continue
        custom_anchors.append((i + 1, anchor_id))

    new_lines = [line for idx, line in enumerate(lines) if idx not in to_delete]

    # Collapse a run of blank lines down to a single blank line (removing an
    # anchor that had its own blank-line spacing above a heading can leave
    # two consecutive blank lines behind).
    collapsed = []
    for line in new_lines:
        if line.strip() == "" and collapsed and collapsed[-1].strip() == "":
            continue
        collapsed.append(line)
    new_lines = collapsed

    updated_text = "\n".join(new_lines)
    trailing = "\n" if text.endswith("\n") else ""

    # Step 2: build the authoritative slug set (post-removal, slugs unchanged
    # since we only removed redundant lines) for fixing link casing.
    valid_slugs = set(heading_slugs.values())
    valid_slugs.update(anchor_id for _, anchor_id in custom_anchors)
    lower_to_real = {s.lower(): s for s in valid_slugs}

    fixed_links = []

    def fix_link(m):
        link_text, anchor = m.group(1), m.group(2)
        if anchor in valid_slugs:
            return m.group(0)
        real = lower_to_real.get(anchor.lower())
        if real and real != anchor:
            fixed_links.append((anchor, real))
            return f"[{link_text}](#{real})"
        return m.group(0)

    updated_text = LINK_RE.sub(fix_link, updated_text) + trailing

    changed = updated_text != text
    if changed:
        if dry_run:
            print(f"[DRY RUN] {path}")
        else:
            out_bytes = updated_text.replace("\n", newline.decode("ascii")).encode("utf-8")
            path.write_bytes(out_bytes)
            print(f"{path}")
        if removed_anchors:
            print(f"  - removed {len(removed_anchors)} redundant anchor(s): {', '.join(removed_anchors)}")
        if fixed_links:
            for old, new in fixed_links:
                print(f"  - fixed link casing: #{old} -> #{new}")
    if custom_anchors:
        for lineno, anchor_id in custom_anchors:
            print(f"  ! kept custom anchor '#{anchor_id}' at {path}:{lineno} (doesn't match any heading slug)")

    return len(removed_anchors) + len(fixed_links)


def main():
    parser = argparse.ArgumentParser(description="Fix mixed HTML/Markdown anchor IDs in Jekyll docs.")
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
    print(f"\nDone: {total_fixes} fix(es) across {total_files} file(s) {verb}.")


if __name__ == "__main__":
    main()