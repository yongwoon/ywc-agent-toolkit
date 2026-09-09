# Codex `ywc-impl-review`: scope guardrail and independent verification

## Purpose

Port the behavior introduced by
[develop-with-llm PR #227](https://github.com/yongwoon/develop-with-llm/pull/227)
to this repository's Codex distribution: reject unusable/oversized review
scopes before worker dispatch, and independently re-derive every Phase 1
Critical/High confirmed finding before reporting it as fact.

The goal is to reduce both wasted multi-agent review runs and high-severity
false positives without changing the existing five review axes or the Phase 2
advisor budget.

## Scope

- Add a Step 2.5 scope guardrail and a Step 4.5 independent-verification pass
  to `codex/skills/ywc-impl-review/SKILL.md`.
- Preserve the PR #227 final semantics: 200-file / 5,000-line hard limits,
  20 verifier-call cap, Critical-before-High dispatch ordering, and distinct
  `verification-failed` versus `verification-error` outcomes.
- Apply the guardrail consistently to every existing target mode: diff-derived
  `--base`, `--git-range`, and `--working-tree` use both thresholds; `--code`
  uses only the file threshold because it has no intrinsic diff line count.
- Make the report template expose verification provenance and aggregate counts.
- Add behavioral contract-eval scenarios for empty/excessive scope and for all
  independent-verification outcomes.
- Update the English source README and all localized README surfaces so they
  describe the new review flow without Codex-inapplicable Sonnet/Haiku/Opus
  model claims.
- Regenerate `plugins/ywc-agent-toolkit/skills/` from the authoritative
  `codex/skills/` source only after source edits and validation.

## Out of Scope

- Changes to `codex/agents/*.toml`. The pass is orchestration in the skill;
  it does not alter any custom agent's read-only mission, model, or output
  contract.
- Changes to Claude Code skills/agents or an attempt to synchronize both
  runtime families. Their content is maintained independently.
- Changing `--advisor-budget`, the five Phase 1 axes, or the existing Phase 2
  advisor selection policy. Independent verifier calls are intentionally not
  advisor calls.
- Implementing a new verifier script, persistence format, or arbitrary
  changed-line estimate for `--code` mode.

## Global Constraints

- `codex/skills/` is the source of truth; do not edit
  `plugins/ywc-agent-toolkit/skills/` first (`codex/AGENTS.md`).
- Codex SKILL frontmatter must contain only `name` and `description`
  (`CLAUDE.md`, `scripts/validate.sh`).
- The generated plugin must be synchronized with
  `bash scripts/sync-codex-plugin.sh`; `bash scripts/validate.sh` rejects a
  stale package (`codex/AGENTS.md`, `scripts/validate.sh`).
- Tier 1 README locales (`README.md`, `.en.md`, `.ja.md`, `.ko.md`) are
  required; maintained Tier 2 Chinese and Spanish files must stay aligned.

## Existing Constraints Touched

| Artifact | Verified current behavior | Planned interaction |
|---|---|---|
| `codex/skills/ywc-impl-review/SKILL.md:62` | Workflow has Steps 0–7; it dispatches Phase 1 immediately after resolving the target in Step 2. | Insert Step 2.5 without renumbering existing integer steps; insert Step 4.5 between candidate aggregation and Phase 2. |
| `codex/skills/ywc-impl-review/SKILL.md:56` | `--advisor-budget` applies only to Phase 2 and defaults to 5. | State that independent verifier calls do not consume it; failed/error verification joins the existing Phase 2 candidate queue. |
| `codex/skills/ywc-impl-review/SKILL.md:181` | Report exposes Phase 1/Phase 2 provenance but no verification state. | Add per-finding Verification line plus a summary that separately counts reproduced, could-not-reproduce, execution-error, and cap-skipped outcomes. |
| `codex/skills/ywc-impl-review/evals/evals.json` | Contains structural behavior scenarios for target selection and architecture-evidence packets. | Add focused orchestration assertions rather than a runtime fixture or a custom-agent implementation. |
| `codex/AGENTS.md:12` | Marketplace skill files are generated from `codex/skills/`. | Sync only after all source, docs, and eval edits are complete. |

## Module Boundaries

| Module | Owner | Responsibility | Consumer |
|---|---|---|---|
| `ywc-impl-review/SKILL.md` | Codex skill | Defines scope refusal, independent verifier packet/outcome routing, and final report contract. | Codex users and delegated review workers. |
| `ywc-impl-review/evals/evals.json` | Codex skill evals | Guards the documented behavior contract. | `scripts/run-codex-skill-contract-evals.sh`. |
| `codex/agents/*.toml` | Codex agents | Existing read-only specialist roles. | `ywc-impl-review` routing. |

No agent boundary changes are required: a verification packet is deliberately
minimal (`file:line` + claimed severity), so it reuses existing reviewer
dispatch capability without expanding an agent's authority or public contract.

## Acceptance Criteria

- **AC1 — empty scope is refused:** an empty `--git-range`, an empty `--code`
  path, or an otherwise empty selected target returns `NEEDS_CONTEXT` with a
  narrowing/check-target action and no Phase 1 dispatch.
- **AC2 — excessive scope is refused deterministically:** `--git-range` blocks
  above 200 files or 5,000 added-plus-removed lines and reports exact counts
  plus the five largest files; the same rule applies to diff-derived `--base`
  and `--working-tree`. `--code` blocks above 200 files but never fabricates a
  changed-line count when no diff exists.
- **AC3 — blind verifier protocol:** every eligible Phase 1 Critical/High
  confirmed finding is independently dispatched with only cited location and
  claimed severity—not the original rationale—and verifier dispatches are
  capped at 20 (Critical, then High, preserving discovery order within tier).
- **AC4 — honest verification state:** reproduced findings carry evidence;
  clean non-reproduction becomes `verification-failed`; timeout/tool/malformed/
  missing-result becomes `verification-error`; capped-out items are explicitly
  unverified. None is presented as an unqualified confirmed fact.
- **AC5 — Phase 2 compatibility:** failed/error findings are prioritized into
  the existing Phase 2 pool before its budget cap is selected when enabled and
  correctly report as unverified under `--no-advisor`; verifier calls do not
  reduce `--advisor-budget`.
- **AC6 — report and docs parity:** the skill report and all six README locale
  surfaces explain verification provenance/counts and the unchanged five-axis
  review model without claiming Claude-only model assignments.
- **AC7 — package integrity:** source validation and plugin synchronization
  both succeed; generated plugin content matches `codex/skills/`.

## Functional Requirements

### FR-1: Scope guardrail

After target resolution and before any Phase 1 worker is dispatched, calculate
the reviewable file count. For `--base`, `--git-range`, and `--working-tree`,
calculate added-plus-removed line count and list the five files with the
largest changed-line count on refusal. For `--code`, enforce only the file
count. Use the current target-mode rules; do not introduce a second
target-selection path or manufacture a diff metric for a path-only review.

### FR-2: Independent verification

After Phase 1 aggregation and before Phase 2 selection, independently verify
Critical/High confirmed findings. The verifier receives a blind packet and
must derive the defect itself. Dispatch at most 20, ordered Critical then High.
Merge failed/error verifier results into the candidate collection before the
existing Phase 2 budget cap and priority ordering are applied.

### FR-3: Outcome routing

`reproduced` is reportable with verifier evidence. `verification-failed` and
`verification-error` are separate statuses; both enter the pre-existing Phase
2 candidate pool ahead of ordinary same-severity candidates when Phase 2 is
enabled. Under `--no-advisor`, show an explicit unverified state. Cap-skipped
findings likewise remain explicit unverified findings, never plain Confirmed.

### FR-4: Report contract

Extend the Summary and each finding template with verification state. Preserve
`[P1]`/`[P2]` provenance and severity symbols; verification status is an
additional dimension, not a replacement for phase provenance.

### FR-5: Documentation and distribution contract

Update the English README source and each maintained locale so the user-facing
description matches FR-1 through FR-4 and does not promise Claude-only model
assignments. Generate the marketplace mirror exclusively from validated
`codex/skills/` source, then prove source/package parity and leave
`codex/agents/*.toml` untouched.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Cost/latency | Scope refusal precedes fan-out; verifier fan-out is bounded to 20. |
| Reliability | Failure to execute a verifier must never look like a clean non-reproduction or an independently confirmed finding. |
| Auditability | Refusal reports counts/largest files; verification reports counts and per-finding status. |
| Compatibility | Existing advisor budget, report phase markers, and custom-agent read-only constraints stay intact. |

## Edge Cases

- Exactly 200 files / exactly 5,000 lines: permit review; values above either
  threshold hard-block.
- More than 20 eligible findings: dispatch Critical first, preserve discovery
  order within severity, and mark every remainder cap-unverified.
- A verifier returns malformed data or times out: classify as
  `verification-error`, never `verification-failed`.
- `--no-advisor` with failed/error verification: still run the independent
  check, then report unverified rather than silently discarding or confirming.
- A Phase 2 budget cannot accommodate all verification-derived candidates:
  follow its existing priority and over-budget reporting contract.

## Data Model / API Contract

N/A — this is an instruction and report-contract change. The relevant internal
record shape is conceptual: `{ finding, phase, severity, verification_status,
verification_evidence? }`; no persisted schema or external API is introduced.

## Quality Gate Contract

N/A — repository validation is structural. The implementation must pass the
existing validation, contract-eval, localization, and generated-package checks.

## Outcome Oracle

| Element | Contract |
|---|---|
| Target | Codex `ywc-impl-review` reliably refuses unusable review scopes and reports Critical/High Phase 1 findings as fact only after independent corroboration. |
| Quality threshold | All AC1–AC7 are represented in skill instructions, eval expectations, localized docs, and generated-package parity; verification state is never silently collapsed. |
| Evidence required | `jq empty` for eval JSON, contract-eval runner success, source/package `diff -qr`, `bash scripts/validate.sh`, and a final source diff showing no `codex/agents/*.toml` edit. |
| Stop condition | The listed commands succeed, all blocking validation findings are resolved, and the only generated changes are the plugin mirror of approved Codex skill source edits. |

## Implementation Steps

- [ ] In `codex/skills/ywc-impl-review/SKILL.md`, add the Rationalization
  Defense entry and Advisor Pattern boundary explaining that independent
  verification is mandatory for Phase 1 Critical/High findings and separate
  from Phase 2 budgeted advice.
- [ ] Add Step 2.5 with target-mode-specific empty and oversized-scope
  enforcement for `--base`, `--git-range`, `--working-tree`, and `--code`;
  define the exact thresholds, refusal response, and top-five changed-file
  calculation without inventing `--code` diff metrics.
- [ ] Add Step 4.5 with blind verifier payload, 20-call ordering/cap,
  reproduced/failed/error/cap-skipped outcomes, and `--no-advisor` routing.
- [ ] Update Step 4/5 and Output Format so verification-derived candidates are
  merged before the existing Phase 2 budget selection, prioritized correctly,
  and reported with aggregate and per-finding verification evidence/status.
- [ ] Add `codex/skills/ywc-impl-review/evals/evals.json` scenarios for empty
  and excessive scope, successful independent reproduction, failed/error
  verification routing, `--no-advisor`, and dispatch-cap behavior.
- [ ] Revise `README.en.md` as the source description, then align
  `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, and
  `README.es.md` to the same behavior and generic Codex worker terminology.
- [ ] Run `bash scripts/sync-codex-plugin.sh` only after source edits, then
  inspect the generated `plugins/ywc-agent-toolkit/skills/ywc-impl-review/`
  diff for source/package parity.

## Verification

```bash
jq empty codex/skills/ywc-impl-review/evals/evals.json
bash scripts/run-codex-skill-contract-evals.sh
bash scripts/sync-codex-plugin.sh
diff -qr codex/skills/ywc-impl-review plugins/ywc-agent-toolkit/skills/ywc-impl-review
bash scripts/validate.sh
```

Also inspect the final diff to confirm that `codex/agents/*.toml` is unchanged
and the generated plugin is the only package-side mutation.

## Risks and Rollback

- **Risk:** blind verifier instructions accidentally include the original
  rationale, biasing the re-derivation. **Mitigation:** spell out the minimal
  packet and add an eval assertion prohibiting original-finding content.
- **Risk:** verification call failures are mistaken for a negative result.
  **Mitigation:** retain the distinct `verification-error` label through
  summary, candidate routing, and `--no-advisor` output.
- **Risk:** synchronizing before source is complete creates noisy generated
  changes. **Mitigation:** source-first ordering and final `diff -qr` check.
- **Rollback:** revert the source skill/eval/README commit, then rerun
  `bash scripts/sync-codex-plugin.sh` to regenerate the package from the
  restored source; no data migration or agent deployment rollback is needed.

## Open Questions

N/A — PR #227 resolves the operational policy (thresholds, cap, and outcomes),
and the local repository already provides the relevant Codex skill, eval, and
package-sync conventions.

## Planning Evidence and Confidence Gate

- Upstream evidence: PR #227 final commits `7674802` and `28754aa` specify the
  guardrail, blind verifier, 20-call cap, and error-state distinction.
- Local evidence: `codex/skills/ywc-impl-review/SKILL.md` currently has no
  Step 2.5/4.5 or verification report field; its README files still name
  Claude-only models; source and plugin are currently identical.
- Complement check: every existing Codex custom agent is a read-only
  specialist; none owns a verification-pass lifecycle, so no agent definition
  is a required change site.

Confidence Gate Report

- Aggregate: **95/100 — PROCEED**
- Scope clarity: 96 — exactly one Codex skill family, its eval/docs, and its
  generated package are in scope; agents are explicitly out.
- Architecture compliance: 94 — inserts use existing Phase 1 → Phase 2 flow
  and preserve budget/agent boundaries.
- Evidence quality: 96 — based on upstream final patch and current local
  SKILL/eval/README/package inspection.
- Reuse verified: 91 — reuses existing target selection, Phase 2 queue,
  evaluator format, localization policy, and package sync rather than adding
  machinery.
- Root cause identified: 95 — the gap is missing scope containment and
  independent corroboration of high-severity Phase 1 claims.

The deterministic gate scorer returned `PROCEED` with no override.

## Amendment Log

### Iteration 1 — 2026-09-09

**Driven by**: spec-ready validation — 2 Critical findings (missing explicit
Outcome Oracle; incomplete target-mode contract for the scope guardrail).

**Signatures**: `completeness:outcome-oracle-contract-missing`,
`consistency:scope-guardrail-target-mode-coverage-ambiguous`

| Section edited | What changed | Why |
|---|---|---|
| `## Scope` | Declared the mode-by-mode threshold policy. | The prior text did not say whether existing diff-derived `--base` and `--working-tree` targets receive the 5,000-line guardrail. |
| `## Acceptance Criteria` | Made AC2 and AC5 explicit about all diff-derived target modes and the ordering of candidate merging versus Phase 2 budget selection. | Cross-section consistency: requirements must produce the advertised behavior for every supported target mode. |
| `### FR-1: Scope guardrail` and `### FR-2: Independent verification` | Specified per-mode metrics and that failed/error verifier results enter the candidate collection before Phase 2 capping. | Removes an implementation-order ambiguity that could otherwise omit verification-derived findings. |
| `## Outcome Oracle` | Added Target, Quality threshold, Evidence required, and Stop condition. | The readiness contract requires all four testable completion elements explicitly. |
| `### FR-5: Documentation and distribution contract` | Added a dedicated requirement for AC6–AC7. | Completeness: report behavior alone did not formally require localized documentation or generated-package parity. |
