---
name: ywc-iac-author
description: >-
  (ywc) Use when authoring or modifying Infrastructure-as-Code from a design —
  Terraform for AWS/GCP/Azure/Kubernetes (K8s/Helm via Terraform
  kubernetes/helm providers, never raw manifests or a second IaC tool),
  including validate/plan verification and a blast-radius summary. Triggers:
  "IaC 작성", "terraform 작성", "인프라 코드", "k8s 매니페스트", "write terraform",
  "author IaC", "provision infrastructure", "IaC を書いて", "ywc-iac-author".
  Do not use for app logic (ywc-backend-coder), topology design
  (ywc-infra-design), IaC review (ywc-infra-review), cost remediation
  (ywc-infra-optimize), or local docker port collisions (ywc-docker-isolate —
  dev-only, not prod infra).
category: implement
phase: implementation
requires: []
---

# ywc-iac-author

**Announce at start:** "I'm using the ywc-iac-author skill to author Terraform from a design, verify it with validate/plan, and summarize the blast radius."

This skill is the Infrastructure-as-Code counterpart to `ywc-code-gen`: it turns an infrastructure design into working Terraform, fans out per-module authoring to the `ywc-cloud-engineer` worker, verifies with `terraform validate` / `terraform plan`, and reports a blast-radius summary before anything is applied. **Terraform is the single fixed IaC tool for this toolkit** — Kubernetes and Helm resources are expressed through the Terraform `kubernetes` / `helm` providers, never raw manifests, a standalone Helm chart, or a second IaC tool (Pulumi / CDK / CloudFormation / Bicep).

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "No `infra-design.md` exists — I'll just infer the topology and start writing Terraform" | Inferring topology duplicates `ywc-infra-design`'s decision and compounds the error downstream. Either ask the user to run `ywc-infra-design` first, or explicitly clarify inline intent (service list, provider, network boundary) and record it before authoring — never guess silently. |
| "`terraform plan` looks safe, I'll run `apply` to confirm it actually works" | `apply` mutates live infrastructure and is irreversible for destroy operations. This skill and its worker stop at `plan`; `apply` requires explicit human approval outside this skill's scope. |
| "Kubernetes work is easier as a raw manifest or a Helm chart" | Design §7 fixes Terraform as the single IaC tool. K8s/Helm resources go through the Terraform `kubernetes` / `helm` providers so the same validate/plan/state discipline applies uniformly — raw manifests and standalone Helm bypass that discipline. |
| "I'll hardcode the DB password as a default so `plan` runs cleanly" | Hardcoded secrets leak into `.tf` files, version control, and Terraform state (which itself must never be committed). Route sensitive values through variables, `TF_VAR_*`, or a secret manager reference. |
| "Terraform state is only local for now, I'll commit it so the next run skips `init`" | `*.tfstate` and `*.tfstate.backup` can contain plaintext secrets and resource IDs; committing them is a leak, not a convenience. Use a remote backend with locking (S3+DynamoDB, GCS, azurerm, Terraform Cloud) and gitignore state files. |
| "The plan output is long, I'll just say 'a few resources change'" | The blast-radius summary must report the exact add/change/destroy counts and name every destroy against a stateful resource (DB, bucket, volume) explicitly — vague summaries hide data-loss risk from the reviewer. |
| "This is a tiny IaC change, I'll skip recommending `ywc-infra-review`" | Even small Terraform diffs can widen a security group or loosen an IAM policy. Recommending `ywc-infra-review` after authoring is not optional ceremony — it is the pre-apply safety net this skill hands off to. |

**Violating the letter of these rules is violating the spirit.** An IaC authoring pass that skips validate/plan discipline or applies without review turns a code review problem into a production incident.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--design-doc` | `--design-doc <path>` | `--design-doc infra-design.md` | Path to the `ywc-infra-design` output to load as the authoring input. Omit to fall back to inline intent clarification (Step 1). |
| `--scope` | `--scope <module-path>` | `--scope infra/modules/network` | Restrict authoring/fan-out to a single Terraform module. Default: every module implied by the design input. |
| `--skip-review-recommendation` | flag | `--skip-review-recommendation` | Skip the closing `ywc-infra-review` recommendation. Only valid when the upstream caller (e.g., an orchestrating skill) already schedules review itself. |

## Workflow

### Step 1: Load the design input, or clarify inline intent

If `--design-doc` is provided or an `infra-design.md` (the `ywc-infra-design` output contract) exists in the working context, load it as the authoring source of truth: service list, network topology, IAM boundaries, data stores, and the reliability/cost/security trade-off notes it recorded.

If no design input exists, do not infer the topology. Clarify inline with the user: target provider (AWS/GCP/Azure/K8s), the services/resources involved, and any network or IAM constraints — then record that intent before moving to Step 2. For anything beyond a small, well-understood change, recommend the user run `ywc-infra-design` first.

### Step 2: Load the fixed IaC tool reference

Read [`../references/iac-tools/terraform.md`](../references/iac-tools/terraform.md) — the canonical `fmt → init → validate → plan → (human approval) → apply` workflow, blast-radius reporting shape, and state-management guards. This is the only IaC-tool reference this skill loads; per design §7, Terraform is fixed and no other IaC tool reference exists in this toolkit.

Load the provider-specific reference matching the design's target provider — only the one file needed, per Progressive Disclosure:

- [`../references/providers/aws.md`](../references/providers/aws.md)
- [`../references/providers/gcp.md`](../references/providers/gcp.md)
- [`../references/providers/azure.md`](../references/providers/azure.md)
- [`../references/providers/k8s.md`](../references/providers/k8s.md) — Kubernetes/Helm via the Terraform `kubernetes`/`helm` providers

### Step 3: Fan out to `ywc-cloud-engineer` per Terraform module

Dispatch `Task(subagent_type: ywc-cloud-engineer)` once per Terraform module implied by the design (network, compute, data store, IAM, etc.), or a single dispatch when `--scope` narrows the work to one module. Each dispatch carries: the relevant slice of the design input, the target provider reference from Step 2, and the module's declared edit scope (so concurrent module dispatches do not collide on the same files).

`ywc-cloud-engineer` is a single-responsibility worker — it authors `.tf` files, runs `terraform validate`/`terraform plan` on its own module, and self-reviews against the reliability lens. It never runs `terraform apply`.

### Step 4: Verify — `terraform validate` / `terraform plan`

Confirm each dispatched module returned a clean `terraform validate` and a completed `terraform plan` (per [`../references/iac-tools/terraform.md`](../references/iac-tools/terraform.md)'s verification workflow). A module that returns `BLOCKED` or `NEEDS_CONTEXT` (missing design input, unresolvable module dependency, provider credentials unavailable) is not authored — surface it rather than papering over it with a guess.

### Step 5: Blast-radius summary

Aggregate every module's `plan` headline into one summary: total resources to add / change / destroy, with every destructive change against a stateful resource (database, bucket, volume, persistent disk) called out explicitly. See Output Format below for the exact shape.

### Step 6: State handling and secret externalization guards

Before closing out, confirm:

- No `*.tfstate` / `*.tfstate.backup` / `.terraform/` was staged or committed.
- No `.tfvars` file containing a literal secret was staged or committed.
- Every credential, password, or API key in the authored `.tf` files flows through a variable, `TF_VAR_*`, or a secret-manager data source — never a hardcoded default.
- A remote backend with locking is configured (or already exists) for any module holding state that matters beyond a single local run.

### Step 7: Recommend `ywc-infra-review`

Unless `--skip-review-recommendation` was passed, close the authoring pass by recommending the user run `ywc-infra-review` before `apply` — especially when the blast radius includes a security group, IAM policy, or public-exposure change.

## Output Format

```text
IaC Authoring Report
─────────────────────────────────────────────────
Design input:    infra-design.md  (or "inline intent" if none was provided)
Tool:            Terraform (single fixed tool — design §7)
Modules authored:
  - infra/modules/network      (ywc-cloud-engineer)  validate: PASS  plan: PASS
  - infra/modules/data         (ywc-cloud-engineer)  validate: PASS  plan: PASS

Blast radius (aggregate):
  Plan: 9 to add, 3 to change, 1 to destroy.
  ⚠ destroy: aws_db_instance.legacy   (stateful — confirm backup/snapshot before apply)

State handling:
  - No *.tfstate staged or committed
  - Remote backend: S3 + DynamoDB (configured)

Secrets:
  - 0 hardcoded credentials found; DB password routed through TF_VAR_db_password
─────────────────────────────────────────────────
Recommended next step: ywc-infra-review (before apply)
```

## Validation Checklist

Before declaring the authoring pass complete, verify:

- [ ] The design input was loaded, or inline intent was explicitly clarified and recorded (never silently inferred)
- [ ] Every dispatched `ywc-cloud-engineer` module returned `terraform validate` PASS
- [ ] Every dispatched module returned a completed `terraform plan` (no live `apply` executed)
- [ ] The blast-radius summary names every destroy against a stateful resource
- [ ] No `.tfstate` file and no literal secret in a `.tfvars` file was staged or committed
- [ ] Every secret in authored `.tf` files flows through a variable or secret-manager reference
- [ ] `ywc-infra-review` was recommended, unless `--skip-review-recommendation` was passed by an upstream caller

## Common Mistakes

- **Re-deriving the topology instead of loading the design input.** When `infra-design.md` exists, use it verbatim — re-deriving from scratch risks drifting from the reviewed trade-offs (network CIDR choices, IAM boundaries) that design phase already settled.
- **Dispatching all modules to a single `ywc-cloud-engineer` call.** Fan out per module so each dispatch carries a narrow, non-overlapping edit scope — a single mega-dispatch loses the module-level `validate`/`plan` isolation and makes a failing module harder to isolate.
- **Treating a `NEEDS_CONTEXT` return from the worker as a prompt to guess and continue.** The worker returns `NEEDS_CONTEXT` specifically when the design decision it needs is missing — surface it to the user rather than filling the gap with an assumption.
- **Skipping Step 6's state/secret guard because `plan` already succeeded.** `terraform plan` succeeding says nothing about whether a secret is hardcoded or whether state got staged — that check is separate and mandatory every pass.

## Integration

- **Upstream**: `ywc-infra-design` (produces the `infra-design.md` input contract); direct user invocation with inline intent when no design phase is warranted.
- **Downstream**: `ywc-infra-review` (recommended after every authoring pass, mandatory before `apply` when the blast radius touches security/IAM/public exposure).
- **Pairs with**: `ywc-cloud-engineer` (the fan-out worker that authors and verifies each Terraform module).
- **Must not be paired with**: authoring a second IaC tool in the same change (Pulumi/CDK/CloudFormation/Bicep/standalone Helm) — Terraform is fixed per design §7.

## References

| Reference | Use when |
|---|---|
| [`../references/iac-tools/terraform.md`](../references/iac-tools/terraform.md) | Every authoring pass — the fixed tool's verification workflow, blast-radius reporting shape, and state guards |
| [`../references/providers/aws.md`](../references/providers/aws.md) | Design's target provider is AWS |
| [`../references/providers/gcp.md`](../references/providers/gcp.md) | Design's target provider is GCP |
| [`../references/providers/azure.md`](../references/providers/azure.md) | Design's target provider is Azure |
| [`../references/providers/k8s.md`](../references/providers/k8s.md) | Design's target includes Kubernetes/Helm (via Terraform providers) |
| [`../references/lenses/security.md`](../references/lenses/security.md) | Spot-checking for an obvious misconfiguration (public bucket, open security group) while authoring, ahead of the full `ywc-infra-review` pass |
| [`../references/lenses/cost.md`](../references/lenses/cost.md) | Flagging an obviously oversized resource while authoring, ahead of `ywc-infra-optimize` |
| [`../references/lenses/reliability.md`](../references/lenses/reliability.md) | Confirming a new module has basic redundancy/backup coverage before handing off to review |
