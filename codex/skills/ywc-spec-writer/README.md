# ywc-spec-writer

Project specification writer. `docs/specification/` 디렉토리를 생성하고 유지보수합니다. 개발자와 비개발자 모두 읽을 수 있는 markdown 형식의 사양서를 작성합니다. Program code 없이, 목표·기능·Data Model·User Flow·비기능 요건을 기술합니다.

## 사용 시나리오

- **새 프로젝트**: Specification 이 없는 프로젝트에 전체 사양서를 처음 작성할 때
- **Task 기반 업데이트**: `ywc-task-generator` 로 작성한 단일 task 문서를 사양서에 반영할 때
- **Task Range / Multi 업데이트**: 여러 task (범위·glob·다중 ID) 를 한 번에 반영할 때
- **PR 기반 업데이트**: 하나 또는 여러 개의 PR diff 와 narrative 로 사양서를 갱신할 때
- **Commit 후 동기화**: Code 변경 후 사양서와 동기화할 때
- **전체 갱신**: 사양서 전체를 최신 상태로 재생성할 때

## 사용 방법

```bash
/ywc-spec-writer                          # 자동 모드 (최근 commit 기반 업데이트)
/ywc-spec-writer --full                   # 전체 사양서 생성 (확인 필요)
/ywc-spec-writer --update                 # 전체 사양서 재생성
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-tasks 000002-010..000003-020   # Task range (phase 경계 가능)
/ywc-spec-writer --from-tasks 000002-* 000003-010      # Glob + 단일 ID 혼합
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --from-pr 42                          # 단일 PR
/ywc-spec-writer --from-prs 42 43 51                   # 여러 PR (union diff)
/ywc-spec-writer --setup-hook             # Git hook 설치
/ywc-spec-writer --lang ja                # 일본어로 작성
```

## 입력

- (선택) `--full` / `--update` — 전체 생성 또는 갱신
- (선택) `--from-task <path>` — 단일 task 디렉토리 경로
- (선택) `--from-tasks <id-or-pattern> ...` — Task range / glob / 다중 ID (active + completed 모두 탐색)
- (선택) `--from-commit <ref>` — commit 참조 (기본: `HEAD`)
- (선택) `--from-pr <num>` — 단일 PR (gh CLI 필요)
- (선택) `--from-prs <num> ...` — 다중 PR union diff (중복 file 자동 dedup)
- (선택) `--lang ko|ja|en` — 출력 언어 (기본: `ko`)
- (선택) `--setup-hook` — Git pre-commit hook 설치

> `--from-pr` / `--from-prs` 사용 시 `gh` CLI 가 설치·인증되어 있어야 합니다. PR title / body / `headRefOid` 는 spec 작성 시 narrative context 와 audit trail 로 함께 기록됩니다.

## 출력

```
docs/specification/
├── README.md              # Index + 변경 이력
├── 01-overview.md         # 프로젝트 개요
├── 02-features.md         # 기능 요건 (User Story 형식)
├── 03-data.md             # Data 모델
├── 04-interfaces.md       # 외부 Interface
├── 05-user-flows.md       # User Flow
├── 06-requirements.md     # 비기능 요건
└── 07-glossary.md         # 용어집
```

## 관련 Skill

- `ywc-plan` — 기능 계획을 수립하여 사양서 작성의 input 을 제공
- `ywc-spec-validate` — 작성된 사양서의 품질을 검토
- `ywc-task-generator` — 검토된 사양서를 task 로 분해
- `ywc-ubiquitous-language` — 도메인 용어를 사양서 語彙와 정렬
