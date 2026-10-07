# Code-Documentation Skill

A skill that analyzes Git branch changes and automatically proposes meaningful code comments explaining *what changed and why*.

## Overview

This skill acts as a senior code reviewer that:
- Analyzes commits on a branch and identifies meaningful changes
- Generates concise, descriptive comments for each change
- Previews all proposals before applying anything
- Requires explicit approval before modifying any files
- Never touches code logic — only adds documentation

## When to Use

- **Document a feature branch** — Add explanatory comments to all changes before merging
- **Annotate a code review** — Explain what's changing and why to reviewers
- **Create change documentation** — Generate a report of significant changes in a PR
- **Improve code clarity** — Mark business logic, architectural decisions, or bug fixes with comments

## Installation in Your Project

If the skill is in a different location than your code project, use the installer script:

### Quick Install

Run this command in PowerShell:

```powershell
C:\IA-Inventory\code-documentation\scripts\install-skill.ps1 -ProjectPath "C:\Your\Project\Path"
```

Replace `C:\Your\Project\Path` with your actual project directory.

**What it does:**
- Creates `.claude/skills/` in your project
- Copies the Code-Documentation skill
- Copies `skill-config.json` template
- Shows success confirmation

**After installation:**
1. Reload Claude Code to activate the skill
2. Edit `skill-config.json` in your project to match your needs
3. Run `/code-documentation`

**Possible errors**
- If you get a message like "`cannot be loaded because running scripts is disabled on this system`"
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## How to Invoke

Use the `/Code-Documentation` skill command in Claude Code:

```
/Code-Documentation
```

### Option 1: Interactive Mode (default)

The skill will prompt you to provide:

| Parameter | Required? | Example | Notes |
|-----------|-----------|---------|-------|
| Target branch | No | `feature/auth-refactor` | Branch to analyze (defaults to current branch) |
| Base branch | No | `main` | Compared against (auto-detected if omitted) |
| Commit IDs | No | `abc123, def456` | Specific commits to analyze instead of full branch |
| File path | No | `src/Services/**` | Glob pattern to filter files (analyzes all files if omitted) |
| File types | No | `.ts, .tsx, .js` | Only analyze these file types (inferred from repo if omitted) |
| Comment format | No | `// Comment here` | Style to follow (ask if unsure) |
| Approval mode | No | `review-one-by-one` | How to apply: `apply-all`, `review-one-by-one`, `select-specific`, or `cancel` |

### Option 2: Configuration File Mode (faster)

Create a `skill-config.json` file in your project root:

```json
{
  "targetBranch": "feature/auth-refactor",
  "baseBranch": "main",
  "commitIds": [],
  "filePath": "src/Services/**",
  "fileTypes": [".ts", ".tsx", ".js", ".cs"],
  "commentFormat": "// {comment}",
  "approvalMode": "review-one-by-one"
}
```

When you run the skill, it will **automatically read from this config** and skip the prompts. You can still override values by mentioning them in your request.

**Benefits:**
- No interactive prompts each time
- Consistent configuration across runs
- Easy to version control your preferences
- Can have different configs for different branches

## Workflow

The skill follows this process:

### 1. **Analyze** 
Examines what changed in the target branch or commits, reading both the diff and surrounding code for context.

### 2. **Filter**
Identifies only meaningful changes—those affecting behavior, business logic, architecture, error handling, or security. Skips:
- Whitespace and formatting changes
- Pure renames with no semantic change
- Changes already explained by existing comments

### 3. **Generate Comments**
Creates brief, clear comments that explain *what changed and why*, following your project's comment style.

### 4. **Preview**
Shows a table of all proposed comments before any files are touched:

| File | Line | Change | Proposed Comment |
|------|------|--------|------------------|
| `src/auth.ts` | 45 | Added token validation | `// Validate JWT signature before accepting token` |

### 5. **Request Approval**
Asks how you'd like to proceed:
- **Apply All** — Add all proposed comments
- **Review One by One** — Approve/reject each comment individually
- **Select Specific** — Pick which proposals to apply
- **Cancel** — Don't modify anything

### 6. **Apply**
Inserts only approved comments near the relevant code, preserving all existing formatting and logic.

### 7. **Report**
Summarizes what was analyzed, proposed, applied, and skipped with a final detailed table.

## Example Usage

### Scenario: Document a feature branch before merging

```
User: "Please document the changes in my auth-refactor branch"

1. Skill analyzes the branch against main
2. Finds 12 meaningful changes across 5 files
3. Proposes comments for 10 changes (2 are already well-documented)
4. Shows preview table
5. User chooses "Review One by One"
6. For each proposal, user can approve, reject, or request rewording
7. Skill applies 9 approved comments
8. Final report shows which comments were added
```

### Scenario: Document specific commits

```
User: "Add documentation comments to commits abc123 and def456 in .cs and .ts files only"

1. Skill analyzes those 2 commits
2. Filters to C# and TypeScript files
3. Finds 6 relevant changes
4. Shows preview and requests approval
5. User selects Option A (Apply All)
6. All 6 comments are added to the files
```

## What Gets Commented

The skill looks for changes in:

✅ **Business logic** — New or modified algorithms, validation, calculations
✅ **Architecture** — Design patterns, layer shifts, dependency changes
✅ **Bug fixes** — Why a bug was fixed, what was wrong
✅ **Error handling** — New exception handling, defensive checks
✅ **Performance** — Optimizations, caching strategies
✅ **Security** — Auth/encryption changes, input validation
✅ **Data shape** — New fields, schema changes, API modifications

❌ **Skipped:**
- Whitespace, indentation, formatting
- Pure renames or moves
- Changes already explained by nearby comments
- Code you can't understand from context (flagged for manual review)

## Important Notes

- **Comment placement** — Comments are placed ABOVE the code they describe, following standard documentation conventions
- **Thorough scanning** — The skill analyzes ALL changes in the diff, not just obvious ones. It catches value changes, behavior modifications, and removed comments
- **Preview before applying** — Always review the preview table and select your approval option carefully
- **No code changes** — The skill only adds comments; it never modifies executable code
- **Language detection** — Automatically uses correct syntax for your language (Python `#`, JavaScript `//`, C# `//`, etc.)
- **Manual review** — If a change's purpose can't be determined from context, the skill flags it for you to review manually
- **No commits or pushes** — Changes are applied to your working files only; you commit and push manually

## Tips

- **For large branches:** Choose "Review One by One" to ensure all comments fit your style
- **For small changes:** "Apply All" is quick for 5-10 proposals
- **Different file types:** Specify file types to focus on certain parts of your codebase
- **Path filtering:** Use `filePath` in `skill-config.json` to analyze only specific directories (e.g., `src/Services/**`, `**/*.component.ts`). If empty or omitted, all changed files are analyzed
- **Consistency:** Run this skill regularly to keep your codebase well-documented as you make changes

## Reference

- See `references/comment-syntax.md` for language-specific comment styles
- See `references/git-diff-commands.md` for advanced Git filtering options
- See `references/preview-and-report-templates.md` for template details

## Questions?

If the skill flags changes for manual review or proposes something that doesn't fit your project, you can always reject individual proposals in the one-by-one review mode and request wording changes.
