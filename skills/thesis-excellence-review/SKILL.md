---
name: thesis-excellence-review
description: Use when improving or auditing a Chinese undergraduate thesis or graduation-design DOCX to an excellent submission standard. Coordinates role-based review for formatting, chapter content, cross-chapter logic, figure/table layout, adversarial defense risks, low-AIGC academic prose, Word/DOCX render validation, citation hyperlink integrity, and final delivery without creating alternate thesis copies. In Codex, spawn subagents only when the user explicitly asks for subagents, delegation, or parallel agent work.
---

# Thesis Excellence Review

Use this skill for Chinese undergraduate thesis improvement, especially engineering theses with code, RAG/LLM systems, experiments, figures, tables, references, and Word template requirements.

## Operating Contract

- Work on the user-designated thesis file in place unless they explicitly ask for a separate copy.
- Temporary snapshots, PDFs, PNGs, and extracted XML are allowed under `/private/tmp`; do not leave alternate thesis DOCX deliverables in the project directory.
- Preserve school template intent, chapter page breaks, citation links, bookmarks, reference list structure, and user-written facts.
- Do not invent experiments, metrics, references, screenshots, system features, or novelty claims.
- Favor clear, natural, technically accurate Chinese over aggressive “anti-AI” rewriting.
- Use the Documents skill/render workflow for DOCX work when available.

## Codex Role Review

Use these roles as a local review checklist for full thesis improvement. In
Codex, spawn subagents only when the user explicitly asks for subagents,
delegation, or parallel agent work. Keep write ownership centralized in the main
agent; delegated agents, when authorized, normally diagnose, challenge, and
verify.

- **Format Agent**: template, headings, page breaks, TOC, citations, references, tables, DOCX integrity.
- **Section Content Agent**: each section’s purpose, paragraph logic, technical specificity, evidence, and prose.
- **Cross-Chapter Logic Agent**: thesis arc from problem to method to implementation to experiments to conclusion.
- **Figure/Table Agent**: figure necessity, placement, caption match, image quality, table readability, blank space.
- **Academic Expression Agent**: low-AIGC prose, natural transitions, non-promotional wording, term consistency.
- **Defense Risk Agent**: examiner questions, unsupported claims, novelty/workload risks, and oral defense risk.
- **Technical Defense Agent**: RAG/LangGraph/Self-RAG necessity, code-to-paper mapping, system boundaries, security/privacy, deployment, cost, failure paths.
- **Experiment QA Agent**: dataset construction, ground truth, metric validity, baseline fairness, statistics, ablations, human evaluation, latency, failure cases.
- **Coordinator**: decides scope, resolves conflicts, applies edits, runs validation, reports residual risk.

Read `references/subagent_workflow.md` before orchestrating a full pass. Treat
the file as a role-review protocol unless delegation is explicitly authorized.

## Execution Workflow

1. **Baseline Scan, No Edits**

   - Locate thesis DOCX, template DOCX, figures, source project, reports, and generated screenshots.
   - Extract headings, section boundaries, tables, figures, citations, references, page count, and media inventory.
   - Render the thesis to PDF/PNG if `soffice` is available.
   - Run `scripts/audit_docx_integrity.py <thesis.docx>`.

2. **Role-Based Diagnosis**

   - Produce role-specific independent findings locally, or ask role-specific
     subagents only when the user explicitly authorized subagents/delegation.
   - Require concrete locations, severity, and suggested action.
   - Merge findings into A/B/C priorities: must fix, should fix, optional polish.

3. **Plan Edits In Order**

   - Cross-chapter logic first.
   - Section content second.
   - Academic expression third.
   - Figure/table layout fourth.
   - Format and DOCX validation last.

4. **Edit Conservatively**

   - Prefer small paragraph-level edits over wholesale rewrites.
   - Keep technical facts, metrics, references, and chapter boundaries consistent.
   - For DOCX, use structured OOXML or python-docx carefully; validate after each high-risk batch.

5. **Adversarial Review**

   - Defense Risk Agent challenges claims, experiment conclusions, novelty, and unsupported wording.
   - Technical Defense Agent challenges whether the system can survive strict oral questioning: why RAG, why LangGraph, whether Self-RAG/multi-agent claims are real, and whether code backs the paper.
   - Experiment QA Agent challenges whether the experiments really support the paper's claims.
   - Format Agent challenges any change that may break Word, citations, tables, or template rules.
   - Cross-Chapter Agent checks whether conclusions still match the body.
   - Adopt the more conservative claim when evidence is weak.

6. **Final Validation Gate**
   - DOCX opens structurally: `document.xml`, `styles.xml`, relationships parse.
   - Citation anchors/bookmarks are intact; no broken internal hyperlinks.
   - Render full DOCX to PDF/PNG and inspect all key pages plus figure/table pages.
   - Check chapter starts, large blanks, captions, table splits, page count changes, and reference list.
   - Report what changed, what was verified, and residual risks.

## When To Read References

- For subagent roles, handoff formats, and debate rules: `references/subagent_workflow.md`.
- For section-level writing, low-AIGC prose, and content checks: `references/content_and_expression.md`.
- For cross-chapter structure and experiment consistency: `references/cross_chapter_logic.md`.
- For strict defense questions on RAG/LangGraph engineering validity: `references/technical_defense.md`.
- For RAG/LLM experiment design and evaluation risks: `references/experiment_qa.md`.
- For DOCX, citation, render, and rollback rules: `references/docx_format_qa.md`.

## Hard Quality Gates

Reject final delivery if any of these remain unexplained:

- Word/LibreOffice repair prompt or XML parse failure.
- Broken citation anchors, missing reference bookmarks, or reference style drift.
- Chapter structure, TOC, figure/table numbering, or page breaks visibly wrong.
- Experimental conclusions exceed the reported data.
- Summary/abstract claims do not match implementation and experiments.
- LangGraph, RAG, Self-RAG, or multi-agent benefits are claimed without code-level mapping and evidence.
- Hybrid retrieval is described as better without Dense-only / Sparse-only / Hybrid comparison or a conservative engineering rationale.
- The system claims hallucination control without no-answer, weak-evidence, conflicting-evidence, or prompt-injection tests.
- Evaluation uses only cherry-picked examples and no defined question set, scoring standard, or ground-truth basis.
- Dataset source, knowledge-base coverage, privacy boundary, deployment dependency, or API cost risk is absent from the defense-risk report.
- Large image/table blank areas, tiny unreadable figures, or severe table overflow.
- Rewrite introduces factual errors, fake data, or a noticeably templated AI tone.
