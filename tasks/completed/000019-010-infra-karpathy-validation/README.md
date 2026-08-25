# 000019-010-infra-karpathy-validation

## Purpose

Phase 000018 전 변경을 통합 검증하는 hard gate. 모든 FR이 반영됐는지 rg로 확인하고, README locale 완비·저장소 검증·범위 경계를 통과시킨다.

## Scope

- FR-11: §A5 확장 rg로 12개 파일에 걸친 토큰 존재 확인, `bash scripts/validate.sh` / `install.sh --list --cc` / `--list --cc-agents` exit 0, 범위 경계(codex/·제품 코드·무관 locale 미변경) 확인.
- 최종 AC 게이트: AC2/AC12/AC13/AC14/AC15/AC16.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §FR-11
- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §Iteration 1 Amendments §A5(확장 rg), §A6(AC2/AC12), §A7(README 목록)
- `CLAUDE.md`(루트) — 스킬 구조/검증 규칙

### Summary

Phase 000018의 5개 태스크가 모두 merge된 뒤 실행되는 hard gate다. 확장 rg(§A5)로 명령 수준 증거를 수집하고, validate.sh + 두 install --list로 구조/메타 무결성을, git diff로 범위 경계를 확인한다.

### Out of Scope (from spec)

- 소스 SKILL.md/agent/reference 편집 — Phase 000018 태스크가 담당(이 태스크는 검증 전용)

## Dependencies

### Depends On

- `000018-010-docs-principles-foundation`
- `000018-020-docs-planning-discipline`
- `000018-030-docs-task-generator-goal-evals`
- `000018-040-docs-surgical-simplicity-detection`
- `000018-050-docs-execution-discipline`

### Depended By

- (None — 최종 게이트)

## Key Files

- (검증 전용 — 소스 편집 없음; 필요 시 구현 노트/검증 로그만)

## Notes

- Phase 하드 게이트: Phase 000018의 모든 태스크 완료 후에만 시작.
- AC2(중복 karpathy skill 없음)·AC12(agent 전문화 보존)·AC13(README 목록 §A7)·AC14(검증 exit 0)·AC15(범위 경계)·AC16(eval) 모두 이 게이트에서 확인.

## Parallel Execution Metadata

### Ownership

- (검증 전용 — 편집 없음; 구현 노트/로그만)

### Shared Surfaces

- (None — read-only 검증)

### Conflicts With

- (None identified)

### Parallelizable After

- `000018-010`, `000018-020`, `000018-030`, `000018-040`, `000018-050` (전부 merge)

### Task Verify

- §A5 확장 rg가 12개 파일에서 토큰 반환:

  ```bash
  rg -n "Assumption|Goal-Driven|NEEDS_CONTEXT|Simplicity|Surgical|Minimalism|success criteria|drive-by|interpretation|Open Questions|Ownership|RED|reproduction" \
    claude-code/skills/references/principles.md \
    claude-code/skills/ywc-spec-validate/SKILL.md \
    claude-code/skills/ywc-plan/SKILL.md \
    claude-code/skills/ywc-spec-writer/SKILL.md \
    claude-code/skills/ywc-task-generator/SKILL.md \
    claude-code/skills/ywc-impl-review/SKILL.md \
    claude-code/skills/ywc-impl-review/references/design-agent.md \
    claude-code/skills/ywc-parallel-executor/SKILL.md \
    claude-code/skills/ywc-sequential-executor/SKILL.md \
    claude-code/skills/ywc-code-gen/SKILL.md \
    claude-code/skills/ywc-debug-rootcause/SKILL.md \
    claude-code/agents/ywc-root-cause-analyst.md
  ```

- `bash scripts/validate.sh` exit 0
- `bash scripts/install.sh --list --cc` exit 0
- `bash scripts/install.sh --list --cc-agents` exit 0
- `git diff --name-only` 가 `codex/`·제품 코드·무관 locale을 포함하지 않음(AC15)
- 새 `claude-code/skills/karpathy-*` 또는 karpathy 전용 agent 없음(AC2)
- impl-review 5-aspect 이름 + Step 3 주입 블록 온전(AC12, §A4 rg)

## Out of Scope

- 발견된 누락의 직접 수정 — 해당 Phase 000018 태스크로 되돌려 수정(이 게이트는 판정만)
