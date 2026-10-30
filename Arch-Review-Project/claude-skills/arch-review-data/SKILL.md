---
name: arch-review-data
description: Specialist sub-skill focused on data models, consistency, migrations, caching. Triggers "review data layer", "audit database design". Read-only. English output.
allowed-tools: Read, Glob, Grep, Bash
---

# Data & Persistence Review

## Workflow
1. Detect migrations, ORM configs, models.
2. Load references/data-models.md, consistency-patterns.md, caching-strategies.md.
3. Analyze (no backups=Critical, unencrypted PII=Critical, shared DB=Critical).
4. Return per output-contract.
