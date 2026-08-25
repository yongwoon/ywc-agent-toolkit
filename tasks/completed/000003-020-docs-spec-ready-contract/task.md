# 000003-020-docs-spec-ready-contract - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] Source PR #120 Codex package and diffs are available for comparison.
- [ ] `docs/ywc-plans/codex-pr110-120-129-port.md` status is `Ready for task generation`.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-spec-ready/**`.
- [ ] Limit existing-skill edits to `codex/skills/ywc-spec-validate/SKILL.md`, `codex/skills/ywc-spec-validate/README*.md`, and `codex/skills/ywc-agentic/SKILL.md`.
- [ ] If catalog, `.codex-plugin`, or unrelated skill edits are needed, stop and report before proceeding.

## Stop Conditions

- [ ] Stop if source PR text requires automatic `ywc-agentic` routing through `ywc-spec-ready`.
- [ ] Stop if the `ywc-spec-validate` report contract cannot preserve existing Programmatic Consumer Policy semantics.
- [ ] Stop if any copied source path references `tools/codex-skill`.

## Implementation Steps

- [ ] Add the `ywc-spec-ready` package.
  - [ ] Create `SKILL.md` with Codex-only frontmatter.
  - [ ] Create README locale set and `agents/openai.yaml`.
  - [ ] Add `references/convergence.md` and `references/loop-log.md`.
- [ ] Implement the readiness loop contract in documentation.
  - [ ] Document mutually exclusive goal vs `--spec <path>` input.
  - [ ] Document `--max-iterations`, `--max-advisor-calls`, `--log`, `--dry-run`, `--format`, and `--focus`.
  - [ ] Document safe failure-context handling and preserving the original spec path.
- [ ] Update `ywc-spec-validate`.
  - [ ] Add `--advisor-budget <n>` argument documentation.
  - [ ] Change report header language to `Phase 2 advisor calls used: X of N`.
  - [ ] Add `Advisor budget status` allowed values.
  - [ ] Add Programmatic Consumer Policy note for `advisor_budget_status` and max-1 generic retry behavior.
- [ ] Update `ywc-agentic` only within the approved boundary.
  - [ ] Apply Codex-native `AGENTS.md` / `CODEX.md` wording if present in source PR #120.
  - [ ] Preserve current phase routing.
  - [ ] Ensure any `ywc-spec-ready` mention is absent or explicitly deferred/follow-up.
- [ ] Update README locale files for user-facing changes in `ywc-spec-ready` and `ywc-spec-validate`.

## Task Verify

- [ ] `find codex/skills/ywc-spec-ready -maxdepth 3 -type f | sort`
- [ ] `rg -n -- "--advisor-budget|Phase 2 advisor calls used: X of N|Advisor budget status|advisor_budget_status" codex/skills/ywc-spec-validate/SKILL.md`
- [ ] `rg -n "ywc-task-generator <spec-path>|DONE_WITH_CONCERNS|convergence" codex/skills/ywc-spec-ready/SKILL.md`
- [ ] `rg -n "ywc-spec-ready" codex/skills/ywc-agentic/SKILL.md || true`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`
