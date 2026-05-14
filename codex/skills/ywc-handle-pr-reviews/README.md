# Handle PR Reviews

PR Review Comment를 확인하고, 수정이 필요한 부분을 Fix한 뒤, 각 Comment에 답변하는 Codex Skill입니다.

## 개요

PR Review를 받은 후 Comment를 하나씩 확인하고 대응하는 반복 작업을 자동화합니다. 명확한 수정 요청은 자동으로 Fix하고, 논쟁의 여지가 있는 Comment는 사용자에게 판단을 요청합니다. 모든 처리 결과는 Comment Thread에 답변으로 남깁니다.

### 주요 특징

- **Comment 자동 분류**: 수정 요청 / 논쟁적 의견 / 질문 / 이미 처리됨 4가지로 분류
- **파일별 그룹 처리**: 같은 파일의 Comment를 모아서 한 번에 처리, 파일당 하나의 Commit 생성
- **답변 언어 매칭**: Reviewer가 한국어로 작성하면 한국어로 답변
- **중복 방지**: 이전에 처리한 Comment나 이미 답변이 달린 Comment는 Skip

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
2. **Comment 수집 및 필터링** - 처리 불필요한 Comment Skip
3. **파일별 그룹화** - 같은 파일의 Comment를 모아서 분석
4. **분류 및 Fix** - Category별 적절한 Action 수행
5. **답변 작성** - 각 Comment Thread에 처리 결과 답변
6. **결과 요약** - 처리/Skip/Deferred Comment 수 보고

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- PR이 존재하는 Branch에서 실행

## 사용 Tool

`Bash`, `Read`, `Edit`, `Write`, `Glob`, `Grep`, `Agent`
