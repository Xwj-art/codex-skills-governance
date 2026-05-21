---
name: cost-aware-parallel-engineering
description: Use when planning or executing architecture-first, module-based, subagent-parallel engineering work with explicit cost control, including choosing cheaper models for bounded subtasks, splitting work by dependency graph, creating context packets, and reserving stronger models for architecture, integration, review, and high-risk decisions.
---

# Cost-Aware Parallel Engineering

Use this skill when the user wants efficient multi-agent development, cheaper-model execution for small modules, architecture/module planning, DAG-based parallel work, or a reusable workflow for cost-sensitive engineering.

## Core Principle

Keep the expensive model on orchestration, architecture, risk, integration, and final judgment. Push narrow, well-specified, low-risk implementation or inspection tasks to cheaper models only after contracts, ownership, and acceptance evidence are clear.

## Operating Contract

1. **Architect before spawning**

   - Define the goal, non-goals, success condition, and expected artifact.
   - Identify modules, dependencies, shared contracts, and write ownership.
   - Mark the critical path that the main agent should handle locally.

2. **Freeze contracts before parallel work**

   - For each module, specify inputs, outputs, file ownership, public interfaces, invariants, and tests.
   - Shared schemas, CLI command contracts, API shapes, style rules, and report formats belong to the main agent first.
   - Do not let workers invent cross-module contracts independently.

3. **Dispatch by DAG**

   - Split work into dependency waves.
   - Tasks with no dependencies can run in parallel.
   - Downstream tasks wait until their providers are done and reviewed.
   - Avoid assigning the immediate blocking task to a subagent if the main rollout depends on it next.

4. **Use cost tiers deliberately**

   - Strong/frontier model: architecture, ambiguous design, contract decisions, integration, migration strategy, security-sensitive code, data-loss risk, final review.
   - Mid-tier model: medium modules with clear interfaces but nontrivial reasoning.
   - Cheap/mini model: bounded CRUD, adapters, tests from clear specs, doc/report generation, mechanical checks, fixture creation, localized refactors, read-only exploration.
   - If a cheap model fails once due to reasoning/context limits, tighten the prompt and retry once. If it fails again, escalate the task.

5. **Keep context packets small**

   - Give subagents only: goal, relevant files, owned write scope, contract, examples, acceptance criteria, exact validation command, and known constraints.
   - Do not pass full history unless necessary.
   - Do not duplicate the same task across agents.

6. **Integrate centrally**
   - Main agent reviews returned changes, runs integration checks, resolves conflicts, and updates the plan.
   - Workers should not push, merge, broadly reformat, or revert others' changes unless explicitly asked.

## Model Routing Heuristic

Use cheaper models only when all are true:

- The task has a clear success condition.
- The write scope is small and disjoint.
- The task can be validated by tests, diff inspection, generated report, or exact command output.
- Failure is cheap to revert.
- The task does not decide architecture or shared contracts.

Prefer the stronger model when any are true:

- Requirements are ambiguous.
- The task touches shared interfaces, data migrations, security, concurrency, or persistence.
- A subtle mistake would silently corrupt output.
- The task requires holistic judgment across many files.
- The user explicitly cares more about correctness than cost.

## Planning Template

Before spawning subagents, produce a compact plan:

```markdown
## Goal

[one sentence]

## Boundary

- In scope:
- Out of scope:
- Success condition:

## Architecture / Contracts

- Shared contracts:
- Module ownership:
- Integration points:

## DAG

Wave 1:

- T1 [model tier, owner, files, validation]
- T2 [model tier, owner, files, validation]

Wave 2:

- T3 depends_on: [T1, T2]

## Cost Strategy

- Main agent keeps:
- Cheap-model tasks:
- Escalation triggers:
```

## Task Spec Template

Every delegated task must include:

```markdown
Task: [short name]
Model tier: [cheap / mid / strong]
Reason for tier: [why this model is enough]
Owned files or responsibility: [exact paths or read-only scope]
Do not touch: [paths/contracts/behaviors]
Inputs/context: [minimal relevant facts]
Contract: [inputs, outputs, invariants]
Acceptance criteria:

- [criterion]
  Validation:
- [exact command or review evidence]
  Return:
- changed files
- summary
- validation evidence
- blockers or uncertainty
```

## Subagent Usage Rules

- Spawn subagents only when the user explicitly asks for parallel/subagent work or this skill is invoked for that purpose.
- Use workers for concrete implementation with disjoint write scopes.
- Use explorers for read-only codebase questions.
- Use review agents only when they can check a concrete risk while implementation continues.
- Do not wait immediately unless the result blocks the main agent's next action.
- While subagents run, the main agent should work on non-overlapping critical-path items.

## Cost-Aware Subagent Prompt Pattern

```markdown
You are not alone in the codebase. Other agents may be working in parallel.
Do not revert or overwrite changes outside your assigned scope.

Your task is intentionally narrow to control cost and reduce integration risk.

[Task Spec]

Implement the smallest change that satisfies the acceptance criteria.
Do not redesign shared contracts. If the contract seems wrong, stop and report why.
```

## Verification Strategy

Use evidence proportional to risk:

- Read-only exploration: exact files/lines and answer.
- Localized implementation: targeted tests or script output.
- Cross-module change: module tests plus integration smoke test.
- Document/report generation: output path plus structural checks.
- UI/layout work: screenshot or renderer evidence when required.

Never mark a task done solely because a subagent said it is done. The main agent must inspect enough evidence to trust integration.

## Anti-Patterns

- Spawning agents before architecture and contracts are clear.
- Giving cheap models broad, ambiguous, or high-risk tasks.
- Letting multiple workers edit the same files.
- Asking every worker to read the whole repository.
- Waiting on subagents while no critical-path work is happening.
- Using parallelism to hide lack of a plan.
- Optimizing for token cost so aggressively that integration cost increases.

## When To Use Tree-Pipeline Ideas

Borrow these ideas from tree-pipeline for larger projects:

- contract-first planning;
- module dependency graph;
- task ledger with statuses;
- context packets;
- dashboard/report after each wave;
- explicit resume state.

Do not introduce a full pipeline framework unless the project has enough modules, repeated waves, or long-running work to justify the overhead.
