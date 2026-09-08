# Mine Review History

이미 Merge된 여러 PR에 걸쳐 Bot Review Comment(CodeRabbit / Codex Review / Claude Review)를 일괄 수집하고, 반복되는 결함 Class를 후보 학습으로 제시하는 Claude Code Skill입니다.

## 개요

기존에는 `ywc-review-learnings --mode update --source pr`(단일 PR, On-demand)와 `ywc-incident-postmortem`(단일 Incident)만 있었고, 두 Skill 모두 채택 이전 시점의 PR History를 **일괄/소급 조사(Batch/Retrospective Sweep)**하지는 못했습니다. 이 Skill은 그 공백을 메웁니다.

지정한 범위의 Merge된 PR에서 Bot Comment를 수집하고, `ywc-review-learnings`가 이미 사용하는 것과 동일한 규칙으로 Accept/Dismiss를 분류한 뒤 결함 Class로 Clustering합니다. `--min-recurrence`(기본값 3) 이상 서로 다른 PR에서 반복된 Class만 `ywc-review-learnings --mode update --source pr`에 승격 후보로 전달합니다. `docs/review-learnings.md`는 이 Skill이 직접 쓰지 않으며, 모든 승격은 해당 Skill의 확인 Gate를 거칩니다.

### 주요 기능

- `--limit` / `--since`로 범위를 제한 — 무제한 전체 Scan은 제공하지 않음
- 기존 `--source pr` Accept/Dismiss 분류 규칙을 Batch 규모로 재사용
- 반복 횟수는 Comment 수가 아니라 **서로 다른 PR 수**로 집계
- `--min-recurrence`(기본값 3) 기준으로 승격 여부 결정 — 미달 Class도 Report에는 항상 포함
- 매 실행마다 전체 Report 제공: 조사한 PR, 수집/분류된 Comment, 발견/승격된 결함 Class

## 사용 방법

```text
/ywc-mine-review-history --limit 50
/ywc-mine-review-history --since 2026-01-01
/ywc-mine-review-history --limit 50 --min-recurrence 4
```

자연어 호출 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## 전제 조건

- `gh` CLI 설치 및 인증 완료
- `--limit` 또는 `--since` 중 최소 하나는 반드시 지정

## 다국어 버전

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
