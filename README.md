<p align="center">
  <img src="assets/banner.svg" alt="Forgelite: same workflow as Superpowers, a fraction of the tokens" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-eb6834"></a>
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-c2410c">
  <img alt="6 skills" src="https://img.shields.io/badge/skills-6-fbbf24">
  <img alt="201 lines" src="https://img.shields.io/badge/instructions-201%20lines-9a3412">
</p>

# Forgelite

**A lean, token-efficient build workflow for Claude Code.** Shape an idea into a spec, plan it, build it test-first, debug by evidence, and prove it works before saying "done", while spending expensive model time only where it pays off.

Forgelite is built on the ideas of [**Superpowers**](https://github.com/obra/superpowers) by Jesse Vincent, which showed that a disciplined, skill-driven workflow makes Claude Code far more reliable. Forgelite was made with one goal: **keep that discipline, and improve speed, performance and token usage.** If you like what Superpowers does but want it to cost less and run faster, this is for you.

> Forgelite is not affiliated with Superpowers or its author. See [Credits](#credits).

---

## The short version

|  | Superpowers 7.0.0 | Forgelite |
|---|---|---|
| Skills | 15 | **6** |
| Instruction lines | 3,828 | **201** |
| Text injected at every session start | ~3,200 chars | **336 chars** |
| Independent reviews (spec, plan, final code) | yes | yes |
| Test-first building | yes | yes |
| Model chosen per subagent | mostly inherits your chat's model | **yes** (Haiku, Sonnet or Opus by job) |
| Opus for design and reviews, Sonnet for building | not built in | **built in** |
| Plain-language summaries aimed at non-coders | not a focus | **yes** |

<p align="center"><img src="assets/size-chart.svg" alt="Forgelite is 5% of the instruction lines of Superpowers" width="720"></p>

## Results

We ran the same task three times: build a command-line to-do manager (add, list, edit, done, delete, filters, search, CSV and Markdown export, saved to a file) from the same starter project, with the same spec answers. The starter has a planted bug in its date code that the existing tests do not catch.

<p align="center"><img src="assets/cost-chart.svg" alt="Forgelite costs 8% less on Opus and 42% less with a Sonnet main chat" width="720"></p>

| Run | Weighted cost | Tests passing | Real issues fixed by the final review |
|---|---|---|---|
| Superpowers, Opus main chat | 1.33M | 67 | 2 (3 more left unfixed) |
| Forgelite, Opus main chat | 1.23M (**-8%**) | 75 | 9 |
| Forgelite, Sonnet main chat | 0.77M (**-42%**) | 150 | 6 |

All three met every requirement, and all three found and fixed the planted bug.

**What to read into this, honestly:**

- On the **same model**, Forgelite is only about 8% cheaper. The big saving comes from the model strategy: design and reviews on Opus, building on Sonnet.
- Superpowers can run on Sonnet too, and would save money the same way. Forgelite makes that the default and builds the handover around it (see [Model strategy](#model-strategy)).
- Costs are a **relative index** (output tokens x5, cache writes x1.25, cache reads x0.1), not a bill. Sonnet is priced at 1/5 of Opus, which is an assumption. At 1/3 the Sonnet run saves about 23% instead of 42%. Run `benchmark/scripts/token_report.py` with your own price.
- One run per row, one small project, Windows only. Treat the numbers as a rough size of the effect, not a precise benchmark. The full reports are in [`benchmark/reports`](benchmark/reports) and the method is in [`benchmark`](benchmark).

A larger real-world check: one 14-task feature in a mobile app (a database change, three server functions and four screens) was designed and planned on Opus, then built on Sonnet with 14 subagents. About three quarters of the total cost was Opus (the design chat and its reviews). The whole build phase cost less than the design phase alone. The plan review found 15 problems and the final review found 2 real bugs, all fixed before anything reached a device.

## Latest testing

Forgelite is under constant testing. I run it on a real app with the newest Claude models, read what it cost and where it slipped, and fix it in the next version. **Please always install the latest version** (`claude plugin update forgelite@forgelite`).

**Latest test: version 0.4.2, one real feature, design and plan on Opus, build on Sonnet**

A mobile app got two new features in one go (one database change, one data-loading script, 13 tasks).

| Phase | Cost index | Notes |
|---|---|---|
| Design and plan (Opus) | 1.68M | Plan review found 9 real problems before any code was written |
| Build and review (Sonnet main, 14 subagents) | 2.08M | 423 test suites, 9,468 tests passing, typecheck and lint clean |

**What went well**
- The final Opus review ran by itself and found 1 medium and 2 low bugs (one could have saved a wrong value for the day). All fixed.
- `forgelite:verifying` ran at the end, as it should.
- No build task went past about 49 tool calls (the previous test had 73).

**What we found, and fixed in 0.4.3**
- Three build tasks ran on Opus and cost about a third of the build. Now Sonnet by default; Opus only for migrations, security and payments, with the reason in the plan.
- One task was built on Opus, then rebuilt on Sonnet. A failed task is now continued by the same agent, never rerun on another model.
- Two tasks were merged into one subagent and went over the size target. Now one task per subagent.
- The main build chat grew to over 250k tokens. It now works in batches (see 0.4.4 below).

Numbers are a relative cost index, not a bill; see [Results](#results) for how it is calculated.

**Test 2: version 0.4.3, a bigger new feature in a mobile app (19 tasks)**

Total cost index 9.3M (design 3.9M, build 5.4M), about 0.49M per task against 0.29M in the first test.

- **Went well:** Opus ran only the database task and the final review. The plan review found 12 problems. The final review found 5 real bugs (including a timing bug that made something run several times too fast). 9,756 tests passing.
- **Found, fixed in 0.4.4:** the build chat grew to 418k tokens and cost the most of any part (now batches of 8 tasks); 8 of 19 tasks were too big and needed a second agent (the plan reviewer now checks task size); two parallel agents overwrote each other's files (tasks that share a file now run in sequence); a timed loop kept waking the huge chat (no `/loop` during builds).

## Install

```bash
claude plugin marketplace add Harriszed/forgelite
claude plugin install forgelite@forgelite
```

Restart Claude Code. If you have Superpowers installed, **disable it** while you use Forgelite. They solve the same problem and compete for control:

```bash
claude plugin disable superpowers@superpowers-dev
```

Forgelite starts itself: a tiny session-start hook (336 characters) tells Claude to use `forgelite:starting-work` before any task that adds, changes or fixes code. Quick questions and one-line fixes are skipped.

## How it works

<p align="center"><img src="assets/workflow.svg" alt="Forgelite workflow: shape and plan on Opus, build and verify on Sonnet" width="760"></p>

| Skill | What it does |
|---|---|
| `forgelite:starting-work` | Reads your project's `CLAUDE.md` first (its rules always win), then routes to the right skill. |
| `forgelite:shaping` | Interviews you one question at a time, offers improvement ideas for you to accept or reject, writes the spec, has it cold-reviewed. |
| `forgelite:planning` | Turns the spec into small test-first tasks, has the plan cold-reviewed by Opus at high effort, shows you a 5-line summary. |
| `forgelite:building` | Builds test-first, runs independent tasks as parallel subagents on the cheapest model that can do the job, then a final Opus review that runs the code with awkward input. |
| `forgelite:debugging` | Reproduce, gather evidence, one hypothesis at a time, failing test, fix the cause. Stops after three failed fixes. |
| `forgelite:verifying` | No "done" without real command output from this session. Ends with exactly what you should check next. |

### Model strategy

| Job | Model | Why |
|---|---|---|
| Interview, spec, plan | Opus (your chat) | Mistakes here are the expensive ones. |
| Spec review | Sonnet | A scoped read-and-report job. |
| Plan review | Opus, high effort | The last gate before work starts. |
| Build tasks | Sonnet (Haiku for pure mechanical edits, never tests). Opus only for migrations, security and payments, with the reason in the plan | The plan already holds the thinking. |
| Final code review | Opus, high effort | The last gate before you see it. |

A skill cannot change your chat's model, so when the plan is approved Forgelite tells you to **open a new Sonnet session** and say `build the plan at <path>`. This is deliberate: switching model mid-chat makes the new model re-read (and re-cache) the whole conversation at full price, and a builder does not need the design discussion anyway. The plan file is the handover.

### Token habits built in

- Every reviewer gets an exact file list, a tool-call limit and a word limit, so it cannot wander through your repo.
- Every build subagent must reply in under 150 words, so reports do not fill your main chat.
- Subagents are meant to stay around 200-300k tokens of context. Tasks are sized to fit, and a subagent that is not nearly done writes a handover file for a fresh one.
- One task per subagent, never merged, and a failed task is continued by the same agent, never rerun on another model.
- Builds run in batches of at most 8 tasks, then a progress note and a fresh session, so the chat never grows huge. Tasks that share a file never run in parallel.

## What Forgelite leaves out

To stay small, Forgelite does **not** include Superpowers' git-worktree skill, finish-branch skill, parallel-agent dispatch skill, or separate code-review request and receive skills. Parallel subagents and a final cold review are built into `forgelite:building` instead. If you rely on those skills, keep Superpowers for them.

## Works with your project

Forgelite reads `CLAUDE.md` before anything else and never overrides it. If your project already has a process (design docs, review steps, end-of-phase checklists, a different specs folder), Forgelite follows it and only fills the gaps. Specs and plans go in `docs/forgelite/specs` and `docs/forgelite/plans` unless your repo already uses another folder.

## Reproduce the benchmark

```bash
cd benchmark/task-list-starter       # the starter project, TASK.md and ANSWERS.md
```

1. Copy `task-list-starter` into a fresh folder and `git init` it. Do this once per run.
2. Open a new Claude Code session there with the plugin you want to test enabled and the other disabled.
3. Paste the contents of `TASK.md`. The agent answers its own questions from `ANSWERS.md`.
4. It writes a `RUN-REPORT.md` (template included).
5. Measure it: `python -I benchmark/scripts/token_report.py "*your-project-folder*" --sonnet-price 0.2`

## Limitations

- Measured on small projects, one run each, on Windows with Node. Real projects will differ.
- The session-start hook is a small `printf` run through bash. It works in Git Bash on Windows and on macOS and Linux, but has only been tested on Windows.
- The token index is relative, and the Sonnet price ratio is an assumption.
- Forgelite is opinionated about models. If you do not use Opus, Sonnet and Haiku, adjust the model names in the skills.

## Credits

Forgelite exists because of [**Superpowers**](https://github.com/obra/superpowers) by Jesse Vincent (obra), MIT licensed. The workflow shape (brainstorm, plan, test-first build with subagents, systematic debugging, verification before completion) comes from his work, and so does the idea of making agent discipline a set of composable skills. Forgelite's text is written from scratch and condensed, with a different model strategy, but it would not exist without his. Please go and star the original.

## License

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
