# Improvement Backlog

Generated: 2026-05-23T10:08:22Z

Open failures: 2 / 2

| Priority | Skill | Open failures | Top failure | Suggested action | Tags |
| --- | --- | ---: | --- | --- | --- |
| 33 | result-reporter | 1 | Agent claimed reproduction without matching the original dataset | Tighten result-reporter rules around evidence tags, unsupported claims, and final-answer restraint. | unsupported-claim, overclaiming, reproducibility |
| 22 | experiment-planner | 1 | Experiment plan accepted a claim without a strong baseline policy | Add baseline-selection requirements and examples to experiment-planner. | missing-baseline, weak-baseline |

## Operating rule

Every merged skill change should close or reduce a recorded failure mode.
