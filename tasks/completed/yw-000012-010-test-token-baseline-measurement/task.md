# yw-000012-010-test-token-baseline-measurement — Implementation Checklist

## Prerequisites

Verify these before starting:

- [ ] `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` status is `DONE` per its
      `spec-ready-log.md` (Iteration 2, gate 92)

## Allowed Edit Scope

- [ ] This task edits no source files — its only write is to this file's Implementation Notes
      section below
- [ ] If a measurement command fails and requires a source-level workaround, stop and report
      rather than editing anything outside this file

## Stop Conditions

- [ ] Stop if `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
      errors out (do not attempt to fix the eval tool itself in this task)
- [ ] Stop if any of the 12 target `SKILL.md` files does not exist at the expected path

## Implementation Steps

- [ ] Run `wc -c` on `SKILL.md` for each of the 12 skills listed in README.md Notes; record
      each byte count
- [ ] For `ywc-sequential-executor`, trace its default (no `--non-interactive`,
      no `--aggregate-pr`, no external-URL branch) execution path and list which
      `**Action required**` directives it actually reads on that path (cross-reference the
      grep list already captured for this spec: `SKILL.md:78` non-interactive-mode.md is
      gated and NOT read by default; determine whether `SKILL.md:126`
      external-url-policy.md and `SKILL.md:203` non-stop-execution.md are read on the default
      path); sum `wc -c` for body + the references actually read by default
- [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
      and extract the per-skill score for each of the 12 modified skills
- [ ] Record all three sets of numbers (per-skill SKILL.md size, `ywc-sequential-executor`
      default-path composite size, per-skill mechanical score) in the Implementation Notes
      section below, labeled clearly as the "before" baseline

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` exits 0 and produces scores for all 12 skills
- [ ] `wc -c` succeeds for all 12 `SKILL.md` files

## Verification

- [ ] `bash scripts/validate.sh` still exits 0 (no source changed, this is a regression check only)

## Implementation Notes

Recorded 2026-09-01. Prerequisite verified: `docs/ywc-plans/20260901-claude-skill-token-efficiency.spec-ready-log.md`
line 24 shows `DONE — gate 92 (PROCEED)`. All 12 target `SKILL.md` files exist.
`python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
exited 0 (a `[coverage] 1 items below minimum ...` notice printed to stderr only, not an error —
JSON on stdout was well-formed).

### 1. `wc -c` per-skill `SKILL.md` — "before" baseline

| Skill | Bytes |
|---|---|
| ywc-auth-implement | 14306 |
| ywc-commit | 14127 |
| ywc-create-pr | 33060 |
| ywc-setup-language | 5891 |
| ywc-spec-writer | 26455 |
| ywc-task-generator | 39405 |
| ywc-docker-isolate | 7582 |
| ywc-handle-pr-reviews | 20867 |
| ywc-finish-branch | 30725 |
| ywc-merge-dependabot | 15487 |
| ywc-parallel-executor | 58374 |
| ywc-sequential-executor | 66361 |
| **Total** | **332640** |

### 2. `ywc-sequential-executor` default (no-flag) execution path — reference composite

All four `**Action required**` / `**Required for**` directives in the file, by line number:

| Line | Directive | Gate | Read on default (no-flag, single-task) path? |
|---|---|---|---|
| `SKILL.md:78` | Read `references/non-interactive-mode.md` | "when `--non-interactive` is set" | No |
| `SKILL.md:126` | Read `references/external-url-policy.md` | "Read it at Pre-flight" (Pre-flight step 5 runs this check unconditionally, once per project, regardless of mode) | **Yes** |
| `SKILL.md:152` | (points to `../references/local-merge-permissions.md`) | "**Required for range execution**" | No |
| `SKILL.md:203` | Read `../references/non-stop-execution.md` | "**Action required before any range task begins**" | No |

Only `references/external-url-policy.md` is read unconditionally on the default path (Pre-flight
step 5 requires determining the External URL Policy before Step 1 of the first task, independent
of any flag). The other three are explicitly flag-gated (`--non-interactive`) or range-mode-gated
("range execution" / "any range task begins") — a single default-mode invocation with no
specifier range never reaches those gates.

Default-path composite (body + the one default-read reference):

| Component | Bytes |
|---|---|
| `claude-code/skills/ywc-sequential-executor/SKILL.md` (body) | 66361 |
| `claude-code/skills/ywc-sequential-executor/references/external-url-policy.md` | 6316 |
| **Composite total** | **72677** |

Cross-check: 66361 bytes / 4 ≈ 16590 tokens, matching the spec Purpose section's stated "16,590
tokens of body" exactly. The spec's stated "~6,600 tokens of eagerly-read references" figure does
not match the literal default-path reference set traced above (6316 bytes ≈ 1579 tokens for
`external-url-policy.md` alone). For context, the byte sizes of the three gated references are:
`references/non-interactive-mode.md` = 3116, `references/local-merge-permissions.md`
(shared, `../references/`) = 2282, `../references/non-stop-execution.md` (shared) = 5504 — summing
all four referenced files (default + all three gated) gives 17218 bytes ≈ 4305 tokens, still short
of ~6600. This gap is a spec/reality divergence worth flagging to the orchestrator, not something
this read-only task resolves.

### 3. Mechanical score (`ywc-toolkit-eval score.py`, S2/S4/S5 axes) — "before" baseline

S1, S3, S6 are judgment axes and print `null` for every skill (mechanical tier does not score
them). All 12 target skills currently score identically on the mechanical axes:

| Skill | S2 (structure) | S4 (token economy) | S5 (integrity) | body_lines |
|---|---|---|---|---|
| ywc-auth-implement | 5 | 5 | 5 | 175 |
| ywc-commit | 5 | 5 | 5 | 253 |
| ywc-create-pr | 5 | 5 | 5 | 389 |
| ywc-setup-language | 5 | 5 | 5 | 78 |
| ywc-spec-writer | 5 | 5 | 5 | 289 |
| ywc-task-generator | 5 | 5 | 5 | 448 |
| ywc-docker-isolate | 5 | 5 | 5 | 94 |
| ywc-handle-pr-reviews | 5 | 5 | 5 | 250 |
| ywc-finish-branch | 5 | 5 | 5 | 328 |
| ywc-merge-dependabot | 5 | 5 | 5 | 285 |
| ywc-parallel-executor | 5 | 5 | 5 | 480 |
| ywc-sequential-executor | 5 | 5 | 5 | 499 |

Note: `ywc-setup-language` is the only one of the 12 with `coverage.sufficient: false`
(`positives: 3, collisions: 0` — below the FR1b minimum of 2 collisions); this is a coverage-gate
signal, not a mechanical-axis score, and does not change its S2/S4/S5 values above.

### Concerns for orchestrator

- The `~6,600 tokens of eagerly-read references` figure in the spec's Purpose section does not
  reconcile with the literal flag-gated reading procedure documented in `ywc-sequential-executor`'s
  own `SKILL.md` (see composite discussion above). `yw-000014-020` (the after-measurement task)
  should re-derive its "before" comparison point from this note's byte-level composite (72677
  bytes / ~16590+1579 tokens), not from the spec's approximate prose figure, or explicitly
  reconcile the discrepancy before comparing.
- `bash scripts/validate.sh` (this task's Verification step) exits 1 on this branch, but the
  failure is unrelated to this task: `[ci] MECHANICAL REGRESSION DETECTED: codex/skills/ywc-skill-author
  S5: 4 -> 2`. This task made zero source edits (`git status --short` shows only this `task.md`
  file changed), and `ywc-skill-author` is not one of the 12 target skills. The regression is a
  pre-existing condition on this branch/base, not something introduced here — flagging for the
  orchestrator rather than fixing it (out of this task's edit scope).
