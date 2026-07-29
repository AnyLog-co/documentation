import os
import re
import urllib.parse
from pathlib import Path


DIR_PATH = Path(
    os.path.expanduser(os.path.expandvars(__file__)).split(".github")[0]
)

OUTPUT_PATH = DIR_PATH / "README_TOC.md"


def sort_key(path: Path):
    """
    Sort by the numeric prefix in the name.

    Examples:
        01- Something.md       -> (1, 0, "01- Something.md")
        02- Something/         -> (2, 0, "02- Something")
        02-1 Something.md      -> (2, 1, "02-1 Something.md")
        05-2 Something.md      -> (5, 2, "05-2 Something.md")
        A- Something.md        -> (inf, 0, "A- Something.md")
    """

    match = re.match(r"^(\d+)(?:-(\d+))?", path.name)

    if match:
        major = int(match.group(1))
        minor = int(match.group(2) or 0)

        return (
            major,
            minor,
            path.name.lower(),
        )

    # Items without a numeric prefix go at the end.
    return (
        float("inf"),
        0,
        path.name.lower(),
    )


def markdown_link(path: Path) -> str:
    """Return a Markdown link relative to DIR_PATH."""

    relative = path.relative_to(DIR_PATH).as_posix()

    if path.is_dir():
        relative += "/"

    # Encode spaces and special characters while preserving /
    relative = urllib.parse.quote(relative, safe="/")

    # Remove numeric prefix from displayed name.
    #
    # 01- Getting Started -> Getting Started
    # 02-1 Something      -> 1 Something
    #
    # If there is no "-", keep the original name.
    if "-" in path.name:
        title = path.name.split("-", 1)[1].strip()
    else:
        title = path.name

    return f"[{title}]({relative})"


def tree(dir_path: Path, depth: int = 0):
    """
    Recursively generate a nested Markdown list.

    Markdown indentation is used instead of ├── / └── so that
    hyperlinks remain clickable.
    """

    contents = sorted(
        dir_path.iterdir(),
        key=sort_key,
    )

    indent = "  " * depth

    for path in contents:
        yield f"{indent}- {markdown_link(path)}"

        if path.is_dir():
            yield from tree(path, depth + 1)


def get_top_level_directories():
    """Return only top-level directories 01 through 20."""

    directories = []

    for path in DIR_PATH.iterdir():
        if not path.is_dir():
            continue

        prefix = path.name.split("-", 1)[0].strip()

        if not prefix.isdigit():
            continue

        number = int(prefix)

        if 1 <= number <= 20:
            directories.append(path)

    return sorted(
        directories,
        key=sort_key,
    )


def build_tree() -> str:
    """Build the complete Markdown TOC."""

    lines = []

    for path in get_top_level_directories():
        lines.append(f"- {markdown_link(path)}")

        if path.is_dir():
            lines.extend(
                tree(path, depth=1)
            )

    return "\n".join(lines)


def main():
    """Generate the TOC and write it to README_TOC.md."""

    content = build_tree()

    OUTPUT_PATH.write_text(
        content + "\n",
        encoding="utf-8",
    )

    print(f"TOC written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
