---
name: finishing
description: Closes out a finished feature branch by letting the user choose to merge, open a pull request, keep it or discard it, then cleans up. Use after verifying passes at the end of a build, or when the user says the work is done or asks to merge, ship or wrap up a branch.
---

# Finishing

Goal: the branch ends up where the user chose, with nothing left behind.

1. **Verified?** If `forgelite:verifying` has not passed in this session on the current commit, run it first. Never finish on red.
2. **Check the state.** Working tree clean (commit or ask about leftovers), branch name, default branch, whether a remote exists, and whether this is a worktree (`git worktree list`). `docs/forgelite/handovers/` must be gone and never committed.
3. **Long-running branch?** If `CLAUDE.md` or the user says work collects on one branch (a phase or release branch) and the user does the rollout, do not ask: keep the branch, push only if the user asked, say so in one line and go to step 5.
4. **Otherwise ask once**, as a multiple choice with your recommendation first. Follow `CLAUDE.md` if it says how branches land (for example "PRs only"), and drop options it forbids:
   1. **Open a pull request** (recommended when there is a remote): push the branch, then open the PR with a plain summary, the spec and plan paths, and the verifying results.
   2. **Merge locally** into the default branch: update it, merge, run the full test suite on the result, and only then delete the feature branch.
   3. **Keep the branch** as it is, for later.
   4. **Discard it:** show what will be lost (`git log <default>..HEAD --oneline`) and require the user to type "discard" before deleting anything.
5. **Clean up.** For options 1, 2 and 4, if this is a worktree, leave it (`cd` to the main checkout) and `git worktree remove <path>`. For option 3, keep the worktree and tell the user its path.
6. **Report** in two lines: where the work is now (PR link, merge commit, or branch name) and anything the user must still do. If there is a rollout (migrations, secrets, deploys), list its steps in order and add: "For rollout questions, open a new Sonnet session and say: help me roll out <plan path>." This build chat is too large to keep asking in.

## Rules

- Merging into or pushing to the default branch happens only when the user picks it here and `CLAUDE.md` allows it.
- Never force-push, never rewrite shared history, never delete a branch with unmerged commits except through option 4.
