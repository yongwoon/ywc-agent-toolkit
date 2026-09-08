# Mine Review History

Merge가 완료된 다수의 PR을 대상으로 Bot Review Comment(CodeRabbit / Codex Review / Claude Review)를 일괄 조사하고, 반복적으로 나타나는 결함 유형을 학습 후보로 제안하는 Claude Code Skill입니다.

## 개요

`ywc-review-learnings --mode update --source pr`는 단일 PR을 On-demand로 다루고, `ywc-incident-postmortem`은 단일 Incident만 다룹니다. 두 Skill이 채택되기 이전에 쌓인 PR History를 소급해서 훑어보는 경로는 존재하지 않았으며, 이 Skill이 바로 그 역할을 합니다.

지정된 범위(개수 또는 날짜) 안의 Merge된 PR에서 Bot Comment를 모으고, 기존 `--source pr` 경로와 동일한 규칙으로 각 Comment를 Accept/Dismiss로 분류합니다. 분류된 Comment는 결함 Class 단위로 묶이며, `--min-recurrence`(기본 3) 이상 서로 다른 PR에서 반복된 Class만 `ywc-review-learnings --mode update --source pr`로 승격 후보를 전달합니다. `docs/review-learnings.md` 파일은 이 Skill이 직접 수정하지 않고, 승격은 항상 대상 Skill의 확인 절차를 거칩니다.

### 주요 기능

- Scope는 `--limit` / `--since`로 제한되며, 둘 다 없으면 실행하지 않음
- 기존 Accept/Dismiss 분류 규칙을 그대로 Batch 규모에 적용
- 반복 집계 단위는 Comment가 아니라 서로 다른 PR
- 임계값 미만 Class도 Report에는 항상 표시(누락 없음)
- 매 실행 시 조사 PR 수, 수집/분류 Comment 수, 발견/승격 결함 Class를 모두 Report

## 사용 방법

```text
/ywc-mine-review-history --limit 50
/ywc-mine-review-history --since 2026-01-01
/ywc-mine-review-history --limit 50 --min-recurrence 4
```

자연어 Trigger는 [SKILL.md](./SKILL.md)를 참고하세요.

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- `--limit`, `--since` 중 최소 하나 지정 필수

## 다국어 버전

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean (Primary)](./README.md)
