# Executable Gate Ledger for ywc-verify-done (Claude Code)

> Status: Draft
> Scale: Medium
> Created: 2026-09-17
> Author: Claude (ywc-plan)
> Spec Reference: Upstream implementation — `yongwoon/develop-with-llm` PR [#228](https://github.com/yongwoon/develop-with-llm/pull/228) (merged, includes one post-merge security-fix round). `develop-with-llm`'s own plan doc for the same feature: `docs/ywc-plans/20260824-verify-done-gate-ledger.md` in that repo.

## Global Constraints

- `claude-code/skills/CLAUDE.md` §"Authoring or Restructuring `ywc-*` Skills": modifying an existing skill's body structure (new section, new `references/` file) should invoke `ywc-skill-author` first, unless the edit is an "ad-hoc minor edit" following an existing pattern in the same directory. This port adds a new body section and a new `references/` file, which is more than a minor edit — Implementation Steps below route through `ywc-skill-author` for the SKILL.md edit.
- `claude-code/skills/CLAUDE.md` §"Writing Rules": `README.md` is Korean prose with English technical terms preserved (no transliteration); `SKILL.md`, `references/*.md`, and `scripts/*` are English-only, with the narrow exception of frontmatter `description` trigger phrases (not touched by this port).
- `claude-code/skills/CLAUDE.md` §"Bundled Execution Scripts": scripts under `<skill>/scripts/` execute without loading their body into LLM context, and any new script must be registered as a row in the shared table in `claude-code/skills/CLAUDE.md`.
- Upstream `gate-check.py` docstring: "Python 3 stdlib only (score-gate.py convention)" — this repo already has a precedent for this convention (`ywc-confidence-gate/scripts/score-gate.py`, confirmed stdlib-only during this plan's own Confidence Gate run). No new dependency is introduced.
- `codex/skills/ywc-verify-done/` and `plugins/ywc-agent-toolkit/skills/ywc-verify-done/` are out of scope for this port (see Out of Scope) — `plugins/ywc-agent-toolkit/` is generated from `codex/skills/` by `.githooks/pre-commit` / `scripts/sync-codex-plugin.sh` and must never be hand-edited directly (confirmed by reading `.githooks/pre-commit`, which errors if `plugins/ywc-agent-toolkit/skills/` is staged without a corresponding `codex/skills/` change).

## Purpose

`claude-code/skills/ywc-verify-done` currently gates completion claims through a prose-based 5-step Gate Function (IDENTIFY → RUN → READ → VERIFY → CLAIM) that the calling LLM executes and self-reports on. For the highest-stakes claims — multi-command verification, PR-ready claims, or a subagent-delivered artifact about to be merged — a prose gate has no mechanism to force independent, machine-checked confirmation that every required check actually ran and passed; the calling agent could still misreport or partially skip steps.

The sibling repository `develop-with-llm` (a project that co-develops the same `ywc-*` skill family and is regularly mined for skill improvements in this repo — see the four prior ports of its PR #220/#221/#225/#226/#227) already designed, implemented, security-hardened, and merged a deterministic answer to this gap: an **Executable Gate Ledger** — a caller-authored markdown ledger of `CHECK:`/`EXPECT:`/`EVIDENCE:` triples that a bundled `gate-check.py` script parses and mechanically executes, so a high-stakes completion claim can be backed by a machine-verified ledger instead of relying solely on the calling LLM's own diligence. Porting the already-reviewed, already-fixed final version into this repo closes an identical gap here, at much lower implementation risk than a fresh design (the two security defects the upstream PR's own review surfaced — a SIGTERM-ignoring descendant process surviving cleanup, and an unbounded EXPECT regex vulnerable to catastrophic backtracking — are already fixed in the version being ported).

## Scope

- Add `claude-code/skills/ywc-verify-done/scripts/gate-check.py` — verbatim port of the upstream final (post-security-fix) implementation, with only the two embedded repo-relative path examples in its docstring/help text adjusted from `tools/claude-code/skills/...` to this repo's `claude-code/skills/...`.
- Add `claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` — verbatim port of the upstream 24-case stdlib-only self-check, with the same path-string adjustment where it invokes `gate-check.py` by path.
- Add `claude-code/skills/ywc-verify-done/references/gate-ledger.md` — the ledger format spec, path-adjusted the same way. The upstream file's opening sentence references `external-repositories/unlazy/references/gates.md`, a path that does not exist in this repository — Implementation Steps below replace that sentence rather than porting a dead link.
- Add one `## Optional Escalation: Executable Gate Ledger` section to `claude-code/skills/ywc-verify-done/SKILL.md`, inserted after the existing `### Step 6: On failure, classify and route` subsection and before `## Integration` (this repo's current file has an identical Step 1–6 Workflow shape to upstream's pre-port version, confirmed by direct comparison in Existing Constraints Touched below).
- Add the two upstream **Common Mistakes** bullets ("Trusting an absence check without a positive control", "Copying a supplied number into the claim instead of recomputing it") to this repo's existing `## Common Mistakes` section.
- Add one row for `references/gate-ledger.md` to the existing `## References` table in `SKILL.md`.
- Register `gate-check.py` as a new row in `claude-code/skills/CLAUDE.md`'s `## Bundled Execution Scripts` table.
- Add one Korean paragraph to `claude-code/skills/ywc-verify-done/README.md` summarizing the optional escalation (mirroring upstream's own README addition, translated/adapted to this repo's existing README voice).

## Out of Scope

- **`codex/skills/ywc-verify-done/`** — explicitly excluded per the user's own instruction for this task ("Target: claude code 용 skill, agent"). `codex/skills/` and `claude-code/skills/` are documented as no-longer-auto-synced (`claude-code/skills/CLAUDE.md` §"Codex-skill: Maintained Independently"); porting to Codex is a deliberate follow-up decision for the user to make separately.
- **`plugins/ywc-agent-toolkit/skills/ywc-verify-done/`** — this directory is generated from `codex/skills/` by `scripts/sync-codex-plugin.sh` (invoked automatically by `.githooks/pre-commit` whenever `codex/skills/` changes) and is not a Claude Code artifact; hand-editing it is actively blocked by the pre-commit hook when `codex/skills/` isn't touched in the same commit. Since `codex/skills/` is itself out of scope, this directory does not change.
- **`docs/ywc-plans/20260824-verify-done-gate-ledger.md`-equivalent internal design doc** — not reproduced in this repo; this spec is the design record for the port. The upstream design doc is cited above as `Spec Reference` for anyone who wants the original rationale.
- **The upstream Claim Classification table's unrelated drift** — the upstream repo's current `SKILL.md` (as of this port) has since diverged further from the version PR #228 shipped: its "PR ready to merge" row now also mentions a `detect-bot-presence.sh` script (`... or detect-bot-presence.sh returned NO_BOTS ...`) that this repo does not have. That drift is from a later, unrelated upstream change, not part of PR #228's Gate Ledger feature — this port does not touch the Claim Classification table at all.
- **Localized README variants** (`README.en.md`, `README.ja.md`, `README.ko.md`) — the escalation summary is added only to the Korean-default `README.md`, matching the precedent set by prior small ports in this repo (`20260909-small_ywc-impl-review-verify-guardrail-port.md` etc. touch only the primary skill file, not every locale). Out of scope for translation follow-up unless the user requests it separately.
- **README.zh.md / README.es.md** (Tier 2, generated) — this skill's directory does not currently ship them (confirmed: `ls claude-code/skills/ywc-verify-done/` shows only the Tier-1 set), so none are added.
- **Any change to the existing 5-step prose Gate Function, Forbidden Vocabulary table, Rationalization Defense table, Claim Classification table, or Steps 1–6 Workflow** — the escalation is strictly additive and optional; Steps 1–6 remain the unchanged default path exactly as upstream's own PR description states ("Steps 1-6 unchanged").

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `claude-code/skills/ywc-verify-done/SKILL.md:113-145` (`## Workflow`, Steps 1–6) | Six numbered subsections ending at `### Step 6: On failure, classify and route` (line 135), immediately followed by `## Integration` (line 146). This repo's Step 1–6 titles and content are byte-for-byte structurally equivalent to upstream's pre-port version (same 6 step titles, same failure-routing table) — confirmed by direct read of both files. | New `## Optional Escalation: Executable Gate Ledger` section is inserted between the end of Step 6 (after line 145) and `## Integration` (line 146), matching upstream's exact insertion point relative to its own Step 6. |
| `claude-code/skills/ywc-verify-done/SKILL.md:165-173` (`## Common Mistakes`) | Five existing bullets ending with the `--skip-post-ci-check` bullet. | Two new bullets appended after the existing fifth bullet, verbatim from upstream (same wording, no repo-specific adjustment needed — they reference no upstream-only paths or scripts). |
| `claude-code/skills/ywc-verify-done/SKILL.md:175-183` (`## References` table) | Four existing rows (`forbidden-vocabulary.md`, `verification-block-examples.md`, `../references/subagent-status-actions.md`, `../references/pr-bot-polling.md`). | One new row added for `references/gate-ledger.md`, positioned as upstream did (second row, after `verification-block-examples.md`, before the two `../references/` shared-file rows). |
| `claude-code/skills/CLAUDE.md:325-352` (`## Bundled Execution Scripts` table) | Table of `Script \| Skill \| Purpose` rows, one per bundled script across all `ywc-*` skills; no `ywc-verify-done` row exists yet (confirmed via grep — zero matches for "verify-done" in this table). | One new row added, following the exact column format and using the upstream-confirmed exit-code semantics (0 = all runnable gates met / well-formed on `--status`; 1 = at least one unmet or malformed ledger), with the path corrected to this repo's `claude-code/skills/ywc-verify-done/scripts/gate-check.py` (the upstream PR's own review caught and fixed an equivalent path-prefix mistake in its first attempt at this exact table row — see commit `454d1f1` "fix: correct CLAUDE.md gate-check.py path to include tools/claude-code/skills prefix" in the upstream repo; this port must not repeat that mistake for this repo's own `claude-code/skills/` prefix). |
| `claude-code/skills/ywc-verify-done/README.md:1-39` | Existing Korean README with sections `## 무엇을 하나요`, `## 언제 trigger 되나요`, `## 언제 사용하지 않나요`, `## 참고`. | One new `## Optional: Executable Gate Ledger` section inserted after `## 무엇을 하나요` and before `## 언제 trigger 되나요`, matching upstream's own README insertion point relative to its equivalent sections. |
| `.githooks/pre-commit:20-24` | Errors if any path under `plugins/ywc-agent-toolkit/skills/` is staged without a corresponding `codex/skills/` change in the same commit. | This port stages zero files under `plugins/ywc-agent-toolkit/` or `codex/`, so the hook's guard condition (`package_files_changed == 0`) short-circuits to a no-op exit 0 before reaching the guard branch — confirmed by reading the script's control flow (line 17's `grep -qE '^(codex/skills/|...)'` against the staged-file set, which will be empty for this port's diff). |
| `scripts/validate.sh` (skill-structure check) | Requires `SKILL.md` with matching `name:`/`description:` frontmatter and the four Tier-1 README files per skill directory; does not require a `scripts/` directory or any particular script content. | This port's `scripts/gate-check.py` and `scripts/test_gate_check.py` additions are invisible to `validate.sh`'s checks (it does not enumerate `scripts/`); the SKILL.md frontmatter (`name:`/`description:`) is untouched by this port, so `validate.sh` continues to pass without modification. |

## Acceptance Criteria

The test seam for this feature is the pair of CLI entry points: `gate-check.py <ledger> [--status\|--reverify]` (public interface) and its own bundled `test_gate_check.py` self-check (the only automated verification this feature ships, per upstream's own "stdlib-only, assert-based, no test framework" design — there is no existing project test runner this script plugs into).

- [ ] **AC1 — Self-check passes**: When `python3 claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` is run after the port, system executes all 24 ported test cases against the ported `gate-check.py`, observable as stdout ending in `ALL PASS` and exit code `0`.
- [ ] **AC2 — `--status` mode is read-only**: When `gate-check.py --status <ledger.md>` is run against a ledger containing a runnable gate whose `CHECK:` would produce an observable side effect (e.g. writing a temp file), system executes zero `CHECK:` commands, observable as the side-effect file never being created and stdout listing the gate as its current (unexecuted) status.
- [ ] **AC3 — Default mode executes only unmet gates**: When `gate-check.py <ledger.md>` (no flag) is run against a ledger with one gate already carrying a valid cached-PASS `EVIDENCE:` (fingerprint matching current `CHECK`/`EXPECT` text) and one gate `pending`, system executes only the pending gate's `CHECK:`, observable as the cached-PASS gate's report line reading `PASS (skipped, fingerprint matched)` and exit code reflecting only the pending gate's outcome.
- [ ] **AC4 — `--reverify` forces re-execution**: When `gate-check.py --reverify <ledger.md>` is run against a ledger where a previously-passing gate's underlying command would now fail, system re-executes that gate regardless of its cached `EVIDENCE:`, observable as the ledger file's `EVIDENCE:` line being rewritten to `FAIL; ...` and exit code `1`.
- [ ] **AC5 — Malformed ledger fails closed**: When `gate-check.py <ledger.md>` (any mode) is run against a ledger containing a gate with exactly one of `CHECK:`/`EXPECT:` present, system refuses to execute anything, observable as stderr naming the offending gate id and the specific missing field, and exit code `1`.
- [ ] **AC6 — Manual gates never block exit 0**: When `gate-check.py <ledger.md>` is run against a ledger containing only manual gates (neither `CHECK:` nor `EXPECT:`), system reports each as `manual (skipped)`, observable as exit code `0` even though zero gates were mechanically verified.
- [ ] **AC7 — Registration is discoverable**: When `grep -n "gate-check.py" claude-code/skills/CLAUDE.md` is run after the port, system's Bundled Execution Scripts table contains exactly one row for `gate-check.py`, observable as a single grep match with a path that resolves from the repo root (`claude-code/skills/ywc-verify-done/scripts/gate-check.py`, verified by `test -f` on that literal path).
- [ ] **AC8 — SKILL.md structural validation still passes**: When `bash scripts/validate.sh` is run after the port, system reports no new errors for `ywc-verify-done`, observable as `Skill is valid!` (or equivalent zero-`ERROR` output) covering that skill directory.

## Functional Requirements

### FR-1: Verbatim script port with path adjustment only

`gate-check.py` and `test_gate_check.py` are copied from the upstream final (post-security-fix) version with no logic changes. The only text edits permitted are: (a) any embedded example invocation string that hardcodes the upstream repo-relative path `tools/claude-code/skills/ywc-verify-done/scripts/gate-check.py`, replaced with this repo's `claude-code/skills/ywc-verify-done/scripts/gate-check.py`; (b) the module docstring's reference to `docs/ywc-plans/20260824-verify-done-gate-ledger.md` — since that design doc is not reproduced in this repo (see Out of Scope), replace the docstring's pointer with a reference to this spec's path instead (`docs/ywc-plans/20260917-verify-done-gate-ledger-port.md`) or drop the sentence if it reads awkwardly standalone. No behavioral line (parsing, timeout, signal handling, regex bounding, fingerprinting) is altered. This preserves the two known-fixed security properties from upstream's own post-merge review round: `stop_process_group()` unconditionally sends `SIGKILL` to the whole process group after the grace period (not only on a `wait()` timeout, which would leave a SIGTERM-ignoring descendant alive), and `matches_expect()` bounds every regex `EXPECT:` match inside a 5-second-capped subprocess (never a thread, since `re.search` holds the GIL for the whole match and a thread cannot be interrupted mid-match).

### FR-2: SKILL.md optional-escalation section

Insert `## Optional Escalation: Executable Gate Ledger` (verbatim upstream prose, path-adjusted) between Step 6 and `## Integration`. The section must preserve upstream's explicit framing that this is **optional** and Steps 1–6 remain the unchanged default, name the three invocation modes with this repo's path, and repeat the security warning about `CHECK:` executing arbitrary shell commands with a pointer to `references/gate-ledger.md` for the full format spec.

### FR-3: Common Mistakes additions

Append upstream's two new `## Common Mistakes` bullets verbatim: "Trusting an absence check without a positive control" and "Copying a supplied number into the claim instead of recomputing it." Both are general verification-discipline principles independent of the ledger feature itself (they apply to the existing prose Gate Function too), which is why upstream placed them in Common Mistakes rather than gating them behind the new optional section.

### FR-4: references/gate-ledger.md port

Port the full ledger format spec (gate structure, runnable-vs-manual distinction, fenced-code-block skip behavior, modes and exit codes, bounds) verbatim except for: (a) the opening sentence's dangling reference to `external-repositories/unlazy/references/gates.md`, which does not exist in this repository and must be replaced with a self-contained sentence (e.g., drop the "narrowed subset of X" framing entirely, since this repo has no `unlazy` reference to narrow from); (b) the three example invocation lines' repo-relative path prefix, adjusted the same way as FR-1.

### FR-5: CLAUDE.md Bundled Execution Scripts registration

Add one row to `claude-code/skills/CLAUDE.md`'s `## Bundled Execution Scripts` table, following the existing table's column convention (`Script | Skill | Purpose`) and this repo's path (not upstream's `tools/`-prefixed path). Content: mode syntax (`[--status\|--reverify] <ledger>`), one-line purpose statement, and exit-code semantics — mirroring the level of detail every other row in that table already carries (e.g., the `poll-pr-reviews.sh` and `verify-transition.sh` rows document their exit codes inline).

### FR-6: README.md Korean summary

Add one `## Optional: Executable Gate Ledger` section to the Korean-default README, in the voice and format of the existing sections (short paragraph, Korean prose with English technical terms preserved per the `claude-code/skills/CLAUDE.md` locale rules), covering: what it's for, the three-mode invocation syntax pointer, and the shell-execution security warning. Positioned after `## 무엇을 하나요`, matching upstream's own placement relative to its equivalent sections.

### FR-7: Skill-authoring discipline compliance

Before finalizing the SKILL.md edit (FR-2, FR-3), invoke `ywc-skill-author` per `claude-code/skills/CLAUDE.md`'s "Authoring or Restructuring `ywc-*` Skills" rule, since this port adds a new body section and a new `references/` file (not a typo-fix or link-correction-scale edit that would qualify for the "ad-hoc minor edit" exemption). This is a process requirement on the implementer, not a new user-facing behavior — included here as an FR so it survives task decomposition as a checked step rather than being silently skipped.

## Quality Gate Contract

N/A — no quality gate contract (this project has no CRAP/mutation-score gate infrastructure; confirmed no `docs/quality-gates/` or equivalent exists in this repo).

## Module Boundaries

N/A — no new module boundary. `gate-check.py` is a standalone CLI script (its own file, its own `if __name__ == "__main__":` entry point), not a library imported by other code in this repository; its "public interface" is fully described by the three CLI invocation modes already documented in Scope/FR-2/FR-5, not by a Python API.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Security | See Critical Surfaces below — `CHECK:` lines execute arbitrary shell with the invoking user's own permissions; there is no allowlist/approval layer, by upstream's own explicit design choice, ported unchanged. |
| Reliability | Per-gate 120-second timeout with guaranteed process-group `SIGKILL` after grace period (not just top-level-shell reap); 64 KB combined stdout+stderr cap per gate, streamed incrementally rather than buffered in full; `EXPECT:` regex matching bounded to 5 seconds in a separate process to survive a catastrophic-backtracking pattern. All three properties are inherited unchanged from the ported implementation (FR-1) — this port introduces no new reliability requirement, it preserves an existing one. |
| Portability | POSIX process-group semantics (`os.killpg`, `start_new_session=True`) are used when `os.name == "posix"`; a `process.terminate()`/`process.kill()` fallback exists for non-POSIX, ported unchanged. Not independently re-verified on Windows as part of this port (upstream did not claim Windows CI coverage either). |

## Critical Surfaces

- **`gate-check.py`'s `CHECK:` field execution (`run_check()`, `subprocess.Popen(gate.check, shell=True, ...)`)** — this is the single most security-relevant surface in this port: any ledger file passed to `gate-check.py` has every one of its `CHECK:` lines executed as shell with the invoking user's full permissions, with no allowlist, sandboxing, or human-approval gate. This is why `references/gate-ledger.md` (FR-4) must carry forward the explicit "read every `CHECK:` line before running a ledger you did not author yourself" warning verbatim, and why `SKILL.md`'s new section (FR-2) repeats the warning rather than only linking to it once.

## Data Model

N/A — no data model change. The "ledger" is a caller-supplied markdown file on disk, not a database table; its format is fully specified in FR-4 / `references/gate-ledger.md`.

## API Contract

N/A — no API contract change. `gate-check.py`'s three-mode CLI surface is documented in Scope/FR-2/FR-5 rather than as an HTTP contract.

## Edge Cases

All of the following are properties of the ported implementation (FR-1) and are exercised by the ported self-check (AC1); they are listed here so a reviewer can confirm each one survives the port unmodified, not because this port introduces new edge-case handling:

- **Ledger contains a fenced code-block example of the gate syntax**: the parser's fence-toggle state machine (`if body.strip().startswith("```")`) skips everything between fence markers, so documentation examples inside the ledger are never parsed as live gates. An odd number of fence-toggle lines (unclosed at EOF) is treated as implicitly closed — not an error.
- **A gate's `EVIDENCE:` line is stale after its `CHECK`/`EXPECT` text was edited**: the SHA-256 fingerprint embedded in a cached-PASS `EVIDENCE:` line no longer matches the gate's current `CHECK`/`EXPECT` bytes, so `evidence_is_cached_pass()` returns `False` and the gate is re-executed even under the non-`--reverify` default mode.
- **`CHECK:` command exceeds the 120-second timeout**: `stop_process_group()` sends `SIGTERM` to the whole process group, waits up to 0.5s, then sends `SIGKILL` to the group unconditionally (not conditionally on whether the top-level shell already exited) — this guards specifically against a backgrounded grandchild process that ignores `SIGTERM` while the top-level shell reaps normally.
- **`CHECK:` command produces output exceeding 64 KB**: capture stops at the cap, the gate fails closed with `EVIDENCE: FAIL; exit=output_limit; ...` — never silently matches `EXPECT:` against a truncated slice that happens to contain the pattern.
- **`EXPECT:` is a regex with catastrophic-backtracking potential**: the match runs in a separate `multiprocessing.Process` (not a thread — `re.search` holds the GIL for the whole match duration, so a thread timeout could not actually interrupt it) capped at 5 seconds; a hang is treated as no-match, not an indefinite block.
- **`EXPECT:` regex uses an unsupported flag letter** (e.g. upstream's JS-only `g`/`u`/`y`, or any letter outside `i`/`m`/`s`): rejected as a parse error at `--status` time, before any `CHECK:` is ever run.
- **A gate id is empty or duplicated**: both are parse errors that fail the whole ledger closed (`errors.append(...)`), never silently ignoring the malformed gate and proceeding with the rest.
- **Ledger file uses CRLF line endings**: `write_evidence()` preserves each line's original terminator (`split_line()` captures `\r\n`/`\r`/`\n` per line) when rewriting an `EVIDENCE:` line in place, so a Windows-authored ledger is not silently converted to LF.
- **Two invocations run concurrently against the same ledger file**: unsupported and undocumented, ported unchanged from upstream (`references/gate-ledger.md` FR-4: "this is a single-session local tool, not a multi-tenant orchestration primitive"). Not a new gap introduced by this port — flagged here explicitly so a reader of this spec sees the constraint without having to open the ported reference file to find it.

## Dependencies

N/A — no external dependencies. Both `gate-check.py` and `test_gate_check.py` use only the Python 3 standard library (`argparse`, `hashlib`, `json`, `os`, `re`, `selectors`, `signal`, `multiprocessing`, `subprocess`, `sys`, `time`, `dataclasses`, `pathlib`), matching this repo's existing `score-gate.py` convention.

## Open Questions

N/A — none identified. This is a verbatim/near-verbatim port of an already-designed, already-implemented, already-security-reviewed-and-fixed upstream feature into a structurally identical sibling skill file; no design decision in this spec is left open for the implementer.

## References

- Upstream PR: [`yongwoon/develop-with-llm#228`](https://github.com/yongwoon/develop-with-llm/pull/228) — "feat: ywc-verify-done Executable Gate Ledger 검증 기능 추가"
- Upstream design doc (not reproduced in this repo): `docs/ywc-plans/20260824-verify-done-gate-ledger.md` in `develop-with-llm`
- This repo's precedent for the same "mine develop-with-llm PRs for skill improvements" pattern: `docs/ywc-plans/20260909-small_ywc-impl-review-verify-guardrail-port.md`, `20260902-small_port-pr225-alternatives-trade-offs.md`, `20260902-small_port-pr220-project-scaffold-enrichment.md`, `20260909-codex-mine-review-history-pr226-port.md`

## Confidence Gate

```text
Confidence Gate Report
──────────────────────
Aggregate: 93/100 — PROCEED

  Scope clarity:           95   Six-file change list is enumerated exactly (Scope), with an explicit Out-of-Scope list naming codex/plugins and why.
  Architecture compliance: 92   Follows this repo's own documented Bundled Execution Scripts + references/ pattern; no new pattern introduced.
  Evidence quality:        95   Primary source read directly — final post-review-fix gate-check.py (431 lines), test_gate_check.py (419 lines, 24 tests), gate-ledger.md, and this repo's current SKILL.md/README.md, not inferred from the PR description alone.
  Reuse verified:          90   The feature IS a reuse of an already-built, already-hardened implementation rather than net-new design; no alternative library search was needed since the upstream script matches this repo's stdlib-only score-gate.py convention.
  Root cause identified:   90   Gap confirmed via grep (zero existing gate-ledger references in this skill) before concluding a port was warranted, not assumed from the PR title alone.
```

No dimension ≤ 70; no advisor dispatch triggered. Proceeding directly to handoff.

## Amendment Log

### Iteration 1 — 2026-09-17

**Driven by**: ywc-spec-validate DONE_WITH_CONCERNS, gate 91/100 PROCEED band, 1/1/1 (Critical/Warning/Suggestion) findings
**Signatures**: `code-compatibility:existing-constraints-touched-stale-line-citation`, `completeness:edge-cases-omits-concurrent-invocation-constraint`

| Section edited | What changed | Why |
|---|---|---|
| `## Existing Constraints Touched` | Corrected the `claude-code/skills/CLAUDE.md` Bundled Execution Scripts table citation from `255-273` to `325-352` | The cited range did not match the actual file (verified via `grep -n "^## Bundled Execution Scripts"`, which returned line 325, with the table body running to line 352) |
| `## Edge Cases` | Added one bullet stating concurrent invocation against the same ledger file is unsupported/undocumented, ported unchanged from upstream | The constraint exists in the ported `references/gate-ledger.md` (FR-4) but was not visible in this spec's own Edge Cases list, leaving a reader unaware of it without opening the ported file |

Duplicate-claim sweep: grepped the whole document for `255-273` and `325-352` — the corrected citation appeared in exactly one location (`## Existing Constraints Touched`), no other site needed reconciliation.
