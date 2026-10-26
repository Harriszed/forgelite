---
name: receiving-review
description: Handles code review findings by checking each one against the code before changing anything. Use when a reviewer subagent reports, when a pull request gets review comments, or when the user passes on someone's feedback.
---

# Receiving review

Goal: every real finding fixed and proven, every wrong one answered with evidence. No blind agreement.

1. **Read all of it first.** If any item is unclear, ask about it before fixing anything: items are often linked.
2. **Check each finding** against the code, the spec and `CLAUDE.md`. Reproduce it where you can (a failing test, a command, the awkward input it names). Sort it: real, wrong (with the evidence), or a design question.
3. **Fix real ones** one at a time, Critical first: failing test, smallest fix, run the related tests. Commit each fix with a message naming the finding.
4. **Push back on wrong ones** in plain words with the evidence: the line, the test, or the spec clause. A reviewer can be wrong; agreeing to keep the peace ships bugs.
5. **Ask the user** about design questions, scope changes and anything that contradicts the spec, with your recommendation first. Do not grow the scope on a reviewer's say-so.
6. **Need a limit the spec did not set?** Pick a sensible one, record it in the spec, and tell the user.
7. **Report:** fixed (with commits), rejected (with the reason), waiting on the user. On a pull request, answer each comment on its own thread.

## Rules

- No "great catch", "you're absolutely right" or thanks: state what you checked and what you did.
- Never loosen or delete a test to make a finding go away.
- Re-run `forgelite:requesting-review` once, on the fix commits only, when the review had Critical findings or any fix touches security, money, limits or permissions. A fix in those areas is new code nobody has checked.
