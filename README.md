# ml-researcher-os

> Turn your coding agent into a disciplined ML research collaborator.

`ml-researcher-os` is a skill and workflow pack for developers who use AI coding agents to read papers, design experiments, train models, debug failures, and write research reports.

The goal is not to make an agent sound smart. The goal is to make it behave like a careful junior researcher: skeptical, reproducible, explicit about assumptions, and allergic to fake results.

## The 30-second demo

```bash
# install path, after the repo is published as a package or cloned locally
gh skill install maximussthegreat/ml-researcher-os

# local setup
python -m pip install -e .
mlro list-skills
mlro init ./research-workspace
mlro extract-claims examples/tiny-paper-replication/paper.md
mlro audit
mlro improve
```

Before:

```text
"I implemented the model from the paper."
```

After:

```text
Hypothesis: the reported gain may depend on sequence length.
Experiment: 3 seeds x 2 baselines x 2 sequence lengths.
Risks: dataset leakage, metric mismatch, weak baseline.
Output: config, training logs, result table, failure notes, report draft.
```

## Why this exists

AI agents can write a lot of code, but ML research fails in quieter places:

- the paper claim was misunderstood
- the baseline is too weak
- the dataset split is leaky
- the metric is not comparable
- the agent reports success without checking logs
- the final writeup hides negative results

`ml-researcher-os` gives agents a repeatable research protocol instead of a vague prompt.

## What will ship first

This repo now includes first drafts of:

- [paper-claim-extractor](skills/paper-claim-extractor/SKILL.md): extract claims, assumptions, datasets, metrics, and ablations.
- [experiment-planner](skills/experiment-planner/SKILL.md): convert claims into controlled tests.
- [training-loop-debugger](skills/training-loop-debugger/SKILL.md): catch common training and evaluation mistakes.
- [result-reporter](skills/result-reporter/SKILL.md): write tables, limitations, and negative results.
- [reproducibility-auditor](skills/reproducibility-auditor/SKILL.md): audit rerun readiness.
- [hf-release-prep](skills/hf-release-prep/SKILL.md): prepare Hugging Face release artifacts.

## Repository layout

```text
skills/                  Agent skill specs and prompt contracts
templates/               Experiment, report, model-card, and dataset-card templates
examples/                Small reproducible research demos
docs/                    Architecture, launch notes, and contribution guides
.github/                 Issues, PR templates, and workflows
```

## Demo example

The first demo storyboard is [examples/tiny-paper-replication](examples/tiny-paper-replication). It uses a synthetic paper excerpt so the workflow can be inspected without external data access.

## Self-improvement system

This repo is built around a failure-driven improvement loop:

```bash
mlro record-failure \
  --title "Agent overclaimed a result" \
  --skill result-reporter \
  --severity high \
  --tag unsupported-claim \
  --observed "The agent claimed reproduction from a stand-in dataset." \
  --expected "The agent should say the claim is only partially supported."

mlro improve --output feedback/IMPROVEMENT_BACKLOG.md
mlro audit
```

See [docs/self-improvement-loop.md](docs/self-improvement-loop.md).

## Design principles

1. Reproducibility beats speed.
2. Every claim needs evidence or a caveat.
3. Negative results are first-class outputs.
4. The agent must separate observation, inference, and speculation.
5. Small examples should run on normal developer hardware.
6. Every skill change should close or reduce a recorded failure mode.

## What this is not

- Not an autonomous scientist.
- Not a replacement for domain expertise.
- Not a benchmark leaderboard for inflated claims.
- Not a wrapper around one proprietary model.
- Not a promise that agents can reproduce every paper.

## Inspiration and adjacent work

This project is inspired by the broader movement around agent skills, MCP, reproducible ML, and open research tooling. It is designed to complement existing projects, not claim ownership over their ideas.

Useful references to study:

- Hugging Face `ml-intern`
- K-Dense scientific agent skills
- GitHub agent skills
- Model Context Protocol
- Reproducible ML practices from Hugging Face and PyTorch

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). The best first contributions are:

- a minimal reproducible ML example
- a paper-reading checklist
- a failure case where an agent made a false research claim
- a benchmark task for `agent-skill-bench`

## License

MIT
