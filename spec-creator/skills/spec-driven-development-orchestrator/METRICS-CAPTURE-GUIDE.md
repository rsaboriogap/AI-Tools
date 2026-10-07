# Metric Capture Guide for Orchestrator

How to capture execution timing and token metrics so the execution summary includes real data.

## Quick Reference

**Goal:** Track how long each stage takes and how many tokens it consumes, then save that to a summary file.

**Three simple steps:**
1. Start a timer when each stage begins
2. Record tokens consumed by each stage
3. Save metrics to JSON and run the Python generator

---

## Step-by-Step Implementation

### Step 1: Initialize Metric Tracking

At the start of orchestrator execution:

```python
import time
import json
from datetime import datetime

# Initialize metrics structure
metrics = {
    "ticket_id": "12345",
    "ticket_title": "Your ticket title",
    "project_name": "YourProject",
    "status": "in_progress",
    "timestamp": datetime.now().isoformat(),
    "stages": {
        "quality": {"duration": 0, "tokens": 0},
        "analysis": {"duration": 0, "tokens": 0},
        "spec": {"duration": 0, "tokens": 0}
    }
}

# Variables to track
quality_start = None
analysis_start = None
spec_start = None
```

### Step 2: Record Stage 1 (Quality Assessment)

```python
# ============================================
# STAGE 1: Ticket Quality Assessment
# ============================================

quality_start = time.time()

# [Invoke azure-devops-ticket-quality skill...]
# quality_response = invoke_skill("azure-devops-ticket-quality", ticket_id)

quality_end = time.time()
quality_duration = int(quality_end - quality_start)
quality_tokens = 2840  # Extract from skill response or estimate
quality_score = 82     # Extract from quality report

# Store metrics
metrics["stages"]["quality"]["duration"] = quality_duration
metrics["stages"]["quality"]["tokens"] = quality_tokens
metrics["stages"]["quality"]["quality_score"] = quality_score
metrics["stages"]["quality"]["gate_decision"] = "proceed"  # or "review" / "block"

print(f"✅ Stage 1 complete: {quality_duration}s, {quality_tokens} tokens")
```

### Step 3: Record Stage 2 (Solution Analysis Gating)

```python
# ============================================
# STAGE 2: Solution Analysis Gating
# ============================================

analysis_start = time.time()

# [Invoke solution-analysis-gate skill...]
# analysis_response = invoke_skill("solution-analysis-gate", ticket_id)

analysis_end = time.time()
analysis_duration = int(analysis_end - analysis_start)
analysis_tokens = 8920  # Extract from skill response or estimate

# Store metrics
metrics["stages"]["analysis"]["duration"] = analysis_duration
metrics["stages"]["analysis"]["tokens"] = analysis_tokens

print(f"✅ Stage 2 complete: {analysis_duration}s, {analysis_tokens} tokens")
```

### Step 4: Record Stage 3 (Technical Spec Generation)

```python
# ============================================
# STAGE 3: Technical Spec Generation
# ============================================

spec_start = time.time()

# [Invoke technical-spec-generator skill...]
# spec_response = invoke_skill("technical-spec-generator", ticket_id)

spec_end = time.time()
spec_duration = int(spec_end - spec_start)
spec_tokens = 5240  # Extract from skill response or estimate

# Store metrics
metrics["stages"]["spec"]["duration"] = spec_duration
metrics["stages"]["spec"]["tokens"] = spec_tokens

print(f"✅ Stage 3 complete: {spec_duration}s, {spec_tokens} tokens")
```

### Step 5: Finalize and Save Metrics

```python
# ============================================
# FINALIZE & GENERATE SUMMARY
# ============================================

# Update status
metrics["status"] = "completed"  # or "blocked" / "failed"

# Calculate totals for reference
total_duration = (metrics["stages"]["quality"]["duration"] +
                  metrics["stages"]["analysis"]["duration"] +
                  metrics["stages"]["spec"]["duration"])
total_tokens = (metrics["stages"]["quality"]["tokens"] +
                metrics["stages"]["analysis"]["tokens"] +
                metrics["stages"]["spec"]["tokens"])

print(f"\n📊 PIPELINE SUMMARY")
print(f"   Total Time:   {total_duration}s")
print(f"   Total Tokens: {total_tokens:,}")

# Save metrics to JSON file
metrics_file = "metrics.json"
with open(metrics_file, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"\n✅ Metrics saved to: {metrics_file}")

# Generate the execution summary markdown
# (Call the Python generator script)
import subprocess
result = subprocess.run([
    "python",
    "skills/spec-driven-development-orchestrator/execution_summary_generator.py",
    metrics_file,
    "documents/"
], capture_output=True, text=True)

if result.returncode == 0:
    print(f"✅ Execution summary saved to: documents/execution-summary-{metrics['ticket_id']}.md")
else:
    print(f"❌ Error generating summary: {result.stderr}")
```

---

## Token Count Extraction

### Method 1: From Tool Response Metadata
Most Claude API responses include token usage:

```python
# In the response from each skill invocation
response = invoke_skill("azure-devops-ticket-quality", ticket_id)

# Extract tokens if available
if hasattr(response, 'usage'):
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = input_tokens + output_tokens
else:
    # Fallback: estimate based on typical usage
    total_tokens = estimate_tokens(response)
```

### Method 2: Estimation
If exact token counts aren't available, estimate based on typical patterns:

```python
def estimate_tokens(skill_name, response_length):
    """Rough estimate of tokens used (adjust based on your metrics)."""
    if skill_name == "azure-devops-ticket-quality":
        return 2800  # Typical: ~2800 tokens
    elif skill_name == "solution-analysis-gate":
        return 8900  # Typical: ~8900 tokens
    elif skill_name == "technical-spec-generator":
        return 5200  # Typical: ~5200 tokens
    return int(response_length / 4)  # Rough estimate: 1 token ≈ 4 chars
```

---

## Complete Metrics JSON Example

```json
{
  "ticket_id": "12345",
  "ticket_title": "Implement user authentication for mobile app",
  "project_name": "MyProject",
  "status": "completed",
  "timestamp": "2026-07-16T14:30:00Z",
  "stages": {
    "quality": {
      "duration": 18,
      "tokens": 2840,
      "quality_score": 82,
      "gate_decision": "proceed"
    },
    "analysis": {
      "duration": 45,
      "tokens": 8920
    },
    "spec": {
      "duration": 32,
      "tokens": 5240
    }
  }
}
```

---

## Verify Your Output

After running the generator, check:

```bash
# Verify metrics were saved
cat metrics.json

# Verify summary was generated
ls -la documents/execution-summary-*.md

# Check summary content
cat documents/execution-summary-12345.md
```

You should see:
- ✅ Execution Timeline table with actual durations and tokens
- ✅ Token Usage Breakdown with per-stage percentages
- ✅ Time Breakdown in readable format
- ✅ Cost estimate (e.g., ~$0.17)
- ✅ Efficiency metric (e.g., 178.9 tokens/second)

---

## Troubleshooting

**Q: Summary shows `{total_duration}` instead of actual time**  
A: Metrics JSON wasn't saved correctly. Verify `metrics.json` exists and has `duration` values.

**Q: Token counts are zero**  
A: Token extraction failed. Check that skill responses include token usage data, or use estimation fallback.

**Q: Python script fails with "file not found"**  
A: Check the script path: `skills/spec-driven-development-orchestrator/execution_summary_generator.py`

**Q: Summary file not created**  
A: Verify `documents/` directory exists or that the script has permission to create it.

---

## Integration Points

This metric tracking integrates with:
- **execution_summary_generator.py** — Takes metrics JSON, generates markdown
- **EXECUTION-EXAMPLE.md** — Shows what a completed summary looks like
- **EXECUTION-SUMMARY-TEMPLATE.md** — Template with placeholder variables
- **SKILL.md** — References metric tracking requirements

---

## Notes

- Duration is in seconds (integer)
- Tokens are in counts (integer)
- Timestamp should be ISO-8601 format
- Quality score is 0-100
- Gate decision is one of: "proceed", "review", "block"
