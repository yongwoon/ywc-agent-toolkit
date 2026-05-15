# Skills Directory — Project Instructions

Guidance for authoring and maintaining the `ywc-*` Claude Code skills in this
directory. For repository-wide conventions, see the root `CLAUDE.md`.

## Subagent Return Payload Contract and Structured Surface-to-User

Skills that dispatch subagents via the Task tool (fan-out skills:
`ywc-code-gen`, `ywc-impl-review`, `ywc-parallel-executor`,
`ywc-sequential-executor`, `ywc-spec-validate`, `ywc-task-generator`) follow
two contracts defined in `references/subagent-status-actions.md`:

**Return payload** — every subagent prompt must include a directive
constraining the return to: `Status | 1-line summary | artifact paths |
(Concerns ≤ 10 lines | Blocker ≤ 5 lines | Missing-context bullets)`.
Generated code, full findings, full diffs, restated prompts, and
chain-of-thought go to files; only paths come back. Without this contract,
3+ verbose returns per fan-out phase saturate the orchestrator's main
context within one or two waves. See the **Return Payload Contract** section
of `references/subagent-status-actions.md`.

**Structured surface-to-user** — when BLOCKED Triage routes to "Plan
problem", the orchestrator surfaces with three required elements (attempted
triage steps + verbatim blocker + proposed default action), not as a bare
halt. Generic "halted, awaiting input" surfaces are a regression. See
**BLOCKED Triage** step 4 of `references/subagent-status-actions.md`.

New fan-out skills must link `references/subagent-status-actions.md` and
inject the Return Payload Contract directive verbatim into each subagent
prompt.
