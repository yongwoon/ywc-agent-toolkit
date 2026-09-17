# Read-Only Agent Inline-Return Contract Fix

> Status: Draft
> Scale: Medium
> Created: 2026-09-17
> Author: Claude (ywc-plan)
> Spec Reference: https://github.com/yongwoon/develop-with-llm/pull/234 (analogous fix in a sibling project; ported here to this project's `claude-code/agents/*.md` + `scripts/validate.sh` structure instead of that project's `tools:` / `validate_ywc_agents.py`)

## Global Constraints

- Documentation is Korean, code/identifiers are English (`/Users/yongwoon.kim/Desktop/yongwoon/source/private/CLAUDE.md` §Language Conventions) — this repo's own `CLAUDE.md` and agent bodies are predominantly English prose describing agent behavior for the model, matching the existing convention of the 7 files being edited; no new user-facing text is introduced.
- `plugins/ywc-agent-toolkit` is generated from `codex/skills` only, never hand-edited (`.githooks/pre-commit`) — not touched by this change since it has no `agents/` mirror.
- `scripts/validate.sh` mirrors `.github/workflows/validate.yml` and must stay runnable via `bash scripts/validate.sh` (CLAUDE.md `Key Commands`).

## Purpose

Seven read-only Claude Code agents (`tools:` omits `Write`) instruct the caller, in three separate places in each agent's own body, to "write analysis to a file under the caller's artifact directory" — an action the agent cannot perform. The pointer these agents give to the shared contract doc (`§3.5` of `subagent-status-actions.md`) is also a dead link: that section does not exist. All 12 agents in this project reference `§3.5`, not only the 7 read-only ones — fixing the dead link (FR-2) repairs it project-wide, while the write-to-file contradiction (FR-1) is specific to the 7 read-only agents. This is the exact defect class documented in PR #234 of the sibling `develop-with-llm` project ("read-only reviewer agent stall": an agent with no terminal move because it can neither write the artifact it was told to write, nor return findings inline because the contract said to write instead). This project's installer-side counterpart from that PR (shared `references/`/`scripts/` sync) is already fixed here (`scripts/install.sh:154-162`), but this contradiction was never ported.

## Scope

- Fix the self-contradictory "write to a file" instruction in all 7 read-only agents by replacing it with an explicit inline-return instruction, in every place it appears (Success Criteria bullet, Return Contract paragraph, Anti-patterns table row):
  `ywc-architect`, `ywc-go-reviewer`, `ywc-performance-engineer`, `ywc-python-reviewer`, `ywc-root-cause-analyst`, `ywc-security-engineer`, `ywc-typescript-reviewer`
- Add a "Read-only review-worker exception" subsection to `claude-code/skills/references/subagent-status-actions.md`, giving it an addressable `§3.5` anchor (fixing the dead link) and defining the bounded inline payload shape.
- Add a mechanical validator check to `scripts/validate.sh` that fails CI if any Claude Code agent whose `tools:` list omits `Write` lacks the inline-return qualifier inside its own `## Return Contract` section.

## Out of Scope

- Codex mirror (`codex/agents/*.toml`) — already correct; each read-only Codex agent's `developer_instructions` already ends with "Do not create artifact files ... return the compact verdict" (verified in `codex/agents/ywc-architect.toml`), so PR #234's Codex-side fix does not apply here.
- `plugins/ywc-agent-toolkit` — generated from `codex/skills` only; has no `agents/` directory to touch.
- Any change to agent `tools:` grants themselves (no agent gains or loses `Write`).
- Porting PR #234's installer shared-asset-sync fix — already present in this repo (`scripts/install.sh` `install_cc_support_dirs`/`install_codex_support_dirs`).
- Introducing a standalone Python validator script (`validate_ywc_agents.py`) — this project's convention is bash checks inside `scripts/validate.sh`; the new check is added there instead, per the user's explicit instruction to adapt to this project's structure.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `claude-code/agents/ywc-architect.md:104-106` (and the same 3-line pointer block, same relative path, in the other 6 agents) | Points readers to `../skills/references/subagent-status-actions.md` §3.5 for the "generic" status payload format | Extend: add the missing `§3.5` heading to the target file; the existing pointer becomes valid without being edited |
| `claude-code/agents/ywc-architect.md:80-82`, `:119-121`, `:132` (Success Criteria / Return Contract / Anti-patterns; equivalent line ranges in the other 6 files per the grep table in Functional Requirements) | Instructs writing full analysis "to a file under the caller's artifact directory" | Override: replace with inline-return instruction referencing the new §3.5 exception |
| `scripts/validate.sh:518-540` `check_agent_file()` | Validates `name:`/`description:` frontmatter only; no `tools:`/body cross-check exists | Extend: add a new check invoked from `check_agent_file()` (or a sibling function called alongside it from `check_cc_agents()` at `scripts/validate.sh:741-760`) |
| `scripts/validate.sh:769-771` `check_cc_agents` dispatch | Already loops `claude-code/agents/ywc-*.md` and calls `check_agent_file "$file"` per file | Reuse: no new loop needed, the new check hooks into the existing per-file loop |

## Acceptance Criteria

- [ ] **AC1 — No agent instructs an impossible write**: For each of the 7 agents (`ywc-architect`, `ywc-go-reviewer`, `ywc-performance-engineer`, `ywc-python-reviewer`, `ywc-root-cause-analyst`, `ywc-security-engineer`, `ywc-typescript-reviewer`), `grep -n "goes to a file\|Write the .* to a file\|file under the.*artifact directory" claude-code/agents/<name>.md` returns zero matches.
- [ ] **AC2 — §3.5 exists and is addressable**: `grep -n "^### " claude-code/skills/references/subagent-status-actions.md` (or `^##`, matching whatever heading depth is used) shows a heading whose numbering or anchor text resolves as `§3.5` under `## Return Payload Contract`, and it defines a payload shape covering Status/Summary/Concerns/Blocker/Missing-context (mirroring the canonical shape in the same file's existing table), explicitly omitting only `Artifacts`.
- [ ] **AC3 — Validator catches a regression**: Running `bash scripts/validate.sh` against the fixed tree exits 0 for the agents section. Manually reintroducing the phrase "goes to a file under the caller's artifact directory" inside any one read-only agent's `## Return Contract` section and re-running `bash scripts/validate.sh` produces a non-zero `ERRORS` count with a message naming that agent file.
- [ ] **AC4 — Write-capable agents unaffected**: `bash scripts/validate.sh` still passes for the 6 agents that hold `Write` (`ywc-backend-coder`, `ywc-cloud-engineer`, `ywc-doc-writer`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-refactor-cleaner`) — the new check must not fire for them.

## Functional Requirements

### FR-1: Rewrite the 3 contradicting sites in each of the 7 read-only agents

For each agent file, three sites currently instruct "write to a file" and must be rewritten to say the payload returns inline per the new §3.5 exception. Exact current line numbers (subject to shift once earlier edits land in the same file — re-`grep` before each edit rather than trusting these numbers across a multi-edit session):

| File | Success Criteria bullet | Return Contract paragraph | Anti-patterns row |
|---|---|---|---|
| `ywc-architect.md` | 80-82 | 119-121 | 132 |
| `ywc-go-reviewer.md` | 185-186 | 231 | 246 |
| `ywc-performance-engineer.md` | 194-195 | 230 | 246 |
| `ywc-python-reviewer.md` | 169 | 214-215 | 229 |
| `ywc-root-cause-analyst.md` | 113 | 141-142 | 157 |
| `ywc-security-engineer.md` | 90 | 141 | 153 |
| `ywc-typescript-reviewer.md` | 128 | 170-171 | 185 |

Replacement wording per site (adapt the agent-specific noun phrase — "trade-off matrix", "goroutine-theory", "findings dump", etc. — already present at each site; only the write-to-file clause changes):

- **Success Criteria bullet**: `... stays under 300 words; supporting analysis returns inline, bounded, per the read-only review-worker exception (§3.5) — never to a file.`
- **Return Contract paragraph**: `Full analysis (<agent-specific list>) returns inline, bounded, per the read-only review-worker exception in [claude-code/skills/references/subagent-status-actions.md](../skills/references/subagent-status-actions.md) §3.5; only status, 1-line summary, verdict/findings, and severity counts return.`
- **Anti-patterns row** (`Avoid` column): `Return the bounded inline payload per §3.5 — never write to a file; this agent holds no Write tool.`

### FR-2: Add the "Read-only review-worker exception" subsection to `subagent-status-actions.md`

`claude-code/skills/references/subagent-status-actions.md`'s 4 existing top-level headings (`## Status Responses`, `## Return Payload Contract`, `## BLOCKED Triage`, `## Aggregating Status`, confirmed via `grep -n "^##"`) carry **no numbers at all** — "§3.5" is not a position in an actual numbering scheme, it is a **literal fixed label** that all 12 `claude-code/agents/ywc-*.md` files (not only the 7 read-only ones — confirmed via `grep -rn "§3.5" claude-code/agents/`) and `claude-code/agents/CLAUDE.md:126` already hardcode verbatim as the canonical pointer text. The fix is to make that literal string resolve to a real heading, not to introduce or imply a renumbering of the file's other 4 headings — those stay exactly as they are.

Insert a new subsection immediately under `## Return Payload Contract` (after its existing table and `MUST NOT` list), headed literally `### 3.5. Read-only review-worker exception`. Content: state that agents whose `tools:` grant omits `Write` return the full canonical payload (Status, Summary, Concerns, Blocker, Missing context) inline in the response text, never to a file, and that `Artifacts` is the only canonical field legitimately omitted (no file exists to point to). Include one bounded example payload showing all of Status/Summary/Findings-or-verdict/Concerns/Blocker/Missing-context so a `BLOCKED` or `NEEDS_CONTEXT` return from one of these agents is not missing fields §4 (BLOCKED Triage) depends on. As a side effect, this also repairs the dead `§3.5` link for the 5 write-capable agents that reference it (`ywc-backend-coder`, `ywc-cloud-engineer`, `ywc-doc-writer`, `ywc-frontend-coder`, `ywc-refactor-cleaner`) — no change to those files is needed, since their pointer text already says "§3.5" verbatim.

### FR-3: Add validator Rule to `scripts/validate.sh`

Add a new bash function, e.g. `check_agent_readonly_return_contract()`, called from `check_agent_file()` (or from `check_cc_agents()` right after the existing `check_agent_file "$file"` call at `scripts/validate.sh:757-760`) with the same `$file` argument. Logic:

1. Read the `tools:` frontmatter line (`sed -n 's/^tools:[[:space:]]*//p' "$file" | head -n1`). If it's absent or doesn't look like a `[...]` list, skip (that malformed-frontmatter case is a pre-existing concern of `check_agent_file`, not this rule's job to invent).
2. If the `tools:` list contains `Write` (word-boundary match, not a substring hit on `Rewrite`/`WriteXyz`), skip — the rule only applies to read-only agents.
3. Otherwise, extract the `## Return Contract` section body (from the `## Return Contract` heading to the next `^## ` heading or EOF — same extraction idiom used for other section-scoped checks already in this file, e.g. `check_codex_agent_file`'s field checks).
4. Within that extracted section only, require a match for a qualifier regex, e.g. `returns? inline|read-only review-worker exception`. If absent, emit `ERROR: agents/<base>.md is a read-only agent (no Write tool) but its Return Contract section does not carry the inline-return qualifier` and increment `ERRORS`.

Scope the search to the `## Return Contract` section specifically (not the whole file body) so a stray mention elsewhere doesn't produce a false pass — this mirrors the exact fix PR #234 applied to its own Rule 8 after discovering the initial whole-body search let mismatched files through.

## Non-Functional Requirements

N/A — no performance/scalability/security-boundary change; this is a documentation/prompt-contract correction plus a CI text-matching check.

## Critical Surfaces

N/A — no critical surface. The changed files are agent prompt bodies and a validation script; no auth, payment, secret-handling, or PII-adjacent code is touched.

## Module Boundaries

N/A — no new module; edits are confined to existing agent Markdown bodies, one shared reference doc, and one existing validator script.

## Quality Gate Contract

N/A — no quality gate contract; this repository's CI is `scripts/validate.sh` / `.github/workflows/validate.yml` structural checks, not CRAP/mutation gates, and this change extends that same mechanism.

## Data Model

N/A — no data model change.

## API Contract

N/A — no API contract change.

## Edge Cases

- **A future 8th read-only agent is added without the qualifier**: FR-3's validator check fires automatically since it scans every `claude-code/agents/ywc-*.md` file via the existing `check_cc_agents` loop — no per-agent allowlist to maintain.
- **An agent's `tools:` list is malformed** (e.g., `tools: Write` as a bare string, not a list): out of scope for this change; `check_agent_file`'s existing frontmatter checks do not currently validate `tools:` shape at all, and inventing that is a separate concern from the inline-return contradiction. The new check's step 1 skip-on-malformed behavior means such a file is silently not checked by this rule, same as today.
- **The qualifier phrase appears outside `## Return Contract`** (e.g., only in Boundaries or Success Criteria, not in the Return Contract section itself): the validator must not treat this as passing — step 3/4 of FR-3 scope the search specifically to `## Return Contract`, so Success Criteria/Anti-patterns fixes in FR-1 are necessary for AC1 but the *validator* only asserts the Return Contract site, matching PR #234's final (not initial) Rule 8 scoping decision.

## Dependencies

N/A — no external dependencies; uses only existing bash/grep/sed already used throughout `scripts/validate.sh`.

## Open Questions

N/A — none identified.

## References

- https://github.com/yongwoon/develop-with-llm/pull/234 — sibling project's postmortem-driven fix for the same defect class (installer shared-asset sync, already ported/present here; read-only agent Write-tool contradiction, the subject of this spec)
- `claude-code/skills/references/subagent-status-actions.md` — target of the new §3.5 subsection
- `scripts/validate.sh` — target of the new validator check

## Amendment Log

### Iteration 1 — 2026-09-17

**Driven by**: DONE_WITH_CONCERNS, gate not re-scored (no design change), 0/1/1 findings
**Signatures**: `consistency:fr2-heading-numbering-scheme-not-actual`

| Section edited | What changed | Why |
|---|---|---|
| `## Purpose` | Added one sentence noting all 12 agents (not just the 7 read-only ones) hardcode `§3.5`, and that FR-2 repairs the dead link project-wide while FR-1 stays scoped to the 7 read-only agents | n/a — additive |
| `### FR-2: ...` | Replaced the "file's current heading order §1/§2/§3..." renumbering justification with a grep-confirmed statement that the file's 4 existing headings carry no numbers at all and that `§3.5` is a literal fixed label to add, not a position to renumber into; also noted the 5 write-capable agents whose dead link this incidentally repairs | Original text: "making it addressable as §3.5 given the file's current heading order: §1 Status Responses, §2 Return Payload Contract ... §3 would be the next top-level concept" — this implied a numbering scheme the file does not actually have, risking unnecessary renumbering of the other 3 headings during implementation |
