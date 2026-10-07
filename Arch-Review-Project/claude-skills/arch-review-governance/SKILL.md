---
name: arch-review-governance
description: Specialist sub-skill focused on documentation, ADRs, C4 diagrams, cost modeling, anti-patterns. Triggers "review documentation", "check ADRs". Read-only. English output.
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Governance, Documentation & Cost Review

## Workflow
1. Detect docs, ADRs, diagrams, READMEs.
2. Load references/adr-guide.md, c4-model.md, cost-modeling.md, red-flags.md.
3. Analyze (no README=Medium, no ADRs=High, no cost monitoring=Medium).
4. Return per output-contract.
