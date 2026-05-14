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
| Date | Section | Summary |
|------|---------|---------|
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

One `## Entity` per key data concept.
**No field types, no column names, no SQL or ORM syntax.**

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
- [e.g., "Page load must complete within X seconds under Y concurrent users"]

## Security
- [e.g., "User data must be encrypted at rest and in transit"]

## Availability
- [e.g., "System must be available 99.9% of the time"]

## Scalability
- [e.g., "Must support growth to X users without architectural change"]

## Compliance
- [Regulation or standard the system must satisfy]
```

---

### 07-glossary.md

```markdown
# Glossary

| Term | Definition |
|------|-----------|
| [Term] | Plain-language definition. No jargon. |
```

Include technical terms used in the spec that a non-developer might not know.
