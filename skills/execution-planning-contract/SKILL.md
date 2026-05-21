---
name: execution-planning-contract
description: Use when Codex is asked to plan or execute multi-step work, especially file edits, debugging, testing, document formatting, delivery workflows, or any task with components, dependencies, verification, TODO tracking, adversarial debate, or shortest-path execution ordering.
---

# Execution Planning Contract

Use this skill for any non-trivial task with multiple steps, components, files,
tests, or delivery risk.

## Core Contract

Before execution, list a concise TODO plan with:

- components or modules
- dependencies between components
- rough time estimate per component
- shortest-path ordering that removes blockers early and avoids rework
- verification method for each component

When the user explicitly asks for a plan, the plan should be refined enough to
execute directly:

- use nested sub-plans when a top-level step still contains multiple distinct
  operations, dependencies, or verification points
- choose and state an explicit operation order instead of listing unordered work
- explain the ordering when it materially reduces rework or prevents one step
  from dirtying another
- if the user asks for both the plan and completion of the work, provide the
  plan first and then carry the work through to completion rather than stopping
  at analysis

Then work each component with `DETECT -> MODIFY -> VERIFY`:

- `DETECT`: identify the target rule, evidence, current mismatch, component
  boundary, and downstream dependencies.
- `MODIFY`: make the narrowest effective change, state risk, and update the
  task ledger or TODO state when one exists.
- `VERIFY`: collect evidence appropriate to the task. Do not mark `pass` unless
  the required evidence actually exists; use `changed`, `needs_visual_check`,
  `blocked`, or `fail` where appropriate.

## Adversarial Debate

Before high-risk or broad edits, run a short opposition pass:

- Why might this plan still fail?
- What counterexample would disprove the global rule?
- Which downstream component could be dirtied?
- What boundary prevents scope creep?
- What evidence is needed before calling this component done?

If the opposition finds a real risk, split the component or change the order
before editing.

## Configurable Checker Tests

When a project loads behavior from user-authored rules, config files, Markdown,
or selectors, design tests from the selector boundary instead of only from the
default profile:

- For every check group and every single-item selector, add a minimal-config test
  that proves the selected item can run without requiring sibling checks in the
  same group.
- Add a no-crash test for missing optional config: a selected item should either
  run or be reported as skipped with the missing config path; it should not fail
  with an incidental `KeyError` or broad unexpected exception.
- Test three selector modes separately: explicitly enabled single item, enabled
  group/alias, and disabled inherited item/group.
- Prefer tests that model an external user's smaller rule file over tests that
  only exercise the built-in default configuration.
- When the current implementation cannot satisfy the desired boundary yet, mark
  the test as a known failing contract only if the suite must remain green, and
  name the test after the behavior that should eventually pass.

## Boundary Conditions

- For a tiny one-command answer or pure explanation, keep the TODO implicit or
  one line.
- Do not let planning replace execution when the user asked for action.
- Do not run unrelated full checks unless the user requested full verification.
- If a task has persistent state files, update them after each component edit.
- If evidence is renderer-, environment-, or user-dependent, mark the component
  `needs_visual_check` or `blocked` instead of claiming pass.
