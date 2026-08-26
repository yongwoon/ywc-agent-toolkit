# 000064-020-domain-isolated-runner-adapter — Implementation Checklist

## Prerequisites

- [ ] `000064-010-infra-evaluator-discovery-schema-registry` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within the runner, adapter, runner-test, and runner-fixture paths in `README.md`.
- [ ] Stop before changing fixture schema, registry policy, CI workflow, or distributable skills.

## Stop Conditions

- [ ] Stop if a target/dependency cannot resolve from `codex/skills/<name>/` with `SKILL.md`.
- [ ] Stop if the supported Codex CLI cannot produce a documented final-output format or text fallback.
- [ ] Stop if credentials require reading persistent `CODEX_HOME` or logging process secrets.
- [ ] Stop if a verifier needs a shell interpreter, unspecified environment, or writable source checkout.

## Hardening Gate

- [ ] Classify this task as security-sensitive behavior change.
- [ ] Start with failing fake-adapter tests for no-provider, stale-artifact isolation, undeclared writes, and timeout.
- [ ] Record runner request/result inputs, outputs, and error statuses before invoking a real CLI.
- [ ] Apply retryable-command hardening: unique workspace/run ID, cleanup boundary, and duplicate-attempt test.
- [ ] Require full implementation review before `DONE`.

## Implementation Steps

- [ ] Implement runner workspace preparation in `runner.py`.
  - [ ] Resolve `fixture_root`, fixture files, and outputs through realpath containment checks.
  - [ ] Copy only declared fixture files to a fresh temporary workspace and reject escaped symlinks.
  - [ ] Build a fresh temporary `CODEX_HOME` with only target skill and declared dependencies.
- [ ] Implement pre/post filesystem snapshots.
  - [ ] Permit only declared output paths, runner transient paths, and declared fixture scratch paths.
  - [ ] Return `FAIL` with a bounded diff summary for undeclared added, changed, deleted, or redirected files.
  - [ ] Snapshot `source_checkout_readonly` verifier roots and fail on tracked-file mutation.
- [ ] Add a minimal `codex_adapter.py` protocol and fake adapter.
  - [ ] Capture supported CLI version and non-secret command arguments.
  - [ ] Parse structured final output with a documented text fallback, and map timeout/cancel/parser errors.
  - [ ] Support only `unavailable`, `injected_ci_secret`, and `ephemeral_session_material`; no provider returns `SKIPPED_UNAVAILABLE`.
- [ ] Execute deterministic verifier checks through registry-owned configuration only, then cover all runner paths with fake-adapter tests.

## Task Verify

- [ ] `python3 -m unittest discover -s .codex/skills/ywc-codex-toolkit-eval/scripts -p 'test_runner.py'`
- [ ] Run two fake-adapter attempts and assert the second cannot observe the first workspace, temporary `CODEX_HOME`, or artifact directory.

## Verification

- [ ] Runner tests pass.
- [ ] `bash scripts/validate.sh` passes.
- [ ] No-provider execution returns `SKIPPED_UNAVAILABLE`, never a pass and never persistent configuration fallback.
