# Thesis Format Checklist

Use this file for full-audit work or whenever the user asks for a detailed plan before execution.

## 1. Plan First

1. Classify the request as:
   - single-issue fix
   - section-level audit
   - full template pass
2. Write a top-level plan in execution order.
3. Add sub-plans when one step contains multiple page types or multiple verification methods.
4. For each step, define:
   - target pages/sections
   - template comparator
   - smallest expected edit surface
   - verification method

## 2. Establish the Baseline

1. Locate the current thesis file and the authoritative template file.
2. Back up the thesis file to `/private/tmp`.
3. Determine whether the change is low-risk or structural:
   - low-risk: run/paragraph font, spacing, small table/image adjustments, isolated footer fixes
   - structural: cover-page replacement, second-page replacement, section-break edits, TOC structure changes, header/footer part transplant
4. For structural work, experiment on a temp copy first.

## 3. Front Matter

Check in this order:

1. Cover page
   - title block alignment
   - line spacing
   - font family / size / weight
   - field positions
   - preserved original text content
2. Second page / declaration / approval page
   - page layout matches template
   - page-specific line and paragraph layout matches template
   - no extra blank paragraphs introduced
3. Abstract pages
   - headings
   - body font
   - keywords line
   - page spacing

Preferred fix order:

1. copy template layout block
2. restore thesis text
3. re-check affected page render

## 4. Table of Contents

1. Compare TOC font, size, alignment, indentation, leader dots, and line spacing to the template TOC.
2. Confirm TOC text is not accidentally formatted like body text.
3. Preserve TOC field machinery if present.
4. If the template TOC is multi-style, compare each visible level separately.

## 5. Body Headings

Check:

1. chapter titles
2. level-2 headings
3. level-3 headings
4. numbering format consistency
5. punctuation after headings

Rules:

- Allow chapter starts on new pages when required.
- Remove other avoidable manual page breaks.
- Compare against the matching heading level in the template, not against neighboring thesis text.

## 6. Body Typography

Check:

1. body font family
2. font size
3. line spacing
4. first-line indent / paragraph spacing
5. English term capitalization consistency when the user asks for strict text-format review

Do not rewrite content unless the user asks.

## 7. Figures

Check:

1. image displays normally
2. caption is below the image
3. caption remains visually paired with the image
4. figure is cited in the body when the review scope includes citation rules
5. figure does not force large avoidable blank space

Preferred fixes:

1. modest resize
2. local paragraph/order adjustment
3. local keep-with-next / keep-lines setting adjustment
4. targeted page-break adjustment

## 8. Tables

Check:

1. caption is above the table
2. table matches required line style, including three-line-table rules when required
3. table font family / size is consistent
4. cell alignment and spacing are intentional
5. table does not create large avoidable blank space

Preferred fixes:

1. per-table geometry adjustment
2. local font and alignment normalization
3. local paragraph flow adjustment around the table

## 9. In-text Citation Superscripts

1. Identify the template behavior for citation superscripts first.
2. Inspect all occurrences of the affected citation pattern, not only the first visible one.
3. Check:
   - superscript positioning
   - font/size
   - bracketed number style
   - spacing relative to punctuation
4. Repair only the affected runs.

## 10. Reference List

1. Compare paragraph indentation and hanging indent to the template.
2. Compare alignment, font, size, and line spacing to the template reference list.
3. Keep numbering/list presentation consistent across entries.
4. If asked for GB-format correctness, validate each entry externally; otherwise report the result as visual normalization only.

## 11. Headers, Footers, and Page Numbers

1. Map section boundaries first.
2. Compare header/footer content and formatting section by section.
3. Check first-page-different settings and page-number behavior.
4. Patch only the drifting section when possible.

## 12. White Space and Blank Pages

Check:

1. accidental blank pages
2. avoidable large blank areas not caused by required chapter starts
3. hidden manual page breaks
4. object-induced half-page white space

Rules:

- Chapter boundaries may start a new page if required.
- Other content should stay compact.
- Prefer local reflow around the offending object instead of global chapter movement.

## 13. Delivery Gate

Before reporting completion:

1. Confirm the fix stayed inside the requested boundary.
2. Confirm intermediate files were kept out of the repo.
3. Record evidence honestly:
   - render-verified
   - word-open-safe-but-not-rendered
   - needs-template-check
   - blocked
