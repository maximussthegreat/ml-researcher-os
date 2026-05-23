---
name: hf-release-prep
description: Use when preparing Hugging Face model cards, dataset cards, Space demos, or release notes for ML artifacts.
---

# Hugging Face Release Prep

Use this skill when a project is ready to publish an ML artifact.

## Goal

Prepare a release that is useful, reproducible, licensed clearly, and explicit about limitations.

## Release types

Support:

- model repo
- dataset repo
- Space demo
- paper reproduction artifact

## Required output

Produce a release checklist with:

1. Artifact type
2. Intended users
3. Required files
4. Model or dataset card fields
5. Evaluation summary
6. Limitations
7. License and data rights
8. Safety or misuse notes
9. Reproduction command
10. Demo script

## Card rules

- State training data source clearly.
- State evaluation setup clearly.
- Include known failure modes.
- Include intended and out-of-scope uses.
- Do not imply clinical, legal, or production suitability without evidence.

## Final check

End with:

```text
Ready to publish: yes/no
Blocking issues:
- ...
```
