# eval-001.json Completion Checklist

## Current Status

**eval-001.json** is a test case for the `azure-devops-ticket-quality` skill.

It defines:
- ✅ `evaluation_id` — "azure-devops-ticket-quality-001"
- ✅ `evaluation_mode` — "pointwise"
- ✅ `user_request` — Analyze work item 791579 (Product Backlog Item)
- ✅ `skill_definition` — Full spec of the azure-devops-ticket-quality skill
- ✅ `expected_behavior` — 22+ required actions, scoring contract, success conditions, deterministic checks

**Missing - REQUIRED for the judge to evaluate:**
- ❌ `execution_trace` — Observable record of what the skill actually did
- ❌ `agent_response` — Final output/response returned to the user

---

## What execution_trace Must Contain

The judge needs to see what the agent actually did:

```
├── skills_invoked
│   └── ["azure-devops-ticket-quality"]
│
├── tool_calls
│   ├── mcp__azure-devops__wit_get_work_item(id=791579, expand="all")
│   │   └── Result: Full work item with fields and relations
│   ├── mcp__azure-devops__wit_list_work_item_comments(id=791579)
│   │   └── Result: Comment thread (if any)
│   ├── mcp__azure-devops__wit_list_work_item_revisions(id=791579)
│   │   └── Result: Revision history
│   ├── mcp__azure-devops__wit_get_work_item_type(type_name="Bug")
│   │   └── Result: Field schema
│   └── [any other tool calls...]
│
├── files_created
│   ├── "documents/ticket-quality-791579.json"
│   └── "documents/ticket-quality-791579.md"
│
├── files_modified
│   └── [] (should be empty - no writes allowed)
│
├── errors
│   └── [] (should be empty if successful)
│
└── timing
    ├── duration_seconds: 45
    └── token_usage: {input: 2500, output: 1200}
```

---

## What agent_response Must Contain

The judge needs to see what the agent returned to the user:

```
{
  "text_output": "[The full text response from the agent...]",
  "structured_result": {
    "ticket_id": 791579,
    "ticket_title": "[Title from work item]",
    "overall_score": 72,
    "criteria": {
      "Clarity": {score: 18, weight: 20, weighted_score: 3.6},
      "Acceptance Criteria": {score: 15, weight: 20, weighted_score: 3.0},
      ...
    },
    "strengths": ["..."],
    "weaknesses": ["..."],
    "red_flags": ["..."],
    "suggested_questions": ["..."],
    "recommendations": ["..."]
  },
  "artifacts_created": [
    "documents/ticket-quality-791579.json",
    "documents/ticket-quality-791579.md"
  ]
}
```

---

## How to Collect These

### Option 1: Manual Capture
1. **Run the skill:**
   ```
   /azure-devops-ticket-quality
   [Analyze work item 791579]
   ```

2. **In Claude Code, record:**
   - All tool calls shown in the execution trace
   - All tool results
   - Files created/modified
   - Any errors

3. **From the agent response:**
   - Copy the final response text
   - Extract the JSON output
   - Note artifacts created

4. **Add to eval-001.json:**
   ```json
   {
     ...existing fields...,
     "execution_trace": {
       "skills_invoked": [...],
       "tool_calls": [...]
     },
     "agent_response": {
       "text_output": "...",
       "structured_result": {...}
     }
   }
   ```

### Option 2: Programmatic Capture
If Claude Code's transcript system is available:
```bash
# Extract execution trace from transcript
# Extract agent response from transcript
# Merge into eval-001.json
```

---

## Why These Fields Are Critical

The judge skill (`azure-devops-ticket-quality-judge`) cannot evaluate the execution without:

1. **execution_trace** — to verify:
   - ✓ The right skill was invoked
   - ✓ The right tools were called with correct parameters
   - ✓ Required artifacts were created
   - ✓ Forbidden actions (like posting comments) didn't happen
   - ✓ Tool results match expected data

2. **agent_response** — to verify:
   - ✓ The response contains the required findings
   - ✓ Scores are mathematically correct
   - ✓ Findings are specific (not generic)
   - ✓ Findings are evidence-based
   - ✓ Output format is correct

Without these, the judge can only:
- Check that expected_behavior was well-specified ✓
- Flag that actual execution is missing ✗
- Report evaluation incomplete

---

## Next Steps

1. **Decide:** Do you want to:
   - Complete eval-001.json with actual execution data? (recommended)
   - Keep it as a specification-only template?
   - Create a new eval-002.json with recorded execution?

2. **If completing:**
   - Run the skill against ticket 791579
   - Capture tool calls and results
   - Capture agent response
   - Add both to eval-001.json

3. **To validate:**
   ```bash
   /azure-devops-ticket-quality-judge evals/eval-001.json
   ```

   The judge will report:
   - Which fields are present/missing
   - Completeness of execution_trace and agent_response
   - Full evaluation if both present
