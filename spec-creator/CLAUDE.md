# vbu-hackathon-project

This repository **is** a Claude Code plugin implementing **spec-driven development**: connect to Azure DevOps via MCP, pull ticket info, generate a plan/spec to drive implementation. Every agent and skill built for this project is created as part of this plugin — add new agents under `agents/` and new skills under `skills/`, not elsewhere.

## Plugin Structure

- **Manifest:** `.claude-plugin/plugin.json`
- **Agents & Commands:** `agents/`, `commands/` — plugin scaffolding, currently empty placeholders to be populated
- **Skills:**
  - `skills/spec-driven-development-orchestrator/` — **Entry point.** Chains all three core skills in sequence with gating and error handling. Invoke with a work item ID; it coordinates quality assessment → solution analysis → spec generation.
  - `skills/azure-devops-ticket-quality/` — Scores ADO ticket quality (clarity, acceptance criteria, risks, etc.) and suggests follow-up questions
  - `skills/technical-solution-analysis/` — Produces a grounded architecture/stack/risk snapshot of a codebase, saved to `documents/technical-solution-analysis.md`
  - `skills/technical-spec-generator/` — Combines a work item with the solution analysis to produce an implementation-ready spec, saved to `documents/technical-spec.md`
  - `skills/solution-analysis-gate/` — Pipeline gate: runs `azure-devops-ticket-quality` and stops if the ticket is too weak to spec from, ensures `documents/technical-solution-analysis.md` exists (generating it if missing), then hands off to `technical-spec-generator`

## Pipeline

**Recommended:** Invoke `spec-driven-development-orchestrator` with a work item ID. It automatically runs:
```
work-item-id
    ↓
azure-devops-ticket-quality (quality gate)
    ↓
solution-analysis-gate (ensures solution analysis exists)
    ↓
technical-spec-generator (produces spec)
    ↓
documents/technical-spec.md
```

## Configuration

- **`.env`** — holds `AZDO_PAT` (Azure DevOps Personal Access Token)
- **`.mcp.json`** — declares the Azure DevOps MCP server (`@azure-devops/mcp`) keyed off `AZDO_PAT`
- **`.claude/settings.json`** — (optional) configure default project to avoid repeating it:
  ```json
  {
    "azureDevOpsTicketQuality": {
      "defaultProject": "your-project-name"
    }
  }
  ```

## Documentation

- **[README.md](./README.md)** — Project overview and quick start
- **[QUICKSTART.md](./QUICKSTART.md)** — 5-minute setup guide
- **[SKILLS-DETAILED-GUIDE.md](./SKILLS-DETAILED-GUIDE.md)** — Comprehensive explanation of all 5 skills
- **[CLAUDE.md](./CLAUDE.md)** — This file (developer instructions)
