# 000047-010-infra-cloud-engineer-specialist — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/codex-infra-skill-suite-port.md`의 Iteration 1 amendments를 읽고 v1 agent가 read-only specialist임을 확인합니다.

## Allowed Edit Scope

- [ ] `codex/agents/ywc-cloud-engineer.toml`만 수정합니다.
- [ ] 범위가 `claude-code/**`, `codex/skills/**`, generated plugin mirror로 번지면 중단합니다.

## Stop Conditions

- [ ] validator가 요구하는 Codex agent TOML shape가 현재 prior art와 다르면 중단합니다.
- [ ] write-enabled behavior를 남겨야만 spec intent를 만족한다고 판단되면 중단하고 spec refinement를 요청합니다.
- [ ] Terraform-only wording 없이 multi-IaC wording이 필요해 보이면 중단합니다.

## Hardening Gate

- [ ] Classify this task: agent-definition / docs-backed contract change.
- [ ] Existing coverage: `bash scripts/validate.sh`.
- [ ] Interface contract: read-only specialist, bounded infra advisory, explicit status + next action output.
- [ ] Critical surface: `sandbox_mode`, mission boundary, and anti-trigger wording require human review.

## Implementation Steps

- [ ] Existing Codex agent prior art를 캡처합니다.
  - [ ] `codex/agents/ywc-architect.toml`, `ywc-security-engineer.toml`, `ywc-performance-engineer.toml`에서 name/description/developer_instructions/output pattern을 확인합니다.
  - [ ] Related AC/FR: `AC6`, `FR-3`
  - [ ] Contract / Behavior Change: 신규 agent가 repository의 Codex agent 규약과 동일한 output contract를 갖습니다.
  - [ ] Verification Command / Evidence: `rg -n '^name = |^description = |^sandbox_mode = ' codex/agents/ywc-*.toml`
- [ ] `codex/agents/ywc-cloud-engineer.toml`을 작성합니다.
  - [ ] Mission에 Terraform feasibility, provider advisory, blast-radius sanity check, reliability review를 명시합니다.
  - [ ] Boundary에 architecture redesign, app security static review, app performance review, direct file edits 비대상을 명시합니다.
  - [ ] Related AC/FR: `AC6`, `AC12`, `FR-3`
  - [ ] Contract / Behavior Change: infra skill들이 read-only specialist dispatch target를 사용할 수 있게 됩니다.
  - [ ] Verification Command / Evidence: `rg -n 'read-only|Terraform|reliability|Next action:' codex/agents/ywc-cloud-engineer.toml`
- [ ] Output contract와 anti-trigger를 정리합니다.
  - [ ] `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`와 `Next action:` 라인을 고정합니다.
  - [ ] description에 `ywc-architect`, `ywc-security-engineer`, `ywc-performance-engineer`로의 routing boundary를 적습니다.
  - [ ] Related AC/FR: `AC6`, `AC8`, `FR-3`
  - [ ] Contract / Behavior Change: 상위 skill이 ambiguous dispatch를 피합니다.
  - [ ] Verification Command / Evidence: `rg -n 'Do not use for|Next action:|Status:' codex/agents/ywc-cloud-engineer.toml`

## Task Verify

- [ ] `test -f codex/agents/ywc-cloud-engineer.toml`
  - Expected Passing Signal: file exists
  - Pre-change Failing Evidence / Exception: 신규 파일이므로 pre-change file absent
  - Contract/Test Evidence: diff review
- [ ] `rg -n 'sandbox_mode = "read-only"|Status:|Next action:|Terraform|blast-radius|reliability' codex/agents/ywc-cloud-engineer.toml`
  - Expected Passing Signal: required contract lines are present
  - Pre-change Failing Evidence / Exception: file absent before task
  - Contract/Test Evidence: grep witness
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: exit 0 or only unrelated pre-existing failures explicitly identified
  - Pre-change Failing Evidence / Exception: repository-level gate may include unrelated pending work
  - Contract/Test Evidence: validator output for Codex agent files

## Verification

- [ ] repository validation evidence is collected
- [ ] diff scope stays within `codex/agents/ywc-cloud-engineer.toml`
