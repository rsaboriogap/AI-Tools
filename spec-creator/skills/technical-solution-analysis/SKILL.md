---
name: technical-solution-analysis
description: Produces a lightweight Technical Solution Analysis of a codebase — architecture, tech stack, frameworks, design patterns, code quality, security, testing, observability, dependencies, and scalability — sized to give a planning/spec-generation skill enough grounded context about the existing system, not to be an exhaustive audit. Use this skill whenever the user (typically a Staff Software Engineer or Staff Software Architect) asks to analyze a codebase/solution/repository, understand the current architecture before planning a change, assess the impact of an Azure DevOps work item/ticket/requirement against the existing system, or otherwise needs a grounded technical snapshot to drive implementation planning. Trigger even without the exact phrase "Technical Solution Analysis" — e.g. "analyze this solution," "what's the architecture here," "what would it take to implement this ticket," or "give me context on this codebase before we plan the work."
---

# Technical Solution Analysis

A structured technical snapshot of a codebase — architecture, stack, design quality, risk — sized for a downstream planning/spec-generation step, not an exhaustive audit. Just enough evidence-based context that a plan built on top won't miss something obvious about how the system works.

## Depth

Match depth to what a planner needs: a handful of files as evidence per area is enough, don't enumerate exhaustively. Let any given requirement/ticket steer focus — e.g. a new-endpoint ticket means more on architecture/API surface, less on test coverage. Skip or one-line areas that don't apply; don't pad.

## Workflow

1. **Identify the project path (priority order).**
   - **First:** If a `projectPath` parameter is provided, use that.
   - **Second:** If `settings.json` has `technicalSolutionAnalysis.defaultProjectPath` configured and it's not empty, use that.
   - **Third:** Use the current working directory.
   - Validate the resolved path exists; fail with a clear error if not.

2. **Gather context.** Read the repo root, solution/project files, entry points, dependency manifests (`.csproj`, `package.json`, etc.). If a work item/ticket is referenced but not pasted in, pull it via the `azure-devops` MCP server (`mcp__azure-devops__wit_get_work_item`, `expand: "all"`) — it tells you where to focus.
3. **Cover the analysis areas below as a starting checklist, not a fixed contract.** Add areas it doesn't list (CI/CD, multi-tenancy, data model, feature flags, etc.) if they matter more here. Ground every finding in what you actually saw — cite files/classes/packages, never guess.
4. **Bucket recommendations/risks** High / Medium / Low by how much they'd affect planning or implementing new work.
5. **Render as Markdown** per `references/report-template.md` — a default shape to adapt, not fill mechanically. Deliver a `.md` file.

## Analysis areas (adapt as needed)

1. **Architecture** — Style in plain terms based on what the code shows (don't force a named category). Key layers/modules and their dependencies. Dependency issues only if they'd trip up new work.
2. **Project Scope** — Projects/services/apps, entry points, internal vs. external-facing.
3. **Technology Stack** — Backend, frontend, data storage, messaging.
4. **Frameworks & Libraries** — Whatever's actually present that matters for how new code should be written (ORM, DI, validation, logging, jobs, etc.).
5. **Design Patterns & Conventions** — Patterns in use, conventions a contributor must follow to fit in, anti-patterns only if likely to bite the next ticket.
6. **Code Quality** — Quick health read (duplication, oversized files) — not static-analysis depth.
7. **Security** — Auth mechanism, red flags relevant to the planned change.
8. **Testing** — Coverage/tooling that exists, so a plan knows its safety net.
9. **Observability** — Logging/monitoring, if relevant to the work.
10. **Dependencies** — Notably outdated/risky ones, if relevant.
11. **Scalability** — Only if the work touches performance, concurrency, or scale.
12. **Recommendations** — What a planner should know before scoping: risks, constraints, suggested approach.

## Parameters

- **`projectPath`** (optional): Absolute or relative path to the project directory to analyze.
  - **Highest priority:** overrides settings and current directory.
  - Example: `/vbu-hackathon-project:technical-solution-analysis --projectPath D:\path\to\project`

## Configuration

Set a default project path in `.claude/settings.json` to avoid typing it repeatedly:

```json
{
  "technicalSolutionAnalysis": {
    "defaultProjectPath": "D:\\path\\to\\your\\project"
  }
}
```

- **Second priority:** used if `projectPath` parameter is not provided.
- Leave empty (`""`) to skip and fall back to current working directory.

## Priority Order

1. `projectPath` parameter (if provided)
2. `settings.json` `defaultProjectPath` (if configured and not empty)
3. Current working directory (fallback)

## Output format

Use `references/report-template.md` as the default shape; cut, expand, or add sections as the codebase warrants. Tables for structured data, fenced `text` blocks for dependency graphs. No emojis, no symbol checkmarks, no scores/percentages/ratings (no "SOLID Score: 80%", no "Maintainability: High") — false precision a planner doesn't need. Instead, name the file/folder/package behind every finding so it can be checked or explored further. Be concise and evidence-based: "3 background jobs run via Hangfire in `Infra/Jobs`" not vague claims.

Deliverable: always a `.md` file saved to `documents/technical-solution-analysis.md` (relative to the analyzed project root). Create the `documents/` directory first if it doesn't exist. This fixed path lets downstream planning/spec-generation steps (e.g. `technical-spec-generator`) find the analysis without being told where it landed. If this skill is invoked directly (not through `solution-analysis-gate`) and the file already exists, confirm with the user that they want to regenerate/overwrite it — `solution-analysis-gate` is what should normally decide this, but a direct invocation bypasses that check.
