# Dispatch artifact: ywc-infra-design (original body, run 1)

**Key**: claude-code/skills/ywc-infra-design/SKILL.md:36-36
**Scenario**: I need help with the following: designing cloud/infrastructure architecture before any IaC is written — requirements gathering, provider selection, network/compute/storage/IAM topology, and a reliability/cost/security 3-lens pre-check that produces infra-design.md, the input contract ywc-iac-author consumes.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Step 1 of the procedure explicitly forbids inferring workload/traffic/data/compliance/budget/RTO-RPO requirements from the feature description alone and requires asking the user for anything not already stated. The user's request only restates the skill's purpose (design cloud/infra architecture, gather requirements, select a provider, design topology, run the 3-lens pre-check) without supplying any of the six required requirement fields or a concrete system/service to design, and none of --provider/--scope/--skip-cloud-consult were supplied. So before any topology or provider decision, I would pause and ask the user for the missing requirements rather than fabricating them.

## Actions
- Read claude-code/skills/ywc-infra-design/SKILL.md as the sole procedure
- Announce skill start verbatim
- Check --provider/--scope/--skip-cloud-consult flags (none supplied)
- Step 1: ask user clarifying questions for workload, traffic, data classification, compliance, budget, RTO/RPO instead of inferring them
- Step 2: if provider undecided, dispatch /ywc-tech-research with requirements as comparison criteria; otherwise record provider + rationale
- Step 3: design network/compute/storage/IAM topology in that order
- Step 3: optionally dispatch Task(subagent_type: ywc-cloud-engineer) in read-only feasibility-consult mode
- Read references/lenses/reliability.md, references/lenses/cost.md, references/lenses/security.md
- Step 4: pre-check topology against all three lenses, recording every finding including 'no issue found'
- Read references/providers/<provider>.md for the selected provider
- Step 5: write ADR entries (Context/Decision/Alternatives/Consequences) for every material trade-off as each is decided
- Step 6: Write infra-design.md at project root (or --scope path) using the Output Format template
- Run Validation Checklist before declaring the design pass complete
- Refuse to write any .tf files or invoke ywc-iac-author in the same pass

## Files touched
- claude-code/skills/ywc-infra-design/SKILL.md (read)
- claude-code/skills/ywc-infra-design/../references/lenses/reliability.md (read)
- claude-code/skills/ywc-infra-design/../references/lenses/cost.md (read)
- claude-code/skills/ywc-infra-design/../references/lenses/security.md (read)
- claude-code/skills/ywc-infra-design/../references/providers/<provider>.md (read, provider-specific)
- infra-design.md (create, project root or --scope path)

## Gates enforced
- Step 1 requirements-not-inferred gate (Validation Checklist item 1)
- Step 2 provider-decision gate: explicit declaration or ywc-tech-research delegation, never invented inline (Validation Checklist item 2)
- Step 3 topology completeness gate: all four dimensions covered (Validation Checklist item 3)
- Step 4 3-lens pre-check completeness gate, including recorded 'no issue found' passes (Validation Checklist item 4)
- Step 5 ADR completeness gate: every material trade-off has Context/Decision/Alternatives/Consequences (Validation Checklist item 5)
- Step 6 output-completeness gate: infra-design.md has all sections and is ready for ywc-iac-author (Validation Checklist item 6)
- Scope boundary gate: never write .tf files or otherwise begin IaC authoring in this pass
- Cloud-engineer consult read-only gate: dispatch must not produce .tf files or run terraform plan/apply

## Full narrative

Here is exactly how I would carry this out under the ywc-infra-design procedure.

First, I would announce the skill exactly as instructed: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written." I would then check the invocation for the three supported flags — `--provider`, `--scope`, `--skip-cloud-consult` — none of which were supplied in this request, so I proceed with the full default workflow (provider comparison in play, whole-architecture scope, cloud-engineer consult available).

**Step 1 — Requirements gathering.** The skill is explicit that I must not infer workload, traffic, data, compliance, budget, or RTO/RPO from the feature description alone — I must ask the user for anything not already stated and record the answers verbatim into the eventual `infra-design.md`. The request as given only restates the skill's own scope (provider selection, network/compute/storage/IAM topology, 3-lens pre-check) — it does not name a concrete system, expected traffic, data sensitivity, compliance regime, budget ceiling, or RTO/RPO targets. Per the Rationalization Defense table's second row ("Requirements gathering is obvious from the feature description, I'll skip to topology" — rejected, because these answers change the topology outcome: multi-AZ vs single-AZ, managed vs self-hosted DB, hot-standby vs backup-only), I would not proceed to topology work on assumed values. So my first concrete action is to ask the user directly for:
- Workload characteristics (read-heavy/write-heavy/mixed, sync/batch/event-driven, stateful or not)
- Expected traffic (RPS/concurrency, peak vs steady-state, 6–12 month growth trajectory)
- Data profile (volume, growth rate, classification — PII/PHI/none, retention requirements)
- Regulatory/compliance constraints (data residency, GDPR/HIPAA/SOC 2/industry mandates)
- Monthly budget ceiling or per-unit cost target
- RTO/RPO (acceptable downtime window and acceptable data-loss window)
- Which system/service this design pass targets (i.e., whether a `--scope` value applies)
- Whether the cloud provider is already decided (existing account, mandated vendor) or should be compared

Only once these are answered would I move forward — this is the point in the procedure where I would stop and ask rather than proceed on assumptions.

**Step 2 — Provider selection (once requirements are known).** If the user states the provider is already decided (existing account, mandated vendor, or supplies `--provider aws|gcp|azure|k8s`), I record that decision plus a 1–3 line rationale and move on. If genuinely undecided, I would not invent a provider comparison myself — I would delegate to `/ywc-tech-research`, feeding it the Step 1 answers (traffic, data, budget, compliance) as explicit comparison criteria, and record its recommendation verbatim as the Provider Decision.

**Step 3 — Topology design.** In strict order: Network (VPC/VNet layout, subnet tiers, public/private boundary, ingress/egress paths), Compute (managed container / VM / serverless matched to the Step 1 workload shape), Storage (DB engine, object storage, cache layer matched to the Step 1 data profile), and IAM/identity boundaries (role structure, least-privilege boundaries, cross-account/cross-service trust). While drafting this I would consult the relevant provider reference file — e.g. `claude-code/skills/references/providers/aws.md` if AWS was selected — to ground the topology in realistic, provider-specific choices rather than generic patterns. Unless `--skip-cloud-consult` were passed, I would then dispatch `Task(subagent_type: ywc-cloud-engineer)` in explicit read-only feasibility-consult mode, carrying the topology sketch with an explicit instruction that this dispatch authors nothing and must not run `terraform plan`/`terraform apply` — its only job is to flag feasibility concerns (quota limits, provider-specific gotchas, unrealistic network layout) before the design is finalized. If that subagent's output included any `.tf` content or an apply/plan attempt, per Common Mistakes I would treat that as a broken dispatch instruction and discard the IaC output, keeping only the feasibility feedback.

**Step 4 — Reliability/cost/security 3-lens pre-check.** I would read the three lens reference files — `claude-code/skills/references/lenses/reliability.md`, `.../cost.md`, and `.../security.md` — and check the Step 3 topology against each lens's taxonomy (e.g., public subnet exposure for a database tier, missing backup/multi-AZ strategy, wildcard IAM policies). I would record every finding for every lens, explicitly writing "no issue found" where a lens turns up nothing, since the skill requires that a clean pass be documented rather than silently omitted — this is what lets `ywc-iac-author` and `ywc-infra-review` inherit a documented baseline instead of re-deriving it.

**Step 5 — ADR log.** For every material decision surfaced in Steps 2–3 (provider choice, single-AZ vs multi-AZ, managed vs self-hosted database, network exposure boundary, and any other trade-off with real alternatives), I would write an ADR entry with four fields — Context, Decision, Alternatives considered, Consequences — as each decision is made, not reconstructed afterward from memory (Common Mistakes warns reconstruction drops the alternatives actually considered).

**Step 6 — Output.** I would then create `infra-design.md` at the project root (or the path implied by a supplied `--scope`) using the exact Output Format template from the skill: `## Requirements`, `## Provider Decision`, `## Topology` (Network/Compute/Storage/IAM subsections), `## 3-Lens Pre-Check`, and `## ADR Log`. I would write this via the Write tool, and I would phrase every section so `ywc-iac-author`'s Step 1 can load it directly without re-asking any question already answered here.

**Validation before declaring done.** Before calling the pass complete I would walk the Validation Checklist explicitly: requirements gathered (not inferred), provider decision explicit or delegated, all four topology dimensions covered, all three lenses checked and recorded (including clean passes), every material trade-off has an ADR entry, and `infra-design.md` contains all sections and is ready for `ywc-iac-author`.

**What I would explicitly refuse to do.** I would not write, sketch, or start any `.tf`/Terraform module in this same pass — that is `ywc-iac-author`'s scope per the skill's own boundary statement and the "Must not be paired with" integration note. I would not invoke `ywc-iac-author` myself as a continuation of this pass; the design output is the handoff artifact, and starting IaC authoring here would collapse the reviewable checkpoint the two-skill split exists to preserve. I also would not let the `ywc-cloud-engineer` consult (if dispatched) produce or apply any infrastructure — it is feasibility-only.

Given all of the above, the actual first move on this specific request — since no concrete requirements were supplied — is to pause and ask the user for the Step 1 requirement fields (workload, traffic, data classification, compliance, budget, RTO/RPO) and the target system/scope, rather than fabricate a topology on an unstated feature description.
