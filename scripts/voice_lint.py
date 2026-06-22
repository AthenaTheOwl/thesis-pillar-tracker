from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANNED_TERMS = [
    "lever" + "age",
    "syn" + "ergy",
    "best" + "-in-class",
    "seam" + "less",
    "cutting" + "-edge",
]
DEFAULT_TARGETS = [
    ROOT / "README.md",
    ROOT / "STATUS.md",
    ROOT / "docs",
    ROOT / "specs",
    ROOT / "thesis",
    ROOT / "monthly_reviews",
    ROOT / "quarterly_snapshots",
]
SKIP_NAMES = {"AGENTS.md"}
SKIP_PARTS = {".git", ".pytest_cache", ".pytest_tmp", "__pycache__"}


def markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() == ".md":
            if path.name not in SKIP_NAMES and not (set(path.parts) & SKIP_PARTS):
                files.append(path)
        elif path.is_dir():
            files.extend(
                candidate
                for candidate in sorted(path.rglob("*.md"))
                if candidate.name not in SKIP_NAMES
                and not (set(candidate.parts) & SKIP_PARTS)
            )
    return files


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    findings: list[str] = []
    for term in BANNED_TERMS:
        pattern = re.compile(rf"(?<![A-Za-z0-9-]){re.escape(term)}(?![A-Za-z0-9-])", re.I)
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"{path.relative_to(ROOT)}:{line}: banned term '{term}'")
    return findings


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    targets = [ROOT / arg for arg in argv] if argv else DEFAULT_TARGETS
    findings: list[str] = []
    for path in markdown_files(targets):
        findings.extend(check_file(path))

    if findings:
        for finding in findings:
            print(finding)
        return 1
    print("OK: voice lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
