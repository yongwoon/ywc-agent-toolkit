# Retrospective Skill (ywc-retro)

> **User-invoked skill** — run it directly with `/ywc-retro`. The model does not route to it automatically (`disable-model-invocation: true`), and other skills cannot call it through the Skill tool.

> **Agent dependency** — the lenses and synthesizer run on the read-only `ywc-retro-lens` agent (Read / Grep / Glob only). Install it with `bash scripts/install.sh --cc-agents ywc-retro-lens`; without it the skill falls back to a single pass.

A Claude Code Skill that reviews a coding session and proposes, ranked by severity (High / Medium / Low), improvements to the **environment** — navigation pointers, automated checks, coding standards, steering files, tooling, information access — so the Agent works better from the next run on. Based on `retro` from `mattpocock/skills`.

## Overview

- Reads the session's primary sources (conversation, tool calls) directly and cites evidence
- Collects candidates in seven categories: Navigation / Automated checks / Coding standards / Steering files / Tool economy / No-ops / Information access
- Three lens subagents (judgment / tooling / divergent, `sonnet`) collect candidates in parallel, and a clean-context synthesizer (`opus`) filters them with rejection reasons — this avoids the self-review bias of the parent session under review, at the cost of four subagent runs per invocation
- **Mechanical violations become checks, not rules**: fixed-pattern, banned-API, and import-shape violations are proposed as a lint rule, pre-commit hook, or CI job; only judgement calls become a written standard
- A repo with neither a pre-commit hook nor CI is itself reported as a finding
- Credentials, tokens, and personal data are replaced with `<REDACTED>` before results are shown
- Proposes only, applies nothing — the user decides what to adopt

## Usage

```text
/ywc-retro
/ywc-retro the session that ran ywc-agentic yesterday
```

## Options Reference

- **Invocation**: `/ywc-retro`
- **Input**: target session (defaults to the current session)

No flags.

## Related Skills

- `ywc-skill-author` — follow-up for candidates caused by a skill instruction, and the source of the Writing Levers the retro applies
- `ywc-review-learnings` — accumulates project-level review preferences
- `ywc-incident-postmortem` — production incident retrospectives (this skill reviews an Agent session)
