# ywc-iac-author

Infrastructure-as-Code authoring skill. Turns an infrastructure design (or clarified inline intent) into Terraform in the current Codex session, consults the read-only `ywc-cloud-engineer` persona when feasibility or blast-radius advice is needed, verifies with `terraform validate` / `terraform plan`, and reports a blast-radius summary before anything is applied. **Terraform is the single fixed IaC tool** for this toolkit — Kubernetes/Helm resources are expressed through the Terraform `kubernetes` / `helm` providers, never raw manifests or a second IaC tool.

## Localized Versions

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## When to Use

- The user says "write terraform", "author IaC", "provision infrastructure", "IaC 작성해줘", "terraform 작성해줘", "인프라 코드 만들어줘", "IaC を書いて"
- An `ywc-infra-design` output (`infra-design.md`) is ready and needs to become working Terraform
- A small, well-understood infra change is needed and the user wants to skip a separate design phase (inline intent)

## How to Invoke

```bash
$ywc-iac-author --design-doc infra-design.md
```

Or in natural language:

> "author the Terraform for this design"
> "write the IaC for the network module"

## Inputs

- (optional) `--design-doc <path>` — the `ywc-infra-design` output to load as the authoring source of truth. Falls back to inline intent clarification if omitted.
- (optional) `--scope <module-path>` — restrict authoring to a single Terraform module (default: every module implied by the design)
- (optional) `--skip-review-recommendation` — only valid when the upstream caller already schedules `ywc-infra-review` itself

## Outputs

- Terraform modules authored in the current Codex session, each with a clean `terraform validate` and a completed `terraform plan`
- An IaC Authoring Report: blast-radius summary (add/change/destroy, destructive changes on stateful resources called out), state-handling confirmation, and a secrets-externalization check
- A closing recommendation to run `ywc-infra-review` before `apply` (unless skipped)

## Related Skills

- `ywc-infra-design` — upstream; produces the `infra-design.md` input contract this skill loads
- `ywc-cloud-engineer` — the read-only specialist persona for feasibility, reliability, and blast-radius advisory
- `ywc-infra-review` — downstream; recommended pre-apply review of the authored IaC
- `ywc-infra-optimize` — cost/right-sizing remediation on *existing* infrastructure (not this skill's job)
- `ywc-backend-coder` — application server / business logic (not infrastructure)
- `ywc-docker-isolate` — local worktree Docker port isolation only, not production infrastructure
