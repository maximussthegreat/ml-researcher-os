from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOOP_DIR = ".mlro"
LEDGER_NAME = "research-loop.json"
REPORT_NAME = "LOOP_REPORT.md"
PROGRAM_NAME = "program.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:48] or "run"


def loop_dir(workspace: Path) -> Path:
    return workspace.resolve() / LOOP_DIR


def ledger_path(workspace: Path) -> Path:
    return loop_dir(workspace) / LEDGER_NAME


def report_path(workspace: Path) -> Path:
    return loop_dir(workspace) / REPORT_NAME


def program_path(workspace: Path) -> Path:
    return loop_dir(workspace) / PROGRAM_NAME


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def init_loop(
    workspace: Path,
    metric: str,
    direction: str,
    budget_minutes: float,
    goal: str,
    command: str,
    force: bool = False,
) -> dict[str, Any]:
    workspace = workspace.resolve()
    target = ledger_path(workspace)
    if target.exists() and not force:
        raise FileExistsError(target)

    state = {
        "version": 1,
        "created_utc": utc_now(),
        "updated_utc": utc_now(),
        "workspace": str(workspace),
        "goal": goal,
        "metric": {
            "name": metric,
            "direction": direction,
        },
        "budget": {
            "minutes_per_run": budget_minutes,
        },
        "default_command": command,
        "runs": [],
    }
    write_loop(workspace, state)
    program_path(workspace).write_text(render_program(state), encoding="utf-8")
    report_path(workspace).write_text(render_report(state), encoding="utf-8")
    return state


def load_loop(workspace: Path) -> dict[str, Any]:
    path = ledger_path(workspace)
    if not path.exists():
        raise FileNotFoundError(f"No loop ledger found at {path}. Run `mlro loop init` first.")
    return read_json(path)


def write_loop(workspace: Path, state: dict[str, Any]) -> None:
    state["updated_utc"] = utc_now()
    write_json(ledger_path(workspace), state)


def completed_runs(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [run for run in state.get("runs", []) if run.get("status") == "completed" and "metric_value" in run]


def best_run(state: dict[str, Any]) -> dict[str, Any] | None:
    runs = completed_runs(state)
    if not runs:
        return None
    reverse = state.get("metric", {}).get("direction") == "higher"
    return sorted(runs, key=lambda run: float(run["metric_value"]), reverse=reverse)[0]


def compare_values(direction: str, candidate: float, current: float) -> tuple[bool, float, float]:
    if direction == "higher":
        delta = candidate - current
        percent = (delta / abs(current)) * 100 if current else 0.0
        return candidate > current, delta, percent
    delta = current - candidate
    percent = (delta / abs(current)) * 100 if current else 0.0
    return candidate < current, delta, percent


def record_run(
    workspace: Path,
    name: str,
    metric_value: float,
    status: str,
    command: str | None,
    notes: str,
    artifacts: list[str],
    changed_files: list[str],
) -> dict[str, Any]:
    workspace = workspace.resolve()
    state = load_loop(workspace)
    previous_best = best_run(state)
    direction = state.get("metric", {}).get("direction", "lower")

    decision = "review"
    delta = None
    delta_percent = None
    reason = "Run was not marked completed."

    if status == "completed":
        if previous_best is None:
            decision = "accept"
            reason = "First completed run becomes the baseline."
        else:
            improved, delta, delta_percent = compare_values(direction, metric_value, float(previous_best["metric_value"]))
            if improved:
                decision = "accept"
                reason = f"Improved {state['metric']['name']} vs {previous_best['id']}."
            else:
                decision = "reject"
                reason = f"Did not improve {state['metric']['name']} vs {previous_best['id']}."

    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}-{slugify(name)}"
    run = {
        "id": run_id,
        "name": name,
        "created_utc": utc_now(),
        "status": status,
        "metric_value": metric_value,
        "decision": decision,
        "decision_reason": reason,
        "command": command or state.get("default_command", "not specified"),
        "notes": notes,
        "artifacts": artifacts,
        "changed_files": changed_files,
    }
    if delta is not None:
        run["delta_from_previous_best"] = round(delta, 8)
        run["delta_percent_from_previous_best"] = round(delta_percent or 0.0, 4)

    state.setdefault("runs", []).append(run)
    write_loop(workspace, state)
    report_path(workspace).write_text(render_report(state), encoding="utf-8")
    return run


def render_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def render_report(state: dict[str, Any]) -> str:
    metric = state.get("metric", {})
    budget = state.get("budget", {})
    best = best_run(state)
    lines = [
        "# Research Loop Report",
        "",
        f"Goal: {state.get('goal', 'not specified')}",
        f"Metric: `{metric.get('name', 'metric')}` ({metric.get('direction', 'lower')} is better)",
        f"Budget: {budget.get('minutes_per_run', 'not specified')} minutes per run",
        f"Updated: {state.get('updated_utc', 'unknown')}",
        "",
        "## Best run",
        "",
    ]
    if best:
        lines.append(f"`{best['id']}` with `{metric.get('name', 'metric')}={render_value(best['metric_value'])}`")
    else:
        lines.append("No completed runs yet.")

    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| Decision | Run | Status | Metric | Delta | Command | Notes |",
            "| --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for run in state.get("runs", []):
        delta = run.get("delta_from_previous_best", "-")
        lines.append(
            f"| {str(run.get('decision', 'review')).upper()} | {run.get('id', '-')} | "
            f"{run.get('status', '-')} | {render_value(run.get('metric_value', '-'))} | "
            f"{delta} | `{run.get('command', '-')}` | {run.get('notes', '') or '-'} |"
        )

    if not state.get("runs"):
        lines.append("| - | - | - | - | - | - | No runs recorded yet. |")

    lines.extend(
        [
            "",
            "## Loop rules",
            "",
            "- Change one meaningful thing per run.",
            "- Keep the run only when the target metric improves under the same budget.",
            "- Record failed runs; they are future regression tests.",
            "- Do not claim scientific progress from a metric-only improvement without checking split, seed, baseline, and artifacts.",
            "",
        ]
    )
    return "\n".join(lines)


def render_program(state: dict[str, Any]) -> str:
    metric = state.get("metric", {})
    budget = state.get("budget", {})
    return "\n".join(
        [
            "# Agent Research Program",
            "",
            f"Goal: {state.get('goal', 'not specified')}",
            "",
            "## Objective",
            "",
            f"Improve `{metric.get('name', 'metric')}`. Direction: `{metric.get('direction', 'lower')}` is better.",
            f"Each experiment has a fixed budget of `{budget.get('minutes_per_run', 'not specified')}` minutes.",
            "",
            "## Command",
            "",
            f"Default command: `{state.get('default_command', 'not specified')}`",
            "",
            "## Required loop",
            "",
            "1. Inspect the current best run in `.mlro/research-loop.json`.",
            "2. Propose one small change with a clear hypothesis.",
            "3. Run the default command under the fixed budget.",
            "4. Record the result with `mlro loop record`.",
            "5. Keep accepted changes and revert rejected changes unless the failure teaches a needed regression.",
            "",
            "## Reporting rule",
            "",
            "Separate observation, inference, and speculation. A better metric is not a paper claim until reproducibility checks pass.",
            "",
        ]
    )
