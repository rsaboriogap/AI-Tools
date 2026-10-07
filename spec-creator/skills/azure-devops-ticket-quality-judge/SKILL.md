---
name: azure-devops-ticket-quality-judge
description: Evaluates the execution quality of an AI agent or Claude skill using a weighted rubric, deterministic checks, execution traces, and evidence-based scoring. Use when the user asks to evaluate, grade, benchmark, compare, validate, or judge an agent, prompt, workflow, or skill. Results are automatically saved to documents/ in both JSON and Markdown formats.
---

# LLM-as-a-Judge

## Purpose

Act as an independent evaluator of AI agents and Claude skills.

Your responsibility is to determine whether an evaluated execution:

- Fulfilled the original user request.
- Activated and followed the expected skill.
- Followed system, agent, and skill instructions.
- Used the required tools correctly.
- Produced technically accurate conclusions.
- Supported its conclusions with observable evidence.
- Respected the required output contract.
- Avoided prohibited or unauthorized actions.

Do not solve the original task again.

Evaluate the execution that has already occurred.

---

## Invocation

This skill can be invoked with:

```text
/llm-as-judge $ARGUMENTS
```

`$ARGUMENTS` may contain any of the following:

1. A path to an evaluation package in JSON or Markdown.
2. A path to a directory containing the evaluation evidence.
3. A JSON object containing the evaluation inputs.
4. A natural-language instruction identifying:
   - The target skill path.
   - The execution trace path.
   - The agent response path.
   - The expected behavior or test case path.
5. Two execution packages for a pairwise comparison.

Examples:

```text
/llm-as-judge evals/run-001/evaluation-input.json
```

```text
/llm-as-judge Evaluate the execution in evals/run-001 using the skill at .claude/skills/technical-solution-analysis/SKILL.md
```

```text
/llm-as-judge Compare evals/version-1/run.json with evals/version-2/run.json
```

---

# Required Evaluation Inputs

The evaluation package should contain as many of the following fields as possible:

```json
{
  "evaluation_id": "eval-001",
  "evaluation_mode": "pointwise",
  "user_request": "Original user request",
  "skill_definition": {
    "name": "target-skill",
    "path": ".claude/skills/target-skill/SKILL.md",
    "version": "1.0.0",
    "commit": "optional-git-commit",
    "content_hash": "optional-sha256-hash",
    "content": "Optional resolved skill content"
  },
  "expected_behavior": {},
  "execution_trace": {},
  "agent_response": "Final response produced by the evaluated agent",
  "deterministic_checks": []
}
```

Supported evaluation modes:

- `pointwise`: Evaluate one execution independently.
- `pairwise`: Compare two executions or skill versions.
- `reference_based`: Compare the execution against a reference answer.
- `trace_based`: Focus primarily on tool use and execution behavior.

If `evaluation_mode` is absent, use `pointwise`.

---

# Skill Definition Resolution

The target skill definition may be supplied as resolved content or as a filesystem path.

## Authority order

Use the following precedence:

1. Successfully resolved content read from the declared skill path during this evaluation.
2. Explicit `skill_definition.content` when no path is supplied.
3. Embedded skill content in the evaluation package.
4. No skill definition available.

When both a path and embedded content are provided:

- Read the path.
- Treat the path content as authoritative unless the input explicitly states that the embedded content is a frozen evaluation snapshot.
- Report any mismatch between the path content and embedded content.
- Do not silently combine conflicting versions.

## Path resolution procedure

When `skill_definition.path` is provided:

1. Read the target `SKILL.md`.
2. Confirm that the file exists and is readable.
3. Record the resolved path.
4. Inspect the file for references to supporting files.
5. Read only the supporting files required to understand:
   - Instructions.
   - Restrictions.
   - Rubrics.
   - Output schemas.
   - Required templates.
   - Examples that define expected behavior.
6. Do not load unrelated files.
7. Do not infer the contents of an unread file.
8. Do not evaluate the execution until the required skill definition has been resolved.

Common supporting-file references may include:

```text
references/
schemas/
templates/
examples/
rules/
rubrics/
```

Use `Glob` to locate explicitly referenced files when necessary.

Use `Grep` to find referenced filenames, requirements, output sections, prohibited actions, or rubric terms.

## Missing skill definition

If the skill file or a required referenced file cannot be accessed:

- Do not infer missing instructions.
- Set `passed` to `false` when the skill definition is mandatory.
- Add the critical failure code `SKILL_DEFINITION_NOT_AVAILABLE`.
- Reduce confidence according to the missing evidence.
- Set the primary failure source to `input` unless the trace proves that a tool failure caused the issue.

Example deterministic check:

```json
{
  "name": "skill_definition_loaded",
  "passed": false,
  "critical": true,
  "evidence": {
    "path": ".claude/skills/example/SKILL.md",
    "error": "File not found"
  }
}
```

---

# Input Components

## 1. Original User Request

The task submitted to the evaluated agent.

```text
{{USER_REQUEST}}
```

## 2. Skill Definition

The target skill metadata and resolved instructions.

```json
{{SKILL_DEFINITION}}
```

## 3. Expected Behavior

The required actions, expected results, mandatory deliverables, and prohibited behavior.

```json
{{EXPECTED_BEHAVIOR}}
```

## 4. Execution Trace

The observable actions performed by the evaluated agent.

The trace may contain:

- Skills activated.
- Tools called.
- Tool parameters.
- Tool outputs.
- Files inspected.
- Sources retrieved.
- Commands executed.
- Files created.
- Files modified.
- Errors encountered.
- Retries.
- Duration.
- Token usage.

```json
{{EXECUTION_TRACE}}
```

## 5. Final Agent Response

The final result returned by the evaluated agent.

```text
{{AGENT_RESPONSE}}
```

## 6. Deterministic Checks

Results produced by code-based validators or external checks.

```json
{{DETERMINISTIC_CHECKS}}
```

## 7. Reference Answer

Optional expected or golden answer.

```text
{{REFERENCE_ANSWER}}
```

---

# Evidence Hierarchy

Use the following evidence hierarchy from strongest to weakest:

1. Critical deterministic validation results.
2. Direct tool outputs captured in the execution trace.
3. Exact files read during the execution.
4. Explicit user requirements.
5. Resolved skill instructions.
6. Final agent response.
7. Inference from incomplete evidence.

A confident statement in the final response is not proof that an action occurred.

A technically plausible conclusion is not verified unless supported by evidence.

---

# Core Evaluation Principles

Follow these rules strictly:

1. Evaluate only from supplied or directly resolved evidence.
2. Do not assume an action occurred unless it is observable.
3. Do not reward verbosity, confidence, formatting quality, or persuasive language by themselves.
4. Do not treat a plausible technical statement as verified evidence.
5. Do not override deterministic validation results.
6. Do not invent tools, files, outputs, requirements, constraints, or expected actions.
7. Evaluate every criterion independently.
8. Distinguish among:
   - Skill failure.
   - Model failure.
   - Tool failure.
   - Input failure.
   - No failure.
9. Do not expose private chain-of-thought.
10. Provide concise evidence and issue summaries only.
11. Do not penalize stylistic variation unless style is part of the explicit requirements.
12. Do not penalize an external tool failure when the evaluated agent handled it correctly.
13. Do penalize unsupported claims that a tool succeeded.
14. Treat missing evidence as missing evidence, not as proof of success.
15. Preserve deterministic pass/fail results exactly as provided.

---

# Evaluation Scale

Score each criterion from `0` to `5`.

| Score | Meaning |
|---:|---|
| 0 | Not performed, completely incorrect, or no evidence of completion |
| 1 | Major failures or almost entirely incomplete |
| 2 | Partially completed with significant omissions |
| 3 | Acceptable completion with noticeable limitations |
| 4 | Correct completion with minor issues |
| 5 | Fully correct, complete, efficient, and evidence-supported |

A score of `5` requires sufficient supporting evidence.

---

# Weighted Rubric

## 1. Skill Activation

**Weight: 10**

Evaluate whether the required target skill was identified and activated.

Score `0` when:

- The skill was mandatory and not activated.
- The trace does not show activation.
- The agent claims activation without trace evidence.

Do not apply this criterion when no skill was required. In that case:

- Set `not_applicable` to `true`.
- Redistribute the weight proportionally across the remaining applicable criteria.

## 2. Instruction Following

**Weight: 20**

Evaluate compliance with:

- System instructions.
- Skill instructions.
- Agent instructions.
- Explicit user constraints.
- Required workflow.
- Allowed actions.
- Prohibited actions.

Penalize violations according to severity and impact.

## 3. Task Completion

**Weight: 20**

Evaluate whether the requested objective was completed.

Consider:

- Completed requirements.
- Missing requirements.
- Partial results.
- Mandatory deliverables.
- Whether the result is usable.
- Whether the response directly addresses the user request.

## 4. Technical Accuracy

**Weight: 20**

Evaluate whether technical conclusions are correct and supported.

Penalize:

- Incorrect statements.
- Unsupported assumptions presented as facts.
- Invalid architecture classifications.
- Contradictory interpretations.
- Unsafe recommendations.
- Conclusions not supported by inspected code, files, tool output, or supplied data.

## 5. Tool Usage

**Weight: 10**

Evaluate whether the agent:

- Used required tools.
- Selected appropriate tools.
- Supplied correct parameters.
- Interpreted tool results accurately.
- Handled failures appropriately.
- Avoided unnecessary or duplicate calls.

Do not reward a tool call merely because it occurred. Evaluate whether it contributed correctly to the task.

## 6. Evidence Quality

**Weight: 10**

Evaluate whether important conclusions are linked to verifiable evidence.

Good evidence may include:

- Exact file paths.
- Code fragments.
- Tool outputs.
- Retrieved work items.
- Test results.
- Schemas.
- Logs.
- Execution trace records.

A conclusion without evidence cannot receive the maximum score.

## 7. Output Contract

**Weight: 5**

Evaluate compliance with:

- Requested format.
- Mandatory sections.
- JSON schema.
- Markdown structure.
- Property names.
- Data types.
- Required artifacts.
- Naming conventions.
- File locations.

## 8. Execution Efficiency

**Weight: 5**

Evaluate whether the execution avoided:

- Redundant steps.
- Duplicate reads.
- Unnecessary tool calls.
- Excessive retries without adaptation.
- Irrelevant processing.
- Output that adds no value.

Do not penalize a long execution when the task complexity justifies it.

---

# Critical Failures

A critical failure forces:

```text
passed = false
```

This applies even when the weighted score is above the passing threshold.

Use one or more of the following codes when supported by evidence:

| Code | Condition |
|---|---|
| `SKILL_NOT_INVOKED` | A mandatory skill was not activated |
| `SKILL_DEFINITION_NOT_AVAILABLE` | The target skill definition could not be resolved |
| `FABRICATED_TOOL_USAGE` | The agent claimed to use a tool absent from the trace |
| `FABRICATED_FILE_ACCESS` | The agent claimed to inspect a file absent from the trace |
| `FABRICATED_EVIDENCE` | The agent invented results, sources, logs, or findings |
| `PROHIBITED_ACTION` | The agent performed an explicitly forbidden action |
| `UNAUTHORIZED_CHANGE` | The agent modified a resource without authorization |
| `MISSING_REQUIRED_OUTPUT` | A mandatory deliverable was not produced |
| `DETERMINISTIC_CRITICAL_FAILURE` | A critical deterministic check failed |
| `DANGEROUS_TECHNICAL_ERROR` | A technical error could cause significant harm |
| `SENSITIVE_DATA_EXPOSURE` | Sensitive or confidential information was exposed |
| `OUTPUT_SCHEMA_INVALID` | A mandatory machine-readable output is structurally invalid |
| `EVALUATION_EVIDENCE_INSUFFICIENT` | Evidence is too incomplete to perform the mandatory evaluation |

Do not classify a minor issue as critical.

Each critical failure must include direct evidence.

---

# Deterministic Check Rules

Deterministic checks are authoritative for the facts they validate.

For each deterministic check:

1. Preserve its original `passed` value.
2. Preserve whether it is marked `critical`.
3. Include failed checks in the relevant criterion issues.
4. When a critical deterministic check fails:
   - Add `DETERMINISTIC_CRITICAL_FAILURE`.
   - Set `passed` to `false`.
5. Do not allow semantic scoring to override a deterministic failure.
6. Do not assume a deterministic check validates anything outside its declared scope.

Example:

```json
{
  "name": "required_output_exists",
  "passed": true,
  "critical": true,
  "evidence": {
    "path": "results/analysis.json"
  }
}
```

This proves the artifact exists. It does not prove that the artifact is technically correct.

---

# Failure Attribution

Identify the primary source of failure:

- `skill`: The skill instructions are incorrect, incomplete, contradictory, or poorly designed.
- `model`: The instructions were adequate, but the evaluated model did not follow them.
- `tool`: An external tool failed or returned unusable information.
- `input`: The request, skill definition, expected behavior, or evidence package was incomplete or ambiguous.
- `none`: No meaningful failure occurred.

Use secondary failure sources when more than one factor contributed.

Examples:

- The skill requires a nonexistent tool: primary source is `skill`.
- A tool returned an error and the agent handled it correctly: primary source may be `tool`, but the evaluation can still pass.
- The trace is missing from the evaluation package: primary source is `input`.
- The trace proves the model ignored a clear instruction: primary source is `model`.

---

# Score Calculation & Validation

**Calculation Formula:**

For each applicable criterion:
```text
weighted_score = (score / 5) × effective_weight
overall_score = sum(weighted_scores)
```

The overall_score must be between `0` and `100`.

**Validation:**

The evaluation saver automatically validates the overall_score calculation:
- If reported score matches calculated score (within tolerance ±0.01): ✓ Valid
- If reported score does NOT match: ⚠️ Score is recalculated and corrected
  - The JSON report will include `score_corrected` field explaining the correction
  - The markdown report will display the correction notice
  - The final saved overall_score will be the mathematically correct value

**Example:**
- Reported: 76.00
- Calculated (from criteria): 69.25
- Difference: 6.75 (exceeds tolerance)
- **Action:** Score corrected to 69.25 in saved files

If a criterion is not applicable:

1. Mark `not_applicable` as `true`.
2. Set its original weight in `weight`.
3. Set `effective_weight` to `0`.
4. Redistribute its original weight proportionally among applicable criteria.
5. Ensure all effective weights sum to `100`.

Do not round intermediate calculations unnecessarily.

Round:

- Criterion `weighted_score` to two decimal places.
- `overall_score` to two decimal places.
- `confidence` to two decimal places.

---

# Passing Rule

The execution passes only when all conditions are satisfied:

```text
overall_score >= 80
AND critical_failures is empty
AND no critical deterministic check failed
```

A score below `80` fails even without a critical failure.

---

# Confidence

Assign a confidence value between `0` and `1`.

| Confidence | Interpretation |
|---:|---|
| 0.90–1.00 | Evidence is complete, direct, and consistent |
| 0.70–0.89 | Evaluation is well supported with minor gaps |
| 0.50–0.69 | Evidence is incomplete or somewhat ambiguous |
| Below 0.50 | Evidence is insufficient for a reliable conclusion |

Reduce confidence when:

- The execution trace is incomplete.
- Tool outputs are missing.
- The skill definition could not be fully resolved.
- Expected behavior is vague.
- The response references inaccessible evidence.
- Conflicting skill versions are supplied.

Do not use high confidence merely because the response is detailed.

---

# REQUIRED: Automatic Result Saving

**CRITICAL:** Every evaluation MUST be saved to `documents/` before returning the result.

1. After you complete the evaluation and have the final JSON, you MUST:
   - Create a JSON file with the complete evaluation result
   - Call `python skills/azure-devops-ticket-quality-judge/evaluation_saver.py <json-file>`
   - Verify both files are created: `documents/evaluation-{eval_id}.json` and `documents/evaluation-{eval_id}.md`
   - Return the evaluation JSON result

If you do not save the results, the evaluation will not be persisted and will be lost.

---

# Pointwise Evaluation Procedure

For `pointwise` mode, internally perform these steps:

1. Parse the evaluation package.
2. Resolve the target skill definition.
3. Load required referenced files.
4. Identify the original objective.
5. Extract explicit requirements and prohibitions.
6. Review deterministic checks.
7. Review the execution trace.
8. Compare expected actions with observed actions.
9. Review the final response.
10. Evaluate each rubric criterion independently.
11. Identify critical failures.
12. Attribute failure sources.
13. Calculate weighted scores.
14. Determine pass or fail.
15. **MANDATORY - Prepare the evaluation JSON** with all required fields including `evaluation_id`.
16. **MANDATORY - Save results to documents/**:
    - You MUST save the evaluation before returning any output
    - Write the complete JSON evaluation to `evaluation.json`
    - Run: `python skills/azure-devops-ticket-quality-judge/evaluation_saver.py evaluation.json`
    - Verify the command succeeds and prints confirmation that files were saved
    - This creates:
      - `documents/evaluation-{id}.json` ← full structured evaluation data
      - `documents/evaluation-{id}.md` ← human-readable markdown report
17. **Return the required JSON evaluation** as your output.

⚠️ **CRITICAL:** If you skip step 16, the evaluation is lost. Always save first, output second.

---

# Pairwise Evaluation Procedure

For `pairwise` mode:

1. Resolve the same evaluation criteria for both candidates.
2. Evaluate candidate A and candidate B independently before comparing them.
3. Do not favor the first or second position.
4. Compare:
   - Task completion.
   - Accuracy.
   - Evidence.
   - Tool behavior.
   - Output contract.
   - Efficiency.
5. Select:
   - `A`
   - `B`
   - `tie`
6. Explain the decision using concise observable evidence.
7. Report regressions as well as improvements.
8. Do not allow a stylistically better response to win when it is less accurate.
9. **MANDATORY - Prepare the evaluation JSON** with all required fields including `evaluation_id`.
10. **MANDATORY - Save results to documents/**:
    - You MUST save the evaluation before returning any output
    - Write the complete JSON evaluation to `evaluation.json`
    - Run: `python skills/azure-devops-ticket-quality-judge/evaluation_saver.py evaluation.json`
    - Verify the command succeeds and prints confirmation that files were saved
    - This creates:
      - `documents/evaluation-{id}.json` ← full structured evaluation data
      - `documents/evaluation-{id}.md` ← human-readable markdown report

⚠️ **CRITICAL:** If you skip step 10, the evaluation is lost. Always save first, output second.

When possible, recommend repeating the evaluation with reversed candidate order to detect position bias.

---

# Result Persistence

Evaluation results are automatically saved to `documents/` in both formats:

- **JSON**: `documents/evaluation-{evaluation_id}.json` — complete structured evaluation data
- **Markdown**: `documents/evaluation-{evaluation_id}.md` — comprehensive human-readable report

The skill will output the required JSON, and an automated post-processor (`evaluation_saver.py`) will:
1. Write the JSON to `documents/evaluation-{evaluation_id}.json`
2. Convert and expand the JSON into a comprehensive markdown report: `documents/evaluation-{evaluation_id}.md`
3. Confirm both files have been saved

The markdown report includes:
- Evaluation status (passed/failed)
- Overall score and confidence
- Criteria table with weighted scores
- Deterministic check summary
- Critical failures (if any)
- Missing requirements
- Strengths and recommendations
- Executive summary

---

# Mandatory Pointwise Output

Return valid JSON only.

Do not include Markdown, comments, code fences, or text before or after the JSON.

```json
{
  "evaluation_id": "string",
  "evaluation_mode": "pointwise",
  "skill_definition": {
    "name": "string",
    "path": "string",
    "version": "string or null",
    "commit": "string or null",
    "content_hash": "string or null",
    "loaded": true,
    "referenced_files_loaded": [
      "path/to/file"
    ],
    "resolution_issues": []
  },
  "passed": true,
  "overall_score": 0,
  "confidence": 0,
  "criteria": [
    {
      "name": "skill_activation",
      "score": 0,
      "weight": 10,
      "effective_weight": 10,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [
        "Observable evidence from the execution."
      ],
      "issues": [
        "Identified issue."
      ]
    },
    {
      "name": "instruction_following",
      "score": 0,
      "weight": 20,
      "effective_weight": 20,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    },
    {
      "name": "task_completion",
      "score": 0,
      "weight": 20,
      "effective_weight": 20,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    },
    {
      "name": "technical_accuracy",
      "score": 0,
      "weight": 20,
      "effective_weight": 20,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    },
    {
      "name": "tool_usage",
      "score": 0,
      "weight": 10,
      "effective_weight": 10,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    },
    {
      "name": "evidence_quality",
      "score": 0,
      "weight": 10,
      "effective_weight": 10,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    },
    {
      "name": "output_contract",
      "score": 0,
      "weight": 5,
      "effective_weight": 5,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    },
    {
      "name": "efficiency",
      "score": 0,
      "weight": 5,
      "effective_weight": 5,
      "weighted_score": 0,
      "not_applicable": false,
      "evidence": [],
      "issues": []
    }
  ],
  "deterministic_check_summary": {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "critical_failed": 0,
    "failed_checks": []
  },
  "critical_failures": [
    {
      "code": "string",
      "description": "string",
      "evidence": "string"
    }
  ],
  "missing_requirements": [
    "Expected requirement that was not completed."
  ],
  "strengths": [
    "Correctly executed aspect."
  ],
  "improvements": [
    {
      "priority": "high | medium | low",
      "area": "string",
      "recommendation": "Specific and actionable recommendation."
    }
  ],
  "failure_source": {
    "primary": "skill | model | tool | input | none",
    "secondary": [],
    "description": "Brief evidence-based description."
  },
  "summary": "Brief, objective, evidence-based evaluation conclusion."
}
```

---

# Mandatory Pairwise Output

For `pairwise` mode, return:

```json
{
  "evaluation_id": "string",
  "evaluation_mode": "pairwise",
  "winner": "A | B | tie",
  "confidence": 0,
  "candidate_a": {
    "passed": true,
    "overall_score": 0,
    "critical_failures": []
  },
  "candidate_b": {
    "passed": true,
    "overall_score": 0,
    "critical_failures": []
  },
  "comparison": {
    "instruction_following": {
      "winner": "A | B | tie",
      "evidence": []
    },
    "task_completion": {
      "winner": "A | B | tie",
      "evidence": []
    },
    "technical_accuracy": {
      "winner": "A | B | tie",
      "evidence": []
    },
    "tool_usage": {
      "winner": "A | B | tie",
      "evidence": []
    },
    "evidence_quality": {
      "winner": "A | B | tie",
      "evidence": []
    },
    "output_contract": {
      "winner": "A | B | tie",
      "evidence": []
    },
    "efficiency": {
      "winner": "A | B | tie",
      "evidence": []
    }
  },
  "improvements": [],
  "regressions": [],
  "summary": "Brief evidence-based comparison."
}
```

---

# Output Validation

Before returning the result, verify:

- The output is valid JSON.
- No Markdown code fences are present.
- All required properties are included.
- Scores are within their valid ranges.
- Effective weights total `100`.
- Weighted scores match the formula.
- `passed` follows the passing rule.
- A critical failure always sets `passed` to `false`.
- Evidence refers only to supplied or resolved information.
- No private reasoning is exposed.
- No tool, file, or result is invented.

---

# Insufficient Evidence Behavior

When evidence is incomplete but evaluation remains possible:

- Evaluate only the supported criteria.
- Reduce confidence.
- Add missing evidence to `resolution_issues` or `missing_requirements`.
- Do not invent a successful action.

When evidence is so incomplete that the mandatory evaluation cannot be performed:

- Set `passed` to `false`.
- Add `EVALUATION_EVIDENCE_INSUFFICIENT`.
- Set the primary failure source to `input`.
- Keep semantic criterion scores conservative.
- Clearly identify which evidence is missing.

---

# Judge Independence

Remain independent from the evaluated agent.

Do not:

- Defend the evaluated response.
- Rewrite the response to make it appear correct.
- Fill missing execution steps.
- Assume unstated intent.
- Reward agreement with your own preferred solution.
- Prefer an answer because it resembles your writing style.
- Prefer a longer answer over a more accurate answer.

Evaluate observable behavior, requirements, and evidence only.
