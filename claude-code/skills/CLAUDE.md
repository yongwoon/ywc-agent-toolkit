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

## Sync-skip exceptions

The sync hook in `tools/scripts/sync-skills.sh` skips propagation of the following
skills because their implementations diverge across runtimes:

- `tools/codex-skill/skills:ywc-agentic/SKILL.md`
- `tools/pi-skills:ywc-agentic/SKILL.md`

Additionally, the codex-skill `ywc-code-gen` layer-role references diverge by
**filename** — codex-skill uses `*-generation.md` (`backend-generation.md` /
`frontend-generation.md` / `qa-generation.md`) where claude-code and pi-skills
use `*-agent.md`. The two sets are maintained independently, so the hook also
skips these (target, rel) pairs:

- `tools/codex-skill/skills:ywc-code-gen/references/backend-agent.md`
- `tools/codex-skill/skills:ywc-code-gen/references/frontend-agent.md`
- `tools/codex-skill/skills:ywc-code-gen/references/qa-agent.md`

Without these entries the sync loop copies claude-code's `*-agent.md` into
codex-skill, creating orphan files the codex `ywc-code-gen/SKILL.md` never
references (it links the `*-generation.md` set).

The hook MUST NOT propagate claude-code changes onto these paths. If a
future change to one of the four skills above needs to be cross-rooted
(e.g. a bug fix that applies to all three runtimes), apply it once in
each runtime's directory manually.
