# yw-000001-010-config-initials-writer — Implementation Checklist

## Prerequisites
- [ ] Confirm the current `.codex/ywc.json` shape and preserve pre-existing keys.

## Allowed Edit Scope
- [ ] Modify only `codex/skills/ywc-setup/**` and the project `.codex/ywc.json` config contract.

## Stop Conditions
- [ ] Stop if preserving unknown config keys requires changing language-resolution semantics.
- [ ] Stop if a dependency on task-generator internals appears.
- [ ] Stop if atomic replacement or locking cannot be implemented with the supported Bash/Python standard-library toolchain.

## Hardening Gate
- [ ] Record RED-first config/concurrency evidence before production edits.
- [ ] Record the CLI/config interface contract in the implementation notes.
- [ ] Apply the Data Integrity Hardening reference for the locked read-modify-write.
- [ ] Require full implementation review before completion.

## Implementation Steps
- [ ] Extend `codex/skills/ywc-setup/SKILL.md`, `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md` with the optional `--initials` contract.
- [ ] Add `codex/skills/ywc-setup/scripts/write-config.sh` with `set -euo pipefail`, scope validation, missing-operand handling, and exact initials validation.
- [ ] Implement the locked JSON merge in a Python standard-library helper or embedded helper: preserve `lang` and unknown keys, use a unique same-directory temporary file, fsync, replace, and validate the result.
- [ ] Add setup eval/smoke coverage for initials-only, lang-only, combined, malformed config, invalid initials, missing operands, and concurrent updates.
- [ ] Keep `.codex/ywc.json` valid with the selected project defaults `{ "lang": "en", "initials": "yw" }`.

## Task Verify
- [ ] `bash -n codex/skills/ywc-setup/scripts/*.sh`
- [ ] Run the focused config smoke and concurrent-write checks.
- [ ] `python3 -m json.tool .codex/ywc.json >/dev/null`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Bash/Python skill tooling)
- [ ] unit tests pass (focused setup fixtures)
- [ ] integration tests pass (concurrent config smoke)
- [ ] app builds without error (N/A — documentation/tooling repository)

