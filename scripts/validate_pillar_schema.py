from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from thesis_pillar_tracker.model import (
    EVIDENCE_RE,
    PILLAR_ID_RE,
    VALID_STATUSES,
    ArtifactError,
    active_pillars,
    load_pillars,
    parse_frontmatter,
)

REQUIRED_FIELDS = {"id", "title", "claim", "falsification", "created", "status"}


def validate_repo(root: Path = ROOT) -> None:
    pillars = load_pillars(root)
    if not pillars:
        raise ArtifactError("no pillar files found")

    for pillar in pillars:
        validate_pillar(pillar.path, pillar.data, pillar.body)

    active = active_pillars(root)
    if not 6 <= len(active) <= 12:
        raise ArtifactError(f"active pillar count must be in [6, 12], got {len(active)}")

    for review_path in sorted((root / "monthly_reviews").glob("*.md")):
        validate_monthly_review(root, review_path)


def validate_pillar(path: Path, data: dict[str, object], body: str) -> None:
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        raise ArtifactError(f"{path}: missing fields: {', '.join(missing)}")
    pillar_id = str(data["id"])
    if pillar_id != path.stem:
        raise ArtifactError(f"{path}: id must match filename")
    if not PILLAR_ID_RE.fullmatch(pillar_id):
        raise ArtifactError(f"{path}: invalid id")
    if str(data["status"]) not in VALID_STATUSES:
        raise ArtifactError(f"{path}: invalid status")
    for field in ["title", "claim", "falsification", "created"]:
        if not str(data[field]).strip():
            raise ArtifactError(f"{path}: {field} cannot be empty")
    if "## Evidence log" not in body:
        raise ArtifactError(f"{path}: missing evidence log")

    evidence_lines = [
        line.strip()
        for line in body.splitlines()
        if line.strip().startswith("- ")
    ]
    if not evidence_lines:
        raise ArtifactError(f"{path}: at least one evidence line is required")
    for line in evidence_lines:
        if not EVIDENCE_RE.fullmatch(line):
            raise ArtifactError(f"{path}: invalid evidence line: {line}")


def validate_monthly_review(root: Path, path: Path) -> None:
    data, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
    reviewed = data.get("pillars_reviewed")
    if not isinstance(reviewed, list) or not reviewed:
        raise ArtifactError(f"{path}: pillars_reviewed must be a non-empty list")
    required = {pillar.id for pillar in active_pillars(root)}
    missing = sorted(required - set(str(item) for item in reviewed))
    if missing:
        raise ArtifactError(f"{path}: missing active pillars: {', '.join(missing)}")
    if "portfolio_action_required" not in data:
        raise ArtifactError(f"{path}: missing portfolio_action_required")


def main() -> int:
    try:
        validate_repo(ROOT)
    except ArtifactError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("OK: 6 pillars validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
