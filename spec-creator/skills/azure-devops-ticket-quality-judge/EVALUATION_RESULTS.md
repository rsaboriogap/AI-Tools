# Evaluation Results Persistence

The `azure-devops-ticket-quality-judge` skill automatically saves evaluation results to the `documents/` folder in both JSON and Markdown formats for tracking, auditing, and reference.

## Result Files

For each evaluation with `evaluation_id` of `eval-001`, the skill saves:

### 1. JSON Result
**File:** `documents/evaluation-eval-001.json`

Complete evaluation data in structured JSON format with all criteria, scores, evidence, and recommendations. Machine-readable and designed for:
- Integration with other tools
- Programmatic analysis
- Archiving and version control
- Batch processing
- API consumption

Example:
```json
{
  "evaluation_id": "eval-001",
  "passed": true,
  "overall_score": 85,
  "criteria": [...],
  "critical_failures": [],
  ...
}
```

### 2. Markdown Report
**File:** `documents/evaluation-eval-001.md`

Comprehensive human-readable markdown report with:
- **Status** — Pass/Fail with emoji indicators
- **Score & Confidence** — Overall metrics
- **Skill Definition** — Target skill info
- **Criteria Table** — All scores with weighted calculations
- **Deterministic Checks** — Summary of checks
- **Critical Failures** — If any, with full details
- **Missing Requirements** — Required but unmet items
- **Strengths** — What went well
- **Recommendations** — Prioritized improvements (High/Medium/Low)
- **Executive Summary** — Concise conclusion

Perfect for:
- Sharing with stakeholders
- Documentation
- Review and discussion
- Git tracking (human-friendly diffs)

## How It Works

1. **Evaluation Runs**: The skill evaluates an agent execution or skill
2. **JSON Generated**: Outputs the required JSON evaluation result
3. **Auto-Save Triggered**: The `evaluation_saver.py` script is invoked automatically
4. **Files Created**: Both JSON and markdown files are saved to `documents/`
5. **Confirmation**: Prints confirmation messages showing where results were saved

## Using the Results

**Track evaluation history:**
```bash
# List all evaluation results
ls documents/evaluation-*.json
ls documents/evaluation-*.md
```

**View the markdown report:**
```bash
# View in terminal
cat documents/evaluation-eval-001.md

# Open in editor/viewer
code documents/evaluation-eval-001.md
```

**Parse results programmatically:**
```python
import json
with open('documents/evaluation-eval-001.json') as f:
    results = json.load(f)
    
# Access evaluation results
print(f"Passed: {results['passed']}")
print(f"Score: {results['overall_score']}/100")
for criterion in results['criteria']:
    print(f"{criterion['name']}: {criterion['score']}/5")
```

**Compare evaluations:**
```bash
# Side-by-side comparison
diff documents/evaluation-eval-001.md documents/evaluation-eval-002.md
```

## Evaluation ID Naming

Choose meaningful evaluation IDs for easy tracking:
- `eval-skill-version-1` — for skill version comparisons
- `eval-agent-run-20260715` — for dated agent runs
- `eval-pr-123` — for pull request validation
- `eval-benchmark-baseline` — for benchmarking

The `evaluation_id` is used to construct the result filenames, so choose descriptive names.

## Integration

To view or process evaluation results programmatically:

```python
from pathlib import Path
import json

# Load all evaluations
for eval_file in Path("documents").glob("evaluation-*.json"):
    with open(eval_file) as f:
        result = json.load(f)
        print(f"Evaluation {result['evaluation_id']}: {'PASSED' if result['passed'] else 'FAILED'}")
```
