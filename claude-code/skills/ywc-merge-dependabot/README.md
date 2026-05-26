# Merge Dependabot Skill

## 개요

**merge-dependabot** Skill은 Dependabot이 생성한 Pull Request를 안전하게 일괄 Merge하는 Claude Code Skill입니다.

**주요 기능:**

- Dependabot PR 자동 탐지 및 일괄 Merge
- Security 관련 PR만 선별 Merge하는 모드 지원
- Pre-Merge 안전 검증 (Dockerfile, Major Version, CI Status)
- Merge Conflict 자동 해결 시도
- PR 번호 오름차순 순차 처리 (이전 Merge가 이후 PR에 미치는 영향 고려)
- **Parallel-auto Mode** — 다수 PR 처리 시 lockfile ecosystem 별로 grouping 한 뒤 GitHub auto-merge queue 에 위임하여 wall-clock 시간을 단축
- 처리 결과 Summary Report 자동 생성

**사용 대상:**

- Dependabot PR이 누적되어 일괄 처리가 필요한 프로젝트
- Security 업데이트를 우선적으로 반영해야 하는 팀
- Dependency 업데이트 Workflow를 자동화하고 싶은 개발자

---

## 사용 방법

### Skill 호출

Claude Code에서 다음과 같이 호출합니다:

```
# 전체 Dependabot PR Merge (sequential, default)
/ywc-merge-dependabot

# Security 관련 PR만 Merge (sequential)
/ywc-merge-dependabot security

# 전체 PR 을 ecosystem 별 parallel-auto queue 로 처리
/ywc-merge-dependabot parallel-auto

# Security PR 만 parallel-auto 로 처리
/ywc-merge-dependabot security parallel-auto
```

또는 자연어로:

```
User: dependabot이 만든 PR들을 merge해줘
User: dependabot security PR만 merge해줘
User: dependabot PR 이 많으니 parallel-auto 로 빠르게 처리해줘
```

### 전제 조건

- GitHub CLI (`gh`) 설치 및 인증 완료
- Repository에 대한 Merge 권한 보유
- Dependabot이 설정되어 PR이 존재하는 상태

---

## Mode 설명

본 Skill 은 두 축의 직교 Flag 를 지원합니다.

- **Scope flag** — 어떤 PR 을 대상으로 할지 결정 (`security` 또는 기본 = 전체)
- **Execution flag** — 어떻게 처리할지 결정 (`parallel-auto` 또는 기본 = sequential)

### 1. All Mode (기본 Scope, 기본 Execution)

모든 Dependabot PR 을 순차적으로 Merge 합니다.

```
/ywc-merge-dependabot
```

### 2. Security Mode (Scope: security)

Security 관련 PR 만 선별하여 Merge 합니다. 다음 조건으로 Security PR 을 식별합니다:

- `security` Label 이 있는 PR
- Title 또는 Body 에 "security advisory", "CVE-", "GHSA-", "vulnerability" 포함
- Dependabot Security Advisory Metadata 가 Body 에 존재

```
/ywc-merge-dependabot security
```

### 3. Parallel-Auto Mode (Execution: parallel-auto)

다수 PR (≥ 5) 이 여러 ecosystem 에 걸쳐 누적되어 wall-clock CI 대기가 병목인 경우 사용합니다. 동작 방식:

1. 모든 eligible PR 을 `npm`, `github-actions`, `python`, `go`, `cargo`, `maven`, `gradle`, `docker` group 으로 분류 (`scripts/group-by-ecosystem.py` 사용)
2. 각 PR 에 대해 `gh pr merge --auto` 로 auto-merge 예약
3. GitHub Server 측에서 동일 ecosystem 은 직렬 merge, 서로 다른 ecosystem 은 병렬 merge 수행
4. Client 는 polling 으로 queue 상태 추적 (최대 30분)
5. Mixed-ecosystem PR (둘 이상의 lockfile 을 동시 변경) 은 마지막에 sequential pass 로 처리

**전제조건:** Repository 에 "Allow auto-merge" 설정이 활성화되어 있어야 합니다. 비활성 상태에서는 sequential mode 로 자동 fallback 됩니다.

```
/ywc-merge-dependabot parallel-auto
/ywc-merge-dependabot security parallel-auto
```

---

## Pre-Merge 안전 검증

각 PR에 대해 Merge 전 다음 항목을 검증합니다:

| 검증 항목 | Skip 조건 | 사유 |
| --- | --- | --- |
| Dockerfile FROM 변경 | `FROM` Image Version이 변경된 경우 | Container Base Image 변경은 수동 검토 필요 |
| Major Version Upgrade | Major Version이 변경된 경우 (e.g. 2.x → 3.x) | Breaking Change 가능성이 높음 |
| CI Status | Required CI Check가 통과하지 않은 경우 | Build/Test 실패 상태에서 Merge 방지 |

---

## 처리 순서 및 Conflict 해결

### Sequential Mode 의 처리 순서

PR 번호 **오름차순**으로 하나씩 처리합니다. 이전 PR 의 Merge 가 이후 PR 에 Conflict 를 발생시킬 수 있으므로, 순차 처리가 필수적입니다.

### Parallel-Auto Mode 의 처리 순서

`parallel-auto` 사용 시에는 client 가 순서를 강제하지 않고 GitHub auto-merge queue 에 위임합니다.

- **Within-ecosystem**: 동일 ecosystem (예: 모든 npm PR) 내에서는 lockfile 충돌이 발생하므로 GitHub 가 자동으로 직렬화. 한 PR 이 merge 되면 나머지가 Dependabot 에 의해 rebase 되어 다시 CI 실행
- **Across-ecosystem**: 서로 다른 ecosystem (예: npm vs github-actions) 의 PR 은 충돌하지 않으므로 GitHub 가 병렬 처리
- **Mixed bucket**: 두 ecosystem 의 lockfile 을 동시에 변경하는 PR 은 별도 격리되어 모든 parallel queue 가 비워진 뒤 sequential 로 처리

### Conflict 해결 Flow

```
Merge 시도
├── 성공 → ✅ Merged
└── Conflict 발생
    ├── Branch Checkout → Conflict 해결 → Push → CI 재실행
    │   ├── CI 통과 → Merge → ✅ Merged
    │   └── CI 실패 → ❌ Failed
    └── 자동 해결 불가 → ❌ Failed
```

---

## 결과 Report 형식

처리 완료 후 다음 형식으로 결과를 출력합니다:

```
## Dependabot Merge Results

- ✅ Merged: #123 Bump axios from 1.6.0 to 1.7.2
- ✅ Merged: #125 Bump lodash from 4.17.20 to 4.17.21
- ⏭️ Skipped (Dockerfile): #127 Bump node from 18 to 20
- ⏭️ Skipped (Major version upgrade): #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed: #132 Bump express from 4.18.0 to 4.19.2 — conflict caused by #125 merge

Total: 2 merged / 2 skipped / 1 failed
```

---

## 파일 구조

```
ywc-merge-dependabot/
├── README.md                          # 이 파일 (Skill 사용 Guide, 한국어 primary)
├── README.en.md / .ja.md / .ko.md     # Locale entry
├── SKILL.md                           # Skill 정의 및 상세 지침
└── scripts/
    └── group-by-ecosystem.py          # PR 번호 → lockfile ecosystem grouping (parallel-auto mode 전용)
```

---

## 사용 예시

### Example 1: 전체 Dependabot PR Merge

```
User: dependabot PR 을 merge 해줘

Claude: Dependabot PR 목록을 확인합니다.

[gh pr list --author "app/dependabot" 실행]

8개의 Dependabot PR을 발견했습니다.
- 6개: Minor/Patch Version Upgrade
- 1개: Dockerfile FROM 변경 (Skip 대상)
- 1개: Major Version Upgrade (Skip 대상)

6개 PR을 PR 번호 오름차순으로 Merge를 진행합니다.

[순차 처리 수행]

## Dependabot Merge Results
- ✅ Merged: #201 Bump express from 4.18.0 to 4.18.2
- ✅ Merged: #203 Bump lodash from 4.17.20 to 4.17.21
...
```

### Example 2: Security PR만 선별 Merge

```
User: dependabot security 관련 PR만 merge 해줘

Claude: Security 관련 Dependabot PR을 필터링합니다.

[PR 목록 조회 및 Security 필터 적용]

3개의 Security 관련 PR을 발견했습니다.
- #210: CVE-2024-1234 관련 axios 업데이트
- #215: GHSA-xxxx 관련 jsonwebtoken 업데이트
- #218: Security advisory 관련 helmet 업데이트

순차 처리를 시작합니다.
```

### Example 3: Parallel-Auto Mode 로 대량 PR 처리

```
User: dependabot PR 이 12개 누적되어 있어. parallel-auto 로 빠르게 처리해줘.

Claude: 12개의 Dependabot PR 을 발견했습니다.
Pre-merge check 와 ecosystem grouping 을 수행합니다.

Ecosystem grouping (10 PRs eligible, 2 skipped):
  - npm:            #301, #305, #308, #312
  - github-actions: #302, #309
  - python:         #304, #310
  - go:             #306, #311
  - mixed:          (none)

GitHub auto-merge queue 에 10개 PR 을 예약했습니다. CI 완료 대기 중...

## Dependabot Merge Results
Mode: parallel-auto
Ecosystem groups processed: npm (4), github-actions (2), python (2), go (2)

- ✅ Merged (npm)            : #301, #305, #308, #312
- ✅ Merged (github-actions) : #302, #309
- ✅ Merged (python)         : #304, #310
- ✅ Merged (go)             : #306, #311
- ⏭️ Skipped (Major version) : #307
- ⏭️ Skipped (Dockerfile)    : #303

Total: 10 merged / 2 skipped / 0 failed
```

---

## Error Handling

| Error | 대응 방법 |
| --- | --- |
| `gh` CLI 미인증 | `gh auth login` 실행 안내 |
| Dependabot PR 없음 | "No Dependabot PRs found" 보고 후 종료 |
| Rate Limit | 대기 후 재시도 또는 진행 상황 보고 후 종료 |
| Branch Protection | 해당 PR Skip 후 Protection Rule 안내 |
| PR 20개 초과 | 사용자 확인 후 진행 |

---

## Best Practices

### 1. Dependabot.yml과 함께 사용

Dependabot이 PR을 자동 생성하도록 설정한 뒤, 이 Skill로 주기적으로 일괄 Merge하면 효과적입니다:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 2. Security PR 우선 처리

보안 취약점은 빠른 대응이 중요합니다. Security Mode 를 활용하여 Security PR 을 먼저 Merge 한 뒤, 나머지를 처리하세요:

```
/ywc-merge-dependabot security    # Security PR 먼저
/ywc-merge-dependabot             # 나머지 PR 처리
```

### 3. Major Version Upgrade 는 수동 검토

Major Version Upgrade 는 Breaking Change 가능성이 높으므로, Skill 이 자동 Skip 합니다. Skip 된 PR 은 수동으로 검토 후 개별 Merge 하세요.

### 4. 대량 PR 처리 시 Parallel-Auto 활용

5개 이상의 Dependabot PR 이 여러 ecosystem 에 걸쳐 누적되어 있다면 `parallel-auto` 를 사용하세요. Sequential mode 는 N 개의 CI cycle 을 직렬로 대기하지만, parallel-auto 는 GitHub 의 auto-merge queue 가 서로 다른 ecosystem 을 동시에 처리하므로 wall-clock 시간이 크게 단축됩니다:

```
/ywc-merge-dependabot parallel-auto                # 전체 PR 을 parallel-auto 로
/ywc-merge-dependabot security parallel-auto       # Security PR 만 parallel-auto 로
```

다만 다음 경우에는 sequential mode 가 더 적합합니다:

- Branch protection 이 엄격하여 auto-merge 가 비활성화된 경우
- PR 이 5개 미만이거나 모두 단일 ecosystem 에 속하는 경우 (병렬화 이득이 없음)
- Conflict 가 빈번하여 client 측에서 즉시 resolve 해야 하는 경우

---

## Troubleshooting

### Q: CI가 통과했는데 Merge가 안 됩니다

**A**: Branch Protection Rule에서 추가 조건 (예: Required Reviewers)이 설정되어 있을 수 있습니다. Repository Settings에서 Branch Protection을 확인하세요.

### Q: Security PR인데 필터링되지 않습니다

**A**: Security PR 식별은 Label, Title/Body 키워드 기반입니다. Dependabot이 `security` Label을 붙이지 않는 경우, Title에 "CVE-" 또는 "GHSA-" 키워드가 포함되어야 합니다.

### Q: Conflict 해결 후에도 Merge가 실패합니다

**A**: Conflict 해결 후 CI가 재실행되며, CI가 실패하면 Merge도 실패합니다. CI 실패 원인을 확인하고 수동으로 대응하세요.

### Q: Parallel-auto 를 호출했는데 sequential 로 fallback 되었습니다

**A**: Repository 의 "Allow auto-merge" 설정이 비활성화되어 있는 경우 자동 fallback 됩니다. Settings → General → Pull Requests → "Allow auto-merge" 를 활성화한 뒤 재시도하세요.

### Q: Parallel-auto Queue 에서 일부 PR 이 `queue stalled` 로 보고됩니다

**A**: 30분 polling window 내에 GitHub 가 merge 를 완료하지 못한 경우입니다. 주된 원인은 (1) Conflict 발생 후 `@dependabot rebase` 가 timeout 이내에 처리되지 않음, (2) Required reviewer 미배정, (3) 동일 ecosystem 내 선행 PR 의 CI 지연. 해당 PR 의 상태를 직접 확인한 뒤 필요 시 `@dependabot rebase` Comment 를 추가하고 skill 을 재실행하세요.

### Q: Mixed bucket 에 어떤 PR 이 분류되나요

**A**: 단일 PR 이 둘 이상의 ecosystem marker 를 동시에 변경하는 경우 (예: monorepo 에서 `package-lock.json` 과 `pyproject.toml` 을 동시 갱신) 또는 인식 가능한 marker 가 없는 경우입니다. 이러한 PR 은 parallel queue 가 모두 완료된 뒤 sequential 로 처리되어 hidden conflict 위험을 차단합니다.

---

## 관련 문서

### 프로젝트 내부 참조

- [GitHub Actions CI Workflow](../../../../prompts/development/github-action.md) — Dependabot.yml 설정 포함

### 외부 참조

- [GitHub Dependabot 공식 문서](https://docs.github.com/en/code-security/dependabot)
- [GitHub CLI (gh) 공식 문서](https://cli.github.com/manual/)

---

## 버전 정보

- **마지막 업데이트**: 2026-05-26 (parallel-auto mode 추가)
- **Skill Version**: 1.1
- **호환 환경**: Claude Code, Codex CLI

---

## License

이 Skill은 `develop-with-llm` 프로젝트의 일부로, 학습 및 참고 목적으로 제공됩니다.
