#!/usr/bin/env python3
"""
validate_md_links.py

Scans Markdown files for links/images and validates them:
  - Relative file paths  -> checked against the filesystem
  - http(s) URLs         -> optionally checked with a real request
  - mailto: / #anchors   -> noted but not treated as broken

Designed to complement generate_toc.py / script2.py, whose links look like:
    [my data](../03- dir3/01- file1.md)
    [Some Section](../02-1%20Something.md)   (space -> %20 via urllib.parse.quote)

Usage:
    python3 validate_md_links.py [ROOT_DIR] [options]

Options:
    --check-urls        Actually request http(s) links (default: skip, syntax-only)
    --timeout SECONDS   Timeout per URL request (default: 8)
    --ext .md,.markdown Comma-separated list of file extensions to scan (default: .md)
    --quiet             Only print broken links, no per-file summary of OK links

Exit code is 1 if any broken links were found, 0 otherwise (handy for CI).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path


LINK_PATTERN = re.compile(r"!?\[([^\]]*)\]\(([^)]*)\)")
TITLE_SUFFIX = re.compile(r'\s+"[^"]*"$')  # strips optional [text](path "title")

# Matches a leading numeric prefix like "01-", "02-1 " etc., mirroring script2.py's
# own sort_key()/markdown_link() convention, so renamed-prefix files can still match.
PREFIX_STRIP = re.compile(r"^\d+(?:-\d+)?[-\s]*")


@dataclass
class LinkResult:
    md_file: Path
    link_text: str
    raw_dest: str
    kind: str          # "local" | "url" | "anchor" | "mailto"
    ok: bool
    detail: str = ""
    span: tuple[int, int] | None = None   # position of raw_dest within the source file text
    suggested_dest: str | None = None     # proposed replacement, if a confident match was found


def iter_markdown_files(root: Path, extensions: set[str]):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def extract_links(text: str):
    for match in LINK_PATTERN.finditer(text):
        link_text = match.group(1)
        raw = match.group(2)
        dest = TITLE_SUFFIX.sub("", raw.strip()).strip()
        if dest:
            # Only offer positional replacement when there's no "title" suffix and
            # no surrounding whitespace to worry about -- keeps --apply-fix conservative.
            span = match.span(2) if raw.strip() == dest else None
            yield link_text, dest, span


def classify_and_check(md_file: Path, link_text: str, dest: str, span, root: Path) -> LinkResult:
    if dest.startswith(("http://", "https://")):
        return LinkResult(md_file, link_text, dest, "url", ok=True, detail="not checked", span=span)

    if dest.startswith("mailto:"):
        return LinkResult(md_file, link_text, dest, "mailto", ok=True, span=span)

    if dest.startswith("#"):
        return LinkResult(md_file, link_text, dest, "anchor", ok=True,
                           detail="in-page anchor, not verified", span=span)

    # Relative (or absolute) local path, possibly with a trailing #anchor
    path_part, has_anchor, anchor = dest.partition("#")
    if not path_part:
        return LinkResult(md_file, link_text, dest, "anchor", ok=True, detail="anchor-only", span=span)

    # Try both the raw path and the percent-decoded version
    candidates = [path_part]
    decoded = urllib.parse.unquote(path_part)
    if decoded != path_part:
        candidates.append(decoded)

    base_dir = md_file.parent
    for candidate in candidates:
        resolved = (base_dir / candidate).resolve()
        if resolved.exists():
            return LinkResult(md_file, link_text, dest, "local", ok=True, detail=str(resolved), span=span)

    attempted = (base_dir / candidates[0]).resolve()
    result = LinkResult(md_file, link_text, dest, "local", ok=False,
                         detail=f"not found: {attempted}", span=span)

    suggestion = find_fix(base_dir, decoded, root)
    if suggestion is not None:
        new_dest = suggestion + (f"#{anchor}" if has_anchor else "")
        result.suggested_dest = new_dest
        result.detail += f"  (suggested fix: {new_dest})"

    return result


def _basename_key(name: str) -> str:
    """Strip a numeric prefix (01-, 02-1 , ...) so renamed-prefix files still match."""
    return PREFIX_STRIP.sub("", name).lower()


def find_fix(base_dir: Path, decoded_path_part: str, root: Path) -> str | None:
    """
    Best-effort repair for a broken local link: look for a file/dir elsewhere in the
    repo whose name matches the broken target's basename (ignoring numeric prefixes,
    since those are what typically change when files get reordered/renamed under the
    01-/02-/... convention used by script2.py). Only returns a suggestion when exactly
    one candidate matches, to avoid guessing wrong.
    """
    target_name = Path(decoded_path_part.rstrip("/")).name
    if not target_name:
        return None

    target_key = _basename_key(target_name)
    wants_dir = decoded_path_part.endswith("/")

    matches = []
    for candidate in root.rglob("*"):
        if wants_dir and not candidate.is_dir():
            continue
        if candidate.name == target_name or _basename_key(candidate.name) == target_key:
            matches.append(candidate)

    if len(matches) != 1:
        return None

    match = matches[0]
    relative = os.path.relpath(match, start=base_dir)
    relative = Path(relative).as_posix()
    if match.is_dir() and not relative.endswith("/"):
        relative += "/"

    # Match generate_toc.py's own encoding convention (spaces -> %20, "/" preserved).
    return urllib.parse.quote(relative, safe="/")


def check_url(dest: str, timeout: float) -> tuple[bool, str]:
    req = urllib.request.Request(dest, method="HEAD", headers={"User-Agent": "link-checker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 405:  # HEAD not allowed, retry with GET
            try:
                req_get = urllib.request.Request(dest, method="GET", headers={"User-Agent": "link-checker/1.0"})
                with urllib.request.urlopen(req_get, timeout=timeout) as resp:
                    return True, f"HTTP {resp.status}"
            except Exception as e2:
                return False, f"GET failed: {e2}"
        return e.code < 400, f"HTTP {e.code}"
    except Exception as e:
        return False, f"unreachable: {e}"


def main():
    parser = argparse.ArgumentParser(description="Validate paths & URLs in Markdown files.")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan (default: current dir)")
    parser.add_argument("--check-urls", action="store_true", help="Actually request http(s) links")
    parser.add_argument("--timeout", type=float, default=8.0, help="Timeout per URL request in seconds")
    parser.add_argument("--ext", default=".md", help="Comma-separated file extensions to scan (default: .md)")
    parser.add_argument("--quiet", action="store_true", help="Only print broken links")
    parser.add_argument("--fix", action="store_true",
                         help="For broken local links, search the repo for a matching "
                              "file/dir (ignoring numeric prefixes) and print a suggested fix")
    parser.add_argument("--apply-fix", action="store_true",
                         help="Like --fix, but rewrites the suggested links in place")
    args = parser.parse_args()
    if args.apply_fix:
        args.fix = True

    root = Path(args.root).resolve()
    extensions = {e if e.startswith(".") else f".{e}" for e in args.ext.split(",")}

    if not root.exists():
        print(f"Root path does not exist: {root}", file=sys.stderr)
        sys.exit(2)

    last_file = None
    results: list[LinkResult] = []

    for md_file in iter_markdown_files(root, extensions):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        for link_text, dest, span in extract_links(text):
            result = classify_and_check(md_file, link_text, dest, span, root)
            if result.kind == "url" and args.check_urls:
                ok, detail = check_url(dest, args.timeout)
                result.ok, result.detail = ok, detail
            if args.fix and not result.ok and result.kind == "local" and result.suggested_dest is None:
                result.detail += "  (no unambiguous match found for auto-fix)"
            results.append(result)

    broken = [r for r in results if not r.ok]

    if args.apply_fix:
        fixable = [r for r in broken if r.suggested_dest and r.span is not None]
        by_file_fixes: dict[Path, list[LinkResult]] = {}
        for r in fixable:
            by_file_fixes.setdefault(r.md_file, []).append(r)

        for md_file, fixes in by_file_fixes.items():
            text = md_file.read_text(encoding="utf-8", errors="replace")
            for r in sorted(fixes, key=lambda r: r.span[0], reverse=True):
                start, end = r.span
                text = text[:start] + r.suggested_dest + text[end:]
            md_file.write_text(text, encoding="utf-8")
            print(f"Applied {len(fixes)} fix(es) in {md_file.relative_to(root)}")

    if not args.quiet:
        by_file: dict[Path, list[LinkResult]] = {}
        for r in results:
            by_file.setdefault(r.md_file, []).append(r)

        for md_file, file_results in by_file.items():
            rel = md_file.relative_to(root)
            print(f"\n{rel}  ({len(file_results)} link(s))")
            for r in file_results:
                status = "OK  " if r.ok else "FAIL"
                print(f"  [{status}] ({r.kind:6}) {r.raw_dest}"
                      f"{'  -> ' + r.detail if r.detail else ''}" if )

    # print("\n" + "=" * 60)
    if broken:
        print(f"{len(broken)} broken link(s) found:\n")
        for r in broken:
            rel = r.md_file.relative_to(root)
            if last_file is None:
                last_file = rel

            print(f"  {rel}: [{r.link_text}]({r.raw_dest})  -> {r.detail}")
        sys.exit(1)
    else:
        checked = len(results)
        print(f"All {checked} link(s) OK."
              + ("" if args.check_urls else " (URLs were syntax-checked only; pass --check-urls to request them)"))
        sys.exit(0)


if __name__ == "__main__":
    main()