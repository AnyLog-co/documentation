#!/usr/bin/env python3
"""
convert_links.py — convert all markdown links in _docs/ to Jekyll relative_url tags.

Before: [Remote-GUI](../Tools%20%26%20UI/remote-gui.md)
After:  <a href="{{ '/docs/Tools-UI/remote-gui/' | relative_url }}">Remote-GUI</a>

Also handles:
  - Same-folder links:   [text](file.md)
  - URL-encoded paths:   Tools%20%26%20UI  →  Tools-UI
  - Anchor-only links:   [text](#anchor)   →  left as-is
  - External links:      [text](https://…) →  left as-is
  - Links already converted (containing relative_url) → skipped

Run from the repo root:
    python3 .github/scripts/convert_links.py

Dry-run (print changes without writing):
    python3 .github/scripts/convert_links.py --dry-run
"""

import os
import re
import sys
import argparse
from urllib.parse import unquote

# ── Folder name mapping ───────────────────────────────────────────────────────
# Maps decoded folder names (as they appear in links) to filesystem folder names.
# Add entries here if new folders are added to _docs/.
FOLDER_MAP = {
    "CLI":                        "CLI",
    "Getting Started":            "Getting-Started",
    "Getting-Started":            "Getting-Started",
    "Managing Data (Southbound)": "Managing-Data-Southbound",
    "Managing-Data-Southbound":   "Managing-Data-Southbound",
    "Managing Data Southbound":   "Managing-Data-Southbound",
    "Monitoring & Operations":    "Monitoring-Operations",
    "Monitoring-Operations":      "Monitoring-Operations",
    "Monitoring Operations":      "Monitoring-Operations",
    "Network & Services":         "Network-Services",
    "Network-Services":           "Network-Services",
    "Network Services":           "Network-Services",
    "Querying Data (Northbound)": "Querying-Data-Northbound",
    "Querying-Data-Northbound":   "Querying-Data-Northbound",
    "Querying Data Northbound":   "Querying-Data-Northbound",
    "Reference":                  "Reference",
    "Tools & UI":                 "Tools-UI",
    "Tools-UI":                   "Tools-UI",
    "Tools UI":                   "Tools-UI",
    "Version Control":            "Version-Control",
    "Version-Control":            "Version-Control",
}


def resolve_folder(raw_folder: str) -> str:
    """Decode URL encoding and map to the correct filesystem folder name."""
    decoded = unquote(raw_folder)
    if decoded in FOLDER_MAP:
        return FOLDER_MAP[decoded]
    # Fall back: strip spaces/special chars the same way Jekyll does
    return decoded


def link_to_jekyll(href: str, current_folder: str) -> str | None:
    """
    Convert a markdown href to a Jekyll /docs/Folder/slug/ path.
    Returns None if the link should be left as-is.
    """
    # Skip external links
    if href.startswith(("http://", "https://", "mailto:")):
        return None
    # Skip anchor-only links
    if href.startswith("#"):
        return None
    # Skip already-converted links
    if "relative_url" in href:
        return None

    # Split off any trailing anchor
    anchor = ""
    if "#" in href:
        href, anchor = href.split("#", 1)
        anchor = "#" + anchor

    # Strip .md extension
    if href.endswith(".md"):
        href = href[:-3]

    # Normalise separators
    href = href.replace("\\", "/")

    # Resolve relative path components
    parts = href.split("/")

    if href.startswith("../"):
        # Cross-folder: ../FolderName/slug  or  ../../FolderName/slug
        # Drop all leading ../
        while parts and parts[0] == "..":
            parts.pop(0)
        if len(parts) == 2:
            folder, slug = parts
            folder = resolve_folder(folder)
        elif len(parts) == 1:
            # ../slug — one level up, same parent — unusual but handle it
            folder = current_folder
            slug = parts[0]
        else:
            # Deeper nesting — just join and hope for the best
            folder = resolve_folder(parts[0])
            slug = "/".join(parts[1:])
    elif len(parts) == 1:
        # Same-folder link: slug only
        folder = current_folder
        slug = parts[0]
    elif len(parts) == 2:
        # Folder/slug with no ../
        folder = resolve_folder(parts[0])
        slug = parts[1]
    else:
        # Absolute-ish path — take last two components
        folder = resolve_folder(parts[-2])
        slug = parts[-1]

    jekyll_path = f"/docs/{folder}/{slug}/"
    return jekyll_path + anchor


def convert_links_in_text(text: str, current_folder: str) -> tuple[str, int]:
    """
    Find all markdown links [text](href) in text and convert them.
    Returns (new_text, count_of_changes).
    """
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    changes = 0

    def replace(match):
        nonlocal changes
        label = match.group(1)
        href = match.group(2).strip()

        jekyll_path = link_to_jekyll(href, current_folder)
        if jekyll_path is None:
            return match.group(0)  # leave unchanged

        changes += 1
        return f'<a href="{{{{ \'{jekyll_path}\' | relative_url }}}}">{label}</a>'

    new_text = pattern.sub(replace, text)
    return new_text, changes


def process_file(filepath: str, dry_run: bool = False) -> int:
    """Process a single markdown file. Returns number of changes made."""
    # Determine current folder from file path
    parts = filepath.replace("\\", "/").split("/")
    # Find _docs in path and take the folder after it
    try:
        docs_idx = parts.index("_docs")
        current_folder = parts[docs_idx + 1] if docs_idx + 1 < len(parts) - 1 else "root"
    except ValueError:
        current_folder = "root"

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    converted, changes = convert_links_in_text(original, current_folder)

    if changes == 0:
        return 0

    if dry_run:
        print(f"\n{'─'*60}")
        print(f"FILE: {filepath}  ({changes} change{'s' if changes != 1 else ''})")
        # Show a diff-style preview
        orig_lines = original.splitlines()
        new_lines = converted.splitlines()
        for i, (o, n) in enumerate(zip(orig_lines, new_lines)):
            if o != n:
                print(f"  line {i+1}")
                print(f"  - {o.strip()}")
                print(f"  + {n.strip()}")
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(converted)
        print(f"  {filepath}: {changes} link{'s' if changes != 1 else ''} converted")

    return changes


def main():
    parser = argparse.ArgumentParser(description="Convert markdown links to Jekyll relative_url tags.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--docs-dir", default="_docs", help="Path to the _docs directory (default: _docs)")
    args = parser.parse_args()

    docs_dir = args.docs_dir
    if not os.path.isdir(docs_dir):
        print(f"Error: docs directory not found: {docs_dir}")
        sys.exit(1)

    total_files = 0
    total_changes = 0

    print(f"{'DRY RUN — ' if args.dry_run else ''}Converting links in {docs_dir}/\n")

    for root, _, files in os.walk(docs_dir):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            changes = process_file(filepath, dry_run=args.dry_run)
            if changes:
                total_files += 1
                total_changes += changes

    print(f"\n{'─'*60}")
    print(f"{'Would convert' if args.dry_run else 'Converted'} {total_changes} link{'s' if total_changes != 1 else ''} across {total_files} file{'s' if total_files != 1 else ''}.")
    if args.dry_run:
        print("Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()