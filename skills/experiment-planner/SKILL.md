---
name: experiment-planner
description: Use when turning an ML hypothesis, paper claim, or model idea into a reproducible experiment plan with baselines, metrics, seeds, risks, and expected artifacts.
---

# Experiment Planner

Use this skill after claim extraction and before writing training code.

## Goal

Convert a research claim into the smallest controlled experiment that can produce useful evidence.

## Required inputs

- Hypothesis or paper claim
- Dataset or proposed dataset
- Target metric
- Compute budget
- Existing baseline, if any

If any input is missing, ask for it or mark it as `unknown` and make a conservative plan.

## Required output

Write an experiment plan with:

1. Hypothesis
2. Minimum viable experiment
3. Baselines
4. Ablations
5. Data split strategy
6. Metrics
7. Seed policy
8. Failure modes
9. Logging and artifacts
10. Stop criteria

## Baseline rules

Every plan needs at least one baseline. Prefer:

- simplest non-neural baseline
- standard library baseline
- previously reported baseline from the source paper
- ablation of the proposed method

## Failure modes to check

- data leakage
- train/validation split mismatch
- metric mismatch
- hidden preprocessing fit on validation or test data
- seed sensitivity
- tiny test set
- weak baseline
- cherry-picked run
- missing negative result

## Rules

- Do not plan an experiment without at least one meaningful baseline.
- Do not compare a heavily tuned model against an untuned baseline.
- Do not claim reproduction when the dataset, split, or metric differs from the source claim.
- Prefer three small controlled runs over one expensive ambiguous run.

## Output style

Be concrete. Prefer a small experiment that can run today over an impressive plan that cannot be verified.
