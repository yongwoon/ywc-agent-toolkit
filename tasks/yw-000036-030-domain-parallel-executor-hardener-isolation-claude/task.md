# yw-000036-030-domain-parallel-executor-hardener-isolation-claude — Implementation Checklist

## Prerequisites
- [ ] `yw-000036-010-domain-parallel-executor-state-schema` is completed (merged) — `integration_branch`/`hardener_verdict`/`promotion_retry_count` fields and their subcommands exist in `claude-code/skills/scripts/update-state.py`.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/ywc-parallel-executor/SKILL.md`, `references/wave-integration-branch.md` (new), `references/checkpoint-resume.md`, `references/aggregate-pr.md`.

## Stop Conditions
- [ ] Stop if `**4e.5.` already sits after a `wave-complete`-stamping step in the file (would mean the ordering defect is already fixed by other work — investigate rather than duplicate).
- [ ] Stop if the mode-mapping table (`SKILL.md:306-312` region) already references `wave-int/` (already implemented).
- [ ] Stop if implementing this task requires changing `ywc-finish-branch/SKILL.md` itself — its existing `--base-branch` argument must be sufficient; if it is not, stop and report rather than editing that file.
- [ ] Stop if the required `SKILL.md` body growth would push the file meaningfully further over its ~500-line soft cap — move more content into `references/wave-integration-branch.md` instead.

## Implementation Steps
- [ ] **Pre-flight scan (new subsection, before Step 4a)**:
  - [ ] For each wave in the `--waves` input, read every member task's declared `quality_gate_contract` field from its task directory's spec/README.
  - [ ] OR across the wave's tasks against the exact `N/A — no quality gate contract` sentinel (`references/quality-gates.md` §7) to compute `has_contract`.
  - [ ] Missing field, malformed field, or an absent task directory each stop Pre-flight with `NEEDS_CONTEXT`, naming the offending task and field — never a silent `false`.
  - [ ] Pass the computed `has_contract` boolean as part of each `--waves` entry into `init-parallel`.
- [ ] **Step 4e amendment**:
  - [ ] After the Pre-flight scan has run, Step 4e creates `wave-int/<N>` if and only if that wave's `integration_branch` is already non-`None` in `.ywc-run-state.json` (never re-derives the contract check).
  - [ ] Idempotent creation: check whether `wave-int/<N>` exists (locally or on origin) before creating; if it exists, reuse it — merge remaining `pending` tasks onto it as if uninterrupted; only branch from base when absent.
  - [ ] Push `wave-int/<N>` to origin immediately at creation, before the first task's `ywc-finish-branch` call.
  - [ ] Extend the `--local-merge`, `--draft`, `--aggregate-pr` mode-mapping rows with `--base-branch wave-int/<N>`; leave the `--per-task-pr` row (`:270-302`) unchanged.
  - [ ] Reword the "Delivery into the base branch is required for every mode" sentence (`:264`) so "the base branch" is not misread as the per-task merge target for the three isolated modes; add the clause that post-promotion base content equals the integration branch.
- [ ] **New promotion step** (label it `4e.6` unless a stronger reason emerges to use something else — see README Notes), inserted after `4e.5` Hardener and before `4g` Clean Up:
  - [ ] Applies only to a wave that created `wave-int/<N>`; a contract-less wave is unaffected (already delivered at 4e).
  - [ ] On a passing Hardener: fast-forward base to `wave-int/<N>`, then push (`--local-merge`) or defer (`--draft`/`--aggregate-pr`); state the postcondition that `HEAD` ends on `<base-branch>`.
  - [ ] Stamp `wave-complete` only after a successful promotion.
  - [ ] On fast-forward failure (base advanced): merge base into `wave-int/<N>` (never rebase, cite `references/pr-conflict-resolution.md`), re-run Hardener against the merged result before retrying promotion.
  - [ ] Two-counter bound: Mutation Loop Cap is fresh per Hardener dispatch (3 attempts each); `promotion_retry_count` (via `yw-000036-010`'s `promotion-retry` subcommand) caps live-lock retries at 2, with `BLOCKED` reason `promotion-churn` distinct from a textual-conflict `BLOCKED`.
  - [ ] On a blocking gate result: base untouched, `wave-complete` not stamped, integration branch and every task worktree preserved, Step 4g skipped for the wave's tasks.
  - [ ] A Hardener dispatch failure (`DONE_WITH_CONCERNS`) must still allow promotion — state this explicitly.
- [ ] **Carve-out rule and `--per-task-pr` advisory cap**: state the rule ("an isolation branch can only protect state whose point-of-no-return sits after the gate") then its consequence for `--per-task-pr` (wave-boundary Hardener is reporting-only, may not return `BLOCKED` even under `enforced`; blocking authority stays at 4c.5); link `references/quality-gates.md` for the enforcement-eligibility statement rather than restating it.
- [ ] **Step 4i third bucket**: add the tasks-`DONE`-but-wave-Hardener-`BLOCKED` bucket, keyed off the wave's `status`/`hardener_verdict`/`integration_branch` state rather than task-directory location (which looks identical to a completed wave since Mark Complete runs before the gate).
- [ ] **New `references/wave-integration-branch.md`**: lifecycle (create/reuse `wave-int/<N>`, push-at-creation), promotion procedure (fast-forward, postcondition), promotion-conflict handling (merge-and-rerun, two-counter bound, `BLOCKED` reasons). Link it from the body with `> **Action required**: Read [...]`; do not restate its content by value in the body.
- [ ] **`references/checkpoint-resume.md` amendment**: amend the `task-merged`/`wave-complete` rows for the new meaning; add: (a) fully-merged-not-promoted resume (`pending` empty, `status != completed`); (b) partial-merge resume (`pending` non-empty, `wave-int/<N>` exists — reuse and merge remaining); (c) `hardener_verdict` branching (absent/`PASS` auto-retry, `BLOCKED` requires explicit user confirmation); (d) a contract-less wave keeps today's resume behavior unchanged.
- [ ] **`references/aggregate-pr.md` amendment**: the end-of-run `git reset --hard origin/<base>` (`:87-89`) must not run while an un-promoted integration branch exists — either carve the aggregate branch only after the last wave's promotion, or refuse the reset with a clear message.

## Task Verify
- [ ] `grep -n "^\*\*4e\.\|^\*\*4e\.5\.\|^\*\*4e\.6\.\|^\*\*4g\." claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm ascending order with the promotion step between Hardener and Clean Up.
- [ ] `grep -n "wave-int/" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `grep -c "isolation branch can only protect state whose point-of-no-return" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `grep -n "Action required" claude-code/skills/ywc-parallel-executor/SKILL.md` — confirms the new reference is linked, not inlined.
- [ ] `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] Confirm no `gate_state` value is written to `.ywc-run-state.json` anywhere in the new prose (`grep -n "gate_state" claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-parallel-executor/references/*.md` — any match must describe it as living in the Completion Report / subagent payload, never `.ywc-run-state.json`).

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
