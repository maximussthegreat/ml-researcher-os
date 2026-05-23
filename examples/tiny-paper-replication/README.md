# Tiny Paper Replication Demo

This example is a launch storyboard for `ml-researcher-os`.

It shows the intended flow:

1. Read a small paper-style claim.
2. Extract assumptions and missing details.
3. Build a controlled experiment plan.
4. Report what can and cannot be claimed.

## Files

- [paper.md](paper.md): a short fake paper excerpt.
- [agent-output-with-skill.md](agent-output-with-skill.md): expected output after using the skills.
- [experiment-plan.md](experiment-plan.md): a concrete plan generated from the claim.
- [configs/smoke.json](configs/smoke.json): seed, split, baseline, and metric policy for the demo.

## Why the paper is fake

The demo uses a synthetic excerpt so the repository can show the workflow without depending on an external paper, license, or dataset.

The first real release should add one small public dataset example.
