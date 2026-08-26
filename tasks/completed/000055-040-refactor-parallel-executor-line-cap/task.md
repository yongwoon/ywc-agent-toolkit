# 000055-040-refactor-parallel-executor-line-cap — Implementation Checklist

## Prerequisites

- [ ] `000054-010-test-skill-audit-validation` is completed and merged (audit report가 존재하며 이 skill에 대한 findings를 인용할 수 있다).
- [ ] `claude-code/skills/ywc-skill-author/SKILL.md:93`의 Tier-2 pinning 규칙을 읽었다.

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-parallel-executor/SKILL.md` 와 `claude-code/skills/ywc-parallel-executor/references/**` 만 편집한다.
- [ ] 다른 skill은 건드리지 않는다.

## Stop Conditions

- [ ] 500줄 아래로 내리는 유일한 방법이 Workflow / Rationalization Defense / Validation Checklist를 추출하는 것뿐이라면 **멈추고 보고한다** — Tier-2 pinning 위반이다.
- [ ] 추출 가능한 정적 블록이 30줄에 못 미치면 멈추고 보고한다 (`references/` 파일은 ≥30줄이어야 한다).
- [ ] RD table에서 행을 하나라도 지우고 싶어지면 멈춘다 (AC2).

## Implementation Steps

- [ ] `wc -l claude-code/skills/ywc-parallel-executor/SKILL.md`로 현재 줄 수(502 예상)를 확인한다.
- [ ] `000054-010`의 audit report에서 이 skill에 대한 findings를 찾아 인용 근거를 확보한다.
- [ ] `SKILL.md`에서 **정적** 콘텐츠 후보(lookup table, decision tree)를 식별한다. Workflow prose / RD table / Validation Checklist는 후보에서 제외한다.
- [ ] 30줄 이상의 블록을 `claude-code/skills/ywc-parallel-executor/references/<name>.md`로 옮긴다.
- [ ] `SKILL.md`의 해당 위치에 pointer **한 줄**을 남긴다. 요약을 남기지 않는다.
- [ ] `SKILL.md`가 500줄 이하가 되었는지 확인한다.

## Task Verify

- [ ] `test "$(wc -l < claude-code/skills/ywc-parallel-executor/SKILL.md)" -le 500`
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/ywc-parallel-executor/` → exit 0
- [ ] `wc -l claude-code/skills/ywc-parallel-executor/references/<name>.md` ≥ 30
- [ ] `grep -q '<name>.md' claude-code/skills/ywc-parallel-executor/SKILL.md` (pointer 존재)

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `git diff -- claude-code/skills/ywc-parallel-executor/SKILL.md`의 삭제 줄(`^-`)이 Rationalization Defense 섹션 밖에만 있다 (AC2).
