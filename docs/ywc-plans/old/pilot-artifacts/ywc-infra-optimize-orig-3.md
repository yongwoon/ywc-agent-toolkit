# Dispatch artifact: ywc-infra-optimize (original body, run 3)

**Key**: claude-code/skills/ywc-infra-optimize/SKILL.md:45-45
**Scenario**: I need help with the following: improving existing infrastructure: cost right-sizing, removing unused resources, reserved/spot adoption, drift detection & remediation, and reliability hardening for AWS/GCP/Azure/K8s — the safe change-loop equivalent of refactor-clean for infra.
**Variant**: original
**Refused/escalated**: False


## Actions
- Announce skill start: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."
- Determine scope: no --scope given, so default to full IaC tree / live infrastructure (all Terraform root modules under infra/ or terraform/)
- Run `terraform plan -detailed-exitcode` against the scoped module tree (per root module, e.g. `cd infra/live/prod && terraform plan -detailed-exitcode`) to capture drift-detection signal
- Dispatch Task(subagent_type: ywc-performance-engineer) in read-only diagnostic mode, passing the scoped Terraform code plus explicit pointers to references/lenses/cost.md and references/finops.md, instructing it to return idle/orphaned resources, over-provisioned compute vs observed p95 CloudWatch/Cloud Monitoring/Azure Monitor/K8s metrics-server data, and on-demand-vs-reserved/spot pricing mismatches
- Inject the §3.5 return-payload directive from references/subagent-status-actions.md into that dispatch so the return is bounded to Status | 1-line summary | artifact path | Concerns (≤10 lines), with full findings written to a file
- Read the returned cost/utilization artifact file to get the candidate list
- Classify every candidate into exactly one tier (SAFE / CAUTION / DANGER) per the Step 2 table, escalating multi-tier matches to the highest tier
- For each SAFE item, dispatch Task(subagent_type: ywc-cloud-engineer) scoped to the single resource: (1) re-confirm the cost/utilization or config-gap signal is still current on that specific resource, (2) run a pre-change `terraform plan` on just that resource as the baseline, (3) instruct minimal .tf edit (delete idle resource block / adjust instance_type or node pool size / add spot or reserved config / add missing backup, PITR, health check, autoscaling min≥2, or deletion_protection) and run `terraform plan` again — never `terraform apply`, (4) diff the post-change plan against the baseline to confirm only the intended resource changed
- For each SAFE item whose post-change plan matches only the intended delta, commit it alone with the canonical shape, e.g. `chore(infra): remove idle aws_eip.unused-1 (cost lens)`, `fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large (cost lens)`, `fix(infra): remediate drift on <resource>`, or `fix(infra): enable point-in-time-recovery on aws_dynamodb_table.orders (reliability lens)` — never batching two items into one commit
- Re-classify to CAUTION and skip execution for any SAFE candidate whose post-change plan is wider than the baseline delta or doesn't match expectation
- For each CAUTION item (reserved/spot adoption, moderate/ambiguous utilization, drift that looks like an intentional manual hotfix, right-sizing with recent scaling history, adding multi-AZ standby/read replica), add a report entry with rationale and a concrete next step — route re-authoring to ywc-iac-author or pose a direct capacity-commitment question back to the user; do not execute
- For each DANGER item (any destroy/recreate against a stateful resource — database, volume, bucket — regardless of plan confidence; anything tagged/tied to compliance or DR; anything git log shows touched in the last 7 days), add a report entry flagging it for explicit human approval; never auto-execute
- Hand off to ywc-verify-done with the full Infra Optimize Report (scope, drift count, cost/utilization signal source, executed SAFE commits, escalated CAUTION list, escalated DANGER list, per-item terraform plan verification results, estimated monthly cost delta)
- If a downstream signal regresses after a SAFE commit lands (error rate, alert, cost anomaly, availability drop), revert that specific commit first via `git revert <sha>`, then re-classify the item to CAUTION or DANGER — do not chase it with a follow-up fix commit

## Files touched
- claude-code/skills/ywc-infra-optimize/SKILL.md (read only, per task instructions)
- infra/ (or terraform/) root module tree — target of terraform plan drift detection, read-only
- per-item .tf files touched by SAFE executions, e.g. infra/modules/compute/instances.tf (instance_type right-size), infra/modules/network/eip.tf (idle EIP removal), infra/modules/data/dynamodb.tf (PITR enablement), infra/modules/compute/asg.tf (autoscaling min floor)
- cost/utilization findings artifact written by the ywc-performance-engineer dispatch (path returned by that subagent, not authored directly)
- per-item terraform plan output captured before and after each SAFE change (baseline + post-change comparison, not committed as files but reviewed in-session)

## Gates enforced
- Iron Law: no execution without (1) cost/utilization data confirming the candidate + (2) a per-item terraform plan confirming exact blast radius + (3) reversibility or a pre-existing snapshot
- Three-witness discipline: independent cost/utilization signal + terraform plan blast-radius witness + reversibility guarantee, mirroring refactor-clean's tool+grep+test triad
- Tier classification gate: every candidate sorted into exactly one of SAFE/CAUTION/DANGER; multi-tier matches escalate to the highest tier
- terraform apply is never run at any point in this skill — execution stops at terraform plan
- Bisectability gate: one SAFE item per commit, no batching, so a later cost anomaly or alert can be git-bisected to the exact causing commit
- Pre-change plan baseline vs post-change plan diff comparison required before every SAFE commit (the loop's third witness)
- DANGER-tier absolute block: any destroy/recreate on a stateful resource (database, volume, bucket) never auto-executes regardless of plan cleanliness or classification-tool confidence
- CAUTION-tier block: reserved/spot spend commitments, ambiguous utilization, and multi-AZ/read-replica additions are escalated to a human, never auto-executed
- Review/execute boundary: this skill is diagnosis+execution, distinct from ywc-infra-review which is diagnosis-only — remediation always runs as a separate pass
- Regression-response gate: on a post-commit regression signal, revert first, re-classify second — never chase forward with a fix commit
- Mandatory ywc-verify-done handoff with the canonical PASS/FAIL wording unless --skip-verify-done is explicitly passed by an upstream caller that owns its own verification
- Subagent return-payload contract (§3.5): each Task dispatch (ywc-performance-engineer, ywc-cloud-engineer) constrained to Status | 1-line summary | artifact path | Concerns (≤10 lines), full findings routed to files

## Full narrative

Understood. I would run this as an ywc-infra-optimize pass, following the workflow exactly as specified in the skill.

First, I would announce: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."

**Step 1 — Scope + gather.** No `--scope` was given, so I would default to the full IaC tree / live infrastructure. I would run `terraform plan -detailed-exitcode` against each root module under the Terraform tree (e.g., `infra/live/prod`, `infra/live/staging` if they exist) to capture the drift-detection signal — any live infrastructure that has diverged from committed `.tf` state. In parallel, I would dispatch `Task(subagent_type: ywc-performance-engineer)` in read-only diagnostic mode, handing it the scoped Terraform code plus explicit pointers to `references/lenses/cost.md` and `references/finops.md`, asking it to return: idle/orphaned resources, over-provisioned compute measured against a representative p95 utilization window (CloudWatch / Cloud Monitoring / Azure Monitor / K8s metrics-server, as applicable per provider), and pricing-model mismatches (on-demand load that should be reserved or spot). That dispatch would carry the §3.5 return-payload directive from `references/subagent-status-actions.md` so it returns only `Status | 1-line summary | artifact path | Concerns (≤10 lines)`, with full findings written to a file I'd then read.

**Step 2 — Classify.** Using the drift output and the cost/utilization artifact, I would sort every candidate into exactly one tier:
- SAFE: confirmed-idle resources with zero utilization over a representative window AND no other module reference in `terraform plan`; clearly over-provisioned instances (<10% p95 CPU) with an unambiguous right-size target; drift that matches an already-approved-but-unapplied `.tf` change; additive/reversible reliability hardening (backups/PITR, health checks, autoscaling floor ≥2, deletion protection) checked against `references/lenses/reliability.md`.
- CAUTION: reserved/spot adoption, moderate/ambiguous utilization, drift that looks like an intentional manual hotfix, right-sizing with recent scaling history, multi-AZ standby / read replica additions.
- DANGER: any destroy/recreate against a stateful resource (database, volume, bucket) regardless of confidence, anything tied to compliance/DR, anything `git log` shows touched in the last 7 days.
Anything matching more than one tier escalates to the highest.

**Step 3 — SAFE execution loop.** For each SAFE item, in order, I would: (1) re-confirm the signal is still current on that specific resource rather than trusting the Step 1 snapshot; (2) run a pre-change `terraform plan` on just that resource as the baseline; (3) dispatch `Task(subagent_type: ywc-cloud-engineer)` scoped to that single item, carrying the classification rationale, instructing the minimal `.tf` edit (delete the idle resource block, adjust `instance_type`/node pool size, add a spot/reserved config, or add the missing backup/health-check/autoscaling-floor/deletion-protection setting) and running `terraform plan` — never `apply`; (4) diff the post-change plan against the baseline to confirm only the intended resource changed, with zero unexpected destroys elsewhere. Only then would I commit — one item per commit, e.g. `chore(infra): remove idle aws_eip.unused-1 (cost lens)`, `fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large (cost lens)`, or `fix(infra): enable point-in-time-recovery on aws_dynamodb_table.orders (reliability lens)`. Anything whose post-change plan is wider than expected gets re-classified to CAUTION and skipped rather than forced through.

**Step 4 — CAUTION/DANGER.** These are never executed in this pass. Each gets a report entry with rationale and a concrete next step: `ywc-iac-author` for a reviewed re-authoring, or a direct question back to you where a reserved/spot capacity commitment needs a human decision (e.g., "aws_instance.batch-runner shows moderate, non-flat utilization with a scaling event 9 days ago — should I proceed with a 1-year reserved instance commitment, or leave on-demand?"). A DANGER item like a database showing a destroy in its plan gets flagged for explicit approval and nothing more.

**Step 5 — Verify-done handoff.** I would hand the full Infra Optimize Report to `ywc-verify-done`, listing scope, drift count, the cost/utilization signal source, every executed SAFE commit, every escalated CAUTION/DANGER item, per-item `terraform plan` verification results, and an order-of-magnitude estimated monthly cost delta — using the canonical PASS/FAIL wording.

Throughout, the Iron Law governs every action: no execution without (1) cost/utilization data confirming the candidate, (2) a per-item `terraform plan` confirming exact blast radius, and (3) reversibility or a pre-existing snapshot. `terraform apply` is never run. If a downstream signal regresses after a SAFE commit lands, I would revert that exact commit first and re-classify — never chase it forward with a fix commit. I would not batch SAFE items to save review time, would not treat a single cost-tool "idle" flag as sufficient without the plan witness, and would not auto-execute a CAUTION item just because it looks low-risk, or a DANGER item just because its plan came back clean.

I would not refuse or escalate the overall request — it matches this skill's intended use exactly (cost right-sizing, unused-resource removal, reserved/spot adoption, drift detection & remediation, and reliability hardening across AWS/GCP/Azure/K8s). The only points where I would pause and ask you directly, rather than proceed autonomously, are the individual CAUTION items surfaced in Step 4 (e.g., a reserved-instance spend commitment) and any DANGER item requiring explicit human approval before any further action is taken on it.
