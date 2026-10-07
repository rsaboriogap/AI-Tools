# Spec-Driven Development Pipeline Execution Summary

**Pipeline ID:** `orch-{timestamp}`  
**Work Item:** {ticket_id} — {ticket_title}  
**Status:** ✅ **Completed Successfully**  
**Date:** {date_time}

---

## Execution Timeline

| Stage | Status | Duration | Tokens Used |
|-------|--------|----------|------------|
| **1. Ticket Quality Assessment** | ✅ Completed | {duration_1} | {tokens_1} |
| **2. Solution Analysis Gating** | ✅ Completed | {duration_2} | {tokens_2} |
| **3. Technical Spec Generation** | ✅ Completed | {duration_3} | {tokens_3} |
| **Total Pipeline** | ✅ Completed | **{total_duration}** | **{total_tokens}** |

---

## What Was Generated

### 1️⃣ Ticket Quality Report
**File:** `documents/ticket-quality-{ticket_id}.md`

- **Quality Score:** {score}/100 ({rating})
- **Key Strengths:** {count} identified
- **Weaknesses to Address:** {count} identified
- **Suggested Questions:** {count} follow-up items

**Recommendation:** {proceed_status}

### 2️⃣ Solution Analysis
**File:** `documents/technical-solution-analysis.md`

- **Codebase Architecture:** {stack_summary}
- **Technology Stack:** {tech_stack}
- **Key Files & Modules:** {file_count} documented
- **Existing Risks:** {risk_count} identified
- **Conventions:** {convention_count} documented

**Status:** {new_or_reused}

### 3️⃣ Technical Specification
**File:** `documents/technical-spec.md`

- **Implementation Scope:** {scope}
- **Affected Components:** {component_count}
- **Implementation Steps:** {step_count}
- **Estimated Complexity:** {complexity}
- **Open Questions:** {question_count}
- **Key Risks:** {risk_count}

---

## Execution Metrics

### Token Usage Breakdown

```
Input Tokens:   {input_tokens:,}
Output Tokens:  {output_tokens:,}
Total Tokens:   {total_tokens:,}
Cost (est):     ${token_cost}
```

**Per Stage:**
- Stage 1 (Quality):     {tokens_1:,} tokens ({percent_1}%)
- Stage 2 (Analysis):    {tokens_2:,} tokens ({percent_2}%)
- Stage 3 (Spec):        {tokens_3:,} tokens ({percent_3}%)

### Time Breakdown

```
Elapsed Time:        {total_duration}
  - Stage 1:         {duration_1}
  - Stage 2:         {duration_2}
  - Stage 3:         {duration_3}
  - I/O & File Ops:  {duration_io}
```

**Efficiency:** {tokens_per_second} tokens/second

---

## Quality Gate Results

### Ticket Quality Assessment

**Score: {score}/100**

| Criterion | Score | Status |
|-----------|-------|--------|
| Clarity | {clarity_score}/100 | {clarity_status} |
| Acceptance Criteria | {ac_score}/100 | {ac_status} |
| Business Context | {context_score}/100 | {context_status} |
| Technical Information | {tech_score}/100 | {tech_status} |
| Dependencies | {deps_score}/100 | {deps_status} |
| Risks | {risk_score}/100 | {risk_status} |
| Supporting Evidence | {evidence_score}/100 | {evidence_status} |
| Estimation | {estimate_score}/100 | {estimate_status} |

**Gate Decision:** {gate_decision}

{gate_details}

---

## Next Steps

### For Development Teams

1. **Review the quality report** — Address flagged weaknesses to clarify scope
2. **Study the solution analysis** — Use `documents/technical-solution-analysis.md` as architecture guide
3. **Follow the technical spec** — `documents/technical-spec.md` is your implementation roadmap

### For Product Managers

1. **Review quality gaps** — Address "Weaknesses" section if ticket scored below 70
2. **Confirm acceptance criteria** — Ensure spec aligns with business goals
3. **Validate scope** — Check that implementation steps match sprint planning

---

## Generated Artifacts

All outputs are saved to the `documents/` folder:

```
documents/
├── ticket-quality-{ticket_id}.md      ← Quality assessment (human-readable)
├── ticket-quality-{ticket_id}.json    ← Quality assessment (structured)
├── technical-solution-analysis.md     ← Codebase context & architecture
└── technical-spec.md                  ← Implementation plan
```

---

## Support & Troubleshooting

**Issue:** Ticket quality score is below 70  
**Action:** Review the "Suggested Questions" in the quality report and update the ticket before development.

**Issue:** Solution analysis is stale  
**Action:** Delete `documents/technical-solution-analysis.md` and re-run the orchestrator to regenerate with current codebase state.

**Issue:** Spec doesn't match team conventions  
**Action:** Review `documents/technical-solution-analysis.md` to understand documented conventions, then update the spec or the codebase accordingly.

---

## Execution Details

**Pipeline Version:** v1.0  
**Orchestrator:** `spec-driven-development-orchestrator`  
**Skills Invoked:** 3  
**Files Generated:** 4  
**Errors Encountered:** {error_count}  

{error_details}

---

**Ready to start development?** Review the three generated documents above and begin with the technical spec.

For questions about the pipeline, see [spec-driven-development-orchestrator SKILL.md](../../skills/spec-driven-development-orchestrator/SKILL.md).
