# ywc-spec-writer

Project specification writer. `docs/specification/` 디렉토리를 생성하고 유지보수합니다. 개발자와 비개발자 모두 읽을 수 있는 markdown 형식의 사양서를 작성합니다. Program code 없이, 목표·기능·Data Model·User Flow·비기능 요건을 기술합니다.

## 사용 시나리오

- **새 프로젝트**: Specification 이 없는 프로젝트에 전체 사양서를 처음 작성할 때
- **Task 기반 업데이트**: `ywc-task-generator` 로 작성한 task 문서를 사양서에 반영할 때
- **Commit 후 동기화**: Code 변경 후 사양서와 동기화할 때
- **전체 갱신**: 사양서 전체를 최신 상태로 재생성할 때

## 사용 방법

```bash
/ywc-spec-writer                          # 자동 모드 (최근 commit 기반 업데이트)
/ywc-spec-writer --full                   # 전체 사양서 생성 (확인 필요)
/ywc-spec-writer --update                 # 전체 사양서 재생성
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --setup-hook             # Git hook 설치
/ywc-spec-writer --lang ja                # 일본어로 작성
```

## 입력

- (선택) `--full` / `--update` — 전체 생성 또는 갱신
- (선택) `--from-task <path>` — task 디렉토리 경로
- (선택) `--from-commit <ref>` — commit 참조 (기본: `HEAD`)
- (선택) `--lang ko|ja|en` — 출력 언어 (기본: `ko`)
- (선택) `--setup-hook` — Git pre-commit hook 설치

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
