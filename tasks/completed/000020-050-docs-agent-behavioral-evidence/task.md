# Task: Agent Behavioral Evidence Strategy

## Summary

Add or document an A8 behavioral evidence strategy for Codex custom agents, bounded to read-only smoke/eval fixtures.

## Implementation Steps

- [ ] Review current agent rubric and agent TOML files.
  - Related AC/FR: AC5, FR-5
  - Contract / Behavior Change: Evidence strategy must align with A8 and the actual custom agent roles.
  - Verification Command / Evidence: Read `agent-rubric.md` and inspect `codex/agents/*.toml`.
- [ ] Define the fixture shape or limitation.
  - Related AC/FR: AC5, FR-5
  - Contract / Behavior Change: Fixtures must be bounded prompts that do not require write access, app execution, external services, or network.
  - Verification Command / Evidence: Create or update `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md`, or record why a reference is unnecessary.
- [ ] Update the 2026-06-18 report A8 evidence section.
  - Related AC/FR: AC5, FR-5
  - Contract / Behavior Change: The report must state whether A8 improves, remains at 3, or is deferred pending harness work.
  - Verification Command / Evidence: `rg -n "A8|behavioral evidence|smoke|fixture|harness" docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- [ ] Avoid unsupported TOML edits.
  - Related AC/FR: AC5, FR-5
  - Contract / Behavior Change: Do not edit `codex/agents/*.toml` unless the evidence review finds a narrow wording defect independent of new harness work.
  - Verification Command / Evidence: `git diff -- codex/agents`

## Task Verify

```bash
test -f docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
rg -n "A8|behavioral evidence|smoke|fixture|harness|read-only" docs/skill-agent-eval/codex/2026-06-18-full-sweep.md tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md
git diff -- docs/skill-agent-eval/codex/2026-06-18-full-sweep.md tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md codex/agents
```

Expected Passing Signal:

- A8 path is explicit: either a concrete bounded fixture strategy exists or the report documents why A8 remains evidence-limited.
- No unsupported agent TOML behavior changes appear.

Pre-change Failing Evidence / Exception:

- The existing eval status is A8 evidence-limited because no agent smoke fixture/harness evidence is recorded.

Contract/Test Evidence:

- Evidence strategy is read-only and does not require external services.

## Out of Scope

- Building a new harness.
- Editing scorer rubric behavior.
