# 000047-020-infra-agent-lens-extensions — Implementation Checklist

## Prerequisites

- [ ] 현재 `codex/agents/ywc-security-engineer.toml`와 `codex/agents/ywc-performance-engineer.toml`의 output contract를 읽고 유지해야 할 공통 구조를 확인합니다.

## Allowed Edit Scope

- [ ] `codex/agents/ywc-security-engineer.toml`
- [ ] `codex/agents/ywc-performance-engineer.toml`
- [ ] 다른 agent 파일이나 skill 파일로 범위가 번지면 중단합니다.

## Stop Conditions

- [ ] infra lens wording을 넣기 위해 기존 app-focused mission을 삭제해야 한다면 중단합니다.
- [ ] reliability lens를 security/performance agent에 흡수해야만 한다면 중단합니다.
- [ ] output contract를 변경해야 validator 또는 caller expectation이 맞는다고 판단되면 중단합니다.

## Hardening Gate

- [ ] Classify this task: agent-definition maintenance on critical review surfaces.
- [ ] Existing coverage: `bash scripts/validate.sh`.
- [ ] Interface contract: existing status/summary/finding format unchanged; infra wording appended only.
- [ ] Critical surface: trust-boundary and severity wording must be reviewed manually.

## Implementation Steps

- [ ] Security specialist의 infra-review wording을 설계합니다.
  - [ ] description과 developer_instructions에 IaC misconfiguration, IAM/RBAC over-privilege, public exposure, secrets-in-state 표현을 추가합니다.
  - [ ] `ywc-architect`/`ywc-root-cause-analyst` 경계는 유지합니다.
  - [ ] Related AC/FR: `AC7`, `FR-4`
  - [ ] Contract / Behavior Change: infra-review skill이 security lens dispatch 시 올바른 specialist를 찾을 수 있습니다.
  - [ ] Verification Command / Evidence: `rg -n 'IaC|IAM|RBAC|public exposure|secrets-in-state' codex/agents/ywc-security-engineer.toml`
- [ ] Performance specialist의 cost lens wording을 설계합니다.
  - [ ] description과 developer_instructions에 FinOps, right-sizing, reserved/spot, transfer cost, idle resource 표현을 추가합니다.
  - [ ] 기존 latency / Web Vitals mission은 유지합니다.
  - [ ] Related AC/FR: `AC7`, `FR-4`
  - [ ] Contract / Behavior Change: infra-review skill이 cost lens dispatch 시 올바른 specialist를 찾을 수 있습니다.
  - [ ] Verification Command / Evidence: `rg -n 'FinOps|right-sizing|reserved|spot|transfer cost|idle resource' codex/agents/ywc-performance-engineer.toml`
- [ ] Scope drift를 검토합니다.
  - [ ] reliability 판단을 `ywc-cloud-engineer`로 남겨두고 wording overlap을 제거합니다.
  - [ ] status line, summary, finding-count conventions가 그대로인지 diff review합니다.
  - [ ] Related AC/FR: `AC7`, `AC8`, `FR-4`
  - [ ] Contract / Behavior Change: infra lens 수용과 기존 caller compatibility를 동시에 유지합니다.
  - [ ] Verification Command / Evidence: `git diff -- codex/agents/ywc-security-engineer.toml codex/agents/ywc-performance-engineer.toml`

## Task Verify

- [ ] `rg -n 'IaC|IAM|RBAC|public exposure|secrets-in-state' codex/agents/ywc-security-engineer.toml`
  - Expected Passing Signal: new infra-security terms appear without removing existing security contract
  - Pre-change Failing Evidence / Exception: current file may not contain infra-specific terms
  - Contract/Test Evidence: grep witness + diff review
- [ ] `rg -n 'FinOps|right-sizing|reserved|spot|transfer cost|idle resource' codex/agents/ywc-performance-engineer.toml`
  - Expected Passing Signal: new infra-cost terms appear
  - Pre-change Failing Evidence / Exception: current file may not contain those terms
  - Contract/Test Evidence: grep witness + diff review
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: exit 0 or only unrelated pre-existing failures explicitly identified
  - Pre-change Failing Evidence / Exception: repository-level gate may include unrelated pending work
  - Contract/Test Evidence: validator output for Codex agent files

## Verification

- [ ] diff scope stays within the two existing agent files
- [ ] no new agent files or skill files are introduced
