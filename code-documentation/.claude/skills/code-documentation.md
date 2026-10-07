---
name: code-documentation
description: Analyzes Git branch or commit changes and proposes concise, meaningful code comments that explain what changed and why, previewing every proposal before applying anything. Use when the user asks to document a branch's changes, annotate a diff with comments, add explanatory comments to changed code, review what a branch introduced, or produce a git change documentation report.
---

# Git Branch Change Documentation

Act as a Senior Software Engineer specializing in code review, Git change analysis, and source code documentation. Analyze the code changes introduced on a target branch (or specific commits), propose brief descriptive comments for each meaningful change, preview all proposals, and apply only what the user explicitly approves.

**Core rule: never modify a file without explicit user approval.**

## Configuration

**Check for `skill-config.json` first:** If a `skill-config.json` file exists in the project root, read all configuration from it. Only ask the user for values that are missing or unclear.

Otherwise, resolve these values before starting. If a value is missing from the user's request, use the default; if there is no safe default, ask the user.

**Path validation:** If `filePath` is empty, null, or not specified, default to analyzing all changed files in the repository (no path restriction). Log this clearly so the user understands the scope.

| Setting | Placeholder | Default | Notes |
|---|---|---|---|
| Target branch | `<BRANCH_NAME>` | `current branch` | Branch whose changes are being documented |
| Base branch | — | auto-detected merge base | Ask if ambiguous |
| Commit IDs | `<COMMIT_ID>` | `latest commit on branch` | Comma-separated, e.g. `AAA1, BBB2` |
| File path | `<FILE_PATH>` | all changed files | Glob pattern to filter files, e.g. `src/Services/**`, `**/*.cs` |
| Allowed file types | `<FILE_TYPES>` | inferred from repo | Comma-separated extensions, e.g. `.cs, .razor, .js, .ts, .sql` |
| Comment format | `<COMMENT_FORMAT>` | user's provided format | Must be followed exactly |
| Approval mode | — | `review-one-by-one` | `apply-all`, `review-one-by-one`, `select-specific`, or `cancel` |

If the comment format is not supplied, ask for it or propose a minimal default and confirm before generating anything.

## Workflow

`Analyze → Filter → Generate Comments → Preview → Request Approval → Apply → Validate → Report`

Do not skip the preview or approval phases, regardless of how small the change set is.

### 1. Analyze branch changes

Determine the base branch and the comparison range. Prefer the merge base so unrelated upstream commits are excluded. See `references/git-diff-commands.md` for the full set of recipes.

```bash
git merge-base <BASE_BRANCH> <TARGET_BRANCH>
git diff --stat <MERGE_BASE>..<TARGET_BRANCH>
git diff --name-status <MERGE_BASE>..<TARGET_BRANCH>
```

If `<COMMIT_ID>` is provided, scope the analysis to those commits instead:

```bash
git show --stat <COMMIT_ID>
git diff <COMMIT_ID>~1 <COMMIT_ID>
```

If `<FILE_PATH>` is provided and not empty, filter the diff results to only include files matching that glob pattern:

```bash
git diff --name-status <MERGE_BASE>..<TARGET_BRANCH> -- <FILE_PATH>
git diff <MERGE_BASE>..<TARGET_BRANCH> -- <FILE_PATH>
```

If `<FILE_PATH>` is empty, null, or not specified, analyze all changed files in the repository:

```bash
git diff --name-status <MERGE_BASE>..<TARGET_BRANCH>
git diff <MERGE_BASE>..<TARGET_BRANCH>
```

For each changed file, read the **complete diff without truncation** and the surrounding code so the purpose of the change can be understood in context.

Rules:

- **Read the complete diff** — do not use head/tail limits or truncate at arbitrary line counts. Process every line of every changed file.
- Include only committed changes introduced by the target branch or the specified commits.
- Exclude unrelated changes and files outside the comparison range.
- If `<FILE_PATH>` is specified and not empty, only process files matching that pattern.
- If `<FILE_PATH>` is empty or not specified, process all changed files in the repository.
- Only process files matching `<FILE_TYPES>`.
- Ignore generated code, lockfiles, vendored dependencies, binaries, and auto-generated artifacts.
- Never modify deleted files.
- If the target or base branch does not exist, report the problem and stop. Do not modify anything.

### 2. Filter to meaningful changes

Not every changed line deserves a comment. Treat a change as meaningful when it affects behavior, components (characteristics and behaviour), business logic, architecture, error handling, performance, security, data shape, or a notable technical decision.

**Scan thoroughly** — review ALL changes in the diff, not just a subset. Look for:
- Value changes (hardcoded values → variables, fixed → dynamic, colors, positions, sizes)
- Behavior changes (algorithm changes, conditional logic, event handling)
- Removed or modified comments (may indicate intentional design reversal)
- Method call changes or new method calls
- Conditional blocks or guard clauses

Skip:

- Whitespace, indentation changes only.
- Pure import reordering with no semantic impact.
- Changes already explained by a clear, adjacent comment.
- Anything whose purpose cannot be determined from the code or available context — flag these for manual review instead of guessing.

### 3. Generate descriptive comments

For each meaningful change:

- Write a short, clear, technically accurate comment.
- Explain **what changed and why** when the reason is reliably inferable from the code or context.
- Focus on behavior, business logic, architectural shifts, bug fixes, and important technical decisions.
- Do not restate what the code already plainly says.
- Use the correct comment syntax for the language — see `references/comment-syntax.md`.
- Follow `<COMMENT_FORMAT>` exactly.
- Prefer one comment per logical change over one comment per modified line.
- Never invent business requirements or implementation rationale.

### 4. Build the change preview

Before touching any file, present every proposal in a table. The full template lives in `references/preview-and-report-templates.md`.

| ID | File | Line | Change Description | Proposed Comment | Link |
|---|---|---|---|---|---|
| 1 | `src/Service.cs` | 45 | Updated validation logic | `<COMMENT>` | `<FILE_LINK>` |
| 2 | `src/Repository.cs` | 120 | Improved database query | `<COMMENT>` | `<FILE_LINK>` |

Line numbers must point at the proposed insertion location.

If there are more than 10 proposals, also write the preview to a Markdown file (e.g. `change-comments-preview.md`) so the user can review it comfortably. Do not write that file into the source tree unless the user agrees.

Link rules: only render a link as clickable when the environment actually supports it (IDE file navigation, repository URL). Otherwise leave the cell as plain text.

### 5. Request approval

After presenting all proposals, ask:

**How would you like to proceed?**

- **Option A — Apply All:** Apply all proposed comments.
- **Option B — Review One by One:** Present each proposed comment individually and request approval before applying it.
- **Option C — Select Specific Changes:** Apply only the proposals the user picks.
- **Option D — Cancel:** Do not modify any files.

Never apply changes automatically.

For one-by-one review: show the proposal with its surrounding code, let the user approve, reject, or request a wording change, and continue until every proposal has been reviewed. Apply only what was explicitly approved.

### 6. Apply approved changes

- Insert approved comments **ABOVE** (before) the line they describe, not below.
- For multi-line statements, place the comment above the first line.
- Preserve existing code behavior, formatting, and conventions. Do not refactor or reformat.
- Avoid duplicate comments.
- Respect language-specific documentation conventions (docblocks vs. inline comments).
- Revalidate the insertion location first if the file changed since the preview.
- Confirm no unrelated edits slipped in.

### 7. Final report

Summarize:

- Total files analyzed
- Total relevant changes identified
- Total comments proposed
- Total comments applied
- Total comments skipped or rejected

Then a detailed table using final line numbers after modification:

| File | Line | Applied Comment | Link | Status |
|---|---|---|---|---|
| `src/Service.cs` | 46 | `<COMMENT>` | `<FILE_LINK>` | Applied |
| `src/Repository.cs` | 121 | `<COMMENT>` | `<FILE_LINK>` | Applied |

Use `Applied`, `Rejected`, `Skipped`, or `Needs manual review` in the Status column.

## Constraints

- Never modify files without explicit approval.
- Never change executable logic.
- Never modify files outside `<FILE_TYPES>`.
- Never add unnecessary or redundant comments.
- Never assume the purpose of a change without sufficient evidence — flag it for manual review instead.
- Never commit or push automatically.
- If the target or base branch does not exist, report the issue without modifying files.
- If a change cannot be adequately understood, flag it rather than writing a speculative comment.

## Reference files

- `references/git-diff-commands.md` — git recipes for scoping, filtering, and inspecting changes.
- `references/comment-syntax.md` — comment syntax per language and placement guidance.
- `references/preview-and-report-templates.md` — preview table, approval prompt, and final report templates.