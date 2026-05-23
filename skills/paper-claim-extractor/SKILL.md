---
name: paper-claim-extractor
description: Use when reading an ML paper, abstract, README, or result section and the task is to extract claims, assumptions, experiments, limitations, or implementation requirements.
---

# Paper Claim Extractor

Use this skill before implementing, reproducing, or summarizing an ML paper.

## Goal

Convert paper text into a structured research brief that makes the agent slow down before coding.

## Required output

Produce these sections:

1. `Core claim`
2. `Evidence table`
3. `Assumptions`
4. `Datasets and splits`
5. `Metrics`
6. `Baselines`
7. `Ablations`
8. `Implementation requirements`
9. `Limitations`
10. `Questions before reproduction`

## Evidence table format

| Claim | Evidence in text | Evidence type | Confidence | Reproduction note |
| --- | --- | --- | --- | --- |

Evidence type must be one of:

- `reported_result`
- `method_description`
- `ablation`
- `theory`
- `author_claim`
- `missing`

Confidence must be one of:

- `high`
- `medium`
- `low`

## Rules

- Do not treat the paper's conclusion as ground truth.
- Do not invent datasets, hyperparameters, or baselines.
- If a detail is missing, write `not specified`.
- Separate what the paper reports from what you infer.
- Flag any claim that depends on a single dataset, a weak baseline, or missing ablations.

## Final check

End with:

```text
Ready to plan experiments: yes/no
Blocking missing details:
- ...
```

