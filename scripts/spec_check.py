from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_HEADINGS = [
    "## Current state",
    "## Known limits",
    "## Next feature queue",
]
REQUIRED_FILES = [
    "PRODUCT_BRIEF.md",
    "SYSTEM_MAP.md",
    "specs/0002-design/requirements.md",
    "specs/0002-design/design.md",
    "specs/0002-design/acceptance.md",
    "specs/0002-design/tasks.md",
    "specs/0002-design/ledger.md",
    "schemas/pillar.schema.json",
    "schemas/monthly_review.schema.json",
    "thesis_pillar_tracker/__init__.py",
    "thesis_pillar_tracker/cli.py",
    "thesis_pillar_tracker/model.py",
    "thesis_pillar_tracker/scoring.py",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def check_status() -> None:
    path = ROOT / "STATUS.md"
    if not path.exists():
        fail("STATUS.md is missing")
    text = path.read_text(encoding="utf-8")
    headings = re.findall(r"^## .+$", text, flags=re.M)
    for required in STATUS_HEADINGS:
        if required not in headings:
            fail(f"STATUS.md missing heading: {required}")
    positions = [headings.index(required) for required in STATUS_HEADINGS]
    if positions != sorted(positions):
        fail("STATUS.md headings are out of order")


def check_pyproject() -> None:
    path = ROOT / "pyproject.toml"
    if not path.exists():
        fail("pyproject.toml is missing")
    text = path.read_text(encoding="utf-8")
    if "[dependency-groups]" not in text:
        fail("pyproject.toml must declare [dependency-groups]")
    if "[project.optional-dependencies]" in text:
        fail("pyproject.toml must not use [project.optional-dependencies]")
    if "[tool.uv]" not in text or "package = true" not in text:
        fail("pyproject.toml must set [tool.uv] package = true")


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def check_report_artifacts() -> None:
    monthly = sorted((ROOT / "monthly_reviews").glob("*.md"))
    reports = sorted((ROOT / "reports").glob("*.jsonl"))
    quarterly = sorted((ROOT / "quarterly_snapshots").glob("*.md"))
    if not monthly:
        fail("at least one monthly review artifact is required")
    if not reports:
        fail("at least one jsonl report artifact is required")
    if not quarterly:
        fail("at least one quarterly snapshot artifact is required")


def main() -> int:
    try:
        check_status()
        check_pyproject()
        check_required_files()
        check_report_artifacts()
    except AssertionError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("OK: spec check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
