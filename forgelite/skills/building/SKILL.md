---
name: building
description: Executes an approved implementation plan test-first, one task at a time, using fresh subagents for independent tasks. Use when a plan is approved and code is about to be written or changed.
---

# Building

Goal: the plan, implemented, tested, committed in small steps.

## Before starting

Confirm you are on a feature branch, never `master`/`main`. Create one if not.

Building is best done on Sonnet (cheaper, and the plan already holds the thinking). If this session is running on Opus, say once: "Design is done. To save tokens, open a new Sonnet session and say: build the plan at <plan path>. (Switching model in this chat would re-cache everything.)" Then continue only if the user says to carry on here.

## Per task

0. If the task touches UI or motion, re-read the relevant design-system or motion-doc section first.
1. **Test first.** Write the failing test. Run it. Confirm it fails for the right reason. If it cannot be unit-tested, say so and add a device check to the QA checklist instead.
2. **Implement** the smallest change that passes. Nothing beyond the task.
3. **Run** the task's proving command plus the related tests. Read the output.
4. **Commit** with the planned message. One task, one commit. No AI co-author lines.

## Running the plan

- Independent tasks: dispatch one fresh subagent each (in parallel when files do not overlap). Give each the task text, the spec and plan paths, and the files it may touch. Do not paste the plan or pass conversation history.
- Every subagent prompt ends with: "Reply in under 150 words: what changed, commit-ready file list, test result (pass/fail counts), anything blocked. No code, no pasted output." Long reports pile up in this chat and fill its context.
- If a subagent is still going after about 40 tool calls, it is probably too big or stuck: have it stop and hand over (see below) instead of continuing.
- Dependent tasks: run in order.
- After each subagent returns, read its diff and test output yourself before moving on. A report is not proof.
- If a task is blocked or the plan is wrong, stop and tell the user what is wrong and your recommended fix. Never quietly improvise around the plan.
- If a bug appears, switch to `forgelite:debugging`.
- If this chat is getting long (many tasks done, big outputs), write a short progress note to `docs/forgelite/handovers/progress.md` (tasks done with commits, tasks left, decisions) so a new session can continue from the plan plus that note.

## Model choice (save tokens)

Set `model` on every subagent. Never let it default to the main session's model.

| Task | Model |
|---|---|
| Pure mechanical edits only: rename, move, copy text, config. Never tests. | `haiku` |
| Normal feature work from a clear plan (default) | `sonnet` |
| Tricky logic, concurrency, security, or a task that already failed once | `opus` |

Tiny tasks are cheaper done inline than with a subagent.

## Keeping subagents small (context limit)

Aim for each subagent to stay around 200-300k tokens of context. It cannot see its own count, so use these signs instead: it has read or changed about 25+ files, or pasted many long outputs, or has gone through several failed attempts.

Tell every subagent this rule in its prompt:
- If you are **nearly finished** with the task, finish it.
- Otherwise, stop and write `docs/forgelite/handovers/<task>-N.md`: what is done (with commits), what remains, files touched, decisions made, failing tests and what was tried. Then return and say you handed over.

When a subagent hands over, read the handover file, then dispatch a fresh subagent (same model) with only the task text, plan path and handover path. Two handovers on one task means the task is too big: stop and ask the user whether to split it.

## Finishing

When all tasks are done, run these two steps without asking the user whether to: they are required, not optional. First dispatch one cold reviewer (always Opus 5.5: `model: opus`, `effort: high`; never a cheaper model) on the full diff against the spec and plan. Give it the diff command, the spec and plan paths and a limit of about 40 tool calls; it reports in under 500 words. Tell it to look for correctness bugs first, then actually run the code with awkward input before reporting:
- Huge, tiny, zero, negative, empty, missing and repeated values.
- Wrong types or formats, and values that look like flags or options.
- Unclear or misleading error messages: each must name what is wrong and what is expected.
- Silent wrong answers (rounding, overflow, lost data), which are worse than crashes.
- Crashes or stack traces shown to the user, and anything that could hang or freeze.
- Spec requirements with no test.

Add a test for each real finding. If a limit is needed that the spec did not set, pick a sensible one, record it, and tell the user. Fold in real findings, then invoke the `forgelite:verifying` skill with the Skill tool (do not just run checks inline).

## Rules

- Follow `CLAUDE.md` conventions over habit.
- Never skip a failing test, loosen it, or delete it to get green.
