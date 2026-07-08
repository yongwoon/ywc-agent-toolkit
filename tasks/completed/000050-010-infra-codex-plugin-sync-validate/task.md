# 000050-010-infra-codex-plugin-sync-validate — Implementation Checklist

## Prerequisites

- [ ] `000047-010-infra-cloud-engineer-specialist` is completed.
- [ ] `000047-020-infra-agent-lens-extensions` is completed.
- [ ] `000048-010-docs-infra-reference-core` is completed.
- [ ] `000048-020-docs-infra-provider-packs` is completed.
- [ ] `000049-010-docs-iac-author-skill` is completed.
- [ ] `000049-020-docs-infra-design-skill` is completed.
- [ ] `000049-030-docs-infra-review-skill` is completed.
- [ ] `000049-040-docs-infra-optimize-skill` is completed.

## Allowed Edit Scope

- [ ] generated plugin/package files only:
  - `plugins/ywc-agent-toolkit/skills/**`
  - `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json`
  - `plugins/ywc-agent-toolkit/README.md`
- [ ] source fixes가 필요하면 중단하고 owning source task로 되돌립니다.

## Stop Conditions

- [ ] `bash scripts/sync-codex-plugin.sh` fails.
- [ ] `bash scripts/validate.sh` reports source-content defects that cannot be fixed inside generated output.
- [ ] install/list checks do not expose the four new skills or new cloud engineer agent.
- [ ] `git diff --name-only` includes unexpected `claude-code/**` changes introduced by this task.

## Hardening Gate

- [ ] Classify this task: generated-file-only / validation hard gate.
- [ ] Existing coverage: `bash scripts/validate.sh`.
- [ ] Interface contract: Codex source to generated plugin mirror sync plus install/list visibility.
- [ ] Critical surface: no source patching in generated mirror; return to source owner if validation fails.

## Implementation Steps

- [ ] Generated mirror를 동기화합니다.
  - [ ] `bash scripts/sync-codex-plugin.sh`를 실행합니다.
  - [ ] generated plugin diff가 Codex source changes에만 대응하는지 `git diff --stat`로 점검합니다.
  - [ ] Related AC/FR: `AC10`, `FR-7`
  - [ ] Contract / Behavior Change: plugin package가 source of truth와 동기화됩니다.
  - [ ] Verification Command / Evidence: sync script output + diff review
- [ ] Repository validation을 실행합니다.
  - [ ] `bash scripts/validate.sh`를 실행합니다.
  - [ ] source issue가 발견되면 generated files를 수동 수정하지 않고 source owner task로 되돌립니다.
  - [ ] Related AC/FR: `AC11`, `FR-7`
  - [ ] Contract / Behavior Change: bundle structure와 metadata correctness를 최종 확인합니다.
  - [ ] Verification Command / Evidence: validator output
- [ ] Install/list visibility와 Codex-only boundary를 확인합니다.
  - [ ] `bash scripts/install.sh --list --codex | rg 'ywc-(iac-author|infra-design|infra-review|infra-optimize)'`
  - [ ] `bash scripts/install.sh --list --codex-agents | rg 'ywc-cloud-engineer'`
  - [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - [ ] Related AC/FR: `AC1`, `AC6`, `AC10`, `AC11`, `AC12`, `FR-7`
  - [ ] Contract / Behavior Change: install surfaces and Codex-only scope are verified before close-out.
  - [ ] Verification Command / Evidence: list output + scope guard

## Task Verify

- [ ] `bash scripts/sync-codex-plugin.sh`
  - Expected Passing Signal: exit 0 and generated plugin files update without manual edits
  - Pre-change Failing Evidence / Exception: plugin mirror may be stale before task
  - Contract/Test Evidence: sync script output
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: exit 0
  - Pre-change Failing Evidence / Exception: earlier phases may legitimately fail before all source tasks land
  - Contract/Test Evidence: validator output
- [ ] `bash scripts/install.sh --list --codex | rg 'ywc-(iac-author|infra-design|infra-review|infra-optimize)'`
  - Expected Passing Signal: all four new skills are listed
  - Pre-change Failing Evidence / Exception: names absent before batch implementation
  - Contract/Test Evidence: list output
- [ ] `bash scripts/install.sh --list --codex-agents | rg 'ywc-cloud-engineer'`
  - Expected Passing Signal: new cloud engineer agent is listed
  - Pre-change Failing Evidence / Exception: name absent before batch implementation
  - Contract/Test Evidence: list output
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
  - Expected Passing Signal: no output, exit 0
  - Pre-change Failing Evidence / Exception: unrelated user changes under `claude-code/**` must be called out, not reverted
  - Contract/Test Evidence: scope guard

## Verification

- [ ] plugin mirror is synced from Codex source
- [ ] full repository validation passes
- [ ] no `claude-code/**` files are modified by this batch
