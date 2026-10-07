---
name: arch-review-structure
description: Specialist sub-skill focused on architectural style, module boundaries, coupling, cohesion, API contracts. Triggers "review architecture style", "check coupling". Read-only. English output.
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Structure & Modularity Review

## Workflow
1. Detect source folders, boundaries, API specs.
2. Load references/architectural-styles.md, coupling-cohesion.md, api-contracts.md.
3. Analyze (cyclic deps=High, shared DB=Critical, god module=High).
4. Return per output-contract.
