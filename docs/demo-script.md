# Demo Script

This is the launch GIF/storyboard for `ml-researcher-os`.

## Demo title

From paper claim to reproducible experiment plan in under two minutes.

## Terminal storyboard

```bash
gh skill install maximussthegreat/ml-researcher-os
mlro init --stack pytorch --agent codex --target paper-to-experiment
mlro ingest paper.pdf
mlro plan --budget "1 GPU hour" --output experiments/plan.md
mlro report --from runs/demo --format markdown
```

## Visual beats

1. Show a paper claim.
2. Agent extracts hypothesis, dataset, metric, and assumptions.
3. Agent proposes baselines and ablations.
4. Agent flags two failure risks.
5. Agent creates a runnable experiment folder.
6. Final output shows a result table and limitations section.

## Launch rule

The demo must show at least one limitation or uncertainty. That is the trust signal.

