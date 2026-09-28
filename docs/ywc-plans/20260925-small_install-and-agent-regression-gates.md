# Wire orphaned install/agent regression tests into validate.sh

## Goal

`develop-with-llm` PR #234 documents two incidents: (1) `install.sh` silently
failed to sync shared `references/`/`scripts/` dirs to the install
destination for 111 days because no test exercised an actual install, and
(2) read-only agents (no `Write` tool) stalled because nothing enforced an
inline-return qualifier in their Return Contract.

Both underlying bugs already do **not** exist in this repo:
- `scripts/install.sh:143-162` (`install_support_dir`, `install_cc_support_dirs`,
  `install_codex_support_dirs`) already copies `references/` and `scripts/`
  correctly for both CC and Codex.
- `scripts/validate.sh:905-927` (`check_agent_readonly_return_contract`) and
  `scripts/validate.sh:718-726` (inside `check_codex_agent_file`) already
  enforce the inline-return qualifier on every read-only agent, at the
  source-file level.

But investigation surfaced the actual regression risk this repo shares with
the incident: two test files that already prove the harder, installed-destination
version of these invariants exist on disk but are **never invoked** by
`scripts/validate.sh` or `.github/workflows/validate.yml` (which only calls
`bash scripts/validate.sh`) — so they can silently rot exactly like the
111-day-blind installer bug, just with the test already written and inert
instead of missing.

- `tests/install-codex-agents-test.sh` — installs Codex agents into a temp
  `CODEX_HOME` across 3 CLI-version branches and asserts the 8 read-only
  agents keep the inline qualifier plus correct `sandbox_mode`/`model` at
  the **installed** destination. Confirmed via
  `grep -rn "install-codex-agents-test" . --include="*.sh" --include="*.yml"`
  → zero hits outside the file itself.
- No equivalent exists for Claude Code's `install_support_dir`: nothing runs
  `scripts/install.sh --cc`/`--codex` against a temp destination and checks
  that `references/`/`scripts/` actually land there and that installed
  `SKILL.md` reference links resolve relative to the installed location
  (today's `check_cc_support_dirs`/`check_codex_support_dirs` in
  `scripts/validate.sh:227-257,833-882` only check the source tree).

This plan closes both gaps with the minimum wiring, mirroring PR #234's
"add a mechanical, installed-destination smoke test" fix.

## Why

Prevent the same incident class (a real fix landing, but with no gate to
catch a future regression) from recurring here, matching the two guardrails
`develop-with-llm` PR #234 added after its postmortems.

## Out of Scope

- Re-implementing or modifying the already-correct `install_support_dir`
  logic in `scripts/install.sh`.
- Re-implementing the already-correct `check_agent_readonly_return_contract`
  / Codex `readonly_qualifier` checks in `scripts/validate.sh` — those stay
  as-is; this plan only adds destination-level coverage that doesn't exist yet.
- `tests/architecture_invariants_test.py`, which is also never invoked by
  `scripts/validate.sh` — same orphaned-test pattern, but it tests
  `codex/skills/scripts/architecture-invariants.py`, an unrelated helper.
  Left for a separate follow-up so this plan stays scoped to the two PR #234
  incidents.
- Adding new incident-postmortem documentation files (`docs/bug-reports/`)
  — this repo has no equivalent directory/convention today; not introducing
  one speculatively.

## Done When

- `bash scripts/validate.sh` runs `tests/install-codex-agents-test.sh` and
  fails the whole script if that suite fails.
- A new smoke test runs `scripts/install.sh --cc` and `--codex` against
  temporary `CLAUDE_SKILLS_DIR`/`CODEX_HOME` destinations, asserts
  `references/` and `scripts/` exist under each, and asserts at least one
  installed file's `../references/...`-style link resolves relative to the
  installed location (not just the source tree) — and this new test is also
  invoked from `scripts/validate.sh`.
- `bash scripts/validate.sh` still exits 0 on the current branch state (no
  regressions from wiring these in).

## Files to Touch

- `scripts/validate.sh` — add invocation of `tests/install-codex-agents-test.sh`
  (pattern-match the existing `scripts/test-wave-int-checkpoint-ownership.sh`
  block at `scripts/validate.sh:1004-1007`); add invocation of the new
  smoke test below in the same style.
- `tests/install-shared-assets-test.sh` (new) — the CC-side installed-destination
  smoke test for shared `references/`/`scripts/` sync.

## Implementation Steps

- [x] In `scripts/validate.sh`, near the existing wave-int test blocks
      (`scripts/validate.sh:1004-1012`), add:
      ```bash
      if [ -f tests/install-codex-agents-test.sh ]; then
        echo "==> Running Codex installed-agent regression suite..."
        bash tests/install-codex-agents-test.sh || ERRORS=$((ERRORS + 1))
      fi
      ```
- [x] Create `tests/install-shared-assets-test.sh` (executable, `set -euo pipefail`,
      `mktemp -d` + `trap ... EXIT` cleanup — mirror
      `tests/install-codex-agents-test.sh`'s structure):
  - Run `CLAUDE_SKILLS_DIR="$tmp/cc" bash scripts/install.sh --cc >/dev/null`
    (no skill args = full install, matching `install_cc_support_dirs` at
    `scripts/install.sh:154-157`); assert `$tmp/cc/references` and
    `$tmp/cc/scripts` exist and are non-empty directories.
  - Pick one installed skill file that contains a `../references/*.md`-style
    link (grep the installed tree the same way
    `check_cc_support_dirs` does at `scripts/validate.sh:870-881`, but rooted
    at `$tmp/cc` instead of `claude-code/skills`) and assert the link resolves
    to an existing file relative to the installed skill's own directory —
    this is the exact check that would have caught PR #234's installer bug,
    now run against install.sh's real output instead of the source tree.
  - Run `CODEX_HOME="$tmp/codex" bash scripts/install.sh --codex >/dev/null`;
    assert `$tmp/codex/skills/references` and `$tmp/codex/skills/scripts`
    exist (per `install_codex_support_dirs` at `scripts/install.sh:159-162`
    and `CODEX_DEST` skills subpath — confirm exact `CODEX_DEST` path from
    `scripts/install.sh` during implementation, e.g. `$CODEX_HOME/skills`).
  - `chmod +x tests/install-shared-assets-test.sh`.
- [x] Add the new test's invocation to `scripts/validate.sh` right after the
      `install-codex-agents-test.sh` block, same `if [ -f ... ]` guard style.
- [x] Run `bash scripts/validate.sh` locally end-to-end and confirm it still
      exits 0.

## Interfaces

N/A — no shared function/type signature is introduced or changed across
files; both touched files communicate only through shell exit codes, the
existing convention `scripts/validate.sh` already uses for every other
`tests/*.sh`/`scripts/test-*.sh` suite.

## Verification Commands

- `bash scripts/validate.sh` (runs the full local CI mirror, including the
  two newly-wired suites)
- `bash tests/install-codex-agents-test.sh` (standalone, to confirm it still
  passes in isolation before wiring)
- `bash tests/install-shared-assets-test.sh` (standalone, once written)
- `shellcheck scripts/validate.sh tests/install-shared-assets-test.sh`
  (matches the `ShellCheck (scripts/)` CI step in `.github/workflows/validate.yml:24-27`
  — note `tests/` is not currently in any shellcheck `scandir`; run shellcheck
  manually here since CI won't catch it, or confirm during implementation
  whether `tests/` should be added to a scandir as a small follow-on)

## Risks / Rollback

- **Risk**: `tests/install-codex-agents-test.sh` currently passes in isolation
  but could interact badly with other `validate.sh` state (e.g. `PATH`
  mutation inside the test's subshell affecting later checks). Mitigation:
  the test already scopes `PATH`/`CODEX_HOME` overrides to each
  `install_with_version` call's own command, not global exports — verify
  this holds when run as part of the full `validate.sh` sequence, not just
  standalone.
- **Risk**: the new smoke test's link-resolution assertion could be brittle
  if a specific skill's reference link path is hardcoded. Mitigation: pick
  the target file via a live grep at test-run time (as specified above),
  not a hardcoded filename, so it doesn't need updating when skills change.
- **Rollback**: both changes are additive (`if [ -f ... ]` guarded and a new
  file); reverting the `scripts/validate.sh` diff and deleting the new test
  file fully rolls back with no side effects on `install.sh` or any shipped
  skill/agent content.
