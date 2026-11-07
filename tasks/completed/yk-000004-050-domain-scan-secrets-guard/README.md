# yk-000004-050-domain-scan-secrets-guard

## Purpose
Make `scan-secrets.sh` fail loudly (exit 2) outside a git work tree or in a bare repo instead of silently passing, document that, and add a focused test registered in `scripts/validate.sh` (AC8).

Spec item: A8 (scan-secrets) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- FIRST measure the current behavior in a scratchpad temp directory (outside work tree, bare repo, unresolved path) and record it as the AC8 baseline.
- `scan-secrets.sh`: exit 2 outside a work tree / in a bare repo; update header comment (`:9-13`) and the `claude-code/skills/CLAUDE.md` Bundled Execution Scripts row to 'exit 2 = usage error or not a work tree'.
- `ywc-create-pr/SKILL.md`: add a sentence that any result other than exit 0/1 is `BLOCKED`.
- New `scripts/test-scan-secrets.sh`: abridged to three cases only (outside work tree, bare repo, unresolved path); built from the #341 `GIT_CEILING_DIRECTORIES` version. Create temp repos with inherited git env removed (`env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE`). Do not copy Phase 2b / symlink / binary / `--committed` cases and do not add `--committed <base>` validation.
- Register the test in `scripts/validate.sh` `check_cc_support_dirs` (`-f` check + `bash` run, next to the poll test loop). It must be shellcheck-clean; do NOT add it to `.github/workflows/validate.yml` `ignore_paths`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 8 (scan-secrets bullet), AC8, Critical Surfaces, Existing Constraints Touched 'scan-secrets exit code'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-create-pr/scripts` — upstream script + test (T0 snapshot; port only the named cases)

### Summary
A secret scanner that exits 0 when it could not scan is a silent pass. Exit 2 already means 'usage error', so its meaning is widened and documented in both places. The test is intentionally small and must not inherit git env vars from the pre-commit hook.

### Out of Scope (from spec)
- `--committed <base>` argument validation
- Snapshot test cases for features the local script lacks
- `validate.yml` shellcheck `ignore_paths` edits

## Criticality
critical — Spec Critical Surface: `scan-secrets.sh` is the secret scan; path also matches the `secret` keyword.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream scan-secrets files
- `yk-000004-040-domain-create-pr-features-api` — serializes edits to `ywc-create-pr/SKILL.md` (A5 → A8c → B2)

### Depended By
- `yk-000005-010-domain-skill-path-convention` — needs the output of this task

## Key Files
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` — exit 2 behavior + header comment
- `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh` — new, 3 cases
- `claude-code/skills/ywc-create-pr/SKILL.md` — BLOCKED sentence
- `claude-code/skills/CLAUDE.md` — Bundled Execution Scripts row
- `scripts/validate.sh` — register test in check_cc_support_dirs

## Notes
- Mode 755 for the new test script, matching snapshot.
- Staging `scripts/validate.sh` triggers `.githooks/pre-commit:16,39`, which runs `validate.sh` with git env vars set — hence the `env -u` requirement.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-create-pr/scripts/**`
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/CLAUDE.md`
- `scripts/validate.sh`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Bundled Execution Scripts table in `claude-code/skills/CLAUDE.md`
- `scripts/validate.sh` `check_cc_support_dirs`

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000004-040-domain-create-pr-features-api`

### Task Verify
- `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `d=$(mktemp -d) && (cd "$d" && bash "$OLDPWD/claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh" --staged; test $? -eq 2)`
- `[ "$(grep -c 'BLOCKED' claude-code/skills/ywc-create-pr/SKILL.md | tr -d ' ')" -ge 3 ]`
- `[ "$(grep -c 'test-scan-secrets' scripts/validate.sh | tr -d ' ')" -ge 1 ]`
- `[ "$(grep -c 'test-scan-secrets' .github/workflows/validate.yml | tr -d ' ')" = 0 ]`
- `shellcheck claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
