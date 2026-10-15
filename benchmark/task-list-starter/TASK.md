I want to turn this project into a command line to-do list manager.

I want to add tasks with a title, an optional due date and optional tags, list them, mark them done, edit them and delete them. The tasks must be saved in a file so they are still there next time. I want to filter the list (by done or not done, by tag, by overdue) and search by words in the title. I also want to export the list as CSV and as a Markdown checklist. Overdue tasks should be easy to spot.

For example: `node src/cli.js add "Pay rent" --due 2026-11-01 --tag home`, `node src/cli.js list --overdue`, `node src/cli.js export --format md`.

Please design it, plan it, build it and tell me when it is done.

If you need answers to questions, use ANSWERS.md in this folder instead of asking me.
