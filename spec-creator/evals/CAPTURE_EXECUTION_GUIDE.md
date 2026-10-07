# How to Capture Execution Data for eval-001.json

This guide shows how to capture real execution data when running the `azure-devops-ticket-quality` skill.

## Step 1: Prepare for Capture

Create a file to collect execution data:
```bash
touch evals/eval-001-capture.json
```

## Step 2: Run the Skill with Attention to Detail

When you invoke the skill:
```
/azure-devops-ticket-quality
Analyze work item 791579 in the Azure DevOps project.
```

**Watch for:**
- ✓ Skill activation message
- ✓ Each tool call (wit_get_work_item, wit_list_work_item_comments, etc.)
- ✓ Tool results (work item data, comments, etc.)
- ✓ Files created (documents/ticket-quality-791579.json, .md)
- ✓ Final response with findings

## Step 3: Record Tool Calls

For each MCP tool call in the execution, record:

**Example 1: wit_get_work_item**
```json
{
  "tool": "mcp__azure-devops__wit_get_work_item",
  "parameters": {
    "id": 791579,
    "expand": "all"
  },
  "result": {
    "id": 791579,
    "revision": 12,
    "fields": {
      "System.Title": "[Title from work item]",
      "System.State": "[State]",
      "System.Description": "[Description]",
      "Microsoft.VSTS.Common.AcceptanceCriteria": "[AC if any]",
      "[other fields...]": "..."
    },
    "relations": [
      {
        "rel": "System.LinkTypes.Duplicate",
        "url": "[if any duplicates]"
      }
    ]
  },
  "success": true,
  "duration_ms": 1200
}
```

**Example 2: wit_list_work_item_comments**
```json
{
  "tool": "mcp__azure-devops__wit_list_work_item_comments",
  "parameters": {
    "id": 791579
  },
  "result": [
    {
      "id": 1,
      "author": "[Author name]",
      "content": "[Comment text]",
      "created_date": "2026-07-15T10:30:45Z"
    }
  ],
  "success": true,
  "duration_ms": 450
}
```

## Step 4: Record Files Created

Document what files the skill created:
```json
{
  "files_created": [
    {
      "path": "documents/ticket-quality-791579.json",
      "size_bytes": 2840,
      "created_timestamp": "2026-07-15T10:35:20Z",
      "content_hash": "sha256:abc123..."
    },
    {
      "path": "documents/ticket-quality-791579.md",
      "size_bytes": 5120,
      "created_timestamp": "2026-07-15T10:35:21Z",
      "content_hash": "sha256:def456..."
    }
  ]
}
```

## Step 5: Capture Agent Response

Record the final response from the skill:

```json
{
  "agent_response": {
    "text_output": "[Full text of what the agent said to the user]",
    "structured_result": {
      "ticket_id": 791579,
      "ticket_title": "[Title]",
      "overall_score": 72,
      "criteria": {
        "Clarity": {
          "score": 18,
          "weight": 20,
          "weighted_score": 3.6
        },
        "Acceptance Criteria": {
          "score": 15,
          "weight": 20,
          "weighted_score": 3.0
        },
        "Business Context": {
          "score": 8,
          "weight": 10,
          "weighted_score": 0.8
        },
        "[... other criteria ...]": "..."
      },
      "strengths": [
        "[Strength 1]",
        "[Strength 2]"
      ],
      "weaknesses": [
        "[Weakness 1]",
        "[Weakness 2]"
      ],
      "red_flags": [
        "[Red flag 1]"
      ],
      "suggested_questions": [
        "[Question 1]",
        "[Question 2]"
      ],
      "recommendations": [
        "[Recommendation 1]",
        "[Recommendation 2]"
      ]
    },
    "artifacts_created": [
      "documents/ticket-quality-791579.json",
      "documents/ticket-quality-791579.md"
    ]
  }
}
```

## Step 6: Merge into eval-001.json

Once you have all the data, merge it into eval-001.json:

```bash
# Backup original
cp evals/eval-001.json evals/eval-001.json.bak

# Use a script or manually add:
# - execution_trace (from step 3-4)
# - agent_response (from step 5)
```

**Manual merge structure:**
```json
{
  "evaluation_id": "azure-devops-ticket-quality-001",
  "evaluation_mode": "pointwise",
  "user_request": { ... },
  "skill_definition": { ... },
  "expected_behavior": { ... },
  "execution_trace": {
    "skills_invoked": ["azure-devops-ticket-quality"],
    "tool_calls": [
      { ... tool call 1 ... },
      { ... tool call 2 ... }
    ],
    "files_created": [
      { ... file 1 ... }
    ],
    "errors": [],
    "duration_seconds": 45
  },
  "agent_response": {
    "text_output": "...",
    "structured_result": { ... },
    "artifacts_created": [...]
  }
}
```

## Step 7: Validate with Judge

Run the judge to verify the execution:

```bash
/azure-devops-ticket-quality-judge evals/eval-001.json
```

The judge will:
1. Load all sections ✓
2. Compare actual execution vs. expected behavior
3. Validate scoring calculations
4. Report any discrepancies
5. Save evaluation report to `documents/evaluation-azure-devops-ticket-quality-001.md`

## Shortcut: Minimal Valid Execution

If you don't have all the details, create a minimal valid execution:

```json
{
  "execution_trace": {
    "skills_invoked": ["azure-devops-ticket-quality"],
    "tool_calls": [
      {
        "tool": "mcp__azure-devops__wit_get_work_item",
        "parameters": {"id": 791579, "expand": "all"},
        "result": {"id": 791579, "fields": {}},
        "success": true
      }
    ],
    "files_created": [
      {"path": "documents/ticket-quality-791579.json"},
      {"path": "documents/ticket-quality-791579.md"}
    ],
    "errors": []
  },
  "agent_response": {
    "text_output": "[Agent's response text]",
    "artifacts_created": [
      "documents/ticket-quality-791579.json",
      "documents/ticket-quality-791579.md"
    ]
  }
}
```

The judge will validate what's present and report what's missing or incomplete.

## References

- `SKILL.md` — Judge skill specification and required fields
- `EVAL_TEMPLATE.md` — Detailed structure of each field
- `EVAL_001_COMPLETION_CHECKLIST.md` — Checklist and next steps
