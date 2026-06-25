# Handle PR Reviews

PR Review Comment를 확인하고, 필요한 수정 사항을 반영한 뒤 각 Thread에 답변하는 Claude Code Skill입니다.

## 개요

PR Review 이후 반복되는 대응 작업을 자동화합니다. 명확한 수정 요청은 직접 반영하고, 판단이 필요한 의견은 사용자 확인 대상으로 분류합니다.

PR을 "대응"한다는 것은 단순히 Comment에 답변하는 것이 아니라 PR을 **Mergeable** 상태로 남기는 것입니다. 이를 위해 **세 가지 독립적인 Gate** — (1) Review Comment, (2) CI Status, (3) Merge-readiness(Conflict) — 를 **매 실행마다** 모두 확인합니다. Comment가 0건이어도 CI가 Red이거나 base와 Conflict가 날 수 있으므로 CI·Conflict Gate는 건너뛰지 않습니다.

### 주요 기능

- Comment를 수정 요청, 논의 필요, 질문, 처리 완료로 분류
- 같은 파일의 Comment를 묶어서 처리
- Reviewer가 사용한 언어에 맞춰 답변 작성
- 이미 처리되었거나 답변된 Comment는 Skip
- Comment 처리 후 CI 실패와 base Conflict를 확인하여 PR을 Mergeable 상태로 마감 (Comment가 0건이어도 두 Gate는 항상 실행)

## 사용 방법

```text
/handle-pr-reviews
/handle-pr-reviews 123
```

자연어 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- PR이 존재하는 Branch에서 실행

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
