# 000018-010-docs-principles-foundation — Implementation Checklist

## Prerequisites

- [ ] (없음 — 루트 태스크)

## Allowed Edit Scope

- [ ] `claude-code/skills/references/principles.md`만 편집
- [ ] Ownership 밖 편집이 필요하면 중단·보고

## Stop Conditions

- [ ] 기존 §2~§10 계층의 의미를 바꿔야 하는 상황이면 중단(보강만 허용)
- [ ] readable-code.md / tdd-deep-module-gray-box.md 본문을 고쳐야 하면 중단(가리키기만)

## Implementation Steps

- [ ] **Assumption & Ambiguity Discipline 절 추가** (§3 Evidence 또는 §6 Failure 인근)
  - 가정은 명시 라벨링 시에만 진술; requirement/파일 동작/API 계약/벤치마크·테스트 결과/사용자 의도 발명 금지
  - 다음 단계가 누락 컨텍스트에 의존하면 `NEEDS_CONTEXT` 반환 또는 최소 차단 질문
  - 요청이 두 해석을 허용하고 scope/data model/의미를 바꾸면 조용히 고르지 말고 둘 제시(저작 skill로 위임)
- [ ] **Goal-Driven Execution 절 추가**
  - 사용자 목표·성공 기준에서 출발, 각 단계를 명명된 산출에 묶음
  - 인접 정리/스타일 churn/추측 재설계 금지 — Surgical은 `readable-code.md` §G·anti-dogma, test-first는 `tdd-deep-module-gray-box.md` §2를 가리킴
  - 목표-특정 검증 실행 또는 문서화된 blocker/예외 후에만 완료 선언
- [ ] **§A9 용어 노트 1줄 추가** — Simplicity(spec-validate)/Minimalism(code-gen)/과설계가 같은 'Simplicity First' 기둥의 다른 라벨임을 명시

## Task Verify

- [ ] `rg -n "Assumption|Goal-Driven|NEEDS_CONTEXT|readable-code|tdd-deep-module" claude-code/skills/references/principles.md` 가 모든 토큰 반환
- [ ] `rg -n "Simplicity|Minimalism" claude-code/skills/references/principles.md` 가 용어 노트 반환

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] markdownlint 통과 (변경 파일이 reference라 README 영향 없음)
- [ ] (typecheck/build 해당 없음 — 마크다운 reference 편집)
