# Mobile-First End-User UI Policy

## Rule

For new end-user UI layout or style work, author the base layout and styles for
the narrowest supported viewport first. Expand outward with `min-width`
breakpoints as the viewport gains space. Do not establish a desktop-first base
and use `max-width` overrides to claw back mobile behavior.

## Trigger

This policy applies when a new or redesigned end-user UI surface changes
layout or styling. It does not apply to non-UI work, admin or internal tools,
or UI tasks that do not change layout or styles.

## Escape hatch

An otherwise in-scope end-user surface may be PC/tablet-only when that product
constraint is explicit. Record the PC/tablet-only exception in the plan or
task; do not infer it from the current design or implementation.

## Backward compatibility

Do not retrofit unchanged legacy desktop-first UI or CSS solely to meet this
policy. Apply the rule to new layout/style work and explicit redesign scope;
preserve existing non-UI, admin/internal, and legacy behavior otherwise.
