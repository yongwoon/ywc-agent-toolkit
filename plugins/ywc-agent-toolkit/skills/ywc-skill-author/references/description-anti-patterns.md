# Description Anti-Patterns

The `description` field in skill frontmatter is the primary mechanism Codex uses to decide whether to activate a skill. Getting it wrong is the #1 cause of skill misfires (wrong skill activated, or right skill skipped).

This guide captures the failure modes documented across superpowers, Anthropic's official skill spec, and production ywc-* skills. Read this before writing or auditing any `description` field.

## The Core Trap: Workflow Summary

**The single biggest anti-pattern**: writing a description that summarizes what the skill does.

When the description summarizes the workflow, Claude reads the description and treats it as the full skill instruction. The SKILL.md body — including the Rationalization Defense, the careful step ordering, the validation checklist — gets skipped as documentation.

Source: superpowers `writing-skills` documents this with empirical evidence. A description saying "code review between tasks" caused Claude to do ONE review even though the skill body specified TWO.

### Example

```yaml
# BAD — summarizes the workflow
description: (ywc) Stage, commit, and optionally push changes following the
  repository's existing commit conventions. Reads git log to infer the project's
  type/scope/message style, selects only files relevant to the current session,
  splits logically distinct changes into separate commits, and reports the result.

# GOOD — trigger only
description: (ywc) Use when the user says "commit", "커밋", "커밋 해줘", "commit
  push", "push", "지금까지 한 작업 커밋", or any phrase indicating intent to stage,
  commit, or push current work. Do not use for PR creation, code review, or
  making code changes.
```

The good version contains zero workflow detail. It only tells Claude **when to activate**.

## Anti-Pattern Catalog

### 1. Workflow Summary

Already covered above. Detection: the description contains verbs describing what the skill does (e.g., "Reads...", "Generates...", "Iterates over...").

### 2. Missing Anti-Triggers

A description that says only "Use when X" without "Do not use for Y" leaves the activation surface ambiguous. Sibling skills with overlapping vocabulary (e.g., `ywc-spec-validate` vs `ywc-impl-review`) collide.

```yaml
# BAD — no anti-triggers
description: (ywc) Use when the user wants a code review.

# GOOD — anti-triggers point to siblings
description: (ywc) Use after implementation is complete and before creating a PR,
  when the user wants to validate code matches the spec... Do not use during
  active code generation, for spec-only review (use ywc-spec-validate), or for
  product/business-level review (use ywc-product-review).
```

### 3. Single-Language Triggers

If the user-base writes in Korean, English, and Japanese, an English-only description loses Korean and Japanese activation entirely.

```yaml
# BAD — English only
description: (ywc) Use when the user wants to commit changes.

# GOOD — multilingual trigger phrases
description: (ywc) Use when the user says "commit", "커밋", "커밋 해줘", "commit
  push", "push", "지금까지 한 작업 커밋", ...
```

Always include realistic phrases users actually type, not abstract trigger names.

### 4. Abstract or Vague Triggers

Triggers like "Use for code work" or "Use when developing" match nothing and everything simultaneously. They produce both false positives (activated when irrelevant) and false negatives (skipped when relevant because match score is low).

```yaml
# BAD — abstract
description: (ywc) Use for technical research.

# GOOD — concrete situations and natural-language phrases
description: (ywc) Use when comparing libraries, investigating implementation
  approaches, evaluating technology options, or gathering best practices before
  writing specifications. Triggers: "기술 조사", "라이브러리 비교", "research",
  "investigate", "compare options", "어떤 걸 쓸까", "best way to implement"...
```

### 5. First-Person Voice

Descriptions are injected into the system prompt. First-person reads as awkward agent self-talk.

```yaml
# BAD
description: I help users commit their work.

# GOOD
description: (ywc) Use when the user says "commit"...
```

### 6. Mentioning Tools or Implementation Detail

The description should describe the **trigger condition**, not the implementation strategy. Tool names, library names, internal architecture — none of these belong in the description.

```yaml
# BAD — mentions implementation
description: (ywc) Use the gh CLI and Bash to read PR comments and reply via
  GitHub API.

# GOOD
description: (ywc) Use when handling PR review feedback, addressing code review
  comments, or responding to GitHub PR review threads...
```

### 7. Promises in Description

Avoid "this skill ensures..." / "guarantees..." / "automatically...". They sound like marketing copy and crowd out trigger information.

```yaml
# BAD
description: (ywc) Automatically generates dependency-safe tasks ensuring quality.

# GOOD
description: (ywc) Use when converting a specification into implementation tasks...
```

### 8. Length Bloat

While the Anthropic spec allows up to ~1024 chars in frontmatter, the description should be **scannable in one read**. Aim for 200–500 characters. Beyond that, the agent's matching attention drops.

If the description grows past 500 chars, it usually means it has slipped into Workflow Summary anti-pattern #1.

### 9. PROACTIVELY Without Specification

Some skills use `Use PROACTIVELY for...`. This is fine when followed by concrete triggering conditions. Without them, "PROACTIVELY" is noise.

```yaml
# BAD
description: (ywc) Use PROACTIVELY for review.

# GOOD
description: (ywc) Use after implementation is complete and before creating a
  PR, when the user wants to validate...
```

## Validation Heuristic

For any description, ask:

1. **Does it answer "When should this skill activate?"** — if yes, ✓
2. **Does it summarize what the skill does?** — if yes, ✗ (anti-pattern #1)
3. **Does it tell siblings apart?** — if no, add anti-triggers
4. **Would a Korean / Japanese user's natural request match?** — if no, add multilingual triggers
5. **Is it under 500 characters?** — if no, audit for workflow summary creep

## Quick Reference Card

| Component | Required? | Format |
|---|---|---|
| `(ywc)` prefix | Yes | Literal `(ywc) ` at start |
| `Use when ...` | Yes | Trigger conditions only |
| `Triggers: "...", "..."` | Yes (user-facing) | Quoted natural-language phrases (한/영/일) |
| `Do not use for ...` | Yes | Explicit anti-triggers, point to sibling skill where relevant |
| Workflow summary | No | Forbidden |
| Tool / library names | No | Forbidden |
| First-person voice | No | Forbidden |
| Marketing language | No | Forbidden |

## Empirical Evidence

The production ywc-* skills were rewritten in 2026-04 to follow this guide. Before/after comparison (from this repository's commit history, `8f69b29`):

- **Before**: descriptions averaged 380 chars, often mixing trigger and workflow summary.
- **After**: descriptions averaged 320 chars, trigger-only with explicit anti-triggers and 한/영/일 keywords.

The change is observable in any ywc-* skill's `git log -p SKILL.md` output.
