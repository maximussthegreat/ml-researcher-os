# Architecture Notes

`ml-researcher-os` is organized as a small set of agent skills plus reproducible research templates.

## Core objects

| Object | Purpose |
| --- | --- |
| Skill | A bounded instruction pack for an agent. |
| Protocol | A repeatable sequence of research steps. |
| Template | A concrete artifact the agent writes or fills. |
| Example | A small runnable research task. |
| Report | Evidence, results, limitations, and next steps. |

## Skill contract

Each skill should define:

- what the agent is allowed to do
- what the agent must not claim
- required inputs
- required outputs
- failure states
- examples of good and bad behavior

## Evidence contract

Every research output should mark statements as one of:

- observed
- computed
- cited
- inferred
- speculative

This prevents the agent from blending facts with confident guesses.

