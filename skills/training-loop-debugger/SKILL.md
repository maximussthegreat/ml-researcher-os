---
name: training-loop-debugger
description: Use when reviewing ML training code, suspicious metrics, unstable loss, broken evaluation, or a model that appears too good to be true.
---

# Training Loop Debugger

Use this skill to review training and evaluation code before trusting results.

## Review order

1. Data loading
2. Split creation
3. Preprocessing fit and transform
4. Model initialization
5. Loss and optimizer
6. Training mode and eval mode
7. Metric computation
8. Checkpoint selection
9. Test set use
10. Logging and reproducibility

## High-risk bugs

Immediately flag:

- fitting scalers, tokenizers, imputers, or feature selectors on validation or test data
- using test data for early stopping
- computing metrics on logits when probabilities or labels are required
- forgetting `model.eval()` during evaluation
- forgetting `torch.no_grad()` during evaluation
- using different preprocessing at train and eval time
- reporting the best validation run as test performance
- changing seeds until a good result appears

## Required output

| Area | Finding | Severity | Evidence | Fix |
| --- | --- | --- | --- | --- |

Severity must be one of:

- `blocker`
- `high`
- `medium`
- `low`

## Rules

- Do not claim the model is fixed until a rerun is available.
- Do not rewrite the whole project when a small patch explains the issue.
- If logs are missing, ask for logs or mark the conclusion as provisional.

