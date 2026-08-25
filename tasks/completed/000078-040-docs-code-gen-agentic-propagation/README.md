# 000078-040-docs-code-gen-agentic-propagation

## Purpose

`ywc-impl-review`를 자동 호출하는 나머지 3개 지점(`ywc-code-gen` 2곳, `ywc-agentic` 1곳)에 `--non-interactive`를 전파하고, `ywc-agentic` Step 5가 sequential executor 선택 시 그 flag를 forward하도록 한다. FR-3의 7개 지점 중 마지막 3개를 닫는 task다.

## Scope

- FR-3(부분): `ywc-code-gen` `:197` Step 8(`--review`) · `:198` critical-path 강제, `ywc-agentic` `:156` Step 6 코드블록 — 총 3곳에 `--non-interactive` 부착.
- FR-4(부분): `ywc-agentic` Step 5(`:148`)가 **sequential** 선택 시 `--non-interactive`를 forward. parallel 선택 시에는 전달하지 않는다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-3-자동-호출-caller-7곳의-flag-전파` — code-gen 2행 + agentic 1행
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-4-ywc-sequential-executor---non-interactive-external-url-policy` — 마지막 bullet(agentic forward)
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#iteration-1-amendments` — AC7 관측 방법 수정본이 authoritative

### Summary

이 spec이 닫는 **주된 hang 경로**는 `ywc-agentic` → executor(`--review` 미지정) → critical task → forced impl-review → Step 7 prompt 다. `ywc-code-gen:198`과 `ywc-agentic:156`은 그 경로의 나머지 절반이다. 특히 `ywc-code-gen:198`의 "forced, even without `--review`" 지점은 upstream spec이 누락했으며 본 repo grep으로 발견된 곳이다. 조건 분기는 두지 않는다 — 3곳 모두 loop step으로서의 자동 호출이며, executor의 Non-Stop Execution Principle과 `ywc-agentic`의 자율 loop 계약이 이미 이 지점의 prompt를 금지하므로 flag 부착은 기존 규칙의 **집행**이다. `ywc-agentic` Step 5는 sequential 선택 시에만 forward하며(`ywc-parallel-executor`는 이 flag를 갖지 않는다), 기존 "`--review` 없이 호출" 규칙은 유지된다.

### Out of Scope (from spec)

- `/ywc-security-audit` 호출 — 해당 skill에 이 flag가 없으며 범위 밖.
- caller status routing 문단(`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`) — 무변경.
- `ywc-agentic:208` compaction 문단 — 이미 존재하며 무변경.
- `ywc-agentic:95,97,262`의 기존 `ywc-plan --non-interactive` 3건 — 무변경. AC7 guard grep이 이를 감시한다.
- `ywc-agentic` Step 5의 "`--review` 없이 executor 호출" 규칙(`:148`) — 무변경.
- `ywc-parallel-executor` 로 forward — 그 skill은 이 flag를 갖지 않는다.

## Criticality

`normal` — skill의 prompt 문서만 수정한다. flag 부착은 기존 Non-Stop Execution 규칙의 집행이며 권한을 확대하지 않는다 (spec §Critical Surfaces).

## Dependencies

### Depends On

- `000078-010-docs-impl-review-bounded-payload-noninteractive` — `ywc-impl-review --non-interactive` 가 실재해야 3개 호출 지점이 유효한 명령을 가리킨다
- `000078-020-docs-sequential-executor-noninteractive` — `ywc-sequential-executor --non-interactive` 가 실재해야 Step 5 forward가 유효한 명령을 가리킨다

### Depended By

- `000079-010-infra-context-safety-validation` — AC7(3/7건), AC11 검증 대상

## Key Files

- `claude-code/skills/ywc-code-gen/SKILL.md` — `:197` 표 셀, `:198` 강제 호출에 flag 부착
- `claude-code/skills/ywc-agentic/SKILL.md` — `:156` Step 6 코드블록에 flag 부착, `:148` Step 5에 sequential forward 규칙 추가

## Notes

- **`ywc-code-gen`의 "Step 7.5"는 본 repo에 없다.** upstream spec의 표기와 달리 실제 지점은 `:197` **Step 8**이다.
- `:198`은 "forced, even without `--review`" 지점으로 upstream spec이 누락했다. **impl-review 호출에만** flag를 부착한다.
- **Step 5 forward는 조건부다** — sequential 선택 시에만. parallel 선택 시에는 전달하지 않는다 (AC11).
- **기존 `ywc-plan --non-interactive` 3건을 건드리지 말 것.** `ywc-agentic/SKILL.md:95,97,262`에 이미 존재하며, AC7의 guard grep(`grep -c "ywc-plan --non-interactive" … # expected: unchanged (1)`)이 이를 감시한다.
- AC7의 관측 방법은 call-site-scoped grep이다: `grep -rnE "ywc-impl-review[^|]*--non-interactive"`. `[^|]*` bound는 Markdown 표에서 한 열의 `ywc-impl-review` 언급과 다른 열의 `--non-interactive` 언급이 잘못 이어지는 것을 막는다.
- 두 skill 모두 README 갱신 대상이 아니다 — 신설 flag가 없으므로 FR-7 범위 밖.
- 본문 편집은 **영문**이다.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-code-gen/SKILL.md`
- `claude-code/skills/ywc-agentic/SKILL.md`

### Shared Surfaces

- `--non-interactive` flag 의미 계약 — `000078-010`(impl-review)과 `000078-020`(sequential) 양쪽을 소비한다
- CI gates: `scripts/validate.sh`, `markdownlint.yml`, `score.py --ci`

### Conflicts With

- (None identified) — 소유 파일이 다른 task와 완전히 분리됨

### Parallelizable After

- `000078-010-docs-impl-review-bounded-payload-noninteractive`
- `000078-020-docs-sequential-executor-noninteractive`

### Task Verify

- `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-code-gen/SKILL.md | wc -l` — **2**
- `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-agentic/SKILL.md | wc -l` — **1**
- `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` — **1** (변경 전과 동일)
- `grep -nE "ywc-sequential-executor[^|]*--non-interactive" claude-code/skills/ywc-agentic/SKILL.md` — ≥ 1 (Step 5 forward)
- `git diff -- claude-code/skills/ywc-agentic/SKILL.md` 에 `:208` compaction 문단과 `:148` 의 "`--review` 없이" 규칙이 나타나지 않음

## Out of Scope

- `ywc-impl-review` / `ywc-sequential-executor` / `ywc-parallel-executor` 파일 수정 — 각각 다른 task 소유.
- 두 skill의 README 갱신 — 신설 flag가 없으므로 FR-7 범위 밖.
- `ywc-agentic` 의 iteration loop / checkpoint mechanics 변경.
- `codex/**` 하위 모든 파일 (AC17).
- mechanical score baseline 재생성 — `000079-010`이 담당.
