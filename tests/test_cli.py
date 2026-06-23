from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from thesis_pillar_tracker.cli import main
from thesis_pillar_tracker.model import load_pillars
from thesis_pillar_tracker.scoring import rank_pillars


def test_help_lists_v01_subcommands() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "thesis_pillar_tracker.cli", "--help"],
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert "new-pillar" in result.stdout
    assert "log-evidence" in result.stdout
    assert "monthly-review" in result.stdout
    assert "quarterly-snapshot" in result.stdout
    assert "show" in result.stdout


def test_new_pillar_and_log_evidence(tmp_path: Path) -> None:
    result = main(
        [
            "new-pillar",
            "--root",
            str(tmp_path),
            "--id",
            "sample-pillar",
            "--title",
            "Sample pillar",
            "--claim",
            "A sample claim remains testable",
            "--falsification",
            "A named public event contradicts the sample claim",
            "--created",
            "2026-06-21",
        ]
    )
    assert result == 0

    result = main(
        [
            "log-evidence",
            "--root",
            str(tmp_path),
            "--pillar",
            "sample-pillar",
            "--source",
            "unit test",
            "--verdict",
            "WEAKENS",
            "--note",
            "sample evidence line appended",
            "--date",
            "2026-06-22",
        ]
    )
    assert result == 0
    text = (tmp_path / "thesis" / "sample-pillar.md").read_text(encoding="utf-8")
    assert "2026-06-22 WEAKENS [unit test] - sample evidence line appended" in text


def test_monthly_review_references_all_active_pillars(tmp_path: Path) -> None:
    for index in range(6):
        result = main(
            [
                "new-pillar",
                "--root",
                str(tmp_path),
                "--id",
                f"pillar-{index}",
                "--title",
                f"Pillar {index}",
                "--claim",
                f"Claim {index} remains falsifiable",
                "--falsification",
                f"Falsification condition {index}",
                "--created",
                "2026-06-21",
            ]
        )
        assert result == 0

    result = main(["monthly-review", "--root", str(tmp_path), "--month", "2026-06"])
    assert result == 0
    text = (tmp_path / "monthly_reviews" / "2026-06.md").read_text(encoding="utf-8")
    for index in range(6):
        assert f"  - pillar-{index}" in text


def _seed_three_pillars(tmp_path: Path) -> None:
    specs = [
        ("alpha-pillar", "Alpha", "Alpha claim stays binding", "Alpha falsifier"),
        ("beta-pillar", "Beta", "Beta claim stays binding", "Beta falsifier"),
        ("gamma-pillar", "Gamma", "Gamma claim stays binding", "Gamma falsifier"),
    ]
    for pid, title, claim, fals in specs:
        assert (
            main(
                [
                    "new-pillar",
                    "--root",
                    str(tmp_path),
                    "--id",
                    pid,
                    "--title",
                    title,
                    "--claim",
                    claim,
                    "--falsification",
                    fals,
                    "--created",
                    "2026-06-01",
                ]
            )
            == 0
        )

    def log(pillar: str, verdict: str, date: str) -> None:
        assert (
            main(
                [
                    "log-evidence",
                    "--root",
                    str(tmp_path),
                    "--pillar",
                    pillar,
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

    # alpha: net +2 (holding), beta: net 0 (contested), gamma: invalidated (-2)
    log("alpha-pillar", "CONFIRMS", "2026-06-10")
    log("alpha-pillar", "CONFIRMS", "2026-06-15")
    log("beta-pillar", "CONFIRMS", "2026-06-10")
    log("beta-pillar", "WEAKENS", "2026-06-15")
    log("gamma-pillar", "INVALIDATES", "2026-06-12")


def test_rank_pillars_orders_by_evidence_score(tmp_path: Path) -> None:
    _seed_three_pillars(tmp_path)
    standings = rank_pillars(load_pillars(tmp_path))
    assert [s.id for s in standings] == [
        "alpha-pillar",
        "beta-pillar",
        "gamma-pillar",
    ]
    by_id = {s.id: s for s in standings}
    assert by_id["alpha-pillar"].score == 2
    assert by_id["alpha-pillar"].standing == "holding"
    assert by_id["beta-pillar"].score == 0
    assert by_id["beta-pillar"].standing == "contested"
    assert by_id["gamma-pillar"].score == -2
    assert by_id["gamma-pillar"].standing == "invalidated"


def test_show_prints_ranked_readable_standing(tmp_path: Path, capsys) -> None:
    _seed_three_pillars(tmp_path)
    assert main(["show", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "thesis pillar standing" in out
    assert "strongest constraint: alpha-pillar" in out
    # the invalidated pillar must surface in the watch line
    assert "watch: gamma-pillar" in out
    # ranking order: alpha appears before gamma in the table body
    assert out.index("alpha-pillar") < out.index("gamma-pillar")


def test_show_on_committed_repo_runs_offline() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "thesis_pillar_tracker.cli", "show", "--root", str(repo_root)],
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert "thesis pillar standing" in result.stdout
    assert "strongest constraint:" in result.stdout


def test_quarterly_snapshot_refuses_overwrite_without_force(tmp_path: Path) -> None:
    args = [
        "quarterly-snapshot",
        "--root",
        str(tmp_path),
        "--quarter",
        "2026Q2",
        "--binding-constraint",
        "advanced packaging capacity",
        "--delta",
        "initial snapshot",
    ]
    assert main(args) == 0
    assert main(args) == 2
    assert main([*args, "--force"]) == 0

