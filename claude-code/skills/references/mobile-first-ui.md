# Mobile-First UI Default

Frontend work in this repository defaults to a **mobile-first, responsive**
implementation order: build the base layout and styles for the narrowest
viewport first, then layer on tablet/desktop rules with `min-width` breakpoints.
This file is the single consumption contract shared by
`ywc-project-scaffold`, `ywc-task-generator`, `ywc-plan`, `ywc-sequential-executor`,
and `ywc-parallel-executor` — each consumer points here rather than restating
the rule inline, the same convention as
[`pr-bot-polling.md`](./pr-bot-polling.md).

## Rule

1. **Author the mobile (narrowest supported) viewport first.** Base CSS/styles
   carry no breakpoint qualifier.
2. **Expand outward with `min-width` breakpoints** (tablet, then desktop) —
   never `max-width` overrides that claw back mobile styles from a
   desktop-first base. `min-width` breakpoints only add rules; they never
   have to undo an earlier rule for a narrower viewport.
3. Apply this to new UI surfaces. Retrofitting an existing desktop-first
   surface to mobile-first is a separate, explicitly-scoped task — this rule
   does not by itself justify rewriting working CSS.

## Trigger

Fires when a task, plan section, or scaffold request both (a) touches
frontend/UI code (category `ui` in `ywc-task-generator`'s taxonomy, or an
`ywc-project-scaffold` request naming a UI framework) and (b) targets a
service consumed by end users on unknown/varied viewport sizes.

## Escape hatch

Does **not** fire — and the desktop/tablet-only layout is the correct
default — when the surface is explicitly PC/tablet-only by nature: an admin
dashboard, an internal operations tool, or any service the request
identifies as desktop-targeted. State the exception explicitly (one line)
rather than silently defaulting either way.

## Backward compatibility

A UI task, plan, or scaffold request that predates this rule, or whose
surface is out of scope per the escape hatch above, behaves exactly as
before this file existed — no retroactive obligation.
