# Supplementary Skills: Deep Dive

Detailed explanation of two advanced skills that complement the core spec-driven pipeline:
- **azure-devops-ticket-quality-judge** — Evaluate skill/agent execution quality
- **bulk-ticket-quality-analyzer** — Analyze portfolio-level ticket patterns

These skills are **optional** and serve specialized use cases (evaluation, metrics, team improvement).

---

## 1. azure-devops-ticket-quality-judge

**Type:** LLM-as-a-Judge evaluator  
**Role:** Validates execution quality of AI agents and Claude skills  
**Invocation:** `/azure-devops-ticket-quality-judge evaluation.json`  
**Dependency:** Evaluation package with execution evidence

### What It Does

Acts as an **independent, evidence-based evaluator** of whether a skill or agent performed correctly. It:

1. **Reads an evaluation package** — Input specification + execution evidence
2. **Loads skill definition** — Gets the actual SKILL.md being evaluated
3. **Judges against rubric** — Scores on 8 weighted criteria
4. **Identifies failures** — Surfaces bugs, instruction violations, fabricated evidence
5. **Produces report** — Saved to `documents/evaluation-{id}.md` and `.json`

### Key Concepts

**Evaluation Package** — Input file containing:
```json
{
  "evaluation_id": "eval-001",
  "evaluation_mode": "pointwise",
  "user_request": "What was asked?",
  "skill_definition": {
    "name": "target-skill",
    "path": "skills/target-skill/SKILL.md"
  },
  "expected_behavior": {
    "must": [...],
    "must_not": [...]
  },
  "execution_trace": {
    "tool_calls": [...],
    "tool_outputs": [...]
  },
  "agent_response": "Final response produced",
  "deterministic_checks": [
    {
      "name": "output_file_exists",
      "passed": true,
      "critical": true
    }
  ]
}
```

**Evaluation Rubric** — 8 weighted criteria:

| Criterion | Weight | Measures |
|-----------|--------|----------|
| **Skill Activation** | 10% | Was the correct skill invoked? |
| **Instruction Following** | 20% | Did it follow all instructions? |
| **Task Completion** | 20% | Was the requested objective completed? |
| **Technical Accuracy** | 20% | Were conclusions correct and supported? |
| **Tool Usage** | 10% | Were tools used correctly? |
| **Evidence Quality** | 10% | Were conclusions linked to evidence? |
| **Output Contract** | 5% | Did output match required format? |
| **Execution Efficiency** | 5% | Was work done without waste? |

**Passing Threshold:** overall_score ≥ 80 AND no critical failures

### Evaluation Modes

**1. Pointwise Evaluation**
```
Evaluate ONE execution independently
  ├─ Read skill definition
  ├─ Review expected behavior
  ├─ Analyze execution trace
  └─ Score against rubric
  
Output: Single evaluation report
```

**2. Pairwise Evaluation**
```
Compare TWO executions (A vs B)
  ├─ Evaluate both independently
  ├─ Compare on each criterion
  ├─ Determine winner: A, B, or tie
  └─ Identify regressions & improvements
  
Output: Comparative analysis (which is better?)
```

**3. Reference-Based Evaluation**
```
Compare execution against golden answer
  ├─ Load reference/expected answer
  ├─ Compare agent response to reference
  └─ Score accuracy/completeness
  
Output: Accuracy report
```

**4. Trace-Based Evaluation**
```
Focus primarily on tool usage & behavior
  ├─ Verify correct tools invoked
  ├─ Check tool parameters
  ├─ Validate tool result interpretation
  └─ Identify unnecessary/duplicate calls
  
Output: Execution trace analysis
```

### Critical Failures

Conditions that force `passed = false` even if score is high:

- `SKILL_NOT_INVOKED` — Mandatory skill wasn't activated
- `SKILL_DEFINITION_NOT_AVAILABLE` — Skill docs couldn't be loaded
- `FABRICATED_TOOL_USAGE` — Agent claimed to use tool absent from trace
- `FABRICATED_EVIDENCE` — Agent invented results/findings
- `PROHIBITED_ACTION` — Agent did something explicitly forbidden
- `MISSING_REQUIRED_OUTPUT` — Mandatory deliverable not produced
- `DETERMINISTIC_CRITICAL_FAILURE` — Code validator failed
- `DANGEROUS_TECHNICAL_ERROR` — Error could cause harm
- `SENSITIVE_DATA_EXPOSURE` — Exposed confidential info
- `OUTPUT_SCHEMA_INVALID` — Output format didn't match spec

### Example Usage

**Test whether `technical-spec-generator` works correctly:**

```
/azure-devops-ticket-quality-judge evals/spec-gen-test/evaluation.json
```

**Compare two versions of a skill:**

```
/azure-devops-ticket-quality-judge Compare evals/v1.json with evals/v2.json
```

**Evaluate a custom agent:**

```
/azure-devops-ticket-quality-judge \
  Evaluate the execution in evals/custom-agent/ \
  using the skill at skills/custom-agent/SKILL.md
```

### Output

**Files Generated:**
```
documents/
├── evaluation-{eval_id}.json    ← Structured evaluation data
└── evaluation-{eval_id}.md      ← Human-readable report
```

**Report Includes:**
- Overall score (0-100) and pass/fail
- Criterion-by-criterion breakdown with evidence
- Deterministic check summary
- Critical failures (if any)
- Missing requirements
- Strengths and improvement areas
- Failure attribution (skill/model/tool/input/none)
- Executive summary

**Example Report:**
```markdown
# Evaluation Report: technical-spec-generator

Evaluation ID: eval-001
Status: ✅ PASSED
Overall Score: 87/100
Confidence: 0.92

## Criteria
| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Skill Activation | 5/5 | 10% | 10.0 |
| Instruction Following | 4/5 | 20% | 16.0 |
| Task Completion | 5/5 | 20% | 20.0 |
| Technical Accuracy | 4/5 | 20% | 16.0 |
| Tool Usage | 5/5 | 10% | 10.0 |
| Evidence Quality | 4/5 | 10% | 8.0 |
| Output Contract | 5/5 | 5% | 5.0 |
| Efficiency | 4/5 | 5% | 4.0 |
───────────────────────────────────────
TOTAL: 87/100 ✅

## Strengths
✔ Correctly activated technical-spec-generator skill
✔ Followed all skill instructions
✔ Produced complete spec with all required sections
✔ Used Azure DevOps MCP tools correctly
✔ Evidence-based recommendations

## Issues
⚠ Minor: Spec could have included more risk examples
⚠ Minor: Testing strategy could be more detailed

## Verdict
Execution passed the quality gate. Skill is functioning correctly.
```

### When to Use

**Use this skill when:**

1. **Testing a new skill** — Validate it works before deploying
   ```
   Create evaluation package → Run judge → Review report
   ```

2. **Comparing skill versions** — Verify improvements
   ```
   Evaluate v1 and v2 with same test case → Compare results
   ```

3. **Debugging failures** — Understand what went wrong
   ```
   Run evaluation → Judge identifies FABRICATED_EVIDENCE → Fix skill
   ```

4. **Continuous validation** — CI/CD pipeline integration
   ```
   Skill changed → Run judge on test cases → Blocks merge if fails
   ```

5. **Team training** — Show how to evaluate quality
   ```
   Run judge on example skill → Discuss criteria → Learn evaluation framework
   ```

### Not For

- **Evaluating business logic** — Judge evaluates process, not results
- **Code review** — Judge evaluates execution, not code quality
- **Performance testing** — Judge evaluates correctness, not speed
- **User satisfaction** — Judge evaluates adherence to spec

---

## 2. bulk-ticket-quality-analyzer

**Type:** Portfolio analyzer  
**Role:** Analyzes multiple ticket quality reports to identify patterns  
**Invocation:** `/bulk-ticket-quality-analyzer`  
**Dependency:** Multiple `ticket-quality-*.json` files in `documents/` folder

### What It Does

Scans all ticket quality reports and produces **portfolio-level insights**:

1. **Aggregates data** — Reads all `ticket-quality-*.json` files from `documents/`
2. **Identifies patterns** — What weaknesses repeat across tickets?
3. **Calculates metrics** — Average scores, distributions, trends
4. **Finds systemic gaps** — Which evaluation criteria are consistently weak?
5. **Prioritizes actions** — Which tickets/issues should be fixed first?
6. **Generates dashboard** — Saved as markdown + JSON reports

### Typical Use Case

**Scenario:** You've run the orchestrator on 15 tickets over the past month. Now you want to understand:
- Is our backlog getting better or worse?
- What's the most common problem across tickets?
- Which tickets should never enter a sprint?
- What should we teach the team?

**Solution:** Run the bulk analyzer.

### Input

**Automatic discovery** — No input needed. The skill:
1. Scans `documents/` directory
2. Finds all files matching `ticket-quality-*.json`
3. Parses and aggregates data
4. Generates insights

```bash
/bulk-ticket-quality-analyzer
```

### Output

**Files:**
```
documents/
├── bulk-ticket-quality-report.md   ← Human-readable dashboard
└── bulk-ticket-quality-report.json ← Structured data
```

**Report Sections:**

#### 1. Portfolio Overview
```
Total Tickets Analyzed: 15
Average Quality Score: 71/100 (Fair)

Score Distribution:
  Excellent (90-100):  2 tickets (13%)
  Good (80-89):        4 tickets (27%)
  Fair (70-79):        6 tickets (40%)
  Poor (60-69):        2 tickets (13%)
  Incomplete (<60):    1 ticket (7%)

Trend: ↗️ Improving (avg 65 last month → 71 this month)
```

#### 2. Criteria Breakdown
```
Criteria Performance (avg score out of 100):

Clarity:              85/100 ✅ Strongest
Acceptance Criteria:  78/100 ✅
Business Context:     75/100 ⚠️
Technical Info:       64/100 ⚠️ Weak
Dependencies:         62/100 ⚠️ Weak
Risks:               52/100 ❌ Weakest
Supporting Evidence:  58/100 ⚠️
Estimation:          68/100 ⚠️

Insight: Your team explains WHAT to build clearly,
but struggles with the RISKS and technical SCOPE.
```

#### 3. Common Weaknesses (Top 10)
```
Weakness #1: Missing risk analysis (12 tickets / 80%)
Weakness #2: Unclear technical scope (10 tickets / 67%)
Weakness #3: No rollback plan documented (8 tickets / 53%)
Weakness #4: Missing acceptance criteria details (7 tickets / 47%)
Weakness #5: No database schema changes specified (6 tickets / 40%)
...
```

#### 4. Red Flag Patterns
```
Most Common Red Flags:

1. Vague timeline ("ASAP", "soon") — 8 tickets
2. Uncertain scope ("maybe", "possibly") — 6 tickets
3. Missing dependencies ("and related work") — 5 tickets
4. Unspecified assumptions ("as usual", "like before") — 4 tickets

High-Risk Tickets (multiple red flags):
  - Ticket 12345: 4 red flags ⚠️⚠️
  - Ticket 12346: 3 red flags ⚠️
  - Ticket 12347: 3 red flags ⚠️
```

#### 5. Question Themes
```
Most Frequently Asked Questions (across all tickets):

Q1: "Which microservice handles this?" (asked in 9 tickets)
   → Suggests: Technical scope process is unclear

Q2: "What is the rollback strategy?" (asked in 7 tickets)
   → Suggests: Risk analysis not standard in process

Q3: "How many users are affected?" (asked in 6 tickets)
   → Suggests: Business impact not always documented

Q4: "What about API contracts?" (asked in 5 tickets)
   → Suggests: Missing template for API changes
```

#### 6. Tickets Below Threshold
```
Tickets Below 70 (Ready for Remediation):

Priority 1 (Below 60 - Incomplete):
  □ Ticket 12350: 55/100 — Major clarification needed
    Top issues: No AC, no technical scope, no risks

Priority 2 (60-70 - Poor):
  □ Ticket 12345: 62/100 — Multiple clarifications
    Top issues: Unclear scope, missing dependencies
  □ Ticket 12346: 68/100 — Significant gaps
    Top issues: Risk analysis missing, no estimation

Priority 3 (70 - Fair):
  □ Ticket 12347: 70/100 — Address before starting
  □ Ticket 12348: 70/100 — Minor gaps acceptable
```

#### 7. Recommendations
```
Portfolio-Level Actions:

Immediate (This Sprint):
  1. Remediate 3 tickets below 60 before sprint commitment
  2. Schedule 30-min training: "How to write risk analysis"
  3. Update ticket template to emphasize technical scope

Short-Term (Next 2 Weeks):
  1. Create Definition of Ready checklist (based on common gaps)
  2. Review tickets scoring 60-70, get quick clarifications
  3. Start "Quality of the Week" — highlight best tickets for team learning

Medium-Term (Next Month):
  1. Re-run analyzer to measure improvement
  2. If avg score > 75, roll out improved process company-wide
  3. Establish ongoing quality metrics dashboard

Long-Term:
  1. Track quality trends monthly
  2. Connect ticket quality to sprint success rates
  3. Use data to improve process
```

#### 8. Saved Data
```
Files Generated:
✓ documents/bulk-ticket-quality-report.md (human-readable)
✓ documents/bulk-ticket-quality-report.json (structured data)

Data Available for Integration:
  - Portfolio metrics (JSON)
  - Ticket-by-ticket breakdown
  - Criteria performance
  - Weakness frequencies
  - Red flag summaries
```

### Example Analysis Flow

**Input:** 15 ticket quality reports (from running orchestrator on 15 tickets)

**Processing:**
1. Read 15 × `ticket-quality-{id}.json` files
2. Aggregate all data
3. Calculate statistics
4. Identify patterns
5. Generate insights

**Output:**
- Overall portfolio health: 71/100 (Fair)
- Strongest area: Clarity (85/100)
- Weakest area: Risks (52/100)
- Most common issue: Missing risk analysis (80% of tickets)
- Actionable recommendation: Add risk analysis training

**Action:** Team learns "risk analysis" is the #1 training need

### Interpretation Guide

**What the scores mean:**

If **Risks = 52/100** but **Clarity = 85/100:**
- ✅ Team understands what to build
- ❌ Team doesn't analyze or document risks
- 🎯 **Action:** Risk analysis training

If **Technical Information = 64/100** across 80% of tickets:
- ❌ Systemic problem (not just one bad ticket)
- 🎯 **Action:** Improve ticket template, add process step

If **Estimation = 68/100** but **Acceptance Criteria = 78/100:**
- ✅ Team knows what "done" looks like
- ❌ Team struggles to size work
- 🎯 **Action:** Estimation workshop

### When to Use

**Use this skill when:**

1. **Pre-sprint planning**
   ```
   Run bulk analyzer → Identify tickets needing work
   → Fix them → Then commit to sprint
   ```

2. **Quarterly reviews**
   ```
   Run analyzer → Compare to last quarter
   → Measure improvement → Celebrate or adjust process
   ```

3. **Team training**
   ```
   Show team the report → "Here are our top 3 gaps"
   → Teach those topics → Re-run next month
   ```

4. **Process improvement**
   ```
   Analyze → Find pattern (e.g., "missing scope")
   → Update ticket template or process → Re-analyze to verify
   ```

5. **New team member onboarding**
   ```
   Show analyzer report → "This is what good looks like"
   → "Here's what we're struggling with" → Set expectations
   ```

6. **Continuous metrics**
   ```
   Monthly: Run analyzer → Track trend
   → If improving, continue process → If declining, intervene
   ```

### Not For

- **Real-time ticket assessment** — Use skill #2 (quality) directly
- **Individual ticket fixes** — Use skill #2 (quality) for specific recommendations
- **Predicting sprint success** — Correlates with quality but isn't causal

---

## Side-by-Side Comparison

| Aspect | Quality Judge | Bulk Analyzer |
|--------|---------------|---------------|
| **Purpose** | Evaluate skill execution quality | Evaluate ticket portfolio health |
| **Input** | Evaluation package + skill + trace | Multiple ticket-quality-*.json files |
| **Output** | Pass/fail + criteria scores | Portfolio insights + patterns |
| **Use Case** | Test & validate skills | Measure & improve backlog |
| **Scope** | Single execution or 2 executions | All tickets across portfolio |
| **Timing** | Run when testing code | Run monthly/before sprint |
| **Users** | Engineers building skills | Engineering managers/leads |
| **Metrics** | Instruction following, accuracy | Quality scores, weaknesses, trends |

---

## Integration with Main Pipeline

These supplementary skills integrate as follows:

```
Main Pipeline (Specs)          Supplementary Skills
═════════════════              ════════════════════

Orchestrator [#1] ────────────→ Quality Judge [#6]
   ↓                            (Validates orchestrator itself)
Quality [#2] ────────┐
   ↓                 │
Gate [#3] ──────────┤
   ↓                 │
Analysis [#4] ──────┤
   ↓                 └────→ Bulk Analyzer [#7]
Spec [#5]                    (Aggregates all quality reports)
   ├─→ ticket-quality-*.json
   └─→ execution-summary-*.md
```

**Data Flow:**
1. Run orchestrator on multiple tickets (generates quality-*.json)
2. Run bulk analyzer (reads all quality-*.json)
3. Run quality judge to validate any skill (ensures quality-*.json are trustworthy)

---

## Practical Workflow Example

**Month 1: Establish Baseline**
```
Step 1: Run orchestrator on 10 tickets
   → Generates: 10 × ticket-quality-{id}.json

Step 2: Run bulk analyzer
   → Report: Average 65/100 (Poor)
   → Weakest: Risks (48/100), Technical Info (61/100)
   → Common issue: Missing risk analysis (70% of tickets)

Step 3: Document findings
   → Team reads report → Realizes risks are gap
```

**Month 2: Improve**
```
Step 1: Team training on "How to write risk analysis"
Step 2: Update ticket template (add risk section)
Step 3: Run orchestrator on 10 new tickets

Step 4: Run bulk analyzer again
   → Report: Average 72/100 (Fair) — Up 7 points!
   → Risks now: 62/100 — Much better!
   → New common issue: Estimation still weak (58/100)
```

**Month 3: Continue**
```
Step 1: Estimation workshop
Step 2: Run orchestrator on 10 new tickets
Step 3: Run bulk analyzer
   → Report: Average 78/100 (Good) — Significant progress!
   → Ready to scale: Process is working
```

---

## Summary

**Quality Judge:** *"Is this skill doing what it's supposed to do?"*
- Validates skill/agent execution
- Evidence-based scoring
- Critical failure detection
- Used for testing and CI/CD

**Bulk Analyzer:** *"How healthy is our backlog?"*
- Portfolio-level insights
- Pattern identification
- Team improvement roadmap
- Used for planning and process improvement

Both skills are **optional** but valuable for teams that want to:
- Measure quality systematically
- Improve processes continuously
- Validate that skills work correctly
- Track progress over time

---

**Next:** See SKILLS-DETAILED-GUIDE.md for the core 5 skills, or README.md for quick start.
