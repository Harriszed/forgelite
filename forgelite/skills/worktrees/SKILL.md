---
name: worktrees
description: Sets up an isolated git worktree for a feature branch, with dependencies installed and a clean test baseline. Use before building when the current checkout has unrelated uncommitted work, when the user wants to keep their checkout untouched, or when asked to use a worktree.
---

# Worktrees

Goal: a separate folder on its own branch, ready to build in, with tests passing before any change.

1. **Check first.** If `CLAUDE.md` says where worktrees go or forbids them, follow it. If Claude Code offers a built-in worktree tool in this session, use it and skip to step 4.
2. **Pick the folder.** Use an existing `.worktrees/` or `worktrees/` folder in the repo; otherwise ask the user once, recommending `.worktrees/`. A folder inside the repo must be git-ignored: run `git check-ignore -q <folder>`, and if it is not ignored, add it to `.gitignore` and commit that alone first.
3. **Create it.** `git worktree add <folder>/<branch> -b <branch>` from the branch the work should start from (usually the default branch, up to date). Then work only inside that folder.
4. **Set up.** Install dependencies with the project's own command (`CLAUDE.md`, or the lockfile: npm/pnpm/yarn, pip/uv/poetry, cargo, go, bundle). Copy nothing secret; if the app needs local env files, tell the user which ones.
5. **Baseline.** Run the full test suite. If anything fails before you have changed a line, stop and report it with the output, and ask whether to continue. Do not fix it silently: it is not part of the plan.
6. **Report** in two lines: the worktree path, the branch, and the baseline result (e.g. "212 tests, 0 failed").

## Rules

- One worktree per feature branch. Never create one inside another.
- Removing it happens in `forgelite:finishing`, never mid-build.
