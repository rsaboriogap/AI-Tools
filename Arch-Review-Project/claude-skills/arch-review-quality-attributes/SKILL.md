---
name: arch-review-quality-attributes
description: Specialist sub-skill focused on scalability, performance, availability/resilience, and maintainability. Triggers "review scalability", "audit performance". Read-only. English output.
allowed-tools: Read, Glob, Grep, Bash
---

# Quality Attributes Review

## Workflow
1. Detect sources, configs, middleware.
2. Load references/scalability.md, performance.md, availability-resilience.md, maintainability.md.
3. Analyze (SPOF=High, N+1=High, no caching=Medium).
4. Return per output-contract.
