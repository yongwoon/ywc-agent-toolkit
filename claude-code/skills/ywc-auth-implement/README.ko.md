# ywc-auth-implement

인증 기능(email/password, OAuth, MFA, shallow RBAC) 구현을 표준화하는 skill입니다. Policy Interview → Stack 감지 → battle-tested Library/managed Service 동적 추천 → `ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer`로의 dispatch 흐름을 orchestration하며, 실제 application 인증 code는 이 skill이 직접 작성하지 않습니다.

## 사용 시나리오

- 사용자가 "인증 구현", "로그인 기능 추가해줘", "OAuth 연동"이라고 말할 때
- 신규 프로젝트에 email/password 또는 OAuth 기반 인증을 처음 도입할 때
- 기존 인증을 확장하거나 마이그레이션해야 할 때 (`new`/`extend`/`migrate` 선택 필요)

## 사용 방법

```bash
/ywc-auth-implement
```

또는 자연어로 호출:

> "인증 구현해줘"

## Input

- 필수: 대상 프로젝트의 Framework/Database 근거 (자동 감지, 부족 시 `ywc-tech-research`로 routing)
- 필수: Policy Interview 9개 카테고리에 대한 사용자 응답 (수단/MFA/session/password/profile/탈퇴/RBAC/consent/abuse 방지)
- (선택) 기존 인증 발견 시 `new`/`extend`/`migrate` 선택

## Output

- Preflight 결과, Policy Interview 요약, 추천 Library/Service, dispatch된 Subagent 목록, Security/E2E Gate 결과, `## Output Format`의 4-값 Completion Status(`DONE`/`DONE_WITH_CONCERNS`/`BLOCKED`/`NEEDS_CONTEXT`)
- Preflight는 어떤 interview 질문보다 먼저 중단되며, 기존 인증이 발견되면(사용자가 `new`/`extend`/`migrate`를 선택할 때까지) 또는 stack 근거가 불충분하면(먼저 `ywc-tech-research`로 routing) `NEEDS_CONTEXT`를 반환합니다
- Security/E2E Gate는 `ywc-security-audit` severity를 status로 매핑합니다: Critical/High = 0이면 policy-conditional E2E로 진행하고, Critical/High ≥ 1이면 `DONE_WITH_CONCERNS`로 종료하며 remediation과 재감사 전까지 E2E·PR 제안·추천 caching을 모두 건너뜁니다. Audit command 실행 실패는 `BLOCKED`, scope/trust boundary 부족은 `NEEDS_CONTEXT`를 반환합니다
- `DONE`은 Security Gate가 clean하고 승인된 모든 E2E flow가 fresh evidence(command, exit code, key output)와 함께 기록되어야 합니다. 그렇지 않으면 어느 Gate에서 중단되었는지와 함께 위 status 중 하나를 보고합니다

## 관련 Skill

- `ywc-backend-coder` / `ywc-frontend-coder` — TDD 규율 하 실제 구현 dispatch 대상
- `ywc-doc-writer` — 법적 검토 전 임시본 ToS/Privacy Policy 초안 dispatch 대상
- `ywc-security-audit` / `ywc-e2e-test-strategy` — 구현 후 Security/E2E Gate
- `ywc-tech-research` — Stack 근거 불충분 시 실시간 리서치 routing
