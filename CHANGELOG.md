# Changelog

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
