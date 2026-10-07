# Evaluation Input Package Structure

For the `azure-devops-ticket-quality-judge` skill to evaluate an execution, the input package must include these **mandatory sections**:

## 1. User Request ✅
**Status:** Present in eval-001.json

Defines what the user asked for:
- Task description
- Input parameters (ticket ID, work item type)
- Expected outputs (file paths, formats)
- Constraints

## 2. Skill Definition ✅
**Status:** Present in eval-001.json

Describes the skill being evaluated:
- Actor (role/persona)
- Goal
- Scoring criteria with weights
- Mandatory artifacts
- Required tools
- Specification details

## 3. Expected Behavior ✅
**Status:** Present in eval-001.json

Specifies what constitutes success:
- Required actions (what the agent must do)
- Scoring contract (formula, tolerance, weights)
- Required JSON properties
- Forbidden actions
- Success and failure conditions
- Deterministic checks

## 4. Execution Trace ❌ MISSING
**Status:** NOT in eval-001.json - **MUST BE ADDED**

Records what the agent actually did:
```json
{
  "execution_trace": {
    "skills_invoked": ["azure-devops-ticket-quality"],
    "tool_calls": [
      {
        "tool": "mcp__azure-devops__wit_get_work_item",
        "parameters": {
          "id": 791579,
          "expand": "all"
        },
        "result": {
          "id": 791579,
          "title": "...",
          "type": "Product Backlog Item",
          "state": "...",
          "fields": {...}
        },
        "timestamp": "2026-07-15T10:30:45Z",
        "success": true
      },
      {
        "tool": "mcp__azure-devops__wit_list_work_item_comments",
        "parameters": {
          "id": 791579
        },
        "result": [...],
        "success": true
      }
    ],
    "files_created": [
      "documents/ticket-quality-791579.json",
      "documents/ticket-quality-791579.md"
    ],
    "files_modified": [],
    "errors": [],
    "duration_seconds": 45,
    "token_usage": {
      "input": 2500,
      "output": 1200
    }
  }
}
```

**Must include:**
- `skills_invoked` — which skills were activated
- `tool_calls` — each tool call with parameters, result, and success status
- `files_created` — what artifacts were written
- `files_modified` — any changes made
- `errors` — any failures or warnings
- Timing/resource metrics

## 5. Agent Response ❌ MISSING
**Status:** NOT in eval-001.json - **MUST BE ADDED**

The final output returned to the user:
```json
{
  "agent_response": {
    "summary": "Quality assessment complete...",
    "quality_score": 72,
    "findings": {
      "strengths": [...],
      "weaknesses": [...],
      "red_flags": [...]
    },
    "artifacts_created": [
      "documents/ticket-quality-791579.md",
      "documents/ticket-quality-791579.json"
    ],
    "text_output": "Full text response shown to user..."
  }
}
```

**Must include:**
- Summary of what was accomplished
- Key findings
- Artifact locations
- Any error/warning messages
- Structured result data

## 6. Deterministic Checks (Optional)
**Status:** Not in eval-001.json - **OPTIONAL BUT RECOMMENDED**

Pre-computed validation results:
```json
{
  "deterministic_checks": [
    {
      "name": "ticket_fetched_with_relations",
      "passed": true,
      "evidence": {
        "tool_called": "mcp__azure-devops__wit_get_work_item",
        "expand_parameter": "all"
      }
    },
    {
      "name": "markdown_report_exists",
      "passed": true,
      "evidence": {
        "path": "documents/ticket-quality-791579.md",
        "size_bytes": 2840
      }
    }
  ]
}
```

---

## To Complete eval-001.json

Add these two sections:

### Option A: Minimal (Fast)
Add stubs that the judge will fill in during evaluation:
```json
{
  "execution_trace": null,
  "agent_response": null
}
```
The judge will note "missing execution evidence" and reduce confidence.

### Option B: Complete (Recommended)
Capture actual execution:
1. Run the skill against ticket 791579
2. Record all tool calls and results
3. Capture the agent's response
4. Add both to eval-001.json
5. Run the judge to evaluate

Example: After running `/azure-devops-ticket-quality` with ticket 791579:
```bash
# eval-001-execution.json contains the tool calls and outputs
# eval-001-response.md contains the agent's final response text
# Merge into eval-001.json
```

---

## Validation

After adding execution_trace and agent_response:

```bash
python3 skills/azure-devops-ticket-quality-judge/evaluation_saver.py eval-001.json
```

The judge will:
1. Verify all mandatory fields are present
2. Compare actual execution against expected behavior
3. Validate mathematical claims (e.g., overall_score calculation)
4. Report any discrepancies
5. Save `documents/evaluation-eval-001.md` and `documents/evaluation-eval-001.json`
