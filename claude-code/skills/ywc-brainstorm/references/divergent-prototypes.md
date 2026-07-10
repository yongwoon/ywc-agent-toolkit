# Divergent Visual Prototypes

For design-heavy brainstorming, prose approaches cannot surface the user's
visual taste. Taste is an "Unknown Known" — a preference so obvious to the user
that they never write it into a spec, but which they recognize instantly when
they see it. The only reliable way to elicit it is to put 2–4 concrete,
*deliberately different* mockups in front of them and watch which one they reach
for.

## When to generate prototypes

Generate divergent mockups when the request's value is in the **look and feel**:

- A new user-facing screen or page with no established visual precedent
- A visual redesign / restyle of an existing surface
- A landing page, marketing page, or hero section
- A component whose whole point is its appearance (data-viz, empty state, pricing table)

Do **not** generate them when the design question is behavioral or structural
(API shape, data model, routing, state management) — prose approaches (Step 4)
already fit those. When in doubt, ask the user whether they care more about
*how it looks* or *how it works* this round.

## How many, and how divergent

- **Count:** 2–4. Two is the floor (one is not a comparison); four is the ceiling
  (more dilutes the reaction and burns tokens).
- **Divergence is the whole point.** The variants must differ on a *structural*
  design axis, not on trivia. A color swap of the same layout is one prototype
  shown twice. Pull each variant from a genuinely different direction, e.g.:
  editorial / magazine, Swiss / minimal grid, bento / card-dense,
  dark-luxury, neo-brutalist, glassmorphism-with-depth. Name the direction at
  the top of each file so the reaction is about a *style*, not a pixel.
- Each variant commits fully to its direction. A timid middle-ground variant
  teaches nothing — the user reacts to conviction, not to a hedge.

## Self-contained single-file rule

Each mockup is one standalone `.html` file with **all** CSS (and any JS) inline —
no external stylesheets, CDN scripts, or remote fonts/images. Embed imagery as
inline SVG or a solid/gradient placeholder. This mirrors the bundle's HTML
convention; read [../../references/html-output.md](../../references/html-output.md)
for the single-file rules, responsive discipline, and theme handling, and apply
the same skeleton here.

Realistic placeholder content only — never lorem ipsum where a real label is
known. The user judges a believable screen, not a wireframe.

## Where they live (disposable)

Write every mockup under the brainstorm scratch directory:

```text
docs/ywc-plans/_brainstorm-<slug>/prototypes/
  variant-a-editorial.html
  variant-b-swiss-grid.html
  variant-c-bento.html
```

These are **throwaway exploration artifacts**, exempt from the skill's Hard Gate
(they are not production code). They are never carried into implementation and
never committed as deliverables — the chosen *direction* feeds the Step 5 design;
the files themselves are discarded (or left in the scratch dir, which is not a
production path). Do not write mockups into `src/`, `app/`, `components/`, or any
real source tree.

## Running the reaction

Present the variants together, each with its one-line style label. Ask the user
which direction resonates and — more valuable — *why*, and what they would pull
from a runner-up. The "why" is the taste you could not have written down; capture
it verbatim into the Step 5 design's "What we're building" and "Failure modes"
sections. It is common for the user to pick a hybrid ("A's layout with C's
density"); record that composition as the chosen direction.

The mockups are the map, not the territory — their job is done the moment the
direction is chosen. Do not polish them further; move to Step 5.
