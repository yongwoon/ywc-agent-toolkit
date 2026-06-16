# Release PR List

Release PR에 포함된 PR 목록을 추출하여 Author별로 정리하고, PR Description을 업데이트하는 Codex Skill입니다.

## 개요

`develop` → `main` 같은 Release PR을 만들 때, 포함된 개별 PR과 Author를 자동으로 정리합니다. Commit Headline에서 PR 번호를 추출하고, 각 PR의 Author를 조회하여 그룹화한 목록을 PR Description의 `## PR LIST` 섹션에 작성합니다.

### 주요 특징

- **자동 PR 추출**: Commit Headline의 `#<number>` 패턴에서 PR 번호 추출
- **Author별 그룹화**: PR을 Author Login 기준으로 알파벳순 정렬
- **선택적 PR Summary**: 실행 시 사용자에게 PR 별 한 줄 적용 내용을 추가할지 물어보고, 동의한 경우에만 PR Title을 기반으로 간단한 Summary를 항목 옆에 기록
- **기존 Description 보존**: `## PR LIST` 섹션만 추가/교체, 나머지는 그대로 유지
- **멱등성**: 여러 번 실행해도 PR LIST 섹션만 갱신

## 사용 방법

### 기본 사용

```
/release-pr-list 301
```

PR 번호는 필수 입력입니다.

### 자연어 호출

```
"Release PR 301의 PR 목록을 정리해줘"
```

## Output 예시

Summary 없이 진행한 경우 (기본 응답):

```markdown
## PR LIST

- #123 @alice
- #145 @alice
- #130 @bob
- #142 @charlie
```

Summary 추가에 동의한 경우, 각 항목 옆에 PR Title 기반의 한 줄 요약이 함께 기록됩니다:

```markdown
## PR LIST

- #123 @alice — Add OAuth login flow with Google provider
- #145 @alice — Fix pagination off-by-one on user list
- #130 @bob — Refactor database connection pool for reuse
- #142 @charlie — Update release notes Template
```

## 실행 흐름

1. **PR 번호 확인** - `$ARGUMENTS`에서 PR 번호 추출 및 검증
2. **Summary 추가 여부 질의** - "PR 별 한 줄 적용 내용을 함께 기록할까요?" 라고 사용자에게 한 번 묻고 응답을 기억
3. **Commit Headline 수집** - Release PR의 모든 Commit에서 Headline 추출
4. **PR 번호 추출** - `#<number>` 패턴 매칭, 중복 제거, 정렬
5. **Author (필요 시 Summary) 조회** - 각 PR의 Author Login을 `gh` CLI로 조회. Summary 모드인 경우 Title을 함께 가져와 정리
6. **그룹화 및 정렬** - Author별 알파벳순 그룹화
7. **PR Description 갱신** - `## PR LIST` 섹션 추가 또는 교체

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- Release PR이 이미 생성되어 있어야 함

## 사용 Tool

`Bash`, `Read`, `Glob`, `Grep`
