---
name: shaping
description: Turns a rough idea into an approved written spec. Use before building any new feature, redesign or behaviour change, when requirements are unclear, or when the user says "let's design, brainstorm or add X".
---

# Shaping

Goal: a spec the user has approved. No code until then.

## Steps

1. **Look first.** Read `CLAUDE.md`, the relevant code, recent commits, and existing specs. Never ask what the project already answers.
2. **Interview.** One question at a time. Prefer multiple choice, with your recommendation first. Cover purpose, who it is for, what "done" looks like, and what is out of scope. Stop when you could write the spec without guessing.
3. **Propose 2-3 approaches** with trade-offs. Recommend one.
4. **Suggest improvements.** List extra UX, polish, native-feel or performance ideas as an itemised list. The user accepts or rejects each. Only accepted ones enter the spec. Never add them silently. Record the accepted and rejected lists in the spec.
5. **Write the spec** to `docs/forgelite/specs/YYYY-MM-DD-<topic>-design.md` (or the project's existing specs folder if `CLAUDE.md` or the repo already uses one). Sections: Goal, Out of scope, Decisions (with the reason), Improvements (accepted/rejected), Behaviour, Data/changes, Edge cases, Known gaps (risks accepted as they are, each with why), Test approach. Concrete, no placeholders.
6. **Cold review.** Dispatch a fresh subagent (`model: sonnet`) that has not seen the conversation. Give it the exact files to read, a limit of about 25 tool calls, and ask for a report under 400 words. It checks the spec against the code and `CLAUDE.md` and reports gaps, contradictions and hidden scope. Any limit, quota, price or permission that depends on a value the app or user sends (a time, an id, a count, a flag) is a Critical finding unless the server checks or bounds it. If the project has a design-system doc it always checks it, and a motion doc (with its checklist) whenever anything moves. Fold every real finding in. Reject findings only with a stated reason.
7. **Show the user** a 5-line plain summary, what the review found and changed, the decisions the user must make, and the spec path. Not the full spec. Get approval.
8. **Hand over to planning in a fresh session.** Commit the approved spec on its own, staged by name, so later sessions and reviewers see it in git. Before handing over, check that every decision, answer and accepted improvement from this chat is written in the spec: the planner sees only the spec, `CLAUDE.md` and the code. Then tell the user: "Spec approved. To save tokens, open a new Opus session and say: plan the spec at <spec path>." A fresh session reloads the project once, which costs far less than carrying this whole design chat through planning. Only if this chat is still short (a few turns, little code read) may you continue with `forgelite:planning` here.

## Rules

- Shaping and planning are the high-stakes thinking, so they are best run on Opus. If this session is on Sonnet, say so once and suggest starting a new Opus session; continue if the user prefers.
- Visual questions (layouts, looks)? Show a mockup file instead of describing it.
- Too big for one spec? Split into parts and shape the first.
