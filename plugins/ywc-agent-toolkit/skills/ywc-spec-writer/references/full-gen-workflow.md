# Full Generation Workflow

Used when `--full` or `--update` flag is set. Requires user confirmation before starting.

## Pre-condition Check

Before any LLM call, verify:
- User has confirmed the operation ("yes" to the confirmation prompt)
- `docs/specification/` directory is initialized (run `init-spec-structure.sh` if not)
- Language is set (`--lang` or default `ko`)

## Model Selection

Use the most capable available Codex reasoning model. Do not use a low-reasoning pass for full spec generation — full codebase analysis requires frontier reasoning.

## Analysis Steps

### 1. Project Identity
Read: `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, `README.md` (repo root; read whichever project guidance files exist)
Extract: project name, purpose, target users, tech stack summary, language policy

### 2. Feature Inventory
Read: `docs/ywc-plans/` (all files), `docs/specification/02-features.md` (if exists)
Extract: list of features already planned or specified

### 3. Data Model Discovery
Scan for: `prisma/schema.prisma`, `*/migrations/*.sql`, `*/models/`, `*/entities/`
Extract: entity names and relationships — translate to plain language; do NOT copy schema syntax

### 4. Interface Discovery
Scan for: `*/routes/`, `*/api/`, `openapi*.yml`, `swagger*.json`
Extract: external-facing integrations — describe purpose and data direction, not implementation

### 5. User Flow Discovery
Scan for: `*/pages/`, `*/views/`, `*/screens/`, `*/components/`
Extract: top-level page/screen names → infer user flows from naming and directory structure

### 6. Non-Functional Requirements
Read: `AGENTS.md`, `CODEX.md`, `CLAUDE.md` (NFR mentions), `docs/architecture/` (if exists)
Extract: explicit or implied constraints on performance, security, availability, compliance

## Writing Order

Generate sections in this order so each section can inform the next:

1. `07-glossary.md` — establish vocabulary first
2. `01-overview.md` — frame scope and stakeholders
3. `03-data.md` — define entities before features reference them
4. `02-features.md` — user stories reference entities from step 3
5. `04-interfaces.md` — external interfaces often correspond to features
6. `05-user-flows.md` — flows connect features and UI
7. `06-requirements.md` — NFRs informed by all prior sections

## Token Efficiency

- Read only the files listed in each Analysis Step; do not perform open-ended codebase exploration
- For large schema files, read entity/table definitions in full; migration history may be skipped
- For large route files, read the route index or top-level exports
- In `--update` mode, read each existing section first and patch rather than replace

### Exceptions — Mandatory Reads (`--full` / `--update` only)

The following file categories are **mandatory reads** in `--full` and `--update` mode regardless of the "no open-ended exploration" rule. They supply the concrete numbers and enumeration boundaries that downstream `ywc-spec-validate` checks for. Skipping them is the most common cause of `DONE_WITH_CONCERNS` at validate time.

| Category | Glob / location | Why mandatory | What to capture |
|---|---|---|---|
| Constants files | `**/*.constants.{ts,js,py}`, `**/*constants*.{ts,js,py}`, `**/config/*.{yaml,yml,json}`, `**/*config*.{ts,js}`, `**/.env.example`, `**/.env.*.example` | Source of truth for plan limits, retry counts, fee rates, retention periods, timeouts (also covers env-var defaults — projects often place defaults in `.env.example`) | Every numeric value → `06-requirements.md` NFR section, with a `file:line`-style citation under "Existing Constraints Touched" |
| Primary schema (full enumeration) | `prisma/schema.prisma`, `*/migrations/*.sql` index, `*/models/index.{ts,py}`, `*/entities/index.{ts,py}` | Every model name must reach `03-data.md` | All model names extracted via `grep "^model " <schema>` (or equivalent) → every name appears by name in `03-data.md` |
| Feature directory listing | `ls <backend-or-src>/features/` (one line) or equivalent module index | Each top-level directory typically corresponds to a 02-features.md section. Missing directories = spec coverage gap | Each directory name → ≥1 user story in `02-features.md` |
| Auth guards / middleware | `**/guard*.{ts,py}`, `**/middleware*.{ts,py}`, `**/auth/*.{ts,py}`, `**/permissions*.{ts,py}` | Defines the role boundaries needed for the Role × Action matrix in `06-requirements.md §Security` | Every role discriminator → Role × Action matrix when project has ≥3 distinct roles |
| Ubiquitous Language (canonical vocabulary) | `docs/ubiquitous-language.md` (if exists) | The `Synonyms to Avoid` column defines the canonical-vocabulary boundary for the entire project. Every role / entity / concept name in the spec MUST be absent from that column, or `ywc-spec-validate` raises a Consistency Warning at validate time | Extract the `Synonyms to Avoid` column before drafting (one-line grep below); cross-check every domain name introduced in the spec against the resulting avoid-list. Found synonyms are either replaced with the canonical term OR proposed as a new canonical term in `§Open Questions`. |

**UL extraction one-liner** (run once before drafting `01-overview.md`, keep the output in scratch buffer):

```bash
grep -E "^\| \*\*" docs/ubiquitous-language.md \
  | awk -F'\\|' '{print $5}' \
  | sed 's/^ *//; s/ *$//' \
  | grep -v "^Synonyms to Avoid$" \
  | grep -v "^$"
```

The output is the avoid-list. Names appearing here are forbidden in the spec body without a canonical replacement.

These exceptions add roughly 1-3× the base token cost. The cost is intentional — they are the difference between a spec that passes `ywc-spec-validate` at the PROCEED band and one that triggers a Re-plan iteration. Re-plan iterations cost more in both tokens and human attention than the initial deep read.

**What is still off-limits** under "no open-ended exploration":

- Full reading of feature implementation files (e.g., `*/features/*/*.service.ts`) — read only the directory names and any colocated `README.md`
- Test files (`*.spec.ts`, `*.test.ts`) — these inform the implementation, not the spec
- Generated code / type definitions (`*.gen.ts`, `*.d.ts`)
- Migration history beyond the most recent schema state
