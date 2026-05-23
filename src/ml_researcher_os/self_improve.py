from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_SKILL_HEADINGS = [
    "#",
    "## Goal",
    "## Required output",
    "## Rules",
]

REQUIRED_TEMPLATES = [
    "experiment-plan.md",
    "result-report.md",
    "reproducibility-checklist.md",
    "model-card.md",
    "dataset-card.md",
    "negative-result.md",
]

SEVERITY_ORDER = {
    "blocker": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


@dataclass
class AuditResult:
    ok: bool
    score: int
    checks: list[dict[str, Any]]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:64] or "failure"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})


def audit_pack(repo_root: Path) -> AuditResult:
    checks: list[dict[str, Any]] = []

    manifest_path = repo_root / "skills" / "manifest.json"
    add_check(checks, "skills manifest exists", manifest_path.exists(), str(manifest_path))

    skills: list[dict[str, Any]] = []
    if manifest_path.exists():
        try:
            manifest = read_json(manifest_path)
            skills = list(manifest.get("skills", []))
            add_check(checks, "skills manifest parses", True, f"{len(skills)} skills")
        except Exception as exc:  # pragma: no cover - defensive path
            add_check(checks, "skills manifest parses", False, str(exc))

    skill_names = set()
    for skill in skills:
        name = str(skill.get("name", "")).strip()
        path = repo_root / "skills" / str(skill.get("path", ""))
        skill_names.add(name)
        add_check(checks, f"skill exists: {name}", path.exists(), str(path))
        if path.exists():
            text = path.read_text(encoding="utf-8")
            has_goal_or_equivalent = "## Goal" in text or "## Required inputs" in text or "## Audit checklist" in text
            add_check(checks, f"skill has purpose section: {name}", has_goal_or_equivalent, "Goal, Required inputs, or Audit checklist")
            add_check(checks, f"skill has rules: {name}", "## Rules" in text or "## Reporting rules" in text or "## Card rules" in text, "Rules section")
            add_check(checks, f"skill has required output: {name}", "## Required output" in text or "## Required sections" in text, "Required output section")

    for template in REQUIRED_TEMPLATES:
        add_check(checks, f"template exists: {template}", (repo_root / "templates" / template).exists(), template)

    demo = repo_root / "examples" / "tiny-paper-replication"
    for demo_file in ["README.md", "paper.md", "agent-output-with-skill.md", "experiment-plan.md"]:
        add_check(checks, f"demo file exists: {demo_file}", (demo / demo_file).exists(), demo_file)

    add_check(checks, "failure issue template exists", (repo_root / ".github" / "ISSUE_TEMPLATE" / "failure_case.md").exists(), "failure_case.md")
    add_check(checks, "self improvement docs exist", (repo_root / "docs" / "self-improvement-loop.md").exists(), "docs/self-improvement-loop.md")

    passed = sum(1 for check in checks if check["ok"])
    score = round((passed / len(checks)) * 100) if checks else 0
    return AuditResult(ok=all(check["ok"] for check in checks), score=score, checks=checks)


def record_failure(
    repo_root: Path,
    title: str,
    observed: str,
    expected: str,
    skill: str,
    severity: str,
    tags: list[str],
    evidence: str,
) -> Path:
    severity = severity.lower()
    if severity not in SEVERITY_ORDER:
        raise ValueError(f"severity must be one of: {', '.join(SEVERITY_ORDER)}")

    failure_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{slugify(title)}"
    payload = {
        "id": failure_id,
        "title": title,
        "status": "open",
        "severity": severity,
        "skill": skill,
        "tags": tags,
        "observed_behavior": observed,
        "expected_behavior": expected,
        "evidence": evidence,
        "created_utc": utc_now(),
        "proposal": {
            "hypothesis": "A skill, template, or example is underspecified for this failure mode.",
            "next_action": "Reproduce the failure, patch the narrowest relevant skill, and add a benchmark or example.",
        },
    }
    path = repo_root / "feedback" / "failures" / f"{failure_id}.json"
    write_json(path, payload)
    return path


def load_failures(repo_root: Path, failures_dir: Path | None = None) -> list[dict[str, Any]]:
    root = failures_dir or (repo_root / "feedback" / "failures")
    failures = []
    if not root.exists():
        return failures
    for path in sorted(root.glob("*.json")):
        item = read_json(path)
        item["_path"] = str(path)
        failures.append(item)
    return failures


def priority_for(failure: dict[str, Any]) -> int:
    severity = str(failure.get("severity", "low")).lower()
    tag_bonus = len(failure.get("tags", []))
    return SEVERITY_ORDER.get(severity, 1) * 10 + tag_bonus


def improvement_backlog(repo_root: Path, failures_dir: Path | None = None) -> dict[str, Any]:
    failures = load_failures(repo_root, failures_dir)
    open_failures = [item for item in failures if item.get("status", "open") == "open"]

    by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for failure in open_failures:
        by_skill[str(failure.get("skill", "unknown"))].append(failure)

    items = []
    for skill, skill_failures in by_skill.items():
        skill_failures = sorted(skill_failures, key=priority_for, reverse=True)
        top = skill_failures[0]
        tags = Counter(tag for failure in skill_failures for tag in failure.get("tags", []))
        items.append(
            {
                "skill": skill,
                "priority": priority_for(top),
                "open_failures": len(skill_failures),
                "top_failure": top.get("title", ""),
                "suggested_action": suggest_action(skill, skill_failures, tags),
                "top_tags": [tag for tag, _ in tags.most_common(5)],
            }
        )

    items.sort(key=lambda item: item["priority"], reverse=True)
    return {
        "generated_utc": utc_now(),
        "total_failures": len(failures),
        "open_failures": len(open_failures),
        "items": items,
    }


def suggest_action(skill: str, failures: list[dict[str, Any]], tags: Counter[str]) -> str:
    common_tags = {tag for tag, _ in tags.most_common(3)}
    if "unsupported-claim" in common_tags or "overclaiming" in common_tags:
        return f"Tighten {skill} rules around evidence tags, unsupported claims, and final-answer restraint."
    if "missing-baseline" in common_tags or "weak-baseline" in common_tags:
        return f"Add baseline-selection requirements and examples to {skill}."
    if "data-leakage" in common_tags:
        return f"Add a leakage-specific checklist and failing example to {skill}."
    if "missing-artifact" in common_tags or "reproducibility" in common_tags:
        return f"Require concrete artifacts, logs, configs, and rerun commands in {skill}."
    return f"Patch {skill} with a narrower rule and add one regression example for: {failures[0].get('title', '')}."


def render_backlog(report: dict[str, Any]) -> str:
    lines = [
        "# Improvement Backlog",
        "",
        f"Generated: {report['generated_utc']}",
        "",
        f"Open failures: {report['open_failures']} / {report['total_failures']}",
        "",
        "| Priority | Skill | Open failures | Top failure | Suggested action | Tags |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for item in report["items"]:
        tags = ", ".join(item["top_tags"]) if item["top_tags"] else "-"
        lines.append(
            f"| {item['priority']} | {item['skill']} | {item['open_failures']} | "
            f"{item['top_failure']} | {item['suggested_action']} | {tags} |"
        )
    if not report["items"]:
        lines.append("| - | - | 0 | No open failures | Keep collecting evidence from real runs. | - |")
    lines.extend(
        [
            "",
            "## Operating rule",
            "",
            "Every merged skill change should close or reduce a recorded failure mode.",
        ]
    )
    return "\n".join(lines) + "\n"

