# 000053-020-refactor-agentic-autonomy-trigger — Implementation Checklist

## Prerequisites

- [ ] Read both target `SKILL.md`, locale READMEs, and Codex `agents/openai.yaml` before edits.

## Allowed Edit Scope

- [ ] Only `claude-code/skills/ywc-agentic/**` and `codex/skills/ywc-agentic/**`.

## Stop Conditions

- [ ] Stop if trigger scope requires workflow/argument changes.
- [ ] Stop if an anti-trigger cannot target a real sibling skill.
- [ ] Stop if requested wording spills into other skills, plugins, hooks, or root scripts.

## Hardening Gate

- [ ] Classify: behavior change / Skill-definition maintenance.
- [ ] Named exception: paired representative prompt routing replaces runtime tests.
- [ ] Record explicit lifecycle input, existing orchestration output, and sibling routes.
- [ ] Require manual multilingual false-positive/false-negative review.

## Implementation Steps

- [ ] Narrow Claude Code description/README activation wording.
  - [ ] Preserve multilingual explicit autonomy phrases and add generic-plan/direct-change anti-triggers.
  - [ ] Keep `/ywc-*` invocation syntax in Claude-facing examples.
- [ ] Mirror the boundary in Codex.
  - [ ] Keep only `name` and `description` frontmatter.
  - [ ] Keep `$ywc-*` syntax in Codex-facing examples and synchronize UI metadata if needed.
- [ ] Update locale README explanation without changing workflow behavior.
- [ ] Review explicit-autonomy, generic-plan, and direct-change prompts; run both validators.

## Task Verify

- [ ] `rg -n 'autonomous|end-to-end|자율|Do not use for|ywc-plan' claude-code/skills/ywc-agentic/SKILL.md codex/skills/ywc-agentic/SKILL.md`
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/ywc-agentic && bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-agentic`
- [ ] `rg -n '\$ywc-' claude-code/skills/ywc-agentic && exit 1 || true`

## Verification

- [ ] `bash scripts/validate.sh` after both Phase 000053 tasks integrate.
- [ ] Diff remains in declared `ywc-agentic` directories.
- [ ] No `ywc-agentic` body workflow or argument contract changed.
