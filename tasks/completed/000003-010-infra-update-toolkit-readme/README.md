# 000003-010-infra-update-toolkit-readme

## Purpose

root `README.md`에 Hook 설치 섹션을 추가하여, 사용자가 `--hooks` 기능을 발견하고 사용할 수 있도록 안내한다.

## Scope

- root `README.md`의 Hook 설치 섹션 신규 추가
  - 설치 가능 Hook 목록 (7개)
  - global / local 설치 명령 예시
  - 선택 설치 예시
  - 의존성 안내 (`jq`, `uv`)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/hooks-distribution.md#scope` — 배포 대상 Hook 7개 목록
- `docs/ywc-plans/hooks-distribution.md#fr-3-installsh-cli-확장` — README에 포함할 CLI 예시 원본
- `000002-010-infra-implement-hook-installer/README.md` — 실제 구현된 CLI 인터페이스 확인

### Summary

Task 2에서 구현된 `--hooks` 인터페이스를 root README.md에 문서화한다. 기존 Skills 설치 섹션과 동일한 문서 스타일로 작성하여 일관성을 유지한다. Hook 별 간단한 설명과 의존성(`jq` 필수, `uv` 필수)을 포함한다.

### Out of Scope (from spec)

- Hook README 다국어 번역 — Spec Out of Scope
- `permissions` 병합 관련 내용 — Spec에서 명시적으로 제외

## Dependencies

### Depends On
- `000002-010-infra-implement-hook-installer` — 실제 동작하는 CLI 인터페이스가 확정된 후에야 정확한 사용 예시를 작성할 수 있음

### Depended By
- (None — 이 태스크는 leaf 태스크)

## Key Files

| 파일 | 변경 유형 |
|------|-----------|
| `README.md` | 수정 (Hook 설치 섹션 추가) |

## Notes

- 기존 Skills 섹션과 동일한 마크다운 스타일(코드 블록, 테이블 포맷)을 따른다.
- `bash scripts/validate.sh` 는 `README.md`를 직접 검사하지 않으나, `markdownlint.yml` CI 워크플로우가 README*.md를 lint하므로 MD 포맷 규칙 준수 필요.

## Parallel Execution Metadata

### Ownership
- `README.md`

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- `000002-010-infra-implement-hook-installer`

### Task Verify
- `grep -q 'hooks' README.md` → Hook 섹션 존재 확인
- `bash scripts/validate.sh`

## Out of Scope

- README.md 이외 문서 수정 (CONTRIBUTING.md, CHANGELOG.md 등)
- Hook Script 내부 동작의 상세 설명 (claude-code/hooks/README.md 역할)
- 다국어 README 파일 업데이트
