# 000004-020-refactor-agent-integration-status

## Purpose

Codex custom agent의 A7 Caller Integration 점수와 shared Status line inventory warning을 개선한다.

## Scope

- `ywc-debug-rootcause`에서 `ywc-root-cause-analyst`를 optional read-only advisor로 실제 호출 가능한 문맥에 연결
- `ywc-security-audit`에서 `ywc-security-engineer`를 optional read-only advisor로 실제 호출 가능한 문맥에 연결
- `ywc-performance-engineer`와 `ywc-root-cause-analyst` TOML Output contract에 정확한 shared Status line 추가

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-3-fix-agent-caller-integration` — A7 caller reference 요구사항
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-4-normalize-shared-agent-status-line` — inventory warning 해소용 exact Status phrase
- `docs/ywc-plans/codex-toolkit-eval-improvements.validation.md#completion-status` — spec validation 완료 상태

### Summary

이 task는 skill 본문에서 agent 이름이 decorative reference가 아니라 실제 bounded delegation guidance로 나타나도록 수정한다. agent TOML에는 inventory gate가 찾는 exact phrase `Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>`를 보존된 role semantics 안에 추가한다.

### Out of Scope (from spec)
- Skill S5 contract 보강 — `000004-010-refactor-skill-s5-contracts`에서 처리
- Trigger fixture 확장 — `000004-030-test-trigger-fixture-coverage`에서 처리
- Evaluator scoring model 변경 — spec Out of Scope

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000005-010-test-evaluation-report-refresh` — A7 score와 inventory warning 검증에 필요

## Key Files

| 파일 | 변경 유형 |
|---|---|
| `codex/skills/ywc-debug-rootcause/SKILL.md` | `ywc-root-cause-analyst` optional caller guidance 추가 |
| `codex/skills/ywc-security-audit/SKILL.md` | `ywc-security-engineer` optional caller guidance 추가 |
| `codex/agents/ywc-performance-engineer.toml` | exact shared Status line 추가 |
| `codex/agents/ywc-root-cause-analyst.toml` | exact shared Status line 추가 |

## Notes

- A7 scorer는 Codex skill text 안의 exact agent-name reference를 찾는다.
- Agent reference에는 언제 호출할지, 어떤 bounded payload를 넘길지, 어떤 output status를 기대할지 포함해야 한다.
- Custom-agent dispatch가 불가능한 환경에서도 inline fallback이 가능하다는 기존 의미를 보존한다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-debug-rootcause/SKILL.md`
- `codex/skills/ywc-security-audit/SKILL.md`
- `codex/agents/ywc-performance-engineer.toml`
- `codex/agents/ywc-root-cause-analyst.toml`

### Shared Surfaces
- Codex custom agent output contract
- A7 caller integration score

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
- `bash scripts/validate.sh`

## Out of Scope

- Adding new custom agents
- Changing agent sandbox mode, model, or role scope
- Making agent delegation mandatory
