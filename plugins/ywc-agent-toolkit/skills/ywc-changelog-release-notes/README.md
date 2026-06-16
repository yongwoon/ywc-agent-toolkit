# ywc-changelog-release-notes

Git History, Merged PR, 또는 `ywc-release-pr-list` 출력을 기반으로
CHANGELOG.md 항목과 User 대상 Release Notes를 생성하는 Skill입니다.
Keep a Changelog 형식의 기술 문서와 비기술 User 대상 릴리즈 노트를 구분하여 생성합니다.

## 핵심 개념: 두 가지 출력물

이 Skill은 **목적이 다른 두 가지 문서**를 생성합니다.

| | CHANGELOG.md | Release Notes |
|---|---|---|
| 독자 | 개발자, 유지보수자 | 최종 사용자, 고객 |
| 포함 내용 | 모든 변경사항, CVE, PR 번호 | 사용자 눈에 보이는 변경만 |
| 어조 | 기술적, 간결 | 평이한 언어, 혜택 중심 |
| refactor/chore | 포함 | 제외 |

## 실제 사용 시나리오

### Case 1: 신규 버전 릴리즈 전 (가장 일반적)

```
/ywc-changelog-release-notes --both --version 1.2.0
```

개발자용 CHANGELOG.md와 사용자용 Release Notes를 한 번에 생성합니다.
GitHub Release 페이지에 올릴 내용이 필요할 때 사용합니다.

### Case 2: CHANGELOG.md만 업데이트할 때

```
/ywc-changelog-release-notes --changelog
```

외부 사용자가 없는 내부 팀 운영 프로젝트처럼, 개발자용 변경이력만 필요할 때 사용합니다.
`git tag`를 찍기 전에 실행합니다.

### Case 3: 고객 공지문이나 Slack 공지 작성

```
/ywc-changelog-release-notes --release
```

"v1.3.0 출시됐습니다" 같은 사용자 대상 공지를 작성할 때 사용합니다.
기술적 내용은 자동으로 걸러지고, 사용자 관점의 문장으로 변환됩니다.

### Case 4: 내용 먼저 확인 후 파일 수정

```
/ywc-changelog-release-notes --dry-run
```

실제로 `CHANGELOG.md`를 수정하기 전에 어떤 내용이 들어갈지 확인할 때 사용합니다.
내용 검토 후 문제 없으면 `--dry-run` 없이 다시 실행합니다.

### Case 5: `ywc-release-pr-list`와 연계할 때

PR 목록을 먼저 정리한 경우, 그 결과를 이 Skill의 Input으로 활용할 수 있습니다.

```
/ywc-release-pr-list > pr-list.md
/ywc-changelog-release-notes --both --pr-list pr-list.md --version 1.2.0
```

`ywc-release-pr-list`는 PR을 테이블로 나열하고, 이 Skill은 그것을 읽기 좋은 CHANGELOG 항목으로 **포맷팅**합니다.

## 사용 방법 (전체 Flag)

```
/ywc-changelog-release-notes --changelog              # CHANGELOG.md 항목만 생성
/ywc-changelog-release-notes --release                # User 대상 Release Notes만 생성
/ywc-changelog-release-notes --both --version 1.2.0  # 두 문서 모두 생성
/ywc-changelog-release-notes --from v1.1.0 --to HEAD # 특정 범위 지정
/ywc-changelog-release-notes --dry-run               # 파일 수정 없이 출력만
```

## 전형적인 릴리즈 흐름

```
1. ywc-release-pr-list          → 이번 릴리즈에 포함된 PR 목록 확인
2. ywc-changelog-release-notes  → CHANGELOG + Release Notes 생성
3. ywc-commit                   → CHANGELOG.md 변경사항 커밋
4. ywc-create-pr                → Release PR 생성
5. git tag -a v1.2.0 -m "..."   → 태그 (Skill이 명령어를 제안해줌)
```

## 관련 Skill

- `ywc-release-pr-list` — PR 목록 정리 (이 Skill의 input으로 사용 가능)
- `ywc-commit` — CHANGELOG.md 변경 후 Commit
- `ywc-create-pr` — Release PR 생성
- `ywc-incident-postmortem` — Patch Release의 원인이 된 장애 회고

## Localized Versions

- [English](README.en.md)
- [日本語](README.ja.md)
- [한국어](README.ko.md)
