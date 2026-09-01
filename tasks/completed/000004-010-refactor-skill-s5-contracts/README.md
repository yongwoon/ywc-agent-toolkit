# 000004-010-refactor-skill-s5-contracts

## Purpose

Codex skill evaluator에서 S5가 0 또는 1로 나온 skill들의 Output / Validation / Status contract를 보강하여, 구현 후 모든 target skill이 S5 >= 3을 만족하게 한다.

## Scope

- FR-1의 target skill `SKILL.md`에 concise한 `## Output Format`, `## Validation`, `Status:` 또는 report contract를 추가
- 필요한 경우 각 skill의 `evals/evals.json` 추가
- `ywc-gen-testcase`와 `ywc-worktrees`는 `Iteration 1 Amendments`의 authoritative row를 따른다
- Codex `SKILL.md` frontmatter를 `name` / `description`만 유지

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-1-improve-s5-contracts-for-targeted-skills` — S5 target skill 목록과 기본 요구사항
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#iteration-1-amendments` — `ywc-gen-testcase`, `ywc-worktrees` authoritative 수정 요구사항
- `docs/ywc-plans/codex-toolkit-eval-improvements.validation.md#completion-status` — spec validation 완료 상태

### Summary

이 task는 Codex skill 문서와 필요한 eval fixture를 수정한다. 핵심 목표는 `score.py`의 S5 네 bucket 중 최소 세 개가 실제로 충족되도록 만드는 것이다. `evals/evals.json`은 placeholder가 아니라 realistic prompt와 concrete anti-behavior를 담아야 한다.

### Out of Scope (from spec)
- Codex agent TOML 수정 — `000004-020-refactor-agent-integration-status`에서 처리
- `trigger-cases.json` 확장 — `000004-030-test-trigger-fixture-coverage`에서 처리
- evaluation report / scoreboard refresh — `000005-010-test-evaluation-report-refresh`에서 처리
- Claude Code skill 수정 — spec Out of Scope

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000005-010-test-evaluation-report-refresh` — post-change S5 score 검증과 report 갱신에 필요

## Key Files

| 파일 | 변경 유형 |
|---|---|
| `codex/skills/ywc-product-review/SKILL.md` | Output / Validation / Status contract 추가 |
| `codex/skills/ywc-project-docs/SKILL.md` | Output path/report contract 및 validation 추가 |
| `codex/skills/ywc-project-scaffold/SKILL.md` | scaffold report contract 및 validation 추가 |
| `codex/skills/ywc-team-assemble/SKILL.md` | `## Output Format` 전환 및 validation 추가 |
| `codex/skills/ywc-changelog-release-notes/SKILL.md` | validation criteria 추가 |
| `codex/skills/ywc-create-pr/SKILL.md` | Status / validation 보강 |
| `codex/skills/ywc-gen-testcase/SKILL.md` | Iteration 1 요구에 맞춘 Output Format / Validation 보강 |
| `codex/skills/ywc-handle-pr-reviews/SKILL.md` | output format / validation 보강 |
| `codex/skills/ywc-incident-postmortem/SKILL.md` | validation checklist 보강 |
| `codex/skills/ywc-merge-dependabot/SKILL.md` | output format / status 보강 |
| `codex/skills/ywc-release-pr-list/SKILL.md` | output format / status / validation 보강 |
| `codex/skills/ywc-ui-ux-review/SKILL.md` | validation checklist 보강 |
| `codex/skills/ywc-worktrees/SKILL.md` | Iteration 1 요구에 맞춘 Output Format / Validation / Status 보강 |
| `codex/skills/*/evals/evals.json` | 필요한 skill에 realistic eval fixture 추가 |

## Notes

- `ywc-gen-testcase`는 현재 body line count가 높으므로 inline example을 늘리기보다 concise section 또는 eval fixture를 우선한다.
- S5 scorer는 `## Output Format` 또는 `Output:`, `## Validation` 또는 `Validation Checklist`, `evals/` 또는 `scripts/`, `Status:` 또는 fenced text를 각각 하나의 bucket으로 본다.
- Existing wording은 가능한 유지하고, scorer 만족만을 위한 meaningless `Status:` text는 피한다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-product-review/**`
- `codex/skills/ywc-project-docs/**`
- `codex/skills/ywc-project-scaffold/**`
- `codex/skills/ywc-team-assemble/**`
- `codex/skills/ywc-changelog-release-notes/**`
- `codex/skills/ywc-create-pr/**`
- `codex/skills/ywc-gen-testcase/**`
- `codex/skills/ywc-handle-pr-reviews/**`
- `codex/skills/ywc-incident-postmortem/**`
- `codex/skills/ywc-merge-dependabot/**`
- `codex/skills/ywc-release-pr-list/**`
- `codex/skills/ywc-ui-ux-review/**`
- `codex/skills/ywc-worktrees/**`

### Shared Surfaces
- Codex skill activation and output contract documentation
- S5 mechanical score output from `score.py`

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
- `bash scripts/validate.sh`

## Out of Scope

- Broad style rewrites of all skill bodies
- Claude Code skill parity updates
- Changing evaluator scoring logic
