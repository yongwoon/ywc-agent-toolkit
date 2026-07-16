# ywc-auth-implement

인증 기능을 바로 구현하는 대신, 프로젝트 증거와 승인된 정책을 바탕으로 보안 감사와 E2E 검증까지 연결하는 Codex 오케스트레이션 Skill입니다. 비밀값을 출력하거나 직접 JWT/비밀번호 암호화를 권장하지 않습니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)
- [中文](./README.zh.md)
- [Español](./README.es.md)

## 사용 시점

- 로그인, OAuth, 세션, 계정 삭제를 포함한 인증 기능의 구현 경로가 필요할 때
- 기존 인증을 `new`, `extend`, `migrate` 중 하나로 결정해야 할 때
- 인증 라이브러리 또는 managed service를 프로젝트 증거에 맞춰 선택해야 할 때

## 사용 방법

```text
$ywc-auth-implement
```

Skill은 읽기 전용 preflight, 9개 정책 인터뷰, evidence-based 추천을 수행한 뒤 아래 경로를 출력합니다. task generation은 자동 실행하지 않습니다.

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

Critical/High 보안 감사 결과가 있으면 E2E, PR 제안, 캐시를 건너뜁니다. 법률 문서는 항상 `법적 검토 전 임시본`입니다.
