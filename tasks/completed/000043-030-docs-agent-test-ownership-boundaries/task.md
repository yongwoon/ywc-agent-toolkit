# Task: 에이전트 테스트 소유권 경계 정리

## Prerequisites
- [ ] (없음) — 독립 실행.

## Allowed Edit Scope
- `claude-code/agents/{ywc-backend-coder,ywc-frontend-coder,ywc-qa-engineer,ywc-doc-writer}.md` 만.

## Stop Conditions
- 공유 규칙 문구가 3개 에이전트(backend/frontend/qa) 간에 서로 모순되게 적용되면 중단하고 재정렬.
- qa-engineer에서 dispatched E2E **작성** 능력까지 제거하려는 유혹이 생기면 중단 — §AC10′는 전략/소유권 주장만 제거.

## Implementation Steps
- [ ] **공유 규칙 확정(먼저)**: 한 문장으로 고정 — "코더 에이전트는 동일 태스크에서 저작한 코드에 대한
      co-located 단위/통합 테스트만 소유한다. standalone 테스트 스위트·커버리지 확장은 ywc-qa-engineer가 소유한다."
- [ ] **FR7** `ywc-backend-coder.md` Mission(:21-24)의 "unit + integration tests that cover the [code]"를 위 공유
      규칙 문구로 교체(co-located 한정). 설명의 기존 anti-trigger와 일치 확인.
- [ ] **FR8** `ywc-frontend-coder.md`(:19 부근, :51-52) 자체 테스트를 "구현 중인 컴포넌트"로 한정하고 standalone/
      coverage-gap 테스트는 ywc-qa-engineer로 라우팅함을 본문에 명시.
- [ ] **FR9** `ywc-doc-writer.md`(:25) scope 서술에 라우팅 노트 추가: "glossary 항목은 ywc-ubiquitous-language가
      본 에이전트를 dispatch한다".
- [ ] **FR10/§AC10′** `ywc-qa-engineer.md`에서 ":77 'or reviewing them'" 제거, Mission(:22-24)의 standalone E2E
      **전략/소유권** 주장 정리. dispatched codified E2E 테스트 **작성** 능력 서술은 보존.

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json`에서
      4개 에이전트의 A3/A4/A5(mechanical)가 모두 5 유지(회귀 없음).
- [ ] 공유 규칙 문구가 backend/frontend/qa 3개 파일에 정합(상호 모순 없음) — 수동 대조.

## Verification
- [ ] `bash scripts/validate.sh` exit 0.
- [ ] `git diff --stat`이 4개 에이전트 파일만 포함.
