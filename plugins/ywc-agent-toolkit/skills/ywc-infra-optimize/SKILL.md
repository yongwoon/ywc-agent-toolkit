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
---

# ywc-infra-optimize

**Announce at start:** "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."

This skill is the infra counterpart to `ywc-refactor-clean`: cost right-sizing, unused-resource removal, reserved/spot adoption, drift detection, and reliability hardening planning against infrastructure that already exists. It borrows refactor-clean's Iron Law discipline — three independent witnesses before any change is recommended — but, in Codex v1, it is a **planning and classification surface**, not an execution worker. Terraform is the single fixed IaC tool for this toolkit; every analysis stops at `terraform plan`, never `apply`. SAFE, CAUTION, and DANGER classify how conservative the recommended next action should be; actual `.tf` edits route back through `ywc-iac-author`.

## The Iron Law

```text
NEVER RECOMMEND A CHANGE AS READY WITHOUT (1) COST/UTILIZATION DATA CONFIRMS THE CANDIDATE + (2) A PER-ITEM TERRAFORM PLAN CONFIRMS THE EXACT BLAST RADIUS + (3) THE CHANGE IS REVERSIBLE OR A SNAPSHOT EXISTS BEFORE IT LANDS
```

A resource a cost report flags "idle" but a per-item `terraform plan` shows referenced by another module or a DR failover path is **not** SAFE — that is a live dependency hiding behind a stale metric. An instance CloudWatch/Cloud Monitoring shows at 4% average CPU but that is a nightly-batch instance's daytime trough is **not** confirmed over-provisioned — utilization data needs a representative window (see `../references/infra/lenses/cost.md`'s p95 guidance), not a single snapshot. Single-source confidence is not confirmation; the discipline requires an independent data witness (cost/utilization report) plus a blast-radius witness (`terraform plan`) plus a reversibility guarantee — mirroring refactor-clean's tool + grep + test triad.

If a previously recommended SAFE change later proves risky, re-classify the item to CAUTION or DANGER before any authoring pass. Do not keep presenting it as SAFE once new evidence contradicts the original witnesses.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "I'll batch all the SAFE changes into one recommendation and let someone figure it out later" | The point of SAFE is narrow blast radius and clear next action. A vague multi-item blob hides which change is actually low risk and which one needs a different owner. |
| "The cost tool says this resource is idle, so it's safe to destroy — skipping the third witness" | A cost report is one signal, not confirmation. It cannot see a DR failover target, a quarterly batch job's off-cycle trough, or a cross-module reference the `terraform plan` blast-radius witness would catch. Skipping the plan witness or the reversibility check turns "the tool said so" into the sole basis for an irreversible action. |
| "This CAUTION item looks low-risk, I'll auto-execute it anyway" | CAUTION exists precisely because "looks low-risk" is a judgment this skill is not authorized to make alone — reserved/spot adoption commits spend, and ambiguous utilization needs a human-reviewed authoring pass, not a confident guess. |
| "I'll skip the per-item plan confirmation since the batch plan already looked clean" | A batch-level `terraform plan` can hide a wider blast radius inside one item. Per-item confirmation is what proves the exact resource changed, and nothing else did — the batch-level view cannot substitute for it. |
| "I'm already running `ywc-infra-review`, I'll execute the fix in the same pass" | `ywc-infra-review` is diagnosis-only by design and has no write access. This skill is also diagnosis-and-planning only in Codex v1; remediation is always a separate authoring pass. |
| "The `terraform plan` for this DB destroy came back clean, so it's fine to proceed" | `plan` succeeding proves syntactic validity, not safety. A destroy against a stateful resource is DANGER regardless of how confident the plan or the classification tool is — it escalates, it never auto-executes. |

**Violating the letter of these rules is violating the spirit.** An optimization pass that trusts a single signal or turns planning into stealth execution turns a cost-saving loop into an outage risk.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--scope` | `--scope <path>` | `--scope infra/modules/compute` | Restrict gather/classify/execute to a single Terraform module or path. Default: full IaC tree / live infrastructure. |
| `--dry-run` | flag | `--dry-run` | Run gather + classify only and skip optional advisory follow-ups. Since this skill does not execute changes, `--dry-run` mainly suppresses extra planning detail. |
| `--skip-verify-done` | flag | `--skip-verify-done` | Skip the final `ywc-verify-done` handoff. Only valid when the upstream caller (e.g., a scheduled hygiene orchestrator) will run it. |

## Workflow

### Step 1: Determine scope + gather current state

Determine scope from `--scope`, or default to the full IaC tree / live infrastructure. Run `terraform plan` (or `terraform plan -detailed-exitcode`) directly against the scoped module tree — this is the drift-detection signal: live infrastructure that has diverged from the committed `.tf` state.

Dispatch a Codex worker carrying the `ywc-performance-engineer` persona in read-only diagnostic mode, carrying the scoped Terraform and an explicit pointer to `../references/infra/lenses/cost.md` and `../references/finops.md`, to produce the cost/utilization report: idle or orphaned resources, over-provisioned compute (against observed p95), and pricing-model mismatches (on-demand load that should be reserved/spot).

> **Fan-out return contract**: this skill dispatches two workers (Steps 1 and 3). Each dispatch must return the bounded status payload from `../references/subagent-status-actions.md` §3.5 — `Status | 1-line summary | artifact path | Concerns (<=10 lines)`, with full findings/plans written to a file whose path is returned.

### Step 2: Classify into SAFE / CAUTION / DANGER

Sort every candidate into exactly one tier. Items that match multiple tiers escalate to the highest tier — same rule as `ywc-refactor-clean`.

| Tier | Pattern | Action |
|---|---|---|
| **SAFE** | *Cost/drift*: confirmed-idle resource (zero utilization over a representative window + `terraform plan` shows no other module references it); a clearly over-provisioned instance (e.g., <10% p95 CPU) with an unambiguous right-size target; drift where live state simply matches an already-approved-but-unapplied `.tf` change. *Reliability hardening* (additive, reversible, no recreation): enabling automated backups / point-in-time recovery on a store that lacks them, adding a missing health/readiness check, raising an autoscaling floor to `min >= 2`, enabling deletion protection — checked against `../references/infra/lenses/reliability.md` | Step 3 — prepare a low-risk remediation plan |
| **CAUTION** | Reserved/Spot adoption (commits spend or trades availability); a resource with moderate or ambiguous utilization; drift where live diverges from code in a way that looks intentional (manual hotfix); right-sizing a resource with recent scaling history; adding a multi-AZ standby or read replica (cost + failover implications) | Step 4 — escalate, do not execute |
| **DANGER** | Any destroy or recreate against a stateful resource (database, volume, bucket) regardless of tool confidence — including a reliability change whose plan would recreate rather than update the resource; a resource tagged/tied to compliance or DR; anything `git log` shows touched in the last 7 days | Step 4 — escalate, never execute in this skill |

### Step 3: SAFE planning loop

For each SAFE item, in order — reliability-hardening SAFE items flow through this identical loop, checked against `../references/infra/lenses/reliability.md` instead of the cost lens:

1. **Re-confirm the signal is still current.** Data gathered in Step 1 (cost/utilization for cost items, the config gap itself for reliability items) can go stale on a large scope — re-check the specific resource before executing.
2. **Capture the per-item plan baseline.** Run a per-item `terraform plan` on the target resource before recommending remediation — pre-state evidence that nothing beyond the classified candidate is already drifting.
3. **Optionally consult** the read-only `ywc-cloud-engineer` persona when feasibility, provider nuance, or blast-radius interpretation is unclear. That consult stays advisory: it does not author files.
4. **Record the recommended next action.** For example: `ywc-iac-author` should remove an idle resource block, adjust `instance_type`, add a backup setting, or fix drift with the minimal `.tf` edit. Include the expected blast radius in the recommendation.
5. **Reject false SAFE cases.** If the per-item plan is wider than expected, or the consult exposes hidden coupling, re-classify the item to CAUTION and do not recommend it as SAFE.

### Step 4: Escalate by tier, do not execute

For each SAFE, CAUTION, or DANGER item, emit a report entry (Output Format below) with the rationale and a concrete suggested next step — usually `$ywc-iac-author` for a reviewed remediation patch, or a direct question back to the user for a reserved/spot capacity commitment. SAFE means "low-risk to author next", not "execute here". DANGER especially never auto-executes regardless of how the classification tool scored it.

### Step 5: Verify-done handoff

Hand off to `$ywc-verify-done` with the optimization report (Output Format below). Mandatory unless `--skip-verify-done` was passed by an upstream caller that will perform its own verify.

## Output Format

```text
Infra Optimize Report
─────────────────────────────────────────────────
Scope:           infra/  (or --scope value)
Drift detected:  2 resources diverged from committed .tf state
Cost/utilization signal: ywc-performance-engineer persona (cost lens)

Planned next actions (SAFE):
  - aws_eip.unused-1            remove via $ywc-iac-author; expected plan: destroy only this idle EIP
  - aws_instance.worker         right-size via $ywc-iac-author: m5.4xlarge -> m5.large

Escalated (CAUTION — not auto-authored):
  - aws_instance.batch-runner   moderate utilization, recent scaling history — needs manual review

Escalated (DANGER — not auto-authored):
  - aws_db_instance.legacy      plan shows a destroy — stateful, requires explicit human approval

Verification (per ywc-verify-done):
  $ terraform plan (per-item, evidence only)
  exit 0  (PASS — blast radius matched expectation on all 2 SAFE candidates)
─────────────────────────────────────────────────
Estimated monthly delta: -$340 (order of magnitude, cost lens estimate)
```

## Validation Checklist

Before declaring the optimization pass complete, verify:

- [ ] Drift detection (`terraform plan`) ran against the declared scope
- [ ] Cost/utilization signal was gathered via the `ywc-performance-engineer` persona before classification
- [ ] Every candidate is classified into exactly one tier (SAFE / CAUTION / DANGER); multi-tier matches escalate to the highest
- [ ] Every SAFE item captured a per-item `terraform plan` baseline and an expected narrow blast radius before being recommended
- [ ] Reliability-hardening candidates (missing backups/PITR, health checks, autoscaling floors, deletion protection) were classified alongside cost/drift candidates, not skipped
- [ ] No SAFE / CAUTION / DANGER item was executed in this skill — all are reported with next actions only
- [ ] No `terraform apply` was run at any point
- [ ] Final `$ywc-verify-done` block uses the canonical wording (PASS / FAIL), unless `--skip-verify-done` was passed

## Common Mistakes

- **Treating a clean per-item `terraform plan` as sufficient for a stateful destroy.** `plan` proves syntactic correctness, not safety — a destroy against a database is DANGER regardless of how clean the plan looks.
- **Re-using Step 1's cost/utilization snapshot for every item without re-checking.** Signals age; a resource idle three days ago at gather-time may be back in active use by execute-time on a slow-moving scope.
- **Treating SAFE as permission to edit immediately.** SAFE means the evidence supports a low-risk follow-up authoring pass, not that this skill can write Terraform directly.
- **Running this skill during a `ywc-infra-review` pass instead of separately.** Review is diagnosis-only and has no write access by design; mixing execution into a review pass collapses a boundary the rest of the toolkit relies on.

## Integration

- **Upstream**: `ywc-infra-review` (diagnosis that surfaces the cost/drift/reliability findings this skill classifies); direct user invocation for a scheduled optimization pass.
- **Downstream**: `ywc-verify-done` (mandatory final claim, unless skipped); `ywc-iac-author` (re-authoring path for SAFE, CAUTION, and DANGER follow-ups).
- **Consults**: `ywc-performance-engineer` persona (cost/utilization signal, Step 1); `ywc-cloud-engineer` persona (read-only feasibility and blast-radius consult, Step 3).
- **Must not be paired with**: greenfield topology design (`ywc-infra-design`), first-time authoring (`ywc-iac-author`), or a pre-apply-only review pass (`ywc-infra-review`) — those own separate lifecycle phases.

## References

| Reference | Use when |
|---|---|
| `../references/infra/lenses/cost.md` | Step 1 — cost/utilization signal gathering, right-sizing and waste taxonomy |
| `../references/finops.md` | Step 1 — the detailed FinOps taxonomy (reserved/spot, data-transfer cost) the `ywc-performance-engineer` persona reviews against |
| `../references/infra/lenses/reliability.md` | Step 2/3 — classification taxonomy for reliability-hardening SAFE/CAUTION candidates (backups, health checks, autoscaling floors, deletion protection, multi-AZ) and the guardrail against a cost change dropping below the reliability floor |
| `../references/subagent-status-actions.md` | Steps 1 and 3 — the §3.5 bounded status-return contract each dispatch must follow so fan-out returns stay bounded |
| `ywc-verify-done` | Step 5 — per-batch verification block shape (command + exit code + claim) — mandatory unless `--skip-verify-done` |
