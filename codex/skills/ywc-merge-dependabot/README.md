# Merge Dependabot Skill

## 개요

**merge-dependabot** Skill은 Dependabot이 생성한 Pull Request를 안전하게 일괄 Merge하는 Codex Skill입니다.

**주요 기능:**

- Dependabot PR 자동 탐지 및 일괄 Merge
- Security 관련 PR만 선별 Merge하는 모드 지원
- Pre-Merge 안전 검증 (Dockerfile, Major Version, CI Status)
- Merge Conflict 자동 해결 시도
- PR 번호 오름차순 순차 처리 (이전 Merge가 이후 PR에 미치는 영향 고려)
- 처리 결과 Summary Report 자동 생성

**사용 대상:**

- Dependabot PR이 누적되어 일괄 처리가 필요한 프로젝트
- Security 업데이트를 우선적으로 반영해야 하는 팀
- Dependency 업데이트 Workflow를 자동화하고 싶은 개발자

---

## 사용 방법

### Skill 호출

Codex에서 다음과 같이 호출합니다:

```
# 전체 Dependabot PR Merge
/merge-dependabot

# Security 관련 PR만 Merge
/merge-dependabot security
```

또는 자연어로:

```
User: dependabot이 만든 PR들을 merge해줘
User: dependabot security PR만 merge해줘
```

### 전제 조건

- GitHub CLI (`gh`) 설치 및 인증 완료
- Repository에 대한 Merge 권한 보유
- Dependabot이 설정되어 PR이 존재하는 상태

---

## Mode 설명

### 1. All Mode (기본)

모든 Dependabot PR을 대상으로 Merge합니다.

```
/merge-dependabot
```

### 2. Security Mode

Security 관련 PR만 선별하여 Merge합니다. 다음 조건으로 Security PR을 식별합니다:

- `security` Label이 있는 PR
- Title 또는 Body에 "security advisory", "CVE-", "GHSA-", "vulnerability" 포함
- Dependabot Security Advisory Metadata가 Body에 존재

```
/merge-dependabot security
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

### 순차 처리

PR 번호 **오름차순**으로 하나씩 처리합니다. 이전 PR의 Merge가 이후 PR에 Conflict를 발생시킬 수 있으므로, 순차 처리가 필수적입니다.

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
merge-dependabot/
├── README.md    # 이 파일 (Skill 사용 Guide)
└── SKILL.md     # Skill 정의 및 상세 지침
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

보안 취약점은 빠른 대응이 중요합니다. Security Mode를 활용하여 Security PR을 먼저 Merge한 뒤, 나머지를 처리하세요:

```
/merge-dependabot security    # Security PR 먼저
/merge-dependabot             # 나머지 PR 처리
```

### 3. Major Version Upgrade는 수동 검토

Major Version Upgrade는 Breaking Change 가능성이 높으므로, Skill이 자동 Skip합니다. Skip된 PR은 수동으로 검토 후 개별 Merge하세요.

---

## Troubleshooting

### Q: CI가 통과했는데 Merge가 안 됩니다

**A**: Branch Protection Rule에서 추가 조건 (예: Required Reviewers)이 설정되어 있을 수 있습니다. Repository Settings에서 Branch Protection을 확인하세요.

### Q: Security PR인데 필터링되지 않습니다

**A**: Security PR 식별은 Label, Title/Body 키워드 기반입니다. Dependabot이 `security` Label을 붙이지 않는 경우, Title에 "CVE-" 또는 "GHSA-" 키워드가 포함되어야 합니다.

### Q: Conflict 해결 후에도 Merge가 실패합니다

**A**: Conflict 해결 후 CI가 재실행되며, CI가 실패하면 Merge도 실패합니다. CI 실패 원인을 확인하고 수동으로 대응하세요.

---

## 관련 문서

### 프로젝트 내부 참조

- [Dependabot PR Merge Prompt](../../../prompts/development/merge-dependabot-pr-list.md) - 원본 Prompt 문서
- [GitHub Actions CI Workflow](../../../prompts/development/github-action.md) - Dependabot.yml 설정 포함

### 외부 참조

- [GitHub Dependabot 공식 문서](https://docs.github.com/en/code-security/dependabot)
- [GitHub CLI (gh) 공식 문서](https://cli.github.com/manual/)

---

## 버전 정보

- **마지막 업데이트**: 2026-03-26
- **Skill Version**: 1.0
- **호환 환경**: Codex CLI

---

## License

이 Skill은 `develop-with-llm` 프로젝트의 일부로, 학습 및 참고 목적으로 제공됩니다.
