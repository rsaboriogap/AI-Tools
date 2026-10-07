#!/usr/bin/env python3
"""
Save evaluation results from azure-devops-ticket-quality-judge to documents/.
Generates both JSON and markdown summary files.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime


def create_documents_dir():
    """Ensure the documents directory exists."""
    docs_dir = Path("documents")
    docs_dir.mkdir(exist_ok=True)
    return docs_dir


def validate_and_fix_overall_score(evaluation: dict) -> dict:
    """
    Validate overall_score calculation and fix if incorrect.
    Formula: overall_score = sum((score / 5) × effective_weight)
    Tolerance: 0.01
    """
    if "criteria" not in evaluation:
        return evaluation

    criteria = evaluation.get("criteria", {})

    # Calculate the correct overall score
    calculated_score = 0.0
    total_effective_weight = 0

    for criterion_name, criterion_data in criteria.items():
        score = criterion_data.get("score", 0)
        effective_weight = criterion_data.get("effective_weight", criterion_data.get("weight", 0))

        weighted_score = (score / 5.0) * effective_weight
        calculated_score += weighted_score
        total_effective_weight += effective_weight

    # Check if calculation matches
    reported_score = evaluation.get("overall_score", 0)
    tolerance = 0.01

    if abs(calculated_score - reported_score) > tolerance:
        print(f"\n⚠️  SCORE CORRECTION DETECTED", file=sys.stderr)
        print(f"   Reported: {reported_score}", file=sys.stderr)
        print(f"   Calculated: {calculated_score:.2f}", file=sys.stderr)
        print(f"   Correcting to calculated value...", file=sys.stderr)
        evaluation["overall_score"] = round(calculated_score, 2)
        if "score_corrected" not in evaluation:
            evaluation["score_corrected"] = {
                "reported": reported_score,
                "calculated": round(calculated_score, 2),
                "reason": "Recalculated from criteria using formula: sum((score/5) × effective_weight)"
            }

    return evaluation


def format_summary(evaluation: dict) -> str:
    """Format the evaluation into a comprehensive markdown report."""
    eval_id = evaluation.get("evaluation_id", "unknown")
    mode = evaluation.get("evaluation_mode", "pointwise")
    passed = evaluation.get("passed", False)
    score = evaluation.get("overall_score", 0)
    confidence = evaluation.get("confidence", 0)

    md = f"""# Evaluation Report: {eval_id}

**Status:** {'✅ PASSED' if passed else '❌ FAILED'}
**Overall Score:** {score}/100
**Confidence:** {confidence:.0%}
**Mode:** {mode}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    # Add note if score was corrected
    if "score_corrected" in evaluation:
        correction = evaluation["score_corrected"]
        md += f"""
> **ℹ️ Score Correction:** The overall score was recalculated from criteria.
> - Originally reported: {correction['reported']}
> - Corrected to: {correction['calculated']} (formula: sum(score/5 × effective_weight))
> - Reason: {correction['reason']}
"""

    md += "\n---\n\n## Skill Definition\n\n"
    if "skill_definition" in evaluation:
        skill = evaluation["skill_definition"]
        md += f"- **Name:** {skill.get('name', 'N/A')}\n"
        md += f"- **Path:** {skill.get('path', 'N/A')}\n"
        md += f"- **Version:** {skill.get('version', 'N/A')}\n"
        md += f"- **Loaded:** {'✓' if skill.get('loaded') else '✗'}\n"

    md += "\n## Evaluation Criteria\n\n"
    md += "| Criterion | Score | Weight | Weighted Score | Status |\n"
    md += "|-----------|-------|--------|---------------|---------|\n"

    if "criteria" in evaluation:
        criteria = evaluation["criteria"]
        # Handle both dict and list formats
        if isinstance(criteria, dict):
            for criterion_name, criterion_data in criteria.items():
                name = criterion_name.replace("_", " ").title()
                score = criterion_data.get("score", 0)
                weight = criterion_data.get("weight", 0)
                w_score = criterion_data.get("weighted_score", 0)
                not_applicable = criterion_data.get("not_applicable", False)
                status = "N/A" if not_applicable else "✓" if score >= 3 else "⚠"
                md += f"| {name} | {score}/5 | {weight} | {w_score:.2f} | {status} |\n"
        else:
            for criterion in criteria:
                name = criterion.get("name", "unknown").replace("_", " ").title()
                score = criterion.get("score", 0)
                weight = criterion.get("weight", 0)
                w_score = criterion.get("weighted_score", 0)
                not_applicable = criterion.get("not_applicable", False)
                status = "N/A" if not_applicable else "✓" if score >= 3 else "⚠"
                md += f"| {name} | {score}/5 | {weight} | {w_score:.2f} | {status} |\n"

    if "deterministic_check_summary" in evaluation:
        summary = evaluation["deterministic_check_summary"]
        md += f"\n## Deterministic Checks\n\n"
        md += f"- **Total:** {summary.get('total', 0)}\n"
        md += f"- **Passed:** {summary.get('passed', 0)}\n"
        md += f"- **Failed:** {summary.get('failed', 0)}\n"
        md += f"- **Critical Failed:** {summary.get('critical_failed', 0)}\n"

    if "critical_failures" in evaluation and evaluation["critical_failures"]:
        md += f"\n## 🚨 Critical Failures\n\n"
        for i, failure in enumerate(evaluation["critical_failures"], 1):
            code = failure.get("code", "UNKNOWN")
            desc = failure.get("description", "")
            evidence = failure.get("evidence", "")
            md += f"### {i}. {code}\n\n"
            md += f"**Description:** {desc}\n\n"
            if evidence:
                md += f"**Evidence:** {evidence}\n\n"

    if "missing_requirements" in evaluation and evaluation["missing_requirements"]:
        md += f"\n## Missing Requirements\n\n"
        for i, req in enumerate(evaluation["missing_requirements"], 1):
            md += f"{i}. {req}\n"

    if "strengths" in evaluation and evaluation["strengths"]:
        md += f"\n## ✓ Strengths\n\n"
        for strength in evaluation["strengths"]:
            md += f"- {strength}\n"

    if "improvements" in evaluation and evaluation["improvements"]:
        md += f"\n## Recommendations for Improvement\n\n"
        for improvement in evaluation["improvements"]:
            priority = improvement.get("priority", "medium").upper()
            area = improvement.get("area", "")
            rec = improvement.get("recommendation", "")
            priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(priority, "•")
            md += f"### {priority_emoji} [{priority}] {area}\n\n{rec}\n\n"

    if "summary" in evaluation:
        md += f"\n## Executive Summary\n\n{evaluation['summary']}\n"

    md += f"\n---\n\n*Full data available in: `documents/evaluation-{eval_id}.json`*\n"

    return md


def save_evaluation(evaluation: dict) -> tuple:
    """Save evaluation result to both JSON and markdown formats."""
    # Validate and fix overall_score if needed
    evaluation = validate_and_fix_overall_score(evaluation)

    eval_id = evaluation.get("evaluation_id", "eval-unknown")
    docs_dir = create_documents_dir()

    # Save JSON
    json_filename = f"evaluation-{eval_id}.json"
    json_filepath = docs_dir / json_filename
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(evaluation, f, indent=2, ensure_ascii=False)

    # Save markdown report
    report = format_summary(evaluation)
    md_filename = f"evaluation-{eval_id}.md"
    md_filepath = docs_dir / md_filename
    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(report)

    return str(json_filepath), str(md_filepath)


def main():
    """Main entry point for the evaluation saver."""
    if len(sys.argv) < 2:
        print("Usage: evaluation_saver.py <evaluation_json_file>", file=sys.stderr)
        sys.exit(1)

    eval_file = sys.argv[1]

    try:
        with open(eval_file, 'r', encoding='utf-8') as f:
            evaluation = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading evaluation file: {e}", file=sys.stderr)
        sys.exit(1)

    # Save the evaluation
    json_filepath, md_filepath = save_evaluation(evaluation)

    eval_id = evaluation.get("evaluation_id", "unknown")
    passed = evaluation.get("passed", False)
    score = evaluation.get("overall_score", 0)
    corrected = "score_corrected" in evaluation

    print(f"\n{'='*60}")
    print(f"Evaluation saved: {eval_id}")
    print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'} | Score: {score}/100")
    if corrected:
        original = evaluation["score_corrected"]["reported"]
        print(f"⚠️  Score corrected from {original} → {score}")
    print(f"{'='*60}")
    print(f"✓ JSON evaluation:  {json_filepath}")
    print(f"✓ Markdown report:  {md_filepath}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
