from __future__ import annotations

import subprocess
import sys
import unittest
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


class CliSmokeTests(unittest.TestCase):
    def test_list_skills_smoke(self) -> None:
        result = run_cli("list-skills")
        self.assertIn("paper-claim-extractor", result.stdout)
        self.assertIn("experiment-planner", result.stdout)

    def test_extract_claims_smoke(self) -> None:
        result = run_cli("extract-claims", "examples/tiny-paper-replication/paper.md")
        self.assertIn("Core claim", result.stdout)
        self.assertIn("TinyDense", result.stdout)

    def test_audit_smoke(self) -> None:
        result = run_cli("audit")
        self.assertIn("Self-audit score", result.stdout)
        self.assertIn("PASS skills manifest exists", result.stdout)

    def test_improve_smoke(self) -> None:
        result = run_cli("improve")
        self.assertIn("Improvement Backlog", result.stdout)
        self.assertIn("result-reporter", result.stdout)


if __name__ == "__main__":
    unittest.main()
