# Implementation Task — 000061-030-docs-auth-implement-catalogs

## Prerequisites

- [ ] `000061-010-domain-auth-implement-skill` is merged.
- [ ] Confirm `codex/skills/ywc-auth-implement/` exists before calculating the count.

## Allowed Edit Scope

Only `codex/skills/README.md`, `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, and `README.es.md`.

## Stop Conditions

- [ ] The live count cannot be determined from `codex/skills/`.
- [ ] Updating a count requires unrelated translation rewrites or a new `README.en.md`.
- [ ] The source skill directory is absent or does not have final naming/description.

## Hardening Gate

- [ ] Record the live count command result before editing README values.
- [ ] Preserve catalog row fields: directory, internal skill name, invocation example, and concise Korean description.
- [ ] Data Integrity and critical-surface review are N/A for static docs; verify every affected locale after edit.

## Implementation Steps

- [ ] Measure the live Codex skill count with the spec command; exclude only `references` and `scripts`.
- [ ] Add one `ywc-auth-implement` row to `codex/skills/README.md` using final source metadata.
- [ ] Update the Codex count in exactly five root READMEs.
  - [ ] Edit `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, and `README.es.md`.
  - [ ] Do not create `README.en.md` or modify `VERSION`/`CHANGELOG.md`.

## Task Verify

- [ ] Run the live-count grep from README.md.
- [ ] `rg -n 'ywc-auth-implement' codex/skills/README.md`
- [ ] `git diff --check -- codex/skills/README.md README.md README.ko.md README.ja.md README.zh.md README.es.md`

## Verification

- [ ] Run all Task Verify commands.
- [ ] Final repository validation is owned by `000062-010`.
