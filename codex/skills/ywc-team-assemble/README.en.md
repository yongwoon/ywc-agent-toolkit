# ywc-team-assemble

Use this Codex skill when the user explicitly asks for a specialist team, subagent delegation, or parallel agent work.

## When to Use

- The user explicitly asks to assemble a team, delegate to agents, or run work in parallel.
- The work has at least two independent workstreams.
- Write scopes can be separated and the parent agent can review and synthesize the results.

Do not use it for simple questions, single-file edits, or strictly sequential work.

## Included Files

- `SKILL.md` — team assembly workflow
- `agents/openai.yaml` — Codex metadata
- `references/prompt-templates.md` — explorer, worker, and reviewer prompt templates
- `evals/evals.json` — role-isolation, Claim/Evidence, cap, and privacy contract evals

## Context Safety

Team prompts validate bounded Claims and cited evidence before projection. Independent reviewers receive scope and artifact paths only; dependent roles receive Claims and their cited artifacts only. Peer conclusions, recommendations, transcripts, raw content, uncited artifacts, and invalid or over-cap Claims are rejected.
