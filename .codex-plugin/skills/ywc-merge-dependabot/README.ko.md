# Merge Dependabot Skill (Codex)

## 개요

Dependabot이 생성한 Pull Request를 안전하게 일괄 Merge하는 Skill입니다.
Claude Code와 Codex CLI 모두에서 사용할 수 있습니다.

## 주요 기능

- 전체 Dependabot PR 또는 Security 관련 PR만 선별 Merge
- Dockerfile `FROM` 변경, Major Version Upgrade, CI Status pre-merge check
- Merge conflict 해결 시도 및 CI 재실행 대기
- 기본값은 PR 번호 오름차순 sequential 처리
- **Parallel-auto mode**: lockfile ecosystem 별 lane 을 만들고 lane 별로 한 PR 만 active auto-merge 상태로 유지하여 대량 PR의 wall-clock 시간을 단축
- 최종 Summary Report 출력

## 사용 방법

### Claude Code

```text
/ywc-merge-dependabot                          # 전체 PR sequential 처리
/ywc-merge-dependabot security                 # Security PR만 sequential 처리
/ywc-merge-dependabot parallel-auto            # 전체 PR ecosystem-lane auto-merge
/ywc-merge-dependabot security parallel-auto   # Security PR만 ecosystem-lane auto-merge
```

### Codex CLI

```text
Use $ywc-merge-dependabot to merge all open Dependabot pull requests.
Use $ywc-merge-dependabot security to merge only security-related Dependabot PRs.
Use $ywc-merge-dependabot parallel-auto to merge a large batch via ecosystem-lane auto-merge scheduling.
Use $ywc-merge-dependabot security parallel-auto to combine the security scope with the parallel-auto execution flag.
```

## 전제 조건

- GitHub CLI (`gh`) 설치 및 인증 완료
- 대상 repository에 대한 Merge 권한 보유
- `parallel-auto` 사용 시 repository의 "Allow auto-merge" 설정 활성화. 비활성 상태에서는 sequential mode로 fallback 됩니다.

## Mode

본 Skill은 두 축의 직교 flag를 지원합니다.

**Scope flag** — 처리 대상:

| Token | Scope |
| --- | --- |
| `security` | Security 관련 Dependabot PR만 |
| _(없음)_ | 모든 Dependabot PR |

**Execution flag** — 처리 방식:

| Token | Execution | 사용 시점 |
| --- | --- | --- |
| `parallel-auto` | Ecosystem lane + lane 별 active auto-merge PR 1개 유지 | 여러 ecosystem에 걸쳐 5개 이상의 PR이 누적된 경우 |
| _(없음)_ | PR 번호 오름차순 sequential 처리 | 소량 batch 또는 strict branch protection 환경 |

## Skip 조건

| 조건 | 사유 |
| --- | --- |
| Dockerfile `FROM` 변경 | Container base image 변경은 수동 review 필요 |
| Major Version Upgrade | Breaking change risk |
| CI 미통과 | Build/Test 실패 상태에서 Merge 방지 |

## Result Format

```text
Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2)

- Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- Skipped   (Major version)  : #130 Bump webpack from 4.x to 5.x
- Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 - CONFLICTING after 30 min
```

Sequential mode에서도 `Mode` line은 출력하고, `Ecosystem groups` header와 PR line의 ecosystem annotation은 생략합니다.

## 파일 구조

```text
ywc-merge-dependabot/
├── README.md
├── README.en.md / README.ja.md / README.ko.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── group-by-ecosystem.py
```

## 관련 Skill

- [ywc-create-pr](../ywc-create-pr/SKILL.md) — PR 생성
- [ywc-handle-pr-reviews](../ywc-handle-pr-reviews/SKILL.md) — PR review comment 처리
- [ywc-release-pr-list](../ywc-release-pr-list/SKILL.md) — Release PR list 생성
