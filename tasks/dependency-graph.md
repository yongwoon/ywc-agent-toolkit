**Next PHASE (yk): `000008`** — authoritative starting point for the next `yk`-initials `ywc-task-generator` batch. Read this line first; do not re-derive by scanning when it is present. After allocating a new batch, update this line to `highest allocated PHASE + 1`.
**Next PHASE (yw): `000005`** — authoritative starting point for the next `yw`-initials `ywc-task-generator` batch. Read this line first; do not re-derive by scanning when it is present. After allocating a new batch, update this line to `highest allocated PHASE + 1`.

# Codex Issue 69 — task dependency graph

Source: `docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md`. Mode: llm; language: en; initials: yk.

## Phase yk-000001 — done
- Completed: `yk-000001-010-domain-model-hints`, `yk-000001-020-domain-analyst-modes`, `yk-000001-030-domain-authoring-feedback`, `yk-000001-040-domain-session-retro`, `yk-000001-050-domain-session-handoff`, `yk-000001-060-domain-review-defects`, `yk-000001-070-domain-operational-safety`, `yk-000001-080-domain-mission-anchor`, `yk-000001-090-domain-infra-evidence`, `yk-000001-100-domain-pr-worktrees`, `yk-000001-110-domain-convergence-callers`, `yk-000001-120-domain-pr-body`

## Phase yk-000002 — done
- Completed: `yk-000002-010-infra-distribution`

## Phase yk-000003 — done
- Completed: `yk-000003-010-config-upstream-snapshot`

## Phase yk-000004 — done
- Completed: `yk-000004-010-domain-plan-auto-converge`, `yk-000004-020-domain-finish-branch-remote-guard`, `yk-000004-030-domain-executor-local-exclude`, `yk-000004-040-domain-create-pr-features-api`, `yk-000004-050-domain-scan-secrets-guard`, `yk-000004-060-domain-skill-contradiction-fixes`, `yk-000004-070-domain-impl-review-linter-defects`, `yk-000004-080-domain-debug-feedback-loop`, `yk-000004-090-domain-brainstorm-tdd-rules`

## Phase yk-000005 — done
- Completed: `yk-000005-010-domain-skill-path-convention`, `yk-000005-020-domain-user-invoked-skills`, `yk-000005-030-refactor-skill-script-paths`, `yk-000005-040-domain-merge-dependabot-workflow`, `yk-000005-050-domain-handoff-retro-skills`

## Phase yk-000006 — done
- Completed: `yk-000006-010-domain-agent-description-alignment`, `yk-000006-020-domain-worktrees-existing-branch`, `yk-000006-030-domain-handle-pr-reviews-worktree`

## Phase yk-000007 — done
- Completed: `yk-000007-010-domain-security-guard-followups`

## Task Summary

| Task ID | Title | Model Hint |
|---|---|---|
| yk-000001-010-domain-model-hints | Model hint metadata | standard |
| yk-000001-020-domain-analyst-modes | Analyst caller and mode contract | advanced |
| yk-000001-030-domain-authoring-feedback | Authoring feedback loops | standard |
| yk-000001-040-domain-session-retro | Evidence bounded retrospective | standard |
| yk-000001-050-domain-session-handoff | Safe session handoff | advanced |
| yk-000001-060-domain-review-defects | Review defects and targeted linters | standard |
| yk-000001-070-domain-operational-safety | Delivery and isolation safety | advanced |
| yk-000001-080-domain-mission-anchor | Durable mission anchor | advanced |
| yk-000001-090-domain-infra-evidence | Applied scope and bounded FinOps | advanced |
| yk-000001-100-domain-pr-worktrees | PR worktree identity and preservation | advanced |
| yk-000001-110-domain-convergence-callers | Single owner spec convergence | advanced |
| yk-000001-120-domain-pr-body | Feature oriented PR body | standard |
| yk-000002-010-infra-distribution | Bundle distribution integration | standard |
| yk-000003-010-config-upstream-snapshot | T0 (Phase 0) | sonnet |
| yk-000004-010-domain-plan-auto-converge | A1 (#371) | opus |
| yk-000004-020-domain-finish-branch-remote-guard | A3 (#346) | opus |
| yk-000004-030-domain-executor-local-exclude | A8 (executors) | sonnet |
| yk-000004-040-domain-create-pr-features-api | A5 (#391) | sonnet |
| yk-000004-050-domain-scan-secrets-guard | A8 (scan-secrets) | opus |
| yk-000004-060-domain-skill-contradiction-fixes | A2 (#337) + A8 (small fixes) | sonnet |
| yk-000004-070-domain-impl-review-linter-defects | A4 (#340) | sonnet |
| yk-000004-080-domain-debug-feedback-loop | A6 (#335) | sonnet |
| yk-000004-090-domain-brainstorm-tdd-rules | A7 (#335, #345) | sonnet |
| yk-000005-010-domain-skill-path-convention | B1 (#345) | sonnet |
| yk-000005-020-domain-user-invoked-skills | B3 (#335, #345) | sonnet |
| yk-000005-030-refactor-skill-script-paths | B2 (#345) | sonnet |
| yk-000005-040-domain-merge-dependabot-workflow | B4 (#341, #345) | opus |
| yk-000005-050-domain-handoff-retro-skills | B5 (#335, #341, #345) | opus |
| yk-000006-010-domain-agent-description-alignment | C1 (#345) | sonnet |
| yk-000006-020-domain-worktrees-existing-branch | C2 (#347) | sonnet |
| yk-000006-030-domain-handle-pr-reviews-worktree | C3 (#347) | opus |
| yk-000007-010-domain-security-guard-followups | Final review M1/M2/M4/M5 | opus |

## Spec Coverage

- FR-1 / AC-1: `yk-000001-010-domain-model-hints` owns advisory tier/rationale and matching preview/summary; `test.md` provides clause-level expected outcomes.
- FR-2 / AC-2: `yk-000001-020-domain-analyst-modes` owns three caller/mode pairs and bounded diagnostic feedback; `test.md` provides clause-level expected outcomes.
- FR-3 / AC-3: `yk-000001-030-domain-authoring-feedback` owns repository-first questions, behavior TDD and Writing Levers; `test.md` provides clause-level expected outcomes.
- FR-4 / AC-4: `yk-000001-040-domain-session-retro` owns retro categories, ranking, evidence and owner rules; `test.md` provides clause-level expected outcomes.
- FR-4 / AC-4: `yk-000001-050-domain-session-handoff` owns handoff sections, safe artifact writes and invocation metadata; `test.md` provides clause-level expected outcomes.
- FR-5 / AC-5: `yk-000001-060-domain-review-defects` owns A-005–007 and installed targeted-linter evidence; `test.md` provides clause-level expected outcomes.
- FR-6 / AC-6: `yk-000001-070-domain-operational-safety` owns remote deletion, isolation setup, polling deadline and severity row guards; `test.md` provides clause-level expected outcomes.
- FR-7 / AC-7: `yk-000001-080-domain-mission-anchor` owns read/update/curate mission with stable NG/CN history; `test.md` provides clause-level expected outcomes.
- FR-8 / AC-8: `yk-000001-090-domain-infra-evidence` owns eligible applied scope and bounded inline FinOps evidence; `test.md` provides clause-level expected outcomes.
- FR-9 / AC-9: `yk-000001-100-domain-pr-worktrees` owns existing-branch producer and pinned PR worktree consumer; `test.md` provides clause-level expected outcomes.
- FR-10 / AC-10: `yk-000001-110-domain-convergence-callers` owns single-owner convergence and artifact-profile preservation; `test.md` provides clause-level expected outcomes.
- FR-10 / AC-10: `yk-000001-120-domain-pr-body` owns feature Changes and conditional API table; `test.md` provides clause-level expected outcomes.
- FR-10 / AC-10: `yk-000002-010-infra-distribution` owns catalog counts/locales, generated plugin and temporary installs; `test.md` provides clause-level expected outcomes.

Failure Modes: provenance/locale gaps → every source task + distribution; analyst mismatch → analyst; absent session/mission bundles → retro/handoff/mission + distribution; read-only artifact writes → retro/infra; transport/cwd failure → worktrees/operational safety; unavailable runtime → every evidence section; recursive convergence → convergence; auth/schema-only route changes → PR body.

### Claude Code Issue 69 port coverage

- AC0 → `yk-000003-010`; AC1/AC2/AC2b/AC2c, FR6, FR7 → `yk-000004-010`; AC4 → `yk-000004-020`; AC9, NFR1 → `yk-000004-030`; AC6 → `yk-000004-040`; AC8 → `yk-000004-050`; AC3, AC8b → `yk-000004-060`; AC5 → `yk-000004-070`; AC7 → `yk-000004-080`; AC7b → `yk-000004-090`.
- AC11b → `yk-000005-010`; AC12 (2 skills), AC13, FR8 → `yk-000005-020`; AC10, AC11 → `yk-000005-030`; AC13b → `yk-000005-040`; AC12 (4 skills), AC14, AC14b, AC14c → `yk-000005-050`; AC15 → `yk-000006-010`; AC16 → `yk-000006-020`; AC16b, AC17 → `yk-000006-030`.
- Final-review follow-up (security Mediums M1, M2, M4, M5) → `yk-000007-010`. M3, M6 and the Lows stay deferred.
- FR1–FR4 apply to every task; FR5 is the graph above; the NFR1 body-line check is in every task that edits a `SKILL.md`; NFR2 follows from B3/B5.
- Failure Modes: `${CLAUDE_SKILL_DIR}` / partial install → B1; user-invoked → B3; malicious branch / PR number / fork PR → C2, C3; recursion / double run / non-DONE → A1; handoff secret → B5; remote deletion → A3; CI red → B3; upstream unavailable → T0; required-check gate → B4.

## Open Questions

No unjustified requirements emitted. Live runtime availability remains an execution-time limitation, not a source-contract success claim. No DB migration or library introduction is required.

Claude Code Issue 69 port: no requirement was dropped for lacking an Acceptance Criterion. Items verified by review only (no grep AC): brainstorm ordering rules and tdd seam line (`yk-000004-090`), fix #4 / checklist alignment (`yk-000004-080`), refactor-clean and security-audit sentence corrections (`yk-000004-060`), advisor-escalation / aggregate-pr / worktree-run corrections (`yk-000004-030`). The spec's Open Questions 1–6 keep their stated defaults.

