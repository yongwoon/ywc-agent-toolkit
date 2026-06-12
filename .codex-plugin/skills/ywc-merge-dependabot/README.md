# Merge Dependabot Skill (Codex)

## 개요

Dependabot이 생성한 Pull Request를 안전하게 일괄 Merge하는 Skill입니다.
Claude Code와 Codex CLI 모두에서 사용할 수 있습니다.

## 주요 기능

- 전체 Dependabot PR Merge 또는 Security PR만 선별 Merge
- Pre-Merge 안전 검증 (Dockerfile FROM 변경, Major Version Upgrade, CI Status)
- Merge Conflict 자동 해결 시도 및 CI 재실행
- PR 번호 오름차순 순차 처리 (이전 Merge 영향 고려)
- **Parallel-auto mode**: lockfile ecosystem 별 lane 을 만들고 lane 별로 한 PR 만 active auto-merge 상태로 유지하여 대량 PR 의 wall-clock 시간을 단축
- 처리 결과 Summary Report 자동 생성

## 사용 방법

### Claude Code

```
/ywc-merge-dependabot                          # 전체 PR sequential 처리
/ywc-merge-dependabot security                 # Security PR 만 sequential 처리
/ywc-merge-dependabot parallel-auto            # 전체 PR ecosystem-lane auto-merge
/ywc-merge-dependabot security parallel-auto   # Security PR 만 ecosystem-lane auto-merge
```

### Codex CLI

```
Use $ywc-merge-dependabot to merge all open Dependabot pull requests.
Use $ywc-merge-dependabot security to merge only security-related Dependabot PRs.
Use $ywc-merge-dependabot parallel-auto to merge a large batch via ecosystem-lane auto-merge scheduling.
Use $ywc-merge-dependabot security parallel-auto to combine the security scope with the parallel-auto execution flag.
```

## 전제 조건

- GitHub CLI (`gh`) 설치 및 인증 완료
- Repository에 대한 Merge 권한 보유

## Mode

본 Skill 은 두 축의 직교 Flag 를 지원합니다.

**Scope flag** — 처리 대상:

| Token | Scope |
| --- | --- |
| `security` | Security 관련 Dependabot PR 만 |
| (없음) | 모든 Dependabot PR |

**Execution flag** — 처리 방식:

| Token | Execution | 사용 시점 |
| --- | --- | --- |
| `parallel-auto` | Ecosystem 별 lane 구성 + lane 별 active auto-merge 1개 유지 | 여러 ecosystem 에 걸쳐 5개 이상의 PR 이 누적된 경우 |
| (없음) | Sequential (PR 번호 오름차순) | 소량 batch 또는 strict branch protection 환경 |

**전제조건 (parallel-auto):** Repository 에 "Allow auto-merge" 설정이 활성화되어 있어야 합니다. 비활성 상태에서는 sequential 로 자동 fallback 됩니다.

## Skip 조건

| 조건 | 사유 |
| --- | --- |
| Dockerfile `FROM` 변경 | Container Base Image 변경은 수동 검토 필요 |
| Major Version Upgrade | Breaking Change 가능성 |
| CI 미통과 | Build/Test 실패 상태에서 Merge 방지 |

## 결과 Report 형식

```
Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2)

- ✅ Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- ⏭️ Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- ⏭️ Skipped   (Major version)  : #130 Bump webpack from 4.x to 5.x
- ❌ Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 — CONFLICTING after 30 min
```

Sequential mode 에서는 `Ecosystem groups` 헤더와 PR 라인의 ecosystem annotation 만 생략하고, `Mode` 라인은 출력합니다.

## 파일 구조

```
ywc-merge-dependabot/
├── README.md                          # 이 파일
├── README.en.md / .ja.md / .ko.md     # Locale entry
├── SKILL.md                           # Skill 정의 및 상세 지침
├── agents/
│   └── openai.yaml                    # Codex CLI Agent 설정
└── scripts/
    └── group-by-ecosystem.py          # PR → lockfile ecosystem 분류 (parallel-auto mode 전용)
```

## 관련 Skill

- [ywc-create-pr](../ywc-create-pr/SKILL.md) — PR 생성
- [ywc-handle-pr-reviews](../ywc-handle-pr-reviews/SKILL.md) — PR Review Comment 처리
- [ywc-release-pr-list](../ywc-release-pr-list/SKILL.md) — Release PR List 생성
