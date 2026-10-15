---
name: starting-work
description: Reads the project's CLAUDE.md and picks the right Forge step. Use at the start of any task that adds, changes or fixes app code, before reading code or asking questions. Skip for quick questions and one-line fixes.
---

# Starting work

1. Read the project's `CLAUDE.md` first. Its rules beat any Forge rule. If it defines a process (reviews, design docs, end-of-phase steps), follow that and use Forge only to fill gaps. Follow its tone rules when talking to the user.
2. Pick the skill:

| Situation | Skill |
|---|---|
| New feature, redesign, unclear idea | `forge:shaping` |
| Approved spec, no plan yet | `forge:planning` |
| Approved plan, ready to code | `forge:building` |
| Something broken or behaving wrongly | `forge:debugging` |
| About to say "done", or a phase just ended | `forge:verifying` |

3. Tiny change (typo, one-line fix, copy tweak)? Just do it, then run `forge:verifying`.

## Rules for every Forge skill

- Plain words, short answers. Ask only decisions, never code questions. Lead with the recommendation.
- Work on a feature branch, never `master`/`main`. Never merge or push to it; `CLAUDE.md` gates that.
- No AI co-author or "Generated with" lines in commits or PRs.
