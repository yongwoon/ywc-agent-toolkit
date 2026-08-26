# Task Initials Resolution — Shared Reference

The single canonical definition of how `ywc-task-generator` resolves **collaborator initials**
to namespace task-ID allocation, ensuring concurrent-execution collisions are structurally
impossible. Consuming skills reference this file with an explicit `> **Action required**: Read
[references/initials-resolution.md]` directive and MUST NOT restate the precedence chain,
derivation algorithm, or section format inline (single-source-of-truth rule).

Used by `ywc-task-generator`. Adding a new consumer means adding one pointer in that skill's
body and one row to the consuming-skill list in `claude-code/skills/CLAUDE.md` — nothing here
changes.

## Scope

This governs **task-ID numbering namespace only** — the `[INITIALS]` segment of task IDs
(`[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`). It never governs session
language, output language, or any user-facing setting. Absence of any initials policy is a
no-op: it never blocks, delays, or errors a consuming skill.

## Precedence Chain

Resolve in this order; the first rung that yields a valid initials string wins:

1. **`--initials` flag** — an explicit per-call flag on the consuming skill (validated against
   `^[a-z0-9]{2,4}$`).
2. **Project policy** — a `## Task Initials` section in the project `CLAUDE.md`.
3. **Derivation + confirmation** — derive from `git config user.email` / `user.name`, present
   the derived value for user confirmation, cache on approval.
4. **Absence is valid** — if no rung yields a value, the skill does not block (see
   no-block invariant, below).

```
resolve(initials_flag, project_claude_md, git_config):
  if initials_flag present            -> validate(initials_flag)
  elif project ## Task Initials       -> extract and validate
  elif git_config yields derivable    -> derive, prompt, cache on approval
  else                                -> proceed without initials (no-block)
```

## Derivation Algorithm

When both `--initials` flag and project `CLAUDE.md` policy are absent:

1. Read `git config user.email`. If unset, fall back to `git config user.name`.
2. Take the local-part (before `@`) of the email, or the full name if email is absent.
3. Split the string on `.` (dot), `_` (underscore), or `-` (hyphen) to form segments.
4. For each segment, take its first character, convert to lowercase.
5. Join all first characters into a single string (e.g., `yongwoon.kim` → `yk`).
6. If the result is fewer than 2 characters:
   - Take the first 2–4 lowercase alphanumeric characters of the original local-part or name
     instead.
   - If the original is entirely non-alphanumeric or shorter than 2 characters, the
     derivation fails and the user must provide a value manually (see [Edge Cases](#edge-cases)).
7. Validate the derived value against `^[a-z0-9]{2,4}$`. If validation fails, propose the
   derived value to the user but require explicit input; re-ask on each failed attempt.

**Examples:**

| Input | Derivation |
|---|---|
| `user.email = yongwoon.kim@example.com` | `yk` (y from yongwoon, k from kim) |
| `user.email = alice_smith@example.com` | `as` (a from alice, s from smith) |
| `user.email = j.doe@example.com` | `jd` (j from j, d from doe) |
| `user.email = bob-jones@example.com` | `bj` (b from bob, j from jones) |
| `user.name = Jane (first 4 chars)` | `jane` (< 5 chars total) |
| `user.email = a_b_c_d_e@…` | `abcde` → fails regex (5 chars), rejects; user specifies |

## Validation

The initials string **must match** `^[a-z0-9]{2,4}$`:

- Exactly 2–4 characters.
- Lowercase only (a–z, 0–9).
- No spaces, hyphens, underscores, or special characters.

A value failing this regex is treated as invalid. If a cached `## Task Initials` value in
`CLAUDE.md` later fails validation, it is treated as absent and re-derived + re-confirmed.

```regex
^[a-z0-9]{2,4}$
```

## Canonical `## Task Initials` Section Format

Written by `ywc-task-generator` when initials are first resolved and cached, read by all
subsequent invocations. A file has at most one such section (create-or-replace semantics,
never append):

```markdown
## Task Initials

- **Initials**: yk   <!-- ^[a-z0-9]{2,4}$ -->
- Applies to: ywc-task-generator가 생성하는 task id의 INITIALS 세그먼트.
```

The comment `<!-- ^[a-z0-9]{2,4}$ -->` is a persistent marker indicating the validation
rule. If two or more `## Task Initials` headings exist, the first is updated with the current
resolved value and all others are removed, leaving exactly one.

## Numbering Scope

When `ywc-task-generator` generates a new task-ID PHASE number:

- **Initials-scoped matching:** Only task-ID entries carrying the resolved initials prefix
  (e.g., `yk-000001-010-…`) are compared to find the maximum PHASE. Entries with other
  initials and legacy unprefixed entries are excluded from this comparison.
- **Worktree union:** The scan includes `tasks/` and `tasks/completed/` directories from:
  - The current worktree (via `pwd`).
  - All linked worktrees returned by `git worktree list --porcelain`.
  - Paths without `tasks/` are silently skipped (no error).
- **Legacy seed rule:** If no initials-prefixed entries exist (count = 0) and at least one
  legacy unprefixed entry exists, seed the first PHASE of the new initials namespace with
  `legacy_max_phase + 1`. This prevents the same `dependency-graph.md` from mixing
  `## Phase 000001` and `## Phase yk-000001` at identical numeric values, which would be
  ambiguous to humans reading the document.
- **Mechanics:** The precise implementation of PHASE scanning, graph validation, and
  worktree union is delegated to the `next-task-number.sh` script's own comments (NFR3:
  single-source-of-truth rule). This reference document defines the rules; the script
  implements them deterministically.

## Caching

Initials are cached to the project `CLAUDE.md` exactly once, on first resolution.

- **Create-or-replace:** The first invocation with a resolved initials value writes a
  `## Task Initials` section. Subsequent invocations read it and skip re-derivation /
  re-confirmation.
- **Idempotency:** If the section already exists and its value validates, the skill does
  not modify it. Re-running the skill on the same project never prompts again.
- **Duplicate removal:** If a file contains more than one `## Task Initials` heading (e.g.,
  from a manual edit or merge conflict), the next write updates the first and removes the
  rest, leaving exactly one.
- **Persistence location:** `CLAUDE.md` at the project root. This differs from sibling specs
  (e.g., Codex uses `.codex/ywc.json`); the choice reflects each runtime's existing
  configuration convention.

## Collision Advisory

Before confirming a derived initials value, the skill must:

1. Scan the `tasks/` and `tasks/completed/` directories of the current worktree and all
   linked worktrees (same union as [Numbering Scope](#numbering-scope)).
2. Collect all unique initials prefixes found in task-ID entries matching
   `^([a-z0-9]{2,4})-[0-9]{6}-[0-9]{3}-`.
3. If the derived value already exists in the list:
   - Include in the confirmation prompt: "This project already has N task(s) prefixed with
     `<initials>`. If you did not create them, specify a different value."
   - Do **NOT** block or error; the user may override.
4. If the derived value is not in the list:
   - Present a standard confirmation prompt without the collision notice.

**Never** automatically block or reject a duplicate initials collision; such collisions
are often legitimate (same person re-running the tool, or intentional reuse). The advisory
is informational only.

## Edge Cases

| Situation | Expected Behavior |
|---|---|
| `git config user.email` and `git config user.name` both unset | Derivation fails. Prompt the user to provide initials directly. Never invent a value. |
| Derived value fails `^[a-z0-9]{2,4}$` (e.g., non-ASCII name, 5+ chars) | Propose the derived value but require explicit user input. Re-ask on each failed validation attempt. |
| `CLAUDE.md` contains two or more `## Task Initials` sections | Apply create-or-replace: update the first, remove duplicates, leaving exactly one. This is not an error condition. |
| Two collaborators derive the same initials (e.g., `yongwoon.kim` and `yuki.kato` both → `yk`) | Structural collision is not automatically detected during derivation (detection requires cross-person coordination not available offline). The collision advisory (above) catches it if one person's tasks are already committed. Recommend: include collision notice in the confirmation prompt ("initials `yk` is already in use") as an advisory, never a block. Users who encounter this in pair work should manually override one initials value. |
| Legacy unprefixed entries (e.g., `000001-010-…`) and initials-prefixed entries coexist in the same repository | Both are valid. Parsing and generation support both. The legacy seed rule ensures the first initials batch does not duplicate a legacy PHASE in the same `dependency-graph.md`. |
| `git worktree list` returns linked worktrees but one or more lack a `tasks/` directory | Silently skip that worktree. No error. |

## No-Block Invariant

**Absence of a `## Task Initials` section in `CLAUDE.md` never blocks, delays, or errors
any consuming skill.**

- When a skill cannot resolve initials (no flag, no section, derivation declined / not run),
  it proceeds without allocating an initials namespace. Legacy unprefixed task IDs remain
  valid and supported.
- This mirrors the no-block invariant of the language-resolution reference and follows the
  design principle that **configuration absence is a valid, predictable state**, not an
  error.
- A project can use task-ID namespacing immediately (via `--initials flag` or one-time
  `CLAUDE.md` section creation) or never (legacy mode indefinitely). Both are correct.
