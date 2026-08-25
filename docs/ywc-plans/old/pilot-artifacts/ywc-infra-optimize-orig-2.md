# Dispatch artifact: ywc-infra-optimize (original body, run 2)

**Key**: claude-code/skills/ywc-infra-optimize/SKILL.md:45-45
**Scenario**: I need help with the following: improving existing infrastructure: cost right-sizing, removing unused resources, reserved/spot adoption, drift detection & remediation, and reliability hardening for AWS/GCP/Azure/K8s — the safe change-loop equivalent of refactor-clean for infra.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The skill's Step 1 requires running `terraform plan` against a scoped Terraform tree and dispatching ywc-performance-engineer with a real cost/utilization data source (CloudWatch / Cloud Monitoring / Azure Monitor / Prometheus) for the target cloud account(s). The current working repository (ywc-agent-toolkit) is a skill/agent distribution toolkit with no Terraform files, no infra/ directory, and no cloud account or cluster context supplied by the user — none of the seven listed subprojects (genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils) is a live-infrastructure repo either. Per the Iron Law, nothing may execute without a confirmed cost/utilization witness plus a per-item terraform plan blast-radius witness, and neither can be produced without a real Terraform tree and cloud target. Rather than guess a --scope or fabricate a target, the correct next step under this procedure is to ask the user which repository/path holds the Terraform configuration to optimize, which AWS/GCP/Azure account(s) or subscription(s) and K8s cluster(s) are in scope, how to authenticate against them, and whether a cost/monitoring data source is already reachable — then proceed through Steps 1-5 exactly as specified once that scope is confirmed.

## Actions
- Announce skill start: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."
- Bash: find . -maxdepth 6 -iname '*.tf' -not -path '*/node_modules/*' (check for a Terraform tree in the current repo before assuming --scope default)
- Bash: find . -maxdepth 3 -type d -iname 'infra*' -o -iname 'terraform*' (check for an infra/ or terraform/ directory convention)
- Re-check already-loaded CLAUDE.md project table (genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils) for any subproject flagged with Terraform/cloud infra
- Ask a clarifying question rather than proceeding: request the target repo/path for --scope, the cloud account/project/subscription/cluster identifiers in scope, and confirmation of accessible cost/monitoring data source (CloudWatch / Cloud Monitoring / Azure Monitor / Prometheus) before Step 1 can gather a cost/utilization signal
- (Deferred pending answer) Step 1: run `terraform plan -detailed-exitcode` against the confirmed --scope path as the drift-detection signal
- (Deferred) Step 1: Task(subagent_type: ywc-performance-engineer) read-only diagnostic dispatch carrying scoped Terraform + pointers to ../references/lenses/cost.md and ../references/finops.md, injecting the §3.5 return-payload directive from ../references/subagent-status-actions.md
- (Deferred) Step 2: classify every candidate into exactly one of SAFE / CAUTION / DANGER per the table in SKILL.md, escalating multi-tier matches to the highest tier
- (Deferred) Step 3 per SAFE item: re-confirm signal currency, run per-item `terraform plan` baseline, Task(subagent_type: ywc-cloud-engineer) scoped to the single resource to make the minimal .tf edit and run `terraform plan` (never apply), diff AFTER-plan against baseline as the third witness, then one commit per item using the prescribed chore(infra):/fix(infra): shape
- (Deferred) Step 4: for every CAUTION/DANGER item, write a report entry with rationale and a next step (route to ywc-iac-author or a direct question to the user) — no execution
- (Deferred) Step 5: hand off to ywc-verify-done with the Infra Optimize Report unless --skip-verify-done is passed by an upstream caller

## Files touched
- claude-code/skills/ywc-infra-optimize/SKILL.md (read only)
- claude-code/skills/ywc-infra-optimize/../references/lenses/cost.md (would read, not touched yet)
- claude-code/skills/ywc-infra-optimize/../references/finops.md (would read, not touched yet)
- claude-code/skills/ywc-infra-optimize/../references/lenses/reliability.md (would read, not touched yet)
- claude-code/skills/ywc-infra-optimize/../references/subagent-status-actions.md (would read, not touched yet)
- <target *.tf files under the confirmed --scope> (not yet identified — none found in this repo)

## Gates enforced
- Iron Law: cost/utilization data + per-item terraform plan + reversibility/snapshot before any execution
- SAFE/CAUTION/DANGER tiering with multi-tier-escalates-to-highest rule
- Per-item bisectable commit, no batching of SAFE items
- terraform plan only, never terraform apply
- DANGER (stateful destroy/recreate) always escalates, never auto-executed regardless of plan cleanliness
- Missing-precondition gate: no Terraform tree / cloud target identifiable in the current repo, so Step 1 (gather current state + cost/utilization signal) cannot start — this blocks proceeding and triggers a clarifying question instead of guessing a scope
- ywc-verify-done mandatory handoff unless --skip-verify-done is passed by an upstream caller

## Full narrative

Before touching anything, I would first verify that the ywc-infra-optimize skill actually has something to operate on in this working directory, because Step 1 of the procedure ("Determine scope + gather current state") is not optional narration — it requires running `terraform plan` (or `terraform plan -detailed-exitcode`) directly against a real, scoped Terraform tree, and it requires dispatching `Task(subagent_type: ywc-performance-engineer)` with a genuine cost/utilization data source behind it (CloudWatch, Cloud Monitoring, Azure Monitor, or Prometheus, per `../references/lenses/cost.md` and `../references/finops.md`).

Concretely, I would run:
- `find . -maxdepth 6 -iname "*.tf" -not -path "*/node_modules/*"` to check whether any Terraform configuration exists anywhere in the repository.
- `find . -maxdepth 3 -type d \( -iname "infra*" -o -iname "terraform*" \)` to check the conventional directory names this toolkit's own docs reference (`infra/modules/compute` appears as the example `--scope` value in the skill itself).
- Cross-check the project table already loaded from the root `CLAUDE.md` (genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils) — none of those seven subprojects is described as owning live cloud infrastructure or a Terraform state; they are Next.js/Supabase, documentation-only, or shell-utility projects.

Given what I already know about this repository — it is `ywc-agent-toolkit`, a skill and agent distribution toolkit whose contents are Markdown skill definitions, install scripts, and validation tooling — I would expect these checks to come back empty: no `.tf` files, no `infra/` tree, no cloud credentials or `kubeconfig` context configured, and no indication of which AWS account, GCP project, Azure subscription, or K8s cluster is meant to be "existing infrastructure" here.

At that point I would stop and ask a clarifying question rather than default `--scope` to "the full IaC tree" the way the skill's Arguments table describes, because there is no tree to default to. I would not fabricate a scope, invent a plausible-looking `infra/` path, or simulate a `terraform plan` output — the Iron Law is explicit that a change (or even a diagnostic pass feeding into one) needs a confirmed cost/utilization witness plus a confirmed blast-radius witness, and neither can exist without a real target. Guessing a scope here would be exactly the kind of single-source, unconfirmed action the skill's Rationalization Defense table warns against, just one step earlier in the pipeline.

The clarifying question I would actually ask: which repository or local path contains the Terraform configuration to optimize (to pass as `--scope`); which AWS account(s)/GCP project(s)/Azure subscription(s) and which K8s cluster context(s) are in scope, and how I should authenticate against them (AWS profile, `gcloud` config, `az login`, `kubeconfig` context); and whether a cost/monitoring backend (CloudWatch, Cloud Monitoring, Azure Monitor, Prometheus) is already reachable for the utilization signal that `ywc-performance-engineer` needs to produce in Step 1. I would also confirm whether they want a `--dry-run` pass first (Steps 1-2 only, report emitted, nothing executed) given this is a first run against unfamiliar infrastructure.

Once that scope is confirmed, here is exactly what I would do, following the skill's five steps without deviation:

**Step 1 — gather state.** Run `terraform plan -detailed-exitcode` against the confirmed scope as the drift-detection signal (exit code 2 means drift; I would capture the full plan output to a file rather than let it flood context). In parallel, dispatch `Task(subagent_type: ywc-performance-engineer)` in read-only diagnostic mode, carrying the scoped Terraform and explicit pointers to `../references/lenses/cost.md` and `../references/finops.md`, instructed to produce a cost/utilization report covering idle/orphaned resources, over-provisioned compute against observed p95, and on-demand load that should be reserved/spot. That dispatch prompt must inject the §3.5 return-payload directive from `../references/subagent-status-actions.md` so it comes back as `Status | 1-line summary | artifact path | Concerns (≤10 lines)` with full findings written to a file, not dumped into my context.

**Step 2 — classify.** Sort every candidate the two Step 1 signals surfaced into exactly one of SAFE, CAUTION, or DANGER using the skill's table verbatim — e.g., a confirmed-idle EIP with zero utilization and no other module reference is SAFE; reserved/spot adoption or ambiguous utilization is CAUTION; any destroy/recreate against a stateful resource (RDS, EBS volume, S3 bucket) or anything touched by `git log` in the last 7 days is DANGER regardless of how clean a plan looks. Any item matching more than one tier escalates to the highest.

**Step 3 — SAFE execution loop, per item, one at a time.** For each SAFE item: re-confirm the Step 1 signal is still current on that specific resource (utilization data ages); run a per-item `terraform plan` baseline before touching anything; dispatch `Task(subagent_type: ywc-cloud-engineer)` scoped to that single resource with the classification rationale, instructed to make the minimal `.tf` change (delete the idle resource block, adjust `instance_type`/node pool size, add a spot/reserved block, or add the missing backup/health-check/autoscaling-floor/deletion-protection setting) and run `terraform plan` — never `apply`; diff the AFTER-change plan against the baseline to confirm only the intended resource changed (the third witness); then commit that single item alone, using the prescribed shape, e.g. `chore(infra): remove idle aws_eip.unused-1` or `fix(infra): right-size aws_instance.worker m5.4xlarge -> m5.large`. No batching — each SAFE item is its own commit so a later `git bisect` on a cost anomaly or alert lands on the exact change.

**Step 4 — CAUTION/DANGER escalation.** For every CAUTION or DANGER item, write a report entry with rationale and a concrete next step — routing to `ywc-iac-author` for re-authoring, or a direct question back to the user for anything requiring a spend/availability decision (e.g., reserved/spot commitment). Nothing in these tiers gets executed, and DANGER items never auto-execute even if their `terraform plan` comes back clean, since `plan` proves syntactic validity, not safety, for a stateful destroy.

**Step 5 — verify-done handoff.** Hand off to `ywc-verify-done` with the full Infra Optimize Report (scope, drift count, executed SAFE commits, escalated CAUTION/DANGER items, per-item `terraform plan` PASS/FAIL, estimated monthly delta) unless the caller passed `--skip-verify-done`.

Throughout, if a SAFE commit lands and a downstream signal regresses afterward (error rate, alert, cost anomaly, availability drop), the correct response under this procedure is to revert that exact commit first and re-classify the item to CAUTION or DANGER — not to chase it with a follow-up fix commit. And at no point in any of this would I run `terraform apply`; every execution in this skill stops at `plan`.

Given the actual state of this repository right now, though, none of Steps 1-5 can begin — the missing precondition (no discoverable Terraform tree, no cloud target) is the blocker I would surface to the user before doing anything else.
