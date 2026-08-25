# Dispatch artifact: ywc-infra-design (deleted body, run 1)

**Key**: claude-code/skills/ywc-infra-design/SKILL.md:36-36
**Scenario**: I need help with the following: designing cloud/infrastructure architecture before any IaC is written — requirements gathering, provider selection, network/compute/storage/IAM topology, and a reliability/cost/security 3-lens pre-check that produces infra-design.md, the input contract ywc-iac-author consumes.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Step 1 of the procedure requires gathering workload, traffic, data, compliance, budget, and RTO/RPO requirements explicitly and forbids inferring them from the feature description alone. The user's request describes the desired process (mirroring the skill's own description) but supplies none of these concrete inputs, so before any provider selection or topology work could begin I would stop and ask the user for them rather than proceeding on assumptions.

## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-infra-design-36-36.md (the ywc-infra-design skill definition) in full
- Announce skill start verbatim per the skill's Announce-at-start line
- Pause at Step 1 and ask the user explicit clarifying questions covering workload characteristics, traffic, data classification/retention, compliance, budget, and RTO/RPO, plus scope and whether the provider is already decided, since none of these were stated in the request
- (after answers are supplied) Record the answers verbatim as the Requirements section
- If provider is undecided, invoke Skill tool with skill=ywc-tech-research, passing traffic/data/budget/compliance as comparison criteria for AWS vs GCP vs Azure vs K8s, and record its recommendation plus rationale as the Provider Decision
- If provider is already decided (flag or prior statement), record the decision and rationale directly and skip the ywc-tech-research delegation
- Design topology in fixed order: Network (VPC/subnet tiers, public/private boundary, ingress/egress), Compute (service shape matched to workload), Storage (DB engine, object storage, cache matched to data profile), IAM/identity boundaries (role structure, least privilege, cross-account/service trust)
- Unless --skip-cloud-consult, dispatch Task(subagent_type: ywc-cloud-engineer) in explicit read-only feasibility-consult mode, carrying the topology sketch and an instruction that the dispatch authors nothing and runs no terraform plan/apply
- Read references/lenses/reliability.md, references/lenses/cost.md, and references/lenses/security.md (relative to the skill directory)
- Read the matching provider reference file (e.g. references/providers/aws.md) once the provider is decided, to ground topology choices
- Pre-check the Step 3 topology against each of the three lenses' taxonomies and record every finding, including explicit 'no issue found' passes
- Write an ADR entry (Context / Decision / Alternatives considered / Consequences) for every material decision from Steps 2-3 as each is decided, not reconstructed afterward
- Write infra-design.md at the project root (or the --scope path) using the exact Output Format template with all five sections: Requirements, Provider Decision, Topology, 3-Lens Pre-Check, ADR Log
- Run the Validation Checklist before declaring the design pass complete (requirements gathered explicitly, provider decision sourced not invented, all four topology dimensions covered, all three lenses recorded, every trade-off has an ADR entry, infra-design.md has all sections)
- Explicitly refrain from creating or modifying any .tf files in this same pass, per the skill's hard boundary with ywc-iac-author

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-infra-design-36-36.md (read only)
- infra-design.md (would be created at project root or --scope path)
- claude-code/skills/ywc-infra-design/references/lenses/reliability.md (would be read)
- claude-code/skills/ywc-infra-design/references/lenses/cost.md (would be read)
- claude-code/skills/ywc-infra-design/references/lenses/security.md (would be read)
- claude-code/skills/ywc-infra-design/references/providers/<provider>.md (would be read, provider-dependent)

## Gates enforced
- Step 1 requirements-gathering gate: do not infer workload/traffic/data/compliance/budget/RTO-RPO from the feature description alone; ask the user and record answers verbatim
- Step 2 provider-decision gate: never invent the AWS/GCP/Azure/K8s comparison inline — delegate to ywc-tech-research unless the provider is already explicitly decided
- Step 4 3-lens pre-check gate: every lens finding, including 'no issue found', must be recorded rather than skipped because the topology 'looks fine'
- Step 5 ADR gate: every material trade-off from Steps 2-3 needs a Context/Decision/Alternatives/Consequences entry, recorded at decision time not reconstructed later
- Scope boundary gate: this skill never authors or edits .tf files — that is ywc-iac-author's separate pass
- Validation Checklist gate before declaring the design pass complete

## Full narrative

I would start by announcing, verbatim as the skill instructs: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written."

Then I would immediately hit the Step 1 gate. The request as given describes the *kind* of work wanted (requirements gathering, provider selection, topology, 3-lens pre-check, infra-design.md) but contains none of the actual inputs Step 1 requires — no workload pattern, no traffic figures, no data classification, no compliance framework, no budget ceiling, no RTO/RPO. The skill is explicit that these must not be inferred from the feature description alone, so my first concrete action would be to ask the user directly:

1. Workload characteristics — is this read-heavy, write-heavy, or mixed; synchronous, batch, or event-driven; stateful or stateless?
2. Traffic — expected concurrency/RPS, peak vs. steady-state, and growth trajectory over the next 6–12 months?
3. Data — volume, growth rate, classification (PII/PHI/none), and retention requirements?
4. Regulatory/compliance — any data residency constraints, and applicable frameworks (GDPR, HIPAA, SOC 2, industry-specific)?
5. Budget — a monthly ceiling or a per-unit cost target?
6. RTO/RPO — acceptable downtime window and acceptable data-loss window?
7. Scope — is this for the whole architecture or a single service (i.e., should I apply `--scope <system-name>`)?
8. Provider — is AWS/GCP/Azure/K8s already decided (existing account, mandated vendor), or genuinely open?

I would not proceed past this point without those answers, since every downstream step depends on them as evidence.

Once the user supplied that information, here is exactly how I would carry the rest of the procedure through, concretely:

**Step 1 (finalize):** Record every answer verbatim — not paraphrased — since `ywc-iac-author`'s Step 1 will load this file directly and should not need to re-ask anything.

**Step 2 (provider selection):** If the user's answer indicates the provider is genuinely undecided, I would invoke the `ywc-tech-research` skill (via the Skill tool), feeding it the traffic, data, budget, and compliance answers from Step 1 as the comparison criteria for an AWS vs. GCP vs. Azure vs. K8s comparison, and record its returned recommendation and rationale as the Provider Decision. If the user instead states a provider is already decided (existing account, mandated vendor, or passes `--provider aws` equivalent), I would record that decision and its rationale directly and skip the delegation — this is the one legitimate shortcut the skill allows, and only under that condition.

**Step 3 (topology design), in the fixed order specified:**
- Network: VPC/VNet layout, subnet tiers, public/private boundary, ingress/egress paths.
- Compute: service shape (managed container, VM, or FaaS) matched to the Step 1 workload characteristics.
- Storage: database engine, object storage, and cache layer matched to the Step 1 data profile.
- IAM/identity boundaries: role structure, least-privilege boundaries, cross-account/cross-service trust relationships.

Unless the user passed `--skip-cloud-consult`, I would then dispatch `Task(subagent_type: ywc-cloud-engineer)` in explicit read-only feasibility-consult mode, carrying the topology sketch and an unambiguous instruction that this dispatch authors nothing and must not run `terraform plan`/`apply` — its only job is to flag feasibility concerns such as quota limits, provider-specific gotchas, or an unrealistic network layout before the design is finalized.

**Step 4 (3-lens pre-check):** I would read the three referenced lens files exactly as pointed to by the skill — `references/lenses/reliability.md`, `references/lenses/cost.md`, and `references/lenses/security.md` (relative to the skill directory) — and, once the provider is known, the matching provider reference (e.g., `references/providers/aws.md`) to ground the topology choices in realistic constraints. I would then pre-check the Step 3 topology against each lens's taxonomy and record every finding, explicitly including "no issue found" where a lens raises nothing, since the skill treats a silent pass as an unrecorded gap that `ywc-iac-author` and `ywc-infra-review` would otherwise have to re-derive.

**Step 5 (ADR log):** For every material decision surfaced in Steps 2–3 — provider choice, single-AZ vs. multi-AZ, managed vs. self-hosted database, network exposure boundary, and any similar structural call — I would write an ADR entry with four fields: Context, Decision, Alternatives considered, Consequences. I would write each entry as the decision is made rather than reconstructing the set at the end, since reconstruction tends to drop the alternatives that were actually weighed.

**Step 6 (output):** I would write `infra-design.md` at the project root (or the path implied by `--scope`, if the user restricted scope to a single service) using the exact Output Format template from the skill: `## Requirements`, `## Provider Decision`, `## Topology` (with Network/Compute/Storage/IAM subsections), `## 3-Lens Pre-Check`, and `## ADR Log`.

**Before declaring the pass complete**, I would walk the Validation Checklist item by item: requirements gathered explicitly rather than inferred; the provider decision either explicitly declared or delegated to `ywc-tech-research`, never invented inline; topology covering all four dimensions; the 3-lens pre-check run with every finding recorded; every material trade-off backed by an ADR entry; and `infra-design.md` written with all five sections in a state `ywc-iac-author` could load directly without re-asking anything.

Throughout, I would not create or touch any `.tf` files, and I would not treat the `ywc-cloud-engineer` consult as an authoring step — both are explicit boundary violations the skill calls out (jumping to Terraform in the same pass, or letting the feasibility consult produce IaC). Writing Terraform itself is `ywc-iac-author`'s separate scope, to be invoked by the user afterward as its own pass once `infra-design.md` exists as a reviewable checkpoint.
