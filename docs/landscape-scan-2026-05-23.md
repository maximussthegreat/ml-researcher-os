# Landscape Scan: Agentic ML Research

Scan date: 2026-05-23.

This project should not compete by claiming to be a full autonomous scientist. The stronger position is narrower: make agentic ML work auditable, reproducible, and useful inside ordinary repos.

## GitHub signals

| Project | Signal | What to learn |
| --- | ---: | --- |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 82k+ stars | One file, one metric, fixed budget, keep/reject loop. |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 13k+ stars | End-to-end research automation is a compelling story. |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 6k+ stars | Agentic tree search and experiment management are central. |
| [aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | 12k+ stars | "Idea to paper" framing pulls attention, but needs guardrails. |
| [facebookresearch/MLGym](https://github.com/facebookresearch/MLGym) | 600+ stars | Research agents need benchmark environments and inspectable trajectories. |
| [openai/mle-bench](https://github.com/openai/mle-bench) | high credibility | Evaluation must be grounded in real tasks and external scoring. |

Star counts are snapshots from GitHub search, not a promise about future popularity.

## Internet and paper signals

- [PaperBench](https://openai.com/index/paperbench/) frames paper replication as a hierarchy of gradable tasks.
- [MLE-bench](https://github.com/openai/mle-bench) frames ML engineering agents around real competition-style scoring.
- [MLGym](https://github.com/facebookresearch/MLGym) focuses on realistic research tasks: hypotheses, data, implementation, training, analysis, and iteration.
- [AI Scientist-v2](https://arxiv.org/abs/2504.08066) uses progressive agentic tree search managed by an experiment manager.
- [autoresearch](https://github.com/karpathy/autoresearch) shows that the public loves a tiny, inspectable loop: edit, run, measure, keep or discard.

## Product ideas for this repo

1. Research loop ledger: fixed-budget metric loops with automatic keep/reject decisions.
2. PaperBench-style rubric generator: turn a paper claim into smaller gradable tasks.
3. MLGym adapter: export failure cases and loop tasks into benchmark-friendly task folders.
4. Trajectory report: summarize an agent's experiment history as a readable lab notebook.
5. Claim firewall: block final reports when metrics improved but reproducibility checks are red.
6. Public "repo doctor" badge: generate a README badge or table from `mlro doctor`.
7. Failure marketplace: curated examples of agent research failures that contributors can fix.

## Decision

Implemented first: the research loop ledger.

Reason: it combines the strongest public pattern from autoresearch with the credibility posture of PaperBench and MLGym. It is useful immediately, requires no GPU to inspect, and gives contributors a concrete artifact to discuss in issues and PRs.
