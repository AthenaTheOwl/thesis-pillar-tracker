from __future__ import annotations

import json
from dataclasses import dataclass
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

# Signed weight each verdict applies to a pillar's standing. A positive sum means
# accepted evidence keeps the pillar's constraint binding; a negative sum means the
# evidence is eroding it. NEUTRAL and the scaffold line carry no weight.
VERDICT_WEIGHT = {
    "CONFIRMS": 1,
    "WEAKENS": -1,
    "INVALIDATES": -2,
    "NEUTRAL": 0,
}


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


def default_pillar_verdict(pillar: Pillar) -> str:
    """The pillar's standing-derived verdict: the latest accepted verdict, or NEUTRAL."""
    real = [row for row in parse_evidence(pillar) if row.source != "scaffold"]
    return real[-1].verdict if real else "NEUTRAL"


def month_evidence_count(pillar: Pillar, month: str) -> int:
    return sum(
        1
        for row in parse_evidence(pillar)
        if row.source != "scaffold" and row.date.startswith(month)
    )


def render_monthly_review(month: str, pillars: list[Pillar]) -> str:
    month = validate_month(month)
    if not pillars:
        raise ArtifactError("monthly review requires at least one active pillar")

    ranked = rank_pillars(pillars)
    action_required = any(s.score < 0 for s in ranked)
    pillar_lines = "\n".join(f"  - {pillar.id}" for pillar in pillars)
    verdict_sections = "\n\n".join(
        (
            f"### {s.id}\n"
            f"- Standing: {s.standing} (score {s.score:+d})\n"
            f"- Verdict: {s.latest_verdict}\n"
            f"- Evidence count this month: {month_evidence_count(s.pillar, month)}\n"
            "- Notes: Human reviewer fills this before commit."
        )
        for s in ranked
    )
    weakest = ranked[-1]
    if action_required:
        summary_action = (
            f"- Portfolio action required: true ({weakest.id} is {weakest.standing})."
        )
    else:
        summary_action = "- Portfolio action required: false."
    return (
        "---\n"
        f"month: {month}\n"
        "pillars_reviewed:\n"
        f"{pillar_lines}\n"
        f"portfolio_action_required: {str(action_required).lower()}\n"
        "---\n\n"
        f"# Monthly review - {month}\n\n"
        "## Summary\n\n"
        f"{summary_action}\n"
        "- Scope: all active pillars, ranked by accepted-evidence standing.\n"
        f"- Strongest constraint: {ranked[0].id} (score {ranked[0].score:+d}).\n\n"
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
    ranked = rank_pillars(pillars)
    action_required = portfolio_action_required or any(s.score < 0 for s in ranked)
    rows = []
    for standing in ranked:
        rows.append(
            {
                "type": "monthly_pillar_verdict",
                "month": month,
                "pillar_id": standing.id,
                "verdict": standing.latest_verdict,
                "standing": standing.standing,
                "evidence_score": standing.score,
                "evidence_count_this_month": month_evidence_count(standing.pillar, month),
                "portfolio_action_required": action_required,
                "notes": f"{standing.standing}; {len(standing.real_evidence)} accepted evidence rows",
            }
        )
    return "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"


@dataclass(frozen=True)
class EvidenceRow:
    date: str
    verdict: str
    source: str
    note: str


@dataclass(frozen=True)
class PillarStanding:
    pillar: Pillar
    evidence: list[EvidenceRow]
    score: int
    standing: str
    latest_verdict: str

    @property
    def id(self) -> str:
        return self.pillar.id

    @property
    def title(self) -> str:
        return self.pillar.title

    @property
    def real_evidence(self) -> list[EvidenceRow]:
        """Logged evidence excluding the scaffold placeholder line."""
        return [row for row in self.evidence if row.source != "scaffold"]


def parse_evidence(pillar: Pillar) -> list[EvidenceRow]:
    """Read the dated evidence lines out of a pillar body, oldest first."""
    rows: list[EvidenceRow] = []
    for line in pillar.body.splitlines():
        line = line.strip()
        if not line.startswith("- ") or not EVIDENCE_RE.fullmatch(line):
            continue
        # shape: "- DATE VERDICT [source] - note"
        rest = line[2:]
        date, verdict, rest = rest.split(" ", 2)
        source = rest[rest.index("[") + 1 : rest.index("]")]
        note = rest.split("] - ", 1)[1]
        rows.append(EvidenceRow(date=date, verdict=verdict, source=source, note=note))
    return rows


def classify_standing(score: int, has_invalidating: bool, evidence_count: int) -> str:
    """Map a signed evidence score to a one-word standing for the reviewer."""
    if has_invalidating and score < 0:
        return "invalidated"
    if score < 0:
        return "weakening"
    if score == 0:
        return "untested" if evidence_count == 0 else "contested"
    if score >= 3:
        return "holding-strong"
    return "holding"


def pillar_standing(pillar: Pillar) -> PillarStanding:
    evidence = parse_evidence(pillar)
    real = [row for row in evidence if row.source != "scaffold"]
    score = sum(VERDICT_WEIGHT.get(row.verdict, 0) for row in real)
    has_invalidating = any(row.verdict == "INVALIDATES" for row in real)
    latest_verdict = real[-1].verdict if real else "NEUTRAL"
    return PillarStanding(
        pillar=pillar,
        evidence=evidence,
        score=score,
        standing=classify_standing(score, has_invalidating, len(real)),
        latest_verdict=latest_verdict,
    )


def rank_pillars(pillars: list[Pillar]) -> list[PillarStanding]:
    """Rank pillars by how strongly the accepted evidence still backs the constraint.

    Highest score (constraint best supported) first; ties break on more evidence,
    then pillar id for stability.
    """
    standings = [pillar_standing(pillar) for pillar in pillars]
    standings.sort(key=lambda s: (-s.score, -len(s.real_evidence), s.id))
    return standings


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
