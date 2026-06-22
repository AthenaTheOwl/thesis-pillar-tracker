from __future__ import annotations

import json
from pathlib import Path

from thesis_pillar_tracker.model import (
    EVIDENCE_RE,
    ArtifactError,
    Pillar,
    active_pillars,
    clean_single_line,
    today_iso,
    validate_month,
    validate_pillar_id,
)

VALID_VERDICTS = {"CONFIRMS", "WEAKENS", "INVALIDATES", "NEUTRAL"}


def validate_verdict(verdict: str) -> str:
    verdict = clean_single_line(verdict, "verdict").upper()
    if verdict not in VALID_VERDICTS:
        allowed = ", ".join(sorted(VALID_VERDICTS))
        raise ArtifactError(f"verdict must be one of: {allowed}")
    return verdict


def append_evidence(
    pillar_id: str,
    verdict: str,
    source: str,
    note: str,
    root: Path,
    event_date: str | None = None,
) -> Path:
    pillar_id = validate_pillar_id(pillar_id)
    verdict = validate_verdict(verdict)
    source = clean_single_line(source, "source")
    note = clean_single_line(note, "note")
    event_date = event_date or today_iso()
    path = root / "thesis" / f"{pillar_id}.md"
    if not path.exists():
        raise ArtifactError(f"{path} does not exist")

    text = path.read_text(encoding="utf-8")
    if "## Evidence log" not in text:
        raise ArtifactError(f"{path} is missing an evidence log")

    line = f"- {event_date} {verdict} [{source}] - {note}"
    if not EVIDENCE_RE.fullmatch(line):
        raise ArtifactError("evidence line does not match the required shape")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n", encoding="utf-8")
    return path


def default_pillar_verdict(_pillar: Pillar) -> str:
    return "NEUTRAL"


def render_monthly_review(month: str, pillars: list[Pillar]) -> str:
    month = validate_month(month)
    if not pillars:
        raise ArtifactError("monthly review requires at least one active pillar")

    pillar_lines = "\n".join(f"  - {pillar.id}" for pillar in pillars)
    verdict_sections = "\n\n".join(
        (
            f"### {pillar.id}\n"
            f"- Verdict: {default_pillar_verdict(pillar)}\n"
            "- Evidence count this month: 0\n"
            "- Notes: Human reviewer fills this before commit."
        )
        for pillar in pillars
    )
    return (
        "---\n"
        f"month: {month}\n"
        "pillars_reviewed:\n"
        f"{pillar_lines}\n"
        "portfolio_action_required: false\n"
        "---\n\n"
        f"# Monthly review - {month}\n\n"
        "## Summary\n\n"
        "- Portfolio action required: false\n"
        "- Scope: all active pillars.\n"
        "- Default verdicts are neutral until the reviewer records evidence.\n\n"
        "## Pillar verdicts\n\n"
        f"{verdict_sections}\n"
    )


def create_monthly_review(root: Path, month: str, force: bool = False) -> Path:
    month = validate_month(month)
    path = root / "monthly_reviews" / f"{month}.md"
    if path.exists() and not force:
        raise ArtifactError(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = render_monthly_review(month, active_pillars(root))
    path.write_text(text, encoding="utf-8")
    return path


def render_monthly_report_jsonl(
    month: str,
    pillars: list[Pillar],
    portfolio_action_required: bool = False,
) -> str:
    month = validate_month(month)
    rows = []
    for pillar in pillars:
        rows.append(
            {
                "type": "monthly_pillar_verdict",
                "month": month,
                "pillar_id": pillar.id,
                "verdict": default_pillar_verdict(pillar),
                "evidence_count_this_month": 0,
                "portfolio_action_required": portfolio_action_required,
                "notes": "scaffold entries only",
            }
        )
    return "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"


def create_monthly_report(root: Path, month: str, force: bool = False) -> Path:
    month = validate_month(month)
    path = root / "reports" / f"{month}-monthly.jsonl"
    if path.exists() and not force:
        raise ArtifactError(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_monthly_report_jsonl(month, active_pillars(root)),
        encoding="utf-8",
    )
    return path
