# ywc-design-renew

A Codex Skill that renews generic or "AI-made" (AI-slop) frontend surfaces
into distinctive designs, and audits a UI for AI-slop design tells. It delegates
to the `impeccable` skill as its design engine when installed, and falls back to
a self-contained ruleset otherwise — so it works in any project or runtime.

## Overview

LLM-generated UIs converge on predictable visual clichés — cyan-on-dark palettes,
gradient text, border-left accent stripes, Inter, uniform card grids — because
every model was trained on the same templates. This skill detects (check) and
removes (renew) those AI-slop signals.

- **renew mode (default)**: takes an existing surface, improves it toward a bold
  aesthetic direction, and leaves before/after evidence.
- **check mode**: audits for AI-slop without editing, applying a pass/fail gate.

The anchoring criterion is the **AI Slop Test** — "If you showed this and said
'AI made this,' would they believe you immediately?"

## Prerequisites

- (Optional) `impeccable` skill — delegated to as a stronger design engine when
  present; self-contained ruleset fallback otherwise. If your project supports
  it, `npx impeccable skills install` can install the external skill. After
  installing, run `impeccable init` once to set the project Design Context — it
  writes the `PRODUCT.md` / `DESIGN.md` files below so the context questions are
  skipped.
- (Optional) A live URL (local dev server) — used by Chrome DevTools MCP for
  before/after screenshots.
- (Optional) `.impeccable.md` / `PRODUCT.md` / `DESIGN.md` — skips the
  context-gathering questions when Design Context already exists.

## Use Cases

- "This dashboard looks too generic, like an AI made it. Renew it."
- "Before release, check this screen for AI-slop design tells."
- "Redesign the hero section to feel distinctive."

## Usage

```text
Use $ywc-design-renew to renew src/components/hero with --url http://localhost:3000.
Use $ywc-design-renew --mode check --target src/app/dashboard --fail-on critical.
```

Or invoke in natural language:

> "This screen looks AI-generated. Please renew the design."

## Input

- **Required**: `--target` (component / page / route) plus Design Context
  (audience / use-cases / brand tone)
- **Optional**: `--url` (live screenshots), `--mode check`, `--fail-on`,
  `--format html`

## Output

- **renew**: renewed code plus a renewal report (chosen direction, resolved slop
  findings before→after, changed files, re-audit result, before/after
  screenshots)
- **check**: a prioritized (Critical / High / Medium / Low) slop audit report
  with the `--fail-on` gate verdict

## Related Skills

- `impeccable` — delegated design engine when installed (craft / polish / audit)
- `ywc-ui-ux-review` — verifies the usability / IA / WCAG axis after renewal
  (this skill owns only the aesthetic / slop axis)
- `ywc-review-learnings` — accumulates confirmed design preferences per project
