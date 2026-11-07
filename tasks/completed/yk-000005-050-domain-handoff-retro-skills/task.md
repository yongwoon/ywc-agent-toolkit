# yk-000005-050-domain-handoff-retro-skills — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000005-040-domain-merge-dependabot-workflow` is completed (merged)
- [ ] `yk-000005-020-domain-user-invoked-skills` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-handoff/**`
  - `claude-code/skills/ywc-retro/**`
  - `claude-code/skills/CLAUDE.md`
  - `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md`
  - `CLAUDE.md`
  - `README.md`
  - `README.ja.md`
  - `README.ko.md`
  - `README.zh.md`
  - `README.es.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Port `ywc-handoff`**
  - [ ] Create `SKILL.md` from the final snapshot with the draft → **Redact** → **Save outside the workspace** order, `mktemp` exclusive create, `0600` check, slug rule, State status tags (`[unverified]` + reason)
  - [ ] Write four READMEs from the snapshot `README.md` (ko), adding the user-invoked blockquote; remove the `ywc-wayfinder` mention
- [ ] **Port `ywc-retro`**
  - [ ] Create `SKILL.md` (High/Medium/Low) and the four lens/synthesizer references
  - [ ] Keep the `Action required … Release … TaskStop` callout and shared async-monitoring links; remove the `tune description` and absent-skill references
- [ ] **Normalize and validate names**
  - [ ] Normalize `tools/claude-code/skills/` prefixes; run the AC14c `ywc-*` existence loop; confirm no `ScheduleWakeup(`
- [ ] **Register the skills**
  - [ ] Add both to the `claude-code/skills/CLAUDE.md` Consumers list and the `cross-skill-graph.md` Standalone list ('user-invoked')
- [ ] **Update the six count sites**
  - [ ] Change 49 → 51 at the six listed lines; leave the generated plugin README alone
- [ ] **Gate**
  - [ ] Run `bash scripts/validate.sh` and `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`; stage the updated baseline

## Acceptance Coverage
Covers: AC12 (4 skills), AC14, AC14b, AC14c

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `for s in ywc-handoff ywc-retro; do for f in SKILL.md README.md README.en.md README.ja.md README.ko.md; do test -f claude-code/skills/$s/$f || exit 1; done; done`
- [ ] `for f in judgment-lens tooling-lens divergent-lens synthesizer; do test -f claude-code/skills/ywc-retro/references/$f.md || exit 1; done`
- [ ] `[ "$(ls -d claude-code/skills/ywc-*/ | wc -l | tr -d ' ')" = 51 ]`
- [ ] `[ "$(grep -l '^disable-model-invocation: true' claude-code/skills/*/SKILL.md | wc -l | tr -d ' ')" = 4 ]`
- [ ] `grep -q mktemp claude-code/skills/ywc-handoff/SKILL.md && grep -q 0600 claude-code/skills/ywc-handoff/SKILL.md && grep -q unverified claude-code/skills/ywc-handoff/SKILL.md`
- [ ] `python3 -c "L=open('claude-code/skills/ywc-handoff/SKILL.md',encoding='utf-8').read().splitlines(); r=next(i for i,l in enumerate(L) if '**Redact**' in l); s=next(i for i,l in enumerate(L) if '**Save outside the workspace**' in l); assert r<s"`
- [ ] `[ "$(grep -rn 'ywc-architecture-invariants\|ywc-wayfinder\|ywc-agent-legibility-audit' claude-code/skills/ywc-retro claude-code/skills/ywc-handoff | wc -l | tr -d ' ')" = 0 ]`
- [ ] `for n in $(grep -rhoE 'ywc-[a-z]+(-[a-z]+)*' claude-code/skills/ywc-retro claude-code/skills/ywc-handoff | sort -u); do test -e claude-code/skills/$n || test -e claude-code/agents/$n.md || { echo missing $n; exit 1; }; done`
- [ ] `[ "$(grep -c 'ywc-handoff\|ywc-retro' claude-code/skills/ywc-skill-author/references/cross-skill-graph.md | tr -d ' ')" -ge 2 ]`
- [ ] `[ "$(grep -rn 'ScheduleWakeup(' claude-code/skills/ywc-handoff claude-code/skills/ywc-retro | wc -l | tr -d ' ')" = 0 ]`
- [ ] `for f in CLAUDE.md README.md README.ja.md README.ko.md README.zh.md README.es.md; do grep -q '51' $f || exit 1; done` (and the original count-site lines no longer contain 49)
- [ ] `bash scripts/validate.sh` (includes `tests/named_agent_release_test.py`)
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-handoff/SKILL.md claude-code/skills/ywc-retro/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->

- T0 snapshot has no README for either skill; the Korean README base was read in place from the installed bundle `~/.claude/skills/ywc-{handoff,retro}/README.md` (installed bundle, commit unpinned). Blockquote replaced with the local B3 form; handoff `관련 Skill` (only `ywc-wayfinder`) dropped.
- FR3: handoff Integration `Pairs with: ywc-wayfinder` removed; retro Integration drops `ywc-agent-legibility-audit`, `ywc-architecture-invariants`, `tune description` mode; lens Owner examples `tools/claude-code/` → `claude-code/`; synthesizer Owner confinement `tools/` → `claude-code/`, `visible, not invoked` now routes Owner to `ywc-skill-author` as a description fix (no `tune description` mode locally).
- Descriptions folded to one line per A16.
- Security tests (stdlib, offline): `ywc-handoff/tests/test_handoff_safety.py` (step order, redact surfaces, save clauses, and executes the prescribed `mktemp` template: mode 0600, new file per run, planted symlink not followed) and `ywc-retro/tests/test_retro_safety.py` (executes the scratchpad block with TMPDIR inside a repo, and the perl redaction block on a secrets fixture). Not registered in `scripts/validate.sh` (outside Ownership).
- RED evidence: both tests exit 1 before SKILL.md existed. Mutation runs (each restored, diff-verified): swap Redact/Save lines → `draft < redact < save order` FAIL; predictable `: >` redirect → mktemp template FAIL; drop 0600 check → FAIL; drop `userinfo` → FAIL; drop `sk-` lookbehind → `benign task- word kept` FAIL; drop eof `$pem = 0` reset → `PEM state reset per file` FAIL; drop email pattern → FAIL; drop inside-repo fallback → `scratchpad created` FAIL.
