# yw-000006-010-docs-task-generator-artifacts-sync — Implementation Checklist

## Prerequisites
- [ ] `yw-000005-020-docs-task-generator-skill-initials` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only files under `claude-code/skills/ywc-task-generator/references/`, `README*.md`, and `evals/evals.json`. Do not touch `SKILL.md` or `scripts/`.

## Stop Conditions
- [ ] Stop if `evals.json` fails to parse after the edit.
- [ ] Stop if a template change would make legacy `## Phase NNNNNN` headings unparsable by the compactor.
- [ ] Stop if a locale would be left describing the old unprefixed grammar.

## Hardening Gate
- [ ] Confirm `evals.json` parses and the added scenario matches the existing legacy-coexistence narration style.
- [ ] Confirm all six locales were updated in the same commit.
- [ ] Mark Data Integrity Hardening N/A — documentation and fixtures only.

## Implementation Steps
- [ ] Update `references/dependency-graph.md.template` phase headings to `## Phase <initials>-NNNNNN` and update every example task ID to the prefixed form.
- [ ] Add a one-line note to that template stating legacy `## Phase NNNNNN` headings remain valid and compact correctly.
- [ ] Update `references/execution-convention.md` `mv` examples and directory-tree examples to prefixed IDs, keeping one legacy example to show coexistence.
- [ ] Update `README.md` (Korean default) with the prefixed ID format and a one-sentence description of initials namespacing.
- [ ] Apply the same substantive update to `README.en.md` as the English source.
- [ ] Apply the same substantive update to `README.ja.md`, `README.ko.md`, `README.zh.md`, and `README.es.md`.
- [ ] Read the existing legacy-coexistence scenarios in `evals/evals.json` and mirror their field shape and narration style.
- [ ] Add one eval scenario covering initials resolution together with legacy coexistence: a tree holding only unprefixed legacy IDs, initials resolved to `yk`, expecting the first PHASE to seed from legacy max + 1 and the emitted directory to match `^yk-[0-9]{6}-[0-9]{3}-`.
- [ ] Validate `evals/evals.json` parses.

## Task Verify
- [ ] `python3 -m json.tool claude-code/skills/ywc-task-generator/evals/evals.json > /dev/null`
- [ ] `grep -q 'Phase <initials>-' claude-code/skills/ywc-task-generator/references/dependency-graph.md.template`
- [ ] All six `README*.md` files appear in `git diff --name-only`
- [ ] `grep -c '@ywc-' claude-code/skills/ywc-task-generator/references/*.md` returns 0

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] markdownlint passes with the CI config and scope
- [ ] typecheck passes (N/A — documentation only)
- [ ] unit tests pass (eval JSON parses)
- [ ] app builds without error (N/A — documentation/tooling repository)
