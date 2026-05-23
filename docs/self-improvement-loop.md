# Self-Improvement Loop

`ml-researcher-os` is designed to improve from observed failures, not from vibes.

The loop is:

1. Use a skill on a real ML research task.
2. Record where the agent failed.
3. Turn failures into a prioritized improvement backlog.
4. Patch the narrowest relevant skill, template, or example.
5. Add a regression example or benchmark task.
6. Re-run the audit before release.

## Commands

Audit the repository:

```bash
mlro audit
```

Score any ML project for reproducibility readiness:

```bash
mlro doctor ../some-ml-project --output doctor-report.md
```

Record a failure:

```bash
mlro record-failure \
  --title "Agent claimed reproduction without matching dataset" \
  --skill result-reporter \
  --severity high \
  --tag unsupported-claim \
  --tag reproducibility \
  --observed "The agent wrote that the paper was reproduced." \
  --expected "The agent should say this is only a stand-in experiment." \
  --evidence "Report paragraph 3"
```

Generate the backlog:

```bash
mlro improve \
  --output feedback/IMPROVEMENT_BACKLOG.md \
  --json-output feedback/improvement-report.json
```

Turn a failure into a GitHub issue draft:

```bash
mlro issue-from-failure \
  --failure feedback/failures/202605230001-unsupported-reproduction-claim.json \
  --output issue.md
```

Turn a failure into a regression task:

```bash
mlro make-regression \
  --failure feedback/failures/202605230001-unsupported-reproduction-claim.json \
  --output-dir benchmarks/regressions
```

Run a fixed-budget experiment loop:

```bash
mlro loop init . \
  --metric val_loss \
  --direction lower \
  --budget-minutes 5 \
  --command "python train.py"

mlro loop record . --run baseline --value 1.0
mlro loop record . --run candidate --value 0.91 --changed-file train.py
mlro loop report .
```

## Failure taxonomy

Use short tags so patterns become visible:

| Tag | Meaning |
| --- | --- |
| `unsupported-claim` | The agent claimed more than evidence supports. |
| `overclaiming` | The agent used stronger language than the result allows. |
| `missing-baseline` | The plan or report lacks a meaningful baseline. |
| `weak-baseline` | The baseline is too weak for the claim. |
| `data-leakage` | Data split, preprocessing, or evaluation leakage. |
| `metric-mismatch` | The metric does not match the source claim. |
| `missing-artifact` | Logs, configs, or outputs are absent. |
| `reproducibility` | A stranger cannot rerun the work. |

## Merge rule

Every meaningful skill change should be tied to one of:

- a recorded failure
- a benchmark task
- a reproducibility audit finding
- a user report that can be turned into one of the above

That keeps the project from becoming a prompt museum.
