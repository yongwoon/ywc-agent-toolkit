# ywc-auth-implement (한국어)

인증 구현을 위한 정책·보안·E2E 게이트 오케스트레이션 Skill입니다. application auth code를 직접 만들거나 secret, JWT, password crypto를 직접 제안하지 않습니다.

## 사용 시점

- 로그인, OAuth, 세션, 계정 삭제 기능을 계획할 때
- 기존 인증의 `new`, `extend`, `migrate` 방향을 결정할 때
- 프로젝트 증거로 established library 또는 managed service를 선택할 때

## 실행

```text
$ywc-auth-implement
```

읽기 전용 preflight와 9개 정책 인터뷰 후 다음 경로를 출력만 하고 자동 실행하지 않습니다. `$ywc-task-generator`는 medium/large 작업에서 `$ywc-spec-ready`가 `DONE`일 때만 출력합니다.

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

Critical/High audit finding은 E2E·PR·cache를 모두 중단하며, remediation과 재감사가 끝날 때까지 경로는 `DONE_WITH_CONCERNS`로 종료됩니다. 법률 초안은 `법적 검토 전 임시본`으로 표시합니다.
