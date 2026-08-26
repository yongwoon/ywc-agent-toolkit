# 000027-060-test-codex-parity-evals — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] Existing eval files use the simple Codex fixture schema and no migration is required.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-project-docs/evals/evals.json` and `codex/skills/ywc-project-scaffold/evals/evals.json`.

## Stop Conditions
- [ ] Stop if fixture schema differs from `prompt` / `expected_output` and requires harness changes.
- [ ] Stop if adding fixture coverage requires changing skill instructions outside eval files.
- [ ] Stop if JSON validity cannot be preserved with the existing formatting style.

## Implementation Steps
- [ ] Update `codex/skills/ywc-project-docs/evals/evals.json`.
  - [ ] Add a fixture prompting `ywc-project-docs` to route product material into `docs/product/`.
  - [ ] Include expected output that checks architecture/specification cross-reference behavior.
  - [ ] Preserve existing array/object shape and indentation.
- [ ] Update `codex/skills/ywc-project-scaffold/evals/evals.json`.
  - [ ] Add a fixture for Rust + Axum + REST API + Layered Architecture.
  - [ ] Include expected output that checks relevant scaffold documents and architecture language.
  - [ ] Preserve existing array/object shape and indentation.

## Task Verify
- [ ] `python3 -m json.tool codex/skills/ywc-project-docs/evals/evals.json >/dev/null`
- [ ] `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null`
- [ ] `rg -n "docs/product|cross-reference|Axum|Layered Architecture|Rust" codex/skills/ywc-project-docs/evals/evals.json codex/skills/ywc-project-scaffold/evals/evals.json`

## Verification
- [ ] Repository validation is deferred to `000028-010-infra-plugin-sync-validation`.
- [ ] `git diff --name-only` for this task contains only the two eval JSON files.
