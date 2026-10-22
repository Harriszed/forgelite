# Changelog

## Unreleased
- Build tasks stage only their own files by name (never `git add -A`), so parallel subagents cannot commit each other's work.
- Design-system, motion-doc, QA-checklist and rebuild steps apply only when the project has them (no more React Native-specific wording).
- Gender-neutral wording; final review says "Opus" rather than a pinned version.
- `token_report.py` exits with a clear message when no transcripts match, and documents `--haiku-price`.
- README: corrected instruction lines (201) and session-start text size (336 chars).

## 0.4.4
- Builds run in batches of at most 8 tasks (fewer after big outputs); then a progress note and a fresh session. Final review and verifying still run in full after the last task.
- The plan reviewer flags tasks over about 8 files or more than one concern, and parallel tasks that share a file.
- Tasks that share a file run in sequence, never in parallel.
- No `/loop` during builds.

## 0.4.3
- Build tasks default to Sonnet. Opus only for migrations, security and payments, with the reason written in the plan.
- One task per subagent, never merged.
- A failed task is never rerun on a different model; the same agent is continued.
- The main build chat hands over to a new session at about 150k tokens of context.

## 0.4.2
- Tasks are sized for about 40 tool calls per subagent; a subagent still going after about 40 hands over instead of continuing.

## 0.4.1
- `building`: the final Opus review and `forgelite:verifying` run automatically; they are no longer offered as optional.

## 0.4.0
- Renamed from Forge to Forgelite (skill prefix is now `forgelite:`; default folders are `docs/forgelite/...`).

## 0.3.2
- Reviewers get an exact file list, a tool-call limit and a word limit.
- Build subagents reply in under 150 words.
- `building` invokes `forgelite:verifying` explicitly, and writes a progress note when the chat gets long.

## 0.3.1
- Handover to building is a new Sonnet session, not a mid-chat model switch (a switch re-caches the whole conversation).

## 0.3.0
- Final code review is always Opus 5.5 at high effort.
- Shape and plan on Opus, build on Sonnet.

## 0.2.x
- Session-start hook (320 characters) so `forgelite:starting-work` triggers reliably.
- Model per subagent; subagent context limit and handover files.
- Final reviewer runs the code with awkward input before reporting.

## 0.1.0
- First six skills: starting-work, shaping, planning, building, debugging, verifying.
