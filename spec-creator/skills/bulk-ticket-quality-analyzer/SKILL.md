---
name: bulk-ticket-quality-analyzer
description: Aggregate and analyze multiple ticket-quality-*.json reports to identify patterns, trends, and improvement opportunities across your backlog. Generates comprehensive dashboards and actionable insights for team quality improvement.
---

# Bulk Ticket Quality Analyzer

Analyzes a portfolio of ticket quality reports to identify patterns, trends, and improvement opportunities across your entire backlog. This skill aggregates data from multiple `ticket-quality-*.json` files and generates comprehensive dashboards and actionable insights.

## Actor and Goal

**Act like a Tech Lead or Engineering Manager** reviewing backlog health. Your goal is to:
- **Identify portfolio-level patterns** — what quality issues repeat across tickets?
- **Spot team gaps** — which evaluation criteria are consistently weak?
- **Prioritize improvements** — which weaknesses block the most tickets?
- **Track progress** — measure backlog quality trends over time
- **Unblock teams** — highlight which tickets need remediation before they enter sprints

## How to Use This Skill

### Input

No direct input needed. The skill automatically:
1. Scans `documents/` directory for all `ticket-quality-*.json` files
2. Reads and aggregates the data
3. Generates portfolio-level insights

### Usage

```
/vbu-hackathon-project:bulk-ticket-quality-analyzer
```

The skill will find all reports and analyze them.

### Output

The skill generates a comprehensive **Bulk Quality Report** with:

1. **Portfolio Overview**
   - Total tickets analyzed
   - Overall average quality score
   - Score distribution (% excellent, good, fair, poor, incomplete)
   - Trend indicators

2. **Criteria Breakdown**
   - Average score for each criterion (Clarity, AC, Business Context, etc.)
   - Which criteria are strongest/weakest
   - Which criteria correlate most with low overall scores

3. **Common Weaknesses Across Portfolio**
   - Top 10 most-cited weaknesses (frequency count)
   - Which weaknesses appear in which tickets
   - Severity assessment

4. **Red Flag Patterns**
   - Most common red flags
   - Tickets with multiple red flags (high risk)
   - Red flag categories (vague language, missing scope, risk analysis gaps, etc.)

5. **Question Themes**
   - Most frequently asked questions across tickets
   - Suggests systematic gaps in ticket specification
   - Indicates missing process or documentation

6. **Tickets Below Threshold**
   - Lists all tickets scoring below 70 (fair/poor/incomplete)
   - Prioritizes for remediation
   - Suggests what to fix first

7. **Recommendations**
   - Portfolio-level actions to improve ticket quality
   - Process improvements (e.g., "add technical review step")
   - Team training opportunities

8. **Saved Reports**
   - **Markdown**: `documents/bulk-ticket-quality-report.md` — human-readable dashboard
   - **JSON**: `documents/bulk-ticket-quality-report.json` — structured data for integration

## Typical Workflows

### Pre-Sprint Quality Gate
```
Run bulk analyzer before sprint planning to:
- Identify which tickets need rework before commitment
- Ensure minimum quality threshold across sprint
- Flag risky items (low scores + high complexity)
```

### Backlog Grooming
```
Use quarterly to measure team's documentation practices:
- Track improvement in average quality scores
- Identify persistent team gaps (e.g., always weak on Risks)
- Validate that Definition of Ready is effective
```

### Team Training
```
Use weak tickets as teachable moments:
- Show the team: "Here are the 5 most common gaps"
- Point to specific examples of what good looks like
- Demonstrate cost of poor specifications
```

### Continuous Improvement
```
Track metrics over time:
- Month 1: Average 65 (poor)
- Month 2: Average 72 (fair) — improving
- Month 3: Average 78 (good) — process working
```

## Quality Score Interpretation

- **90-100**: Excellent. Ready for development.
- **80-89**: Good. Minor gaps, shouldn't block work.
- **70-79**: Fair. Significant gaps. Address before starting.
- **60-69**: Poor. Multiple issues. Major clarification needed.
- **Below 60**: Incomplete. Needs substantial revision.

## Report Sections Explained

### Portfolio Overview
Shows the big picture: How healthy is your backlog overall? What % of tickets are ready to start?

### Criteria Breakdown
Reveals systemic gaps. If "Risks" averages 35/100 but "Clarity" averages 82/100, your team understands *what* to build but not *the risks* — suggests training gap around risk analysis.

### Common Weaknesses
If 8 out of 10 tickets say "Missing technical scope", that's a signal to improve your ticket template or process, not individual tickets.

### Red Flags
Highlights tickets with vague language or hidden assumptions. These are early warnings — catch before sprint.

### Tickets Below Threshold
Your remediation backlog. Start here for quick wins.

## Example Output

**Input:** 15 ticket quality reports

**Analysis:**
- Average score: 71/100 (Fair)
- Distribution: 2 Excellent, 4 Good, 6 Fair, 2 Poor, 1 Incomplete
- Weakest criteria: Risks (avg 52), Technical Information (avg 64)
- Most common weakness: "Missing rollback plan" (12 tickets)
- Tickets below 70: 8 tickets (priority for remediation)

**Report saved to:** `documents/bulk-ticket-quality-report.md`

## Tips for Best Results

1. **Run regularly** — Schedule weekly or before each sprint to track trends
2. **Act on insights** — Don't just generate reports; use them to improve process
3. **Share with team** — Make patterns visible to shift team behavior
4. **Update your DoR** — If a weakness is common, add it to your Definition of Ready checklist
5. **Track over time** — Compare reports month-to-month to measure improvement

---

*This skill measures and improves your backlog's health at scale.*
