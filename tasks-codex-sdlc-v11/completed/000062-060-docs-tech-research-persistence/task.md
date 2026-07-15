# 000062-060-docs-tech-research-persistence — Implementation Checklist

## Prerequisites

- [ ] `000062-020-docs-wayfinder-routing-catalog` complete.
- [ ] `000062-040-docs-task-generator-preview-assets` complete.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-tech-research/**`
- [ ] consumer handoff paragraphs in `codex/skills/ywc-plan/SKILL.md`, `codex/skills/ywc-spec-ready/SKILL.md`, `codex/skills/ywc-task-generator/SKILL.md`, `codex/skills/ywc-wayfinder/SKILL.md`

## Stop Conditions

- [ ] output path validation이 repository-relative safe roots를 벗어나면 중단한다.
- [ ] overwrite가 explicit confirm 없이 허용되거나 evidence/inference 경계가 흐려지면 중단한다.

## Implementation Steps

- [ ] persistence argument contract를 정의한다.
  - `--output`, `--overwrite`, `--confirm-overwrite`, `--non-interactive`의 allowed combinations와 Markdown-only safe roots를 명시한다.
  - Related AC/FR: AC5, Amendment E.
- [ ] provenance-aware report contract를 추가한다.
  - fetch date, source URL, version/date hints, `[INFERRED]`, known gaps를 구분해 기록하는 예시와 규칙을 넣는다.
  - Related AC/FR: AC6, Amendment I.
- [ ] downstream handoff wording을 정렬한다.
  - plan/spec-ready/task-generator/wayfinder가 persisted research artifact를 읽는 방식과 overwrite expectations를 동일하게 맞춘다.
  - Related AC/FR: AC4, AC5, Amendments E/N.

## Task Verify

- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-tech-research`
  - Expected Passing Signal: skill structure and references valid.
  - Pre-change Failing Evidence / Exception: persistence flags/contracts absent.
  - Contract/Test Evidence: validator output plus reference path checks.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: overwrite, invalid path, provenance markers covered.
  - Pre-change Failing Evidence / Exception: no research persistence assertions.
  - Contract/Test Evidence: runner output.

## Verification

- [ ] `rg -n -- '--(output|overwrite|confirm-overwrite|non-interactive)' codex/skills/ywc-tech-research codex/skills/ywc-plan codex/skills/ywc-spec-ready codex/skills/ywc-task-generator codex/skills/ywc-wayfinder`
