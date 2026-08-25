# Dispatch artifact: ywc-infra-design (deleted body, run 2)

**Key**: claude-code/skills/ywc-infra-design/SKILL.md:36-36
**Scenario**: I need help with the following: designing cloud/infrastructure architecture before any IaC is written — requirements gathering, provider selection, network/compute/storage/IAM topology, and a reliability/cost/security 3-lens pre-check that produces infra-design.md, the input contract ywc-iac-author consumes.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Step 1 of the procedure explicitly states requirements (workload, traffic, data, compliance, budget, RTO/RPO) must not be inferred from the feature description alone -- they must be asked of the user and recorded verbatim. The user's request describes the skill's overall purpose but supplies none of these six data points, so before doing any provider selection or topology work I would stop and ask clarifying questions rather than fabricate requirements, consistent with the Rationalization Defense table's rejection of skipping evidence-gathering.

## Actions
- Announce skill start per the skill's required announcement line
- Step 1: ask the user explicit clarifying questions for the six requirement categories (workload, traffic, data, compliance, budget, RTO/RPO) rather than inferring them from the request
- Pause further steps until requirements are answered, per Step 1's 'do not infer' instruction and Validation Checklist item 1
- (Once answered) Step 2: check for --provider flag or an already-decided provider; if genuinely undecided, invoke the ywc-tech-research skill, feeding it traffic/data/budget/compliance as comparison criteria, and record its recommendation as the Provider Decision
- (Once provider known) Step 3: draft Network / Compute / Storage / IAM topology sections in that order, matched to Step 1 answers
- (Once topology sketched) Optionally dispatch Task(subagent_type: ywc-cloud-engineer) in read-only feasibility-consult mode with explicit no-authoring, no-terraform-apply/plan instructions, unless --skip-cloud-consult is set
- Step 4: Read references/lenses/reliability.md, references/lenses/cost.md, references/lenses/security.md (and the matching references/providers/<provider>.md) and pre-check the topology against each taxonomy, recording every finding including 'no issue found'
- Step 5: write an ADR entry (Context/Decision/Alternatives considered/Consequences) for each material decision as it is made -- provider choice, AZ strategy, managed vs self-hosted DB, network exposure boundary, etc.
- Step 6: Write infra-design.md at the project root (or --scope path) using the exact Output Format template with all five sections
- Run the six-item Validation Checklist before declaring the design pass complete
- Explicitly do not write, edit, or plan/apply any .tf files in this pass -- hand off infra-design.md to ywc-iac-author as a separate downstream pass

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-infra-design-36-36.md (read only, procedure source)
- infra-design.md (would be created at project root or --scope path in Step 6, not created in this closed-book narration)
- claude-code/skills/ywc-infra-design/references/lenses/reliability.md (would Read in Step 4)
- claude-code/skills/ywc-infra-design/references/lenses/cost.md (would Read in Step 4)
- claude-code/skills/ywc-infra-design/references/lenses/security.md (would Read in Step 4)
- claude-code/skills/ywc-infra-design/references/providers/<chosen-provider>.md (would Read in Step 4, provider-dependent)

## Gates enforced
- Step 1 requirements-must-be-explicit gate (do not infer workload/traffic/data/compliance/budget/RTO-RPO from the feature description)
- Step 2 provider-decision gate (declare or delegate to ywc-tech-research, never invent inline)
- Step 3 topology completeness gate (all four dimensions: network, compute, storage, IAM)
- Step 4 3-lens pre-check gate (reliability/cost/security, every finding recorded including 'no issue found')
- Step 5 ADR-per-material-decision gate
- Step 6 infra-design.md five-section completeness gate
- Validation Checklist (6 items) before declaring the design pass complete
- Skill boundary gate: never write/modify .tf files in this pass (that is ywc-iac-author's scope)
- Cloud-engineer consult must stay read-only feasibility-only, never authoring

## Full narrative

Understood -- this falls squarely inside the infra-design workflow. I would open by announcing: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written," then work the six-step workflow in order, without touching any Terraform.

**Step 1 -- Requirements gathering (blocking gate, would ask before proceeding).** The workflow is explicit that these must be gathered, not inferred from the feature description. Since the request as given states none of them, my concrete next action would be to ask the user directly:
- Workload characteristics: is this read-heavy, write-heavy, or mixed? Synchronous request/response, batch, or event-driven? Any stateful components?
- Traffic: expected concurrency/RPS at peak and steady-state, and the growth trajectory over the next 6-12 months?
- Data: volume today, growth rate, classification (PII/PHI/none), and retention requirements?
- Regulatory/compliance: data residency constraints, and any applicable frameworks (GDPR, HIPAA, SOC 2, industry-specific)?
- Budget: a monthly ceiling or a per-unit cost target?
- RTO/RPO: acceptable downtime window and acceptable data-loss window?

I would record the answers verbatim, since infra-design.md's Requirements section is meant to be quoted evidence, not a paraphrase, and because ywc-iac-author's Step 1 loads this file expecting it to already answer these questions without re-asking.

**Step 2 -- Provider selection (once requirements are in hand).** I would check whether the user passed `--provider` or otherwise already has a decided provider (existing account, mandated vendor, explicit statement). If so, I'd record that decision and its rationale directly. If genuinely undecided, I would not invent a comparison myself -- I would invoke the `ywc-tech-research` skill, handing it the traffic, data, budget, and compliance answers from Step 1 as the comparison criteria for AWS vs GCP vs Azure vs K8s, and record its recommendation as the Provider Decision with a 1-3 line rationale.

**Step 3 -- Topology design.** In order: Network (VPC/VNet layout, subnet tiers, public/private boundary, ingress/egress paths), Compute (managed container vs VM vs serverless/FaaS, matched to the Step 1 workload shape), Storage (DB engine, object storage, cache layer matched to the data profile), and IAM/identity boundaries (role structure, least-privilege boundaries, cross-account/cross-service trust). Unless `--skip-cloud-consult` was passed, I would then dispatch `Task(subagent_type: ywc-cloud-engineer)` in explicit read-only feasibility-consult mode, carrying the topology sketch with an explicit instruction that this dispatch authors nothing and runs no `terraform plan`/`apply` -- it only flags quota limits, provider-specific gotchas, or an unrealistic network layout.

**Step 4 -- 3-lens pre-check.** I would Read `references/lenses/reliability.md`, `references/lenses/cost.md`, and `references/lenses/security.md` from the skill's reference directory (and the matching `references/providers/<provider>.md` for provider-specific realism), then walk the Step 3 topology against each taxonomy, recording every finding -- including an explicit "no issue found" where nothing surfaces -- so downstream `ywc-iac-author` and `ywc-infra-review` inherit a documented baseline instead of re-deriving one.

**Step 5 -- ADR log.** For every material decision from Steps 2-3 (provider choice, single-AZ vs multi-AZ, managed vs self-hosted database, network exposure boundary, etc.) I would write an ADR entry with Context, Decision, Alternatives considered, and Consequences fields, recording each one as it is decided rather than reconstructing the list from memory at the end.

**Step 6 -- Output.** I would Write `infra-design.md` at the project root (or the `--scope` path if a single system was targeted) using the exact template: Requirements, Provider Decision, Topology (Network/Compute/Storage/IAM), 3-Lens Pre-Check, and ADR Log.

**Validation before declaring done:** I would run the six-item checklist -- requirements gathered explicitly, provider decision declared or delegated (never invented), all four topology dimensions covered, all three lenses run with every finding recorded, every material trade-off backed by an ADR entry, and infra-design.md written with all five sections ready for `ywc-iac-author` to load directly.

**Explicit boundary I would hold:** at no point in this pass would I create, edit, or plan/apply any `.tf` file -- per the skill's Common Mistakes and Integration sections, that is `ywc-iac-author`'s job in a separate, later pass that consumes the finished `infra-design.md`. I would also keep the `ywc-cloud-engineer` consult strictly read-only feasibility feedback, not authoring.

Given that the request itself supplies none of the Step 1 data points, my actual first concrete action -- rather than fabricating traffic numbers, data classification, or a budget -- would be to ask the user the six requirements questions above and wait for answers before moving to provider selection or topology.
