# Dispatch artifact: ywc-infra-design (original body, run 2)

**Key**: claude-code/skills/ywc-infra-design/SKILL.md:36-36
**Scenario**: I need help with the following: designing cloud/infrastructure architecture before any IaC is written — requirements gathering, provider selection, network/compute/storage/IAM topology, and a reliability/cost/security 3-lens pre-check that produces infra-design.md, the input contract ywc-iac-author consumes.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a refusal — a required clarifying-question gate. The user's message names the skill's purpose but supplies none of the Step 1 requirements inputs (workload pattern, traffic/RPS and growth, data volume/classification/retention, compliance/residency, budget ceiling, RTO/RPO) or a provider preference. Per Step 1 ('Do not infer these from the feature description alone — ask the user for anything not already stated') and the Rationalization Defense table's second row, the design pass cannot proceed straight to topology without first eliciting these answers, so before any topology, lens pre-check, or infra-design.md drafting begins, I would pause and ask the user for this requirements set (and whether a provider/cloud account is already decided) rather than assuming defaults.

## Actions
- Announce skill start: 'I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written.'
- Check request for --provider/--scope/--skip-cloud-consult flags — none supplied, so treat provider as undecided and scope as whole architecture
- Step 1: Ask the user explicit clarifying questions for workload pattern, traffic/RPS and growth trajectory, data volume/classification/retention, compliance/residency requirements, monthly budget ceiling, and RTO/RPO — do not infer any of these from the feature description
- Record the user's verbatim answers as the Requirements section draft (held in-memory, later written into infra-design.md)
- Step 2: Since provider is undecided, dispatch Task(subagent_type: ywc-tech-research) with the gathered traffic/data/budget/compliance requirements as comparison criteria for AWS vs GCP vs Azure vs K8s, and record its recommendation as the Provider Decision with 1-3 line rationale
- Step 3: Design topology in order — Network (VPC/VNet, subnet tiers, public/private boundary, ingress/egress), Compute (service shape matched to workload), Storage (DB engine/object storage/cache matched to data profile), IAM (role structure, least-privilege, cross-account/service trust)
- Dispatch Task(subagent_type: ywc-cloud-engineer) in read-only feasibility-consult mode, carrying the topology sketch, with an explicit instruction that it authors nothing and runs no terraform plan/apply — only flags quota limits, provider-specific gotchas, unrealistic network layout
- Read claude-code/skills/ywc-infra-design/references/lenses/reliability.md, .../cost.md, .../security.md
- Read the provider-specific reference matching the Step 2 decision, e.g. claude-code/skills/ywc-infra-design/references/providers/aws.md (or gcp.md/azure.md/k8s.md)
- Step 4: Pre-check the Step 3 topology against each of the three lens taxonomies and record every finding, including explicit 'no issue found' passes
- Step 5: For every material decision (provider choice, single-AZ vs multi-AZ, managed vs self-hosted DB, network exposure boundary, etc.) write an ADR entry with Context / Decision / Alternatives considered / Consequences fields, recorded as each decision is made rather than reconstructed afterward
- Step 6: Write infra-design.md at the project root (or path implied by --scope) using the six-section Output Format: Requirements, Provider Decision, Topology (Network/Compute/Storage/IAM), 3-Lens Pre-Check, ADR Log
- Run the Validation Checklist before declaring the pass complete: requirements gathered explicitly, provider decision declared or delegated (never invented), all four topology dimensions covered, 3-lens pre-check run with every finding recorded, every material trade-off has an ADR entry, infra-design.md written with all sections
- Explicitly stop at infra-design.md — do not write any .tf files or invoke ywc-iac-author in the same pass; hand off infra-design.md as the input contract for a separate ywc-iac-author invocation

## Files touched
- claude-code/skills/ywc-infra-design/SKILL.md (read only — the procedure)
- claude-code/skills/ywc-infra-design/references/lenses/reliability.md (read, Step 4)
- claude-code/skills/ywc-infra-design/references/lenses/cost.md (read, Step 4)
- claude-code/skills/ywc-infra-design/references/lenses/security.md (read, Step 4)
- claude-code/skills/ywc-infra-design/references/providers/aws.md or gcp.md/azure.md/k8s.md (read, whichever matches Step 2's decision)
- infra-design.md (create, at project root or --scope path — the only file this skill writes)

## Gates enforced
- Requirements gathered explicitly via user Q&A, never inferred from the feature description alone (Step 1)
- Provider decision either explicitly declared via --provider/prior decision, or delegated to ywc-tech-research — never invented inline (Step 2, Validation Checklist item 2)
- ywc-cloud-engineer consult constrained to read-only feasibility mode — explicit no-authoring, no terraform plan/apply instruction in the dispatch (Step 3, Common Mistakes)
- 3-lens (reliability/cost/security) pre-check run against the topology with every finding recorded, including 'no issue found' passes (Step 4, Validation Checklist item 4)
- Every material trade-off backed by a four-field ADR entry (Context/Decision/Alternatives/Consequences), recorded at decision time not reconstructed after the fact (Step 5, Validation Checklist item 5)
- infra-design.md written with all required sections so ywc-iac-author's Step 1 can load it without re-asking questions (Step 6, Validation Checklist item 6)
- Hard boundary: no .tf files written and ywc-iac-author not invoked in the same pass — this skill's scope ends at infra-design.md (Common Mistakes, Integration 'Must not be paired with')

## Full narrative

I read claude-code/skills/ywc-infra-design/SKILL.md in full and would follow it exactly as written, in order, without collapsing any step or jumping ahead to IaC.

First, I would announce the skill per its required opening line: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written."

I would check the request for the skill's three flags. None were supplied — no `--provider`, no `--scope`, no `--skip-cloud-consult` — so I would treat the provider as undecided (triggering the Step 2 delegation later), the scope as the whole architecture (not a single named service), and the optional `ywc-cloud-engineer` feasibility consult as still in play in Step 3.

**Step 1 — Requirements gathering (the actual first action).** The user's message states the skill's purpose but supplies none of the six required inputs: workload characteristics (request pattern, sync/batch/event-driven, statefulness), traffic (RPS/concurrency, peak vs steady-state, 6–12 month growth), data (volume, growth, PII/PHI/none classification, retention), regulatory/compliance constraints (residency, GDPR/HIPAA/SOC2/industry mandates), budget (monthly ceiling or per-unit target), and RTO/RPO. The skill's own text is explicit that these must never be inferred from the feature description — "ask the user for anything not already stated, and record the answers verbatim." So my concrete next action would be to stop and ask the user a structured clarifying question covering exactly these six items, plus whether a cloud provider or account is already decided (so I know whether to delegate Step 2 or record it directly). I would not fabricate placeholder numbers to keep moving — the Rationalization Defense table calls out exactly this shortcut ("Requirements gathering is obvious from the feature description, I'll skip to topology") as invalid, since traffic shape, data classification, RTO/RPO, and budget all change concrete topology decisions like multi-AZ vs single-AZ or managed vs self-hosted database.

Once the user answers, I would record those answers verbatim as the draft Requirements section.

**Step 2 — Provider selection.** If the user's answer names an existing account, mandated vendor, or explicit preference, I would record that decision with its rationale and move on. If it is genuinely undecided, I would dispatch `Task(subagent_type: ywc-tech-research)`, feeding it the Step 1 traffic/data/budget/compliance criteria as the comparison basis for AWS vs GCP vs Azure vs K8s, and record its recommendation as the Provider Decision — never inventing that comparison inline myself.

**Step 3 — Topology design.** I would design, strictly in this order: Network (VPC/VNet layout, subnet tiers, public/private boundary, ingress/egress paths), Compute (service shape — managed container, VM, or serverless — matched to the Step 1 workload), Storage (DB engine, object storage, cache layer matched to the Step 1 data profile), and IAM/identity boundaries (role structure, least-privilege, cross-account/cross-service trust). Unless `--skip-cloud-consult` were passed (it was not), I would then dispatch `Task(subagent_type: ywc-cloud-engineer)` in explicit read-only feasibility-consult mode, carrying the topology sketch with an explicit instruction that this dispatch authors nothing and runs no `terraform plan`/`apply` — it only flags quota limits, provider gotchas, or unrealistic network shapes.

**Step 4 — 3-lens pre-check.** I would read `claude-code/skills/ywc-infra-design/references/lenses/reliability.md`, `.../cost.md`, and `.../security.md`, then check the Step 3 topology against each lens's taxonomy, recording every finding — including explicit "no issue found" passes where nothing was flagged — so `ywc-iac-author` and `ywc-infra-review` inherit a documented baseline instead of re-deriving it. I would also read the provider-specific reference matching the Step 2 decision (e.g., `references/providers/aws.md`) to keep the topology realistic for that provider.

**Step 5 — ADR log.** For every material decision from Steps 2–3 (provider choice, single-AZ vs multi-AZ, managed vs self-hosted database, network exposure boundary, etc.), I would write an ADR entry with four fields — Context, Decision, Alternatives considered, Consequences — capturing each one as it is decided rather than reconstructing the list from memory at the end, since reconstruction tends to drop the alternatives that were actually weighed.

**Step 6 — Output.** I would create `infra-design.md` at the project root (or the `--scope`-implied path) using the skill's six-section format: Requirements, Provider Decision, Topology (Network/Compute/Storage/IAM), 3-Lens Pre-Check, and ADR Log — written so that `ywc-iac-author`'s Step 1 can load it directly without re-asking any question this pass already answered.

Before declaring the pass complete I would run the Validation Checklist verbatim: requirements gathered explicitly (not inferred); provider decision either declared or delegated to `ywc-tech-research`, never invented; all four topology dimensions covered; the 3-lens pre-check run with every finding recorded; every material trade-off backed by an ADR entry; and `infra-design.md` written with all sections and ready for `ywc-iac-author` to consume.

Two hard boundaries I would enforce throughout: I would not write or modify any `.tf` file in this same pass — that is explicitly `ywc-iac-author`'s scope, and the skill's Common Mistakes and Integration sections both call out "jumping straight to Terraform" and "pairing with `.tf` authoring" as violations to avoid. And the `ywc-cloud-engineer` dispatch, if it produced any `.tf` output instead of feasibility commentary, would signal that my dispatch instruction was wrong and I would not accept that output as part of the design.

Given all of this, the concrete first move on receiving this request — rather than guessing at a topology — is the Step 1 clarifying question to the user for the six requirements inputs and the provider status, since none of that was included in the request as given.
