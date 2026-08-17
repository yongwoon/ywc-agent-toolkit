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
- **PR 언어 지원**: `--lang` / `--language`로 PR title/body prose를 `en`, `ja`, `ko`, `zh`, `es` 중 하나로 작성하며, task ID, branch name, file path, command, label, 명시적 `--title` 값은 그대로 유지
- **관련 설계 문서 인용**: branch에 대응하는 task의 `## Spec Reference`를 우선 확인하고, 없으면 `docs/ywc-plans/` 하위 plan을 best-effort로 탐색해 PR 본문에 설계 배경을 append

## 사용 방법

### 기본 사용

```
$ywc-create-pr
```

### Base Branch 지정

```
$ywc-create-pr main
```

### CI Check Skip

```
$ywc-create-pr --skip-ci-check
$ywc-create-pr main --skip-ci-check
$ywc-create-pr --lang zh
$ywc-create-pr --language spanish
$ywc-create-pr --plan-doc docs/ywc-plans/20260814-small_example.md
$ywc-create-pr --no-plan-ref
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
