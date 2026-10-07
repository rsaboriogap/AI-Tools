# vbu-hackathon-project

A **Claude Code plugin** for spec-driven development: it connects to **Azure DevOps (ADO)** via MCP, pulls context from a work item/ticket, and turns it into a spec/plan document ready to drive implementation.

## Workflow

**Quick path (recommended):** Invoke `spec-driven-development-orchestrator` with a work item ID. It chains all steps below automatically.

**Step-by-step path:** Run each skill individually:

1. You reference an ADO ticket (work item ID).
2. The plugin fetches the ticket's details (title, description, acceptance criteria, comments) through the Azure DevOps MCP server.
3. `azure-devops-ticket-quality` scores the ticket; if it's too vague to spec from, gaps are surfaced before continuing.
4. `solution-analysis-gate` ensures a grounded `documents/technical-solution-analysis.md` exists for the codebase (generating it via `technical-solution-analysis` if missing).
5. `technical-spec-generator` combines the ticket and the solution analysis into an implementation-ready `documents/technical-spec.md`.
6. That spec drives the implementation work.

## Repo structure

| Path | Purpose |
|------|---------|
| `.claude-plugin/plugin.json` | Plugin manifest (name, version, author, license) |
| `agents/` | Agent definitions (placeholder — not yet populated) |
| `commands/` | Slash commands, e.g. a future `/vbu-hackathon-project:pull-ticket` (placeholder — not yet populated) |
| `skills/spec-driven-development-orchestrator/` | **Entry point:** chains all three core skills in sequence (quality → analysis → spec) with gating and error handling |
| `skills/azure-devops-ticket-quality/` | Scores an ADO ticket's quality (clarity, acceptance criteria, risks, etc.) and suggests follow-up questions |
| `skills/technical-solution-analysis/` | Produces a grounded architecture/stack/risk snapshot of the codebase, saved to `documents/technical-solution-analysis.md` |
| `skills/solution-analysis-gate/` | Pipeline gate: checks ticket quality and ensures the solution analysis exists before handing off to spec generation |
| `skills/technical-spec-generator/` | Combines a work item with the solution analysis into an implementation-ready spec, saved to `documents/technical-spec.md` |
| `.env` | Local secrets — currently `AZDO_PAT` (Azure DevOps Personal Access Token) |

Not yet present, planned: an `.mcp.json` at the repo root declaring the Azure DevOps MCP server (via the `@azure-devops/mcp` package), authenticated using `AZDO_PAT` from `.env`.

## Quick Start

👉 **[QUICKSTART.md](./QUICKSTART.md)** — 5-minute setup guide. Start here.

📚 **[SKILLS-DETAILED-GUIDE.md](./SKILLS-DETAILED-GUIDE.md)** — Comprehensive explanation of all 5 skills, what each does, how they work together, and when to use each one. Start here to understand the system.

## Using the Orchestrator

Once set up, invoke the orchestrator to run the full pipeline:

```
"Generate the spec for ticket 12345"
"Run the full pipeline on work item 789 in the MyProject project"
```

The orchestrator will:
1. **Check ticket quality** — scores the ticket against clarity, acceptance criteria, scope, risks, and other dimensions. If the score is too low, it surfaces gaps and asks whether to proceed.
2. **Ensure solution analysis exists** — automatically generates `documents/technical-solution-analysis.md` if missing (grounding the spec in real codebase structure).
3. **Generate the spec** — produces `documents/technical-spec.md` with scope, approach, sequencing, risks, and testing strategy.

All three artifacts are generated and linked for easy reference.

**For advanced use:** Run individual skills directly (`azure-devops-ticket-quality`, `technical-solution-analysis`, `solution-analysis-gate`, `technical-spec-generator`) if you need to debug a specific stage or work with pre-existing artifacts.

## Setup

1. Copy your Azure DevOps PAT into `.env`:
   ```
   AZDO_PAT=<your-pat>
   AZURE_DEVOPS_EXT_PAT=<your-pat>
   ```
   (See [QUICKSTART.md](./QUICKSTART.md) for how to get your PAT)

2. Update `.mcp.json` with your Azure DevOps organization name (replace `"wearegap"` with your org):
   ```json
   "args": ["@azure-devops/mcp", "YOUR-ORG-NAME", "-a", "env"]
   ```

3. Configure `.claude/settings.json` with your default project (optional but recommended):
   ```json
   {
     "azureDevOpsTicketQuality": {
       "defaultProject": "your-project-name"
     }
   }
   ```
   This allows you to invoke the orchestrator with just the work item ID, without repeating the project name each time.

4. Install the plugin in Claude Code:
   ```bash
   claude plugin install /path/to/vbu-hackathon-project
   ```

## Status

Hackathon-stage scaffold. `agents/` and `commands/` are still empty placeholders; `skills/` has the full ticket-to-spec pipeline:
- ✅ `spec-driven-development-orchestrator` (end-to-end entry point)
- ✅ `azure-devops-ticket-quality` (ticket scoring and gap detection)
- ✅ `technical-solution-analysis` (codebase architecture analysis)
- ✅ `solution-analysis-gate` (pipeline gating and orchestration)
- ✅ `technical-spec-generator` (implementation spec generation)

More skills and agents to come as the spec-driven-dev workflow is built out.
