# Visual Design Checklist

Use this checklist during Phase 4 of `ywc-ui-ux-review`. Every "✗" item becomes a report finding; severity is decided in Phase 5 using `severity-rubric.md`.

## Table of Contents

1. Typography hierarchy
2. Color system and contrast
3. Spacing and rhythm
4. Visual hierarchy
5. Alignment and grid
6. Component consistency
7. Iconography
8. Imagery and media
9. Motion (visual subset)
10. Responsive visual integrity
11. Anti-generic design patterns (AI tell detection)

## 1. Typography Hierarchy

- [ ] No more than 2 type families in production (display + body, or single)
- [ ] Type scale is documented (e.g., 12 / 14 / 16 / 20 / 24 / 32 / 48) and adhered to
- [ ] Body copy size ≥16px on mobile, ≥14px on dense desktop tables
- [ ] Line-height: ~1.4–1.6 for body, tighter (~1.1–1.2) for headlines
- [ ] Line-length: 50–75 characters for readable body copy
- [ ] No more than 3 weights in active use within a single screen
- [ ] All-caps reserved for labels ≤24 characters; not for sentences

**Code signals**: design tokens, CSS custom properties, Tailwind theme keys, Material `Typography` roles.

## 2. Color System and Contrast

- [ ] Tokenized palette — no hex / rgb literals scattered through components
- [ ] Semantic tokens exist for: `surface`, `text`, `accent`, `success`, `warning`, `danger`, `border`, `muted`
- [ ] **WCAG 2.2 AA — text contrast ≥4.5:1** for body, ≥3:1 for large text (≥18.66px regular OR ≥14px bold)
- [ ] **Non-text contrast ≥3:1** for UI components and graphical objects (WCAG SC 1.4.11)
- [ ] Focus indicator contrast ≥3:1 against adjacent colors (WCAG SC 2.4.11 / 2.4.13)
- [ ] State colors (hover / active / disabled / focus) are derivable from the base, not arbitrary
- [ ] Color is never the sole carrier of meaning (icon + label + color, not color alone) (WCAG SC 1.4.1)
- [ ] Dark mode (if shipped) uses an inverted *intent* mapping, not a naive color flip

**Verification**: `browser script evaluation tool` to read computed styles and compute contrast ratios when in doubt.

## 3. Spacing and Rhythm

- [ ] Spacing scale is tokenized (e.g., 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64)
- [ ] Multiples of the base unit are used everywhere — no `padding: 13px`
- [ ] Vertical rhythm between sections is consistent
- [ ] Touch targets ≥24×24 CSS pixels (WCAG 2.2 SC 2.5.8 minimum); prefer ≥44×44 on mobile
- [ ] Spacing scales appropriately across breakpoints (not fixed pixel margins everywhere)
- [ ] No "orphaned" white space that isolates an element from its meaning group

## 4. Visual Hierarchy

- [ ] Each screen has one clear primary focus, supported by scale / weight / color
- [ ] Importance maps to size, then weight, then color — not arbitrary emphasis
- [ ] Decorative elements never out-weigh interactive elements
- [ ] First viewport answers "What is this and what can I do here?"

## 5. Alignment and Grid

- [ ] Content respects a defined grid (12-col is conventional; consistency is what matters)
- [ ] Optical alignment is fixed where geometric alignment misleads (e.g., icons in buttons)
- [ ] Form labels and inputs share a consistent alignment (top-aligned recommended for scanability)

## 6. Component Consistency

- [ ] Same UX pattern uses the same component everywhere (one Modal, not three custom dialogs)
- [ ] Variant proliferation is bounded (e.g., Button has size × intent matrix, not ad-hoc props)
- [ ] States exist for: default, hover, focus, active, disabled, loading, error, success
- [ ] Disabled state is not a faded clone of default — it must be visually distinct

## 7. Iconography

- [ ] Single icon set (or visually compatible set) — no mixing line + filled + duotone arbitrarily
- [ ] Icons paired with labels for primary actions (icon-only only when the metaphor is unambiguous)
- [ ] Icon size aligned with adjacent text size (typically 1× to 1.25× cap-height)
- [ ] Icons that act like buttons have ≥24×24 hit area (preferably ≥44×44 on mobile)

## 8. Imagery and Media

- [ ] Images have explicit `width` and `height` attributes (CLS prevention)
- [ ] Hero / above-the-fold media uses `loading="eager"` and `fetchpriority="high"`; the rest uses `loading="lazy"`
- [ ] Images have meaningful `alt` text, or `alt=""` when purely decorative
- [ ] Aspect ratios are consistent within a content set (e.g., card thumbnails)

## 9. Motion (Visual Subset)

- [ ] Transitions ≤300ms for state changes; ≤500ms for entrance
- [ ] Easing is consistent (a defined curve set, not ad-hoc cubic-bezier values)
- [ ] `prefers-reduced-motion` is honored — non-essential motion is removed or reduced
- [ ] No motion that competes with primary content for attention

## 10. Responsive Visual Integrity

- [ ] Layout integrity verified at 360 / 768 / 1280 / 1920 (use `resize_page` + `take_screenshot`)
- [ ] No horizontal scroll at any tested width
- [ ] Touch targets meet size requirements at the smallest breakpoint
- [ ] Content prioritization adapts (key info first on small screens — not just a squeeze)
- [ ] Sticky elements do not occlude critical content on small viewports

## 11. Anti-Generic Design Patterns (AI Tell Detection)

Detect AI-generated template aesthetics that signal absent design intent. These patterns are acceptable in a scaffold but unacceptable in a shipped product. Flag any ✗ as **Medium** severity minimum; three or more ✗ items within the same group signals a systemic issue — escalate to **High**.

**Evidence requirement per ✗**: screenshot at 1280px + the specific component path (`file:line` or browser selector). Generic patterns are invisible at component level but obvious at full-page scale — always run `take_screenshot` at 1280px before this checklist.

### Layout Tells

- [ ] Page is not built entirely from equal-width 3-column grids
- [ ] Hero section is not the canonical `centered-H1 + subheading + CTA button over gradient blob` and nothing else
- [ ] Sections are not all identical height with perfectly symmetrical left/right splits
- [ ] Page is not composed entirely of alternating full-bleed sections (`text-left/image-right`, `image-left/text-right`)
- [ ] At least one layout element breaks the grid intentionally (editorial overlap, offset card, bento cell, or asymmetric column split)

### Typography Tells

- [ ] Not using only Inter or Roboto (system sans default) with no pairing rationale
- [ ] Heading and body are not the same font at different weights (no typographic voice)
- [ ] H1 is not exactly 2× body size with no intermediate scale steps
- [ ] At least one typographic element uses deliberate weight contrast (e.g., light + bold pairing, or a display cut)

### Color Tells

- [ ] Palette is not exactly `{white background, dark text, one blue/purple accent}` with no variation
- [ ] Gradient usage (if any) is directional and purposeful — not a generic purple-to-blue diagonal blob
- [ ] Accent color appears on more than one element type (not CTAs only)
- [ ] Dark mode (if present) has a considered palette — not `#000000` background with inverted text

### Motion and State Tells

- [ ] Interactive elements have ≥2 visually distinct states (not only `opacity: 0.7` for disabled)
- [ ] Hover transitions are not all uniform `opacity` fades at 200ms
- [ ] At least one entry animation differentiates content sections (not the same `fade-in translateY` on every block)
- [ ] Loading states provide skeleton or contextual indication — not only a centered spinner

### Content Quality Tells

- [ ] No lorem ipsum or obvious placeholder text in shipped code
- [ ] CTA copy is specific to the product ("Start free trial" not "Learn More" / "Get Started" as the only variation)
- [ ] Section headings are product-specific — generic structure ("How it works" / "Features" / "Pricing" with zero product language) is a tell
- [ ] No unresolved `https://via.placeholder.com/` URLs or stock photo placeholder `src` values

### Component Tells

- [ ] Cards within a set are not all identical aspect ratio, padding, and border-radius with no visual variation
- [ ] Features section is not only `icon + title + one-sentence description` in a 3-column equal grid
- [ ] Testimonial section (if present) is not only `avatar + name + single sentence` in equal columns
- [ ] Pricing table (if present) differentiates plans visually beyond a single "Most Popular" badge

## How to Capture Evidence

For every "✗" item:

- Screenshot at the failing breakpoint
- Computed style excerpt (font-size, color pair, spacing) when relevant
- Token reference if the violation is "literal value used instead of token"
- File path + line for the responsible CSS / styled component
