# Terraform — IaC Tool Reference

> Shared reference for the infra skill suite. Per design §7, **Terraform is the
> single fixed IaC tool** for this toolkit. CDK, Pulumi, CloudFormation, Bicep,
> and standalone Helm are intentionally *not* authored — Kubernetes/Helm go
> through the Terraform `kubernetes`/`helm` providers. This file is the shared
> workflow + guardrail contract every infra skill links.

## The verification workflow (non-negotiable order)

```
terraform fmt      # canonical formatting — run before commit
terraform init     # provider + module download, backend init
terraform validate # syntax + internal consistency (no cloud calls)
terraform plan      # shows blast radius: add / change / destroy
# → human reviews the plan →
terraform apply     # ONLY after approval; mutates real infrastructure
```

- Skills and the `ywc-cloud-engineer` worker **stop at `plan`**. `apply` against
  live infrastructure requires explicit human approval — never auto-apply.
- Always read the plan's **destroy** count first. A non-zero destroy on a
  stateful resource (DB, bucket, volume) is a data-loss risk and must be called
  out.

## Blast-radius summary (what to report)

After `plan`, report the headline, not the full log:

```
Plan: 6 to add, 2 to change, 1 to destroy.
  ⚠ destroy: aws_db_instance.legacy  (stateful — confirm backup/snapshot)
```

## State management guards

- **Never commit state** — `*.tfstate`, `*.tfstate.backup`, `.terraform/`, and
  `*.tfvars` with secrets belong in `.gitignore`, never in a commit.
- **Use a remote backend** with locking (S3 + DynamoDB, GCS, azurerm, or
  Terraform Cloud). Local state does not scale to a team and has no locking.
- **State contains secrets** — DB passwords, generated keys, and tokens land in
  state in plaintext; treat the backend as a secret store (encrypt at rest,
  restrict access).

## Secret externalization guards

- No hardcoded credentials in `.tf` — use `variable` + `TF_VAR_*` env, or a
  secret manager data source (`aws_secretsmanager_secret_version`,
  `google_secret_manager_secret_version`, `azurerm_key_vault_secret`).
- Mark sensitive outputs/variables `sensitive = true` so they are redacted in
  plan/apply logs.
- Provider auth flows through the environment (SSO, assumed role, workload
  identity, managed identity) — never a static key in the config.

## Module hygiene

- Prefer small, composable modules with explicit `variables.tf` /
  `outputs.tf`; pin module `source` versions.
- Pin provider versions with `~>` in `required_providers`.
- Use `for_each` over `count` for keyed collections (stable addressing on
  add/remove); `count` reindexes and can force needless recreation.
- Avoid `depends_on` unless a real hidden dependency exists — let Terraform
  infer ordering from references.

## Review lenses

Every IaC change is reviewed through three lenses — see
[`../lenses/security.md`](../lenses/security.md),
[`../lenses/cost.md`](../lenses/cost.md), and
[`../lenses/reliability.md`](../lenses/reliability.md).
