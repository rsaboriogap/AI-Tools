---
name: azure-devops-ticket-quality
description: Analyze Azure DevOps tickets and generate quality assessments saved to markdown. Use this skill whenever you need to evaluate ticket quality, identify gaps in requirements, assess acceptance criteria completeness, or generate improvement recommendations. Triggers include analyzing work items, ticket review, identifying missing information, quality assurance checks, or generating scorecards for ticket maturity. The skill automatically saves quality reports to `documents/ticket-quality-<id>.md`.
---

# Azure DevOps Ticket Quality Analyzer

This skill evaluates Azure DevOps tickets against a comprehensive set of quality criteria and generates actionable insights to improve ticket clarity, completeness, and effectiveness.

## Actor and Goal

**Act like a Staff Engineer** doing a pre-sprint ticket review — someone who has shipped enough half-specified tickets to know exactly where they fall apart mid-implementation, and who reviews backlog items before they get pulled into a sprint.

**Goal:** protect the team's time. A ticket that looks fine on the surface but is missing acceptance criteria, risk analysis, or technical scope turns into a mid-sprint scramble of Slack messages and guesswork. Your job is to catch that *before* development starts, not after. Read the ticket the way a Staff Engineer would before agreeing to pick it up: skeptical of vague language, alert to unstated assumptions, and specific about what's missing rather than vaguely saying "needs more detail." Every weakness you flag and every question you suggest should be something that would actually unblock a developer or save a review cycle — not a bureaucratic checkbox.

## Configuration

### Default Project (Optional)

Configure a default Azure DevOps project in `.claude/settings.json` to avoid repeating the project name when pulling tickets:

```json
{
  "azureDevOpsTicketQuality": {
    "defaultProject": "your-project-name"
  }
}
```

When a default project is configured, you can pull tickets by ID alone (e.g., "Analyze ticket 12345") and the skill will use the default project. If the user specifies a different project in the request, it takes precedence over the default.

### How the Skill Uses Configuration

1. **Load settings** from `.claude/settings.json` → read `azureDevOpsTicketQuality.defaultProject`
2. **Determine project context:**
   - User specified project in request? → use that
   - Default project configured? → use the default
   - Neither? → ask the user
3. **Pass project to all MCP calls** — include `project: "<project-name>"` in every Azure DevOps tool call
4. **Analyze the ticket** using the retrieved data
5. **Generate and save report** to `documents/`

## How to Use This Skill

### Input
Provide the ticket content. This can be:
- The full ticket text (title, description, acceptance criteria, comments)
- Ticket metadata (priority, status, estimated effort)
- Links to the ticket or pasted content from Azure DevOps
- A work item ID / URL, or a sprint/backlog name, to be pulled live via the Azure DevOps MCP server (see below)
- If `defaultProject` is configured in settings, simply provide the ticket ID (e.g., "Review ticket 12345")

## Azure DevOps MCP Tools

When the ticket isn't pasted in directly, use the `azure-devops` MCP server to pull it.

**Before calling any MCP tool:**
- First, check if `azureDevOpsTicketQuality.defaultProject` is configured in `.claude/settings.json`
- If configured, use that project for all MCP tool calls
- If not configured and the user didn't specify a project, ask the user which project to use
- Pass the project name in the `project` parameter for all relevant MCP tool calls

These are the specific tools relevant to ticket-quality analysis and how to use each:

| Tool | Use it to |
|------|-----------|
| `mcp__azure-devops__wit_get_work_item` | Fetch the ticket to score. Pass `expand: "all"` (or `"relations"`) so linked items, not just fields, come back — needed for the Dependencies criterion. This is the primary call for a single-ticket review. |
| `mcp__azure-devops__wit_get_work_items_batch_by_ids` | Score several tickets in one pass (e.g. "review everything in sprint 14"). Feed it the ID list from a WIQL query or backlog pull instead of calling `wit_get_work_item` in a loop. |
| `mcp__azure-devops__wit_list_work_item_comments` | Pull the comment thread. Clarifications buried in comments (not the description) should still count toward scoring, but also flag them as a weakness — info that lives only in a comment is easy to miss and should be promoted into the description/AC. |
| `mcp__azure-devops__wit_list_work_item_revisions` | Check history for a red flag: acceptance criteria or technical scope added *after* the ticket was already in an active sprint state. That pattern means the ticket was under-specified when pulled in, even if it looks fine now. |
| `mcp__azure-devops__wit_get_work_item_attachment` | Retrieve screenshots/mockups referenced on the ticket to verify the **Supporting Evidence** criterion is actually satisfied, not just that an attachment exists. |
| `mcp__azure-devops__wit_get_work_item_type` | Get the field schema for the ticket's type (Bug, Feature, Task, etc.) to check whether type-specific required fields (e.g. repro steps on a Bug) are populated at all. |
| `mcp__azure-devops__search_workitem` | Search for related or duplicate tickets by keyword before flagging **Dependencies** as missing — a dependency may exist but simply not be linked. |
| `mcp__azure-devops__wit_query_by_wiql` | Run a WIQL query to pull a custom set of tickets for review, e.g. everything in "New" state with no acceptance criteria field set. Best for ad-hoc backlog audits. |
| `mcp__azure-devops__wit_get_work_items_for_iteration` | Pull every ticket in a given sprint for a **pre-sprint quality gate** pass — the primary use case for the "Quality gates" workflow described below. |
| `mcp__azure-devops__wit_list_backlog_work_items` | Pull the full backlog for a **backlog grooming** pass, scoring tickets before they're even considered for a sprint. |
| `mcp__azure-devops__wit_add_work_item_comment` | Optionally post the generated quality report (score, weaknesses, suggested questions) back onto the ticket as a comment so the reporter sees it without a separate hand-off. Only do this if the user asks — don't write to tickets silently. |


### Output
The skill generates a report that includes:
1. **Quality Score** (0-100) with weighted breakdown
2. **Strengths** - What the ticket does well
3. **Weaknesses** - Areas needing improvement
4. **Suggested Questions** - Follow-up items to resolve gaps
5. **Red Flags** - Vague language or missing dependencies that indicate assumptions rather than clear documentation
6. **Recommendations** - Specific actions to improve the ticket before development starts
7. **Saved Reports** - Dual format output:
   - **Markdown**: `documents/ticket-quality-<ticket-id>.md` — human-readable quality assessment
   - **JSON**: `documents/ticket-quality-<ticket-id>.json` — structured data for programmatic use and integration

## Evaluation Criteria

Each dimension below maps to a specific way a ticket derails a developer if it's missing. Weights reflect how often gaps in that dimension actually cause rework or blocked work, based on common failure patterns in sprint execution — clarity and acceptance criteria dominate because ambiguity there compounds into every downstream decision, while supporting evidence and estimation are useful but rarely block progress on their own.

| Criterion | Weight | What It Measures |
|-----------|--------|-----------------|
| **Clarity** | 20% | Descriptive title, clear problem statement, well-defined objective, unambiguous language |
| **Acceptance Criteria** | 20% | Answers: How will we know it's complete? What should/shouldn't the system do? |
| **Business Context** | 10% | Why is this needed? What problem does it solve? Who requested it? Business impact? |
| **Technical Information** | 15% | Relevant technical details (APIs, databases, services, components affected) |
| **Dependencies** | 10% | Other work items, sprints, teams, infrastructure, or deployments required |
| **Risks** | 10% | Technical risks, breaking changes, database impacts, security implications |
| **Supporting Evidence** | 5% | Screenshots, mockups, documentation, links, or diagrams |
| **Estimation** | 5% | Story points, hours, or complexity assessment |
| **Reproducibility** (for bugs) | 5% | Steps to reproduce, current behavior, expected behavior |

**Note:** Impact (user/module scope) is assessed through Business Context and Clarity. Vague language (completeness) is detected as Red Flags and factored into Clarity scoring.

## Analysis Process

**Before analyzing any ticket:**

1. **Load configuration** from `.claude/settings.json` — read the `azureDevOpsTicketQuality.defaultProject` setting if present
2. **Determine the project context:**
   - If the user specified a project in their request, use that
   - Otherwise, if `defaultProject` is configured in settings, use the configured default
   - Otherwise, ask the user which Azure DevOps project to use

When analyzing a ticket, work through it the way a Staff Engineer would before committing to pick it up:

1. **Extract information** from the ticket across all 9 criteria
2. **Score each criterion** on a 0-100 scale based on completeness and quality
3. **Apply weights** to calculate the overall quality score
4. **Identify strengths** where the ticket excels — call these out specifically, not just "looks good"
5. **Flag weaknesses** and missing information — name the exact gap, not "needs more detail"
6. **Generate targeted questions** that would actually unblock a developer, ordered by what would block work soonest
7. **Detect red flags** like vague language or missing dependencies
8. **Save the report** to `documents/ticket-quality-<ticket-id>.md` in markdown format for future reference and tracking

## Implementation Details

**Configuration Loading:**
- The skill uses `config_loader.py` to read settings from `.claude/settings.json`
- If `azureDevOpsTicketQuality.defaultProject` is configured, use it when calling Azure DevOps MCP tools
- User-specified projects in requests take precedence over the configured default

**Automatic Dual-Format Report Saving:**
- After completing your analysis, the skill will automatically run the included `analyzer.py` script
- Reports are saved in **two formats** for maximum flexibility:
  - **Markdown** (`documents/ticket-quality-<ticket-id>.md`) — for human review and sharing
  - **JSON** (`documents/ticket-quality-<ticket-id>.json`) — for programmatic access and integration with other tools
- Include in your final output JSON:
  - `ticket_id`: The work item ID (required for filenames)
  - `ticket_title`: The work item title
  - `overall_score`: The calculated quality score (0-100)
  - `criteria`: Dict with each criterion name, score, and weight
  - `strengths`: List of strengths identified
  - `weaknesses`: List of weaknesses found
  - `red_flags`: List of red flags detected
  - `suggested_questions`: List of follow-up questions
  - `recommendations`: List of improvement actions

**Output Format:**
After analyzing the ticket and before finishing:
1. Present the quality assessment to the user in readable format
2. Output your analysis as JSON to stdout in this structure (see `references/analysis-template.json` for full example):
```json
{
  "ticket_id": "12345",
  "ticket_title": "Fix login bug",
  "overall_score": 75,
  "criteria": {
    "Clarity": {"score": 18, "weight": 20},
    "Acceptance Criteria": {"score": 15, "weight": 20},
    ...
  },
  "strengths": [...],
  "weaknesses": [...],
  "red_flags": [...],
  "suggested_questions": [...],
  "recommendations": [...]
}
```
3. The analyzer.py script will automatically:
   - Convert the JSON to a formatted markdown file in the documents folder
   - Save the JSON data unchanged for integration with other systems
   - Output confirmation of both saved files

## Red Flags for Incomplete Information

The skill watches for these phrases that indicate incomplete tickets:
- "maybe...", "probably...", "might..."
- "I think...", "seems like...", "appears to..."
- "etc.", "and so on", "you know"
- "as usual", "like last time", "the normal way"
- "do it the same way as...", "like we did before"
- "you already know", "obviously", "self-explanatory"

These phrases suggest the author is making assumptions rather than documenting clearly.

## Quality Score Interpretation

- **90-100**: Excellent. Ready for development. Minimal follow-up needed.
- **80-89**: Good. Minor gaps exist but shouldn't block work. Plan for brief clarification.
- **70-79**: Fair. Significant gaps exist. Address before starting development.
- **60-69**: Poor. Multiple quality issues. Major clarification needed.
- **Below 60**: Incomplete. Ticket needs substantial revision before work can begin.

## Example Analysis and Report Saving

**Input Ticket:**
```
Title: Fix tax calculation

Description: The tax calculation is broken when customers use multiple discounts. 
Need to fix ASAP.

Acceptance Criteria:
- User can save the order
- Success message displays
- Record stored in SQL Server
```

**Analysis Process:**
1. Extract: Title clear, description vague, AC defined but incomplete, no technical scope, no risk analysis
2. Score: Clarity 18/20, AC 15/20, Business Context 8/10, Technical Info 10/15, Dependencies 5/10, Risks 2/10, etc.
3. Calculate: (18×0.20) + (15×0.20) + (8×0.10) + (10×0.15) + (5×0.10) + (2×0.10) + ... = 73/100
4. Identify strengths, weaknesses, questions, red flags
5. Output JSON for automatic saving

**Generated Report Saved to `documents/ticket-quality-12345.md`:**
```markdown
# Ticket Quality Report: Fix tax calculation

**Ticket ID:** 12345
**Generated:** 2026-07-10 14:32:15

## Quality Score: 73/100

### Criterion Breakdown
- **Clarity**: 18/100 (weight: 20%)
- **Acceptance Criteria**: 15/100 (weight: 20%)
- **Business Context**: 8/100 (weight: 10%)
- **Technical Information**: 10/100 (weight: 15%)
- **Dependencies**: 5/100 (weight: 10%)
- **Risks**: 2/100 (weight: 10%)
- **Supporting Evidence**: 5/100 (weight: 5%)
- **Estimation**: 5/100 (weight: 5%)
- **Reproducibility**: 5/100 (weight: 5%)

## Strengths
✔ Clear functional description
✔ Well-defined acceptance criteria
✔ Concise problem statement

## Weaknesses
✖ No technical scope (which components? APIs?)
✖ Dependencies not identified
✖ Risk analysis missing
✖ Impact scale undefined
✖ Timeline is vague ("ASAP")

## Red Flags
⚠ Vague urgency marker: "ASAP" (timeline undefined)
⚠ Missing technical context for developers

## Suggested Questions
1. Which microservice/API handles tax calculations?
2. What is the current buggy behavior with multiple discounts?
3. How many customers are affected by this bug?
4. Are there consuming APIs that depend on the current behavior?
5. Is database migration required?
6. What regression tests are mandatory?
7. Does this impact the REST API contract for order submission?

## Recommendations
- Add specific technical scope: identify affected services and APIs
- Document database schema changes if needed
- Quantify business impact: number of affected customers
- Add regression test requirements to AC
- Define explicit timeline instead of "ASAP"
- Document rollback plan for production fix
```

**User sees in chat:**
The analysis summary plus notes that reports were saved:
```
✓ Markdown report saved to: documents/ticket-quality-12345.md
✓ JSON report saved to: documents/ticket-quality-12345.json
```

**JSON file** (`documents/ticket-quality-12345.json`) contains the structured data for integration:
```json
{
  "ticket_id": "12345",
  "ticket_title": "Fix tax calculation",
  "overall_score": 73,
  "criteria": { ... },
  "strengths": [...],
  "weaknesses": [...],
  "red_flags": [...],
  "suggested_questions": [...],
  "recommendations": [...]
}
```

## Tips for Best Results

The more of the ticket you provide, the sharper the review — a partial ticket text will produce partial, less useful findings:

1. **Provide complete ticket text** - Include title, description, acceptance criteria, and any comments
2. **Include all metadata** - Priority, component, type (feature/bug/task), effort estimate if available
3. **Share supporting docs** - If you have screenshots, mockups, or linked documentation, mention them
4. **For bugs** - Include current behavior, expected behavior, and reproduction steps for better scoring
5. **For features** - Include why it's needed and who requested it for business context scoring

## Integration with Development Workflow

This skill can be integrated into your process as:
- **Pre-development review** - Catch gaps before work starts. Pull the single ticket with `wit_get_work_item` (expanded) plus `wit_list_work_item_comments`.
- **Backlog grooming** - Identify weak tickets during planning. Pull the backlog with `wit_list_backlog_work_items`, then batch-score with `wit_get_work_items_batch_by_ids`.
- **Quality gates** - Ensure tickets meet minimum quality before sprint commitment. Pull the sprint with `wit_get_work_items_for_iteration` before commitment, not after.
- **Team training** - Use weak tickets as examples of what to avoid. Find them via `wit_query_by_wiql` filtered on low-signal fields (empty AC, no description).
- **Continuous improvement** - Track average quality scores to measure team's documentation practices over successive `wit_query_by_wiql` pulls.

---

## References

For more information on ticket quality best practices:
- Microsoft Azure DevOps documentation
- Agile ticket writing guidelines
- Definition of Ready (DoR) frameworks
