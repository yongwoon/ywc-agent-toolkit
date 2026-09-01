# 000070-010-domain-ywc-implement-skill — Implementation Checklist

## Prerequisites
- [ ] Repository guidance and `docs/ywc-plans/codex-sdlc-v11-gap-closure.md` have been read.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-implement/**`.
- [ ] Stop before editing adjacent skills or generated package output.

## Stop Conditions
- [ ] Stop if the spec cannot be represented without changing executor ownership.
- [ ] Stop if the required direct-lane contract would exceed 500 lines without a justified reference extraction.
- [ ] Stop if eval conventions or Codex metadata requirements conflict with repository validation.

## Hardening Gate
- [ ] Classify as a new workflow skill and metadata/eval behavior change.
- [ ] Record RED-first evidence in `evals/evals.json`, then use focused contract evaluation before finalizing the skill.
- [ ] Record the public invocation/report contract in `README.md`.
- [ ] Require full `ywc-impl-review` before any delivery status; `BLOCKED`, `NEEDS_CONTEXT`, or unresolved Critical/High findings cannot commit.

## Implementation Steps
- [ ] Create `codex/skills/ywc-implement/SKILL.md` with Codex-only frontmatter, announce line, focused triggers, anti-triggers, and the input gate for exactly one approved `--spec` or `--ticket`.
- [ ] Document approval evidence, acceptance-criteria checks, ticket snapshot resolution, clean-tree baseline capture, and feature-branch requirements.
- [ ] Document existing-pattern inspection, TDD/focused verification, full configured verification, review routing, bounded correction, and conventional commit rules.
- [ ] Add `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md` consistent with the skill contract.
- [ ] Add `agents/openai.yaml` with valid display name, short description, and default prompt.
- [ ] Add `evals/evals.json` covering approved spec, approved ticket, missing approval/AC, vague idea, task range, broad generation, baseline/review routing, and no-push boundaries.

## Task Verify
- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-implement`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] Repository validation is not the terminal gate for this task; run it after all source tasks merge.
- [ ] Confirm no new runtime dependency or helper script was added.

## Implementation Notes
