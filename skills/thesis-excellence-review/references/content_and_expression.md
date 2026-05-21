# Section Content And Academic Expression

## Section-Level Checks

For each section ask:

1. What is this section responsible for?
2. Does the text match the title?
3. Does it explain why this design or result matters for this system?
4. Are terms explained in the project context, not as generic encyclopedia text?
5. Does each paragraph add new information?
6. Is there a figure/table before or after this section that must be explained?

## Natural Low-AIGC Writing Rules

Avoid making prose mechanically “humanized.” Keep clarity first.

High-risk AI patterns:

- Dense chains of “首先、其次、最后、此外、因此、综上所述”.
- Repeated frames: “该模块负责…”, “该设计能够…”, “系统通过…实现…”.
- Empty praise: “显著提升”, “极大增强”, “具有重要意义”, “提供有力支撑”.
- Over-abstract nouns with few concrete objects: 系统、模块、机制、能力、质量、效率.
- Symmetric three-part lists in every paragraph.

Preferred fixes:

- Use the concrete module/data/condition as the subject.
- Replace praise with observable behavior or measured result.
- Mix short and medium sentences.
- Keep necessary transitions but do not force enumeration.
- Add boundary conditions when evidence is limited.

## Technical Specificity

A strong section usually names:

- Input and output.
- Main component or file/module.
- Decision condition or threshold, if real.
- Data flow or state field.
- Failure path or limitation.
- Link to figure/table or experiment.

## Do Not

- Invent metrics, datasets, model versions, references, screenshots, or deployed usage.
- Make a bachelor thesis sound like a doctoral dissertation.
- Delete all connectives and damage readability.
- Replace accurate terms with vague synonyms just to reduce AI feel.
- Rewrite a whole section when a paragraph-level repair is enough.
