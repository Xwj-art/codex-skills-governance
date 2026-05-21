# DOCX Format And Render QA

## User-Safety Rules

- Edit only the user-designated original thesis DOCX unless instructed otherwise.
- Use `/private/tmp` for snapshots, rendered PDFs/PNGs, and extracted files.
- Do not leave extra “final”, “统一格式”, or “修正版” DOCX files in the project directory.
- Before high-risk edits, create a temporary snapshot for rollback.
- If the file breaks, rollback immediately instead of stacking fixes.

## Required Structural Checks

- `word/document.xml`, `word/styles.xml`, `word/_rels/document.xml.rels` parse as XML.
- `python-docx` can open the file and count paragraphs/tables.
- Media count, table count, hyperlink count, and bookmark count do not unexpectedly drop.

Run:

```bash
python scripts/audit_docx_integrity.py path/to/thesis.docx
```

## Citation Checks

- Superscript appearance is not enough; citation numbers must be real internal links.
- Check all `w:hyperlink/@w:anchor` targets exist in `w:bookmarkStart`.
- Check reference entries use consistent paragraph style, hanging indent, font, and numbering.
- After any citation/reference edit, rerun full link audit.

## Render Checks

Use LibreOffice if available:

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir /private/tmp/render thesis.docx
pdftoppm -png -r 144 /private/tmp/render/thesis.pdf /private/tmp/render/page
```

Inspect:

- Chapter starts and page breaks.
- TOC pages, abstract, references, acknowledgments.
- Every figure/table page.
- Large blanks, tiny figures, clipped images, table overflow, table continuation without context.
- Captions: figure below image, table above table.

## Rollback Triggers

Rollback to the last temporary snapshot if:

- Word/LibreOffice reports repair or unreadable content.
- XML parse fails.
- Citation anchor count drops unexpectedly.
- Images, tables, paragraphs, or references disappear.
- Render page count changes without explanation.
- A table or figure becomes visibly worse.

## Table/Figure Fix Preferences

- First shorten table text; then adjust widths; then reduce font modestly.
- Prefer one readable compact table over a wide table with broken words.
- If a table must span pages, repeat header and make continuation clear.
- Crop screenshots to meaningful UI; remove large empty browser or desktop areas.
- Replace schematic screenshots with real system screenshots when the chapter claims interface display.
