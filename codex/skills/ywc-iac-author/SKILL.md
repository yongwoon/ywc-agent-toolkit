---
name: ywc-iac-author
description: >-
  (ywc) Use when authoring or modifying Infrastructure-as-Code from a design —
  Terraform modules and resources for AWS/GCP/Azure/Kubernetes (K8s/Helm
  expressed via the Terraform kubernetes/helm providers, never raw manifests
  or a second IaC tool), including terraform validate/plan verification and a
  blast-radius summary. Triggers: "IaC 작성", "terraform 작성", "인프라 코드",
  "k8s 매니페스트", "write terraform", "author IaC", "provision infrastructure",
  "IaC を書いて", "ywc-iac-author". Do not use for application server /
  business logic (use ywc-backend-coder), designing the topology first (use
  ywc-infra-design), reviewing IaC quality (use ywc-infra-review), cost /
  right-sizing remediation (use ywc-infra-optimize), or local worktree docker
  port collisions (use ywc-docker-isolate — dev-only, not prod infra).
---

# ywc-iac-author

**Announce at start:** "I'm using the ywc-iac-author skill to author Terraform from a design, verify it with validate/plan, and summarize the blast radius."

This skill is the Infrastructure-as-Code counterpart to `ywc-code-gen`: it turns an infrastructure design into working Terraform, dispatches per-module authoring to a Codex worker carrying the `ywc-cloud-engineer` persona (single-responsibility infra worker — the infra counterpart to `ywc-backend-coder`), verifies with `terraform validate` / `terraform plan`, and reports a blast-radius summary before anything is applied. **Terraform is the single fixed IaC tool for this toolkit** — Kubernetes and Helm resources are expressed through the Terraform `kubernetes` / `helm` providers, never raw manifests, a standalone Helm chart, or a second IaC tool (Pulumi / CDK / CloudFormation / Bicep).
This skill is the Infrastructure-as-Code counterpart to `ywc-code-gen`: it turns an infrastructure design into working Terraform inside the current Codex session, uses the read-only `ywc-cloud-engineer` persona for feasibility and blast-radius advisory where helpful, verifies with `terraform validate` / `terraform plan`, and reports a blast-radius summary before anything is applied. **Terraform is the single fixed IaC tool for this toolkit** — Kubernetes and Helm resources are expressed through the Terraform `kubernetes` / `helm` providers, never raw manifests, a standalone Helm chart, or a second IaC tool (Pulumi / CDK / CloudFormation / Bicep).

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "No `infra-design.md` exists — I'll just infer the topology and start writing Terraform" | Inferring topology duplicates `ywc-infra-design`'s decision and compounds the error downstream. Either ask the user to run `$ywc-infra-design` first, or explicitly clarify inline intent (service list, provider, network boundary) and record it before authoring — never guess silently. |
| "`terraform plan` looks safe, I'll run `apply` to confirm it actually works" | `apply` mutates live infrastructure and is irreversible for destroy operations. This skill and its worker stop at `plan`; `apply` requires explicit human approval outside this skill's scope. |
| "Kubernetes work is easier as a raw manifest or a Helm chart" | Terraform is fixed as the single IaC tool for this toolkit. K8s/Helm resources go through the Terraform `kubernetes` / `helm` providers so the same validate/plan/state discipline applies uniformly — raw manifests and standalone Helm bypass that discipline. |
| "I'll hardcode the DB password as a default so `plan` runs cleanly" | Hardcoded secrets leak into `.tf` files, version control, and Terraform state (which itself must never be committed). Route sensitive values through variables, `TF_VAR_*`, or a secret manager reference. |
| "Terraform state is only local for now, I'll commit it so the next run skips `init`" | `*.tfstate` and `*.tfstate.backup` can contain plaintext secrets and resource IDs; committing them is a leak, not a convenience. Use a remote backend with locking (S3+DynamoDB, GCS, azurerm, Terraform Cloud) and gitignore state files. |
| "The plan output is long, I'll just say 'a few resources change'" | The blast-radius summary must report the exact add/change/destroy counts and name every destroy against a stateful resource (DB, bucket, volume) explicitly — vague summaries hide data-loss risk from the reviewer. |
| "This is a tiny IaC change, I'll skip recommending `ywc-infra-review`" | Even small Terraform diffs can widen a security group or loosen an IAM policy. Recommending `$ywc-infra-review` after authoring is not optional ceremony — it is the pre-apply safety net this skill hands off to. |

**Violating the letter of these rules is violating the spirit.** An IaC authoring pass that skips validate/plan discipline or applies without review turns a code review problem into a production incident.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--design-doc` | `--design-doc <path>` | `--design-doc infra-design.md` | Path to the `ywc-infra-design` output to load as the authoring input. Omit to fall back to inline intent clarification (Step 1). |
| `--scope` | `--scope <module-path>` | `--scope infra/modules/network` | Restrict authoring to a single Terraform module. Default: every module implied by the design input. |
| `--skip-review-recommendation` | flag | `--skip-review-recommendation` | Skip the closing `ywc-infra-review` recommendation. Only valid when the upstream caller already schedules review itself. |

## Workflow

### Step 1: Load the design input, or clarify inline intent

If `--design-doc` is provided or an `infra-design.md` (the `ywc-infra-design` output contract) exists in the working context, load it as the authoring source of truth: service list, network topology, IAM boundaries, data stores, and the reliability/cost/security trade-off notes it recorded.

If no design input exists, do not infer the topology. Clarify inline with the user: target provider (AWS/GCP/Azure/K8s), the services/resources involved, and any network or IAM constraints — then record that intent before moving to Step 2. For anything beyond a small, well-understood change, recommend the user run `$ywc-infra-design` first.

### Step 2: Load the fixed IaC tool reference

Read `../references/infra/iac/terraform.md` — the canonical `fmt → init → validate → plan → (human approval) → apply` workflow, blast-radius reporting shape, and state-management guards. This is the only IaC-tool reference this skill loads; Terraform is fixed and no other IaC tool reference exists in this toolkit.

Load the provider-specific reference matching the design's target provider — only the one file needed, per Progressive Disclosure:

- `../references/infra/providers/aws.md`
- `../references/infra/providers/gcp.md`
- `../references/infra/providers/azure.md`
- `../references/infra/providers/k8s.md` — Kubernetes/Helm via the Terraform `kubernetes`/`helm` providers

### Step 3: Author per Terraform module with optional advisory consult

For each Terraform module implied by the design (network, compute, data store, IAM, etc.), or a single narrowed pass when `--scope` targets one module, author the `.tf` files in the current Codex session. When provider-specific feasibility, reliability, or blast-radius judgment is unclear, consult the read-only `ywc-cloud-engineer` persona with the relevant slice of the design input and the matching provider reference from Step 2. That consult is advisory only: it does not author files, run `terraform apply`, or replace the main session's ownership of the Terraform edits.

### Step 4: Verify — `terraform validate` / `terraform plan`

Confirm each authored module returned a clean `terraform validate` and a completed `terraform plan` (per the terraform.md verification workflow). If an advisory consult returns `BLOCKED` or `NEEDS_CONTEXT` (missing design input, unresolved provider constraint, blast-radius ambiguity), surface it rather than papering over it with a guess.

### Step 5: Blast-radius summary

Aggregate every module's `plan` headline into one summary: total resources to add / change / destroy, with every destructive change against a stateful resource (database, bucket, volume, persistent disk) called out explicitly. See Output Format below for the exact shape.

### Step 6: State handling and secret externalization guards

Before closing out, confirm:

- No `*.tfstate` / `*.tfstate.backup` / `.terraform/` was staged or committed.
- No `.tfvars` file containing a literal secret was staged or committed.
- Every credential, password, or API key in the authored `.tf` files flows through a variable, `TF_VAR_*`, or a secret-manager data source — never a hardcoded default.
- A remote backend with locking is configured (or already exists) for any module holding state that matters beyond a single local run.

### Step 7: Recommend `ywc-infra-review`

Unless `--skip-review-recommendation` was passed, close the authoring pass by recommending the user run `$ywc-infra-review` before `apply` — especially when the blast radius includes a security group, IAM policy, or public-exposure change.

## Output Format

```text
IaC Authoring Report
─────────────────────────────────────────────────
Design input:    infra-design.md  (or "inline intent" if none was provided)
Tool:            Terraform (single fixed tool)
Modules authored:
  - infra/modules/network      (authoring in current session, advisory consult optional)  validate: PASS  plan: PASS
  - infra/modules/data         (authoring in current session, advisory consult optional)  validate: PASS  plan: PASS

Blast radius (aggregate):
  Plan: 9 to add, 3 to change, 1 to destroy.
  ⚠ destroy: aws_db_instance.legacy   (stateful — confirm backup/snapshot before apply)

State handling:
  - No *.tfstate staged or committed
  - Remote backend: S3 + DynamoDB (configured)

Secrets:
  - 0 hardcoded credentials found; DB password routed through TF_VAR_db_password
─────────────────────────────────────────────────
Recommended next step: $ywc-infra-review (before apply)
```

## Validation Checklist

Before declaring the authoring pass complete, verify:

- [ ] The design input was loaded, or inline intent was explicitly clarified and recorded (never silently inferred)
- [ ] Every dispatched module returned `terraform validate` PASS
- [ ] Every dispatched module returned a completed `terraform plan` (no live `apply` executed)
- [ ] The blast-radius summary names every destroy against a stateful resource
- [ ] No `.tfstate` file and no literal secret in a `.tfvars` file was staged or committed
- [ ] Every secret in authored `.tf` files flows through a variable or secret-manager reference
- [ ] `$ywc-infra-review` was recommended, unless `--skip-review-recommendation` was passed by an upstream caller

## Common Mistakes

- **Re-deriving the topology instead of loading the design input.** When `infra-design.md` exists, use it verbatim — re-deriving from scratch risks drifting from the reviewed trade-offs (network CIDR choices, IAM boundaries) that design phase already settled.
- **Treating the advisory consult as the authoring worker.** The `ywc-cloud-engineer` persona is read-only; it can clarify feasibility or blast radius, but the current Codex session owns the Terraform edits.
- **Treating a `NEEDS_CONTEXT` return from the advisory consult as a prompt to guess and continue.** The consult returns `NEEDS_CONTEXT` specifically when the design decision it needs is missing — surface it to the user rather than filling the gap with an assumption.
- **Skipping Step 6's state/secret guard because `plan` already succeeded.** `terraform plan` succeeding says nothing about whether a secret is hardcoded or whether state got staged — that check is separate and mandatory every pass.

## Integration

- **Upstream**: `ywc-infra-design` (produces the `infra-design.md` input contract); direct user invocation with inline intent when no design phase is warranted.
- **Downstream**: `ywc-infra-review` (recommended after every authoring pass, mandatory before `apply` when the blast radius touches security/IAM/public exposure).
- **Pairs with**: `ywc-cloud-engineer` persona (the read-only specialist that advises on feasibility, reliability, and blast radius while this skill authors the Terraform).
- **Must not be paired with**: authoring a second IaC tool in the same change (Pulumi/CDK/CloudFormation/Bicep/standalone Helm) — Terraform is fixed.

## References

| Reference | Use when |
|---|---|
| `../references/infra/iac/terraform.md` | Every authoring pass — the fixed tool's verification workflow, blast-radius reporting shape, and state guards |
| `../references/infra/providers/aws.md` | Design's target provider is AWS |
| `../references/infra/providers/gcp.md` | Design's target provider is GCP |
| `../references/infra/providers/azure.md` | Design's target provider is Azure |
| `../references/infra/providers/k8s.md` | Design's target includes Kubernetes/Helm (via Terraform providers) |
| `../references/infra/lenses/security.md` | Spot-checking for an obvious misconfiguration (public bucket, open security group) while authoring, ahead of the full `ywc-infra-review` pass |
| `../references/infra/lenses/cost.md` | Flagging an obviously oversized resource while authoring, ahead of `ywc-infra-optimize` |
| `../references/infra/lenses/reliability.md` | Confirming a new module has basic redundancy/backup coverage before handing off to review |
