# Mission

project 의 Mission, Success Criteria, Rejected Approach, 그리고 선택적인 Non-goals/Constraints 를 `docs/mission.md` 에 저장해서 future Codex session 이 durable 한 project intent 와 경계를 참조할 수 있게 하는 Skill 입니다.

## Usage

```text
Use $ywc-mission --mode read.
Use $ywc-mission --mode update --dry-run.
```

## 옵션 Reference

> `SKILL.md` 의 Arguments 와 이 README 를 기준으로 정리한 전체 옵션입니다. 두 문서가 다르면 SKILL.md 를 우선합니다.

- **호출**: `$ywc-mission` (README: `Use $ywc-mission --mode read.`)
- **입력**: Mission / Success Criterion / Rejected Approach / Non-goal / Constraint 설명 (free text, update 시)
- **제약 · 조합**: `--dry-run` 은 CHANGESET 표시 후 확인/쓰기 없이 중단.

| 옵션 | 값 / 형식 | 기본값 | 설명 |
|---|---|---|---|
| `--mode` | `read\|update\|curate` | auto-detect | Mode 를 강제합니다 (`read`=Mission Anchor, `update`=CHANGESET 제안 후 기록, `curate`=stale entry deprecate). |
| `--output` | `<path>` | `docs/mission.md` | Mission file 경로입니다. |
| `--dry-run` | flag | off | 쓰지 않고 제안 CHANGESET 만 보여줍니다. |

## Modes

- `read`: active Mission Anchor 반환
- `update`: CHANGESET 제안 후 확인 뒤 기록
- `curate`: stale entry 를 hard-delete 하지 않고 deprecate

## Optional sections

- `## Non-goals`는 stable `NG###` ID, Non-goal, 필수 Reason, Status, Provenance를 사용합니다.
- `## Constraints`는 stable `CN###` ID, Constraint, 필수 Rationale, Status, Provenance를 사용합니다.
- 두 section은 선택 사항이며 첫 confirmed entry에서만 생성합니다. NG/CN section이 없는 기존 `docs/mission.md`도 계속 유효하고, 모든 entry가 deprecated되면 빈 section을 남기지 않습니다.
- Reason/Rationale이 빠진 row는 CHANGESET에 넣기 전에 해당 설명을 요청합니다. Proposed CHANGESET이 비어 있으면 confirmation 없이 no-op 처리합니다. Deprecated ID는 재사용하지 않으며, 비어 있지 않은 CHANGESET은 confirmation 후 기존 date/history 규칙대로 기록합니다.
- Read mode는 존재하는 optional section의 active rows만 Mission Anchor에 포함합니다.

## 쓰기 경계

- update/curate는 전체 파일을 먼저 읽고 정확한 ADD/MODIFY/DEPRECATE CHANGESET의 사용자 확인 후에만 기록합니다.
- `--dry-run`과 빈 CHANGESET은 확인 요청, 파일 생성, 날짜/변경 이력 갱신 없이 종료합니다.
- Mission은 active 하나만 유지합니다. SC는 observable Criterion/Rationale, RA는 Reason이 필요합니다. 폐기 시 원문·이유·출처를 보존하며 ID는 재사용하거나 삭제하지 않습니다.
- 확인 후 파일이 바뀌면 새 CHANGESET과 확인이 필요합니다. 재시도는 이미 반영된 변경을 중복 기록하지 않습니다.
- 최초 생성 후 AGENTS.md/CODEX.md 활성화 안내만 제공하며 해당 파일을 수정하지 않습니다.
- 평가 fixture는 source assertion이며 live 실행은 별도 근거가 없으면 UNVERIFIED입니다.

## Output

`docs/mission.md` 를 읽거나 갱신하고, compact Mission Anchor 또는 user-confirmed CHANGESET 결과를 반환합니다.
