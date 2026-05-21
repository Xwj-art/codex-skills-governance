# Cross-Chapter Logic

## Expected Seven-Chapter Arc

```text
Chapter 1: why this topic matters, problem, objectives, contributions
Chapter 2: only the technologies actually used later
Chapter 3: requirements, boundaries, architecture, data/knowledge base design
Chapter 4: core workflow/method design and why nodes cooperate this way
Chapter 5: engineering implementation evidence and interface/system display
Chapter 6: experiments and tests that verify core claims
Chapter 7: conservative summary, limitations, and grounded future work
```

## Boundary Checks

- Chapter 1 should not become a full method chapter.
- Chapter 2 should not include unused technology survey material.
- Chapter 3 defines what the system needs and how it is organized.
- Chapter 4 explains method choices and workflow rules.
- Chapter 5 proves implementation, not just repeats diagrams.
- Chapter 6 validates key design claims, with clear limits.
- Chapter 7 must not introduce new completed work.

## Claim Trace Table

Build a table during full review:

| Claim / goal | Source | Design support | Implementation support | Experiment support | Status |
| ------------ | ------ | -------------- | ---------------------- | ------------------ | ------ |

Mark status as Pass, Weak, Missing, or Overstated.

## Experiment Consistency

- Match metrics to claims.
- Keep table title, figure title, body analysis, and conclusion consistent.
- If Sparse-only beats Hybrid, do not hide it; frame Hybrid as engineering/extensibility only if supported.
- If testing is small, say “初步验证” or “在当前测试集上”.
- Never use “显著提升” without comparable evidence.

## Bridge Sentences

Add bridge sentences when chapters feel disconnected:

- End of Chapter 3 should point to why the workflow design is needed.
- End of Chapter 4 should point to implementation mapping.
- Start of Chapter 6 should state which design decisions are being tested.
- Chapter 7 should explicitly return to Chapter 1 objectives and Chapter 6 results.
