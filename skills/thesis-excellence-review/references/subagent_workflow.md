# Role Review Workflow

In Codex, this protocol is a role-review checklist by default. Spawn subagents
only when the user explicitly asks for subagents, delegation, or parallel agent
work.

## Standard Role Output

```markdown
## Role: [role]

### Verdict

Pass / Conditional Pass / Reject

### Findings

1. [issue] — Location: [chapter/section/page/paragraph] — Severity: High/Med/Low

### Required Changes

- Must fix:
- Should fix:

### Impact Scope

[local section / whole chapter / cross-chapter / figure numbering / references / DOCX integrity]

### Needs Review From

- [role]: [reason]
```

## Rounds

### Round 0: Baseline Scan

No edits. Establish facts: chapter map, claims, figures/tables, citations, page render status, high-risk areas.

### Round 1: Draft Fixes

Order: cross-chapter logic -> section content -> academic expression -> figure/table layout -> format.

### Round 2: Adversarial Debate

Every dispute must end as Accept, Defer, or Reject.

Typical challenges:

- Defense Risk -> Content: Does this experiment support the conclusion?
- Technical Defense -> Cross-Chapter: Does the paper justify why RAG/LangGraph/Self-RAG is needed instead of simpler alternatives?
- Technical Defense -> Content: Can every claimed node, state field, threshold, and failure path be found in code?
- Experiment QA -> Content: Is the dataset, ground truth, metric, and baseline design strong enough for this conclusion?
- Cross-Chapter -> Content: Does this section serve the thesis problem?
- Figure/Table -> Content: Is this visual necessary and explained?
- Format -> Figure/Table: Does this layout violate the template or harm render stability?
- Expression -> Content: Is the prose natural, or is it just term stacking?

### Round 3: Delivery Gate

Coordinator, Format Agent, Cross-Chapter Agent, and Defense Risk Agent views decide final status.

## Pass Standards

- Format matches the school template closely enough for submission.
- Research goal, design, implementation, experiments, and conclusion form a closed chain.
- Every chapter has a distinct role.
- Figures and tables are referenced, readable, and placed near relevant text.
- Language is natural, restrained, and technically accurate.
- Claims are not stronger than evidence.
- Technical choices are defensible against simpler alternatives.
- Experiments define data, baselines, metrics, and limits clearly enough for oral defense.

## One-Vote Reject Items

- Broken DOCX or repair prompt.
- TOC, headings, references, or figure/table numbering visibly wrong.
- Experimental result cannot support stated conclusion.
- RAG/LangGraph/Self-RAG/multi-agent claims have no implementation mapping.
- Dataset, ground truth, or scoring method is too vague to evaluate.
- Baselines are unfair or missing while the thesis claims superiority.
- Security, privacy, deployment, or API dependency risks are ignored while claiming practical deployment.
- Abstract/conclusion claim work not present in body.
- Large unrelated or template-like generated prose.
- Factual error introduced by editing.
