# Technical Solution Analysis — Report Template

Default shape, not a fixed contract. No placeholders, no scores/percentages. Every finding names a file/folder/package. Drop what doesn't apply, expand what matters, add sections not listed here if needed.

```markdown
# Technical Solution Analysis

# 1. Architecture

## Observed Architecture
Plain-terms description based on what the code shows.

### Layers / Modules
- <layer/module> — <path(s)>

### Projects
| Project | Type | Path |
|---------|------|------|
| <name> | <type> | <path> |

### Dependency Graph
```text
<ASCII dependency tree>
```

### Dependency Notes
- <observation with path, or "None notable">

---

# 2. Project Scope
- Projects/services/apps: <n> — <paths>
- APIs: <list with paths>
- External services: <list>

---

# 3. Technology Stack
## Backend
- <tech> — <path>
## Frontend
- <tech> — <path>
## Data / Messaging
- <tech> — <path or config file>

---

# 4. Frameworks & Libraries
| Framework/Library | Where used |
|---|---|
| <name> | <path(s)/manifest entry> |

---

# 5. Design Patterns & Conventions
### Patterns in use
- <pattern> — <path(s)>
### Conventions to follow
- <convention> — <path(s)>
### Anti-patterns worth flagging
- <anti-pattern> — <path(s)>

---

# 6. Code Quality
- <observation, e.g. duplication, oversized files> — <path(s)>

---

# 7. Security
## Authentication
- <mechanism> — <path(s)>
## Notable findings
- <finding> — <path(s)>

---

# 8. Testing
- Tooling: <name(s)> — <path(s)>
- Coverage summary: <what's covered/not, with paths to test folders>

---

# 9. Observability
## Logging
- <mechanism> — <path(s)>
## Metrics / Tracing
- <mechanism, or "None found">

---

# 10. Dependencies
- Notable outdated/risky: <name(s)> — <manifest file, current version>

---

# 11. Scalability
(include only if the planned work touches performance, concurrency, or scale)
- <observation> — <path(s)>

---

# 12. Recommendations
## High Priority
- <recommendation> — <why, path reference if applicable>
## Medium Priority
- ...
## Low Priority
- ...

---

# Overall Assessment
<2-4 sentences: how the system is built, key risks/constraints for the planned work, highest-leverage next steps — pointing back to sections above, not restating scores.>
```
