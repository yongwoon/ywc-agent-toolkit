# Codex Skill Evaluation Rubric

Score every distributable Codex skill under `codex/skills/*` on
eight dimensions. Each dimension uses `0-4`.

| Level | Meaning |
|---|---|
| 0 | Missing or invalid |
| 1 | Present but materially weak |
| 2 | Adequate operating baseline |
| 3 | Strong and reliable |
| 4 | Exemplary reference quality |

Composite grade: `A >= 3.5`, `B 2.5-3.49`, `C 1.5-2.49`, `D < 1.5`.

| Dim | Weight |
|---|---:|
| S1 Trigger and anti-trigger precision | 0.18 |
| S2 Codex skill schema compliance | 0.14 |
| S3 Progressive disclosure | 0.10 |
| S4 Workflow actionability | 0.17 |
| S5 Output and verification contract | 0.13 |
| S6 Bundle maintainability | 0.10 |
| S7 Codex runtime fit | 0.10 |
| S8 Scope discipline | 0.08 |

## S1: Trigger and Anti-trigger Precision

| Score | Criteria |
|---|---|
| 0 | Missing `description` or pure workflow summary |
| 1 | Vague trigger wording; no anti-trigger; likely sibling collisions |
| 2 | Clear primary use case and at least one anti-trigger |
| 3 | Korean/English/Japanese triggers plus explicit sibling disambiguation |
| 4 | L3 plus realistic user phrasing and complete collision coverage |

Evidence: frontmatter `description`, sibling skill catalog, repeated keywords.

## S2: Codex Skill Schema Compliance

| Score | Criteria |
|---|---|
| 0 | YAML frontmatter invalid or missing `name`/`description` |
| 1 | Extra frontmatter keys or unquoted `: ` risk in `description` |
| 2 | Strict Codex schema passes; minor local convention gaps |
| 3 | Strict schema plus `ywc-skill-author` mandatory body conventions |
| 4 | L3 plus meaningful `agents/openai.yaml` synchronized to current purpose |

Evidence: `inventory_gate.py`, `scripts/validate.sh`, `SKILL.md`, and
`agents/openai.yaml`.

## S3: Progressive Disclosure

| Score | Criteria |
|---|---|
| 0 | Body is bloated and no references are used |
| 1 | Body exceeds 500 lines or large static tables remain inline |
| 2 | Body is acceptable but some lookup material should be extracted |
| 3 | Workflow stays inline; long rubrics/templates live in `references/` |
| 4 | L3 plus references are one level deep and explicitly linked from `SKILL.md` |

Evidence: body line count, reference directory, large static sections.

## S4: Workflow Actionability

| Score | Criteria |
|---|---|
| 0 | Aspirational guidance only |
| 1 | Steps exist but require guessing key inputs or ordering |
| 2 | A competent Codex agent can execute the happy path |
| 3 | Explicit inputs, commands, stop conditions, and failure routing |
| 4 | L3 plus domain-specific Rationalization Defense and common mistakes |

Evidence: workflow section, arguments table, validation checklist.

## S5: Output and Verification Contract

| Score | Criteria |
|---|---|
| 0 | No expected output is defined |
| 1 | Output described only in prose |
| 2 | Output sections are named |
| 3 | Concrete report/template plus verification criteria |
| 4 | L3 plus eval fixtures or deterministic scripts proving expected output |

Evidence: output format, validation section, `evals/`, scripts.

## S6: Bundle Maintainability

| Score | Criteria |
|---|---|
| 0 | Missing required README locale set or broken references |
| 1 | Locale docs or UI metadata are materially stale |
| 2 | README locale set exists; minor drift or weak default prompt |
| 3 | README set, `agents/openai.yaml`, and cross-links are aligned |
| 4 | L3 plus ownership, changelog/version impact, and install behavior are clear |

Evidence: README files, `agents/openai.yaml`, bundle README, `CHANGELOG.md`, and
`VERSION` when the skill changed meaningfully.

## S7: Codex Runtime Fit

| Score | Criteria |
|---|---|
| 0 | Uses Claude Code-only syntax as required execution path |
| 1 | Contains confusing Claude paths, model names, or `Task(subagent_type=...)` examples |
| 2 | Mostly Codex-compatible, with small ambiguous references |
| 3 | Uses Codex terminology, Codex custom-agent TOML, and installed skill paths |
| 4 | L3 plus graceful fallback when Codex subagent/custom-agent dispatch is unavailable |

Evidence: grep for Claude-only terms, installed path examples, agent dispatch prose.

## S8: Scope Discipline

| Score | Criteria |
|---|---|
| 0 | Performs several unrelated jobs |
| 1 | Leaks into adjacent sibling skill responsibilities |
| 2 | Primary responsibility is clear |
| 3 | Clean boundaries and downstream handoff are documented |
| 4 | L3 plus integrations compose without circular ownership |

Evidence: description anti-triggers, integration section, sibling overlap.
