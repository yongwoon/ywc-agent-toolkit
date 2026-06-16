# Anti-Slop Ruleset (Self-Contained, Portable)

This is the **fallback design-quality ruleset** that makes `ywc-design-renew`
work without the external `impeccable` skill installed. It is distilled from
impeccable's `absolute_bans` + DO/DON'T guidance and the project-wide
Anti-Template Policy. When `impeccable` IS available, prefer delegating to it
(see [impeccable-delegation.md](impeccable-delegation.md)); this file is the
portable baseline used everywhere else, and the scoring rubric for **check
mode** in both cases.

## Part A — The AI Slop Test (the gate)

The single qualitative question that anchors every finding:

> If you showed this interface to someone and said "AI made this," would they
> believe you **immediately**?

If yes, that is the problem. A distinctive interface makes someone ask "how was
this made?" not "which AI made this?" Every detector rule below is a concrete,
checkable instance of this test.

## Part B — Critical bans (auto-fail in check mode)

These are the most recognizable AI tells. Any occurrence is a **Critical** slop
finding. Each row gives a grep-able signal so check mode can detect it
mechanically before any judgment pass.

| ID | Ban | Detection signal (grep / inspect) | Why it is slop | Fix direction |
|---|---|---|---|---|
| B1 | Side-stripe accent border | `border-left:` / `border-right:` with width > 1px (incl. CSS vars) | The single most overused dashboard/admin/medical "design touch"; never looks intentional | Rewrite the element structure — full border, background tint, leading number/icon, or no indicator |
| B2 | Gradient text | `background-clip: text` / `-webkit-background-clip: text` + any `*-gradient(` | Decorative, not meaningful; a top-3 AI tell | Single solid color; emphasize with weight/size |
| B3 | AI color palette | cyan-on-dark, purple→blue gradients, neon accent on dark | The default "cool" palette every model reaches for | Derive palette from brand hue in OKLCH (Part D) |
| B4 | Default dark + glowing accents | `#000`/near-black bg + saturated glow shadows as the default theme | "Looks cool" without an actual design decision | Derive theme from audience/context, not reflex |
| B5 | Pure black / pure white | `#000`, `#fff`, `rgb(0,0,0)`, `rgb(255,255,255)` on large surfaces | Never appears in nature; reads as un-tuned | Tint toward brand hue (even chroma 0.005–0.01) |

## Part C — High-severity tells

Each occurrence is a **High** slop finding (judgment may downgrade a single
isolated instance to Medium with a noted reason).

| ID | Tell | Detection signal | Fix direction |
|---|---|---|---|
| C1 | Overused fonts | `Inter`, `Roboto`, `Arial`, `Open Sans`, system stack, or the reflex set (Fraunces, Newsreader, Playfair, Space Grotesk, DM Sans, Plus Jakarta, Outfit, IBM Plex, Cormorant, Syne, Instrument…) | Pick against 3 brand words from a catalog (Part D) — do NOT switch to your second-favorite |
| C2 | Uniform card grid | repeated same-size cards: icon + heading + text, `repeat(auto-fit,...)` with identical content shells | Break the grid; vary emphasis; flatten nesting |
| C3 | Nested cards | a card surface inside another card surface | Flatten the hierarchy |
| C4 | Everything centered | `text-align: center` + `margin: auto` as the page-wide default | Left-align with asymmetric composition |
| C5 | Uniform spacing | one padding value everywhere; no rhythm | 4pt scale with varied rhythm (Part D) |
| C6 | Hero-metric template | big number + small label + supporting stats + gradient accent block | Design the data as part of the system, not a template |
| C7 | Glassmorphism everywhere | blur/glass/glow used decoratively on many surfaces | Reserve for one purposeful moment, if at all |
| C8 | Monospace as "technical" vibe | body/UI set in monospace for developer aesthetic | Monospace only for code/data |
| C9 | Bounce / elastic easing | `cubic-bezier` bounce, `bounce`, `elastic`, `back` easing | Exponential ease-out (real objects decelerate smoothly) |
| C10 | Animating layout props | transition/animation on `width`/`height`/`top`/`left`/`margin`/`padding` | Animate `transform` / `opacity` only |
| C11 | Gray text on colored bg | gray (`#888` family) text over a non-neutral background | Use a shade of the background color instead |
| C12 | Flat type hierarchy | heading/body sizes < 1.25 ratio apart | ≥1.25 ratio, fewer sizes with more contrast |

## Part D — DO rules (apply during renew; always-on, no reference needed)

These are the positive moves that replace the bans. Apply them directly.

### Typography

- Modular type scale, fluid `clamp()` on marketing/content headings; fixed `rem`
  scale for app/dashboard UI.
- Fewer sizes, more contrast — ≥1.25 ratio between steps.
- Pair a distinctive display font with a refined body font. Choose against 3
  concrete brand words (e.g. "warm + mechanical + opinionated"), browsing a
  catalog as a physical object (shop sign, terminal manual, fabric label) — not
  "modern/elegant" (dead categories).
- Cap line length ~65–75ch. All-caps only for short labels.

### Color

- OKLCH, not HSL (perceptually uniform). Reduce chroma toward white/black.
- Tint neutrals toward the brand hue (chroma 0.005–0.01 is perceptible).
- 60-30-10 by visual *weight*: 60% surface / 30% secondary / 10% accent.
- Theme derived from audience + viewing context, never a default.
- Modern CSS: `oklch()`, `color-mix()`, `light-dark()`.

### Layout & space

- 4pt scale with semantic token names (`--space-sm`, not `--spacing-8`):
  4, 8, 12, 16, 24, 32, 48, 64, 96.
- `gap` over margins for sibling spacing.
- Vary spacing for hierarchy; embrace asymmetry; break the grid intentionally.
- Self-adjusting grid: `repeat(auto-fit, minmax(280px, 1fr))`.
- Container queries for components, viewport queries for page layout.

### Motion / interaction

- One well-orchestrated page load with staggered reveals > scattered
  micro-interactions.
- Exponential ease-out; `transform`/`opacity` only; `grid-template-rows` for
  height reveals.
- Progressive disclosure; empty states that teach; hierarchy of button weights
  (not every button primary).

## Part E — Required qualities (renew acceptance bar)

A renewed surface should demonstrate **at least four**:

1. Clear hierarchy through scale contrast
2. Intentional spacing rhythm (not uniform padding)
3. Depth/layering via overlap, surfaces, or motion
4. Typography with a real pairing strategy
5. Color used semantically, not decoratively
6. Designed hover / focus / active states
7. Grid-breaking editorial or bento composition where it fits
8. Texture / grain / atmosphere when it suits the direction
9. Motion that clarifies flow
10. Data visualization treated as part of the design system

## Scoring map (check mode)

| Finding source | Severity |
|---|---|
| Any Part B row | Critical |
| Any Part C row | High |
| < 4 of Part E qualities present on a primary surface | Medium |
| Token inconsistency (color/spacing/type not from a scale) | Medium |
| Minor polish (single isolated instance, easily fixed) | Low |

Check mode **fails** when Critical count > 0 (default `--fail-on critical`).
