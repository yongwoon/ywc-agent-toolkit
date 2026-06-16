# ywc-onboard-repo

A 4-phase (Reconnaissance → Architecture → Conventions → Generate) skill for entering an existing or unfamiliar repository. It emits an Onboarding Guide to the conversation and writes a Starter AGENTS.md to the repo root, enhancing any existing AGENTS.md in place. It is **not** a scaffolder — `ywc-project-scaffold` is the inverse direction. Reconnaissance is Glob + Grep only to keep token cost bounded.

## Localized Versions

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## When to Use

- The user says "onboard me", "walk me through this repo", "help me understand this codebase"
- Setting up Codex in a project for the first time (generates the Starter AGENTS.md)
- A subagent runner needs an AGENTS.md before delegating implementation

## How to Invoke

```bash
$ywc-onboard-repo --scope apps/web/
```

Or in natural language:

> "onboard me to this repo"
> "generate an AGENTS.md from the existing conventions"

## The Iron Law

1. **Reconnaissance uses Glob + Grep only** — Read is reserved for ambiguous signals surfaced by later phases
2. **Conventions verified from source code win over conventions inferred from config**
3. **Existing AGENTS.md is enhanced in place** — never overwritten

## Inputs

- (optional) `--scope <dir>` — limit reconnaissance to a workspace (useful in monorepos)
- (optional) `--guide-only` — emit the Onboarding Guide, skip AGENTS.md
- (optional) `--agents-md-only` — write the AGENTS.md, skip the Guide
- (optional) `--enhance` — force the enhancement path even when no AGENTS.md exists yet

## Outputs

- **Output A**: Onboarding Guide (printed Markdown) — Tech Stack, Architecture, Key Entry Points, Directory Map, Request Lifecycle, Conventions, Common Tasks, Where to Look, Detection Confidence
- **Output B**: Starter AGENTS.md (written to repo root) — if an AGENTS.md exists, only the `## Detected Conventions (<YYYY-MM-DD>)` section is appended

## Related Skills

- `ywc-project-scaffold` — inverse direction (creates a new repo); never invoke both in one session
- `ywc-refactor-clean` — downstream when reconnaissance reveals significant dead-code accumulation
- `ywc-impl-review` — the generated Onboarding Guide anchors a cold reviewer
- `ywc-plan` — Phase 2's Request Lifecycle is the architectural anchor consumed by plan Step 2
- `ywc-verify-done` — vocabulary rules for the final "Wrote AGENTS.md" claim
