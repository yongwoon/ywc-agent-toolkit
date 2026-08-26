# 000063-020-test-auth-implement-evals — Implementation Checklist

## Prerequisites

- [ ] `000063-010-domain-auth-implement-skill` is merged.
- [ ] Read the final `claude-code/skills/ywc-auth-implement/SKILL.md` and `references/rationalization-evidence.md` (read-only — do not edit the latter).
- [ ] Read `claude-code/skills/ywc-commit/evals/evals.json` as the field-shape reference for this repository's actual eval convention.

## Allowed Edit Scope

- [ ] Only `claude-code/skills/ywc-auth-implement/evals/**`.
- [ ] Do not modify `SKILL.md`, `README*.md`, or `references/**` — those belong to `000063-010`.

## Stop Conditions

- [ ] Stop if a required scenario cannot be stated without inventing an unsupported agent name, command, or a fixed stack playbook.
- [ ] Stop if a fixture would need a real secret, token, or credential value.
- [ ] Stop if the merged `SKILL.md` wording does not match what this task's README assumed — re-read the actual file rather than guessing.

## Implementation Steps

- [ ] Create `evals/evals.json` with top-level `skill_name: "ywc-auth-implement"`, a `description`, and `last_updated`, matching `ywc-commit/evals/evals.json`'s shape.
  - [ ] `evals[0]` — happy path: policy interview approved, stack evidence sufficient, recommendation issued, `ywc-backend-coder`/`ywc-frontend-coder` dispatched under `ywc-tdd-ritual`, security audit clean, E2E passes, `ywc-create-pr` suggested.
  - [ ] `evals[1]` — existing-auth hard stop: preflight detects existing auth, skill returns `NEEDS_CONTEXT` until the user picks `new`/`extend`/`migrate`, no scaffolding or dispatch happens first.
- [ ] Add the unknown-stack and direct-crypto-rejection scenarios.
  - [ ] `evals[2]` — unknown stack + `generic-fallback.md` insufficient → routes to `ywc-tech-research`, no guessed recommendation.
  - [ ] `evals[3]` — user or context implies hand-rolled JWT/password/secret crypto → skill refuses and points to a battle-tested library/managed service instead.
- [ ] Add the security-fail no-cache scenario.
  - [ ] `evals[4]` — `ywc-security-audit` returns ≥1 Critical/High → `DONE_WITH_CONCERNS`, E2E/PR/recommendation-caching all skipped, remediation/re-audit path stated.
- [ ] Add `expected_behavior` and `anti_behavior` arrays to every scenario, cross-checked against the actual merged `SKILL.md` wording (not this task's README summary).
- [ ] Parse and validate the JSON.

## Task Verify

- [ ] `python3 -m json.tool claude-code/skills/ywc-auth-implement/evals/evals.json >/dev/null`
- [ ] `jq -e '.evals | length == 5' claude-code/skills/ywc-auth-implement/evals/evals.json`
- [ ] `jq -e '[.evals[].id] | unique | length == 5' claude-code/skills/ywc-auth-implement/evals/evals.json`

## Verification

- [ ] Run all Task Verify commands above.
- [ ] Leave `SKILL.md`/`README*.md`/`references/**` changes to their owning task (`000063-010`).
- [ ] Full `bash scripts/validate.sh` is deferred to `000063-030`.
