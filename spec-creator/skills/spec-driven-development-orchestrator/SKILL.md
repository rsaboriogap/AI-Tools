---
name: spec-driven-development-orchestrator
description: End-to-end orchestrator for the spec-driven development pipeline. Accepts an Azure DevOps work item ID and coordinates the full workflow: ticket quality assessment → solution analysis (with gating) → technical spec generation. Generates quality reports, architectural analysis, and implementation-ready specs all in one go. Use this skill when you want to run the complete pipeline from a single entry point for a work item.
---

# Spec-Driven Development Orchestrator

An end-to-end orchestrator that chains the three core skills of spec-driven development: quality assessment, solution analysis, and spec generation. Invoke this once with a work item ID, and it coordinates the full pipeline, handling gating, error cases, and file management transparently.

## Actor and Goal

**Act like a Project Manager** overseeing handoffs between specialized teams — your job is to ensure each stage completes successfully and to communicate blockers or decisions back to the user clearly.

**Goal:** Turn a single work item ID into a complete, implementation-ready package:
1. Validate the ticket is clear enough to work from (quality gate)
2. Ground the solution in the existing codebase architecture (solution analysis)
3. Produce a concrete plan a developer can pick up immediately (technical spec)

All three steps should feel like one coherent workflow, not three separate skill invocations.

## How to Use This Skill

### Input

The skill requires:
- **Work item ID** (e.g., `12345`) — a numeric Azure DevOps work item ID
- **Project name** (optional) — the Azure DevOps project. If `azureDevOpsTicketQuality.defaultProject` is configured in `.claude/settings.json`, this can be omitted and the default will be used. If not configured, you'll be asked to provide it.

Example invocations:
- "Generate the spec for ticket 12345" (uses configured default project if set)
- "Generate the spec for ticket 12345 in the MyProject project"
- "Run the full pipeline on work item 789"

### Output

The skill produces:

1. **Quality Report** — saved to `documents/ticket-quality-<id>.md` (and `.json`)
   - Quality score and breakdown
   - Identified strengths and weaknesses
   - Suggested questions to resolve gaps
   - Red flags in the ticket

2. **Technical Solution Analysis** — saved to `documents/technical-solution-analysis.md` (if not already present)
   - Codebase architecture and structure
   - Tech stack and conventions
   - Existing risks and patterns
   - Key files and modules

3. **Technical Specification** — saved to `documents/technical-spec.md`
   - Scope and approach
   - Affected components and files
   - Sequencing and implementation steps
   - Risks and open questions
   - Testing and verification strategy

4. **Execution Summary** — saved to `documents/execution-summary-{ticket_id}.md` AND presented in chat showing:
   - Overall status (✅ Completed, ⚠️ Blocked, ❌ Failed)
   - Total execution time (e.g., "95 seconds")
   - Total tokens consumed (e.g., "17,000 tokens, ~$0.17")
   - Token breakdown per stage
   - Quality score and gate decision
   - Links to all generated documents
   - Detailed metrics table
   - Next steps and troubleshooting

**Example summary metrics:**
```
Total Execution Time: 95 seconds
Token Usage:
  - Stage 1 (Quality):  2,840 tokens (16.7%)
  - Stage 2 (Analysis): 8,920 tokens (52.5%)
  - Stage 3 (Spec):     5,240 tokens (30.8%)
  ────────────────────────────────
  Total:              17,000 tokens (~$0.17)

Quality Score: 82/100 ✅ Proceed
```

See `EXECUTION-EXAMPLE.md` in this skill folder for a complete example of what the summary looks like.

## Saved Artifacts

All output files are automatically saved to `documents/`:

```
documents/
├── ticket-quality-{ticket_id}.md              ← Quality report (human-readable)
├── ticket-quality-{ticket_id}.json            ← Quality report (structured)
├── technical-solution-analysis.md             ← Codebase architecture analysis
├── technical-spec.md                          ← Implementation plan
└── execution-summary-{ticket_id}.md           ← Pipeline execution metrics & summary ✨ NEW
```

The **execution summary** includes:
- Execution timeline with durations and token usage
- Quality assessment details
- All generated artifacts and their purposes
- Recommendations for development teams
- Troubleshooting guide for common issues
- Total cost estimate (based on token count)

## Pipeline Workflow

This skill orchestrates three distinct stages:

### Stage 1: Ticket Quality Assessment
- **Skill:** `azure-devops-ticket-quality`
- **Goal:** Determine if the ticket is clear enough to build from
- **Action:** Analyze the work item against quality criteria (clarity, acceptance criteria, technical scope, dependencies, risks, etc.)
- **Gate:** Score must be ≥ 70 (Fair or better) to proceed
- **If blocked:** Surface the quality report to the user and ask whether to:
  - Resolve the gaps first (recommended), or
  - Proceed anyway at the user's explicit direction

### Stage 2: Solution Analysis Gating
- **Skill:** `solution-analysis-gate`
- **Goal:** Ensure architectural context exists before spec generation
- **Action:** 
  1. Optionally re-run the quality gate (if invoked directly on a weak ticket)
  2. Check if `documents/technical-solution-analysis.md` already exists
  3. If missing, invoke `technical-solution-analysis` to generate it
  4. If present, skip regeneration (idempotent by design)
- **Output:** Confirmed existence of `documents/technical-solution-analysis.md`

### Stage 3: Technical Spec Generation
- **Skill:** `technical-spec-generator`
- **Goal:** Produce a developer-ready implementation plan
- **Action:** Combine the ticket requirements with the codebase architecture to produce a concrete, sequenced approach
- **Input:** The ticket and `documents/technical-solution-analysis.md`
- **Output:** `documents/technical-spec.md`

## Detailed Flow

```
1. User invokes: "Generate spec for ticket 12345"
        ↓
2. Determine project context (use default if configured, ask user if not)
        ↓
3. Invoke azure-devops-ticket-quality
   ├─ Fetch work item via MCP
   ├─ Analyze against quality criteria
   ├─ Save report to documents/ticket-quality-12345.{md,json}
   └─ Return: quality score, summary
        ↓
4. Quality gate decision:
   ├─ Score ≥ 70? → Proceed to stage 2
   └─ Score < 70? → Show report, ask user to confirm or fix
        ↓
5. Invoke solution-analysis-gate
   ├─ Check for documents/technical-solution-analysis.md
   ├─ If missing: invoke technical-solution-analysis
   │  ├─ Analyze codebase structure, stack, conventions, risks
   │  └─ Save to documents/technical-solution-analysis.md
   └─ Return: path to analysis file
        ↓
6. Invoke technical-spec-generator
   ├─ Read the work item
   ├─ Read documents/technical-solution-analysis.md
   ├─ Map requirements to codebase
   ├─ Design implementation approach
   ├─ Sequence work steps
   ├─ Surface risks and questions
   └─ Save to documents/technical-spec.md
        ↓
7. Return summary to user:
   ├─ Quality score and key findings
   ├─ Confirmation that solution analysis was used
   └─ Path to final technical spec
```

## Handling Common Scenarios

### Scenario: Ticket quality is too low (< 70)
The orchestrator will:
1. Show the quality report (score, weaknesses, suggested questions)
2. Ask: "This ticket scores [X]/100. Recommended gaps to address before proceeding: [list]"
3. Offer two paths:
   - "Address these gaps first, then re-run the pipeline"
   - "Proceed anyway at my own risk" (user's explicit choice required)
4. If user chooses to proceed, continue to stage 2 without requiring another quality run

### Scenario: Solution analysis already exists
The orchestrator will:
1. Detect `documents/technical-solution-analysis.md` on disk
2. Skip the `technical-solution-analysis` skill
3. Use the existing analysis (presumed current in this conversation session)
4. Proceed directly to spec generation
5. Tell the user: "Using existing solution analysis from earlier in this conversation"

### Scenario: Multiple work items in one conversation
Each invocation is independent:
- Provide a different work item ID each time
- Quality reports, solution analyses, and specs are saved with the work item ID in the filename
- Users can run the pipeline on multiple tickets in sequence, each with its own set of artifacts

### Scenario: User wants to regenerate (e.g., after updating the ticket)
The user should say so explicitly:
- "Regenerate the spec for ticket 12345" — the orchestrator will re-run all three stages fresh, overwriting prior outputs for that work item
- "Update the solution analysis for ticket 12345" — explicitly re-run the solution analysis (the `solution-analysis-gate` won't regenerate if the file exists, so you'd need to say "regenerate")

This isn't automatic because overwriting prior work should always be explicit.

## Metric Tracking (CRITICAL)

To generate the execution summary with accurate timing and token metrics:

### 1. Record Metrics During Execution

**For each stage (quality, analysis, spec):**
```python
import time

# At stage start
stage_start = time.time()

# [Invoke skill...]

# At stage end
stage_end = time.time()
duration_seconds = int(stage_end - stage_start)

# Track tokens (from tool outputs or model response metadata)
tokens_used = token_count_from_response()

# Store metrics
metrics["stages"]["quality"] = {
  "duration": duration_seconds,
  "tokens": tokens_used,
  "quality_score": 82,  # from skill output
  "gate_decision": "proceed"
}
```

### 2. Aggregate and Save Metrics

After all three stages complete:
```json
{
  "ticket_id": "12345",
  "ticket_title": "Feature title",
  "project_name": "ProjectName",
  "status": "completed",
  "timestamp": "2026-07-16T14:30:00Z",
  "stages": {
    "quality": {"duration": 18, "tokens": 2840, "quality_score": 82, "gate_decision": "proceed"},
    "analysis": {"duration": 45, "tokens": 8920},
    "spec": {"duration": 32, "tokens": 5240}
  }
}
```

### 3. Generate and Save the Summary File

Call the Python script to generate the markdown summary:
```bash
python skills/spec-driven-development-orchestrator/execution_summary_generator.py metrics.json documents/
```

This produces: `documents/execution-summary-{ticket_id}.md` with:
- ✅ Execution timeline table (duration & tokens per stage)
- ✅ Total execution time
- ✅ Total tokens consumed
- ✅ Token percentage breakdown
- ✅ Cost estimation
- ✅ Per-stage efficiency metrics

**WITHOUT THIS STEP:** The execution summary will be generated but metrics will show as placeholders `{total_duration}`, `{total_tokens}`, etc.

---

## Configuration

The orchestrator respects the same configuration as `azure-devops-ticket-quality`:

### Default Project (Optional)

Configure a default Azure DevOps project in `.claude/settings.json` to avoid specifying the project each time:

```json
{
  "azureDevOpsTicketQuality": {
    "defaultProject": "your-project-name"
  }
}
```

When configured, you can invoke the orchestrator with just the work item ID:
- "Generate spec for ticket 12345"

The default project applies to all three stages (quality assessment, solution analysis, spec generation).

## Error Handling

The orchestrator handles these failure cases gracefully:

1. **Work item not found**
   - The MCP call to fetch the ticket fails
   - Surface the error to the user and ask them to verify the work item ID and project

2. **Ticket too weak to build from (quality score < 70)**
   - Show the quality report
   - Ask user to confirm they want to proceed
   - Don't silently push a vague ticket downstream

3. **Solution analysis skill unavailable**
   - The orchestrator attempts to invoke `technical-solution-analysis`
   - If the skill isn't loaded/available, say so explicitly
   - Don't fabricate an analysis or skip the stage

4. **Technical spec generation fails**
   - If the spec generator runs but produces no output, surface that to the user
   - Ask whether to retry, check the ticket/analysis, or escalate

In all cases, the user sees the issue clearly rather than silent failures downstream.

## Tips for Best Results

1. **Start with a work item ID** — the orchestrator will pull the full ticket, including comments, attachments, and revision history (via the MCP calls)
2. **Use a configured default project** — set `azureDevOpsTicketQuality.defaultProject` in `.claude/settings.json` to skip repeating it each time
3. **Check the quality report first** — if it flags weaknesses, address them in the ticket before development. The report suggests specific follow-up questions to resolve gaps
4. **Review the solution analysis** — if you're unfamiliar with the codebase, use `documents/technical-solution-analysis.md` as a guide. It documents the stack, conventions, and existing risks
5. **Customize the spec** — the generated spec is a starting point. Developers and tech leads should review and refine it against team practices before committing to it

## Integration with Your Workflow

Run this orchestrator as part of your pre-sprint process:

1. **Backlog grooming** — Run the orchestrator on candidate tickets a day or two before sprint planning. Weak tickets surface early, giving you time to improve them
2. **Sprint commitment** — Before pulling a ticket into a sprint, ensure it has at least a quality score of 70. The orchestrator surfaces this immediately
3. **Onboarding** — For a developer new to the codebase, the spec + solution analysis pair is a complete onboarding document (what to build + how the system is structured)
4. **Architecture alignment** — If the solution analysis documents existing patterns and conventions, the generated spec automatically aligns new work to those patterns

---

## References

### Core Skill Documentation

- **Ticket Quality**: See `azure-devops-ticket-quality` skill documentation
- **Solution Analysis**: See `technical-solution-analysis` skill documentation  
- **Technical Spec**: See `technical-spec-generator` skill documentation
- **Pipeline Gating**: See `solution-analysis-gate` skill documentation

### Execution Examples & Templates

- **[EXECUTION-EXAMPLE.md](./EXECUTION-EXAMPLE.md)** — Real example of a complete execution summary with metrics
  - Shows sample quality scores, token usage, timing
  - Demonstrates metric collection and reporting
  - Good reference for what a successful run looks like

- **[EXECUTION-SUMMARY-TEMPLATE.md](./EXECUTION-SUMMARY-TEMPLATE.md)** — Template for generating execution summaries
  - Fields to capture: timing, tokens, quality scores, risks
  - Format for presenting results to users
  - Troubleshooting section structure
