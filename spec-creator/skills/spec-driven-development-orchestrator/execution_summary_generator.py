#!/usr/bin/env python3
"""
Execution Summary Generator for Spec-Driven Development Orchestrator

Generates a markdown summary of the orchestrator execution with metrics:
- Execution time and tokens per stage
- Quality gate results
- Generated artifacts
- Next steps and troubleshooting

Usage:
    python execution_summary_generator.py <metrics.json>

Metrics JSON structure:
    {
        "ticket_id": "12345",
        "ticket_title": "Implement feature X",
        "project_name": "MyProject",
        "status": "completed|blocked|failed",
        "timestamp": "2026-07-16T14:30:00Z",
        "stages": {
            "quality": {
                "duration": 18,
                "tokens": 2840,
                "quality_score": 82,
                "gate_decision": "proceed",
                "gate_details": "Score 82/100 exceeds 70-point threshold"
            },
            "analysis": {
                "duration": 45,
                "tokens": 8920,
                "new_or_reused": "freshly_generated"
            },
            "spec": {
                "duration": 32,
                "tokens": 5240
            }
        }
    }
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def calculate_percentages(stage_tokens):
    """Calculate token percentages for each stage."""
    total = sum(stage_tokens.values())
    if total == 0:
        return {}
    return {stage: (tokens / total * 100) for stage, tokens in stage_tokens.items()}

def estimate_cost(total_tokens):
    """Estimate cost in USD (Claude 3.5 Sonnet pricing as baseline)."""
    # Example: $0.003 per 1K input tokens, $0.015 per 1K output tokens
    # This is a rough estimate; adjust for your actual pricing
    cost_per_1k_tokens = 0.0036  # Average rate
    return (total_tokens / 1000) * cost_per_1k_tokens

def format_duration(seconds):
    """Format duration in seconds to human-readable format."""
    if seconds < 60:
        return f"{seconds}s"
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}m {secs}s" if secs else f"{mins}m"

def generate_summary(metrics):
    """Generate execution summary markdown from metrics."""

    ticket_id = metrics.get("ticket_id", "UNKNOWN")
    ticket_title = metrics.get("ticket_title", "Unknown Ticket")
    project = metrics.get("project_name", "Unknown Project")
    status = metrics.get("status", "unknown")
    timestamp = metrics.get("timestamp", datetime.now().isoformat())

    # Extract stage metrics
    quality = metrics.get("stages", {}).get("quality", {})
    analysis = metrics.get("stages", {}).get("analysis", {})
    spec = metrics.get("stages", {}).get("spec", {})

    # Calculate totals
    durations = {
        "quality": quality.get("duration", 0),
        "analysis": analysis.get("duration", 0),
        "spec": spec.get("duration", 0)
    }
    tokens = {
        "quality": quality.get("tokens", 0),
        "analysis": analysis.get("tokens", 0),
        "spec": spec.get("tokens", 0)
    }

    total_duration = sum(durations.values())
    total_tokens = sum(tokens.values())
    total_cost = estimate_cost(total_tokens)

    percentages = calculate_percentages(tokens)
    efficiency = total_tokens / total_duration if total_duration > 0 else 0

    # Quality score
    quality_score = quality.get("quality_score", 0)
    quality_rating = "Excellent" if quality_score >= 90 else \
                     "Good" if quality_score >= 80 else \
                     "Fair" if quality_score >= 70 else \
                     "Poor"

    gate_decision = quality.get("gate_decision", "unknown").upper()
    gate_emoji = "✅" if gate_decision == "PROCEED" else "⚠️" if gate_decision == "REVIEW" else "❌"

    status_emoji = "✅" if status == "completed" else "⚠️" if status == "blocked" else "❌"

    # Parse timestamp for display
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        date_display = dt.strftime("%B %d, %Y at %I:%M %p %Z")
    except:
        date_display = timestamp

    # Build markdown
    md = f"""# Spec-Driven Development Pipeline Execution Summary

**Pipeline ID:** `orch-{ticket_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}`
**Work Item:** {ticket_id} — {ticket_title}
**Project:** {project}
**Status:** {status_emoji} **{status.upper()}**
**Date:** {date_display}

---

## Execution Timeline

| Stage | Status | Duration | Tokens Used |
|-------|--------|----------|------------|
| **1. Ticket Quality Assessment** | ✅ Completed | {format_duration(durations['quality'])} | {tokens['quality']:,} |
| **2. Solution Analysis Gating** | ✅ Completed | {format_duration(durations['analysis'])} | {tokens['analysis']:,} |
| **3. Technical Spec Generation** | ✅ Completed | {format_duration(durations['spec'])} | {tokens['spec']:,} |
| **Total Pipeline** | {status_emoji} {status.upper()} | **{format_duration(total_duration)}** | **{total_tokens:,}** |

---

## Execution Metrics

### Token Usage Breakdown

```
Input Tokens:   ~{int(total_tokens * 0.35):,} (estimated)
Output Tokens:  ~{int(total_tokens * 0.65):,} (estimated)
Total Tokens:   {total_tokens:,}
Cost (est):     ${total_cost:.2f}
```

**Per Stage:**
- Stage 1 (Quality):     {tokens['quality']:,} tokens ({percentages.get('quality', 0):.1f}%)
- Stage 2 (Analysis):    {tokens['analysis']:,} tokens ({percentages.get('analysis', 0):.1f}%)
- Stage 3 (Spec):        {tokens['spec']:,} tokens ({percentages.get('spec', 0):.1f}%)

### Time Breakdown

```
Elapsed Time:        {format_duration(total_duration)}
  - Stage 1:         {format_duration(durations['quality'])}
  - Stage 2:         {format_duration(durations['analysis'])}
  - Stage 3:         {format_duration(durations['spec'])}
```

**Efficiency:** {efficiency:.1f} tokens/second

---

## Quality Gate Results

### Ticket Quality Assessment

**Score: {quality_score}/100** — {quality_rating}

**Gate Decision:** {gate_emoji} **{gate_decision}**

{quality.get('gate_details', 'See quality report for details.')}

---

## Generated Artifacts

All outputs are saved to the `documents/` folder:

```
documents/
├── ticket-quality-{ticket_id}.md      ← Quality assessment (human-readable)
├── ticket-quality-{ticket_id}.json    ← Quality assessment (structured)
├── technical-solution-analysis.md     ← Codebase architecture analysis
├── technical-spec.md                  ← Implementation plan
└── execution-summary-{ticket_id}.md   ← This summary file
```

---

## Next Steps

### For Development Teams

1. **Review the quality report** — Address flagged weaknesses in `documents/ticket-quality-{ticket_id}.md`
2. **Study the solution analysis** — Understand architecture in `documents/technical-solution-analysis.md`
3. **Follow the technical spec** — Execute plan in `documents/technical-spec.md`

### For Product Managers

1. **Review quality score** — {quality_rating} ({quality_score}/100)
2. **Check gate decision** — {gate_emoji} {gate_decision}
3. **Validate artifacts** — Review all generated documents

---

## Execution Details

**Pipeline Version:** v1.0
**Orchestrator:** `spec-driven-development-orchestrator`
**Skills Invoked:** 3
**Files Generated:** 5
**Status:** {status.upper()}

---

**Ready to start development?** Review the technical spec and quality report above.

Generated by: Spec-Driven Development Orchestrator v1.0
"""

    return md

def save_summary(markdown_content, ticket_id, output_dir="documents"):
    """Save the summary to a markdown file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary_file = output_path / f"execution-summary-{ticket_id}.md"
    summary_file.write_text(markdown_content)

    print(f"✅ Execution summary saved to: {summary_file}")
    return summary_file

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python execution_summary_generator.py <metrics.json> [output_dir]")
        sys.exit(1)

    metrics_file = Path(sys.argv[1])
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "documents"

    if not metrics_file.exists():
        print(f"❌ Error: Metrics file not found: {metrics_file}")
        sys.exit(1)

    try:
        metrics = json.loads(metrics_file.read_text())
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in metrics file: {e}")
        sys.exit(1)

    summary = generate_summary(metrics)
    save_summary(summary, metrics["ticket_id"], output_dir)

    print(f"✅ Execution summary generated successfully")
    print(f"Ticket: {metrics['ticket_id']}")
    print(f"Total Tokens: {sum(m.get('tokens', 0) for m in metrics.get('stages', {}).values()):,}")
    print(f"Total Duration: {sum(m.get('duration', 0) for m in metrics.get('stages', {}).values())}s")

if __name__ == "__main__":
    main()
