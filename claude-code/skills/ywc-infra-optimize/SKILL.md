---
name: ywc-infra-optimize
description: >-
  (ywc) Use when improving existing infrastructure: cost right-sizing,
  removing unused resources, reserved/spot adoption, drift detection &
  remediation, and reliability hardening for AWS/GCP/Azure/K8s — the safe
  change-loop equivalent of refactor-clean for infra. Triggers: "인프라 개선",
  "비용 최적화", "right-sizing", "drift 점검", "미사용 리소스 정리", "cost
  optimization", "optimize infrastructure", "terraform drift", "インフラ最適化",
  "ywc-infra-optimize". Do not use for greenfield infrastructure design (use
  ywc-infra-design), first-time IaC authoring (use ywc-iac-author), pre-apply
  review only (use ywc-infra-review), or app-code performance / code hotspots
  (use ywc-performance-engineer).
category: maintenance
phase: cleanup
requires: []
advisor_budget: 2
---

# ywc-infra-optimize

**Announce at start:** "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."

This skill is the infra counterpart to `ywc-refactor-clean`: cost right-sizing, unused-resource removal, reserved/spot adoption, drift detection & remediation, and reliability hardening against infrastructure that already exists. It borrows refactor-clean's Iron Law discipline — three independent witnesses before any change lands — and its per-item, bisectable commit shape. Terraform is the single fixed IaC tool for this toolkit (design §7); every execution stops at `terraform plan`, never `apply`. This skill diagnoses **and** executes SAFE items; CAUTION and DANGER items are escalated, never auto-executed — a destroy on a stateful resource is DANGER regardless of how confident the classification tool is.

## The Iron Law

```text
NEVER EXECUTE A CHANGE WITHOUT (1) COST/UTILIZATION DATA CONFIRMS THE CANDIDATE + (2) A PER-ITEM TERRAFORM PLAN CONFIRMS THE EXACT BLAST RADIUS + (3) THE CHANGE IS REVERSIBLE OR A SNAPSHOT EXISTS BEFORE IT LANDS
```

A resource a cost report flags "idle" but a per-item `terraform plan` shows referenced by another module or a DR failover path is **not** SAFE — that is a live dependency hiding behind a stale metric. An instance CloudWatch/Cloud Monitoring shows at 4% average CPU but that is a nightly-batch instance's daytime trough is **not** confirmed over-provisioned — utilization data needs a representative window (see [`../references/lenses/cost.md`](../references/lenses/cost.md)'s p95 guidance), not a single snapshot. Single-source confidence is not confirmation; the discipline requires an independent data witness (cost/utilization report) plus a blast-radius witness (`terraform plan`) plus a reversibility guarantee — mirroring refactor-clean's tool + grep + test triad.

If a SAFE execution is committed and a downstream signal regresses (error rate, alert, cost anomaly, availability drop), **revert that commit first**, then re-classify the item to CAUTION or DANGER. Do not chase the failure forward with a follow-up "fix" commit — the original commit is the regression.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "I'll batch all the SAFE changes into one commit — faster to review" | Bisectability is the entire point, same as `ywc-refactor-clean`: when a cost anomaly or alert surfaces two weeks later, `git bisect` must land on the exact change that caused it. A batched commit forces a human to re-classify every item by hand. |
| "The cost tool says this resource is idle, so it's safe to destroy — skipping the third witness" | A cost report is one signal, not confirmation. It cannot see a DR failover target, a quarterly batch job's off-cycle trough, or a cross-module reference the `terraform plan` blast-radius witness would catch. Skipping the plan witness or the reversibility check turns "the tool said so" into the sole basis for an irreversible action. |
| "This CAUTION item looks low-risk, I'll auto-execute it anyway" | CAUTION exists precisely because "looks low-risk" is a judgment this skill is not authorized to make alone — reserved/spot adoption commits spend, and ambiguous utilization needs a human, not a confident guess. |
| "I'll skip the per-item plan confirmation since the batch plan already looked clean" | A batch-level `terraform plan` can hide a wider blast radius inside one item. Per-item confirmation is what proves the exact resource changed, and nothing else did — the batch-level view cannot substitute for it. |
| "I'm already running `ywc-infra-review`, I'll execute the fix in the same pass" | `ywc-infra-review` is diagnosis-only by design and has no write access. Executing changes inside a review pass collapses the review/execute boundary the rest of the infra skill suite depends on — remediation is always a separate pass. |
| "The `terraform plan` for this DB destroy came back clean, so it's fine to proceed" | `plan` succeeding proves syntactic validity, not safety. A destroy against a stateful resource is DANGER regardless of how confident the plan or the classification tool is — it escalates, it never auto-executes. |

**Violating the letter of these rules is violating the spirit.** An optimization pass that batches commits, trusts a single signal, or auto-executes past CAUTION/DANGER turns a cost-saving change loop into an outage risk.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--scope` | `--scope <path>` | `--scope infra/modules/compute` | Restrict gather/classify/execute to a single Terraform module or path. Default: full IaC tree / live infrastructure. |
| `--dry-run` | flag | `--dry-run` | Run gather + classify only (Steps 1–2); emit the SAFE/CAUTION/DANGER report without executing any SAFE item. |
| `--skip-verify-done` | flag | `--skip-verify-done` | Skip the final `ywc-verify-done` handoff. Only valid when the upstream caller (e.g., a scheduled hygiene orchestrator) will run it. |

## Workflow

### Step 1: Determine scope + gather current state

Determine scope from `--scope`, or default to the full IaC tree / live infrastructure. Run `terraform plan` (or `terraform plan -detailed-exitcode`) directly against the scoped module tree — this is the drift-detection signal: live infrastructure that has diverged from the committed `.tf` state.

Dispatch `Task(subagent_type: ywc-performance-engineer)` in read-only diagnostic mode, carrying the scoped Terraform and an explicit pointer to [`../references/lenses/cost.md`](../references/lenses/cost.md) and [`../references/finops.md`](../references/finops.md), to produce the cost/utilization report: idle or orphaned resources, over-provisioned compute (against observed p95), and pricing-model mismatches (on-demand load that should be reserved/spot).

> **Fan-out return contract**: this skill dispatches two workers (Steps 1 and 3). Each dispatch MUST inject the §3.5 return-payload directive from [`../references/subagent-status-actions.md`](../references/subagent-status-actions.md) — every dispatch returns `Status | 1-line summary | artifact path | Concerns (≤10 lines)`, with full findings/plans written to a file whose path is returned.

### Step 2: Classify into SAFE / CAUTION / DANGER

Sort every candidate into exactly one tier. Items that match multiple tiers escalate to the highest tier — same rule as `ywc-refactor-clean`.

| Tier | Pattern | Action |
|---|---|---|
| **SAFE** | *Cost/drift*: confirmed-idle resource (zero utilization over a representative window + `terraform plan` shows no other module references it); a clearly over-provisioned instance (e.g., <10% p95 CPU) with an unambiguous right-size target; drift where live state simply matches an already-approved-but-unapplied `.tf` change. *Reliability hardening* (additive, reversible, no recreation): enabling automated backups / point-in-time recovery on a store that lacks them, adding a missing health/readiness check, raising an autoscaling floor to `min ≥ 2`, enabling deletion protection — checked against [`../references/lenses/reliability.md`](../references/lenses/reliability.md) | Execute via Step 3 |
| **CAUTION** | Reserved/Spot adoption (commits spend or trades availability); a resource with moderate or ambiguous utilization; drift where live diverges from code in a way that looks intentional (manual hotfix); right-sizing a resource with recent scaling history; adding a multi-AZ standby or read replica (cost + failover implications) | Step 4 — escalate, do not execute |
| **DANGER** | Any destroy or recreate against a stateful resource (database, volume, bucket) regardless of tool confidence — including a reliability change whose plan would recreate rather than update the resource; a resource tagged/tied to compliance or DR; anything `git log` shows touched in the last 7 days | Step 4 — escalate, never execute in this skill |

### Step 3: SAFE execution loop (dispatch `ywc-cloud-engineer`)

For each SAFE item, in order — reliability-hardening SAFE items flow through this identical loop, checked against [`../references/lenses/reliability.md`](../references/lenses/reliability.md) instead of the cost lens:

1. **Re-confirm the signal is still current.** Data gathered in Step 1 (cost/utilization for cost items, the config gap itself for reliability items) can go stale on a large scope — re-check the specific resource before executing.
2. **Capture the pre-change plan baseline.** Run a per-item `terraform plan` on the target resource before dispatching the change — pre-state evidence that nothing beyond the classified candidate is already drifting.
3. **Dispatch** `Task(subagent_type: ywc-cloud-engineer)` scoped to the single item, carrying the classification rationale and an instruction to make the minimal `.tf` change (delete the idle resource block, adjust `instance_type` / node pool size, add a spot/reserved configuration, or add the missing backup/health-check/autoscaling-floor/deletion-protection setting) and run `terraform plan` — never `apply`.
4. **Confirm the post-change plan matches only the intended delta — the loop's third witness.** Compare the AFTER-change plan against the Step 2 baseline and the expected blast radius from classification: only the intended resource changes, zero unexpected destroys elsewhere. This pre-state-evidence-plus-post-change-diff comparison mirrors `ywc-refactor-clean`'s tests-green-before / tests-green-after shape, and it is what makes the eventual `git revert` a clean, exact undo. A plan wider than the baseline delta, or one that doesn't match expectation, is not SAFE; re-classify to CAUTION and skip.
5. **Commit** with shape `chore(infra): remove idle <resource> (cost lens)`, `fix(infra): right-size <resource> (cost lens, <from> → <to>)`, `fix(infra): remediate drift on <resource>`, or `fix(infra): enable <backup/health-check/autoscaling-floor> on <resource> (reliability lens)` — name the source lens. One item per commit; bisectability is the entire point, same as `ywc-refactor-clean`.

Do **not** batch multiple SAFE items into one commit.

### Step 4: CAUTION / DANGER — escalate, do not execute

For each CAUTION or DANGER item, emit a report entry (Output Format below) with the rationale and a concrete suggested next step — `ywc-iac-author` for a reviewed re-authoring, or a direct question back to the user for a reserved/spot capacity commitment. Do not execute either tier in this skill; DANGER especially never auto-executes regardless of how the classification tool scored it.

### Step 5: Verify-done handoff

Hand off to `ywc-verify-done` with the optimization report (Output Format below). Mandatory unless `--skip-verify-done` was passed by an upstream caller that will perform its own verify.

## Output Format

```text
Infra Optimize Report
─────────────────────────────────────────────────
Scope:           infra/  (or --scope value)
Drift detected:  2 resources diverged from committed .tf state
Cost/utilization signal: ywc-performance-engineer (cost lens)

Executed (SAFE):
  - chore(infra): remove idle aws_eip.unused-1                          (1 commit)
  - fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large   (1 commit)

Escalated (CAUTION — not executed):
  - aws_instance.batch-runner   moderate utilization, recent scaling history — needs manual review

Escalated (DANGER — not executed):
  - aws_db_instance.legacy      plan shows a destroy — stateful, requires explicit human approval

Verification (per ywc-verify-done):
  $ terraform plan (per-item)
  exit 0  (PASS — blast radius matched expectation on all 2 SAFE items)
─────────────────────────────────────────────────
Estimated monthly delta: -$340 (order of magnitude, cost lens estimate)
```

## Validation Checklist

Before declaring the optimization pass complete, verify:

- [ ] Drift detection (`terraform plan`) ran against the declared scope
- [ ] Cost/utilization signal was gathered via `ywc-performance-engineer` before classification
- [ ] Every candidate is classified into exactly one tier (SAFE / CAUTION / DANGER); multi-tier matches escalate to the highest
- [ ] Every SAFE item captured a pre-change `terraform plan` baseline AND a post-change plan whose diff matched only the intended delta before commit (the loop's third witness)
- [ ] Reliability-hardening candidates (missing backups/PITR, health checks, autoscaling floors, deletion protection) were classified alongside cost/drift candidates, not skipped
- [ ] Every SAFE execution is its own commit (no batching)
- [ ] No CAUTION or DANGER item was executed — both are reported, not applied
- [ ] No `terraform apply` was run at any point
- [ ] Final `ywc-verify-done` block uses the canonical wording (PASS / FAIL), unless `--skip-verify-done` was passed

## Common Mistakes

- **Treating a clean per-item `terraform plan` as sufficient for a stateful destroy.** `plan` proves syntactic correctness, not safety — a destroy against a database is DANGER regardless of how clean the plan looks.
- **Re-using Step 1's cost/utilization snapshot for every item without re-checking.** Signals age; a resource idle three days ago at gather-time may be back in active use by execute-time on a slow-moving scope.
- **Batching SAFE items into one commit "to save review time."** Bisectability is lost the moment two unrelated resource changes share a commit.
- **Running this skill during a `ywc-infra-review` pass instead of separately.** Review is diagnosis-only and has no write access by design; mixing execution into a review pass collapses a boundary the rest of the toolkit relies on.

## Integration

- **Upstream**: `ywc-infra-review` (diagnosis that surfaces the cost/drift/reliability findings this skill remediates); direct user invocation for a scheduled optimization pass.
- **Downstream**: `ywc-verify-done` (mandatory final claim, unless skipped); `ywc-create-pr` (optimization branches ship as their own PRs); `ywc-iac-author` (re-authoring path for escalated CAUTION/DANGER items).
- **Consults**: `ywc-performance-engineer` (cost/utilization signal, Step 1); `ywc-cloud-engineer` (SAFE execution worker, Step 3).
- **Must not be paired with**: greenfield topology design (`ywc-infra-design`), first-time authoring (`ywc-iac-author`), or a pre-apply-only review pass (`ywc-infra-review`) — those own separate lifecycle phases.

## References

| Reference | Use when |
|---|---|
| [`../references/lenses/cost.md`](../references/lenses/cost.md) | Step 1 — cost/utilization signal gathering, right-sizing and waste taxonomy |
| [`../references/finops.md`](../references/finops.md) | Step 1 — the detailed FinOps taxonomy (reserved/spot, data-transfer cost) `ywc-performance-engineer` reviews against |
| [`../references/lenses/reliability.md`](../references/lenses/reliability.md) | Step 2/3 — classification taxonomy for reliability-hardening SAFE/CAUTION candidates (backups, health checks, autoscaling floors, deletion protection, multi-AZ) and the guardrail against a cost change dropping below the reliability floor |
| [`../references/subagent-status-actions.md`](../references/subagent-status-actions.md) | Steps 1 and 3 — the §3.5 return-payload contract each dispatch must inject so fan-out returns stay bounded |
| [`../ywc-verify-done/SKILL.md`](../ywc-verify-done/SKILL.md) | Step 5 — per-batch verification block shape (command + exit code + claim) — mandatory unless `--skip-verify-done` |
