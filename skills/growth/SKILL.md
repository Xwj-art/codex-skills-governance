---
name: growth
description: Use when Codex needs to improve SEO, social sharing metadata, structured data, AI-search citation readiness, Core Web Vitals tied to SEO, conversion CTAs, forms, or funnel-oriented page changes. Do not use for generic frontend polish, analytics dashboards, or broad content writing unless growth metrics are the goal.
---

# Growth

Use this skill for growth work with a measurable outcome: search visibility,
social preview quality, AI citation readiness, conversion rate, form completion,
or page-speed metrics that affect acquisition.

## Boundaries

Use `growth` for:

- SEO metadata: title, description, canonical, robots, sitemap/robots checks.
- Heading hierarchy and crawlable semantic structure.
- Open Graph and Twitter/X card metadata.
- JSON-LD structured data that matches visible page content.
- GEO / AI-search citation readiness: answer-first content, entity clarity,
  crawlability, credible citations, and structured extraction.
- Core Web Vitals when the user goal is SEO or acquisition impact.
- CRO changes: CTA placement/copy, form friction, conversion path issues.

Do not use `growth` for:

- generic UI redesign without a search/conversion goal,
- product analytics dashboard design,
- pure backend performance,
- broad copywriting that is not tied to SEO/GEO/CRO,
- dark patterns or manipulative conversion tactics.

## Workflow

1. **AUDIT**
   Identify current state before changing anything: page type, target metric,
   existing metadata, headings, schema, crawlability, page speed, CTA/form path,
   and available analytics.

2. **SELECT**
   Pick one primary lever: `seo`, `smo`, `geo`, `vitals`, `cro`, or `audit`.
   Avoid mixing unrelated growth experiments in one pass.

3. **IMPLEMENT**
   Make the smallest change that can improve the chosen metric. Preserve visible
   truth: schema, metadata, and claims must match page content.

4. **VERIFY**
   Provide concrete validation: rendered head tags, JSON-LD parse result,
   Lighthouse/Web Vitals target, social preview check, or CRO hypothesis and
   measurement plan.

## Recipe Map

- `seo`: read `references/seo-checklist.md`.
- `smo`: read `references/ogp-twitter-card-guide.md`.
- `geo`: read `references/json-ld-templates.md` and relevant sections of
  `references/seo-checklist.md`.
- `vitals`: read `references/core-web-vitals.md`; use
  `references/core-web-vitals-deep.md` for deeper debugging.
- `cro`: read `references/cro-patterns.md`.
- `audit`: read `references/seo-audit.md`.
- `keyword`: read `references/keyword-research.md`.

Load only the reference needed for the selected recipe.

## Output Requirements

Every answer or patch should state:

- target metric,
- changed surface,
- expected or measured impact,
- validation method,
- remaining risks or data gaps.

For implementation work, include the exact files changed and verification
commands or tools used.

## Guardrails

- Ask before adding analytics scripts, trackers, consent-affecting behavior, or
  new routes.
- Respect GDPR/CCPA and existing consent flows.
- Do not declare A/B winners without adequate data.
- Do not add schema that contradicts visible content.
- Do not hide costs, force deceptive urgency, or use misleading CTAs.
- Treat GEO claims as time-sensitive; verify current platform behavior before
  making strong claims.
