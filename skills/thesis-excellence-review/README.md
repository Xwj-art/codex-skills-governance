# Thesis Excellence Review

A Codex skill for improving and auditing Chinese undergraduate thesis or graduation-design DOCX files, especially engineering theses that involve RAG, LLM applications, LangGraph workflows, experiments, figures, tables, references, and Word template constraints.

The skill is designed for conservative, evidence-based thesis polishing: it coordinates multi-role review, applies only defensible edits, validates DOCX integrity, and requires render-based visual QA before delivery.

## What It Does

- Reviews thesis structure from problem statement to method, implementation, experiments, conclusion, and defense risk.
- Coordinates specialist review roles for format, section content, cross-chapter logic, figures/tables, academic expression, technical defense, and experiment QA.
- Checks whether claims are supported by code, experiments, citations, and figures.
- Keeps experimental conclusions conservative when data is weak or baselines disagree.
- Audits DOCX integrity, citation anchors, reference bookmarks, table/figure layout, chapter starts, and render output.
- Helps reduce obvious AI-like prose while preserving technical accuracy and natural Chinese academic writing.

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── content_and_expression.md
│   ├── cross_chapter_logic.md
│   ├── docx_format_qa.md
│   ├── experiment_qa.md
│   ├── subagent_workflow.md
│   └── technical_defense.md
└── scripts/
    └── audit_docx_integrity.py
```

## Core Workflow

1. Baseline scan without edits.
2. Multi-agent diagnosis across formatting, content, logic, figures/tables, experiments, and defense risks.
3. Merge findings into must-fix, should-fix, and optional polish priorities.
4. Apply conservative paragraph-level or OOXML edits to the original thesis file.
5. Run adversarial review against unsupported claims and weak experiments.
6. Validate DOCX integrity, citation links, render output, page layout, figures, tables, and references.

## Quality Gates

The skill treats the following as blocking issues unless explicitly explained:

- DOCX repair prompts, XML parse failures, or broken internal citation anchors.
- Chapter, heading, TOC, figure/table numbering, or reference-list drift.
- Experimental conclusions that exceed reported data.
- RAG, LangGraph, Self-RAG, or multi-agent claims without implementation mapping.
- Hybrid retrieval described as empirically best when Sparse-only or another baseline is stronger.
- Missing dataset source, ground-truth basis, privacy boundary, deployment dependency, or API cost discussion.
- Large layout gaps, unreadable figures, table overflow, or broken captions.
- Edits that invent facts, experiments, references, screenshots, or system features.

## Utility Script

Run the DOCX integrity checker:

```bash
python3 scripts/audit_docx_integrity.py path/to/thesis.docx
```

The script verifies that required DOCX XML parts parse, counts document objects, and checks whether internal hyperlinks point to existing bookmarks. It does not replace visual rendering and page-by-page QA.

## Installation

Place this directory under your Codex skills directory:

```text
~/.codex/skills/thesis-excellence-review
```

Then invoke it by asking Codex to use `thesis-excellence-review` for a thesis DOCX review or improvement task.

## Notes

- This skill is intentionally conservative. It should not fabricate experiments, metrics, references, screenshots, system features, or novelty claims.
- For DOCX modifications, it expects render-and-inspect validation when LibreOffice or an equivalent renderer is available.
- It is optimized for Chinese undergraduate thesis review, but the review criteria can also help with similar engineering design reports.
