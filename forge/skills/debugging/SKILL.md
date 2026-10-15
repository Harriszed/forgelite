---
name: debugging
description: Finds the real cause of a bug or failing test before changing code. Use when something is broken, a test fails, there is a crash or error message, behaviour is unexpected, a fix did not work, or the user says "it's not working".
---

# Debugging

Goal: fix the cause, prove it, and stop it returning.

1. **Reproduce.** Get the exact error or wrong behaviour, and the steps that trigger it. Cannot reproduce? Say so and gather more evidence, do not guess.
2. **Collect evidence.** Read the full error, recent changes (`git log`, `git diff`), and the code on the failing path. Add temporary logging if needed.
3. **Form one hypothesis** that explains all the evidence. State it.
4. **Test the hypothesis** with the smallest check that could prove it wrong. Wrong? Form the next hypothesis from the new evidence.
5. **Write a failing test** that captures the bug. If it only shows on a device and cannot be tested in code, say so and add a device check to the QA checklist instead.
6. **Fix the cause**, not the symptom. Confirm the test passes and nothing else broke.
7. **Remove** temporary logging.

## Stop rule

Three failed fixes in a row means the diagnosis is wrong or the design is. Stop and tell the user plainly what you learned. Give one recommended next step, in plain words, as a yes/no question. Do not try a fourth guess.

## Report

Plain words: what was wrong, why, what changed, how it was proven.
