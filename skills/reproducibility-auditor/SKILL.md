---
name: reproducibility-auditor
description: Use when auditing an ML repository, experiment folder, model release, or paper reproduction for missing files, hidden assumptions, and rerun readiness.
---

# Reproducibility Auditor

Use this skill before publishing results, releasing a model, or asking others to reproduce a run.

## Audit checklist

Check for:

- environment file
- dependency versions
- dataset source and license
- split creation code
- preprocessing code
- seed policy
- training config
- evaluation config
- logs
- checkpoints
- result table
- model card or report
- known limitations

## Required output

| Item | Status | Evidence | Required fix |
| --- | --- | --- | --- |

Status must be one of:

- `present`
- `missing`
- `unclear`
- `not_applicable`

## Reproducibility grade

End with:

```text
Grade: A/B/C/D/F
Can a stranger rerun this? yes/no/partial
Smallest next fix: ...
```

## Rules

- Prefer one small fix that unlocks reruns over a large refactor.
- Do not accept screenshots as a substitute for logs.
- Do not accept "works on my machine" as evidence.

