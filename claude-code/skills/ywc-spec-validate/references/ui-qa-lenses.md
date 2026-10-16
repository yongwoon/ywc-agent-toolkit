# UI/Interaction QA Lenses

Canonical lens table for Step 3.6 (UI/Interaction Omission Check). Each lens is a
generic QA expectation — not a project-specific rule — that experienced QA
engineers apply by habit even when a spec never states it. A spec's trigger
surface decides which lenses apply; a spec with no UI surface triggers none of
them.

| Lens | Trigger surface | Rule |
|---|---|---|
| Round-trip fidelity | Spec includes an edit UI that reads an existing value into an editable field | The spec must state that read → edit → save → re-display preserves the value's user-visible meaning (line breaks, formatting) — not just its storage representation |
| Loading / empty / error states | Spec adds or changes any UI displaying async/server-sourced data | The spec must define all three: what renders while loading, what renders when the result set is empty, and what renders on fetch/submit failure |
| Optimistic UI vs. actual result | Spec applies a UI change immediately before server confirmation (optimistic update) | The spec must define the rollback/reconciliation behavior when the server call fails |
| Input validation feedback | Spec adds a form field with a validity constraint | The spec must define when the constraint is surfaced (on input vs. on submit) and which field the error message attaches to |
| Text-length extremes | Spec displays or accepts user-authored free text | The spec must define truncation/wrap behavior for very long text and behavior for empty/whitespace-only text |
| IME composition | Spec adds a text input reachable from a CJK-locale UI | The spec must define that uncommitted IME composition does not trigger form submission or validation before the IME commits the input, without requiring specific event handlers or an event model |
| Viewport / responsive | Spec is a UI change with no explicit "desktop-only" scope note | The spec must state the mobile-viewport behavior, or explicitly declare desktop-only as Out of Scope |
| Keyboard / focus accessibility | Spec adds an interactive UI control (button, modal, form) | The spec must state the control is operable via keyboard alone (tab order, Enter/Escape), or explicitly defer accessibility as Out of Scope |
| Stale-on-revisit data | Spec adds a UI that displays data mutated elsewhere in the same session | The spec must define whether re-opening/revisiting the view re-fetches, or state which mutation invalidates a cached value |
| Destructive-action reversibility | Spec adds a delete/reset/overwrite action | The spec must define a confirmation step or an undo path, or explicitly declare the action as non-reversible by design |

## Usage

For each row whose Trigger surface matches the spec under review, check whether
the spec's Acceptance Criteria, Functional Requirements, or Edge Cases satisfy
that row's Rule. A triggered row the spec does not address is a Completeness
Warning — cite the row's Lens name and the nearest relevant spec section (or
its absence) in the finding description. Do not force-fit a row whose trigger
surface the spec does not touch.

This table is a fixed set of general QA habits, not a per-project checklist —
do not append new rows for a case-specific bug found during one review. A
recurring case-specific defect belongs in `ywc-impl-review`'s recurring-defects
catalog instead, which is scoped to post-hoc code review, not pre-implementation
spec review.
