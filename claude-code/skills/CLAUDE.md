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

## HTML Output Mode

Eight review and report skills (`ywc-impl-review`, `ywc-security-audit`,
`ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`,
`ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`) support an
opt-in `--format html` flag that emits a self-contained HTML report instead
of Markdown. The canonical convention — single-file rule, severity color
tokens, document structure, and the embedded `Copy as Markdown` surface — is
defined in `references/html-output.md`.

Rules for skills that adopt this mode:

- The default must stay `markdown`. HTML output costs 2–4× the output tokens,
  so it is opt-in, not a new default.
- Do not inline the HTML skeleton or conventions in a SKILL.md body — link
  `references/html-output.md` with a one-line pointer.
- Never apply HTML output to version-controlled canonical documents
  (`docs/specification/`, `tasks/`, CHANGELOG, the ubiquitous-language
  glossary) — HTML diff noise outweighs the benefit. Those skills do not
  expose `--format`.

When authoring a new review or report skill whose output a human reads to
make a decision, add the `--format` flag and the `html-output.md` pointer
following the eight skills above.
