# Combined Heuristic Reference

Use during Phase 4 of `ywc-ui-ux-review` to attach an authoritative citation to every finding. Every issue in the final report must reference at least one item below.

## Table of Contents

1. Nielsen — 10 Usability Heuristics
2. WCAG 2.2 AA — Priority Success Criteria
3. Material Design 3 — Key Principles
4. Apple HIG — Key Principles
5. Internal Design System — How to Apply
6. Citation Order

## 1. Nielsen — 10 Usability Heuristics

| # | Heuristic | Cite as |
|---|---|---|
| 1 | Visibility of system status | Nielsen #1 |
| 2 | Match between system and real world | Nielsen #2 |
| 3 | User control and freedom | Nielsen #3 |
| 4 | Consistency and standards | Nielsen #4 |
| 5 | Error prevention | Nielsen #5 |
| 6 | Recognition rather than recall | Nielsen #6 |
| 7 | Flexibility and efficiency of use | Nielsen #7 |
| 8 | Aesthetic and minimalist design | Nielsen #8 |
| 9 | Help users recognize, diagnose, and recover from errors | Nielsen #9 |
| 10 | Help and documentation | Nielsen #10 |

**IA mapping**: #2, #4, #6 most often.
**Visual mapping**: #4, #8 most often.

## 2. WCAG 2.2 AA — Priority Success Criteria

Cite WCAG findings as `WCAG SC X.X.X` followed by the criterion name.

### Perceivable

- **SC 1.1.1** Non-text Content (alt text)
- **SC 1.3.1** Info and Relationships (semantic structure)
- **SC 1.3.5** Identify Input Purpose (autocomplete)
- **SC 1.4.1** Use of Color (color is not the sole carrier)
- **SC 1.4.3** Contrast (Minimum) — 4.5:1 body, 3:1 large text
- **SC 1.4.10** Reflow (no horizontal scroll at 320 CSS px)
- **SC 1.4.11** Non-text Contrast — 3:1 for UI / graphical objects
- **SC 1.4.12** Text Spacing — must remain readable when user overrides spacing

### Operable

- **SC 2.1.1** Keyboard — all functionality available via keyboard
- **SC 2.4.3** Focus Order — logical tab order
- **SC 2.4.7** Focus Visible
- **SC 2.4.11** Focus Not Obscured (Minimum) — new in 2.2
- **SC 2.5.7** Dragging Movements — new in 2.2
- **SC 2.5.8** Target Size (Minimum) — 24×24 (new in 2.2 AA)

### Understandable

- **SC 3.2.3** Consistent Navigation
- **SC 3.2.4** Consistent Identification
- **SC 3.3.1** Error Identification
- **SC 3.3.3** Error Suggestion
- **SC 3.3.7** Redundant Entry — new in 2.2
- **SC 3.3.8** Accessible Authentication (Minimum) — new in 2.2

### Robust

- **SC 4.1.2** Name, Role, Value — accessible name for every interactive element

## 3. Material Design 3 — Key Principles

Cite as `Material 3 — {topic}`.

- **Color roles** (primary / secondary / tertiary / surface / on-surface) — semantic, not literal
- **Type scale** (display / headline / title / body / label) — defined sizes per role
- **Elevation** signals importance and grouping; should be consistent
- **State layers** for hover / focus / pressed / dragged
- **Motion** uses defined `easing` and `duration` tokens

When the project uses Material, deviations are findings.

## 4. Apple HIG — Key Principles

Cite as `Apple HIG — {section}`.

- **Hierarchy**: organize content from most to least important
- **Harmony**: consistent typography, color, spacing across the app
- **Consistency**: standard controls behave the standard way
- **Direct manipulation**: gestures match expectations
- **Feedback**: every action acknowledged within ~100ms

When the project targets iOS / iPadOS / macOS, HIG deviations are findings.

## 5. Internal Design System — How to Apply

If the project ships a design system (tokens / components / guidelines):

1. **Locate** tokens during Phase 2 (`tokens.css`, `theme.ts`, `tailwind.config.*`, `*.tokens.json`, `design-system/`).
2. **Treat tokens as the highest-precedence reference** — internal tokens override generic guidelines.
3. Cite as `Design System — {token-name}` (e.g., `Design System — color.surface.subtle`).
4. Findings include: literal values used instead of tokens; missing tokens forcing duplication; drift between component and token.

If no internal design system exists, that itself can become a Medium-or-higher finding ("no shared token system → inconsistent execution").

## 6. Citation Order

Every finding has a `Heuristic` field. When multiple frameworks apply, cite in this priority order:

1. Internal Design System (highest precedence — project-specific)
2. WCAG 2.2 AA (legal / accessibility precedence)
3. Nielsen 10 (user-experience precedence)
4. Platform (Material 3 / Apple HIG) (platform-conformance precedence)

A single finding may carry multiple citations when multiple frameworks reinforce the same conclusion.
