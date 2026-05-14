---
name: ywc-ui-ux-review
description: "(ywc) Use when the user wants a UI/UX review combining static code analysis with live UI exploration (available browser tooling) covering information architecture, visual design, usability, and accessibility. Triggers: 'UI/UX review', 'UX 점검', 'UI 검토', 'usability audit', 'design review', 'accessibility review', '사용성 점검', '디자인 리뷰', 'UX 監査', 'UI レビュー'. Do not use for backend/API review (use ywc-impl-review), product/business strategy review (use ywc-product-review), or code-only review without a running UI."
---

# UI/UX Review — Hybrid (Code + Live UI)

**Announce at start:** "I'm using the ywc-ui-ux-review skill to combine static code analysis with live UI exploration."

Conduct a prioritized UI/UX review of a project by combining static code analysis with live UI exploration. Focus areas: Information Architecture and Visual Design. Output: a four-tier (Critical / High / Medium / Low) Markdown report.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Code-only review is enough, no need to launch the browser" | Hybrid means **both**. Static analysis cannot detect runtime layout shift, focus traps, or hover state breakage. |
| "WCAG checks are exhaustive, skip them on internal tools" | Internal tools have employees with disabilities too. WCAG 2.2 AA is the minimum, not an opt-in. |
| "Reduced motion / dark mode are edge cases, drop them" | These are accessibility requirements, not edge cases. Test both. |
| "Severity feels Critical, mark it Critical regardless of impact" | Critical = blocks core flow or violates accessibility law. Reserve it. Inflated severity buries real critical findings. |
| "Visual taste is subjective, do not flag design inconsistency" | Inconsistency in tokens (color, spacing, typography) is objective. Always flag. |
| "Live exploration is risky on production, skip it" | Use a staging or preview URL. Skipping live exploration drops half the value of this skill. |

**Violating the letter of these rules is violating the spirit.** Static-only review with no live UI is design auditing on paper.

## Triggers

- "Review the UI/UX of this project"
- "Audit usability of {feature/page}"
- Information Architecture or navigation evaluation
- Visual hierarchy / typography / spacing / color audit
- Pre-release UX checks against WCAG 2.2 AA
- Cross-cutting design review against an internal design system

## Workflow

Run the six phases in order. Skip a phase only with explicit user consent.

### Phase 1 — Scope & Context

Confirm the following with the user before any analysis. When ambiguous, ask:

- **Target**: pages, routes, or feature flows in scope
- **Primary user journey**: the one or two flows that matter most
- **Stack**: framework (React / Vue / Flutter / Astro / etc.) and design system in use
- **Live URL**: a running URL or local dev server (required for Phase 3)
- **Internal design system**: location of tokens, components, design guidelines (if any)

If no live URL is available, note it in the report and proceed with code-only review (degrade gracefully).

### Phase 2 — Code Reconnaissance

Use Codex file and shell tools to map. Prefer `rg`, `rg --files`, `find`, and targeted file reads:

- Routing tree and navigation structure (router config, route files)
- Top-level layouts and shell components
- Design tokens (colors, typography, spacing) — typically `tokens.css`, `theme.ts`, `tailwind.config.*`, `*.tokens.json`, `design-system/`
- Shared UI components and their variants
- Localization / i18n surface, if any

Capture findings as raw notes — do not score yet.

### Phase 3 - Live UI Exploration

Use the best available Codex browser capability for inspection-focused analysis. Prefer Playwright or a browser MCP when available; use available browser tooling if the environment exposes it. If no browser tool is available, note the limitation and continue with code-only review.

Recommended browser evidence sequence:

1. `browser open/navigation tool` or `navigate_page` — open the target URL
2. `browser accessibility or DOM snapshot tool` — get accessibility tree (token-efficient, structured)
3. `browser screenshot tool` — capture visual evidence per breakpoint
4. `browser resize tool` — repeat for 360 / 768 / 1280 / 1920
5. `browser audit tool` — automated accessibility / performance scoring
6. `browser console inspection tool` — surface runtime errors
7. `browser script evaluation tool` — pull computed styles, contrast, focus chain when needed

For each piece of evidence record: URL, breakpoint, screenshot reference, snapshot excerpt.

### Phase 4 — Per-Domain Review

Apply checklists in this order:

1. **Information Architecture** → load `references/ia-checklist.md`
2. **Visual Design** → load `references/visual-design-checklist.md`
3. Cross-check each finding against `references/heuristics-combined.md` to attach an authoritative citation (Nielsen / WCAG / Material / HIG / internal design system) to every issue.

Every issue must include:

- Concrete location (file path + line number, OR screen + selector)
- Observed behavior
- Expected behavior (per heuristic)
- Heuristic citation (which framework, which item)

### Phase 5 — Severity Triage

Load `references/severity-rubric.md` and classify every finding into one of: Critical / High / Medium / Low. The rubric is the single source of truth — do not invent custom levels.

### Phase 6 — Report Generation

Generate the report using `assets/report-template.md` as the structural template. Fill all placeholders. Default output path: `claudedocs/ui-ux-review-{YYYY-MM-DD}.md` unless the user specifies otherwise.

## Reference Files

| File | When to load |
|---|---|
| `references/ia-checklist.md` | Phase 4, IA review |
| `references/visual-design-checklist.md` | Phase 4, Visual Design review |
| `references/heuristics-combined.md` | Phase 4, attaching authoritative citation |
| `references/severity-rubric.md` | Phase 5, severity classification |
| `assets/report-template.md` | Phase 6, report scaffolding |

## Output Rules

- **Every finding cites a heuristic** (Nielsen #N / WCAG SC X.X.X / Material spec / HIG section / internal token name)
- **Every finding has a location** (file:line OR screen:selector)
- **Every finding has a concrete recommendation** — code snippet or design change, not just "improve UX"
- Group findings under the four severity tiers exactly as the template defines
- Lead the report with an executive summary: count per tier, top 3 systemic patterns, top 5 recommended actions
- Keep tone factual and respectful — review the work, not the people

## Advisor Escalation Policy

**Budget**: up to **2 high-capability advisor calls per invocation**.

Escalate to an high-capability advisor only when the executor cannot resolve the severity classification from `references/severity-rubric.md` alone. Two conditions qualify:

| Condition | Example |
|---|---|
| **Borderline Critical vs High** | An accessibility issue blocks assistive-technology users on a primary flow, but only under a specific screen-reader / browser combination that the rubric does not explicitly address — both Critical and High are defensible |
| **Heuristic conflict** | Nielsen's "Visibility of system status" (#1) and Apple HIG's "Clarity" principle produce opposite recommendations for the same UI element (e.g., a persistent loading indicator that aids status visibility but creates visual noise per HIG clarity) |

For all other borderline cases — High vs Medium, Medium vs Low, uncertain evidence from code-only analysis — choose the more conservative (lower) tier and add a brief inline note explaining the uncertainty. Do not escalate these to Opus.

## Boundaries

**Will:**

- Review IA, Visual Design, accessibility, and usability of the target project
- Combine static code evidence with live UI evidence
- Produce a prioritized, citation-backed Markdown report

**Will Not:**

- Re-design or refactor code on the user's behalf (review only — implementation is a separate task)
- Fabricate findings without code or runtime evidence
- Replace formal user testing with real users
- Score subjective beauty — every judgment is anchored to a heuristic
