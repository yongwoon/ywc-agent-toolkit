# 000063-010-infra-codex-release-evidence — Implementation Checklist

## Prerequisites

- [ ] All Phase 000062 tasks complete.

## Allowed Edit Scope

- [ ] ignored release evidence docs under `docs/ywc-plans/`
- [ ] `CHANGELOG.md`
- [ ] `VERSION`
- [ ] source-owned validation/install/sync documentation that is necessary to record release evidence

## Stop Conditions

- [ ] generated plugin을 source of truth처럼 수동 수정해야만 통과하는 상태면 중단한다.
- [ ] any Phase 000062 contract가 미정인데 release evidence로 우회하려 하면 중단한다.

## Implementation Steps

- [ ] validation matrix를 기록한다.
  - author validator, contract eval runner, required install/list commands의 command, exit status, timestamp, evidence location을 남긴다.
  - Related AC/FR: AC10, Amendment M.
- [ ] controlled smell review evidence를 작성한다.
  - prompt fixture, runtime context, checked skills, human verification points, unresolved findings를 명시한다.
  - Related AC/FR: AC10, Amendment O.
- [ ] release metadata와 plugin parity를 마감한다.
  - `CHANGELOG.md`, `VERSION`, source/plugin sync 결과, temporary `CODEX_HOME` install verification을 정리한다.
  - Related AC/FR: AC10, Amendment O.

## Task Verify

- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: repository validation passes after all source updates.
  - Pre-change Failing Evidence / Exception: missing contracts or metadata drift.
  - Contract/Test Evidence: validator output captured in release evidence doc.
- [ ] `bash scripts/install.sh --list`
  - Expected Passing Signal: installable Codex skills and agents enumerate cleanly.
  - Pre-change Failing Evidence / Exception: stale or malformed skill metadata.
  - Contract/Test Evidence: command log in validation matrix.
- [ ] `tmpdir="$(mktemp -d)" && CODEX_HOME="$tmpdir" bash scripts/install.sh --codex ywc-plan && rm -rf "$tmpdir"`
  - Expected Passing Signal: targeted temporary install succeeds without touching real Codex home.
  - Pre-change Failing Evidence / Exception: packaging drift.
  - Contract/Test Evidence: install log and cleanup note.
- [ ] `bash scripts/sync-codex-plugin.sh`
  - Expected Passing Signal: generated plugin refreshes from source without manual edits.
  - Pre-change Failing Evidence / Exception: source/plugin parity drift.
  - Contract/Test Evidence: sync log and follow-up diff check.

## Verification

- [ ] `git diff -- codex/skills plugins/ywc-agent-toolkit/skills`
