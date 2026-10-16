# Conditional UI omission lenses

Apply a row only when its trigger appears in the reviewed requirements or
verified project context. Identify the source requirement and missing observable
postcondition; do not prescribe an unrelated feature. Record `N/A` and a reason
for untriggered rows. Missing applicable behavior is a finding, not an excuse to
invent implementation details. Inspect recorded evidence; do not run spec commands.

| Lens | Trigger | Observable requirements / verification to check |
|---|---|---|
| round-trip fidelity | User edits, saves, reloads or exports values | Accepted values survive edit -> save -> reload/export without unintended normalization or loss; invalid input has a defined response. |
| loading / empty / error | Async data or operations, collections | Loading, no results and failed operations are distinguishable; retry and retained input are defined where needed. |
| optimistic updates | UI changes before server confirmation | Success reconciliation, rollback on rejection and duplicate/reordered responses have observable outcomes. |
| IME composition | Editable text with IME input | Composition is not submitted, normalized or truncated prematurely; Enter behavior distinguishes composition from commit. |
| keyboard accessibility | Interactive controls, dialogs or navigation | Keyboard operation, visible focus, focus order/return, and accessible names/states are specified for the affected controls. |

Report applicability with trigger evidence, missing behavior, and a verification
location or explicit evidence gap. A document with no UI surface needs no UI
requirements. These are review questions, not authorization to build new UI.
