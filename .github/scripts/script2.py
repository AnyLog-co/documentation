import os
import re
from pathlib import Path

# Prefix components
space = "    "
branch = "│   "

# Pointers
tee = "├── "
last = "└── "

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
        return (major, minor, path.name.lower())

    return (float("inf"), 0, path.name.lower())


def markdown_link(path: Path):
    """Return a markdown link relative to DIR_PATH."""
    relative = path.relative_to(DIR_PATH).as_posix()

    if path.is_dir():
        relative += "/"

    # Remove the numeric prefix from the displayed name.
    title = path.name.split("-", 1)[-1].strip()

    return f"[{title}]({relative})"


def tree(dir_path: Path, prefix: str = ""):
    """Recursively yield a visual tree structure line by line."""

    contents = sorted(
        dir_path.iterdir(),
        key=sort_key
    )

    pointers = [tee] * (len(contents) - 1) + [last]

    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + markdown_link(path)

        if path.is_dir():
            extension = branch if pointer == tee else space
            yield from tree(path, prefix + extension)


def get_top_level_directories():
    """Return only numbered top-level directories 01 through 20."""

    directories = [
        path
        for path in DIR_PATH.iterdir()
        if path.is_dir()
        and path.name.split("-", 1)[0].strip().isdigit()
        and 1 <= int(path.name.split("-", 1)[0].strip()) <= 20
    ]

    return sorted(directories, key=sort_key)


def build_tree() -> str:
    """Build the complete documentation tree as a string."""

    lines = []

    directories = get_top_level_directories()

    pointers = [tee] * (len(directories) - 1) + [last]

    for pointer, path in zip(pointers, directories):
        lines.append(pointer + markdown_link(path))

        extension = branch if pointer == tee else space

        lines.extend(tree(path, extension))

    return "\n".join(lines)


def main():
    """Generate the tree and write it to README_TOC.md."""

    content = build_tree()

    OUTPUT_PATH.write_text(
        content + "\n",
        encoding="utf-8"
    )

    print(f"TOC written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
