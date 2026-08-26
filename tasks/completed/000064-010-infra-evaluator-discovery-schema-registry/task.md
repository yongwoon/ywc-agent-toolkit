# 000064-010-infra-evaluator-discovery-schema-registry — Implementation Checklist

## Prerequisites

- [ ] No predecessor task is required.

## Allowed Edit Scope

- [ ] Stay within the `README.md` Ownership paths.
- [ ] If a change requires runner, workflow, or distributable fixture edits, stop and report.

## Stop Conditions

- [ ] Stop if V2 requirements need arbitrary fixture command text or inherited environment access.
- [ ] Stop if a registry entry cannot declare a fixed argv/cwd/timeout/mode contract.
- [ ] Stop if path containment requires changing the repository-wide bundle validation policy.

## Hardening Gate

- [ ] Classify this task as behavior change / security-sensitive evaluator infrastructure.
- [ ] Add a failing discovery or fixture-validation test before production edits.
- [ ] Record the V2 manifest and verifier registry interface contract before runner integration.
- [ ] Mark Data Integrity fields `N/A`; no mutable production data is written.
- [ ] Require full implementation review for command allowlist and realpath-containment code.

## Implementation Steps

- [ ] Update `inventory_gate.py` discovery and tests.
  - [ ] Enumerate only immediate `codex/skills/*` directories that contain `SKILL.md`.
  - [ ] Add a temporary-repository regression fixture proving `references/` and `scripts/` are excluded.
  - [ ] Emit warning-only linter findings with rule ID, source line, and reasoned suppression support.
- [ ] Add `fixture_validator.py` and its test module.
  - [ ] Normalize legacy V1 fixtures without mutating them and report remaining V1 count.
  - [ ] Validate V2 `schema: 2`, required case fields, exact category enum, and `should_trigger` boolean.
  - [ ] Reject V1/V2 ambiguity, unsupported check types, absolute paths, `..`, free-form commands, unknown dependencies, and escaped fixture-root symlinks.
- [ ] Add evaluator-owned `verifier_registry.py`.
  - [ ] Define typed registry entries with `fixture_workspace` or `source_checkout_readonly` mode.
  - [ ] Require fixed argv, runner-owned cwd, timeout, allowed environment, expected exit status, and readonly roots when applicable.
  - [ ] Register `bundle.validate` as `source_checkout_readonly`; do not make it runnable in selected-skill workspaces.
- [ ] Wire validator/registry diagnostics into evaluator-facing commands without changing V1 fixture content.

## Task Verify

- [ ] `python3 -m unittest discover -s .codex/skills/ywc-codex-toolkit-eval/scripts -p 'test_*.py'`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json --skip-gate`

## Verification

- [ ] Python unit tests pass with the command above.
- [ ] `bash scripts/validate.sh` passes.
- [ ] No executable command or executable path is accepted from a V2 fixture.
