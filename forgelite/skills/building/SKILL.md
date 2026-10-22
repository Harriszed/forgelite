---
name: building
description: Executes an approved implementation plan test-first, one task at a time, using fresh subagents for independent tasks. Use when a plan is approved and code is about to be written or changed.
---

# Building

Goal: the plan, implemented, tested, committed in small steps.

## Before starting

Confirm you are on a feature branch, never `master`/`main`. Create one if not. If the checkout has unrelated uncommitted work, or the user wants their checkout left alone, use `forgelite:worktrees` first.

Building is best done on Sonnet (cheaper, and the plan already holds the thinking). If this session is running on Opus, say once: "Design is done. To save tokens, open a new Sonnet session and say: build the plan at <plan path>. (Switching model in this chat would re-cache everything.)" Then continue only if the user says to carry on here.

## Per task

0. If the task touches UI or motion, re-read the relevant design-system or motion-doc section first, if the project has one.
1. **Test first.** Write the failing test. Run it. Confirm it fails for the right reason. If it cannot be unit-tested, say so and add a device check to the QA checklist instead.
2. **Implement** the smallest change that passes. Nothing beyond the task.
3. **Run** the task's proving command plus the related tests. Read the output. When tasks run in parallel, each runs only its own tests, never the full suite (parallel runs can clash over shared files, ports or databases).
4. **Commit** with the planned message. One task, one commit. Stage only this task's files by name, never `git add -A` or `git add .` (parallel subagents share the working tree). Never stage `docs/forgelite/handovers/`. No AI co-author lines unless `CLAUDE.md` asks for them.

## Running the plan

- Independent tasks: dispatch one fresh subagent per task, never merging two tasks into one (in parallel only when their file lists do not overlap at all; tasks that share any file run one after another). Give each the task text, the spec and plan paths, and the files it may touch. Do not paste the plan or pass conversation history.
- Every subagent prompt ends with: "Reply in under 150 words: what changed, commit-ready file list, test result (pass/fail counts), anything blocked. No code, no pasted output." Long reports pile up in this chat and fill its context.
- If a subagent is still going after about 40 tool calls, it is probably too big or stuck: have it stop and hand over (see below) instead of continuing.
- Dependent tasks: run in order.
- After each parallel group finishes, run the full test suite once yourself before starting the next group.
- After each subagent returns, read its diff and test output yourself before moving on. A report is not proof.
- If a task is blocked or the plan is wrong, stop and tell the user what is wrong and your recommended fix. Never quietly improvise around the plan.
- If a bug appears, switch to `forgelite:debugging`.
- Work in batches of at most 8 tasks per chat, or fewer if the chat has had a lot of big outputs (long diffs, test logs, big files). A fresh session reloads the project context once, which is cheaper than carrying a growing chat. At the end of a batch, finish and commit the current task, write `docs/forgelite/handovers/progress.md` (tasks done with commits, tasks left, decisions, anything surprising), then tell the user to open a new Sonnet session and say: "continue the plan at <plan path>; progress note at <note path>". The final review and `forgelite:verifying` run only after the LAST task, always in full. Do not use `/loop` or timed wake-ups during a build.

## Model choice (save tokens)

Set `model` on every subagent. Never let it default to the main session's model.

| Task | Model |
|---|---|
| Pure mechanical edits only: rename, move, copy text, config. Never tests. | `haiku` |
| Normal feature work from a clear plan (default) | `sonnet` |
| Database migrations, security, payments or other money/data-loss risk. The plan must name the task and give the reason. | `opus` |

Sonnet is the default. Use `opus` for a build task only when the plan marks it with a reason; "tricky" alone is not one. Never rerun a task on a different model: if a subagent fails or is blocked, continue the same agent with SendMessage. Tiny tasks are cheaper done inline than with a subagent.

## Keeping subagents small (context limit)

Aim for each subagent to stay around 200-300k tokens of context. It cannot see its own count, so use these signs instead: it has read or changed about 25+ files, or pasted many long outputs, or has gone through several failed attempts.

Tell every subagent this rule in its prompt:
- If you are **nearly finished** with the task, finish it.
- Otherwise, stop and write `docs/forgelite/handovers/<task>-N.md`: what is done (with commits), what remains, files touched, decisions made, failing tests and what was tried. Then return and say you handed over.

When a subagent hands over, read the handover file, then continue the same agent if it is still available, otherwise dispatch a fresh subagent (same model) with only the task text, plan path and handover path. Two handovers on one task means the task is too big: stop and ask the user whether to split it.

## Finishing

When all tasks are done, run these steps in order without asking whether to: they are required, not optional.
1. Invoke `forgelite:requesting-review` (always Opus at high effort) on the full branch diff against the spec and plan.
2. Invoke `forgelite:receiving-review` on its report, adding a test for each real finding.
3. Invoke `forgelite:verifying` with the Skill tool (do not just run checks inline). Once it passes, delete `docs/forgelite/handovers/`: handover and progress notes are working files, never committed.
4. Invoke `forgelite:finishing` so the user chooses where the branch goes.

## Rules

- Follow `CLAUDE.md` conventions over habit.
- Never skip a failing test, loosen it, or delete it to get green.
