---
name: arch-review-communication
description: Specialist sub-skill focused on sync/async, error handling, idempotency, API versioning. Triggers "review communication", "audit messaging", "revisar comunicaciÃ³n", "evaluar manejo de errores". Read-only. English output.
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Communication & Integration Review

## Workflow
1. Detect clients, producers, consumers, brokers.
2. Load references/sync-vs-async.md, error-handling.md, api-versioning.md.
3. Analyze (no timeouts=High, non-idempotent payments=Critical, no DLQ=Medium).
4. Return per output-contract.
