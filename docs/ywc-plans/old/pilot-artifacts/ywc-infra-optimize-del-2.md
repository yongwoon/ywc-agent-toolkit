# Dispatch artifact: ywc-infra-optimize (deleted body, run 2)

**Key**: claude-code/skills/ywc-infra-optimize/SKILL.md:45-45
**Scenario**: I need help with the following: improving existing infrastructure: cost right-sizing, removing unused resources, reserved/spot adoption, drift detection & remediation, and reliability hardening for AWS/GCP/Azure/K8s — the safe change-loop equivalent of refactor-clean for infra.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a full refusal of the task - the ywc-infra-optimize skill itself is the correct, exact match for the request and I would proceed with it. But two things get escalated rather than auto-done: (1) before Step 1 gather work, I would ask the user to confirm which repository/Terraform root and environment (prod vs staging) to target, since --scope was not given and the current workspace's listed projects (genbatime, homepage, our-assets-lp, beacon, etc.) do not show an obviously live Terraform-managed infra tree to run against; and (2) per the skill's own Iron Law, any CAUTION-tier item (e.g. reserved/spot capacity commitments, ambiguous-utilization right-sizing) and any DANGER-tier item (any destroy/recreate on a stateful resource, compliance/DR-tagged resources, anything touched in git log in the last 7 days) would be escalated in the Output Format report and never auto-executed, regardless of how clean a terraform plan looked.

## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-infra-optimize-45-45.md (ywc-infra-optimize skill definition)
- Announce skill invocation per the skill's required announce-at-start line
- Ask a clarifying question: which repository/Terraform root and environment (prod/staging) to target, since no --scope was given and no project in this workspace visibly carries live Terraform-managed infra
- Step 1: locate IaC tree (git ls-files '*.tf'), run terraform init + terraform plan -detailed-exitcode per root module to capture drift
- Step 1: dispatch Task(subagent_type: ywc-performance-engineer) read-only, pointing at references/lenses/cost.md and references/finops.md, for the cost/utilization report
- Step 2: classify every candidate into SAFE / CAUTION / DANGER per the skill's tier table, checking git log --since='7 days ago' for DANGER recency and terraform plan blast radius for cross-module references
- Step 3: for each SAFE item - re-confirm signal, capture terraform plan -target=<resource> baseline, dispatch Task(subagent_type: ywc-cloud-engineer) scoped to that single resource to make the minimal .tf edit and run terraform plan (never apply), diff post-change plan against baseline, commit one item per commit with the lens-tagged message shape
- Step 4: for each CAUTION/DANGER item, write a report entry with rationale and next step (ywc-iac-author or a direct spend-commitment question to the user) without executing
- Step 5: hand off to ywc-verify-done with the Infra Optimize Report; then create the optimization branch's PR via gh pr create / ywc-create-pr
- Explicitly refuse to run terraform apply and refuse to auto-execute any CAUTION or DANGER item at any point

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-infra-optimize-45-45.md (read only)
- infra/**/*.tf (hypothetical target repo - would be read and, for SAFE items only, minimally edited)
- references/lenses/cost.md, references/lenses/reliability.md, references/finops.md, references/subagent-status-actions.md (referenced, not modified)
- a scratch report file capturing the SAFE/CAUTION/DANGER classification and drift/cost findings (artifact path returned by the Step 1 and Step 3 subagent dispatches)

## Gates enforced
- Iron Law: cost/utilization data + per-item terraform plan blast-radius + reversibility/snapshot guarantee required before any execution
- SAFE/CAUTION/DANGER tier classification with multi-tier matches escalating to the highest tier
- Pre-change plan baseline vs post-change plan diff must match only the intended delta (third witness) before commit
- One SAFE item per commit - no batching, for bisectability
- terraform apply never run at any point - plan only
- CAUTION and DANGER items are escalated/reported only, never executed, regardless of classifier or plan confidence
- Reliability-hardening SAFE items checked against references/lenses/reliability.md before executing
- Review pass (ywc-infra-review) and execution pass never mixed in the same run
- Mandatory ywc-verify-done handoff unless --skip-verify-done passed by an upstream orchestrator

## Full narrative

Here is exactly how I would carry out this request under the ywc-infra-optimize procedure.

First, I would announce the skill per its required opening line: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."

Before touching anything, I would ask one clarifying question: which repository/Terraform root and environment (prod vs staging) should this pass target? No `--scope` was given, and the request doesn't name a specific codebase. This matters because the skill's default (`full IaC tree / live infrastructure`) is only safe to assume if I can actually locate a Terraform tree — running `git ls-files '*.tf'` blind against the wrong project risks silently doing nothing or, worse, targeting infra the user didn't intend. Once the target repo is confirmed, I would proceed without further questions using the skill's defaults.

**Step 1 — scope + gather.** I would run `git ls-files '*.tf' '*.tfvars'` to enumerate the IaC tree (or the `--scope` path if given), then `terraform -chdir=<root> init -backend=true` followed by `terraform -chdir=<root> plan -detailed-exitcode -out=tfplan-baseline.out` per root module — this is the drift-detection signal. I would save the plan output (`terraform show -json tfplan-baseline.out > drift-report.json`) as the artifact for later diffing. In parallel, I would dispatch `Task(subagent_type: ywc-performance-engineer)` in read-only diagnostic mode, carrying the scoped Terraform paths plus explicit pointers to `references/lenses/cost.md` and `references/finops.md`, instructing it to produce a cost/utilization report covering idle/orphaned resources, over-provisioned compute against observed p95, and on-demand load that should be reserved/spot. I would inject the §3.5 return-payload directive from `references/subagent-status-actions.md` into that dispatch so it returns `Status | 1-line summary | artifact path | Concerns (≤10 lines)` with full findings in a file.

**Step 2 — classify.** I would walk every candidate from the drift report and the cost/utilization report and sort each into exactly one tier, escalating multi-tier matches to the highest tier:
- SAFE: e.g. `aws_eip.unused-1` confirmed zero-utilization with `terraform plan` showing no other module references it; `aws_instance.worker` at <10% p95 CPU with a clear `m5.4xlarge → m5.large` target; drift matching an already-approved-but-unapplied `.tf` diff; additive reliability items like enabling PITR on a store that lacks it, adding a missing health check, raising an autoscaling `min` to 2, or turning on deletion protection (checked against `references/lenses/reliability.md`).
- CAUTION: reserved/spot capacity commitments, moderate or ambiguous utilization, drift that looks like an intentional manual hotfix, right-sizing a resource with recent scaling history, or adding a multi-AZ standby/read replica.
- DANGER: any destroy or recreate against a stateful resource (database, volume, bucket) no matter how clean the plan looks, anything tagged compliance/DR, or anything `git log --since="7 days ago" --name-only -- <path>` shows touched in the last week.

**Step 3 — SAFE execution loop.** For each SAFE item, in order: re-confirm the signal is still current (re-check that specific resource's metrics, not the Step 1 snapshot); capture a per-item baseline with `terraform -chdir=<root> plan -target=<resource>`; dispatch `Task(subagent_type: ywc-cloud-engineer)` scoped to that single resource with the classification rationale and instructions to make the minimal `.tf` edit (e.g. delete the `aws_eip.unused-1` block in `infra/modules/network/main.tf`, or change `instance_type` in `infra/modules/compute/main.tf`, or add a `backup_retention_period` argument) and run `terraform plan` — never `apply`. I would then diff the post-change plan against the baseline; if it touches anything beyond the intended resource, I would re-classify the item to CAUTION and skip it rather than force it through. On a clean match, I would commit immediately with the lens-tagged shape, e.g. `chore(infra): remove idle aws_eip.unused-1 (cost lens)` or `fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large (cost lens)` or `fix(infra): enable point-in-time-recovery on aws_dynamodb_table.orders (reliability lens)` — one commit per item, never batched, so the eventual `git revert` is a clean bisectable undo. I would do this work on a dedicated branch (e.g. `feature/infra-optimize-<date>`) so the pass ships as its own PR later.

**Step 4 — escalate CAUTION/DANGER.** For every CAUTION or DANGER item I would write a report entry with the rationale and a concrete next step — pointing to `ywc-iac-author` for a reviewed re-authoring, or asking the user directly for an explicit spend commitment before any reserved/spot purchase. I would not execute either tier under any circumstance, including a DANGER item whose `terraform plan` came back clean — a clean plan proves syntactic validity, not safety, for a stateful destroy.

**Step 5 — verify-done handoff.** I would compile the Infra Optimize Report (scope, drift count, executed SAFE commits, escalated CAUTION/DANGER entries, per-item `terraform plan` verification results, and an order-of-magnitude monthly cost delta) and hand off to `ywc-verify-done`, since `--skip-verify-done` was not passed. After that PASSes, the natural next step is `ywc-create-pr` (or `gh pr create` directly) to ship the optimization branch as its own PR, per the skill's stated downstream integration.

Throughout, I would treat three things as hard stops rather than judgment calls: I would never run `terraform apply`; I would never batch two SAFE items into one commit even if it seemed faster to review; and I would never auto-execute a CAUTION or DANGER item just because the cost tool or a clean plan made it look low-risk — those tiers exist precisely because "looks safe" is not a call this skill is authorized to make alone, and any reserved/spot adoption specifically requires the user's explicit go-ahead since it commits real spend.
