# Dispatch artifact: ywc-infra-optimize (deleted body, run 3)

**Key**: claude-code/skills/ywc-infra-optimize/SKILL.md:45-45
**Scenario**: I need help with the following: improving existing infrastructure: cost right-sizing, removing unused resources, reserved/spot adoption, drift detection & remediation, and reliability hardening for AWS/GCP/Azure/K8s — the safe change-loop equivalent of refactor-clean for infra.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a full refusal -- the skill's own workflow was fully narrated end-to-end -- but before Step 1's gather could actually run, execution would stop for a clarifying question: the current workspace (per CLAUDE.md's project table: genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils) contains no visible Terraform/IaC tree or live-cloud credentials for this skill to target, and the user's request named all four platforms (AWS/GCP/Azure/K8s) generically without specifying which repo, which cloud account(s)/project(s)/subscription(s), which environment (prod vs staging), or confirming terraform-init'd backend access -- all of which Step 1 (terraform plan against the scoped module tree, plus a cost/utilization dispatch needing cloud credentials) requires before any classification or SAFE execution can begin. Additionally, per the skill's own DANGER tier and Rationalization Defense table, any CAUTION/DANGER item encountered later (reserved/spot commitments, any stateful destroy, anything touched in the last 7 days) would be escalated back to the user rather than executed, regardless of how clean a terraform plan looked.

## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-infra-optimize-45-45.md (only tool used)
- Would announce: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."
- Would check current workspace for a Terraform root (Glob **/*.tf, ls infra/ terraform/) before Step 1
- Would ask a clarifying question about repo/path, cloud(s) in scope, environment, and credential access before running terraform plan
- Would run terraform plan -detailed-exitcode against the scoped module tree (Step 1 drift signal)
- Would dispatch Task(subagent_type: ywc-performance-engineer) read-only, carrying references/lenses/cost.md and references/finops.md pointers, to produce cost/utilization report
- Would inject the ยง3.5 return-payload directive from references/subagent-status-actions.md into both fan-out dispatches
- Would classify every candidate into SAFE/CAUTION/DANGER per the Step 2 table, escalating multi-tier matches to the highest tier
- Would run the Step 3 SAFE loop per item: re-confirm signal, capture pre-change terraform plan baseline, dispatch Task(subagent_type: ywc-cloud-engineer) scoped to one resource, edit the single .tf file, run terraform plan (never apply), diff post-change plan against baseline, commit one item per commit with lens-tagged conventional commit message
- Would escalate every CAUTION/DANGER item in Step 4 with rationale and a suggested next step (ywc-iac-author or a direct question to the user), never executing them
- Would hand off to ywc-verify-done with the Infra Optimize Report (Step 5), unless --skip-verify-done was passed by an upstream caller
- Would assemble the final Infra Optimize Report using the skill's exact Output Format template
- Would open a PR via gh pr create (or ywc-create-pr) for the SAFE-item branch as a downstream step, without ever running terraform apply

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-infra-optimize-45-45.md (read only)
- hypothetical: infra/modules/network/eip.tf (SAFE delete of idle aws_eip.unused-1)
- hypothetical: infra/modules/compute/worker.tf (SAFE right-size aws_instance.worker instance_type m5.4xlarge -> m5.large)
- hypothetical: infra/modules/db/rds.tf (SAFE add backup_retention_period / PITR, reliability lens)
- hypothetical: references/lenses/cost.md, references/finops.md, references/lenses/reliability.md, references/subagent-status-actions.md (referenced by the skill, not this repo)

## Gates enforced
- Iron Law: cost/utilization data + per-item terraform plan blast-radius + reversibility/snapshot, all three required before any execution
- SAFE/CAUTION/DANGER tier classification with multi-tier-matches-escalate-to-highest rule
- Pre-change terraform plan baseline vs post-change plan diff must match only the intended delta (third witness) before commit
- One SAFE item per commit -- no batching, for bisectability
- terraform apply never run at any point -- plan only
- CAUTION and DANGER items are always escalated, never auto-executed, regardless of classification-tool confidence or how clean a plan looks
- Revert-first discipline if a downstream signal regresses after a SAFE commit, rather than a forward-fix commit
- ywc-verify-done handoff mandatory unless --skip-verify-done is explicitly passed by an upstream caller
- Review/execute boundary respected -- this is the execute pass, distinct from ywc-infra-review's diagnosis-only pass

## Full narrative

I would follow the ywc-infra-optimize procedure exactly as written, and I would announce it first: "I'm using the ywc-infra-optimize skill to improve existing infrastructure under a SAFE/CAUTION/DANGER change loop with per-item terraform plan verification."

Before touching Step 1, I would check whether this workspace actually has something for the skill to operate on. I would run a Glob for `**/*.tf` and `ls` against likely roots (`infra/`, `terraform/`) across the workspace's known projects (genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils, per this repo's CLAUDE.md project table). None of those are described as infra-as-code projects, and none of them list Terraform. That matters because Step 1 requires running `terraform plan` (or `terraform plan -detailed-exitcode`) directly against a scoped module tree, and Step 1's cost signal requires dispatching `Task(subagent_type: ywc-performance-engineer)` with real cloud credentials (CloudWatch/Cost Explorer for AWS, Cloud Monitoring/Billing for GCP, Azure Monitor/Cost Management for Azure, metrics-server/Prometheus for K8s). Since the user's request named AWS/GCP/Azure/K8s generically rather than pointing at a specific repo or account, I would stop here and ask a clarifying question rather than guess: which repository (or path) holds the Terraform configuration to optimize, which of the four platforms are actually in play for their footprint, which environment (production vs. staging) is in scope, and whether I already have a `terraform init`'d backend plus working cloud credentials to run `plan` against. Proceeding without this would mean either fabricating a scope or running `terraform plan` against nothing, both of which the skill's own Iron Law forbids (the plan witness is one of three mandatory pieces of evidence, not optional).

Once that scope were confirmed, I would execute the workflow precisely:

**Step 1 — scope + gather.** Run `terraform plan -detailed-exitcode` against the confirmed module tree (exit 2 = drift, 0 = clean, 1 = error) to get the drift signal. In parallel, dispatch `Task(subagent_type: ywc-performance-engineer)` in read-only diagnostic mode, carrying the scoped `.tf` files and explicit pointers to `../references/lenses/cost.md` and `../references/finops.md`, instructing it to report idle/orphaned resources, over-provisioned compute against observed p95 utilization (not a single snapshot — cost.md's representative-window guidance), and on-demand-vs-reserved/spot mismatches. I would inject the §3.5 return-payload directive from `../references/subagent-status-actions.md` so the dispatch returns `Status | 1-line summary | artifact path | Concerns (≤10 lines)` with full findings written to a file rather than dumped inline.

**Step 2 — classify.** Sort every candidate into exactly one of SAFE/CAUTION/DANGER, escalating any multi-tier match to the highest tier. Concretely: an unattached `aws_eip` with zero attachment and no cross-module reference in the plan → SAFE (delete); an `aws_instance.worker` sitting at <10% p95 CPU with an unambiguous right-size target and no recent scaling history → SAFE (right-size); an RDS instance missing automated backups/PITR → SAFE (additive, reversible reliability fix, checked against `../references/lenses/reliability.md`); a steady-state fleet being considered for Reserved Instances or Spot → CAUTION (commits spend/availability, escalate with a direct question to the user); a resource with 35–55% ambiguous utilization or recent autoscaling history → CAUTION; any `aws_db_instance`/Cloud SQL/Azure SQL/EBS/PersistentVolume/bucket whose plan shows a destroy or recreate, or anything `git log` shows touched in the last 7 days, or anything tagged compliance/DR → DANGER, regardless of how clean the plan looks.

**Step 3 — SAFE execution loop, per item, never batched.** For `aws_eip.unused-1`: re-confirm via a fresh utilization/attachment check that it's still idle right before executing (Step 1's signal can go stale); capture a pre-change baseline with `terraform plan -target=aws_eip.unused-1`; dispatch `Task(subagent_type: ywc-cloud-engineer)` scoped to only this resource, carrying the classification rationale, instructing it to delete the `aws_eip.unused-1` block in its owning `.tf` file and run `terraform plan` — never `apply`; diff the post-change plan against the baseline to confirm only that resource is destroyed and nothing else drifts (the loop's third witness); commit as its own change: `chore(infra): remove idle aws_eip.unused-1 (cost lens)`. Repeat identically for `aws_instance.worker`'s `instance_type` edit (`fix(infra): right-size aws_instance.worker (cost lens, m5.4xlarge -> m5.large)`) and for the RDS backup/PITR addition (`fix(infra): enable automated backups on aws_db_instance.x (reliability lens)`). Each is its own commit for bisectability — I would not combine any two SAFE items into a single commit even if reviewed together.

**Step 4 — CAUTION/DANGER, escalate only.** For the Reserved/Spot candidate, I would write a report entry recommending either `ywc-iac-author` for a reviewed re-authoring or a direct question back to the user about commitment term and risk tolerance — and take no action. For any stateful destroy (e.g., `aws_db_instance.legacy`), I would flag it as requiring explicit human sign-off and would not touch it even if its `terraform plan` came back clean, per the skill's own Rationalization Defense table ("plan succeeding proves syntactic validity, not safety").

**Step 5 — verify-done handoff.** Unless `--skip-verify-done` were passed by an upstream caller, I would hand the assembled Infra Optimize Report to `ywc-verify-done`, which re-checks the per-item `terraform plan` exit codes and the PASS/FAIL wording independently rather than trusting my own claim.

Throughout, I would never run `terraform apply`, never batch SAFE commits, never auto-execute a CAUTION or DANGER item no matter how confident the classification looked, and if any downstream signal regressed after a SAFE commit landed (alert, cost anomaly, availability drop), I would revert that exact commit first rather than chase it with a follow-up fix. After the SAFE-item branch was complete, the natural downstream step would be opening a PR (`gh pr create`, or the `ywc-create-pr` skill) carrying only those bisectable SAFE commits for human/CD-gated merge — the skill itself stops at `plan`, never applies.
