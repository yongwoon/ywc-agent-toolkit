# Full Generation Workflow

Used when `--full` or `--update` flag is set. Requires user confirmation before starting.

## Pre-condition Check

Before any LLM call, verify:
- User has confirmed the operation ("yes" to the confirmation prompt)
- `docs/specification/` directory is initialized (run `init-spec-structure.sh` if not)
- Language is set (`--lang` or default `ko`)

## Model Selection

Use the most capable available reasoning model. Do not use a low-reasoning pass for full spec generation — full codebase analysis requires frontier reasoning.

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
- For large schema files, read only entity/table definitions, not the full migration history
- For large route files, read only the route index or top-level exports
- In `--update` mode, read each existing section first and patch rather than replace
