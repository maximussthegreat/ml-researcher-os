from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "src" / "ml_researcher_os" / "cli.py"), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_list_skills_smoke() -> None:
    result = run_cli("list-skills")
    assert "paper-claim-extractor" in result.stdout
    assert "experiment-planner" in result.stdout


def test_extract_claims_smoke() -> None:
    result = run_cli("extract-claims", "examples/tiny-paper-replication/paper.md")
    assert "Core claim" in result.stdout
    assert "TinyDense" in result.stdout

