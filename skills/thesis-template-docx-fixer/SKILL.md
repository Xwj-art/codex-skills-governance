---
name: thesis-template-docx-fixer
description: Strict workflow for repairing an existing thesis or graduation-project `.docx` to match a school template with minimal, local, Word-safe edits. Use when Codex needs to compare a thesis against a template, plan nested formatting work, and fix cover pages, abstracts, table of contents, heading levels, body fonts, figure/table layout, reference superscripts, references formatting, headers/footers, blank pages, or excessive white space without broad reformatting.
---

# Thesis Template Docx Fixer

Use this skill to modify an existing thesis `.docx` under a strict template standard. Treat the template and the final rendered pages as the only authority. Prefer minimal edits, and do not broaden scope beyond the user's stated issue unless the user explicitly asks for a wider audit.

## Execution Contract

- For any multi-step request, first list a plan. When one step still contains multiple page types or verification methods, nest a sub-plan under it.
- Choose an explicit execution order that reduces rework. Default order: template baseline -> front matter -> table of contents -> abstracts -> body headings/fonts -> figures/tables -> citations/references -> headers/footers -> white space/blank pages.
- Work in `DETECT -> MODIFY -> VERIFY`.
- Mark evidence honestly as `render-verified`, `word-open-safe-but-not-rendered`, `needs-template-check`, or `blocked`.

## Hard Rules

- Treat the template as a hard standard, not a rough visual reference.
- For `.docx` visual layout, use Microsoft Word's actual display or Word-exported PDF as the authority. LibreOffice or other renderers may be used only as auxiliary structural checks, not as the final basis for pagination, white-space, figure/table placement, header/footer, or page-break conclusions.
- Compare rendered pages, not just style names, XML, or extracted text.
- Keep edits local. If the user reports one issue, fix that issue first.
- Preserve Word-open safety. Avoid risky broad transforms, whole-document style resets, or blind OOXML rewrites across the package.
- Never rewrite OOXML package parts with Python `xml.etree.ElementTree.write()` or any serializer that renames namespace prefixes unless a Word-open test has already proven that exact method safe for this document. In WordprocessingML, prefix churn such as `w:`/`mc:` becoming `ns0:`/`ns1:` can leave attributes like `mc:Ignorable="w14 w15 ..."` pointing at undeclared prefixes, which makes Word show "unreadable content" repair dialogs.
- Never extract every `<w:p>` paragraph from `word/document.xml` and reassemble them as a flat sequence. Paragraphs can be nested inside tables, text boxes, headers/footers, comments, or other containers; flattening them destroys parent structure such as cover-page tables even if paragraph counts still match.
- For narrow OOXML fixes, prefer a prefix-preserving patch on a temporary copy: copy the `.docx`, edit only the specific XML fragment or attribute, rebuild the package without changing unrelated parts, then verify Word can open it before replacing the working file.
- Keep intermediate DOCX/PDF/PNG artifacts in `/private/tmp` or another ignored location. Do not dirty the repo with delivery-irrelevant files.

## Workflow

### 1. Detect the boundary

- Decide whether the request is a single-issue fix, a sectional audit, or a full template pass.
- Identify the affected thesis pages and the matching template pages before editing.
- If the request is ambiguous, choose the narrowest reasonable boundary.

### 2. Preserve a safe rollback path

- Copy the original `.docx` to `/private/tmp` before risky edits.
- If a change is structural or likely to affect pagination, test on a temporary copy first.
- Only write the successful change back to the main file after visual proof and a Word-open safety check.

### 3. Modify the smallest possible surface

- Prefer object-level edits: paragraph/run properties, section/page breaks, specific inline shapes, table geometry, caption paragraphs, header/footer parts, and citation runs.
- For fixed-layout front matter such as the cover or second page, prefer cloning the template layout container/block and re-filling the original text over re-creating spacing by guesswork.
- For white space caused by figures or tables, adjust the specific object, its nearby paragraphs, or the relevant page-break behavior instead of globally reflowing the chapter.

### 4. Verify visually

- Use the `documents` skill render workflow when available. Use page-image inspection as the default verification method for layout claims.
- Render only the affected pages when the change is local. Render the full document only when the user asks for a full audit or the edit can shift pagination widely.
- Check for overlap, clipping, broken pagination, caption separation, TOC drift, superscript anomalies, header/footer drift, and accidental blank pages.

### 5. Report precisely

- If the user asks for an audit only, list problems by section or page and stop.
- If the user asks for a fix, state what was changed and what was not rechecked.
- Do not claim bibliographic correctness for reference entries unless each entry was checked against an external authoritative source; otherwise describe the work as visual/format normalization only.

## Component Strategies

### Front matter

- Keep cover, second page, declaration, and similar fixed-layout pages template-identical in typography, alignment, spacing, and line structure.
- When direct style matching fails, transplant the relevant template layout block and then restore the thesis text.

### Table of contents

- Compare TOC paragraph/run formatting against the template TOC, not body text.
- Preserve TOC fields if present. Fix styles and paragraph properties around them instead of flattening the TOC into plain text unless the user explicitly asks.

### Abstracts

- Align Chinese and English abstract headings, body fonts, keywords line, and spacing to the template's abstract pages.
- Keep content unchanged unless the user explicitly requests language edits.

### Body headings and typography

- Compare each heading level against the matching template level.
- Allow chapter starts on new pages when required by the template or school rule. Remove other avoidable page breaks or large empty areas.
- Restore numbering consistency with the smallest effective change.

### Figures and tables

- Keep figure captions below figures and table captions above tables when required.
- For tables, fix geometry per table. Do not push all tables through a global transform.
- When a figure or table causes a large blank area, prefer modest local reflow: resize the object, move it slightly earlier/later, or move adjacent paragraphs across the page boundary.
- When moving a figure, move only the exact top-level paragraph fragment containing the drawing and the adjacent caption paragraph. Do this by cutting the contiguous XML slice from the original document part and inserting it near the reference paragraph, preserving all unrelated bytes and container hierarchy. Do not rebuild the document from a list of paragraphs.
- Before writing back a figure/table move, compare the temporary file against the baseline: `w:tbl` count unchanged, `w:drawing` count unchanged, the moved caption now follows the intended reference, and any known front-matter table still has its closing `</w:tbl>` in the same local region.
- For tight thesis layout, scan from front to back and fix the first non-chapter-ending large gap before moving on; earlier edits can change later pagination.
- Diagnose white space by cause before editing:
  - real empty paragraph: delete only if it is inside the body and not an intentional chapter-ending gap;
  - heading pushed to next page: check `keepNext`/`keepLines` on heading styles; this is common for `heading 2`/`heading 3`, and can leave the previous page sparse when Word keeps a heading with its following text;
  - figure/table pushed to next page: check object size plus caption/table adjacency; if the remaining page area cannot hold the block, use "move following text before the object", "move the object closer to its first reference", or a modest object resize;
  - natural text pagination: if there is no empty paragraph, no page break, and no following title/table/figure block being forced, a one- or two-line bottom gap may be normal Word line-grid/footer behavior and should not be overfixed.
- Keep in-text references close to their visuals: when text says "as shown in Figure X" or "as shown in Table X", the corresponding figure/table should normally appear immediately after that paragraph unless doing so creates a worse layout problem.

### References and citation superscripts

- Treat in-text citation superscripts and the reference list as separate tasks.
- For superscripts, match vertical alignment, font, bracket/number presentation, punctuation spacing, and run segmentation to the template behavior.
- For the reference list, match indentation, alignment, font/size, line spacing, and hanging-indent behavior to the template.

### Headers, footers, and section settings

- Compare section-specific headers/footers, page numbers, margins, and first-page settings. Do not assume one footer applies everywhere.
- If only one section drifts, patch that section instead of resetting all sections.
- For page-number restarts, patch only the target section's `w:pgNumType` on a temporary copy. Do not reserialize `word/settings.xml`, `word/document.xml`, headers, footers, or styles through a generic XML writer just to add `w:start`; preserve original namespace declarations and unrelated package bytes.

## Common Failure Modes

- Trusting style names or XML similarity without checking the rendered page
- Solving a local defect with a full-document reformat
- Letting one fix silently alter unrelated pages
- Leaving intermediate files in the repo
- Declaring success without render evidence
- Breaking Word open behavior with aggressive package-wide OOXML edits
- Breaking Word open behavior by reserializing OOXML with changed namespace prefixes or stale `mc:Ignorable` prefix references
- Breaking document structure by flattening nested WordprocessingML paragraphs during figure moves; this can make a cover/table layout render as loose text while the `.docx` still opens and zip integrity still passes.

## Ordered Checklist

Read [references/format-checklist.md](references/format-checklist.md) before a full audit or when the user asks for a plan. Use it as the ordered checklist for front matter, TOC, abstracts,正文,图表,参考文献,页眉页脚,留白, and blank-page checks.
