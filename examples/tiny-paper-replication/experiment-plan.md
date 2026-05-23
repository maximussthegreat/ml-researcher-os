# Experiment Plan

## Hypothesis

A compact transformer classifier improves macro F1 over a logistic regression baseline on short text classification when train/test splits are clean and preprocessing is matched.

## Minimum viable experiment

Use a public short-text classification dataset as a stand-in, run logistic regression and a compact transformer under the same split, and report macro F1 across three seeds.

## Baselines

| Baseline | Reason | Expected strength |
| --- | --- | --- |
| Majority class | Sanity check | Weak |
| TF-IDF + logistic regression | Matches paper baseline style | Medium |
| Compact transformer | Proposed method | Medium to strong |

## Ablations

| Ablation | What it tests | Required? |
| --- | --- | --- |
| Mean pooling vs CLS pooling | Whether pooling choice drives result | Yes |
| One seed vs three seeds | Seed sensitivity | Yes |
| Short notes only vs mixed length | Robustness to length | Optional |

## Failure modes

- validation leakage through preprocessing
- comparing tuned transformer against untuned baseline
- reporting best validation as test performance
- claiming reproduction of the private dataset result

## Claim support

The experiment can support a weaker claim: whether the idea works on a public stand-in task. It cannot support the original private-dataset claim.

