# arch-review  Claude Agent Skills Family

A family of Claude Agent Skills for **read-only software architecture audits**.

## What it does

- Detects project type (monolith, microservices, serverless)
- Routes to specialized sub-skills
- Audits 8 dimensions: quality attributes, structure, data, communication, infra+security, governance
- Emits severity-classified findings, ATAM tradeoffs, proposed ADRs, and a scorecard

## Safety

- Read-only on the audited project
- All writes go to ./arch-review-output/

## Quick start
pip install -r tests/requirements.txt
pytest tests/python -v

text

## Specialists

| Prompt | Skill |
|---|---|
| "Review the architecture of X" | arch-review (orchestrator) |
| "Audit only security of X" | arch-review-infra-security |
| "Review data layer of X" | arch-review-data |
| "Analyze coupling in X" | arch-review-structure |
| "Review communication in X" | arch-review-communication |
| "Evaluate scalability in X" | arch-review-quality-attributes |
| "Find anti-patterns in X" | arch-review-governance |
| "Generate ADRs for X" | arch-review-adr-generator |

## License

MIT
