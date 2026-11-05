---
name: ywc-infra-review
description: >-
  (ywc) Use when reviewing bounded Terraform plans, diffs, topology packets,
  or applied scoped IaC for security, cost, and reliability.
  Triggers: "인프라 리뷰", "IaC 리뷰", "infra review", "インフラレビュー".
  Do not use for app-code auth/injection review (use ywc-security-audit),
  writing IaC (use ywc-iac-author), or applied-environment optimization
  sweeps (use ywc-infra-optimize).
---

# ywc-infra-review

**Announce at start:** "I'm using the ywc-infra-review skill to review the supplied infrastructure evidence across security, cost, and reliability before any apply decision."

This skill is the standalone review-phase counterpart to `ywc-iac-author`: it fans an already-authored Terraform change out to three independent lenses — security (misconfiguration, least-privilege), cost (right-sizing, waste), and reliability (SPOF, backups, health) — then aggregates every finding into one severity-rated report. **This skill never writes or modifies IaC.** Terraform is the single fixed IaC tool for this toolkit; provider coverage is AWS/GCP/Azure/K8s expressed through the Terraform providers, the same scope `ywc-iac-author` authors against.

The applied-scope and bounded FinOps contracts are adapted from `yongwoon/develop-with-llm` #348, frozen merge `29068f9f690fbf09e0ace8d562e4fb846b4d1339`; retain this bundle's three-lens fan-out and read-only agent boundaries.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "We're short on time, I'll skip the cost lens and just run security + reliability" | Every admitted review runs all three lenses — a CRITICAL security finding does not excuse missing a HIGH-severity idle-resource waste or an over-provisioned instance. Rejected or incomplete inputs stop before all lens calls. |
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

Separate submitted fresh plan/diff input, existing scoped IaC file sets (including `--scope` paths), and the existing topology-packet input before any lens dispatch. A path alone is not reviewable content; do not infer findings from a filename or attestation.

Always emit one `Scope evidence:` header naming the evidence type, binding target, applied status, and any rejection reason; for mixed input list every eligible and excluded scoped path with its binding status. Attestation does not require raw state, credentials, or an apply-command transcript. Keep forwarded evidence sanitized.

- For each existing scoped set, request a one-time user attestation with `evidence_type=state_backend|apply_record|applied_commit`, `binding_target`, and `applied=yes|no`. `binding_target` is the exact submitted path set or an applied commit SHA attested to include those paths. A general statement that a state backend exists is not path binding.
- Do not query a cloud provider, state backend, or apply system to verify this attestation. Do not require additional repository or revision fields.
- Scoped-only: missing, unbound, or unapplied evidence returns `BLOCKED` with zero reviewer calls. Name the evidence type, target, and rejection reason in `Scope evidence:`.
- Valid binding with absent or truncated IaC content returns `NEEDS_CONTEXT` with zero reviewer calls. Name the missing paths; binding metadata never substitutes for content.
- Mixed input requires a reviewable, complete fresh plan/diff payload and complete content for every validly bound scoped set. Exclude only scoped sets with missing, unbound, or unapplied evidence from every lens, recording each excluded path and binding status in `Scope evidence:` even when another required input is incomplete.
- Missing or truncated fresh payload or eligible scoped content returns `NEEDS_CONTEXT` with zero reviewer calls. Never use an excluded set as fallback, and do not silently drop a validly bound set whose content is incomplete.
- Fresh-only and topology-only requests retain their existing input paths. Require their supplied content before dispatch and use `Scope evidence: N/A — fresh plan/diff only` or `Scope evidence: N/A — topology packet only`, respectively.
- Freeze one eligible input packet and pass the identical fresh-plus-eligible content to all three lenses. For scoped-only, use the complete bound scoped content; for topology-only, use the same supplied topology packet. Lens-specific references may differ, but the eligible surface must not.

**Fan-out return contract**: dispatch the three lenses only after this admission gate passes. Read-only lenses return bounded findings inline; they never create report files. Require Status, Summary, Finding counts, and evidence-linked findings/concerns. The aggregator owns any report file and retains a specialist's options and recommendation in that report. An owner/input/output/status mismatch returns `NEEDS_CONTEXT`; do not treat missing or truncated evidence as a clean review. This read-only return boundary takes precedence over artifact-path examples in the general status reference.

### Step 2: Security lens

Dispatch a Codex worker carrying the `ywc-security-engineer` persona, the frozen eligible input packet from Step 1, and an explicit pointer to `../references/infra/lenses/security.md` and `../references/iac-security.md`. This lens covers: security groups / firewall rules, IAM / RBAC over-permission, public exposure (buckets, endpoints, load balancers), and secrets committed to code or state.

### Step 3: Cost lens

Dispatch a Codex worker carrying the `ywc-performance-engineer` persona, the frozen eligible input packet from Step 1, and an explicit pointer to `../references/infra/lenses/cost.md` and `../references/finops.md`. This lens covers: compute right-sizing against observed/expected utilization, idle or orphaned resources, and pricing model fit (on-demand vs reserved vs spot).

For an escalated FinOps comparison, include exactly one finding's Evidence Snapshot v1 performance lane slice: finding ID and summary, affected resource or workload, evidence source and timestamp, supplied cost/usage metrics, and applicable budget or constraints. Keep the analysis in this caller's report: options, each option's cost/risk trade-off, and a recommended option. This bounded analysis does not replace the shared eligible scope or hand the finding away from the caller.

Missing or truncated required evidence returns `NEEDS_CONTEXT` naming the exact input. Do not estimate missing prices or savings, and do not run a provider lookup, apply, or applied-environment sweep. Keep missing values `unknown`, name the missing evidence and next recheck. Use supplied usage, region, currency, price date/source, and calculation assumptions where relevant; distinguish immediate from commitment savings and name reliability effects. Route a requested environment-wide optimization sweep to `ywc-infra-optimize`.

### Step 4: Reliability lens

Dispatch a Codex worker carrying the `ywc-cloud-engineer` persona in **review mode** — carry the frozen eligible input packet from Step 1 and an explicit instruction that this dispatch is read-only diagnosis: it authors nothing, runs no `terraform apply`, and confines itself to the reliability lens at `../references/infra/lenses/reliability.md`. This lens covers: single points of failure, missing backups / point-in-time recovery, missing resource limits or autoscaling floors, and missing health/readiness checks.

### Step 5: Aggregate severity-rated findings

Collect all three lenses' findings into one report. Deduplicate a finding that two lenses independently flag on the same resource (e.g., a public DB is both a security and a reliability concern — report once, tag both lenses). Rate every finding Critical / High / Medium / Low using each lens reference's severity guidance. Any **CRITICAL or HIGH** finding recommends **blocking** the apply until remediated.

Preserve a required lens's missing-evidence status in the aggregate: a `NEEDS_CONTEXT` result is not a clean lens or a successful full review. Name its exact missing input while retaining other evidence-backed findings and any apply-blocking recommendation. Never let successful lenses mask an owner/input/output/status mismatch.

### Step 6: Recommend `ywc-infra-optimize` for remediation

Unless `--skip-optimize-recommendation` was passed, close the review by recommending the user run `$ywc-infra-optimize` to execute cost/drift remediation, or route reliability/security fixes back through `$ywc-iac-author`. This skill diagnoses; it does not remediate.

## Output Format

```text
Infra Review Report
─────────────────────────────────────────────────
Status:       <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
Scope:        <submitted eligible scope>
Scope evidence: <evidence type, binding target, applied status; eligible/excluded paths and reasons, or the applicable N/A header>
Lenses run:   Security | Cost | Reliability  (all three after admission; zero on rejected/incomplete input)

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

For rejected or incomplete admission, return the status, `Scope evidence:` header, and zero reviewer calls before this completion checklist.

- [ ] All three lenses (security, cost, reliability) were dispatched against the identical scope — none skipped
- [ ] Scoped evidence admission was decided before dispatch; BLOCKED/NEEDS_CONTEXT admission returned zero reviewer calls
- [ ] `Scope evidence:` names each eligible/excluded binding or the fresh-only/topology-only N/A header
- [ ] FinOps comparisons use supplied complete evidence, return bounded options inline, and leave report-file ownership with the aggregator
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
| `../references/infra/lenses/security.md` | Step 2 — security lens dispatch, IaC misconfiguration taxonomy |
| `../references/iac-security.md` | Step 2 — the detailed IaC misconfiguration taxonomy the `ywc-security-engineer` persona reviews against |
| `../references/infra/lenses/cost.md` | Step 3 — cost lens dispatch, right-sizing and waste taxonomy |
| `../references/finops.md` | Step 3 — the detailed FinOps taxonomy (reserved/spot, data-transfer cost) the `ywc-performance-engineer` persona reviews against |
| `../references/infra/lenses/reliability.md` | Step 4 — reliability lens dispatch, SPOF/backup/health taxonomy |
| `../references/infra/providers/aws.md` | Scoped IaC targets AWS — provider-specific misconfiguration/cost/reliability signals |
| `../references/infra/providers/gcp.md` | Scoped IaC targets GCP — provider-specific misconfiguration/cost/reliability signals |
| `../references/infra/providers/azure.md` | Scoped IaC targets Azure — provider-specific misconfiguration/cost/reliability signals |
| `../references/infra/providers/k8s.md` | Scoped IaC includes Kubernetes/Helm (via Terraform providers) |
| `../references/subagent-status-actions.md` | General status actions; the read-only inline fan-out contract above owns this skill's return shape |
