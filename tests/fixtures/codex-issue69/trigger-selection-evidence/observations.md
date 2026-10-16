# Observed Codex skill selections — FR-8 / AC-9

Evidence kind: **observed live selection**, separate from predetermined JSON fixtures.

- Source revision: `0c164f105184f78d4c8579e660b31b878f7cc9ed`.
- Runtime: `codex-cli 0.163.0`; six fresh ephemeral native `codex exec` sessions, user config ignored, read-only sandbox, isolated working directory.
- Catalog: all **51** repository `ywc-*` skills installed through `scripts/install.sh --codex --skip-agents` into a temporary Codex home. Installed SKILL.md bytes matched this source revision. No real user skill folders changed.
- Catalog identity SHA-256: `2545bfba99b09f4f1f46232ed4898c0c1a13ab4eb6921493e4b542db6306ef1c` over sorted relative SKILL.md paths + NUL + file bytes + NUL.
- Protocol: select the single best installed skill for the exact request below; return only its name and stop before invocation, tools, implementation, audit or publishing. Expected selections were kept in the parent recorder and were not supplied to Codex.
- Each CLI exit was 0. Event inspection found only reasoning/agent-message items and **zero tool calls/file changes**. These observations establish bounded selection only, not execution of the selected workflows. Full transcripts and credentials are not retained here.

| Trial | Exact prompt | Actual selected skill | Expected skill | Observed UTC | Result |
|---|---|---|---|---|---|
| T1 | Compare implementation libraries and their technical trade-offs before writing a spec. | `ywc-tech-research` | `ywc-tech-research` | 2026-10-16T04:03:40.147878+00:00 | MATCH; zero tools |
| T2 | Assess whether this feature is worth building for the business, including user value and ROI. | `ywc-product-review` | `ywc-product-review` | 2026-10-16T04:03:48.265525+00:00 | MATCH; zero tools |
| T3 | Threat-model this existing authenticated file-upload implementation and its trust boundaries. | `ywc-security-audit` | `ywc-security-audit` | 2026-10-16T04:03:56.325677+00:00 | MATCH; zero tools |
| T4 | Review the product's adoption and monetization risks. | `ywc-product-review` | `ywc-product-review` | 2026-10-16T04:04:03.252928+00:00 | MATCH; zero tools |
| T5 | Check whether this completed implementation conforms to its approved specification. | `ywc-impl-review` | `ywc-impl-review` | 2026-10-16T04:04:10.475017+00:00 | MATCH; zero tools |
| T6 | Generate Backend, Frontend, and QA layers in parallel from this approved specification. | `ywc-code-gen` | `ywc-code-gen` | 2026-10-16T04:04:18.746091+00:00 | MATCH; zero tools |

All six mandatory selections matched at the same changed source/catalog revision. Source-only SDK/monitoring scenarios remain source assertions; no live SDK execution or optional dedicated monitoring cost experiment is claimed.
