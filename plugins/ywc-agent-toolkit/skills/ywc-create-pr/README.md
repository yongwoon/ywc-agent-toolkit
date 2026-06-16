# Create PR

변경 사항을 Commit하고 PR Template에 따라 Draft PR을 생성하는 Codex Skill입니다.

## 개요

Feature Branch에서 작업이 완료된 후, 변경 사항 Commit부터 Draft PR 생성까지의 과정을 자동화합니다. PR Template이 있으면 해당 구조를 따르고, 없으면 기본 구조(Summary, Changes, Test Plan)로 PR을 생성합니다.

### 주요 특징

- **Base Branch 자동 감지**: `develop` → `main` → `master` 순으로 자동 결정
- **Security Check**: `.env`, `*.key`, `*.pem` 등 민감 파일 감지 및 경고
- **CI Check (Pre-push Validation)**: Push 전에 lint, format, typecheck, test 등을 로컬에서 실행하여 CI 실패를 사전에 방지
- **PR Template 지원**: `.github/pull_request_template.md`가 있으면 자동 적용
- **Draft PR 생성**: 모든 PR은 Draft 상태로 생성

## 사용 방법

### 기본 사용

```
/create-pr
```

### Base Branch 지정

```
/create-pr main
```

### CI Check Skip

```
/create-pr --skip-ci-check
/create-pr main --skip-ci-check
```

### 자연어 호출

```
"PR 만들어줘"
"PR 올려줘"
"코드 리뷰 요청해줘"
"push and create PR"
```

## 실행 흐름

1. **Base Branch 결정** - 지정된 Branch 또는 자동 감지
2. **Pre-flight Check** - `gh` CLI 인증 확인, 기존 PR 존재 여부 확인
3. **Security Check** - 민감 파일 스캔 및 경고
4. **Commit** - 변경 사항을 목적별로 분리하여 Commit
5. **CI Check** - lint, format, typecheck, test 실행 (CI 실패 사전 방지)
6. **Push** - Remote에 Push
7. **PR 생성** - Draft PR 생성 및 URL 출력

## 전제 조건

- `gh` CLI 설치 및 인증 완료 (`gh auth login`)
- Git Repository에서 Feature Branch로 작업 중

## 사용 Tool

`Bash`, `Read`, `Glob`, `Grep`
