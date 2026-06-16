---
name: ywc-ubiquitous-language
description: >-
  (ywc) Use when creating, extracting, or updating a project's ubiquitous
  language document (shared domain vocabulary between developers, domain experts,
  and LLMs). Triggers: "유비쿼터스 언어 작성", "도메인 용어 정리", "ubiquitous language",
  "도메인 glossary 만들어줘", "용어집 업데이트", "ubiquitous language 추출",
  "プロジェクト用語集作成", "domain glossary", "DDD 용어 정리",
  "ubiquitous language document". Do not use for general project documentation
  structure (use ywc-project-docs), spec writing (use ywc-plan), or
  implementation task decomposition (use ywc-task-generator).
---

# Ubiquitous Language

**Announce at start:** "I'm using the ywc-ubiquitous-language skill to create or update the project's shared domain vocabulary."

This skill produces or maintains `docs/ubiquitous-language.md` — a shared vocabulary file that aligns developers, domain experts, and LLMs on canonical term usage. It operates in three modes: **new** (interview-driven creation from scratch), **extract** (term discovery from an existing codebase), and **update** (incremental revision of an existing document).

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Everyone on the team knows the terms — no need for a document" | LLMs do not share team knowledge. Every term the LLM misinterprets costs a correction cycle. The document is primarily for LLM context injection, not just team alignment. |
| "I'll auto-extract and write the file without user confirmation" | Extracted terms without definition review produce a synonym-polluted glossary. A raw class name is not a domain term until a human confirms its meaning. Always present candidates before writing. |
| "Korean translation is obvious — I'll infer it" | Machine-inferred Korean business terms introduce errors that survive in code and prompts for years. Surface every Korean equivalent to the user for confirmation. |
| "Bounded Contexts add complexity for a small project, use a flat list" | A flat glossary lets homonyms (same term, different meaning in different contexts) silently coexist. Start with "Core Domain" if only one context exists — it takes one line. |
| "The file already exists, I'll append without reading it" | Appending without reading creates duplicate entries and contradictory definitions. Always read the full file before any write. |
| "ywc-project-docs handles the docs/ structure, I'll skip update" | ywc-project-docs manages directory skeleton and README-level docs. ywc-ubiquitous-language owns domain vocabulary content. Both must run independently. |
| "DDD types (Entity, Aggregate etc.) are overkill here, skip the column" | DDD Type column is optional — controlled by `--ddd` flag. But the **Synonyms to Avoid** column is always required; it is the highest-value anti-confusion signal. |

**Violating the letter of these rules is violating the spirit.** A glossary with unconfirmed terms or missing synonyms degrades LLM output quality with every prompt that references it.

## Arguments

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| `--mode` | `--mode new\|extract\|update` | auto-detect | Force a specific mode (see Mode Detection below) |
| `--context` | `--context <name>` | all contexts | Scope to a single Bounded Context for extract/update |
| `--output` | `--output <path>` | `docs/ubiquitous-language.md` | Output file path |
| `--ddd` | flag | off | Add DDD Type column (Entity / Value Object / Aggregate / Domain Event / Policy) |
| `--dry-run` | flag | off | Show proposed changes without writing to disk |

### Mode Detection (when `--mode` is omitted)

| Condition | Auto-selected mode |
|---|---|
| `docs/ubiquitous-language.md` exists | `update` |
| File absent AND source files found (`src/`, `app/`, `lib/`, `internal/`) | `extract` |
| File absent AND no source files | `new` |

## Workflow

### Mode: new — Interview-Driven Creation

**Step 1: Domain Overview**
Ask the user for a 2-3 sentence description of the domain if not already in context. Identify the primary domain and any obvious sub-domains.

**Step 2: Bounded Context Identification**
Propose "Core Domain" as the default single context. If the domain description suggests multiple areas of responsibility, propose 2-4 candidate context names and ask the user to confirm or revise. Start with the minimum set — contexts can be added in `update` mode.

**Step 3: Term Elicitation per Context**
For each context, gather 5–15 core terms via conversation. For each term, collect:
- Canonical English name (the term used in code)
- Korean equivalent (always confirm with user, never infer)
- Definition: 1–2 sentences, from the domain's perspective
- Synonyms to Avoid: names that mean the same thing but must NOT be used

If `--ddd` flag is set, also collect: DDD Type (Entity / Value Object / Aggregate / Domain Event / Policy).

**Step 4: Write File**
Write to `--output` path using the format in [references/document-format.md](references/document-format.md).

**Step 5: CLAUDE.md Integration Prompt**
After writing, print:
```
★ To give LLMs automatic access to this vocabulary, add the following line to your CLAUDE.md:
  @docs/ubiquitous-language.md
```

---

### Mode: extract — Codebase Discovery

**Step 1: Scan for Candidate Terms**
Apply the extraction heuristics in [references/extraction-guide.md](references/extraction-guide.md). Focus on:
- Domain model class/struct names
- Repository, Service, UseCase, Handler names (strip suffix)
- Meaningful enum values
- Prominent variable names in domain logic files

**Step 2: Cluster into Context Candidates**
Group candidates by module/package path. Propose each group as a Bounded Context name. Show the user a table:

```
Context candidate: "Order" (from src/order/, 12 candidates)
Context candidate: "Payment" (from src/payment/, 7 candidates)
```

**Step 3: User Confirmation**
Present the full candidate list. User confirms, rejects, or relabels each term. Do not write any term the user has not confirmed.

**Step 4: Definition Gathering**
For confirmed terms, gather definitions the same way as Mode: new — Step 3.

**Step 5: Write File**
Same as Mode: new — Step 4 and Step 5.

---

### Mode: update — Incremental Revision

**Step 1: Read Existing File**
Read the full `docs/ubiquitous-language.md`. Parse all existing terms, contexts, and synonyms.

**Step 2: Identify Changes**
Ask the user: "What changed since the last update?" Options:
- User describes new features/terms → proceed with description
- User says "check recent commits" → run `git log --oneline -20` and surface domain-relevant changes
- User says "just review" → compare existing terms against current codebase naming

**Step 3: Build CHANGESET**
Propose three lists for user confirmation:
- **ADD**: New terms not yet in the document
- **MODIFY**: Existing terms whose definition or synonyms need revision
- **DEPRECATE**: Terms that no longer exist in the codebase (mark with `~~strikethrough~~` + note, do not delete)

**Step 4: Apply and Update**
Apply confirmed changes. Update the `<!-- updated: DATE -->` header. Append a brief change summary at the bottom of the file.

---

## Output Format

The full format specification is in [references/document-format.md](references/document-format.md).

Summary:

```markdown
# Ubiquitous Language — [Project Name]

<!-- updated: YYYY-MM-DD -->

## Overview
[Domain description, 2-3 sentences]

## Bounded Contexts
| Context | Responsibility |
|---------|---------------|

---

## [Context Name]
| Term | Korean | Definition | Synonyms to Avoid |
|------|--------|-----------|------------------|
```

With `--ddd` flag, a `Type` column (Entity/Value Object/Aggregate/Domain Event/Policy) is inserted between `Korean` and `Definition`.

## Validation

Before declaring complete:

- [ ] Every term has a non-empty Korean equivalent (confirmed with user, not inferred)
- [ ] Every term has at least one entry in Synonyms to Avoid (or explicit `—` if truly none)
- [ ] No two terms share the same Korean equivalent within the same context
- [ ] `docs/ubiquitous-language.md` is parseable Markdown with no broken table rows
- [ ] `<!-- updated: DATE -->` header reflects today's date
- [ ] CLAUDE.md integration prompt was printed to the user

## Common Mistakes

- **Writing before confirming all terms** — The LLM may batch terms and write immediately. Always present the full term list for one confirmation round before writing.
- **Inferred Korean translations** — Korean business terms that look obvious (e.g., "Order" → "주문") may still need confirmation because the team might use a specific nuance (e.g., "발주" vs "주문" for B2B vs B2C).
- **Silent deprecation** — Removing a term without a `~~deprecated~~` marker destroys the history of why a term was abandoned. Teams need that context.
- **Flat list for multi-context domains** — Without Bounded Context separation, "Account" can mean a financial account in one context and a user account in another — both valid, both conflicting.

## Integration

- **Upstream**: `ywc-plan` (call during planning to establish vocabulary before spec writing), `ywc-project-docs` (project docs skeleton)
- **Downstream**: `ywc-task-generator` (tasks reference canonical terms), `ywc-code-gen` (code generation uses canonical naming), `ywc-spec-validate` (spec consistency check)
- **Pairs with**: `ywc-spec-validate` — spec terms should match ubiquitous language; flag mismatches
