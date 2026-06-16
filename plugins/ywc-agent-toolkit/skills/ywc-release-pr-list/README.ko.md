# Release PR List

Release PR에 포함된 PR 목록을 추출하고, Author별로 정리하여 PR Description을 업데이트하는 Codex Skill입니다.

## 개요

`develop` → `main` 같은 Release PR을 만들 때, Commit Headline에서 PR 번호를 추출하고 Author 정보를 조회하여 `## PR LIST` 섹션을 갱신합니다.

### 주요 기능

- Commit Headline의 `#<number>` 패턴에서 PR 번호 추출
- PR을 Author Login 기준으로 그룹화하고 알파벳순 정렬
- 실행 시 사용자에게 PR 별 Summary 추가 여부를 묻고, 동의한 경우에만 PR Title 기반 한 줄 요약을 항목에 함께 기록
- `## PR LIST` 외 기존 Description은 유지
- 여러 번 실행해도 같은 섹션만 갱신

## 사용 방법

```text
/release-pr-list 301
```

자연어 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- Release PR이 이미 생성되어 있어야 함

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
