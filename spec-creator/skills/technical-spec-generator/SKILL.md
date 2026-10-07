---
name: technical-spec-generator
description: Turns an Azure DevOps work item plus a grounded Technical Solution Analysis into an implementation-ready technical spec — scope, approach, affected files/components, sequencing, risks, and testing strategy. Use this skill whenever the user asks to "generate a spec," "write an implementation plan," "turn this ticket into a plan," or asks what it would take to build/fix a work item once the existing system's architecture is already understood. Trigger even without the exact phrase "technical spec" — e.g. "plan out this ticket," "how should we implement this," "break this down for a developer to pick up." Depends on a Technical Solution Analysis existing first (see `technical-solution-analysis` skill, or the `solution-analysis-gate` skill that ensures one is present) — don't fabricate architectural context that analysis would normally supply.
---

# Technical Spec Generator

Produces a developer-ready implementation spec by combining a work item's requirements with grounded facts about the existing codebase. The spec is the bridge between "what the ticket asks for" and "what a developer actually changes" — concrete enough to start work from, without prescribing every line of code.

## Inputs required

1. **The work item** — full ticket text, or a work item ID/URL to pull live via `mcp__azure-devops__wit_get_work_item` (`expand: "all"`). If comments carry clarifications not in the description, pull them too with `mcp__azure-devops__wit_list_work_item_comments`. If the ticket reads as vague or thin (missing acceptance criteria, no clear scope, heavy on phrases like "maybe"/"as usual") and this skill was invoked directly rather than through `solution-analysis-gate`, say so and suggest running `azure-devops-ticket-quality` first — don't fabricate requirements to fill the gap.
2. **A Technical Solution Analysis** — expected at `documents/technical-solution-analysis.md`. If it's not present and wasn't otherwise provided in-conversation, say so explicitly and suggest running the `technical-solution-analysis` skill (or the `solution-analysis-gate` skill, which handles this automatically) rather than guessing at the architecture.

## Workflow

1. **Read the analysis.** Pull the architecture, stack, conventions, and existing risks from the Technical Solution Analysis. This is your source of truth for how the system is built — don't re-derive it from scratch or contradict it without re-checking the code.
2. **Read the ticket.** Extract the actual requirement: what should change, for whom, and why. Note any acceptance criteria — they become your test/verification checklist.
3. **Map requirement to codebase.** Using the analysis's named files/modules/patterns, identify which specific components the work touches. Cite paths, not generic layers — "the `OrderController` in `Api/Controllers`" not "the API layer."
4. **Decide the approach.** Pick an implementation strategy consistent with the conventions the analysis already documented (same ORM, same DI pattern, same test tooling) unless the ticket explicitly calls for deviating — and if it does, flag that as a decision point, not a silent choice.
5. **Sequence the work.** Break the approach into ordered steps a developer can pick up one at a time. Steps should be small enough to review individually but not so granular they're just restating the diff.
6. **Surface risks and open questions.** Anything the analysis or ticket left ambiguous, any breaking change, any migration — call it out rather than assuming an answer.
7. **Render as Markdown** per `references/spec-template.md` — a default shape to adapt, not fill mechanically. Deliver a `.md` file.

## Output format

Use `references/spec-template.md` as the default shape; cut, expand, or reorder sections as the ticket warrants — a one-file bug fix doesn't need a sequencing table, a multi-service feature might. No scores/percentages, no false-precision estimates unless the ticket or user asked for sizing. Every proposed change should name the file/module it touches; if you don't know exactly which file, say what you'd need to check rather than guessing.

Deliverable: a `.md` file, always. Default path: `documents/technical-spec.md` (relative to project root, mirroring where the solution analysis lives) — create `documents/` first if needed, unless the user specifies a different location. If `documents/technical-spec.md` already exists, that's most likely a previous ticket's spec — confirm with the user before overwriting it (or write to a ticket-specific filename, e.g. `documents/technical-spec-<work-item-id>.md`, if they'd rather keep both) rather than silently clobbering prior work.
