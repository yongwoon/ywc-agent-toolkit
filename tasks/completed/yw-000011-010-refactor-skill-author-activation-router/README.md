# yw-000011-010-refactor-skill-author-activation-router

## Purpose

Reduce activation-time context for the Codex `ywc-skill-author` without changing its bounded authoring or report-only audit behavior.

## Scope

Compact the source router, extract only conditional create/restructure detail, preserve the inline canonical rule and audit index, add the routing scenario and durable manual evidence, review metadata, and regenerate the plugin mirror.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-small_codex-skill-creator-token-efficiency.md` — authoritative goal, scope, acceptance criteria, and verification requirements.
- `docs/ywc-plans/20260901-small_codex-skill-creator-token-efficiency.spec-ready-log.md` — known validation caveat for the local-reference check.

### Summary

The source `SKILL.md` must fall from its recorded 4,724 `o200k_base` tokens to at most 4,251 while retaining the executable authoring and audit contract inline. Create/restructure runs must load the new detailed authoring reference before edits; audit runs must remain report-only and must not load it. Record the required baseline, A1–A16/audit rule ledger, and four fresh-context forward-test records in the prescribed evidence file.

### Out of Scope (from spec)

- Installed OpenAI system `$skill-creator` changes.
- `claude-code/**` edits or cross-platform wording parity.
- New meta-skills, relaxed `ywc-*` conventions, or claims of universal behavioral equivalence.

## Criticality

normal

The spec's use of “token” concerns activation-token measurement, not credentials or authentication tokens; no critical surface is in scope.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- (None — this batch has no successor task)

## Key Files

- `codex/skills/ywc-skill-author/SKILL.md` — compact, always-loaded router and canonical rule/audit index.
- `codex/skills/ywc-skill-author/references/authoring-rules.md` — conditional create/restructure detail.
- `codex/skills/ywc-skill-author/evals/evals.json` — structural contracts including compact-routing.
- `codex/skills/ywc-skill-author/agents/openai.yaml` — reviewed interface metadata.
- `docs/ywc-plans/evidence/20260901-small_codex-skill-creator-token-efficiency.md` — immutable baseline, rule ledger, forward-test artifacts, and verdict.
- `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` — generated mirror from source sync.

## Notes

- Use the spec's exact `o200k_base` command and thresholds; do not replace an unavailable tokenizer or encoding.
- The local-reference check must inspect direct local Markdown links only. It must not treat bundle-level prose references such as `references/advisor-pattern.md` as skill-local targets.
- No production architecture-contract manifest applies to these bounded paths.

## Hardening Evidence

### Test Feedback Path

- RED-first target: retain the current authoring and audit prompts from `codex/skills/ywc-skill-author/evals/evals.json`, then record four fresh-context response artifacts in `docs/ywc-plans/evidence/20260901-small_codex-skill-creator-token-efficiency.md`.
- Existing coverage: `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author` and `bash scripts/run-codex-skill-contract-evals.sh`.

### Interface Contract

- N/A — no public API, exported type, or cross-task interface. The inline rule/audit index and conditional routing are behavioral requirements verified by the required fresh-context artifacts.

### Critical Surface Review

- Review requirement: N/A — documentation/skill routing only; run the targeted structural and manual behavior checks below.

### Data Integrity Hardening

- Trigger surface: N/A — documentation and generated plugin files only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: `bash scripts/sync-codex-plugin.sh` is the sole generated-mirror writer.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-skill-author/SKILL.md`
- `codex/skills/ywc-skill-author/references/authoring-rules.md`
- `codex/skills/ywc-skill-author/evals/evals.json`
- `codex/skills/ywc-skill-author/agents/openai.yaml` (review; edit only if interface drift is proven)
- `docs/ywc-plans/evidence/20260901-small_codex-skill-creator-token-efficiency.md`
- Generated output: `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**`

### Shared Surfaces

- Codex source-to-plugin synchronization via `scripts/sync-codex-plugin.sh`.
- `ywc-skill-author` activation and audit behavior consumed by later skill-authoring work.

### Conflicts With

- Any task or local change editing `codex/skills/ywc-skill-author/**` or `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` — overlapping router or generated output.

### Parallelizable After

- Root task — no predecessor required.

### Task Verify

- `python3 -c 'import tiktoken; print(len(tiktoken.get_encoding("o200k_base").encode(open("codex/skills/ywc-skill-author/SKILL.md").read())))'`
- `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/sync-codex-plugin.sh && bash scripts/validate.sh`

## Out of Scope

- Editing `claude-code/**`, installed skills outside the repository, or unrelated `ywc-*` skills.
- Adding libraries, scripts, or documentation not required by the specification.
