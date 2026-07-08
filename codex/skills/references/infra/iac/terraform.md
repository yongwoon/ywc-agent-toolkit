# Terraform — IaC Tool Reference

> Shared reference for the infra skill suite. **Terraform is the single fixed
> IaC tool** for this toolkit. CDK, Pulumi, CloudFormation, Bicep, and
> standalone Helm are intentionally out of scope. Kubernetes and Helm resources
> are handled through the Terraform `kubernetes` and `helm` providers.

## Verification Workflow

```bash
terraform fmt
terraform init
terraform validate
terraform plan
```

- Skills and `ywc-cloud-engineer` stop at `terraform plan`.
- `terraform apply` requires explicit human approval.
- Always review the `destroy` count first and call out any stateful resource.

## Blast-Radius Summary

After `plan`, report the headline rather than the full log:

```text
Plan: 6 to add, 2 to change, 1 to destroy.
```

- Highlight destroys separately when they affect DBs, buckets, or volumes.
- Summarize add / change / destroy counts in review output.

## State And Secret Guards

- Never commit `*.tfstate`, `*.tfstate.backup`, `.terraform/`, or secret-bearing
  `*.tfvars`.
- Use a remote backend with locking.
- Treat Terraform state as sensitive because it can contain plaintext secrets.
- Externalize credentials through variables, `TF_VAR_*`, or secret-manager data
  sources.
- Mark secret outputs and variables `sensitive = true`.

## Module Hygiene

- Prefer small, composable modules with explicit inputs and outputs.
- Pin provider versions in `required_providers`.
- Prefer `for_each` over `count` for keyed collections.
- Avoid `depends_on` unless a real hidden dependency exists.

## Review Lenses

Every IaC change is reviewed through three shared lenses:

- [Security](../lenses/security.md)
- [Cost](../lenses/cost.md)
- [Reliability](../lenses/reliability.md)
