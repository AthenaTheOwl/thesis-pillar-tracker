from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, script],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def test_repo_validation_scripts_pass() -> None:
    for script in [
        "scripts/voice_lint.py",
        "scripts/spec_check.py",
        "scripts/validate_pillar_schema.py",
    ]:
        result = run_script(script)
        assert result.returncode == 0, result.stdout + result.stderr

