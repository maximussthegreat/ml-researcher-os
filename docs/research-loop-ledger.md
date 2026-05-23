# Research Loop Ledger

`mlro loop` turns an agentic ML experiment into a small, auditable loop:

1. Pick one metric.
2. Fix the per-run budget.
3. Record every run.
4. Keep runs only when the metric improves.
5. Preserve failed runs as future regression material.

This is intentionally boring infrastructure. Boring is good when a coding agent is allowed to edit research code.

## Quickstart

```bash
mlro loop init . \
  --metric val_loss \
  --direction lower \
  --budget-minutes 5 \
  --goal "Lower validation loss without changing the data split." \
  --command "python train.py"

mlro loop record . \
  --run baseline \
  --value 1.0 \
  --artifact runs/baseline/metrics.json

mlro loop record . \
  --run candidate-dropout-0.2 \
  --value 0.91 \
  --changed-file train.py \
  --artifact runs/dropout-0.2/metrics.json \
  --notes "Added dropout after the encoder block."

mlro loop report .
```

The ledger lives in `.mlro/research-loop.json`. The human report lives in `.mlro/LOOP_REPORT.md`. The agent instructions live in `.mlro/program.md`.

## Why this matters

Agentic research demos become believable when they leave a trail:

- the exact target metric
- the optimization direction
- the fixed budget per run
- the command used
- the changed files
- the artifact paths
- the keep/reject decision

Without this trail, an overnight agent loop is just vibes with a GPU bill.

## Operating rule

Use the loop ledger for optimization decisions. Use `mlro doctor` and the skill pack for scientific claims. A better metric can justify keeping a code change, but it does not justify saying a paper was reproduced.
