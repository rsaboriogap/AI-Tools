# Comment Syntax by Language

Use the correct comment form for each language, and follow `<COMMENT_FORMAT>` exactly when one is supplied. If `<COMMENT_FORMAT>` conflicts with the language's syntax, `<COMMENT_FORMAT>` wins for content while the language's delimiters still apply.

## Inline and block comments

| Language | Single line | Multi-line / block | Doc comment |
|---|---|---|---|
| C# | `// comment` | `/* comment */` | `/// <summary>...</summary>` |
| Razor | `@* comment *@` | `@* ... *@` | `@* ... *@` |
| JavaScript | `// comment` | `/* comment */` | `/** ... */` |
| TypeScript | `// comment` | `/* comment */` | `/** ... */` |
| SQL | `-- comment` | `/* comment */` | `-- comment` |
| Python | `# comment` | `"""docstring"""` | `"""docstring"""` |
| Java | `// comment` | `/* comment */` | `/** ... */` |
| Kotlin | `// comment` | `/* comment */` | `/** ... */` |
| Go | `// comment` | `/* comment */` | `// comment` above declaration |
| Rust | `// comment` | `/* comment */` | `/// ...` |
| C / C++ | `// comment` | `/* comment */` | `/** ... */` |
| Ruby | `# comment` | `=begin ... =end` | `# comment` |
| PHP | `// comment` | `/* comment */` | `/** ... */` |
| Shell | `# comment` | `: <<'EOF' ... EOF` | `# comment` |
| YAML | `# comment` | — | `# comment` |
| JSON | not supported | not supported | not supported — skip JSON |
| HTML | `<!-- comment -->` | `<!-- ... -->` | `<!-- ... -->` |
| CSS / SCSS | `/* comment */` | `/* ... */` | `/* ... */` |
| Markdown | `<!-- comment -->` | `<!-- ... -->` | — |

## Placement rules

- Put the comment immediately **above** the changed block for most languages.
- For SQL, place the comment above the statement, not inside it.
- For YAML and JSON-like configs, keep comments on their own line above the key.
- For Razor, wrap the comment so it is not rendered in output.
- For C#, prefer `///` doc comments on public members and `//` inline comments inside method bodies.
- For Python, prefer `#` above the block unless documenting a module, class, or function, where a docstring is more appropriate.
- Never place a comment between a decorator or attribute and its declaration.
- Never break an existing multi-line expression to insert a comment.

## Style guidance

- Keep comments short — one or two lines where possible.
- Start with a capital letter and end with a period only if the format requires it.
- Use the imperative or descriptive mood consistently within a single change set.
- Avoid trailing punctuation styles that conflict with `<COMMENT_FORMAT>`.
- Do not repeat the code's own wording; explain intent, reason, or consequence.

## Duplicate avoidance

Before inserting, scan the surrounding 10 lines for an existing comment that already covers the change. If one exists, skip the proposal and note it as `Skipped` in the final report.