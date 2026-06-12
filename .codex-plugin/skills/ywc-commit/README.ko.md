# Commit Skill (ywc-commit)

현재 세션에서 작업한 변경 사항을 안전하게 Git commit(및 선택적으로 push)하는 Codex Skill입니다.

## 개요

이 Skill은 다음을 자동으로 처리합니다:

- 세션과 관련된 파일만 선별하여 stage
- 논리적으로 다른 성격의 변경을 별도 commit으로 분리
- 프로젝트의 기존 commit 스타일(type/scope/message)을 `git log`에서 학습하여 일관된 메시지 작성
- commit 결과 요약 보고

## 사용 방법

자연어로 다음과 같이 요청합니다:

```text
/ywc-commit
```

```text
커밋 해줘
```

```text
commit and push
```

```text
지금까지 한 작업 커밋푸쉬 ㄱㄱ
```

```text
authentication 관련 파일만 commit해줘
```

## 주요 규칙

| 규칙 | 내용 |
| --- | --- |
| 세션 관련 파일만 stage | 이번 대화에서 수정/생성/논의된 파일만 대상 |
| 논리 단위로 commit 분리 | 한 commit = 한 목적 |
| push는 명시적 요청 시만 | "push", "푸쉬", "올려줘" 등이 포함된 경우만 실행 |
| `--no-verify` 금지 | Hook 실패 시 원인 수정 또는 사용자에게 보고 |
| `git add .` 금지 | 항상 파일 경로를 명시하여 stage |
| main/master 직접 commit 전 확인 | 거의 항상 실수이므로 먼저 확인 |
| 비밀값·산출물 제외 | `.env*`, `dist/`, `build/` 등은 의도한 경우가 아니면 제외 |
| 도구 전용 co-author trailer 기본 금지 | 저장소 관례 또는 사용자 명시 요청이 있을 때만 포함 |

## Workflow

```text
Step 0: Arguments 파싱
  └─ --skip-ubiquitous-update 등 caller skill 이 전달한 flag 처리

Step 0.5: Ubiquitous Language Update (조건부 자동 ON)
  └─ docs/ubiquitous-language.md 존재 시 ywc-ubiquitous-language --mode update 호출
  └─ 파일이 없으면 silent skip
  └─ --skip-ubiquitous-update flag 있으면 skip (중복 호출 방지)

Step 1: 현재 상태 파악
  └─ git status, git diff, git log (스타일 학습), 브랜치 확인

Step 2: 변경 파일 분류
  └─ IN (세션 관련) / UNKNOWN (출처 불명) / OUT (무관)
  └─ Step 0.5 에서 갱신된 docs/ubiquitous-language.md 는 IN 으로 분류
  └─ UNKNOWN/OUT 있으면 사용자에게 분류 목록 제시 후 승인 요청

Step 3: 논리 단위로 commit 분리
  └─ 성격이 다른 변경은 별도 commit으로 계획
  └─ 필요 시 git add -p로 hunk 단위 stage
  └─ 계획(파일 + 메시지 초안)을 사용자에게 보여주고 승인

Step 4: commit 메시지 작성
  └─ git log에서 프로젝트 스타일 학습 후 동일 형식 적용
  └─ co-author trailer는 저장소 관례 또는 사용자 요청이 있을 때만 포함

Step 5: Stage & Commit
  └─ 명시적 경로로 stage → diff 확인 → heredoc으로 commit

Step 6: 결과 확인
  └─ git log, git status로 누락/잔여 변경 확인

Step 7: Push (요청된 경우만)
  └─ 기본 push, upstream 없으면 -u 플래그 사용
  └─ force-push는 명시적 요청 시만
```

## Arguments

| Flag | Default | 동작 |
| --- | --- | --- |
| `--skip-ubiquitous-update` | off | Step 0.5 (Ubiquitous Language update) skip. ywc-create-pr / ywc-finish-branch 등 caller skill 이 이미 update 를 수행한 경우 전달하여 중복 호출을 방지합니다. |

Direct 호출 (`/ywc-commit`) 시에는 flag 없이도 정상 동작합니다.

## Commit 메시지 형식

프로젝트의 기존 `git log` 스타일을 따릅니다. 일반적인 형식:

```text
<type>(<scope>): <summary>

<body — 필요할 때만>
```

**type 예시** (프로젝트에서 관찰된 것만 사용):
`feat`, `fix`, `refactor`, `perf`, `chore`, `docs`, `test`

**scope**: `git log`에서 관찰된 패턴 사용 (패키지명, 모듈명 등). 여러 영역에 걸치면 생략.

`Co-Authored-By` trailer는 기본으로 추가하지 않습니다. 최근 commit 이력에서 AI co-author trailer가 일관되게 사용되거나 사용자가 명시적으로 요청한 경우에만 해당 저장소의 관례를 따릅니다. 저장소 관례가 없고 사용자가 co-author trailer를 요청한 경우 `Co-Authored-By: Claude <noreply@anthropic.com>`를 사용합니다.

## 보고 형식

commit 완료 후 다음 형식으로 보고합니다:

```text
✅ N개 commit 생성 [+ push 여부]
  1. <hash> <type>(<scope>): <summary>
  2. <hash> <type>(<scope>): <summary>
제외한 파일: <있으면 나열, 없으면 생략>
```

## Error Handling

| Situation | Behavior |
| --- | --- |
| UNKNOWN 파일 발견 | 분류 목록을 사용자에게 보여주고 승인 후 진행 |
| Hook 실패 | `--no-verify` 사용 금지, 원인 보고 후 중단 |
| main/master에 직접 commit | 먼저 사용자에게 확인 요청 |
| Non-fast-forward push 거절 | 상황 설명 후 옵션 제시, force-push는 명시 요청 시만 |
| 비밀값/산출물 파일 발견 | 사용자에게 알리고 제외 |

## Integration

이 Skill은 다음 Skill과 연동됩니다:

- **ywc-ubiquitous-language** — Step 0.5 에서 `--mode update` 로 호출하여 domain glossary 를 commit 직전에 동기화
- **ywc-create-pr** — commit 후 PR 생성이 필요한 경우, ywc-create-pr 의 Step 4 에서 `--skip-ubiquitous-update` flag 와 함께 내부적으로 사용
- **ywc-finish-branch** — Branch lifecycle 종료 흐름에서 ywc-create-pr 을 경유해 간접적으로 호출
- **ywc-sequential-executor** — Task 실행 중 commit 단계에서 참조 가능

## Example Prompt

```text
/ywc-commit
커밋 해줘
commit and push
지금까지 한 작업 커밋푸쉬 ㄱㄱ
/ywc-commit --skip-ubiquitous-update  # caller skill 위임 시
```

## 번역본

- [English](./README.md)
- [Japanese](./README.ja.md)
- [Spanish](./README.es.md)
- [Chinese](./README.zh.md)
