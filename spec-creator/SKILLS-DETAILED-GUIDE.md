# Detailed Skills Guide

Complete explanation of all skills in the spec-driven development plugin, how they work, and how they fit together.

---

## Overview

The plugin contains **5 skills** that work together to convert Azure DevOps tickets into implementation-ready specifications:

```
Work Item ID
    ↓
[1] spec-driven-development-orchestrator
    ├─→ [2] azure-devops-ticket-quality (quality gate)
    ├─→ [3] solution-analysis-gate
    │   └─→ [4] technical-solution-analysis (if needed)
    ├─→ [5] technical-spec-generator
    └─→ Generates execution summary with metrics
    ↓
4 Artifacts + 1 Summary
```

---

## 1. spec-driven-development-orchestrator

**Type:** Orchestrator (entry point)  
**Role:** Coordinates all three core skills in sequence  
**Invocation:** `/spec-driven-development-orchestrator 12345` or "Generate the spec for ticket 12345"

### What It Does

The orchestrator is the **single entry point** to the entire pipeline. You provide it with a work item ID, and it:

1. **Validates configuration** — checks if default project is configured in settings
2. **Chains three skills** — calls quality → gate → spec in sequence
3. **Handles errors gracefully** — catches failures at each stage and surfaces them
4. **Tracks metrics** — records execution time and token usage
5. **Generates summary** — produces an execution summary file with metrics

### Input

- **Work Item ID** (required) — e.g., `12345`
- **Project Name** (optional if default configured) — e.g., `MyProject`

### Output

**Files Generated:**
```
documents/
├── ticket-quality-12345.md           ← Quality report
├── ticket-quality-12345.json         ← Quality data (JSON)
├── technical-solution-analysis.md    ← Architecture analysis
├── technical-spec.md                 ← Implementation spec
└── execution-summary-12345.md        ← Pipeline metrics & summary
```

**Chat Output:**
- Overall status (✅ Completed / ⚠️ Blocked / ❌ Failed)
- Quality score and gate decision
- Total execution time & token count
- Links to all generated artifacts

### How It Works

```
1. User invokes with ticket ID
   ↓
2. Load configuration (project name, default settings)
   ↓
3. START TIMER
   ↓
4. Invoke skill #2: azure-devops-ticket-quality
   ├─ Quality score ≥ 70? → Proceed
   └─ Quality score < 70? → Ask user to confirm or fix
   ↓
5. Invoke skill #3: solution-analysis-gate
   ├─ Check if documents/technical-solution-analysis.md exists
   ├─ If missing → invoke skill #4: technical-solution-analysis
   └─ If exists → skip (reuse existing)
   ↓
6. Invoke skill #5: technical-spec-generator
   ├─ Read work item & solution analysis
   ├─ Generate implementation spec
   └─ Save to documents/technical-spec.md
   ↓
7. END TIMER
   ↓
8. Collect metrics (duration, tokens)
   ↓
9. Generate execution summary
   ├─ Save metrics.json
   ├─ Call execution_summary_generator.py
   └─ Generate documents/execution-summary-12345.md
   ↓
10. Present summary to user
```

### Key Features

- **Idempotent** — Running twice doesn't duplicate work
- **Recoverable** — Handles mid-pipeline failures gracefully
- **Transparent** — Every decision is shown to the user
- **Measurable** — Tracks execution time and tokens
- **Configured** — Respects `.claude/settings.json` for default project

### When to Use

**Use the orchestrator when:**
- You want the full pipeline in one command
- You need timing and cost metrics
- You want everything saved in one place
- You're starting spec-driven development for a ticket

**Don't use when:**
- You only need quality assessment (use skill #2 directly)
- You only need solution analysis (use skill #4 directly)
- You only need spec generation (use skill #5 directly)

---

## 2. azure-devops-ticket-quality

**Type:** Analyzer  
**Role:** Evaluates ticket quality and identifies gaps  
**Invocation:** `/azure-devops-ticket-quality 12345`  
**Dependency:** None (standalone)

### What It Does

Scores a work item against **9 quality dimensions** and identifies gaps that would cause development problems. It acts like a **Staff Engineer** reviewing a ticket before committing to pick it up.

### Quality Dimensions (Weighted)

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| **Clarity** | 20% | Is the problem clear? Is the objective unambiguous? |
| **Acceptance Criteria** | 20% | How will we know it's done? What should/shouldn't the system do? |
| **Business Context** | 10% | Why is this needed? Who requested it? What's the business impact? |
| **Technical Information** | 15% | Which APIs, databases, services are involved? |
| **Dependencies** | 10% | What other work/teams/sprints are required? |
| **Risks** | 10% | Breaking changes? Database impacts? Security concerns? |
| **Supporting Evidence** | 5% | Screenshots, mockups, documentation, links? |
| **Estimation** | 5% | Story points or complexity assessment provided? |
| **Reproducibility** (bugs only) | 5% | Steps to reproduce? Current vs. expected behavior? |

### Scoring

- **90-100:** Excellent — Ready for development
- **80-89:** Good — Minor gaps, can proceed
- **70-79:** Fair — Significant gaps, address before starting
- **60-69:** Poor — Multiple issues, major clarification needed
- **Below 60:** Incomplete — Substantial revision needed

### Input

- **Work Item ID** or **Ticket Text** — Full ticket with title, description, AC, comments
- **Project Name** (optional if configured) — Azure DevOps project

### Output

**Files:**
```
documents/
├── ticket-quality-12345.md    ← Human-readable report
└── ticket-quality-12345.json  ← Structured data (for integration)
```

**Report Contents:**
1. **Overall Score** (0-100) with visual breakdown
2. **Strengths** — What the ticket does well
3. **Weaknesses** — Specific gaps and missing info
4. **Red Flags** — Vague language indicating assumptions ("maybe", "probably", "as usual", etc.)
5. **Suggested Questions** — Specific follow-up items to resolve gaps
6. **Recommendations** — Actions to improve before development

### Example Report

```markdown
# Ticket Quality Report: Fix tax calculation

Quality Score: 73/100 (Fair)

## Criterion Breakdown
- Clarity: 18/20 (90%)
- Acceptance Criteria: 15/20 (75%)
- Business Context: 8/10 (80%)
- Technical Information: 10/15 (67%)
- Dependencies: 5/10 (50%)
- Risks: 2/10 (20%)
- Supporting Evidence: 3/5 (60%)
- Estimation: 3/5 (60%)

## Strengths
✔ Clear problem statement
✔ Well-defined acceptance criteria
✔ Concise description

## Weaknesses
✖ No technical scope (which services? which APIs?)
✖ Dependencies not identified
✖ Risk analysis missing
✖ Timeline is vague ("ASAP")

## Red Flags
⚠ "ASAP" (timeline undefined)
⚠ No technical details for developers

## Suggested Questions
1. Which microservice handles tax calculations?
2. What is the exact buggy behavior with multiple discounts?
3. How many customers are affected?
4. Are there consuming APIs that depend on current behavior?
5. Is database migration required?
```

### Gate Threshold

**Quality Gate ≥ 70:**
- ✅ **Proceed** to next stage (gate passes)
- ⚠️ **Review** or ask user (7 to 8 points below 70)
- ❌ **Stop** and ask to fix (significantly below 70)

### When to Use

**Use when:**
- Reviewing a ticket before pulling into sprint
- Backlog grooming / pre-planning
- Quality auditing a set of tickets
- New team members learning ticket standards
- Training on what makes a good ticket

**Output:**
- Quality score (0-100)
- Specific weaknesses to fix
- Follow-up questions
- Recommendations

---

## 3. solution-analysis-gate

**Type:** Pipeline Controller  
**Role:** Ensures quality and solution analysis before spec generation  
**Invocation:** Called by orchestrator (not typically invoked directly)  
**Dependency:** Calls skills #2, #4, #5

### What It Does

A **pipeline control point** that decides whether to proceed to spec generation. It does two checks:

1. **Quality Gate** — Optional, re-checks ticket quality if needed
2. **File Existence Check** — Verifies solution analysis exists (generates if missing)
3. **Hands Off** — Passes context to spec generator

### Workflow

```
Input: work item ID

├─ Step 1: Check ticket quality (optional)
│  ├─ If score < 70 → Stop, ask user
│  └─ If score ≥ 70 → Continue
│
├─ Step 2: Check solution analysis file
│  ├─ If documents/technical-solution-analysis.md exists
│  │  └─ Skip generation (reuse existing)
│  └─ If missing
│     └─ Invoke skill #4 to generate it
│
└─ Step 3: Hand off to spec generator
   └─ Invoke skill #5 with ticket + analysis

Output: documents/technical-spec.md
```

### Key Features

- **Idempotent** — Running twice won't regenerate analysis
- **Smart** — Only generates what's missing
- **Gating** — Prevents weak tickets from becoming specs
- **Transparent** — Tells user what's happening at each step

### When to Use

**Direct invocation:**
```
"Generate the spec for ticket 12345"
or
/solution-analysis-gate 12345
```

**Typically:** Called by the orchestrator (skill #1), not invoked directly.

### Why It Exists

Prevents two problems:
1. **Weak tickets become weak specs** — Gate ensures minimum quality
2. **Stale analysis** — Checks file existence instead of blind regeneration

---

## 4. technical-solution-analysis

**Type:** Analyzer  
**Role:** Documents existing codebase architecture and conventions  
**Invocation:** Called by solution-analysis-gate if needed  
**Dependency:** Reads the actual codebase (filesystem)

### What It Does

**One-time analysis** of your codebase. It reads the repo structure and produces a snapshot of:
- Architecture and tech stack
- Key files and modules
- Coding conventions and patterns
- Existing risks and technical debt
- Integration points

This becomes the **grounding document** for all future specs on this codebase.

### Analysis Includes

1. **Architecture Overview**
   - System design (monolith, microservices, etc.)
   - Major components and their relationships
   - Data flow

2. **Technology Stack**
   - Languages, frameworks, libraries
   - Databases, caching, messaging
   - Deployment platforms

3. **Key Files & Modules** (with paths)
   - Essential services: `src/services/auth/`, `api/controllers/`, etc.
   - Data access: `models/`, `repositories/`
   - Utilities: `utils/helpers/`
   - Tests: `tests/`, `__tests__/`

4. **Coding Conventions**
   - Naming patterns (camelCase, snake_case, etc.)
   - Error handling approach
   - Logging standards
   - API response format
   - Test structure

5. **Existing Risks**
   - Known technical debt
   - Security concerns
   - Performance issues
   - Architecture limitations

6. **Integration Points**
   - External APIs used
   - Message queues
   - Third-party services
   - Inter-service communication

### Output

**File:**
```
documents/technical-solution-analysis.md
```

**Size:** 2,000-4,000 words (comprehensive but readable)

**Usage:** Referenced by all subsequent specs to ensure consistency

### Important Note

- **Run once per project** when architecture is stable
- **Update when** major architectural changes occur
- **Cached by design** — Won't regenerate if file exists
- **Shared across tickets** — All specs for this project use the same analysis

### When to Use

**Typically not invoked directly.** The solution-analysis-gate (skill #3) calls it automatically when:
- File `documents/technical-solution-analysis.md` doesn't exist
- User asks to "generate the spec for this ticket"

**Invoke directly when:**
```
/technical-solution-analysis
```
- You want to create/update the analysis
- Your codebase architecture changed significantly
- You're starting a new project

---

## 5. technical-spec-generator

**Type:** Generator  
**Role:** Produces implementation plan from ticket + codebase context  
**Invocation:** Called by solution-analysis-gate  
**Dependency:** Requires documents/technical-solution-analysis.md

### What It Does

Combines:
- **Work item requirements** (what to build)
- **Solution analysis** (how the system works)
- **Technical conventions** (team patterns)

→ Produces a **developer-ready spec** with concrete steps, risks, and decisions.

### Output Structure

**File:**
```
documents/technical-spec.md
```

**Typical Sections:**

1. **Overview**
   - What's being built and why
   - Success criteria (acceptance criteria from ticket)

2. **Scope & Approach**
   - What's in scope (do this)
   - What's out of scope (don't do this)
   - Design decision (e.g., REST vs GraphQL, sync vs async)

3. **Affected Components**
   - Which files/modules change
   - Which external services are involved
   - Database schema changes (if any)

4. **Implementation Steps** (Sequenced)
   - Step 1: Create database schema
   - Step 2: Add API endpoint
   - Step 3: Implement business logic
   - Step 4: Add client-side code
   - Step 5: Write tests
   - Step 6: Document

5. **Risk Assessment**
   - What could go wrong
   - Mitigation strategies
   - Breaking changes

6. **Testing Strategy**
   - Unit tests
   - Integration tests
   - Manual test cases

7. **Open Questions & Assumptions**
   - Things that need clarification
   - Assumptions made

8. **References**
   - Links to related tickets
   - Architecture diagrams
   - Design docs

### Example Spec Structure

```markdown
# Technical Spec: Implement User Authentication

## Overview
Add OAuth2 + JWT-based authentication to mobile app...

## Scope
✅ In Scope:
- OAuth2 provider integration
- JWT token generation and validation
- Refresh token mechanism
- Session management

❌ Out of Scope:
- Biometric authentication (future work)
- LDAP integration (not required)

## Affected Components
- `src/services/auth/` — Authentication logic
- `src/api/controllers/users.js` — User endpoints
- `frontend/screens/Login.tsx` — Login UI
- PostgreSQL: `users`, `sessions` tables

## Implementation Steps
1. Create database schema for sessions
2. Implement OAuth2 provider integration
3. Create JWT token generation service
4. Add token validation middleware
5. Implement refresh token flow
6. Update API endpoints for auth
7. Create login screen component
8. Add integration tests
9. Document authentication flow

## Risks
- Concurrent token refresh race conditions
  → Mitigation: Use optimistic locking on refresh
- Token expiration handling
  → Mitigation: Implement automatic refresh on 401
- CORS configuration complexity
  → Mitigation: Document setup clearly

## Testing
Unit Tests:
- Token generation and validation
- Refresh logic
- Error handling

Integration Tests:
- Full auth flow from login to API call
- Token expiration and refresh
- Session cleanup

Manual Tests:
- Login with invalid credentials
- Login after password reset
- Logout from multiple devices

## Open Questions
1. Should we support multiple concurrent sessions?
2. Token expiration time: 15 min or 1 hour?
3. Biometric fallback auth: required now or future?
```

### When to Use

**Typically called automatically** by solution-analysis-gate.

**Invoke directly when:**
```
/technical-spec-generator 12345
```
- You want to regenerate the spec for a ticket
- You have the solution analysis ready and want to jump to spec generation

---

## Skill Relationships

### Execution Flow

```
orchestrator (#1)
    ├─ calls quality (#2)
    │  ├─ Input: work item ID
    │  └─ Output: quality score, weaknesses, questions
    │
    ├─ calls gate (#3)
    │  ├─ calls solution-analysis (#4) if needed
    │  │  ├─ Input: codebase (filesystem)
    │  │  └─ Output: documents/technical-solution-analysis.md
    │  └─ Output: confirms analysis exists
    │
    └─ calls spec-generator (#5)
       ├─ Input: ticket + solution-analysis.md
       └─ Output: documents/technical-spec.md
```

### Data Dependencies

```
Ticket (from Azure DevOps)
    ↓
Quality (#2) → Quality Score + Weaknesses
    ↓
Gate (#3) → Quality Check + Analysis Check
    ↓
Analysis (#4) → Architecture Context
    ↓
Spec (#5) → Implementation Plan
    ↓
Orchestrator (#1) → Summary + Metrics
```

### Output Files Created

```
documents/
├── ticket-quality-{id}.md          ← From quality (#2)
├── ticket-quality-{id}.json        ← From quality (#2)
├── technical-solution-analysis.md  ← From analysis (#4)
├── technical-spec.md               ← From spec (#5)
└── execution-summary-{id}.md       ← From orchestrator (#1)
```

---

## Skill Selection Guide

### I want to...

**"Check ticket quality before development"**
→ Use skill #2: `azure-devops-ticket-quality`
- Fast (18 seconds)
- Tells you gaps to fix
- Output: quality score + weaknesses

**"Generate a spec for this ticket"**
→ Use skill #1: `spec-driven-development-orchestrator`
- Everything in one command
- Includes timing and cost metrics
- Output: spec + quality + analysis + summary

**"Update the architecture documentation"**
→ Use skill #4: `technical-solution-analysis`
- One-time per project
- Reads codebase structure
- Output: comprehensive architecture doc

**"Just generate the spec without quality check"**
→ Use skill #5: `technical-spec-generator` (directly)
- Requires existing solution-analysis.md
- Fastest (32 seconds for spec alone)
- Output: implementation spec only

**"Control the pipeline with gating"**
→ Use skill #3: `solution-analysis-gate`
- Gating logic (quality + file checks)
- Hands off to next stage
- Typically called by orchestrator

---

## Configuration & Prerequisites

### Required

1. **`.env`** — Azure DevOps PAT
   ```
   AZDO_PAT=<your-pat>
   AZURE_DEVOPS_EXT_PAT=<your-pat>
   ```

2. **`.mcp.json`** — MCP server configuration
   ```json
   {
     "mcpServers": {
       "azure-devops": {
         "command": "npx",
         "args": ["@azure-devops/mcp", "YOUR-ORG", "-a", "env"]
       }
     }
   }
   ```

### Optional (Recommended)

**`.claude/settings.json`** — Default project
```json
{
  "azureDevOpsTicketQuality": {
    "defaultProject": "MyProject"
  }
}
```
Lets you invoke skills with just the ticket ID.

---

## Performance Characteristics

| Skill | Typical Duration | Token Usage | When Slow |
|-------|-----------------|-------------|----------|
| #2 Quality | 18 seconds | 2,840 | Large tickets with many comments |
| #4 Analysis | 45 seconds | 8,920 | Large/complex codebase (1000+ files) |
| #5 Spec | 32 seconds | 5,240 | Highly complex requirements |
| **Total (Orchestrator)** | **~95 seconds** | **~17,000** | N/A |

**Cost estimate:** ~$0.17 per full pipeline run (at Claude 3.5 Sonnet pricing)

---

## Troubleshooting

### Quality score is too low

**Problem:** Skill #2 returns quality < 70

**Solution:**
- Review "Suggested Questions" in quality report
- Update ticket with clarifications
- Re-run quality check
- Proceed only if score improves or user explicitly accepts risk

### Solution analysis won't generate

**Problem:** Skill #4 fails or produces incomplete output

**Solution:**
1. Check repo structure is accessible
2. Verify codebase isn't too large (simplify or split)
3. Delete existing `documents/technical-solution-analysis.md`
4. Re-run orchestrator to regenerate fresh

### Spec doesn't match team conventions

**Problem:** Skill #5 generates spec that differs from team practices

**Solution:**
1. Review `documents/technical-solution-analysis.md` for documented conventions
2. Either:
   - Update the spec to match conventions
   - Update the solution analysis if conventions changed
   - Re-generate spec after updating analysis

### Skills not showing in `/` menu

**Problem:** Skills aren't discoverable

**Solution:**
1. Verify plugin installed: `claude plugin list`
2. Check `.env` has valid PAT
3. Reload Claude Code / IDE
4. Check IDE logs for errors

---

## Summary Table

| Skill | Type | Role | Speed | Tokens | When to Use |
|-------|------|------|-------|--------|------------|
| #1 Orchestrator | Controller | Entry point, chains all skills | 95s | 17,000 | Full pipeline |
| #2 Quality | Analyzer | Scores ticket quality | 18s | 2,840 | Ticket review, backlog grooming |
| #3 Gate | Controller | Quality + file gating | Varies | Varies | Pipeline control (called by #1) |
| #4 Analysis | Analyzer | Codebase architecture | 45s | 8,920 | Once per project, on architecture changes |
| #5 Spec | Generator | Implementation plan | 32s | 5,240 | Spec generation (called by #1 or #3) |

---

**Next:** See README.md for quick start, QUICKSTART.md for setup, or CLAUDE.md for project overview.
