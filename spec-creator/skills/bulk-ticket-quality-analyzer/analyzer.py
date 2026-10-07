#!/usr/bin/env python3
"""
Bulk Ticket Quality Analyzer
Aggregates multiple ticket-quality-*.json reports and generates portfolio insights.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Dict, List, Any


def find_quality_reports() -> List[Path]:
    """Find all ticket-quality-*.json files in documents directory."""
    docs_dir = Path("documents")
    if not docs_dir.exists():
        return []
    return sorted(docs_dir.glob("ticket-quality-*.json"))


def load_reports(report_paths: List[Path]) -> List[Dict[str, Any]]:
    """Load all quality reports from JSON files."""
    reports = []
    for path in report_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reports.append(json.load(f))
        except Exception as e:
            print(f"Warning: Could not load {path}: {e}", file=sys.stderr)
    return reports


def calculate_score_distribution(reports: List[Dict]) -> Dict[str, int]:
    """Categorize tickets by score range."""
    distribution = {
        "Excellent (90-100)": 0,
        "Good (80-89)": 0,
        "Fair (70-79)": 0,
        "Poor (60-69)": 0,
        "Incomplete (<60)": 0
    }

    for report in reports:
        score = report.get("overall_score", 0)
        if score >= 90:
            distribution["Excellent (90-100)"] += 1
        elif score >= 80:
            distribution["Good (80-89)"] += 1
        elif score >= 70:
            distribution["Fair (70-79)"] += 1
        elif score >= 60:
            distribution["Poor (60-69)"] += 1
        else:
            distribution["Incomplete (<60)"] += 1

    return distribution


def analyze_criteria(reports: List[Dict]) -> Dict[str, Dict[str, float]]:
    """Analyze average scores and variance for each criterion."""
    criteria_scores = {}

    for report in reports:
        criteria = report.get("criteria", {})
        for criterion_name, criterion_data in criteria.items():
            if criterion_name not in criteria_scores:
                criteria_scores[criterion_name] = []
            criteria_scores[criterion_name].append(criterion_data.get("score", 0))

    analysis = {}
    for criterion_name, scores in criteria_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            analysis[criterion_name] = {
                "average": round(avg, 1),
                "min": min_score,
                "max": max_score,
                "count": len(scores)
            }

    return dict(sorted(analysis.items(), key=lambda x: x[1]["average"]))


def count_weaknesses(reports: List[Dict]) -> Dict[str, int]:
    """Count frequency of each weakness across all tickets."""
    weakness_counter = Counter()

    for report in reports:
        weaknesses = report.get("weaknesses", [])
        for weakness in weaknesses:
            weakness_counter[weakness] += 1

    return dict(weakness_counter.most_common(15))


def count_red_flags(reports: List[Dict]) -> Dict[str, int]:
    """Count frequency of red flags across all tickets."""
    flag_counter = Counter()

    for report in reports:
        red_flags = report.get("red_flags", [])
        for flag in red_flags:
            flag_counter[flag] += 1

    return dict(flag_counter.most_common(10))


def count_questions(reports: List[Dict]) -> Dict[str, int]:
    """Count frequency of suggested questions across all tickets."""
    question_counter = Counter()

    for report in reports:
        questions = report.get("suggested_questions", [])
        for question in questions:
            question_counter[question] += 1

    return dict(question_counter.most_common(10))


def tickets_below_threshold(reports: List[Dict], threshold: int = 70) -> List[Dict]:
    """Get all tickets scoring below threshold."""
    below = []
    for report in reports:
        if report.get("overall_score", 100) < threshold:
            below.append({
                "ticket_id": report.get("ticket_id"),
                "ticket_title": report.get("ticket_title"),
                "overall_score": report.get("overall_score"),
                "criteria": report.get("criteria", {})
            })
    return sorted(below, key=lambda x: x.get("overall_score", 0))


def generate_recommendations(reports: List[Dict], criteria_stats: Dict, weaknesses: Dict) -> List[str]:
    """Generate portfolio-level recommendations."""
    recommendations = []

    # Find criteria with lowest average scores
    lowest_criteria = sorted(criteria_stats.items(), key=lambda x: x[1]["average"])[:3]
    for criterion, stats in lowest_criteria:
        recommendations.append(f"Focus on improving '{criterion}' (currently {stats['average']}/100 avg) — add to team training or process checklist")

    # Find most common weaknesses
    top_weakness_count = list(weaknesses.values())[0] if weaknesses else 0
    top_weakness = list(weaknesses.keys())[0] if weaknesses else ""
    if top_weakness and top_weakness_count > len(reports) * 0.5:
        recommendations.append(f"'{top_weakness}' appears in {top_weakness_count} tickets ({int(top_weakness_count/len(reports)*100)}%) — systemic issue, address in process")

    # Check if many tickets below threshold
    below_70 = sum(1 for r in reports if r.get("overall_score", 100) < 70)
    if below_70 > len(reports) * 0.3:
        recommendations.append(f"{below_70} tickets ({int(below_70/len(reports)*100)}%) score below 70 — establish quality gate before sprint entry")

    # Check average
    avg_score = sum(r.get("overall_score", 0) for r in reports) / len(reports) if reports else 0
    if avg_score < 70:
        recommendations.append("Overall backlog quality is fair/poor — consider implementing Definition of Ready workshop with team")
    elif avg_score < 80:
        recommendations.append("Continue focus on weak criteria — backlog is improving but not yet optimized")

    return recommendations[:5]  # Return top 5


def create_documents_dir():
    """Ensure the documents directory exists."""
    docs_dir = Path("documents")
    docs_dir.mkdir(exist_ok=True)
    return docs_dir


def format_report(reports: List[Dict], analysis: Dict) -> str:
    """Format aggregated analysis into markdown report."""
    if not reports:
        return "# Bulk Ticket Quality Report\n\nNo ticket quality reports found in documents/ directory.\n"

    total = len(reports)
    avg_score = round(sum(r.get("overall_score", 0) for r in reports) / total, 1)

    report = f"""# Bulk Ticket Quality Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Tickets Analyzed:** {total}
**Overall Average Score:** {avg_score}/100

---

## Portfolio Overview

### Score Distribution
"""

    distribution = analysis.get("distribution", {})
    for category, count in distribution.items():
        pct = int(count / total * 100) if total > 0 else 0
        report += f"- **{category}**: {count} tickets ({pct}%)\n"

    report += "\n### Interpretation\n"
    if avg_score >= 80:
        report += "✅ **Excellent** — Your backlog is well-specified and ready for development.\n"
    elif avg_score >= 70:
        report += "⚠️ **Fair** — Significant gaps exist; address before sprinting.\n"
    elif avg_score >= 60:
        report += "❌ **Poor** — Multiple quality issues; requires major improvement.\n"
    else:
        report += "🚨 **Incomplete** — Backlog needs substantial revision before development.\n"

    # Criteria Breakdown
    criteria_stats = analysis.get("criteria_stats", {})
    report += "\n## Criteria Breakdown\n\n"
    report += "| Criterion | Avg Score | Min | Max | Variance |\n"
    report += "|-----------|-----------|-----|-----|----------|\n"

    for criterion, stats in sorted(criteria_stats.items(), key=lambda x: x[1]["average"]):
        avg = stats["average"]
        min_s = stats["min"]
        max_s = stats["max"]
        variance = max_s - min_s
        report += f"| {criterion} | {avg}/100 | {min_s} | {max_s} | {variance} |\n"

    report += "\n**Key Insight:** Criteria with lower averages indicate team gaps. Consider adding to Definition of Ready.\n"

    # Common Weaknesses
    weaknesses = analysis.get("weaknesses", {})
    report += "\n## Top 10 Common Weaknesses\n\n"
    for i, (weakness, count) in enumerate(weaknesses.items(), 1):
        pct = int(count / total * 100) if total > 0 else 0
        report += f"{i}. **{weakness}** — {count} tickets ({pct}%)\n"

    # Red Flags
    red_flags = analysis.get("red_flags", {})
    report += "\n## Top Red Flags\n\n"
    for i, (flag, count) in enumerate(red_flags.items(), 1):
        pct = int(count / total * 100) if total > 0 else 0
        report += f"{i}. ⚠️ **{flag}** — {count} tickets ({pct}%)\n"

    # Question Themes
    questions = analysis.get("questions", {})
    report += "\n## Frequently Asked Questions (Top 10)\n\n"
    report += "These questions appear in multiple tickets, suggesting systemic information gaps:\n\n"
    for i, (question, count) in enumerate(questions.items(), 1):
        report += f"{i}. {question} *(asked {count}x)*\n"

    # Tickets Below Threshold
    below_threshold = analysis.get("below_threshold", [])
    report += f"\n## Tickets Below Quality Threshold (<70: {len(below_threshold)})\n\n"
    if below_threshold:
        report += "| Ticket ID | Title | Score | Weakest Criteria |\n"
        report += "|-----------|-------|-------|------------------|\n"
        for ticket in below_threshold[:10]:  # Show top 10
            ticket_id = ticket.get("ticket_id", "?")
            title = ticket.get("ticket_title", "?")[:50]
            score = ticket.get("overall_score", 0)

            # Find weakest criterion
            criteria = ticket.get("criteria", {})
            if criteria:
                weakest = min(criteria.items(), key=lambda x: x[1].get("score", 0))
                weakest_name = weakest[0]
                weakest_score = weakest[1].get("score", 0)
            else:
                weakest_name = "?"
                weakest_score = 0

            report += f"| {ticket_id} | {title}... | {score} | {weakest_name} ({weakest_score}) |\n"

        if len(below_threshold) > 10:
            report += f"\n*... and {len(below_threshold) - 10} more below 70*\n"
    else:
        report += "✅ All tickets score 70 or above!\n"

    # Recommendations
    recommendations = analysis.get("recommendations", [])
    report += "\n## Portfolio Recommendations\n\n"
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"

    report += f"\n---\n*Report generated by Bulk Ticket Quality Analyzer*\n"

    return report


def save_report(report_content: str, analysis: Dict) -> tuple:
    """Save report to both markdown and JSON files."""
    docs_dir = create_documents_dir()

    # Save markdown
    md_filename = "bulk-ticket-quality-report.md"
    md_filepath = docs_dir / md_filename
    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)

    # Save JSON
    json_filename = "bulk-ticket-quality-report.json"
    json_filepath = docs_dir / json_filename
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    return str(md_filepath), str(json_filepath)


def main():
    """Main entry point."""
    # Find and load reports
    report_paths = find_quality_reports()

    if not report_paths:
        print("❌ No ticket-quality-*.json files found in documents/ directory")
        print("   Generate ticket quality reports first using the azure-devops-ticket-quality skill")
        return

    reports = load_reports(report_paths)

    if not reports:
        print("❌ Could not load any ticket quality reports")
        return

    print(f"✓ Loaded {len(reports)} ticket quality reports")

    # Analyze data
    distribution = calculate_score_distribution(reports)
    criteria_stats = analyze_criteria(reports)
    weaknesses = count_weaknesses(reports)
    red_flags = count_red_flags(reports)
    questions = count_questions(reports)
    below_threshold = tickets_below_threshold(reports, 70)
    recommendations = generate_recommendations(reports, criteria_stats, weaknesses)

    # Compile analysis
    analysis = {
        "generated": datetime.now().isoformat(),
        "total_tickets": len(reports),
        "average_score": round(sum(r.get("overall_score", 0) for r in reports) / len(reports), 1),
        "distribution": distribution,
        "criteria_stats": criteria_stats,
        "weaknesses": weaknesses,
        "red_flags": red_flags,
        "questions": questions,
        "below_threshold_count": len(below_threshold),
        "below_threshold": below_threshold,
        "recommendations": recommendations
    }

    # Generate and save report
    report_content = format_report(reports, analysis)
    md_filepath, json_filepath = save_report(report_content, analysis)

    print(f"✓ Markdown report saved to: {md_filepath}")
    print(f"✓ JSON report saved to: {json_filepath}")
    print("\n" + "="*70)
    print(report_content)


if __name__ == '__main__':
    main()
