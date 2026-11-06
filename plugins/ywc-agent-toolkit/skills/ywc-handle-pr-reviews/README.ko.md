# Handle PR Reviews

PR Review Comment를 확인하고, 필요한 수정 사항을 반영한 뒤 각 Thread에 답변하는 Codex Skill입니다.

## 개요

PR Review 이후 반복되는 대응 작업을 자동화합니다. 명확한 수정 요청은 직접 반영하고, 판단이 필요한 의견은 사용자 확인 대상으로 분류합니다.

### 주요 기능

- Comment를 수정 요청, 논의 필요, 질문, 처리 완료로 분류
- 같은 파일의 Comment를 묶어서 처리
- Reviewer의 원 Comment 언어에 맞춰 한국어, 영어, 일본어, 중국어, 스페인어 등으로 답변하고, 코드/명령 출력/파일 경로/API 이름/인용문은 번역하지 않음
- 이미 처리되었거나 답변된 Comment는 Skip

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
- [Chinese (Simplified)](./README.zh.md)
- [Spanish](./README.es.md)

## 기존 브랜치와 PR worktree

`--worktree 123`은 같은 저장소의 열린 PR 번호와 head를 고정합니다. 정확한 fetch/fast-forward, 작업별 cwd/root/branch 확인과 한 번의 재진입만 허용하며, 필수 명령 실패 뒤 mutation을 중단합니다. 생성한 worktree만 `--keep-branch` 정리 안내를 제공합니다.
