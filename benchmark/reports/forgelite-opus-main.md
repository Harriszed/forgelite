# RUN-REPORT

Fill in honestly from what actually happened. Do not guess. Write "none" where it applies.

## 1. Workflow
- Plugin/workflow used (Superpowers or Forgelite): Forgelite
- Skills invoked, in order: forgelite:starting-work → forgelite:shaping → forgelite:planning → forgelite:building → forgelite:verifying
- Number of questions asked to the user: 0 (all answers taken from ANSWERS.md, as the request asked)
- Did a cold review happen on the spec? (who/what model/findings count): Yes — fresh general-purpose subagent, Sonnet, 15 findings. All folded in (e.g. dropped comma-tags and a separate `search` command as extra scope, defined exit codes, export details, id errors, file shape rules).
- Did a cold review happen on the plan? (who/what model/findings count): Yes — fresh general-purpose subagent, Opus (effort medium), 15 findings. 14 folded in (save-failure message, `--out tasks.json` guard, Windows run check, BOM, missing tests, option parsing rules, temp cleanup, branch named). Rejected: years below 1000 (out of scope) and a CSV BOM for Excel (not needed for this user).
- Improvement list presented to the user before the plan was final? (yes/no): yes — written into the spec as an itemised accepted/rejected list (5 accepted, 5 rejected), decided using the ANSWERS.md rule (accept data safety, error messages, date correctness; reject the rest). Not shown to the user interactively, because the request said to use ANSWERS.md instead of asking.

## 2. Subagents
| Purpose | Model | Parallel? | Handed over? |
|---|---|---|---|
| Spec cold review | sonnet | no | no |
| Plan cold review | opus (effort medium) | no | no |
| Task 2 — storage (`src/store.js`) | sonnet | yes (with Task 3) | no |
| Task 3 — task logic (`src/tasks.js`) | sonnet | yes (with Task 2) | no |
| Final build review (ran the CLI with awkward input) | opus | no | no |

## 3. Build
- Branch name: `claude/cli-todo-manager-afe1de`
- Tasks in the plan (count): 7 (6 build tasks + final check/report)
- Commits (paste `git log --oneline`):
```
3efcce2 Record limits added after build review
1688964 Fix review findings: guard tasks.json from export, reject huge ids and bad file data
a52b898 Add done, edit, delete and export commands
5c6cd37 Add command line with add, list and help
3ec0ec5 Add list, CSV and Markdown formats
d646e98 Add task logic
a553fb0 Add safe task storage
2fff9b5 Fix month bug in parseDate and add date validation
069918b Add to-do CLI implementation plan
fa18dad Add to-do CLI implementation plan
9a3668f Add to-do CLI design spec
cf84822 starter
```
  (plus the commit adding this report). Note: `fa18dad` is mislabelled — it actually holds the spec updates from the plan review; a script error meant the plan itself was committed separately in `069918b`.
- Tests written first? (yes/no, evidence): yes. Each task's test file was run before the code existed and failed for the right reason: dates (`does not provide an export named 'isValidDate'`), store and tasks (subagents reported `ERR_MODULE_NOT_FOUND`), format and cli (`ERR_MODULE_NOT_FOUND`), Task 6 (8 failing tests before the commands were added), review fixes (7 failing tests before the fixes).
- Which tasks ran inline vs in subagents, and why: Tasks 2 and 3 ran in parallel Sonnet subagents (independent, separate files; the lead reviewed the code, re-ran the tests and committed one at a time). Tasks 1, 4, 5, 6 and 7 ran inline: they were small, and Task 4–6 depended on earlier work, so a subagent would have cost more than doing them.
- Bugs hit during the build and how each was handled:
  - Starter code bug: `parseDate` in `src/dates.js` did not subtract 1 from the month, so January read as February and 2026-01-31 became 3 March. The starter test only checked the day, so it passed. Fixed with `m - 1`. `isOverdue` now compares the date text directly. Added tests for the month and for overdue across a month boundary.
  - Final review found 9 real issues, all fixed with tests first: export `--out` could overwrite tasks.json through a Windows short name (now checks file identity); a huge `nextId` caused duplicate ids; huge typed ids were silently rounded; a cleanup error hid the "could not save" message; line breaks in titles faked extra list lines; `--out ""` printed to screen; Windows device names (`con`) and names ending in dot/space were accepted; ids below 1, empty titles and bad tags in a hand-edited file loaded; "Exported 1 tasks" grammar.
  - Own slip: a shell heredoc turned `\r\n` in a regex into real line breaks, breaking two source files; caught by the test run and repaired at byte level.

## 4. Verification
- Commands run at the end and their real output (paste):
```
$ npm test
# tests 75
# pass 75
# fail 0

$ add Pay rent --due 2026-11-01 --tag home
Added task 1: Pay rent
$ add Renew passport --due 2026-09-01 --tag admin
Added task 2: Renew passport
$ add Buy milk --tag home --tag shop
Added task 3: Buy milk
$ list
[ ] 2  Renew passport  (due 2026-09-01)  #admin  OVERDUE
[ ] 1  Pay rent  (due 2026-11-01)  #home
[ ] 3  Buy milk  #home #shop
$ list --overdue
[ ] 2  Renew passport  (due 2026-09-01)  #admin  OVERDUE
$ list --tag home --todo
[ ] 1  Pay rent  (due 2026-11-01)  #home
[ ] 3  Buy milk  #home #shop
$ list --search RENT
[ ] 1  Pay rent  (due 2026-11-01)  #home
$ done 3
Marked task 3 as done
$ edit 2 --due 2026-12-01
Updated task 2
$ list --done
[x] 3  Buy milk  #home #shop
$ delete 1
Deleted task 1
$ export --format csv
id,title,due,tags,done
2,Renew passport,2026-12-01,admin,false
3,Buy milk,,home;shop,true
$ export --format md --out list.md
Exported 2 tasks to list.md
(list.md:)
- [ ] 2 Renew passport (due 2026-12-01) #admin
- [x] 3 Buy milk #home #shop
$ add Bad --due 2026-13-01
Error: due date must be a real date in YYYY-MM-DD form, got "2026-13-01"   (exit 1)
$ done 99
Error: no task with id 99   (exit 1)
$ fly
Error: unknown command "fly". Run: node src/cli.js help   (exit 1)
```
  (run with the real date, 2026-10-14, from a scratch folder that was then deleted)
- Spec requirements met / not met: all met — add (title, optional due, optional tags), list, done, edit, delete, saved to `tasks.json`, filters (done / todo / tag / overdue, combined with AND), search (case-insensitive), sorting, CSV and Markdown export to screen or `--out`, OVERDUE marker, one-line errors with exit code 1, ids never reused, and the 5 accepted improvements (safe save, damaged-file guard, real dates only, starter date fix, helpful errors). None not met.

## 5. Output files
- Spec path, plan path: `docs/superpowers/specs/2026-10-14-todo-cli-design.md`, `docs/superpowers/plans/2026-10-14-todo-cli.md`
- Anything skipped or not verified: the Windows short-name (`TASKS~1.JSO`) case is tested through a hard link (same protection path), not with a real short name, since short names may be off on the test drive. Behaviour on macOS/Linux was not run (built and tested on Windows only). PowerShell quoting of titles with quote marks was only tested automatically, not by hand.
