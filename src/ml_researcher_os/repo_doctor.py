from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "runs",
    "venv",
    "wandb",
}

TEXT_SUFFIXES = {
    ".cfg",
    ".ini",
    ".ipynb",
    ".json",
    ".md",
    ".py",
    ".ps1",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    ok: bool
    weight: int
    detail: str
    recommendation: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "weight": self.weight,
            "detail": self.detail,
            "recommendation": self.recommendation,
        }


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part.lower() in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def read_small_text(path: Path) -> str:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return ""
    try:
        if path.stat().st_size > 500_000:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def contains_any(text: str, needles: list[str]) -> bool:
    lower = text.lower()
    return any(needle.lower() in lower for needle in needles)


def find_named(files: list[Path], root: Path, names: set[str]) -> list[str]:
    return sorted(relative(path, root) for path in files if path.name.lower() in names)


def find_by_suffix(files: list[Path], root: Path, suffixes: set[str]) -> list[str]:
    return sorted(relative(path, root) for path in files if path.suffix.lower() in suffixes)


def find_containing(files: list[Path], root: Path, needles: list[str]) -> list[str]:
    matches: list[str] = []
    for path in files:
        text = read_small_text(path)
        if text and contains_any(text, needles):
            matches.append(relative(path, root))
    return sorted(matches)


def top_paths(paths: list[str], limit: int = 4) -> str:
    if not paths:
        return "missing"
    shown = ", ".join(paths[:limit])
    if len(paths) > limit:
        shown += f", +{len(paths) - limit} more"
    return shown


def check(name: str, ok: bool, weight: int, detail: str, recommendation: str) -> DoctorCheck:
    return DoctorCheck(name=name, ok=ok, weight=weight, detail=detail, recommendation=recommendation)


def doctor_repo(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    if not repo_root.exists():
        raise FileNotFoundError(repo_root)
    if not repo_root.is_dir():
        raise NotADirectoryError(repo_root)

    files = iter_files(repo_root)
    file_names = {path.name.lower() for path in files}
    readmes = find_named(files, repo_root, {"readme.md", "readme.rst", "readme.txt"})
    dependency_files = find_named(
        files,
        repo_root,
        {
            "environment.yml",
            "environment.yaml",
            "pyproject.toml",
            "requirements.txt",
            "setup.cfg",
            "setup.py",
        },
    )
    config_files = [
        relative(path, repo_root)
        for path in files
        if path.suffix.lower() in {".yaml", ".yml", ".toml", ".json"}
        and any(part.lower() in {"config", "configs", "conf"} for part in path.parts)
    ]
    run_entrypoints = [
        relative(path, repo_root)
        for path in files
        if path.suffix.lower() == ".py"
        and any(token in path.stem.lower() for token in ["train", "eval", "evaluate", "infer", "predict", "run"])
    ]
    test_files = [
        relative(path, repo_root)
        for path in files
        if path.suffix.lower() == ".py" and (path.name.lower().startswith("test_") or "tests" in [part.lower() for part in path.parts])
    ]
    workflow_files = [
        relative(path, repo_root)
        for path in files
        if ".github" in [part.lower() for part in path.parts] and "workflows" in [part.lower() for part in path.parts]
    ]
    license_files = find_named(files, repo_root, {"license", "license.md", "license.txt", "copying"})

    readme_text = "\n".join(read_small_text(repo_root / path) for path in readmes)
    command_docs = readmes if contains_any(readme_text, ["pip install", "python ", "make ", "uv ", "conda ", "docker "]) else []
    seed_hits = find_containing(files, repo_root, ["seed", "manual_seed", "random_state", "deterministic"])
    split_hits = find_containing(files, repo_root, ["train_test_split", "validation split", "test split", "data split", "leakage"])
    baseline_hits = find_containing(files, repo_root, ["baseline", "control run", "ablations", "ablation"])
    metric_hits = find_containing(files, repo_root, ["accuracy", "f1", "auc", "loss", "precision", "recall", "rouge", "bleu", "metric"])
    result_files = [
        relative(path, repo_root)
        for path in files
        if any(part.lower() in {"results", "reports", "metrics", "logs"} for part in path.parts)
        or path.name.lower() in {"results.csv", "metrics.json", "eval.json", "report.md"}
    ]
    model_dataset_docs = [
        relative(path, repo_root)
        for path in files
        if path.name.lower() in {"model-card.md", "model_card.md", "dataset-card.md", "dataset_card.md", "datasheet.md"}
        or "model card" in read_small_text(path).lower()
        or "dataset card" in read_small_text(path).lower()
    ]
    failure_loop = [
        relative(path, repo_root)
        for path in files
        if "failure" in path.name.lower()
        or "negative-result" in path.name.lower()
        or "improvement" in path.name.lower()
    ]
    reproducibility_docs = [
        relative(path, repo_root)
        for path in files
        if "reproduc" in path.name.lower()
        or "reproducibility" in read_small_text(path).lower()
    ]

    checks = [
        check(
            "README with project orientation",
            bool(readmes),
            8,
            top_paths(readmes),
            "Add a README that explains what the project does, what claim it tests, and how to start.",
        ),
        check(
            "Dependencies are pinned or declared",
            bool(dependency_files),
            8,
            top_paths(dependency_files),
            "Add pyproject.toml, requirements.txt, or environment.yml so strangers can install the project.",
        ),
        check(
            "Runnable training or evaluation entrypoint",
            bool(run_entrypoints or command_docs),
            10,
            top_paths(run_entrypoints or command_docs),
            "Add a tiny train/eval command and document the exact smoke-test invocation.",
        ),
        check(
            "Tests or smoke checks",
            bool(test_files),
            8,
            top_paths(test_files),
            "Add at least one smoke test that exercises the smallest reproducible path.",
        ),
        check(
            "Continuous integration",
            bool(workflow_files),
            6,
            top_paths(workflow_files),
            "Add a GitHub Actions workflow that runs the smoke test on every push.",
        ),
        check(
            "Configs or hyperparameters are tracked",
            bool(config_files),
            8,
            top_paths(config_files),
            "Put experiment parameters in a config file instead of hiding them in prose.",
        ),
        check(
            "Seed or determinism policy",
            bool(seed_hits),
            8,
            top_paths(seed_hits),
            "Document and set seeds for Python, NumPy, framework code, and data splits.",
        ),
        check(
            "Data split or leakage policy",
            bool(split_hits),
            9,
            top_paths(split_hits),
            "Document train/validation/test split rules and leakage checks.",
        ),
        check(
            "Baseline or ablation policy",
            bool(baseline_hits),
            8,
            top_paths(baseline_hits),
            "Name the baseline, why it is fair, and which ablations are required before claiming improvement.",
        ),
        check(
            "Metrics and result artifacts",
            bool(metric_hits or result_files),
            9,
            top_paths(result_files or metric_hits),
            "Store metrics, logs, and result tables in a predictable location.",
        ),
        check(
            "Model or dataset cards",
            bool(model_dataset_docs),
            6,
            top_paths(model_dataset_docs),
            "Add model-card.md and dataset-card.md for release and data provenance.",
        ),
        check(
            "License",
            bool(license_files),
            4,
            top_paths(license_files),
            "Add an explicit license so people know whether they can use the code.",
        ),
        check(
            "Failure or negative-result loop",
            bool(failure_loop),
            4,
            top_paths(failure_loop),
            "Track failed runs and negative results so future changes are evidence-driven.",
        ),
        check(
            "Reproducibility checklist",
            bool(reproducibility_docs),
            4,
            top_paths(reproducibility_docs),
            "Add a reproducibility checklist that names artifacts required for a rerun.",
        ),
    ]

    earned = sum(item.weight for item in checks if item.ok)
    total = sum(item.weight for item in checks)
    score = round((earned / total) * 100) if total else 0
    failed = [item for item in checks if not item.ok]

    if score >= 85:
        grade = "release-ready"
    elif score >= 70:
        grade = "promising"
    elif score >= 50:
        grade = "fragile"
    else:
        grade = "not reproducible yet"

    return {
        "path": str(repo_root),
        "score": score,
        "grade": grade,
        "checks": [item.as_dict() for item in checks],
        "top_recommendations": [
            {"name": item.name, "weight": item.weight, "recommendation": item.recommendation}
            for item in sorted(failed, key=lambda value: value.weight, reverse=True)[:5]
        ],
    }


def render_doctor_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ML Repo Doctor",
        "",
        f"Path: `{report['path']}`",
        f"Score: **{report['score']}/100**",
        f"Grade: **{report['grade']}**",
        "",
        "## Checks",
        "",
        "| Status | Weight | Check | Evidence |",
        "| --- | ---: | --- | --- |",
    ]
    for item in report["checks"]:
        status = "PASS" if item["ok"] else "FAIL"
        lines.append(f"| {status} | {item['weight']} | {item['name']} | {item['detail']} |")

    lines.extend(["", "## Highest-leverage fixes", ""])
    if report["top_recommendations"]:
        for item in report["top_recommendations"]:
            lines.append(f"- **{item['name']}**: {item['recommendation']}")
    else:
        lines.append("- No critical gaps found. Keep collecting failure cases from real runs.")

    lines.extend(
        [
            "",
            "## Operating rule",
            "",
            "Do not claim a model improvement until the dependency, seed, split, baseline, metric, and artifact checks are green.",
        ]
    )
    return "\n".join(lines) + "\n"
