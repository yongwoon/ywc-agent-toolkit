# ywc-plan

A pre-implementation planning Skill that converts a rough idea into one of two ready-to-execute artifacts: a Small-path direct execution plan, or a Medium/Large-path spec document. Automatically assesses scale and routes to the right downstream Skill.

## Use Cases

- When the user says "Make a plan for this feature"
- When there is no Spec or task yet and the user does not know where to start
- When it is unclear whether the change is a Small one-shot edit or warrants a full Spec
- When preparing the input Spec that `ywc-task-generator` will consume

## Usage

```bash
/ywc-plan "<rough request>"
```

Or invoke naturally:

> "I want to add notification preferences to the profile page — make a plan."

## Input

- A natural-language change request (rough idea, feature request, change description)

## Output

Depending on scale, one of:

| Scale | Output |
|---|---|
| Small | `./plan.md` — a directly-executable single-PR plan |
| Medium / Large | `docs/ywc-plans/<slug>.md` — a Spec document that `ywc-spec-validate` and `ywc-task-generator` will consume |

Each path emits an explicit handoff message naming the next Skill.

## Flow

1. **Clarify** — Ask the user once for the four anchors: What / Why / Out of Scope / Done When
2. **Investigate** — Read only the essential files: `AGENTS.md` / `CODEX.md` / `CLAUDE.md`, `package.json`, `docs/architecture/`, etc.
3. **Assess Scale** — Pick exactly one of Small / Medium / Large (default to Medium when ambiguous)
4. **Branch** — Small writes `plan.md`; Medium/Large writes a Spec document
5. **Handoff** — Print the next-step Skill explicitly (execution is the user's decision, not this Skill's)

## Safety Invariants

Any of the following auto-escalates to Medium scale or higher:

- Database migration / schema change
- New library / framework introduction
- New API contract exposed to external consumers
- Authentication / authorization logic touched
- Cross-cutting change across 2+ modules

## Related Skills

- `ywc-tech-research` — Run before `ywc-plan` when technology choice is unsettled
- `ywc-product-review` — Run before `ywc-plan` when product/business framing is unclear
- `ywc-spec-validate` — Next step on the Medium/Large path
- `ywc-task-generator` — Decomposes the Spec into tasks after review passes
- `ywc-code-gen` — Direct execution option for the Small path
- `ywc-sequential-executor` / `ywc-parallel-executor` — Execute the generated tasks

## Triggering

Trigger conditions are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [Korean (default)](./README.md)
- [Japanese](./README.ja.md)
