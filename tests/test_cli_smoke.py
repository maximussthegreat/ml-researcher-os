from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAILURE_FILE = ROOT / "feedback" / "failures" / "202605230001-unsupported-reproduction-claim.json"


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

    def test_doctor_smoke(self) -> None:
        result = run_cli("doctor", ".")
        self.assertIn("ML Repo Doctor", result.stdout)
        self.assertIn("Score:", result.stdout)
        self.assertIn("Highest-leverage fixes", result.stdout)

    def test_issue_from_failure_smoke(self) -> None:
        result = run_cli("issue-from-failure", "--failure", str(FAILURE_FILE))
        self.assertIn("Failure case:", result.stdout)
        self.assertIn("Acceptance criteria", result.stdout)

    def test_make_regression_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli("make-regression", "--failure", str(FAILURE_FILE), "--output-dir", tmp)
            self.assertIn("Wrote regression task:", result.stdout)
            task_files = list(Path(tmp).glob("*/task.json"))
            self.assertEqual(len(task_files), 1)
            self.assertTrue(task_files[0].with_name("README.md").exists())


if __name__ == "__main__":
    unittest.main()
