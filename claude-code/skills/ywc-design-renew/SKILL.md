---
name: ywc-design-renew
description: >-
  (ywc) Use when an existing frontend surface looks generic, template-like, or
  "AI-made" and the user wants to renew its visual design to feel distinctive, or
  to audit a UI specifically for AI-slop design tells (gradient text,
  cyan-on-dark, Inter, uniform card grids) before shipping.
  Triggers: "디자인 리뉴얼", "디자인이 너무 평범해", "LLM이 만든 것 같은 디자인", "AI 슬롭",
  "design renew", "de-slop this UI", "make this design less generic", "make it
  look less AI-generated", "디자인 개선", "이 화면 AI slop 점검", "AI slop check",
  "デザインリニューアル", "AIっぽいデザインを直して", "デザイン刷新". Do not use for usability /
  information-architecture / WCAG accessibility audit or a general design / UX
  review (use ywc-ui-ux-review), building a brand-new UI or component from scratch
  rather than renewing an existing one (use the frontend-design or impeccable
  skill), backend or API review (use ywc-impl-review), product / business strategy
  review (use ywc-product-review), or only persisting a design preference without
  changing code (use ywc-review-learnings).
---

# Design Renew — De-Slop & Check

**Announce at start:** "I'm using the ywc-design-renew skill to renew the design and check it against AI-slop tells."

This skill takes an existing frontend surface that reads as generic or
"AI-generated" and renews it into something distinctive, then verifies the result
against an anti-slop audit. The user provides a target (component, page, or
route) and design context (audience, use-case, brand tone); the skill produces
either renewed code with before/after evidence (`--mode renew`, default) or a
prioritized slop-audit report with a pass/fail gate (`--mode check`). It uses the
`impeccable` skill as its design engine when installed, and a self-contained
portable ruleset otherwise — so it works in any project or runtime.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "I can infer the design context from the codebase — skip the context step" | Code tells you what was built, not who it is for or how it should feel. Renewing without audience / use-case / brand tone produces *generic* output — the exact AI-slop you were asked to remove. Always confirm the three context inputs first. |
| "impeccable isn't installed, so I can't renew the design" | impeccable is an enhancement, not a hard dependency. The self-contained `references/anti-slop-ruleset.md` is the portable baseline — run it. Refusing to act because an optional skill is absent defeats the skill's portability purpose. |
| "Inter is banned, so I'll just switch to Fraunces / my next-favorite font" | Swapping to your second-favorite recreates the monoculture one font over. The whole reflex set is banned. Pick against 3 concrete brand words from a catalog, evaluating the font as a physical object. |
| "A colored border-left stripe / gradient heading adds visual flair" | Those are the top AI tells (Critical bans B1/B2). They never look intentional. Rewrite the element structure entirely — do not just recolor the stripe. |
| "Beauty is subjective — I can't audit design quality objectively" | Token inconsistency and the banned-pattern set are objective and grep-able. The AI Slop Test is the gate. Subjectivity is not a license to skip the audit. |
| "Renew means redesign everything from scratch" | Renewal changes aesthetic *execution*, not behavior or information architecture. Preserve working flows, routes, and IA; do not break functionality to chase a look. |
| "Default to dark mode with glowing accents — it looks polished" | That is the lazy reflex and itself a slop tell (B4). Theme is derived from audience and viewing context, not picked for cool factor. |
| "The code diff is enough — skip the before/after screenshot" | Design is visual. A diff hides layout shift, contrast regressions, and broken hover states. Capture both states when a live URL exists; this is the only proof the renewal helped. |

**Violating the letter of these rules is violating the spirit.** A "renewal" that swaps one slop pattern for another, or skips the context gate, ships the same AI-generated feel under a new coat of paint.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--mode` | `--mode renew\|check` | `--mode check` | `renew` (default): apply de-slop improvements. `check`: audit only, no edits, with a pass/fail gate. |
| `--target` | `--target <path\|route>` | `--target src/components/hero` | Surface to renew or check. Required. |
| `--url` | `--url <live-url>` | `--url http://localhost:3000` | Live URL for before/after screenshots (Phase 1 + 4). Optional; degrades to code-only. |
| `--fail-on` | `--fail-on critical\|high\|none` | `--fail-on high` | check-mode gate threshold. Default `critical` (fail if any Critical slop finding). |
| `--format` | `--format markdown\|html` | `--format html` | Report format for check mode. Default `markdown`. See [../references/html-output.md](../references/html-output.md). |

## Workflow

Run the phases in order. `--mode check` stops after Phase 2.

### Phase 0 — Capability & context gate

1. **Detect impeccable.** Set `IMPECCABLE_AVAILABLE` per
   [references/impeccable-delegation.md](references/impeccable-delegation.md).
   This decides the engine for every later phase.
2. **Load prior learnings.** If `docs/review-learnings.md` exists, run
   ywc-review-learnings `--mode read` scoped to the target's file glob and apply
   any design-polarity learnings (e.g. a project that prefers a specific font
   pairing, or has marked a pattern as a `FALSE-POSITIVE`).
3. **Confirm design context (REQUIRED).** You cannot infer this from code.
   Obtain audience, use-cases, and brand tone via the handshake in
   impeccable-delegation.md (read `.impeccable.md` / `PRODUCT.md` / `DESIGN.md`
   → else `/impeccable teach` → else ask the three questions inline). Do not
   proceed to renew without it.

### Phase 1 — Baseline capture

- Read the target's component/style/token files; note the current fonts, color
  values, spacing scale, and layout structure.
- If `--url` is set, capture **before** screenshots at 320 / 768 / 1024 / 1440
  via Chrome DevTools MCP (`new_page` → `resize_page` → `take_screenshot`).
- This baseline is the comparison anchor for Phase 4 — do not skip it.

### Phase 2 — Check (anti-slop audit)

Detect every slop tell against the target:

- **With impeccable**: delegate to `/impeccable audit <scope>` (or
  `npx impeccable detect <path>` for the CLI-only path).
- **Self-contained**: grep the Part B / Part C detection signals in
  [references/anti-slop-ruleset.md](references/anti-slop-ruleset.md), then apply
  the AI Slop Test and Part E required-qualities count as a judgment pass.

Classify each finding with the scoring map (Critical / High / Medium / Low).

**If `--mode check`**: emit the audit report (see Output Format), apply the
`--fail-on` gate, and **stop**. Do not edit code in check mode.

### Phase 3 — Renew (apply improvements)

1. **Commit to a bold direction.** From the Phase 0 context, choose one clear
   aesthetic point of view (editorial, brutalist, refined-minimal, retro-
   futuristic, etc.). Intentionality over intensity — both maximal and minimal
   work if executed precisely. Do not converge on the same direction across
   projects.
2. **Apply the engine.**
   - **With impeccable**: `/impeccable craft <feature>` for a new surface, or
     `/impeccable polish <scope>` to refine the existing one.
   - **Self-contained**: apply Part D DO rules — modular type scale + deliberate
     font pairing, OKLCH palette tinted to the brand hue, 4pt spacing with varied
     rhythm, asymmetric/grid-breaking composition, motion on transform/opacity —
     while removing every Part B / Part C tell found in Phase 2.
3. **Preserve behavior.** Keep routes, IA, data flow, and accessibility
   semantics intact. Renewal is aesthetic execution, not a functional rewrite.

### Phase 4 — Verify

- **Re-audit.** Re-run Phase 2 detection; confirm Critical/High findings are
  resolved and no new tell was introduced.
- **Before/after.** If `--url` is set, capture **after** screenshots at the same
  breakpoints and present them paired with the Phase 1 baseline.
- **Hand off the other axis.** Renewal covers aesthetics only. Recommend
  ywc-ui-ux-review for the usability / IA / WCAG axis — do not claim those here.

### Phase 5 — Capture learnings (optional)

If the user accepted or rejected a specific design choice during renewal (a font
pairing, a palette, a "we never use X here"), offer to persist it via
ywc-review-learnings `--mode update --source review` so future renewals on this
repo start sharper. Never write learnings without the user's confirmation.

## Banned Output Patterns

Never emit these in renewed code — they are the slop tells the skill exists to
remove. Full detection signals in
[references/anti-slop-ruleset.md](references/anti-slop-ruleset.md).

| Banned pattern | Replace with |
|---|---|
| `border-left/right` > 1px accent stripe (incl. CSS vars) | Full border, background tint, leading number/icon, or no indicator |
| `background-clip: text` + any gradient (gradient text) | Single solid color; emphasize with weight/size |
| cyan-on-dark / purple→blue gradient / neon-on-dark palette | OKLCH palette derived from the brand hue |
| Pure `#000` / `#fff` on large surfaces | Tinted near-black / near-white toward brand hue |
| `Inter` / `Roboto` / system stack / the reflex font set | A font chosen against 3 brand words from a catalog |
| Animating `width`/`height`/`top`/`left`/`margin`/`padding` | Animate `transform` / `opacity` only |
| Bounce / elastic / `back` easing | Exponential ease-out |
| Nested cards / uniform icon-heading-text card grid | Flattened hierarchy; varied, grid-breaking composition |

## Output Format

**check mode** — Markdown audit report (default path
`claudedocs/design-slop-audit-{YYYY-MM-DD}.md`):

```text
# Design Slop Audit — <target>
## Verdict: FAIL (2 Critical) — gate: --fail-on critical
## Summary: 2 Critical · 3 High · 1 Medium · 0 Low

### Critical
- [B2 Gradient text] src/components/Hero.tsx:42
  Observed: `background-clip: text` on the H1 with a purple→blue gradient.
  Why: top-3 AI tell — decorative, not meaningful.
  Fix: solid `oklch(...)` fill; emphasize with weight.

### High
- [C1 Overused font] src/styles/tokens.css:7 — `--font-display: Inter`.
  Fix: pair a display face chosen against the brand words "<w1> <w2> <w3>".
...
### Required-qualities check (Part E): 2 / 4 minimum — BELOW BAR
```

**renew mode** — renewal report:

```text
# Design Renewal — <target>
## Direction: <chosen aesthetic POV> — rationale: <1 line from context>
## Engine: impeccable polish | self-contained ruleset
## Slop findings resolved: 2 Critical, 3 High (before → after table)
## Files changed: <list>
## Verification: re-audit 0 Critical · before/after screenshots @ 320/768/1024/1440
## Next: ywc-ui-ux-review for the usability / IA / WCAG axis
```

## Validation

Before declaring the task complete, verify:

- [ ] Design context (audience / use-cases / brand tone) was confirmed, not inferred
- [ ] `IMPECCABLE_AVAILABLE` was detected and the correct engine path was used
- [ ] (renew) Every Phase 2 Critical/High finding is resolved in the re-audit
- [ ] (renew) No new Banned Output Pattern was introduced
- [ ] (renew) Behavior / routes / IA / a11y semantics are unchanged
- [ ] (check) Every finding has an ID, file:line, observed, why, and fix
- [ ] (check) The `--fail-on` gate verdict is stated explicitly
- [ ] Before/after screenshots captured when `--url` was provided

## Common Mistakes

- **Skipping the context gate** because "the codebase makes it obvious" — it does
  not. Generic context is the root cause of generic output. Confirm the three
  inputs every time.
- **Treating impeccable as required** — the skill must degrade gracefully to the
  self-contained ruleset. Never refuse to act because impeccable is absent.
- **Font monoculture by reflex** — banning Inter and reaching for Fraunces is the
  same failure one step over. Use the brand-words procedure.
- **Claiming the usability axis** — this skill audits aesthetics/slop, not WCAG or
  IA. Hand that to ywc-ui-ux-review rather than over-claiming coverage.
- **Renewing without a before baseline** — without Phase 1 capture there is no
  evidence the renewal improved anything.

## Integration

- **Upstream**: N/A — standalone; optionally consumes `.impeccable.md` /
  `PRODUCT.md` / `DESIGN.md` and `docs/review-learnings.md` when present.
- **Downstream**: ywc-ui-ux-review (usability / IA / WCAG verification on the
  renewed surface); ywc-review-learnings (persist accepted design preferences).
- **Pairs with**: the `impeccable` skill (design engine when installed) and the
  `frontend-design` skill (alternative generative engine).
