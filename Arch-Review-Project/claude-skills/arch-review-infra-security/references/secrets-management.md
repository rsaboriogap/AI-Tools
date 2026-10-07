# Secrets Management

Sources: Vault, AWS/GCP/Azure Secret Manager, SOPS.
Rules: never in code/logs/images, rotate, least privilege, audit.
Anti-patterns: .env committed, base64 as encryption, shared secrets.
