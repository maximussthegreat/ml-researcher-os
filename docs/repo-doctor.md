# ML Repo Doctor

`mlro doctor` is a fast reproducibility scan for ML repositories. It gives a stranger-facing score and tells contributors which missing artifact would raise confidence the most.

## Run it

```bash
mlro doctor .
mlro doctor ../some-ml-project --output doctor-report.md
mlro doctor ../some-ml-project --json-output doctor-report.json
mlro doctor . --min-score 80
```

## What it checks

The doctor scores the pieces that usually decide whether an ML claim can be rerun:

| Area | Why it matters |
| --- | --- |
| README | Explains the claim, setup, and run path. |
| Dependencies | Lets a new user install the environment. |
| Train/eval command | Gives a concrete smoke-test entrypoint. |
| Tests and CI | Prevents demos from silently rotting. |
| Configs | Keeps hyperparameters inspectable. |
| Seed policy | Makes variance visible instead of accidental. |
| Data split policy | Reduces leakage and metric confusion. |
| Baselines and ablations | Prevents weak comparison claims. |
| Metrics and artifacts | Keeps results tied to files, not memory. |
| Model and dataset cards | Captures release and provenance context. |
| Failure loop | Turns bad runs into future improvements. |

## How to use the report

Treat the highest-weight failed checks as the next contribution queue. A good issue or PR title should name the failing check directly:

```text
Add seed and split policy for tiny classifier demo
Add CI smoke test for evaluation command
Add baseline section to experiment template
```

The operating rule is simple: do not claim a model improvement until dependency, seed, split, baseline, metric, and artifact checks are green.
