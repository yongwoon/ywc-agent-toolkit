# yw-000043-010-infra-port-gate-ledger-script

## Purpose
Port the upstream `develop-with-llm` Executable Gate Ledger implementation (`gate-check.py`, its self-check `test_gate_check.py`, and the format spec `references/gate-ledger.md`) into `claude-code/skills/ywc-verify-done/`, and register the new script in this repo's shared Bundled Execution Scripts table. This gives `ywc-verify-done` a machine-checked escalation path for high-stakes completion claims, reusing an already-designed, already-security-hardened implementation rather than a fresh design.

## Scope
- Add `claude-code/skills/ywc-verify-done/scripts/gate-check.py` — verbatim port of upstream's final (post-security-fix) implementation, with only the embedded repo-relative path examples adjusted from `tools/claude-code/skills/...` to `claude-code/skills/...`, and the docstring's dangling design-doc reference replaced or dropped (see FR-1).
- Add `claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` — verbatim port of upstream's 24-case stdlib-only self-check, with the same path-string adjustment where it invokes `gate-check.py` by path.
- Add `claude-code/skills/ywc-verify-done/references/gate-ledger.md` — the ledger format spec, with the same path adjustment plus a rewritten opening sentence (upstream's dangling `external-repositories/unlazy/references/gates.md` reference does not exist in this repo — see FR-4).
- Add one row for `gate-check.py` to `claude-code/skills/CLAUDE.md`'s existing `## Bundled Execution Scripts` table.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-verify-done-gate-ledger-port.md` — FR-1, FR-4, FR-5, AC1–AC7, Critical Surfaces, Edge Cases (this task covers all script/reference-file content and the CLAUDE.md registration)
- Upstream source files (read directly for this port, available in the sibling checkout `/Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm`):
  - `tools/claude-code/skills/ywc-verify-done/scripts/gate-check.py`
  - `tools/claude-code/skills/ywc-verify-done/scripts/test_gate_check.py`
  - `tools/claude-code/skills/ywc-verify-done/references/gate-ledger.md`
- Upstream PR: [`yongwoon/develop-with-llm#228`](https://github.com/yongwoon/develop-with-llm/pull/228) (merged, includes one post-merge security-fix round)

### Summary
This task ports three files verbatim (with only path-string and one dangling-reference edit permitted — no behavioral line changes) and registers the new script in the shared CLAUDE.md table. The two security-relevant properties already fixed upstream — `stop_process_group()` unconditionally sending `SIGKILL` to the whole process group after the grace period, and `matches_expect()` bounding every regex match inside a 5-second-capped `multiprocessing.Process` — must survive the port unmodified. The ported self-check (`test_gate_check.py`) is this feature's only automated verification; there is no other project test runner it plugs into.

### Out of Scope (from spec)
- SKILL.md `## Optional Escalation` section, Common Mistakes bullets, References table row, README.md Korean summary — handled by `yw-000043-020-docs-document-gate-ledger-escalation`
- `codex/skills/ywc-verify-done/` and `plugins/ywc-agent-toolkit/skills/ywc-verify-done/` — explicitly out of scope for the whole spec (Codex/plugins port is a deliberate follow-up decision for the user)
- Any change to the existing 5-step prose Gate Function, Forbidden Vocabulary table, Rationalization Defense table, or Claim Classification table

## Criticality
`normal` — this task ports an already-hardened implementation with no new design decision; the security-sensitive surface (`CHECK:` executing arbitrary shell) is inherited unchanged from upstream's own reviewed-and-fixed version, not introduced by this task. Flagged in Notes below for visibility since the keyword heuristic (no explicit spec Critical Surfaces override for this repo) would otherwise warrant a second look.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000043-020-docs-document-gate-ledger-escalation` — needs `references/gate-ledger.md` to exist (for its new References table row and the SKILL.md section's pointer) and the script's confirmed CLI invocation modes to document accurately in SKILL.md/README.md

## Key Files
- `claude-code/skills/ywc-verify-done/scripts/gate-check.py` — new file, ported CLI script
- `claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` — new file, ported self-check (24 cases)
- `claude-code/skills/ywc-verify-done/references/gate-ledger.md` — new file, ledger format spec
- `claude-code/skills/CLAUDE.md` — one new row in `## Bundled Execution Scripts` (lines ~325-352)

## Notes
- **Verbatim-port discipline**: do not "clean up" or refactor any ported logic. The only permitted text edits are described in FR-1 (path strings, docstring reference) and FR-4 (path strings, opening-sentence rewrite). If a diff against the upstream file shows anything beyond those, revert it.
- Upstream's own review caught and fixed a path-prefix mistake in its equivalent CLAUDE.md table row (commit `454d1f1`, "fix: correct CLAUDE.md gate-check.py path to include tools/claude-code/skills prefix") — this repo's row must use `claude-code/skills/ywc-verify-done/scripts/gate-check.py` (no `tools/` prefix), not repeat that mistake.
- `references/gate-ledger.md`'s opening sentence in upstream references `external-repositories/unlazy/references/gates.md`, which does not exist in this repository. Per FR-4, drop the "narrowed subset of X" framing entirely rather than porting a dead link — write a self-contained opening sentence instead.
- The module docstring in `gate-check.py` references upstream's own design doc (`docs/ywc-plans/20260824-verify-done-gate-ledger.md`), which is not reproduced in this repo. Per FR-1, replace the pointer with this repo's own spec path (`docs/ywc-plans/20260917-verify-done-gate-ledger-port.md`) or drop the sentence if it reads awkwardly standalone.
- `.githooks/pre-commit` guard for `plugins/ywc-agent-toolkit/skills/` is a no-op for this task's diff (zero files under `plugins/` or `codex/` are touched).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-verify-done/scripts/gate-check.py`
- `claude-code/skills/ywc-verify-done/scripts/test_gate_check.py`
- `claude-code/skills/ywc-verify-done/references/gate-ledger.md`
- `claude-code/skills/CLAUDE.md` (limited to the `## Bundled Execution Scripts` table only — do not edit any other section of this shared file)

### Owned Interface
- CLI surface: `gate-check.py <ledger.md> [--status | --reverify]` — three invocation modes (default, `--status`, `--reverify`); exit 0 = all runnable gates met / well-formed on `--status`, exit 1 = at least one unmet or malformed ledger. Downstream task `yw-000043-020` documents this signature in prose without re-reading the implementation.

### Shared Surfaces
- `claude-code/skills/CLAUDE.md` — shared table edited by many unrelated tasks across this repo's history; only append one row, do not reformat or reorder existing rows.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` (must end in `ALL PASS`, exit 0 — AC1)
- `grep -n "gate-check.py" claude-code/skills/CLAUDE.md` (exactly one match — AC7)
- `test -f claude-code/skills/ywc-verify-done/scripts/gate-check.py && echo OK` (AC7's path-resolution check)

## Out of Scope
- Any behavioral change to the ported script's parsing, timeout, signal-handling, regex-bounding, or fingerprinting logic
- Windows-specific re-verification of the POSIX/non-POSIX fallback path (upstream did not claim Windows CI coverage either — ported unchanged, not independently re-verified here)
- Any edit to `claude-code/skills/ywc-verify-done/SKILL.md` or `README.md` (handled by `yw-000043-020`)
