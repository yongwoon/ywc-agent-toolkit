# Implementation Task — 000061-020-test-auth-implement-routing-evals

## Prerequisites

- [ ] `000061-010-domain-auth-implement-skill` is merged.
- [ ] Read final `SKILL.md` and `references/rationalization-evidence.md` without editing the latter.

## Allowed Edit Scope

Only `codex/skills/ywc-auth-implement/evals/**`.

## Stop Conditions

- [ ] Required behavior cannot be stated without unsupported worker names or a fixed stack playbook.
- [ ] A fixture would contain a real secret, token, or credential.
- [ ] The existing JSON runner cannot validate the intended field shape; report the gap rather than changing the runner.

## Hardening Gate

- [ ] Start by adding a behavior array for each acceptance scenario before treating the fixture as passing.
- [ ] Preserve the status/routing interface defined by `SKILL.md`.
- [ ] Complete manual review for direct-crypto refusal and Critical/High audit skip assertions; Data Integrity is N/A.

## Implementation Steps

- [ ] Create `evals/evals.json` with `skill_name: "ywc-auth-implement"` and unique numeric IDs.
  - [ ] Add happy-path policy-to-plan/spec/task/code-gen routing.
  - [ ] Add existing-auth `new | extend | migrate` hard stop and unknown-stack research routing.
- [ ] Add direct JWT/password/secret crypto refusal and Critical/High audit skip fixtures.
- [ ] Add `expected_behavior` and `anti_behavior` arrays to every fixture, then cross-check final skill wording.
- [ ] Parse JSON and run the repository contract runner.

## Task Verify

- [ ] `python3 -m json.tool codex/skills/ywc-auth-implement/evals/evals.json >/dev/null`
- [ ] `jq -e '.evals | length == 5' codex/skills/ywc-auth-implement/evals/evals.json`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification

- [ ] Run all Task Verify commands.
- [ ] Leave source body/reference changes for their owning task.
