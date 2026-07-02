# Create PR

변경 사항을 Commit하고 저장소의 PR Template에 따라 Draft PR을 생성하는 Codex Skill입니다.

## 개요

Feature Branch 작업이 완료된 뒤, Commit 생성부터 Draft PR 생성까지의 흐름을 자동화합니다.

### 주요 기능

- `develop` → `main` → `master` 순서로 Base Branch 자동 감지
- `.env`, `*.key`, `*.pem` 등 민감 파일 Security Check
- push 전에 lint, format, typecheck, test 등 CI Check 수행
- `.github/pull_request_template.md`가 있으면 자동 적용
- 모든 PR을 Draft 상태로 생성
- `--lang` / `--language`로 PR title/body prose를 `en`, `ja`, `ko`, `zh`, `es` 중 하나로 작성하며, task ID, branch name, file path, command, label, 명시적 `--title` 값은 그대로 유지

## 사용 방법

```text
$ywc-create-pr
$ywc-create-pr main
$ywc-create-pr --skip-ci-check
$ywc-create-pr main --skip-ci-check
$ywc-create-pr --lang zh
$ywc-create-pr --language spanish
```

자연어 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- Git Repository의 Feature Branch에서 작업 중

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Chinese (Simplified)](./README.zh.md)
- [Spanish](./README.es.md)
