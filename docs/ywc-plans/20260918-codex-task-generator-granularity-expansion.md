# Codex Task Generator Granularity Expansion

> Status: Draft
> Scale: Medium
> Created: 2026-09-18
> Author: Codex
> Spec Reference: GitHub `yongwoon/develop-with-llm` PR #236

## Global Constraints

- `Codex skills live under codex/skills/ in a flat codex/skills/<skill-name>/ structure.` (`codex/AGENTS.md`)
- `For Codex skills, codex/skills/ is the source of truth. The marketplace package under plugins/ywc-agent-toolkit/skills/ is generated from it by bash scripts/sync-codex-plugin.sh; do not edit the generated package first.` (`codex/AGENTS.md`)
- `Codex SKILL.md frontmatter must keep only name and description.` (`CLAUDE.md`)
- `bash scripts/validate.sh` is the local CI mirror; Codex skill contract evals are run by `scripts/run-codex-skill-contract-evals.sh`. (`CLAUDE.md`, `scripts/validate.sh:141-161`)

## Purpose

Align Codex `ywc-task-generator` with the proven granularity contract in PR #236. The current thresholds encourage unnecessary fragmentation for agent-operated work and the optional Planning Advisor always evaluates against the old human threshold, even when `llm` mode was selected.

## Scope

- Raise Codex-only advisory size guidelines to `human: ~15 files / ~500 LOC` and `llm: ~35 files / ~1,200 LOC`.
- Make `llm` vertical bundling explicitly limited to one feature with exclusive Ownership and declared Shared Surfaces.
- Pass the selected mode and its single corresponding guideline to the Planning Advisor; preserve boundary-based reasons to split.
- Add source-level contract eval fixtures for accepted LLM vertical slices, rejected cross-feature bundles, human category splitting, and mode-aware advisor behavior.
- Synchronize the generated marketplace package after source validation.

## Out of Scope

- Claude Code skill changes, parity policy changes, and unrelated task-generator behavior.
- Any change to `codex/agents/*.toml`: `ywc-architect` already has a bounded architecture-advisor contract and must not become the owner of task-size policy.
- Implementing a runtime task generator; this repository distributes instruction and evaluation contracts.
- Changing Safety Invariants, mode selection, task-ID allocation, preview approval, or existing task metadata schemas.

## Quality Gate Contract

This documentation-and-evaluation change uses the following Outcome Oracle as its project-owned quality gate:

- **Target:** Codex `ywc-task-generator` communicates and evaluates the expanded `human`/`llm` granularity contract consistently across `SKILL.md`, the granularity reference, maintained public README guidance, eval fixtures, and the generated marketplace mirror.
- **Quality threshold:** `human` states `~15 files / ~500 LOC`; `llm` states `~35 files / ~1,200 LOC`; LLM bundling remains limited to one feature with exclusive Ownership and declared Shared Surfaces; human mode preserves category splitting; the advisor receives the selected mode and only its matching guideline; no safety invariant is relaxed.
- **Evidence required:** Targeted repository searches and the four new source-level eval fixtures prove the instruction contract; `bash scripts/sync-codex-plugin.sh` proves source-to-mirror propagation; `git diff --check`, `bash scripts/validate.sh`, and `bash scripts/run-codex-skill-contract-evals.sh` pass.
- **Stop condition:** Handoff is permitted only when the source and generated mirror agree, targeted searches find no superseded threshold in the affected Codex task-generator surfaces, all four new eval fixtures pass, and both validation commands pass. If any condition fails, the spec is incomplete and must not be handed to task generation.

## Blind Spot Pass

- **Highest-risk assumption:** The PR #236 behavior and the repository’s current task-generator/eval surfaces are sufficiently represented by the cited anchors to implement the contract without discovering an additional generated or locale-maintained copy.
- **Invalidating evidence:** A repository search or validation result that identifies another maintained task-generator instruction/eval surface, a sync rule that does not cover the named files, or a locale policy requiring additional translated strings.
- **Action:** `proceed` — the Scope, Existing Constraints Touched, FR-3/FR-5, targeted-search verification, and standard sync/validation commands explicitly cover the source, maintained documentation, eval, and generated-package surfaces. Any newly discovered maintained surface is a validation failure that reopens this spec before handoff.

## Module Boundaries

| Module | Owned public interface | Consumers | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|---|
| `codex/skills/ywc-task-generator` | Granularity and advisor instructions | Codex task-generation sessions | Its references and eval contract | Direct edits to generated plugin first; custom-agent policy ownership |
| `plugins/ywc-agent-toolkit/skills` | Generated distribution copy | Marketplace installs | Sync output from `codex/skills` | Hand-authored divergent changes |

## Existing Constraints Touched

| Existing artifact | Behavior (verified) | New interaction |
|---|---|---|
| `codex/skills/ywc-task-generator/SKILL.md:177-191` | Mode is explicit; old sizes are shown to users; four invariants apply in both modes. | Replace all user-facing values and add single-phase invariant without changing mode selection. |
| `codex/skills/ywc-task-generator/SKILL.md:238-272` | One bounded advisor pass receives a small payload but uses the fixed `~10/~300` size check. | Add selected mode + one matching guideline and require mode-aware, boundary-aware size review. |
| `codex/skills/ywc-task-generator/references/granularity-modes.md:19-24,30-36,45-69` | References define old sizes, both-mode invariants, and LLM feature-level ownership. | Revise values and make cross-feature prohibition, exclusive Ownership, and explicit Shared Surfaces unambiguous. |
| `codex/agents/ywc-architect.toml:11-28,42-53` | Agent gives bounded architecture advice, is read-only, and does not own task decomposition. | No change; task-generator supplies the correct bounded payload to whichever advisor pass is used. |
| `scripts/sync-codex-plugin.sh:47-68` | Copies all `codex/skills` content to the generated marketplace package. | Run only after source edits; review the generated mirror, not hand-edit it. |
| `scripts/run-codex-skill-contract-evals.sh:86-112` | Validates each `evals/evals.json` schema and existing task-generator preview tokens. | New fixtures must preserve valid JSON and pass this runner; no runner modification is needed. |

## Acceptance Criteria

- [ ] **AC1 — Mode-consistent guidance:** When a user selects `human` or `llm`, the prompt, task-design rules, reference table, and public README state respectively `~15 files / ~500 LOC` or `~35 files / ~1,200 LOC`, observable by repository-wide targeted searches returning no old `~10/~300` or `~25/~800` granularity guidance in the changed Codex skill.
- [ ] **AC2 — Safe LLM bundling:** When an LLM-mode candidate is within `~35 files / ~1,200 LOC`, it may be retained only when it is one feature with exclusive Ownership and explicit Shared Surfaces; unrelated features or any invariant work are split, observable through explicit instruction and matching eval assertions.
- [ ] **AC3 — Human reviewability:** When `human` mode spans Database/API/UI changes, task decomposition continues to split those categories by default and remains single-PR reviewable, observable through reference rules and an eval fixture.
- [ ] **AC4 — Advisor correctness:** When the optional Planning Advisor runs, its bounded payload names the selected mode and exactly its corresponding guideline; it may still require splitting for deep-module boundaries, multiple major concerns, unsafe Shared Surfaces, cross-feature overlap, or invariant bundling, observable in `SKILL.md` and the advisor eval fixture.
- [ ] **AC5 — Distributable contract:** When validation and package sync run, the source and generated marketplace copies agree and `bash scripts/validate.sh` plus `bash scripts/run-codex-skill-contract-evals.sh` pass.

## Functional Requirements

### FR-1: Update the primary skill contract

Update the reviewability, mode-confirmation, Safety Invariant, Planning Advisor, and LLM task-naming language in `codex/skills/ywc-task-generator/SKILL.md`. State that the sizes are advisory rather than automatic bundling authorization.

### FR-2: Specify mode boundaries in the reference material

Update `references/granularity-modes.md` and the LLM decomposition example so the thresholds, one-feature limit, ownership boundary, Shared Surface requirement, category split, and full invariant set are mutually consistent.

### FR-3: Align public documentation

Update the Korean default `README.md` Granularity Mode section. Update the locale README set only where the repository's translation workflow marks the changed strings as maintained, preserving the Tier 1 file set required by validation.

### FR-4: Lock the instruction contract with evaluations

Append four focused entries to `evals/evals.json`: LLM accepted vertical slice, LLM cross-feature rejection, human category split, and advisor mode awareness. Use source assertions for the relevant instruction/reference file and ban the superseded thresholds.

### FR-5: Regenerate package and verify

Run the standard plugin synchronization, inspect the resulting `plugins/ywc-agent-toolkit/skills/ywc-task-generator/**` mirror, then run the project's full validation and the targeted Codex contract-eval runner.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Compatibility | Keep `--mode` and `--granularity` semantics intact; this is a guideline-only change. |
| Safety | No threshold permits cross-feature bundling or relaxation of Database migration, Library introduction, Phase hard gate, post-task buildability, or single-phase constraints. |
| Maintainability | Each changed rule has a single consistent value and at least one evaluation that detects regression. |

## Data Model

N/A — no data model change.

## API Contract

N/A — no external API contract change.

## Edge Cases

- A candidate under the LLM numeric guideline but containing two unrelated features must split; size is not a bundling license.
- A candidate over either numeric guideline may need decomposition, but deep-module and shared-boundary risks can require a split even below it.
- `ui` and directly coupled `api` work can bundle only under exclusive ownership; shared/reusable APIs stay explicit Shared Surfaces and serialization/conflict metadata remains available.
- An advisor unavailable to the session retains the existing inline bounded-checklist fallback; the revised rule changes its inputs, not its availability behavior.

## Dependencies

- Existing `bash scripts/sync-codex-plugin.sh` distribution workflow.
- Existing `bash scripts/validate.sh` and `bash scripts/run-codex-skill-contract-evals.sh` checks.

## Open Questions

N/A — none identified. The Codex-specific values and guardrails are explicit in PR #236, and this repository has the corresponding skill/eval/package surfaces.

## Implementation Plan

1. [ ] Update `codex/skills/ywc-task-generator/SKILL.md` at Reviewability, Step 5, Planning Advisor, and LLM naming rules; retain the one-advisor budget and all current invocation fallbacks.
2. [ ] Update `codex/skills/ywc-task-generator/references/granularity-modes.md` and the relevant LLM example/decomposition guidance with the complete, non-contradictory contract.
3. [ ] Update `codex/skills/ywc-task-generator/README.md` (and only required maintained locale counterparts) so public documentation agrees with runtime instructions.
4. [ ] Add the four regression-focused eval records to `codex/skills/ywc-task-generator/evals/evals.json`; do not alter `codex/agents/ywc-architect.toml` or the generic contract runner unless the new fixtures reveal an actual runner limitation.
5. [ ] Run targeted contract checks, synchronize `plugins/ywc-agent-toolkit/skills/`, inspect the generated diff, then run the full validation mirror.

## Verification

```bash
bash scripts/run-codex-skill-contract-evals.sh
bash scripts/sync-codex-plugin.sh
git diff --check
bash scripts/validate.sh
```

Also use targeted `rg` checks to confirm no superseded size-guideline strings remain in the affected Codex task-generator source and generated mirror, while intentionally not scanning unrelated historical plans or fixtures.

## Risks and Rollback

- **Risk:** Larger numeric limits are misread as permission to create cross-feature tasks. **Mitigation:** repeat the one-feature, exclusive-Ownership, explicit-Shared-Surfaces, and invariant rules in primary instructions, reference material, example, and evals.
- **Risk:** A new value drifts between README, `SKILL.md`, references, and plugin output. **Mitigation:** source assertions, targeted search, and sync-before-full-validation order.
- **Rollback:** Revert the source skill/reference/README/eval commit and re-run `bash scripts/sync-codex-plugin.sh`; generated content is reproducible from source.

## References

- GitHub `yongwoon/develop-with-llm` PR #236 — task-generator granularity expansion and mode-aware advisor correction.
- `codex/skills/ywc-task-generator/SKILL.md:177-191,238-272`
- `codex/skills/ywc-task-generator/references/granularity-modes.md:14-69`

## Amendment Log

### Iteration 1 — 2026-09-18

- Driven by: `completeness:outcome-oracle-missing-or-nontestable`
- Signatures: `completeness:outcome-oracle-missing-or-nontestable`

| Section edited | What changed | Why |
|---|---|---|
| Quality Gate Contract | Replaced `N/A` with explicit Target, Quality threshold, Evidence required, and Stop condition. | The validator requires a compact, testable Outcome Oracle before task-generation handoff. |
| Blind Spot Pass | Added the highest-risk assumption, invalidating repository evidence, and `proceed` routing. | The validator requires a resolved or explicitly routed Blind Spot Pass. |
