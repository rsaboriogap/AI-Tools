---
name: arch-review-infra-security
description: Specialist sub-skill focused on infrastructure, CI/CD, observability, auth, secrets, OWASP. Triggers "audit security", "review deployment". Read-only. English output.
allowed-tools: Read, Glob, Grep, Bash
---

# Infrastructure & Security Review

## Workflow
1. Detect Docker, k8s, terraform, CI, auth code, .env.
2. Load references/deployment-topologies.md, cicd-observability.md, auth-authz.md, secrets-management.md, owasp-top10.md.
3. Analyze (hardcoded secrets=Critical, missing authn=Critical, no TLS=High).
4. Return per output-contract.
