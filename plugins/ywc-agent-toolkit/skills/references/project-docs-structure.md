# Project docs/ Structure — Shared Reference

Canonical directory layout, routing rules, naming, anti-patterns, and per-folder conventions for `docs/`. Used by the unified `ywc-project-docs` skill. Locale selection belongs to the in-document **Language Policy**, not to split skill names.

## Recommended Directory Structure

```text
docs/
├── README.md
├── product/            # Product goals, target users, scope
├── architecture/       # System structure, technical choices, ADR
├── specification/      # Per-feature detailed rules, implementation criteria
├── plans/              # Implementation order, milestones, dependencies
├── manuals/            # Operating procedures, configuration guides, how-to
├── troubleshooting/    # Incident response, known-issue resolution
├── design/             # Mockups, brand assets, master designs
├── imgs/               # Auxiliary images for Markdown documents
└── todo/               # Unconfirmed ideas, temporary notes
```

A repository may use `tasks/` instead of `plans/` depending on project flavor, but only one of the two should be fixed as the official name within a single repository.

## Directory Routing Rules

When creating a new document, choose the directory by the document's **purpose**.

### Primary axis (core documents)

| Purpose | Directory | Question it answers | Examples |
|---|---|---|---|
| Product goals, target users, scope | `docs/product/` | "Why does this feature exist?" | `product-overview.md`, `prd-*.md`, `feature-scope.md` |
| System design, technical choices | `docs/architecture/` | "Why and how was it built?" | `technical-spec.md`, `directory-structure.md`, `adr-*.md` |
| Per-feature detailed rules | `docs/specification/` | "What should be built?" | `authentication.md`, `data-model.md`, `api-contract.md` |
| Implementation order, milestones | `docs/plans/` | "When do we implement what?" | `implementation-plan.md`, `phase-1.md`, `dependency-graph.md` |

### Secondary axis (operations, assets, temporary)

| Purpose | Directory | Question it answers | Examples |
|---|---|---|---|
| Operating procedures, configuration guides | `docs/manuals/` | "How to configure and operate?" | `google-oauth-setup.md`, `local-dev-setup.md` |
| Incident response, known issues | `docs/troubleshooting/` | "What to do when problems occur?" | `oauth-debugging.md`, `email-sync-issue.md` |
| Mockups, design assets | `docs/design/` | Visual reference for UI implementation | `.pen`, `logo/`, `screens/` |
| Auxiliary images for documents | `docs/imgs/` | Images referenced in Markdown | diagrams, screenshots |
| Unconfirmed ideas, temporary notes | `docs/todo/` | Content not yet an official baseline | draft notes, follow-up ideas |

### Decision Flow

1. "Why does this feature exist?" → `product/`
2. "Why does this system behave this way?" → `architecture/`
3. "What are the detailed rules of this feature?" → `specification/`
4. "What do we implement first?" → `plans/`
5. "How do we configure this service?" → `manuals/`
6. "How do we resolve this problem?" → `troubleshooting/`
7. Still a pre-confirmation note? → `todo/`
8. None of the above → ask the user.

## LLM Reading Order

When delegating coding to an LLM, the reading order should be fixed even when many documents exist. Each stage becomes the criterion for the next:

```
1. product/        → so scope is not misunderstood
2. architecture/   → criteria for file placement and responsibility separation
3. specification/  → criteria for detailed behavior implementation
4. plans/          → so dependencies are not ignored
5. as needed: manuals/, troubleshooting/, design/
```

Cross-references should follow the same direction — newer documents link upward to higher-order baseline documents.

## Naming Convention

```
<subject>[-<detail>].md
```

- **Lowercase ASCII + hyphen** only (no Korean/Japanese/Chinese filenames).
- **Minimize suffixes**: `-architecture`, `-system`, `-design`, etc. are unnecessary because the directory already conveys role.
  - `architecture/authentication.md` (not `authentication-architecture.md`)
  - `manuals/deploy-checklist.md` (not `setup-deploy-checklist.md`)
- **No verbs**: use noun-form subjects.

## Document Structure Template

Every document follows this pattern (translate inline labels into the target locale):

```markdown
# Title

Description (1–2 sentences)

> **Related documents**
>
> - [Document title](../relative/path.md) — one-line description
> - [Document title](../relative/path.md) — one-line description

---

## Table of contents

1. [Section 1](#1-section-1)
2. [Section 2](#2-section-2)

---

## 1. Section 1

### 1.1 Subsection

Content...
```

**Key rules:**
- Cross-reference related documents in the top `> Related documents` block.
- Include a TOC when there are 5 or more sections.
- Section numbering: `## N. Title`, sub `### N.M Title`.
- Separate major sections with horizontal rules (`---`).

## Document Authoring Rules

These rules ensure the LLM codes against the correct documentation baseline.

1. **One folder, one responsibility** — do not place product-vision documents in `specification/` or task checklists in `architecture/`.
2. **Separate official baselines from working drafts** — keep drafts and unconfirmed notes in `todo/`; promote to an official folder only after confirmation.
3. **Folder meaning should precede document title** — LLMs interpret path together with title. The folder name itself should explain the document's responsibility.
4. **Do not duplicate the same content across folders** — duplication looks like conflicting baselines to an LLM. Keep one source and link from elsewhere.
5. **Implementation-baseline documents are rule-centric, not narrative** — especially `specification/` documents prioritize expected behavior, constraints, edge cases, data contracts, and acceptance criteria over background prose.
6. **Temporary notes must not look like official documents** — `todo/` should signal draft status by name alone.

## Anti-patterns to Avoid

- **No boundary between `architecture/` and `specification/`** — mixing high-level design and detailed rules makes it ambiguous which document the LLM should treat as the primary baseline.
- **Placing requirement originals inside `plans/`** — execution plans should describe order and dependencies. Requirement originals belong in `product/` or `specification/`.
- **Putting Markdown baseline documents inside `design/`** — keep `design/` as an asset store; baseline documents go elsewhere.
- **Drafts shown at the same level as official documents** — when `todo/` notes appear at the same hierarchy as confirmed `specification/` documents, the LLM may follow the wrong draft.
- **Operations procedures mixed with product specifications** — writing OAuth setup steps and authentication policy in the same document conflates implementation criteria with environment configuration.

## When to Introduce `operations/`

The default structure does not include `operations/` as a separate folder. `manuals/` and `troubleshooting/` are sufficient initially.

Introduce `operations/` when:
- Deploy and rollback procedures are referenced as separate runbooks frequently.
- Monitoring, alerting, incident response, and on-call documents grow.
- Backup, restore, and migration become independently managed.

Roles after separation:
- `manuals/`: setup, admin guide, external service configuration.
- `operations/`: deploy, rollback, monitoring, incident response, runbooks.
- `troubleshooting/`: per-problem symptom diagnosis and resolution.

## Architecture Document Convention

`architecture/` documents are recommended to include:

1. **System overview** — big-picture diagram.
2. **Architecture** — layers, components, API structure.
3. **Workflows** — primary process flows.
4. **Business logic** — rules, constraints.
5. **Data model** — primary table relationships.
6. **Error handling** — error codes, exception handling.
7. **Future plans** — unimplemented features (→ separate into `docs/plans/`).

Operating procedures do not belong in `architecture/` → place them as separate documents in `manuals/`.

## Specification Document Convention

`specification/` documents are rule-centric, not narrative. Prioritize:

- **Expected behavior** — normal-case behavior baseline.
- **Constraint** — restrictions.
- **Edge case** — handling for exceptional situations.
- **Data contract** — input/output data formats.
- **Acceptance criteria** — completion conditions.

## Product Document Convention

`product/` documents are the starting point for understanding "why this feature exists" before implementation. Include:

- **Product goals** — the problem this product solves.
- **Target users** — who it is for.
- **Core capabilities** — what it can do.
- **Scope** — included / excluded items.
- **Success metrics** — how success is measured.

## Pre-creation Checklist

Before creating any document, verify:

1. **Existing document check** — if a document on the same topic already exists, **update it** (do not create a new one).
2. **Directory selection** — confirm the appropriate directory using the routing rules above.
3. **Cross-references** — when related documents exist, link from the newer/lower-level document to the higher-order baseline document.
4. **Official vs. draft** — pre-confirmation content goes in `todo/`; confirmed content moves to the official folder.
5. **CLAUDE.md rule** — generate documents only when the user explicitly requests them.
