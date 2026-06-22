from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

VALID_STATUSES = {"active", "weakened", "invalidated", "retired"}
PILLAR_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
QUARTER_RE = re.compile(r"^\d{4}Q[1-4]$")
EVIDENCE_RE = re.compile(
    r"^- \d{4}-\d{2}-\d{2} "
    r"(CONFIRMS|WEAKENS|INVALIDATES|NEUTRAL) "
    r"\[[^\]]+\] - .+$"
)


class ArtifactError(ValueError):
    """Raised when a repo artifact violates the local file contract."""


@dataclass(frozen=True)
class Pillar:
    path: Path
    data: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def title(self) -> str:
        return str(self.data["title"])

    @property
    def status(self) -> str:
        return str(self.data["status"])


def today_iso() -> str:
    return date.today().isoformat()


def clean_single_line(value: str, field_name: str) -> str:
    cleaned = " ".join(value.strip().split())
    if not cleaned:
        raise ArtifactError(f"{field_name} cannot be empty")
    return cleaned


def validate_pillar_id(pillar_id: str) -> str:
    pillar_id = clean_single_line(pillar_id, "id")
    if not PILLAR_ID_RE.fullmatch(pillar_id):
        raise ArtifactError("id must use lowercase letters, numbers, and hyphens")
    return pillar_id


def validate_month(month: str) -> str:
    month = clean_single_line(month, "month")
    if not MONTH_RE.fullmatch(month):
        raise ArtifactError("month must use YYYY-MM")
    return month


def validate_quarter(quarter: str) -> str:
    quarter = clean_single_line(quarter, "quarter")
    if not QUARTER_RE.fullmatch(quarter):
        raise ArtifactError("quarter must use YYYYQn")
    return quarter


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ArtifactError("missing frontmatter start")
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        raise ArtifactError("missing frontmatter end")

    frontmatter = _parse_frontmatter_lines(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body


def _parse_frontmatter_lines(lines: list[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    list_key: str | None = None

    for line in lines:
        if not line.strip():
            continue
        if line.startswith("  - ") and list_key:
            data.setdefault(list_key, []).append(line[4:].strip())
            continue
        if ":" not in line:
            raise ArtifactError(f"invalid frontmatter line: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        list_key = None

        if not key:
            raise ArtifactError("frontmatter key cannot be empty")
        if value == "":
            data[key] = []
            list_key = key
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [] if not inner else [item.strip() for item in inner.split(",")]
            continue
        if value.lower() == "true":
            data[key] = True
            continue
        if value.lower() == "false":
            data[key] = False
            continue

        data[key] = value.strip('"').strip("'")

    return data


def render_pillar(
    pillar_id: str,
    title: str,
    claim: str,
    falsification: str,
    created: str | None = None,
) -> str:
    pillar_id = validate_pillar_id(pillar_id)
    title = clean_single_line(title, "title")
    claim = clean_single_line(claim, "claim")
    falsification = clean_single_line(falsification, "falsification")
    created = created or today_iso()

    return (
        "---\n"
        f"id: {pillar_id}\n"
        f"title: {title}\n"
        f"claim: {claim}\n"
        f"falsification: {falsification}\n"
        f"created: {created}\n"
        "status: active\n"
        "---\n\n"
        "# "
        f"{title}\n\n"
        "## Evidence log\n\n"
        f"- {created} NEUTRAL [scaffold] - pillar created; no public-event evidence logged yet\n"
    )


def create_pillar(
    pillar_id: str,
    title: str,
    claim: str,
    falsification: str,
    root: Path,
    created: str | None = None,
) -> Path:
    text = render_pillar(pillar_id, title, claim, falsification, created)
    path = root / "thesis" / f"{validate_pillar_id(pillar_id)}.md"
    if path.exists():
        raise ArtifactError(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def load_pillars(root: Path) -> list[Pillar]:
    thesis_dir = root / "thesis"
    if not thesis_dir.exists():
        return []
    pillars: list[Pillar] = []
    for path in sorted(thesis_dir.glob("*.md")):
        data, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        pillars.append(Pillar(path=path, data=data, body=body))
    return pillars


def active_pillars(root: Path) -> list[Pillar]:
    return [pillar for pillar in load_pillars(root) if pillar.status == "active"]


def render_quarterly_snapshot(
    quarter: str,
    binding_constraint: str,
    delta: str,
    confidence: str,
) -> str:
    quarter = validate_quarter(quarter)
    binding_constraint = clean_single_line(binding_constraint, "binding constraint")
    delta = clean_single_line(delta, "delta")
    confidence = clean_single_line(confidence, "confidence")

    return (
        "---\n"
        f"quarter: {quarter}\n"
        f"current_binding_constraint: {binding_constraint}\n"
        f"delta_vs_prior_quarter: {delta}\n"
        f"confidence: {confidence}\n"
        "---\n\n"
        f"# Quarterly snapshot - {quarter}\n\n"
        "## Binding constraint\n\n"
        f"- Current constraint: {binding_constraint}\n"
        f"- Delta vs prior quarter: {delta}\n"
        f"- Confidence: {confidence}\n\n"
        "## Evidence to review next\n\n"
        "- Add accepted public-event evidence before raising confidence.\n"
    )


def create_quarterly_snapshot(
    root: Path,
    quarter: str,
    binding_constraint: str,
    delta: str,
    confidence: str = "low",
    force: bool = False,
) -> Path:
    quarter = validate_quarter(quarter)
    path = root / "quarterly_snapshots" / f"{quarter}.md"
    if path.exists() and not force:
        raise ArtifactError(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = render_quarterly_snapshot(quarter, binding_constraint, delta, confidence)
    path.write_text(text, encoding="utf-8")
    return path
