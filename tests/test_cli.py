from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from thesis_pillar_tracker.cli import main


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

