---
name: solution-analysis-gate
description: Checks whether the ADO ticket is high-quality enough to spec from and whether documents/technical-solution-analysis.md already exists, before moving on to the technical-spec-generator skill — so spec generation is never built on a vague ticket or on stale/missing architectural context. Use this skill whenever the user is running the spec-driven-development pipeline and asks to "check for the technical solution analysis," "make sure the solution analysis exists before generating the spec," "proceed to the technical spec generator," or similar staged-workflow language — e.g. "let's move to spec generation for this ticket" or "generate the spec, but make sure the analysis is there first." If the ticket looks weak, it flags that before continuing. If the solution analysis file is missing, this skill first runs the technical-solution-analysis skill to produce it, then hands off to technical-spec-generator. If both checks already pass, it skips straight to technical-spec-generator. Trigger any time a pipeline step references documents/technical-solution-analysis.md or asks to gate/guard progression into spec generation.
---

# Solution Analysis Gate

A pipeline-control skill. It does no analysis itself — it decides whether `azure-devops-ticket-quality` and/or `technical-solution-analysis` need to run before handing off to `technical-spec-generator`, so the spec generator is never invoked against a vague ticket or without grounded architectural context behind it.

## Workflow

1. **Gate on ticket quality (if a ticket is in play).**
   If this pipeline run is seeded from an ADO work item (ID/URL or pasted ticket text), run `azure-devops-ticket-quality` against it first.
   - **Score ≥ 70 (Fair or better)** → proceed to step 2.
   - **Score < 70** → stop and surface the quality report (score, weaknesses, suggested questions) to the user. Ask whether to proceed anyway or resolve the gaps first. Don't silently continue into spec generation with a ticket you already know is under-specified — that just pushes the guessing downstream onto `technical-spec-generator`, which explicitly refuses to fabricate requirements.
   - If the user explicitly says to skip the quality check (e.g. "just generate the spec, skip quality review"), honor that and go straight to step 2.

2. **Check for the solution analysis file on disk.**
   Look for `documents/technical-solution-analysis.md`, relative to the project root. Verify this by actually checking the filesystem (e.g. `Read` or `test -f documents/technical-solution-analysis.md`) every time this skill runs — a file mentioned earlier in conversation may since have been deleted, moved, or belong to a different repo, and a stale assumption here defeats the point of the gate.

3. **Branch on the result.**
   - **File exists** → skip generation. Tell the user: "Found existing `documents/technical-solution-analysis.md` — skipping analysis." Go to step 4.
   - **File does not exist** → invoke the `technical-solution-analysis` skill. It already saves to `documents/technical-solution-analysis.md` by default (creating `documents/` if needed) — don't redirect its output elsewhere. If `technical-solution-analysis` isn't available/loaded for some reason, say so explicitly and stop; don't fabricate a report to unblock the pipeline.

4. **Hand off to `technical-spec-generator`.**
   Once the file is confirmed present (pre-existing or freshly generated) and the ticket has cleared the quality gate (or the user explicitly waived it), invoke it with:
   - The path to `documents/technical-solution-analysis.md`
   - The originating work item/ticket, and any other pipeline context already gathered in this conversation

## Notes

- **Idempotent by design.** Running this twice in a row shouldn't regenerate the analysis the second time — that's the entire point of gating on the file's existence rather than on conversation memory.
- **Never silently overwrite.** If the user wants a fresh analysis even though one exists, that's a distinct request ("regenerate the solution analysis") they need to say explicitly — this gate's job is to avoid unnecessary regeneration, not to enforce staleness.
- If `documents/` doesn't exist at all, create it as part of running `technical-solution-analysis` in step 3 (that skill already handles this) — don't create an empty `documents/` directory speculatively before knowing generation is needed.
- The ticket-quality gate (step 1) is a checkpoint, not a hard block — the user always has final say on whether to proceed with a weak ticket. Its job is to make sure that choice is made knowingly, not skipped by default.
