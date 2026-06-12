# Spec Directory Structure

## Directory Layout

```
docs/specification/
├── README.md              # Index + last-updated + change log
├── 01-overview.md         # Project goals, stakeholders, scope
├── 02-features.md         # Feature areas with user stories
├── 03-data.md             # Data entities and relationships
├── 04-interfaces.md       # External integrations and APIs
├── 05-user-flows.md       # User journeys and screen flows
├── 06-requirements.md     # Non-functional requirements
└── 07-glossary.md         # Key terms explained in plain language
```

---

## Section Templates

### README.md

```markdown
# [Project Name] Specification
**Last updated**: YYYY-MM-DD
**Language**: Korean / Japanese / English

## Sections
- [Overview](01-overview.md)
- [Features](02-features.md)
- [Data](03-data.md)
- [Interfaces](04-interfaces.md)
- [User Flows](05-user-flows.md)
- [Requirements](06-requirements.md)
- [Glossary](07-glossary.md)

## Change Log
| Date | Section | Source | Summary |
|------|---------|--------|---------|
```

---

### 01-overview.md

```markdown
# Overview

## Project Goal
One-paragraph description of what the system does and why it exists.

## Target Users
| User Type | Description |
|-----------|-------------|
| [Primary user] | Who they are and what they primarily need |

## Scope
### In Scope
- [Capability 1]

### Out of Scope
- [Deferred feature] — reason for deferral

## Stakeholders
| Role | Name / Team | Interest |
|------|-------------|---------|

## Constraints
- [Technical or business constraint]
```

---

### 02-features.md

```markdown
# Features

## [Feature Area Name]

### [Feature Name]
**User story**: As a [user type], I want to [action] so that [benefit].

**Acceptance criteria**:
- [ ] [Observable outcome 1]
- [ ] [Observable outcome 2]

**Notes**: [Business rule or edge case in plain language]
```

One `## Feature Area` per major functional domain.
Each `### Feature` is one user-facing capability.
**No code, no technical implementation detail.**

---

### 03-data.md

```markdown
# Data

## [Entity Name]
**What it represents**: One sentence describing the real-world concept.

**Key attributes**:
- [Attribute name]: [What it stores, in plain language]

**Relationships**:
- Connected to [Other Entity] — [what the relationship means]
```

One `## Entity` per key data concept. **All models in the project's primary schema (e.g., `prisma/schema.prisma`, `*/migrations/*.sql`, `*/models/`, or `*/entities/`) MUST appear by name in this file** when in `--full` / `--update` mode. Sibling entities sharing a prefix MAY be grouped under one `### <Family>` heading (e.g., `### CampaignTarget Family`), but each member name MUST appear in an inline list under that heading. Silent omission causes Code Compatibility Critical findings at `ywc-spec-validate` time.

**No field types, no column names, no SQL or ORM syntax.** This rule applies to **all sections**, not only 03-data — Prisma directives (`@default`, `@relation`, `dbgenerated(...)`), SQL fragments (`SELECT`, `WHERE`, `CREATE TABLE`), and ORM decorators in any section (including 06-requirements §Multi-Tenant Isolation, 04-interfaces, etc.) must be paraphrased into plain prose. Field-reference identifiers (`tenantId`, `BeaconSite.samplingState`) in inline backticks remain permitted. See SKILL.md §6 Writing Rules for the full ruleset.

---

### 04-interfaces.md

```markdown
# Interfaces

## [Interface Name]
**Purpose**: What this connection enables.
**Direction**: [External system] → [This system] / bidirectional
**Triggered by**: [What causes data to flow across this interface]
**Data exchanged**: [Description in plain language]
**Error handling**: [What happens when the interface is unavailable]
```

---

### 05-user-flows.md

```markdown
# User Flows

## [Flow Name]
**Actor**: Who initiates this flow.
**Trigger**: What event or decision starts the flow.

**Steps**:
1. [Actor] [action]
2. System [response]
3. ...

**Outcome**: What the actor achieves.

**Alternate paths**:
- If [condition]: [what happens instead]
```

---

### 06-requirements.md

```markdown
# Non-Functional Requirements

## Performance
- Concrete example: "Operator console p95 < 1.5s under 1000 concurrent users"
- Placeholder example (DO NOT SHIP): "Page load must complete within X seconds under Y concurrent users"

## Security
- [e.g., "User data must be encrypted at rest and in transit"]

## Authentication & Authorization (required when project has ≥3 distinct actor roles)
- Role × Action matrix listing every role × every protected action
- Source of truth for role determination (e.g., DB-first vs JWT claim vs both)

## Availability
- [e.g., "System must be available 99.9% of the time"]

## Scalability
- [e.g., "Must support growth to X users without architectural change"]

## Audit Trail (required when the project records state changes for compliance)
- What state-change actions are recorded (canonical action list)
- Required fields (actor, before/after snapshot, correlation ID, etc.)
- Retention period and physical-delete policy
- Read access policy (cross-tenant vs own-tenant only)

## Data Lifecycle (required when the project has audit / analytics / time-series data)
- Retention period per entity
- Sampling strategy (if data volume requires it)
- Aggregation timing

## Compliance
- [Regulation or standard the system must satisfy]

## Existing Constraints Touched (required when `--full` / `--update` mode runs)
- Each numeric value used elsewhere in this file MUST be cited here with a `file:line`-style reference to the constants / config / migration file that owns it
- Example: `BASIC_AD_SPEND_CAP_JPY = 500,000` → `backend/src/features/billing/basic-ad-spend-cap.constants.ts:42`
```

**Critical writing rules for `06-requirements.md`:**

- Every NFR MUST include ≥1 concrete number. Placeholder values like `X seconds`, `Y users`, `数秒以内` are NOT acceptable in the shipped file.
- If a target is genuinely undefined for the project, list it under `## Open Questions` with the reason, do NOT leave it as a placeholder.
- The `## Existing Constraints Touched` subsection is the source of truth — every number above must be cited there to prove it was extracted from code, not invented.
- `## Authentication & Authorization`, `## Audit Trail`, and `## Data Lifecycle` sections may be omitted (or replaced with `N/A — <reason>`) when the project genuinely does not need them. Omission MUST be justified, not silent.

---

### 07-glossary.md

```markdown
# Glossary

| Term | Definition |
|------|-----------|
| [Term] | Plain-language definition. No jargon. |
```

Include technical terms used in the spec that a non-developer might not know.
