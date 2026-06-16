# Symbol System for Codex Skill Output

> Shared reference document. Linked from any `ywc-*` skill that produces a status report, completion summary, or multi-step progress trace.

## 1. Purpose

This document defines a small, fixed symbol vocabulary that `ywc-*` skills can use in their output to:

- **Compress repetitive status language** without losing information (typically 25–40% fewer tokens in step-by-step reports).
- **Preserve hierarchy at a glance** in long executor reports where prose status lines blur together.
- **Standardize severity and flow markers** so a reader can scan reports from different skills without context-switching.

The symbol set is intentionally small. Skills must not invent new symbols — if a needed concept is not on this page, write it as plain text.

## 2. Status Markers

Use these for step outcomes, gate decisions, and per-item completion state.

| Symbol | Meaning | When to use |
|--------|---------|-------------|
| ✅ | passed, completed | Step finished successfully and produced expected output. |
| ❌ | failed, error | Step finished with a failure that requires attention. |
| ⚠️ | warning, concern | Step completed but with a caveat the reader must see. |
| 🔄 | in progress | Step is currently running (for live progress traces). |
| ⏳ | pending, queued | Step is scheduled but has not started. |
| 🚫 | blocked | Step cannot run because a prerequisite is unmet. |
| ⏭ | skipped | Step was intentionally skipped (with reason given inline). |

## 3. Severity Markers

Use these for findings in review skills (`ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-product-review`).

| Symbol | Severity | Definition |
|--------|----------|------------|
| 🚨 | Critical | Blocks merge or release. Security risk, data loss risk, or specification contradiction. |
| 🔴 | High | Should be fixed before merge. Bug, regression risk, or significant maintainability concern. |
| 🟡 | Medium | Address soon. Code smell, missing test, or inconsistency with conventions. |
| 🔵 | Low | Optional. Style suggestion or minor refactor opportunity. |
| ℹ️ | Info | Observation only. No action required. |

The five-level scale matches the existing severity vocabulary used in `ywc-impl-review` and `ywc-security-audit`. Symbols replace the words but not the structure.

## 4. Flow Operators

Use these to compress sequential and causal relationships in step traces.

| Symbol | Meaning | Example |
|--------|---------|---------|
| → | leads to, then | `lint ✅ → test 🔄 → deploy ⏳` |
| » | sequence with emphasis | `Phase 1 » Phase 2 » merge` |
| ⇒ | transforms into, produces | `spec ⇒ task list ⇒ branches` |
| ← | rolled back from, reverted | `release ← v1.4.2 (hotfix)` |
| ∴ | therefore | `tests ❌ ∴ blocked at Step 4` |
| ∵ | because | `escalated to advisor ∵ ambiguous severity` |

## 5. Domain Markers (Optional)

Use these only when a report mixes findings across multiple domains and the reader needs to filter by domain at a glance. Most skills do not need them.

| Symbol | Domain |
|--------|--------|
| 🛡️ | Security |
| ⚡ | Performance |
| 🏗️ | Architecture |
| 🎨 | UI / UX |
| 📦 | Build / Release |
| 🧪 | Test / QA |

## 6. Example Output Conversions

### Before (executor completion, prose)

```
Step 1: Branch creation succeeded.
Step 2: Code generation succeeded.
Step 3: Tests are currently running.
Step 4: PR creation is blocked because Step 3 has not completed.
Step 5: Merge is queued and will run after Step 4.
```

### After (executor completion, symbol)

```
Step 1: branch       ✅
Step 2: code-gen     ✅
Step 3: test         🔄
Step 4: PR           🚫 ∵ Step 3 not complete
Step 5: merge        ⏳
```

### Before (review finding, prose)

```
Critical: SQL injection risk in src/api/users.ts:42 — user input
is concatenated into a query string. Should be parameterized.
```

### After (review finding, symbol)

```
🚨 [src/api/users.ts:42] SQL injection — input concatenated into query.
   Action: parameterize.
```

## 7. Rules of Use

- **Do not duplicate symbols for the same concept.** Avoid repeated status or severity markers such as `✅✅` or `🚨🚨`.
- **Domain marker combinations are allowed when they add filtering value.** If needed, combine one severity marker with one optional domain marker, separated by a space and in consistent order, for example `🚨 🛡️`. Do not stack multiple domain markers on one finding.
- **Symbols supplement structure, not replace it.** Severity and step IDs still carry meaning; the symbol is a visual marker that lets the reader scan.
- **Plain-text fallback is always allowed.** A skill writing a Slack message or a non-rendering target may emit `[CRITICAL]` instead of `🚨`. Pick one mode per output and stay consistent within that output.
- **Do not use symbols inside generated code, commit messages, or PR titles.** They belong in skill *output* (reports, summaries, status traces), not in artifacts the skill produces for downstream tools.
- **Domain markers are opt-in.** A pure security audit does not need 🛡️ on every line; the audience already knows the domain.

## 8. Anti-Patterns

- **Inventing new symbols.** If a concept is missing, write it in words and propose an addition to this file.
- **Decorative use.** Symbols mark status, severity, flow, or domain. They are not bullet replacements or visual flair.
- **Mixed vocabularies in one report.** A report that mixes 🚨/🔴/🟡 with `[CRITICAL]/[HIGH]/[MED]` is harder to scan than either alone.
- **Symbols without anchors.** Every status line must include a step ID, file path, or named target. `✅` on its own communicates nothing.

## 9. Scope and Limits

This symbol set covers the four output dimensions skills actually produce: status, severity, flow, and (optionally) domain. It deliberately excludes:

- Decorative symbols (sparkles, fire, rocket).
- Sentiment or judgment markers (good, bad, surprising).
- Domain-specific markers beyond the six listed in §5.

If a skill needs richer visual structure (tables, nested trees, color), use Markdown — not more symbols.
