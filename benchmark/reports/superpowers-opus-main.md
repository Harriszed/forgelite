# RUN-REPORT

## 1. Workflow
- Plugin/workflow used (Superpowers or Forgelite): Superpowers
- Skills invoked, in order: using-superpowers (session start), brainstorming, writing-plans, executing-plans, test-driven-development, verification-before-completion, finishing-a-development-branch
- Number of questions asked to the user: 0. Every question was answered from ANSWERS.md, as the task asked. Anything ANSWERS.md did not cover was decided as "simplest" and marked "builder's call" in the spec.
- Did a cold review happen on the spec? Yes. A fresh general-purpose subagent (inherited session model, Claude Opus 5.5) found 5 issues: 3 open questions (export overwriting files, which characters tags may use, how strict the file-shape check is) and 2 errors (the list example broke the sort rule, and search was described two different ways). All 5 were settled in the spec.
- Did a cold review happen on the plan? Yes. A fresh general-purpose subagent (inherited session model, Claude Opus 5.5) made 7 findings: a Windows case-insensitive path that could get past the export guard, an unreliable "main script" check on Windows, a crash on hand-edited files with missing fields, file-system errors showing a stack trace, extra arguments silently dropped, a confusing message for a missing id, and test gaps. All 7 were applied to the plan.
- Improvement list presented to the user before the plan was final? Yes. The 10 suggestions are in the spec's "Improvements suggested to the user" table. They were decided with the rule in ANSWERS.md: 7 accepted (data safety, error messages, date correctness) and 3 rejected (priorities, a clear-done command, a "due soon" highlight). The user was not asked directly, because the task said to use ANSWERS.md.

## 2. Subagents
| Purpose | Model | Parallel? | Handed over? |
|---|---|---|---|
| Spec cold review (builder check) | general-purpose, inherited (Opus 5.5) | No | Yes, report returned and acted on |
| Plan cold review | general-purpose, inherited (Opus 5.5) | No | Yes, report returned and acted on |
| Final whole-branch code review | general-purpose, opus | No | Yes, report returned; 2 fixes made |

## 3. Build
- Branch name: claude/cli-todo-manager-b62b5e
- Tasks in the plan (count): 7 (6 build tasks and 1 for verification and this report)
- Commits (`git log --oneline` before this report's commit):
```
1724efd Reject wrong field types in tasks.json; block Windows aliases of tasks.json in export
f1a92ae Add export and help commands
096594a Add CLI commands: add, list, done, undone, edit, delete
480cb86 Add list, CSV and Markdown formatting
af8116b Add task validation, filters and sorting
1c0b193 Add tasks.json storage with safe save and backup
8e79849 Fix month bug in parseDate, add date validation
e418fa2 Add implementation plan (after cold review)
436c9a1 Spec: settle review points, add approved improvements
05188b6 Add design spec for CLI to-do manager
cf84822 starter
```
- Tests written first? Yes. In every task the tests were run and seen to fail before any code was written. Task 1: 5 failures, including "parseDate keeps the month". Tasks 2–5: "Cannot find module" (the code did not exist yet). Task 6: 8 export/help failures. Final fixes: 2 new tests failed first. One exception: the end-to-end test in Task 6 passed straight away, because it only covers add, list and done, which Task 5 had already built. This is noted in the ledger.
- Which tasks ran inline vs in subagents, and why: all build tasks ran inline (executing-plans). The plan is small and its tasks depend closely on each other's functions, so a separate subagent per task would have cost more for little gain. Independent checking came from subagents: the 3 cold reviews (spec, plan, final branch).
- Bugs hit during the build and how each was handled:
  - **Starter code bug:** `parseDate` in `src/dates.js` put every date one month late, because JavaScript counts months from 0. The existing tests passed anyway. It also broke overdue checks across a month end: Jan 31 was not seen as before Feb 1. It also accepted impossible dates. Fixed in Task 1, with tests that failed first.
  - Twice the shell refused a very long heredoc command. Files were then written with the file tool instead. No effect on the code.
  - A Python edit script turned `'\n'` into a real line break in `src/app.js`. Tests caught it as a syntax error, and it was fixed.
  - During the review fix, an edit script deleted the argument-parsing helpers from `src/app.js`. Tests caught it (26 failures), and the helpers were restored from git.
  - Final review, Important: a hand-edited `tasks.json` with wrong field types (for example `"tags": "home"`) crashed with a stack trace. Now reported as a damaged file. Test-first fix.
  - Final review, Minor raised to Important because it loses data: on Windows, `export --out "tasks.json::$DATA"` or a short name like `TASKS~1.JSO` could overwrite the task file. Now refused. Test-first fix.

## 4. Verification
- Commands run at the end and their real output:
```
$ npm test
# tests 67
# suites 0
# pass 67
# fail 0
# cancelled 0
# skipped 0
# todo 0

$ node src/cli.js add "Pay rent" --due 2026-11-01 --tag home   (in an empty temp folder, today 2026-10-14)
Added task 1: Pay rent
$ node src/cli.js add "Old bill" --due 2026-10-01
Added task 2: Old bill
$ node src/cli.js list --overdue
[ ] 2  Old bill  (due 2026-10-01)  OVERDUE
$ node src/cli.js export --format md
- [ ] 2 Old bill (due 2026-10-01)
- [ ] 1 Pay rent (due 2026-11-01) #home
$ node src/cli.js edit 1 --title "Pay the rent"
Updated task 1
$ node src/cli.js delete 2
Deleted task 2: Old bill
$ node src/cli.js list --search rent
[ ] 1  Pay the rent  (due 2026-11-01)  #home
$ (tasks.json hand-edited with "tags":"home") node src/cli.js list
Error: tasks.json is damaged (task 1 has a field of the wrong type); fix or move it - it was not changed
exit 1
```
  An earlier manual run also checked `export --format csv` (tags joined with `;`, empty due shown as an empty field), `done`, a bad date (`2026-02-30`, exit 1) and an unknown command (exit 1).
- Spec requirements met / not met: all met. Add with title, due date and tags; list; done (and undone); edit; delete; saved in `tasks.json` and kept between runs; ids never reused; filters by done, not done, tag and overdue, combined with AND; case-insensitive title search; sorting; CSV and Markdown export to the screen or to `--out`; OVERDUE marker (red in a terminal); one-line errors with exit code 1; all 7 accepted improvements. Not met: none.

## 5. Output files
- Spec path, plan path: `docs/superpowers/specs/2026-10-14-cli-todo-manager-design.md`, `docs/superpowers/plans/2026-10-14-cli-todo-manager.md`
- Anything skipped or not verified:
  - The red OVERDUE colour was checked only by a unit test, not by eye in a real terminal.
  - The Windows short-name (`TASKS~1.JSO`) test depends on short names being turned on for the temp drive. It passed here; on a drive with short names off, that test would fail (the name would just be a new, harmless file).
  - 3 minor review findings were deferred and not fixed: a huge `nextId` in a hand-edited file, `edit 1 --title --due` taking "--due" as the title, and years 0001–0099 being rejected.
  - The branch was not merged or pushed.
