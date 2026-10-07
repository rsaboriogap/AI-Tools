# Technical Spec — Report Template

Default shape, not a fixed contract. Every proposed change names a file/module. Drop what doesn't apply, expand what matters.

```markdown
# Technical Spec: <Work Item Title>

**Work item:** <ID/link, if applicable>
**Source analysis:** documents/technical-solution-analysis.md

---

# 1. Summary
2-4 sentences: what's being built/fixed, and why, in plain terms.

---

# 2. Requirements
## In scope
- <requirement, derived from ticket/acceptance criteria>
## Out of scope
- <explicitly excluded, or "None called out — confirm before starting">

---

# 3. Current State
Relevant facts pulled from the Technical Solution Analysis — only what bears on this change.
- <fact> — <path/module, per the analysis>

---

# 4. Proposed Approach
Plain-terms description of the implementation strategy and why it fits the existing conventions.

## Affected Components
| Component | Change | Path |
|---|---|---|
| <name> | <what changes> | <path> |

## Decision Points
- <place where the ticket/analysis leaves a choice — recommendation + why, or "None">

---

# 5. Implementation Steps
1. <step> — <file(s)/module(s)>
2. <step> — <file(s)/module(s)>
...

---

# 6. Risks & Open Questions
- <risk or unknown> — <why it matters, who should confirm>

---

# 7. Testing Strategy
- <what needs coverage, mapped to acceptance criteria>
- Existing test tooling to use: <per the analysis>

---

# 8. Acceptance Criteria Mapping
| Acceptance Criterion | Verified By |
|---|---|
| <criterion from ticket> | <step/test that satisfies it> |
```
