---
name: arch-review-adr-generator
description: Generates retroactive ADRs from an existing codebase or findings. Triggers "generate ADRs", "document decisions". Read-only on target; writes to ./arch-review-output/adrs/. English output.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# ADR Generator

## Workflow
1. Identify decisions (configs, compose, terraform, openapi, auth, README, findings.json).
2. Rank by Impact x Reversibility x Ambiguity. Top 5-10.
3. Fill MADR template (assets/adr-template.md). Mark Status: Reconstructed.
4. Write to ./arch-review-output/adrs/ADR-NNN-*.md + index.md.
5. Report count, table, link.

## Rules
Never invent. Mark uncertainty. One decision per ADR. Immutable.
