# 000018-050-docs-execution-discipline

## Purpose

실행 클러스터에 Karpathy 원칙 4(검증 가능한 루프)와 원칙 3(범위 통제)을 강화한다. parallel-executor의 회귀 비대칭을 해소하고, 두 executor에 기계적 Ownership 게이트를, debug 경로에 test-first 순서와 재현 요구를 추가한다.

## Scope

- FR-6: `ywc-parallel-executor/SKILL.md` Step 4c에 전체/영향범위 회귀 스위트 레이어(sequential :315 미러링).
- FR-8: `ywc-sequential-executor`/`ywc-parallel-executor`에 첫 커밋/델리버리 전 `git diff --name-only` Ownership 게이트.
- FR-9: `ywc-debug-rootcause/SKILL.md` Phase 3 §2에 "자동화 가능 시 실패 테스트가 첫 수정 이전 RED" 1절.
- FR-10: `ywc-root-cause-analyst.md` NEEDS_CONTEXT 트리거에 재현 증거 부재 추가.
- parallel-executor README locale set 동기화(§A7 — 4c 검증 단계 변경). sequential/debug-rootcause/analyst는 내부 메커니즘이라 README 불필요(§A7).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §FR-6, §FR-8, §FR-9, §FR-10
- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §Iteration 1 Amendments §A7(README 목록), §A8(agents 경로)
- `claude-code/skills/ywc-parallel-executor/SKILL.md:272` — 4c Task Verify(전체 스위트 없음)
- `claude-code/skills/ywc-sequential-executor/SKILL.md:265,290,315` — Simplicity+Surgical/Completeness Gate/전체 스위트(보존)
- `claude-code/skills/ywc-debug-rootcause/SKILL.md:110,122-125` — Phase 3/4 RED 순서
- `claude-code/agents/ywc-root-cause-analyst.md:131` — NEEDS_CONTEXT 트리거

### Summary

parallel 4c는 현재 Task Verify만 돌려 sequential(:315 전체 스위트)과 검증 깊이가 비대칭이다 — 회귀 레이어를 추가한다. 두 executor의 prose Surgical 규율을 보완하는 기계적 git-diff Ownership 게이트를 더한다. debug-rootcause는 RED를 첫 수정 이전으로 당기고, analyst는 재현 없는 판정을 거부한다.

### Out of Scope (from spec)

- sequential의 기존 :265/:315 절 재작성(보존; 게이트만 추가)
- agent model/tool/출력 상태 변경

## Dependencies

### Depends On

- `000018-010-docs-principles-foundation` — Goal-Driven/Surgical 표준 원칙 이름

### Depended By

- `000019-010-infra-karpathy-validation` — 최종 검증(AC7/AC9/AC10/AC11)

## Key Files

- `claude-code/skills/ywc-parallel-executor/SKILL.md` — 4c 회귀 레이어 + Ownership 게이트
- `claude-code/skills/ywc-sequential-executor/SKILL.md` — Ownership 게이트(+ FR-12 대칭 'no objective eval' 노트, 필요 시 evals/)
- `claude-code/skills/ywc-debug-rootcause/SKILL.md` — Phase 3 RED 순서
- `claude-code/agents/ywc-root-cause-analyst.md` — NEEDS_CONTEXT 트리거
- `claude-code/skills/ywc-parallel-executor/README.md`/`README.ko.md`/`README.en.md`/`README.ja.md`

## Notes

- §A8: analyst 편집은 소스 경로 `claude-code/agents/`.
- §A2 대칭: sequential evals가 기계적 게이트를 객관적으로 검증하기 어려우면 'no objective eval — 사유' 노트.
- parallel 회귀가 worktree에서 전체 스위트 비현실적이면 영향범위 한정 + 근거 문서화(완전 생략 금지).

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-parallel-executor/**`
- `claude-code/skills/ywc-sequential-executor/**`
- `claude-code/skills/ywc-debug-rootcause/**`
- `claude-code/agents/ywc-root-cause-analyst.md`

### Shared Surfaces

- `공유 SoT: principles.md` / `tdd-deep-module-gray-box.md` (읽기 전용 인용)

### Conflicts With

- (None identified)

### Parallelizable After

- `000018-010-docs-principles-foundation`

### Task Verify

- `rg -n "전체|full|회귀|regression|impacted" claude-code/skills/ywc-parallel-executor/SKILL.md`
- `rg -n "git diff --name-only|Ownership" claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md`
- `rg -n "RED|reproduction|재현" claude-code/skills/ywc-debug-rootcause/SKILL.md`
- `rg -n "NEEDS_CONTEXT|reproduction|재현" claude-code/agents/ywc-root-cause-analyst.md`
- `bash scripts/validate.sh`

## Out of Scope

- sequential 전체 스위트(:315) 로직 변경
- debug-rootcause/analyst의 README 신설
