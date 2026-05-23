---
name: result-reporter
description: Use when summarizing experiment logs, benchmark outputs, ablations, failed runs, or model results into an honest research report.
---

# Result Reporter

Use this skill after experiments produce logs, metrics, or artifacts.

## Required sections

1. Summary
2. Setup
3. Results table
4. Observations
5. Interpretation
6. Limitations
7. Negative results
8. Next experiments

## Evidence tags

Every important statement must be tagged:

- `[observed]` direct from logs or artifacts
- `[computed]` derived from available data
- `[cited]` from a source
- `[inferred]` plausible but not directly measured
- `[speculative]` hypothesis for follow-up

## Reporting rules

- Do not hide failed runs.
- Do not round away meaningful differences.
- Do not claim state of the art unless the benchmark setup exactly matches.
- Do not compare against a baseline that was not run or cited.
- Include uncertainty when seeds or confidence intervals are missing.

## Results table format

| Run | Seed | Dataset split | Metric | Value | Notes |
| --- | --- | --- | --- | --- | --- |

## Final line

End with a clear answer:

```text
Claim supported: yes/no/partial
Reason: ...
```

