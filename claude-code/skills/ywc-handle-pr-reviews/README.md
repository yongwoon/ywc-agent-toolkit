# Handle PR Reviews

PR Review Comment를 확인하고, 수정이 필요한 부분을 Fix한 뒤, 각 Comment에 답변하는 Claude Code Skill입니다.

## 개요

PR Review를 받은 후 Comment를 하나씩 확인하고 대응하는 반복 작업을 자동화합니다. 명확한 수정 요청은 자동으로 Fix하고, 논쟁의 여지가 있는 Comment는 사용자에게 판단을 요청합니다. 모든 처리 결과는 Comment Thread에 답변으로 남깁니다.

PR을 "대응"한다는 것은 단순히 Comment에 답변하는 것이 아니라 PR을 **Mergeable** 상태로 남기는 것입니다. 이를 위해 **세 가지 독립적인 Gate** — (1) Review Comment, (2) CI Status, (3) Merge-readiness(Conflict) — 를 **매 실행마다** 모두 확인합니다. Comment가 0건이어도 CI가 Red이거나 base와 Conflict가 날 수 있으므로 CI·Conflict Gate는 건너뛰지 않습니다.

### 주요 특징

- **Comment 자동 분류**: 수정 요청 / 논쟁적 의견 / 질문 / 이미 처리됨 4가지로 분류
- **파일별 그룹 처리**: 같은 파일의 Comment를 모아서 한 번에 처리, 파일당 하나의 Commit 생성
- **답변 언어 매칭**: Reviewer가 한국어로 작성하면 한국어로 답변
- **중복 방지**: 이전에 처리한 Comment나 이미 답변이 달린 Comment는 Skip
- **CI·Conflict까지 대응**: Comment 처리 후 CI 실패와 base Conflict를 확인하여 PR을 Mergeable 상태로 마감 (Comment가 0건이어도 두 Gate는 항상 실행)

## 사용 방법

### 기본 사용 (현재 Branch의 PR)

```
/handle-pr-reviews
```

### PR 번호 지정

```
/handle-pr-reviews 123
```

### 자연어 호출

```
"PR 리뷰 처리해줘"
"리뷰 코멘트 반영해줘"
"Review feedback 처리해줘"
```

## Comment 분류 기준

| Category | Action |
| --- | --- |
| **명확한 수정 요청** | 자동으로 Fix 적용 |
| **논쟁적/모호한 요청** | 사용자에게 판단 요청 (자동 Fix 안 함) |
| **질문** | 설명 답변만 작성 |
| **이미 처리됨** | Skip |

## 실행 흐름

1. **PR 식별** - PR 번호 확인 또는 현재 Branch에서 자동 감지
2. **Comment 수집 및 필터링** - 처리 불필요한 Comment Skip (Comment가 0건이면 3~5단계는 건너뛰되 6~7단계 Gate는 반드시 실행)
3. **파일별 그룹화** - 같은 파일의 Comment를 모아서 분석
4. **분류 및 Fix** - Category별 적절한 Action 수행
5. **답변 작성** - 각 Comment Thread에 처리 결과 답변
6. **CI Gate (항상 실행)** - `gh pr checks`로 CI 상태 확인, 실패 시 분류·Fix(최대 2회) 또는 사용자 보고
7. **Merge-readiness Gate (항상 실행)** - `gh pr view --json mergeable`로 base Conflict 확인, merge-not-rebase로 갱신하거나 실제 Conflict는 사용자에게 surface
8. **결과 요약** - Comment/CI/Conflict 세 Gate 상태를 모두 보고

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- PR이 존재하는 Branch에서 실행

## 사용 Tool

`Bash`, `Read`, `Edit`, `Write`, `Glob`, `Grep`, `Agent`
