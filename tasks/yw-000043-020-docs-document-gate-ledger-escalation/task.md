# yw-000043-020-docs-document-gate-ledger-escalation — Implementation Checklist

## Prerequisites
- [ ] `yw-000043-010-infra-port-gate-ledger-script` is completed (merged) — `references/gate-ledger.md` exists and `gate-check.py`'s CLI path/invocation modes are confirmed

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`: `claude-code/skills/ywc-verify-done/SKILL.md`, `claude-code/skills/ywc-verify-done/README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `yw-000043-010` is not actually merged (i.e., `claude-code/skills/ywc-verify-done/references/gate-ledger.md` does not exist yet)
- [ ] Stop if the current `SKILL.md`'s Step 1–6 shape has diverged from the structure described in the spec's "Existing Constraints Touched" table (re-read the file first; do not assume line numbers are still accurate)
- [ ] Stop if `ywc-skill-author` flags a structural concern with the proposed section placement — do not override its guidance and hand-edit anyway

## Implementation Steps

- [ ] **Invoke `ywc-skill-author` (FR-7)**
  - [ ] Before editing `SKILL.md`, invoke the `ywc-skill-author` skill per `claude-code/skills/CLAUDE.md`'s "Authoring or Restructuring `ywc-*` Skills" rule, since this edit adds a new body section (`## Optional Escalation`) and a new `references/` file reference — not an ad-hoc minor edit
  - [ ] Provide it the upstream section content (path-adjusted) and the confirmed insertion point (after Step 6, before `## Integration`)

- [ ] **Add `## Optional Escalation: Executable Gate Ledger` to SKILL.md**
  - [ ] Insert the new section between the end of `### Step 6: On failure, classify and route` and `## Integration`
  - [ ] Preserve upstream's explicit framing: this is optional; Steps 1–6 remain the unchanged default path
  - [ ] Name the three invocation modes with this repo's path: `claude-code/skills/ywc-verify-done/scripts/gate-check.py <ledger> [--status|--reverify]`
  - [ ] Repeat the security warning that `CHECK:` executes arbitrary shell commands, with a pointer to `references/gate-ledger.md` for the full format spec

- [ ] **Append Common Mistakes bullets (FR-3)**
  - [ ] Append, verbatim, after the existing fifth bullet in `## Common Mistakes`: "Trusting an absence check without a positive control."
  - [ ] Append, verbatim: "Copying a supplied number into the claim instead of recomputing it."

- [ ] **Add References table row (FR-4 registration)**
  - [ ] In `## References`, add one row for `references/gate-ledger.md`, positioned as the second row (after `verification-block-examples.md`, before the two `../references/` shared-file rows)

- [ ] **Add Korean README section (FR-6)**
  - [ ] Insert `## Optional: Executable Gate Ledger` into `claude-code/skills/ywc-verify-done/README.md`, positioned after `## 무엇을 하나요` and before `## 언제 trigger 되나요`
  - [ ] Write in Korean prose with English technical terms preserved (no transliteration), matching the voice/format of the existing sections
  - [ ] Cover: what it's for, the three-mode invocation syntax pointer (with this repo's path), and the shell-execution security warning

## Task Verify
- [ ] `bash scripts/validate.sh` — no new errors for `ywc-verify-done`
- [ ] `grep -n "gate-ledger.md" claude-code/skills/ywc-verify-done/SKILL.md` — new References row present
- [ ] `grep -n "Optional Escalation" claude-code/skills/ywc-verify-done/SKILL.md` — new section present
- [ ] `grep -n "Optional: Executable Gate Ledger" claude-code/skills/ywc-verify-done/README.md` — new Korean section present

## Verification
- [ ] SKILL.md structural validation passes: `bash scripts/validate.sh` → `Skill is valid!` (or equivalent zero-`ERROR` output) covering `ywc-verify-done` (AC8)
- [ ] Manual read-through: `## Optional Escalation` section sits between Step 6 and `## Integration`, names all three CLI modes with the correct path, and repeats the shell-execution warning
- [ ] Manual read-through: Common Mistakes has exactly two new bullets appended, verbatim, after the existing fifth bullet
- [ ] Manual read-through: References table has exactly one new row for `gate-ledger.md` in the correct position
- [ ] Manual read-through: README.md's new Korean section reads consistently with the existing sections' voice and covers all three required points (purpose, invocation pointer, security warning)

## Implementation Notes (optional)

<!-- Starts empty at generation time. Add bullets here in real time as
     unanticipated issues surface during implementation. -->
