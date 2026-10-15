---
name: planning
description: Turns an approved spec into a step-by-step implementation plan, independently reviewed before the user sees it. Use when a spec exists and code is about to be written, or when asked to write or review a plan.
---

# Planning

Goal: a plan another agent could follow with no extra context.

## Steps

1. **Read** the approved spec and `CLAUDE.md`. No approved spec? Use `forgelite:shaping` first. If the spec has no record of accepted/rejected improvements, present that list (shaping step 4) now, before writing the plan.
2. **Write the plan** to `docs/forgelite/plans/YYYY-MM-DD-<topic>.md` (or the project's existing plans folder):
   - Start with a 3-line summary and the spec path.
   - Break work into small tasks, each doing one thing with an exact file list. Size each so one subagent can finish it well inside its context (roughly under 10 files); split anything bigger.
   - Each task has: the failing test to write first (or, if it cannot be unit-tested, the device check to add to the QA checklist), the change, the command that proves it, and a commit message.
   - Mark which tasks are independent (can run in parallel) and which depend on others.
   - No placeholders such as "add validation". Say what, where, and how.
3. **Independent review.** Dispatch a fresh subagent, cold, scoped tightly (see Reviewer scope below), with `model: opus` and `effort` one level above this session's (`high` if unknown; stay at `max` if already there). It looks for: unstated assumptions, steps that cannot run in the stated order, contradictions with the spec, missing tests, scope that grew or shrank. It always checks the design-system doc, and the motion doc with its checklist whenever anything moves.
4. **Fold in findings.** Fix every real one. For any rejected finding, write why.
5. **Show the user** a 5-line plain summary, what the review found and changed, the decisions he must make, and the plan path. Not the full plan. Wait for approval. Then hand over to building: if this session is on Opus, tell the user to open a NEW Sonnet session and say "build the plan at <plan path>" (switching model mid-chat re-caches the whole conversation, which costs more). Otherwise use `forgelite:building`.

## Reviewer scope (saves tokens)

Give every reviewer: the exact files to read (spec, plan, and only the code and docs the plan touches), the questions to answer, and a limit of about 25 tool calls. No browsing the whole repo or re-reading large docs for background. It reports in under 400 words, ranked, with a fix for each finding.

## Rules

- Never send a plan straight from the author to the user.
- Files that change together live together. Do not plan unrelated refactors.
