# 000078-040-docs-code-gen-agentic-propagation — Implementation Checklist

## Prerequisites

- [ ] `000078-010-docs-impl-review-bounded-payload-noninteractive` 가 완료(merge)되었고 `ywc-impl-review` Arguments 표에 `--non-interactive` 행이 존재한다
- [ ] `000078-020-docs-sequential-executor-noninteractive` 가 완료(merge)되었고 `ywc-sequential-executor` Arguments 표에 `--non-interactive` 행이 존재한다
- [ ] 변경 전 `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` 값을 기록했다 (guard baseline)

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-code-gen/SKILL.md` 와 `claude-code/skills/ywc-agentic/SKILL.md` 만 편집한다
- [ ] Ownership 밖 편집이 필요하면 중단하고 보고한다

## Stop Conditions

- [ ] `ywc-code-gen` 에서 `:197` / `:198` 에 해당하는 두 호출 지점을 특정할 수 없으면 중단
- [ ] `ywc-agentic` Step 5 에서 sequential / parallel 선택 분기를 특정할 수 없으면 중단
- [ ] 기존 `ywc-plan --non-interactive` 3건(`:95`, `:97`, `:262`)을 수정해야 한다고 판단되면 중단
- [ ] `ywc-agentic` Step 5의 "`--review` 없이 executor 호출" 규칙을 바꿔야 한다고 판단되면 중단 (AC11 위반)

## Implementation Steps

- [ ] **FR-3a — `ywc-code-gen` 2곳**
  - [ ] `:197` Step 8 (`--review` 시): 표 셀의 `/ywc-impl-review --spec <spec-path> --working-tree` 에 `--non-interactive` 를 추가한다
  - [ ] `:198` critical-path 강제 ("forced, even without `--review`"): `/ywc-impl-review` 호출에만 flag를 부착한다. `/ywc-security-audit` 에는 부착하지 않는다
  - [ ] 두 지점의 status routing 문단은 변경하지 않는다
- [ ] **FR-3b — `ywc-agentic` Step 6**
  - [ ] `:156` 코드블록의 `ywc-impl-review --spec docs/ywc-plans/agentic-<slug>-iter1.md --git-range <pre-iter-sha>..HEAD` 끝에 리터럴 `--non-interactive` 를 추가한다
  - [ ] Step 6의 status routing 문단은 변경하지 않는다
- [ ] **FR-4(부분) — `ywc-agentic` Step 5 forward**
  - [ ] `:148` Step 5에서 **sequential** executor 선택 시 `--non-interactive` 를 함께 전달하도록 규정한다
  - [ ] **parallel** 선택 시에는 전달하지 않음을 명시한다 (`ywc-parallel-executor` 는 이 flag를 갖지 않는다)
  - [ ] 기존 "`--review` 없이 executor 호출" 규칙(Step 6이 review를 소유)은 **그대로 유지**한다
- [ ] **경계 확인**
  - [ ] `ywc-agentic:95,97,262` 의 `ywc-plan --non-interactive` 3건이 변경되지 않았는지 확인한다
  - [ ] `ywc-agentic:208` compaction 문단이 변경되지 않았는지 확인한다
  - [ ] 두 skill의 README 는 수정하지 않는다 (신설 flag 없음 → FR-7 범위 밖)

## Task Verify

- [ ] `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-code-gen/SKILL.md | wc -l` — **2**
- [ ] `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-agentic/SKILL.md | wc -l` — **1**
- [ ] `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` — Prerequisites 에 기록한 baseline 과 **동일**
- [ ] `grep -nE "ywc-sequential-executor[^|]*--non-interactive" claude-code/skills/ywc-agentic/SKILL.md` — ≥ 1
- [ ] `git diff -- claude-code/skills/ywc-agentic/SKILL.md` 에 `:208` compaction 문단이 나타나지 않음을 육안 확인
- [ ] `git diff --name-only` 에 README 파일이 없음

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] markdownlint 통과 — `.github/workflows/markdownlint.yml` 의 실제 invocation 형태를 재현한다
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --format json` 으로 read-only 확인
- [ ] `git diff --name-only | grep -c '^codex/'` — 0 (AC17)

## Implementation Notes

- Baseline `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` = 1 (the literal contiguous string only matches line 95; line 262's `--non-interactive` is separated from `ywc-plan` by prose). Unchanged after edit — verified.
- All three call sites and the Step 5 conditional forward matched the spec's described locations exactly (`:197`/`:198` in `ywc-code-gen`, `:156` in `ywc-agentic`, `:140`-`:148` region for Step 5's executor invocation). No structural divergence encountered; proceeded without escalation.
- All Task Verify greps pass: code-gen impl-review count = 2, agentic impl-review count = 1, ywc-plan baseline unchanged = 1, sequential-executor forward present, no README files touched, no codex/** files touched, `bash scripts/validate.sh` passes.
