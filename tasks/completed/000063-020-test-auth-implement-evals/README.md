# 000063-020-test-auth-implement-evals

## Purpose

Fix `ywc-auth-implement`'s routing and safety-rejection behavior as deterministic eval fixtures so future edits to the skill body cannot silently regress its safety gates.

## Scope

- Author `claude-code/skills/ywc-auth-implement/evals/evals.json` with 5 scenarios matching the actual `ywc-commit/evals/evals.json` field shape (`skill_name`, `description`, `last_updated`, `evals[]` with `id`/`name`/`prompt`/`context`/`expected_behavior`/`anti_behavior` — no `"harness"` field required; the spec's own prose calls this "prompt/expected_output" loosely, but the repository's actual convention uses `expected_behavior`/`anti_behavior` arrays, which this task follows).
- Cover: happy path, existing-auth hard stop, unknown-stack routing, direct-crypto rejection, security-fail no-cache.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude_auth_implement_skill.md#acceptance-criteria` — AC9 (5-scenario requirement, no `"harness"` field)
- `docs/ywc-plans/claude_auth_implement_skill.md#fr-9-output-contract-readme-catalogs` — evals authoring instruction, pattern source (`ywc-commit/evals/evals.json`)
- `claude-code/skills/ywc-commit/evals/evals.json` — the natural-language `prompt`/`expected_output` pattern to follow

### Summary

These fixtures are documentation-grade regression checks — they assert what the finished `SKILL.md` should say and do for five scenarios, not runnable application tests (this repository has no CI-discovered eval harness for `claude-code` skills, per `claude-code/skills/CLAUDE.md`). Each scenario's `expected_output` must be traceable to specific language actually present in the final `000063-010` `SKILL.md`.

### Out of Scope (from spec)

- Skill body, references, and README authoring — handled by `000063-010-domain-auth-implement-skill`
- Repository-wide `bash scripts/validate.sh` and §3.5 verbatim-contract verification — handled by `000063-030-docs-auth-implement-verification`

## Criticality

`critical` — Ownership path `claude-code/skills/ywc-auth-implement/evals/**` matches the security-sensitive keyword heuristic (`auth`); these fixtures are the regression gate for the skill's safety-rejection behavior (existing-auth hard stop, direct-crypto rejection, no-cache-on-fail). Heuristic inference, logged per the fallback rule.

## Dependencies

### Depends On

- `000063-010-domain-auth-implement-skill` — needs the final routing/policy/gate prose in `SKILL.md` to write matching scenario text; must not be written against a draft.

### Depended By

- `000063-030-docs-auth-implement-verification` — needs a valid, parseable `evals.json` for the final `bash scripts/validate.sh` and JSON-parse check (AC9).

## Key Files

- `claude-code/skills/ywc-auth-implement/evals/evals.json` — the 5 routing/safety scenarios

## Notes

- Do not place real secrets, tokens, or credentials in any `prompt` or `expected_output` value.
- `references/rationalization-evidence.md` is read-only input for this task and remains `000063-010`'s ownership — do not edit it here.
- Match scenario language to the actual final wording in `SKILL.md`; if wording drifts after this task starts, re-read the merged `SKILL.md` rather than relying on the description above.

## Parallel Execution Metadata

### Ownership

`claude-code/skills/ywc-auth-implement/evals/**` only.

### Shared Surfaces

`SKILL.md` routing/status vocabulary (read-only) and the repository's natural-language eval JSON pattern (`prompt`/`expected_output`, no `"harness"` field).

### Conflicts With

`000063-010-domain-auth-implement-skill` before its merge; otherwise `(None identified)`.

### Parallelizable After

`000063-010-domain-auth-implement-skill` merged.

### Task Verify

- `python3 -m json.tool claude-code/skills/ywc-auth-implement/evals/evals.json >/dev/null`
- `jq -e '.evals | length == 5' claude-code/skills/ywc-auth-implement/evals/evals.json`

## Out of Scope

Changing the skill body, metadata, references, or catalogs.
