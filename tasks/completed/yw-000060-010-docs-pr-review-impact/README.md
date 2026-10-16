# yw-000060-010-docs-pr-review-impact

## Purpose
PR 본문과 수동 testsheet, 리뷰 판단의 근거를 강화한다 — create-pr Impact 섹션, gen-testcase Impact 시나리오 소스, impl-review SDK 예외 계층 검증 (Phase C).

## Scope
- create-pr Step 7 optional Impact 섹션 + diff 재조회 금지 (FR-C1)
- gen-testcase Impact 블록 lift / 시나리오 소스 (FR-C2)
- impl-review devex-agent §3 + coderabbit-methodology §4 SDK 예외 계층 문단 (FR-C3)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — `## Scope` Phase C, FR-C1~FR-C3, AC-8, AC-12(C3)
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #258 / #260(Impact 부분) / #262 를 반영한다. FR-C2 는 FR-C1 의 Impact 섹션을 전제하므로 같은 task. #260 의 Security lens 문장과 eval case 6 은 제외한다.

### Out of Scope (from spec)
- #260 Security lens / `evals.json` — #259 선행 필요 (Open Questions 1)
- #283 screenshot evidence

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- `yw-000059-010-docs-spec-plan-omission-checks` — Phase B 머지 base

### Depended By
- `yw-000061-010-docs-fastify-scaffold` — Phase C 머지 base

## Key Files
- `claude-code/skills/ywc-create-pr/SKILL.md` (`:193`, `:243`, `:264`)
- `claude-code/skills/ywc-gen-testcase/SKILL.md` (`:96`, `:195`)
- `claude-code/skills/ywc-impl-review/references/devex-agent.md` (`:32`)
- `claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md` (`:59`)

## Notes
- create-pr 는 414 줄 — Impact 5 언어 표 추가 후에도 500 줄 이하 확인.
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: haiku — M2 (Ownership 전부 `*.md`, category docs)

### Ownership
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-gen-testcase/SKILL.md`
- `claude-code/skills/ywc-impl-review/references/devex-agent.md`
- `claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`

### Owned Interface
- PR 본문 Impact 섹션 heading (5 언어 표, upstream `cc-258` 과 동일) — gen-testcase 가 이 heading 을 lift 대상으로 인식

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified — Phase hard gate)

### Parallelizable After
- `yw-000059-010-docs-spec-plan-omission-checks`

### Task Verify
- `grep -n "Impact" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-gen-testcase/SKILL.md` → create-pr Step 7 5 언어 표 + gen-testcase 시나리오 소스 1 번 (AC-8)
- `grep -c "exception hierarchy\|exception taxonomy" claude-code/skills/ywc-impl-review/references/devex-agent.md claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md` 각 ≥1 (AC-12 C3)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- gen-testcase Security lens / eval case
