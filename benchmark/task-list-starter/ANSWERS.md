# Canned answers (use the same ones in every run)

Paste the matching answer if the agent asks. If it asks something not listed, answer "you decide, recommend what is simplest".

- Who is it for? Just me, on my own computer, from the terminal.
- Where are tasks saved? A JSON file called `tasks.json` in the folder the command is run from. Create it if missing.
- Task ids? Simple numbers (1, 2, 3...) that are never reused after a delete.
- Due date format? YYYY-MM-DD only. Reject anything else with a clear error.
- What is "overdue"? Due date is before today and the task is not done.
- Tags? Several per task, lowercase, no spaces. Filtering by a tag matches tasks that have it.
- Search? Case-insensitive match on the title.
- Combining filters? All given filters must match (AND).
- Sorting? By due date (soonest first, no due date last), then by id.
- Export CSV? Columns: id,title,due,tags,done. Quote fields with commas or quotes. Tags joined with `;`.
- Export Markdown? A checklist: `- [ ] 3 Pay rent (due 2026-11-01) #home`, `- [x]` for done.
- Export destination? Print to the screen; `--out file` writes to a file instead.
- Marking overdue in the list? Show "OVERDUE" next to the task.
- Bad input (unknown id, empty title, bad date, unknown command)? One-line error, exit code 1.
- Out of scope: reminders, recurring tasks, multiple lists, sync, a web page.
- Improvement suggestions: accept any about data safety (corrupt or missing file, not losing tasks), error messages, or date correctness; reject anything else.
- Approve the spec and the plan when they look reasonable.
