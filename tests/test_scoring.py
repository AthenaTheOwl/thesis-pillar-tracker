from __future__ import annotations

from pathlib import Path

import pytest

from thesis_pillar_tracker.model import (
    ArtifactError,
    clean_single_line,
    load_pillars,
    validate_pillar_id,
)
from thesis_pillar_tracker.scoring import (
    month_evidence_count,
    pillar_standing,
)
from thesis_pillar_tracker.cli import main


def _new_pillar(tmp_path: Path, pillar_id: str) -> None:
    assert (
        main(
            [
                "new-pillar",
                "--root",
                str(tmp_path),
                "--id",
                pillar_id,
                "--title",
                f"Title for {pillar_id}",
                "--claim",
                f"{pillar_id} claim stays binding",
                "--falsification",
                f"{pillar_id} falsifier",
                "--created",
                "2026-06-01",
            ]
        )
        == 0
    )


def _log(tmp_path: Path, pillar_id: str, verdict: str, date: str) -> None:
    assert (
        main(
            [
                "log-evidence",
                "--root",
                str(tmp_path),
                "--pillar",
                pillar_id,
                "--source",
                "accepted public event",
                "--verdict",
                verdict,
                "--note",
                "reviewer-approved evidence note",
                "--date",
                date,
            ]
        )
        == 0
    )


def _standing_of(tmp_path: Path, pillar_id: str):
    by_id = {p.id: p for p in load_pillars(tmp_path)}
    return pillar_standing(by_id[pillar_id])


def test_three_net_confirms_is_holding_strong(tmp_path: Path) -> None:
    # Pins the score>=3 branch of classify_standing.
    _new_pillar(tmp_path, "strong-pillar")
    _log(tmp_path, "strong-pillar", "CONFIRMS", "2026-06-05")
    _log(tmp_path, "strong-pillar", "CONFIRMS", "2026-06-10")
    _log(tmp_path, "strong-pillar", "CONFIRMS", "2026-06-15")

    standing = _standing_of(tmp_path, "strong-pillar")
    assert standing.score == 3
    assert standing.standing == "holding-strong"


def test_weakens_only_negative_pillar_is_weakening(tmp_path: Path) -> None:
    # Pins the score<0-without-INVALIDATES branch of classify_standing.
    _new_pillar(tmp_path, "weak-pillar")
    _log(tmp_path, "weak-pillar", "WEAKENS", "2026-06-05")
    _log(tmp_path, "weak-pillar", "WEAKENS", "2026-06-10")

    standing = _standing_of(tmp_path, "weak-pillar")
    assert standing.score == -2
    assert standing.standing == "weakening"


def test_month_evidence_count_filters_by_month(tmp_path: Path) -> None:
    # Pins the row.date.startswith(month) date filter: two June rows, one May row.
    _new_pillar(tmp_path, "dated-pillar")
    _log(tmp_path, "dated-pillar", "CONFIRMS", "2026-05-20")
    _log(tmp_path, "dated-pillar", "CONFIRMS", "2026-06-10")
    _log(tmp_path, "dated-pillar", "WEAKENS", "2026-06-25")

    pillar = {p.id: p for p in load_pillars(tmp_path)}["dated-pillar"]
    assert month_evidence_count(pillar, "2026-06") == 2
    assert month_evidence_count(pillar, "2026-05") == 1


def test_clean_single_line_rejects_blank() -> None:
    # Pins the empty-string guard in clean_single_line.
    with pytest.raises(ArtifactError):
        clean_single_line("   ", "title")


@pytest.mark.parametrize("bad_id", ["Bad ID", "with/slash", "UPPER"])
def test_validate_pillar_id_rejects_malformed(bad_id: str) -> None:
    # Pins the PILLAR_ID_RE guard in validate_pillar_id.
    with pytest.raises(ArtifactError):
        validate_pillar_id(bad_id)
