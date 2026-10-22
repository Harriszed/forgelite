---
name: requesting-review
description: Dispatches one cold, tightly scoped Opus code review of a diff against its spec and plan. Use after all build tasks are done, after a large bug fix, before finishing a branch, or when the user asks for a code review.
---

# Requesting review

Goal: an independent reviewer who has not seen this chat finds the bugs before the user does.

1. **Fix the range.** Base is where the branch left the default branch (`git merge-base HEAD <default-branch>`); head is `HEAD`. Commit or stash first so the diff is complete.
2. **Dispatch one reviewer**, always `model: opus`, `effort: high`, never a cheaper model. Give it only: the diff command (`git diff <base>..HEAD`), the spec and plan paths (if any), the `CLAUDE.md` path, a limit of about 40 tool calls, and this brief:
   - Correctness bugs first, then actually run the code with awkward input: huge, tiny, zero, negative, empty, missing and repeated values; wrong types or formats; values that look like flags or options.
   - Silent wrong answers (rounding, overflow, lost data), which are worse than crashes.
   - Crashes or stack traces shown to the user, and anything that could hang or freeze.
   - Error messages that do not say what is wrong and what is expected.
   - Spec requirements with no test, and changes outside the plan.
   - Security: untrusted input reaching a shell, query, file path or HTML; secrets in the diff.
   - Report in under 500 words, ranked: **Critical** (wrong result, data loss, security), **Important** (bug in a likely path, missing test), **Minor** (clarity, small cleanups). Each finding: `file:line`, what goes wrong, how it was shown, the suggested fix. Say plainly if nothing real was found.
3. **Act on it** with `forgelite:receiving-review`.

## Rules

- Never review your own diff and call it independent. The reviewer starts cold.
- Do not paste the diff or the chat into the prompt; the reviewer runs the command itself.
