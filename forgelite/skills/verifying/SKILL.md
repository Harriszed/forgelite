---
name: verifying
description: Proves work is finished before claiming it. Use before saying done, fixed or passing, before committing or opening a PR, when the user asks "is it done?" or "does it work?", and at the end of every phase or significant update.
---

# Verifying

Goal: no claim without evidence from this session.

1. **Run the project's checks** (see `CLAUDE.md` for the commands: tests, type check, lint, build). Read the real output.
2. **Check against the spec.** Go through each requirement and point to where it is met. Missing items are not done.
3. **Review your own diff** (`git diff`): leftover logging, dead code, unrelated changes, secrets, files that should not be committed.
4. **Run `CLAUDE.md`'s end-of-phase procedure** if it has one. Do every step it lists and report each result.
5. **Report plainly:**
   - What passed, with the numbers (e.g. "212 tests, 0 failed").
   - What failed or was skipped, and why.
   - What the user must check on a device or in the app.
   - Exactly what to do next: the run command (and whether a full rebuild is needed, and why) and the QA checklist path, if there is one.

## Rules

- Never write "should work", "probably fixed" or "done" without a command's output to back it.
- A failing check is reported with its output, not worked around.
- Anything you could not run is listed as not verified.
- Never merge or push to `master`/`main`; `CLAUDE.md` gates that.
