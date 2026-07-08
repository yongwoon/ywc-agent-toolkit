---
name: ywc-infra-review
description: >-
  (ywc) Use when reviewing IaC / cloud configuration for misconfiguration,
  least-privilege, cost, and reliability before applying — security groups,
  IAM/RBAC, public exposure, secrets in state, cost right-sizing, idle
  resources, pricing model, SPOF, missing backups, resource limits, and
  health checks across AWS/GCP/Azure/K8s Terraform. Fans out to
  security/cost/reliability lenses and aggregates severity-rated findings.
  Triggers: "인프라 리뷰", "IaC 리뷰", "terraform 검토", "보안 그룹 점검",
  "iam 과권한", "infra review", "review my terraform", "IaC review",
  "インフラレビュー", "ywc-infra-review". Do not use for app-code
  auth/injection review (use ywc-security-audit), writing IaC (use
  ywc-iac-author), executing cost/drift remediation (use
  ywc-infra-optimize), or general application code review (use
  ywc-impl-review).
---

# ywc-infra-review

**Announce at start:** "I'm using the ywc-infra-review skill to review this IaC / cloud configuration across the security, cost, and reliability lenses before it is applied."

This skill is the standalone review-phase counterpart to `ywc-iac-author`: it fans an already-authored Terraform change out to three independent lenses — security (misconfiguration, least-privilege), cost (right-sizing, waste), and reliability (SPOF, backups, health) — then aggregates every finding into one severity-rated report. **This skill never writes or modifies IaC.** Terraform is the single fixed IaC tool for this toolkit; provider coverage is AWS/GCP/Azure/K8s expressed through the Terraform providers, the same scope `ywc-iac-author` authors against.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "We're short on time, I'll skip the cost lens and just run security + reliability" | All three lenses run every pass — a CRITICAL security finding does not excuse missing a HIGH-severity idle-resource waste or an over-provisioned instance. Each lens covers a non-overlapping taxonomy; skipping one blinds the review to that entire dimension. |
| "This is really an application-security question, I'll route it to ywc-security-audit instead" | `ywc-security-audit` reviews app-code auth/injection (OWASP Top 10 on source). This skill's security lens reviews IaC misconfiguration (security groups, IAM policies, public exposure, secrets in state) — a different taxonomy entirely, defined in `references/iac-security.md`. |
| "I found a CRITICAL finding, I'll just fix the `.tf` file inline instead of routing to infra-optimize" | This skill is diagnosis-only — it has no write access to IaC. Auto-fixing here bypasses the `terraform validate`/`plan` discipline that the `ywc-cloud-engineer` persona and `ywc-infra-optimize` own. Report the finding; route remediation downstream. |
| "The plan output was clean, I'll recommend apply even though a lens flagged CRITICAL" | A clean `terraform plan` only proves syntactic validity, not policy safety. Every CRITICAL/HIGH finding recommends **blocking** apply regardless of plan success — the two signals answer different questions. |
| "One lens already looks thorough, the other two are probably fine too" | A security-clean, cost-wasteful, single-AZ deployment passes the security lens and fails the other two. Each lens must be dispatched and its findings recorded independently — a strong result in one lens is not evidence for the others. |
| "This is a one-line security-group diff, full review is overkill" | A one-line CIDR change can open `0.0.0.0/0` ingress to a database port. Blast radius does not correlate with diff size — every reviewable change gets the same 3-lens pass. |

**Violating the letter of these rules is violating the spirit.** A review pass that skips a lens, auto-fixes inline, or waves through a CRITICAL finding turns a pre-apply safety net into a rubber stamp.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--scope` | `--scope <path>` | `--scope infra/modules/network` | Restrict the review fan-out to a single Terraform module or path instead of the whole IaC tree. |
| `--skip-optimize-recommendation` | flag | `--skip-optimize-recommendation` | Skip the closing `ywc-infra-optimize` recommendation. Only valid when the upstream caller already schedules remediation itself. |

## Workflow

### Step 1: Determine review scope

Identify the Terraform files/modules under review: a staged or committed diff, the `terraform plan` output if the caller already has one, or the full IaC tree when `--scope` is omitted. Record the scope so all three lens dispatches review the identical surface — a lens reviewing a narrower scope than another produces findings that cannot be cross-checked.

> **Fan-out return contract**: this skill dispatches three workers. Each lens worker (Steps 2–4) must return the bounded status payload from `../references/subagent-status-actions.md` §3.5 — `Status | 1-line summary | artifact path | Concerns (<=10 lines)`, with full findings written to a file whose path is returned. Three verbose lens dumps would otherwise saturate this skill's context before aggregation (Step 5).

### Step 2: Security lens

Dispatch a Codex worker carrying the `ywc-security-engineer` persona, carrying the scoped Terraform files and an explicit pointer to `../references/lenses/security.md` and `../references/iac-security.md`. This lens covers: security groups / firewall rules, IAM / RBAC over-permission, public exposure (buckets, endpoints, load balancers), and secrets committed to code or state.

### Step 3: Cost lens

Dispatch a Codex worker carrying the `ywc-performance-engineer` persona, carrying the scoped Terraform files and an explicit pointer to `../references/lenses/cost.md` and `../references/finops.md`. This lens covers: compute right-sizing against observed/expected utilization, idle or orphaned resources, and pricing model fit (on-demand vs reserved vs spot).

### Step 4: Reliability lens

Dispatch a Codex worker carrying the `ywc-cloud-engineer` persona in **review mode** — carry the scoped Terraform files and an explicit instruction that this dispatch is read-only diagnosis: it authors nothing, runs no `terraform apply`, and confines itself to the reliability lens at `../references/lenses/reliability.md`. This lens covers: single points of failure, missing backups / point-in-time recovery, missing resource limits or autoscaling floors, and missing health/readiness checks.

### Step 5: Aggregate severity-rated findings

Collect all three lenses' findings into one report. Deduplicate a finding that two lenses independently flag on the same resource (e.g., a public DB is both a security and a reliability concern — report once, tag both lenses). Rate every finding Critical / High / Medium / Low using each lens reference's severity guidance. Any **CRITICAL or HIGH** finding recommends **blocking** the apply until remediated.

### Step 6: Recommend `ywc-infra-optimize` for remediation

Unless `--skip-optimize-recommendation` was passed, close the review by recommending the user run `$ywc-infra-optimize` to execute cost/drift remediation, or route reliability/security fixes back through `$ywc-iac-author`. This skill diagnoses; it does not remediate.

## Output Format

```text
Infra Review Report
─────────────────────────────────────────────────
Scope:        infra/modules/network  (or "full IaC tree")
Lenses run:   Security | Cost | Reliability  (all three, every pass)

Findings (severity-rated):
CRITICAL
  - [Security] aws_security_group.db ingress 0.0.0.0/0:5432 — scope CIDR to app subnet
HIGH
  - [Reliability] aws_db_instance.primary — no multi-AZ, no automated backups — enable multi-AZ + 7-day backup retention
MEDIUM
  - [Cost] aws_instance.worker — m5.4xlarge at 8% avg CPU over 30d — right-size to m5.large

Apply recommendation: BLOCK (1 CRITICAL, 1 HIGH found)
─────────────────────────────────────────────────
Recommended next step: $ywc-infra-optimize (cost/drift remediation), or $ywc-iac-author (security/reliability fixes)
```

## Validation Checklist

Before declaring the review pass complete, verify:

- [ ] All three lenses (security, cost, reliability) were dispatched against the identical scope — none skipped
- [ ] Every finding is severity-rated (Critical / High / Medium / Low), not left unrated
- [ ] Every CRITICAL/HIGH finding includes a concrete remediation and the report states an explicit BLOCK recommendation
- [ ] A finding flagged by more than one lens on the same resource is reported once, with both lens tags
- [ ] The reliability lens dispatch to the `ywc-cloud-engineer` persona was explicitly instructed as review-only (no authoring, no `apply`)
- [ ] `$ywc-infra-optimize` was recommended for remediation, unless `--skip-optimize-recommendation` was passed by an upstream caller

## Common Mistakes

- **Skipping a lens because the other two already found enough.** Each lens's taxonomy is non-overlapping — a clean security lens says nothing about cost waste or SPOF risk.
- **Auto-fixing a CRITICAL finding inline.** This skill has no write access by design; remediation routes to `$ywc-infra-optimize` (cost/drift) or `$ywc-iac-author` (re-authoring), never inline.
- **Treating a clean `terraform plan` as sufficient.** `plan` validates syntax and diff shape, not policy — the lens findings are the actual safety gate.
- **Confusing this skill with `ywc-security-audit`.** That skill reviews application-code auth/injection; this skill's security lens reviews IaC misconfiguration — different taxonomy, different worker dispatch.

## Integration

- **Upstream**: `ywc-iac-author` (produces the Terraform this skill reviews); direct user invocation against any existing Terraform tree.
- **Downstream**: `ywc-infra-optimize` (executes cost/drift remediation); `ywc-iac-author` (re-authoring for security/reliability fixes).
- **Consults**: `ywc-security-engineer` persona (security lens), `ywc-performance-engineer` persona (cost lens), `ywc-cloud-engineer` persona in review mode (reliability lens).
- **Must not be paired with**: writing or modifying `.tf` files in the same pass — that boundary belongs to `ywc-iac-author` and `ywc-infra-optimize`.

## References

| Reference | Use when |
|---|---|
| `../references/lenses/security.md` | Step 2 — security lens dispatch, IaC misconfiguration taxonomy |
| `../references/iac-security.md` | Step 2 — the detailed IaC misconfiguration taxonomy the `ywc-security-engineer` persona reviews against |
| `../references/lenses/cost.md` | Step 3 — cost lens dispatch, right-sizing and waste taxonomy |
| `../references/finops.md` | Step 3 — the detailed FinOps taxonomy (reserved/spot, data-transfer cost) the `ywc-performance-engineer` persona reviews against |
| `../references/lenses/reliability.md` | Step 4 — reliability lens dispatch, SPOF/backup/health taxonomy |
| `../references/providers/aws.md` | Scoped IaC targets AWS — provider-specific misconfiguration/cost/reliability signals |
| `../references/providers/gcp.md` | Scoped IaC targets GCP — provider-specific misconfiguration/cost/reliability signals |
| `../references/providers/azure.md` | Scoped IaC targets Azure — provider-specific misconfiguration/cost/reliability signals |
| `../references/providers/k8s.md` | Scoped IaC includes Kubernetes/Helm (via Terraform providers) |
| `../references/subagent-status-actions.md` | Steps 2–4 — the §3.5 bounded status-return contract each lens worker must follow so three fan-out returns stay bounded |
