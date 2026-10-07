# Preview and Report Templates

Copy these templates verbatim when producing the preview, the approval prompt, and the final report.

## 1. Change preview table

Present this before modifying any file.

```markdown
## Change Preview

| ID | File | Line | Change Description | Proposed Comment | Link |
|---|---|---|---|---|---|
| 1 | `src/Service.cs` | 45 | Updated validation logic | `// Validate input before persistence` | `src/Service.cs:45` |
| 2 | `src/Repository.cs` | 120 | Improved database query | `// Use indexed column to avoid full scan` | `src/Repository.cs:120` |
```

Notes:

- `Line` is the proposed insertion line, not the current diff line.
- `Link` is clickable only when the environment supports it. Otherwise render as plain text like `src/Service.cs:45`.
- If more than 10 proposals exist, also write this table to `change-comments-preview.md` after confirming with the user.

## 2. Optional detailed preview entry

When context is needed, expand a row into this form.

```markdown
### Proposal 1 — `src/Service.cs`

- **Line:** 45
- **Change:** Updated validation logic
- **Proposed comment:** `// Validate input before persistence`
- **Link:** `src/Service.cs:45`

**Context**

```csharp
// ...
public void Save(Order order)
{
    // Validate input before persistence
    if (order == null) throw new ArgumentNullException(nameof(order));
    _repository.Save(order);
}
// ...
```
```

## 3. Approval prompt

```markdown
**How would you like to proceed?**

- **Option A — Apply All:** Apply all proposed comments.
- **Option B — Review One by One:** Present each proposed comment individually and request approval before applying it.
- **Option C — Select Specific Changes:** Apply only the proposals you pick.
- **Option D — Cancel:** Do not modify any files.
```

Never proceed without an explicit answer.

## 4. One-by-one review loop

For each proposal, present:

```markdown
### Proposal <ID> of <TOTAL>

- **File:** `src/Service.cs`
- **Line:** 45
- **Change:** Updated validation logic
- **Proposed comment:** `// Validate input before persistence`

**Context**

```csharp
<surrounding code>
```

**Approve, reject, or request a wording change?**
```

Continue until every proposal has been reviewed. Apply only what was explicitly approved.

## 5. Final report

```markdown
## Final Report

- Files analyzed: <N>
- Relevant changes identified: <N>
- Comments proposed: <N>
- Comments applied: <N>
- Comments skipped or rejected: <N>

| File | Line | Applied Comment | Link | Status |
|---|---|---|---|---|
| `src/Service.cs` | 46 | `// Validate input before persistence` | `src/Service.cs:46` | Applied |
| `src/Repository.cs` | 121 | `// Use indexed column to avoid full scan` | `src/Repository.cs:121` | Applied |
| `src/Legacy.cs` | — | — | — | Needs manual review |
```

Status values:

- `Applied` — comment inserted successfully.
- `Rejected` — user declined the proposal.
- `Skipped` — not meaningful, duplicate, or excluded by file type.
- `Needs manual review` — purpose could not be determined from available evidence.

Line numbers in this table reflect the file **after** modifications.

## 6. Error report

If the target or base branch does not exist, or the comparison cannot be performed:

```markdown
## Cannot Proceed

- Reason: <e.g. base branch `origin/main` not found>
- Files modified: none
- Suggested next step: <e.g. confirm the base branch name>
```

Stop immediately. Do not modify any files.