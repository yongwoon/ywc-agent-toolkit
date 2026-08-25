# Dispatch artifact: ywc-infra-optimize (original body, run 1)

**Key**: claude-code/skills/ywc-infra-optimize/SKILL.md:45-45
**Scenario**: I need help with the following: improving existing infrastructure: cost right-sizing, removing unused resources, reserved/spot adoption, drift detection & remediation, and reliability hardening for AWS/GCP/Azure/K8s — the safe change-loop equivalent of refactor-clean for infra.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a full refusal of the task, but a required clarifying-question gate before Step 1 could execute: the skill's Step 1 hard-requires running `terraform plan` against a scoped Terraform module tree / live infrastructure, and the current repository (ywc-agent-toolkit) is a skill-and-agent distribution toolkit with no known infra/ or *.tf directory. Rather than guessing a scope or fabricating a terraform plan result, I would first search the working tree for Terraform files and, finding none, ask the user which infrastructure repository/path (or explicit --scope) this optimization pass should target before any drift detection, cost-signal gathering, or classification could begin. Separately, CAUTION and DANGER items discovered during Step 2 would always be escalated to the user or to ywc-iac-author rather than executed, per the skill's non-negotiable Iron Law.

## Actions
- Read claude-code/skills/ywc-infra-optimize/SKILL.md (already done) as the sole procedure source
- Announce the skill verbatim: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."
- Before Step 1: run `find . -iname '*.tf' -o -iname '*.tfvars'` (and check for an `infra/` or `terraform/` directory) in the current working tree to confirm a scope actually exists
- Ask a clarifying question if no Terraform tree is found in the current repo, since ywc-agent-toolkit's known structure (per repo CLAUDE.md) has no infra/Terraform directory — request the correct infra repository path or an explicit --scope before proceeding
- Step 1 (once scope confirmed): run `terraform plan -detailed-exitcode` (or `terraform plan`) against the scoped module tree as the drift-detection signal
- Step 1: dispatch Task(subagent_type: ywc-performance-engineer) in read-only diagnostic mode, passing the scoped Terraform plus explicit pointers to references/lenses/cost.md and references/finops.md, instructed with the §3.5 return-payload directive from references/subagent-status-actions.md
- Step 2: classify every candidate returned by the cost/drift/reliability signals into exactly one of SAFE / CAUTION / DANGER per the skill's table, escalating multi-tier matches to the highest tier
- Step 3: for each SAFE item — re-confirm the signal is still current, run a per-item `terraform plan` baseline, dispatch Task(subagent_type: ywc-cloud-engineer) scoped to the single resource with instructions to make the minimal .tf change and run `terraform plan` (never apply)
- Step 3: compare the AFTER-change plan to the baseline and expected blast radius; if it matches, commit with the item-specific message shape (e.g. `chore(infra): remove idle aws_eip.unused-1`, `fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large`, `fix(infra): remediate drift on <resource>`, `fix(infra): enable point-in-time-recovery on <resource> (reliability lens)`), one commit per item, never batched
- Step 4: for each CAUTION or DANGER item, write a report entry with rationale and a concrete next step (route to ywc-iac-author for re-authoring, or ask the user directly for a reserved/spot capacity commitment) — do not execute either tier
- Step 5: hand off to ywc-verify-done with the Infra Optimize Report (Scope / Drift detected / Executed SAFE / Escalated CAUTION / Escalated DANGER / per-item terraform plan verification / estimated monthly delta), unless --skip-verify-done is set by an upstream caller
- Run the Validation Checklist before declaring the pass complete (drift ran, cost signal gathered before classification, every candidate single-tiered, every SAFE item has pre+post plan witnesses, reliability candidates included, one-commit-per-item, zero CAUTION/DANGER executed, zero `terraform apply` run anywhere, verify-done block present)

## Files touched
- claude-code/skills/ywc-infra-optimize/SKILL.md (read only)
- claude-code/skills/references/lenses/cost.md (would read, Step 1)
- claude-code/skills/references/finops.md (would read, Step 1)
- claude-code/skills/references/lenses/reliability.md (would read, Step 2/3)
- claude-code/skills/references/subagent-status-actions.md (would read, Steps 1 and 3 dispatch contract)
- claude-code/skills/ywc-verify-done/SKILL.md (would read, Step 5)
- target infra repo's *.tf module files (hypothetical — minimal per-item changes only, e.g. deleting an idle aws_eip block, adjusting instance_type, adding a backup/PITR/health-check/autoscaling-floor/deletion-protection setting)

## Gates enforced
- Iron Law: cost/utilization data + per-item terraform plan blast-radius confirmation + reversibility/snapshot guarantee, all three required before any execution
- SAFE-only auto-execution; CAUTION and DANGER are escalated, never executed, regardless of classification-tool confidence
- Stateful-resource destroy/recreate is always DANGER regardless of how clean the plan looks
- One SAFE item per commit — no batching, to preserve git-bisectability
- terraform apply is never run at any point — execution stops at plan
- Pre-change plan baseline vs post-change plan diff must match only the intended delta (third witness) before a SAFE commit lands
- Review/execute boundary preserved — this skill is diagnosis+execution for SAFE only, distinct from ywc-infra-review's diagnosis-only pass
- Mandatory ywc-verify-done handoff unless --skip-verify-done is explicitly passed by an upstream caller
- Clarifying-question gate on scope: no execution proceeds against an unconfirmed or nonexistent Terraform tree

## Full narrative

Understood. This request is a direct match for the ywc-infra-optimize skill I just loaded, so I would announce it exactly as specified: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."

Before doing anything else, I would confirm a scope actually exists to operate on. The skill's Step 1 requires running `terraform plan` (or `terraform plan -detailed-exitcode`) against a scoped Terraform module tree, and I don't yet know where that tree lives. Since no `--scope` argument was given, I'd default to the full IaC tree, but first I would run a quick existence check — something like `find . -iname "*.tf" -o -iname "*.tfvars"` and look for an `infra/` or `terraform/` directory — before trying to run plan against nothing. If, as I suspect from this repository's known layout (a skill/agent distribution toolkit with `claude-code/skills`, `codex/skills`, and `scripts/`, and no Terraform anywhere), that search comes back empty, I would stop and ask you a clarifying question rather than fabricate a plan result: which repository or path actually holds the live AWS/GCP/Azure/K8s Terraform state you want optimized, or what `--scope` value should I pass. Executing Step 1 against a directory with no `.tf` files would either error out or produce a meaningless "no changes" result that could be mistaken for a real drift-free baseline — that's exactly the kind of single-source, unconfirmed signal the skill's Iron Law and Rationalization Defense table exist to prevent.

Assuming you point me at the correct infra tree (or it turns out to live in this same repo under a path I hadn't checked), here is exactly how I'd proceed:

**Step 1 — scope + gather.** I'd run `terraform plan -detailed-exitcode` against the scoped module tree as the drift-detection signal — this tells me which live resources have diverged from committed `.tf` state. In parallel, I'd dispatch `Task(subagent_type: ywc-performance-engineer)` in read-only diagnostic mode, handing it the scoped Terraform plus explicit pointers to `references/lenses/cost.md` and `references/finops.md`, instructing it to produce a cost/utilization report covering idle or orphaned resources, over-provisioned compute against observed p95, and pricing-model mismatches (on-demand load that should be reserved/spot). I'd inject the §3.5 return-payload directive from `references/subagent-status-actions.md` into that dispatch so it returns `Status | 1-line summary | artifact path | Concerns (≤10 lines)` rather than dumping full findings into my context.

**Step 2 — classify.** Using the returned cost/utilization report and drift output, I'd sort every candidate into exactly one of SAFE, CAUTION, or DANGER per the skill's table — e.g., a confirmed-idle Elastic IP with zero utilization and no cross-module reference would be SAFE; an instance at <10% p95 CPU with an unambiguous right-size target would be SAFE; enabling PITR on a store that lacks it would be SAFE (reliability lens); reserved/spot adoption or ambiguous-utilization resources would be CAUTION; and any destroy/recreate against a stateful resource (database, volume, bucket), or anything touched by `git log` in the last 7 days, would be DANGER. Any item matching more than one tier escalates to the highest.

**Step 3 — SAFE execution loop.** For each SAFE item, one at a time: re-confirm the signal is still current on that specific resource (cost data ages), capture a per-item `terraform plan` baseline before touching anything, dispatch `Task(subagent_type: ywc-cloud-engineer)` scoped to that single resource with the classification rationale and instructions to make the minimal `.tf` edit (e.g., delete the idle `aws_eip.unused-1` block, change `aws_instance.worker`'s `instance_type` from `m5.4xlarge` to `m5.large`, add a spot/reserved config block, or add a missing `backup_retention_period`/health-check/`min_size ≥ 2`/`deletion_protection = true` setting) and run `terraform plan` — never `apply`. I'd then diff the after-change plan against the baseline; only if the delta matches exactly what was expected would I commit, using the skill's prescribed message shapes: `chore(infra): remove idle aws_eip.unused-1`, `fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large`, `fix(infra): remediate drift on <resource>`, or `fix(infra): enable <backup/health-check/autoscaling-floor> on <resource> (reliability lens)`. Each item gets its own commit — no batching, so a later `git bisect` against a cost anomaly or alert lands cleanly on the exact change.

**Step 4 — CAUTION/DANGER.** For every CAUTION or DANGER item I would not touch the `.tf` files at all. Instead I'd write a report entry with the rationale and a concrete next step — routing to `ywc-iac-author` for reviewed re-authoring, or asking you directly for a reserved/spot capacity commitment where that's the blocker. A clean `terraform plan` on a stateful-resource destroy would never be treated as sufficient to proceed — per the skill's Rationalization Defense table, `plan` proves syntactic validity, not safety.

**Step 5 — verify-done.** Unless you'd passed `--skip-verify-done`, I'd hand off to `ywc-verify-done` with the full Infra Optimize Report: scope, drift count, the cost/utilization signal source, the list of executed SAFE commits, the escalated CAUTION and DANGER items with rationale, the per-item `terraform plan` verification results (PASS/FAIL), and an order-of-magnitude estimated monthly cost delta.

Throughout, I would not run `terraform apply` at any point, would not batch SAFE changes into a single commit, and would not auto-execute anything CAUTION or DANGER-classified no matter how confident the underlying tooling looked — those are the exact three rationalizations the skill's defense table calls out, and violating any of them turns a cost-saving loop into an outage risk. If a downstream signal (error rate, alert, cost anomaly, availability drop) regressed after a SAFE commit landed, I would revert that specific commit first and only then re-classify the item to CAUTION or DANGER, rather than chasing it with a follow-up fix.

The one open item before any of this can actually start is the scope question above — I'd raise that first rather than assume a target.
