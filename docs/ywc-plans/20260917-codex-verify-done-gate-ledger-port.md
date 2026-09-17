# Spec: Port PR #228's Executable Gate Ledger into Codex `ywc-verify-done`

> Status: Draft
> Scale: Medium
> Created: 2026-09-17
> Source: [develop-with-llm PR #228](https://github.com/yongwoon/develop-with-llm/pull/228)
> Confidence Gate: 96/100 — PROCEED (Scope 96 / Architecture 95 / Evidence 98 / Reuse 95 / Root cause 96)
> Spec Reference: N/A — standalone Codex-skill enhancement

## Global Constraints

- “Codex skills live under `codex/skills/` in a flat `codex/skills/<skill-name>/` structure.” (`codex/AGENTS.md:7`)
- “For Codex skills, `codex/skills/` is the source of truth. The marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from it by `bash scripts/sync-codex-plugin.sh`; do not edit the generated package first.” (`codex/AGENTS.md:12`)
- “Codex `SKILL.md` frontmatter must contain only those two fields; do not copy Claude-only fields such as `version`, `category`, or `requires`.” (`AGENTS.md:20`)
- “Treat `bash scripts/validate.sh` as the required pre-PR test.” (`AGENTS.md:24`)
- Existing Tier 2 `README.zh.md` and `README.es.md` files must remain maintained alongside the required Tier 1 README set for this changed skill. (`AGENTS.md:5,24`)

## Purpose

PR #228 adds an optional executable ledger for high-stakes completion claims: it records each check, expected result, and freshly derived evidence in one reviewable Markdown artifact. The current Codex `ywc-verify-done` has the same prose-only fresh-evidence gate but no deterministic, repeatable multi-command mechanism. Porting the final PR behavior fills that gap without making ordinary, single-command verification heavier.

## Outcome Oracle

- **Target:** `ywc-verify-done` offers an optional Markdown Gate Ledger and a stdlib-only checker for multi-command and accepted-subagent-artifact claims; it can contribute fast, repeatable PR-readiness evidence but does not replace the separately required PR polling/health proof. Ordinary verification-block workflow remains unchanged.
- **Quality threshold:** `--status` is read-only and exits 0 for a syntactically valid ledger regardless of PENDING state; normal mode only resumes uncached gates; `--reverify` is the only checker mode accepted as fresh evidence for a runnable-ledger claim; malformed ledgers fail closed.
- **Evidence required:** Hermetic assertion tests cover parsing, execution, evidence caching/invalidation, rewrites, invalid input, timeout/output caps, fence handling, regex behavior, and POSIX process cleanup. Source/package validation and temporary-CODEX_HOME installation pass.
- **Stop condition:** Do not hand off to task generation until `ywc-spec-validate` reports no Critical or Warning findings and the generated marketplace copy is fresh.

## Scope

- Add a Codex-local, optional Gate Ledger grammar and operational reference to `ywc-verify-done`.
- Add a Python 3 standard-library checker and self-contained executable test suite beneath the skill.
- Update the `ywc-verify-done` instruction contract, eval fixture, and all maintained localized README summaries to teach the safety boundary and the distinction between resume and fresh re-verification.
- Synchronize the generated marketplace skill after editing its source.

## Out of Scope

- Claude Code skill sources, the upstream `develop-with-llm` repository, and any cross-bundle sync: PR #228 is evidence, not a source tree to edit.
- New `codex/agents/*.toml` custom agents or changes to `codex/agents/README.md`: a ledger is a skill runtime utility, not a new delegation role.
- Changing `codex/skills/ywc-verify-done/agents/openai.yaml`: its display name and default prompt remain accurate; inspect it during verification but do not make a cosmetic change.
- Making a ledger mandatory for simple or single-command claims, auto-creating ledgers in upstream callers, approval enforcement, sandboxing arbitrary `CHECK` commands, concurrent ledger writes, or changing the canonical five-step Gate Function.
- Changing the existing Claim Classification table: PR #228's ledger escalation is additive. The current PR-ready row and its independently required `poll-pr-reviews.sh --verify` head-SHA freshness gate remain authoritative.
- Root release/version/changelog changes unless a separate release request requires them.

## Quality Gate Contract

N/A — no project-owned complexity or mutation quality-gate contract applies. The checker must be tested with its hermetic self-check; repository structural, contract-eval, installation, package-sync, and validation gates apply.

## Module Boundaries

| Module | Owned public interface | Consumers | Allowed dependencies | Forbidden dependencies |
| --- | --- | --- | --- | --- |
| `codex/skills/ywc-verify-done/SKILL.md` | Optional ledger workflow: `--status <ledger>`, `<ledger>`, `--reverify <ledger>`; completion-claim policy | Codex users and existing upstream skill callers | Local reference and checker | Automatic caller rewrites or weakened fresh-evidence rule |
| `scripts/gate-check.py` | `python3 gate-check.py [--status | --reverify] <ledger.md>`; status exits 0 for valid parsing and execution exits 0 only when all runnable gates pass | Skill users; self-check | Python 3 stdlib; caller shell for explicit checks | Third-party libraries, network policy, approval/sandbox claims, concurrent-write coordination |
| `references/gate-ledger.md` | Ledger grammar, cache/evidence format, execution safety limits | Skill instructions and ledger authors | Checker behavior | A second, divergent parser contract |
| `evals/evals.json` and README locales | Discoverability and prompt-level behavior contract | Skill selection and validation | Existing eval/README conventions | Runtime implementation ownership |
| `plugins/ywc-agent-toolkit/skills/ywc-verify-done/` | Generated distribution mirror | Marketplace installation | `scripts/sync-codex-plugin.sh` only | Hand editing |

## Existing Constraints Touched

| Existing artifact | Behavior (verified) | New code's interaction |
| --- | --- | --- |
| `codex/skills/ywc-verify-done/SKILL.md:20-38` | The Iron Law requires current-message fresh evidence and the Gate Function orders IDENTIFY → RUN → READ → VERIFY → CLAIM. | Add an optional escalation after the workflow; only `--reverify`, not cached/bare execution, is ledger fresh evidence. |
| `codex/skills/ywc-verify-done/SKILL.md:70-85` | Claim Classification maps multi-command and PR-ready claims to explicit evidence. | Leave the table unchanged; the optional ledger section adds a reusable evidence mechanism without replacing current requirements. |
| `codex/skills/ywc-verify-done/SKILL.md:109-140` | Existing workflow ends in failure classification and routing. | Insert the optional ledger section without renumbering or altering Steps 1–6. |
| `codex/skills/ywc-verify-done/evals/evals.json:1-22` | Three descriptive fixtures cover fresh execution, forbidden wording, and independent subagent verification. | Retain all three and add a ledger-specific fixture; no runner change. |
| `codex/skills/ywc-verify-done/agents/openai.yaml:1-4` | UI metadata accurately invokes fresh verification before a completion claim. | Validate it remains structurally valid; no semantic change is needed. |
| `scripts/run-codex-skill-contract-evals.sh:35-67,86-92` | Skill eval JSON files are recursively discovered and schema-checked. | Add a normal fixture only; do not add a one-off runner branch. |
| `scripts/sync-codex-plugin.sh:47-84` | Source skills copy into the marketplace package and copied file modes are retained. | Add executable source scripts, then regenerate the package once; never edit its copy directly. |
| `scripts/validate.sh:300-369` | Validation builds an isolated synced package, diffs it against the tracked package, and compares executable file modes; it also rejects unsafe workspace-relative `bash`, `python`, or `cp` paths in package docs. | Use its existing package-freshness/mode oracle rather than add a duplicate check. |
| `codex/skills/references/pr-bot-polling.md:17-38`; `codex/skills/scripts/poll-pr-reviews.sh:35-56` | PR-ready flow requires a poll allowed at least 600 seconds and a separate `--verify` that rejects a stale `head_ref_oid`. | Keep this prerequisite outside a 120-second ledger CHECK and state its fresh evidence must accompany any PR-ready claim. |

## Acceptance Criteria

- [ ] **AC1 — Read-only inspection:** `gate-check.py --status <ledger>` prints each gate’s ID, CHECK, EXPECT, and state, starts no subprocess, and leaves bytes unchanged; a self-check proves this with a side-effect sentinel and before/after bytes.
- [ ] **AC2 — Honest result:** A runnable gate is PASS only when CHECK exits 0 and combined output matches EXPECT. Either failed condition reports named FAIL and exits 1.
- [ ] **AC3 — Fail-closed grammar:** Missing ledger, zero gates, duplicate ID, only one of CHECK/EXPECT, empty CHECK/EXPECT, unsupported regex flag, and invalid regex produce specific nonzero diagnostics before any CHECK starts. A gate with neither field is MANUAL; duplicate fields follow the final upstream parser's last-field-wins behavior and must be covered by a regression assertion.
- [ ] **AC4 — Freshness:** Bare execution runs only runnable gates lacking a valid cached-PASS string: `PASS; exit=0; fingerprint=sha256:<64 lowercase hex>; decisive=<JSON string>`. The SHA-256 input is UTF-8 `CHECK` value bytes, one NUL byte, then UTF-8 `EXPECT` value bytes. Missing, malformed, wrong-fingerprint, or non-string JSON `decisive` is PENDING, not a cache hit. `--reverify` runs every runnable gate and can replace stale PASS evidence with FAIL.
- [ ] **AC5 — Evidence integrity:** Executed gates rewrite the final effective EVIDENCE line in place; when none exists, they insert directly after the final effective EXPECT line, without reordering unrelated content and while retaining LF/CRLF. A PASS uses the AC4 one-line form; a FAIL is `FAIL; exit=<integer|124|125>; decisive=<JSON string>`, where `124` is timeout and `125` is output cap. `--status` exits 0 after valid parsing even with PENDING/FAIL evidence and exits nonzero only for absent/malformed input.
- [ ] **AC6 — Bounded execution:** Each CHECK uses `shell=True`, a 120-second and 64-KiB combined-output limit, and fails on timeout/output cap. POSIX cleanup kills the complete process group including SIGTERM-ignoring descendants. Regex matching runs in a separate process with `EXPECT_TIMEOUT_SECONDS = 5`; the self-check may copy the script and replace named module constants to exercise timeout behavior without weakening production limits.
- [ ] **AC7 — Instruction boundary:** Documentation gives exact CLI/grammar, arbitrary-shell warning, status/resume/reverify semantics, MANUAL semantics, positive-control rule for absence checks, and independent recomputation rule while retaining the default workflow.
- [ ] **AC8 — Distribution and agent boundary:** All six existing README locales describe optional ledger use; `agents/openai.yaml` stays valid and unchanged; no custom-agent TOML changes occur; synchronized marketplace files and executable modes match source.
- [ ] **AC9 — Verification:** The self-check, contract-eval validator, temporary Codex-only install/list smoke test that executes all three installed-path modes, and `bash scripts/validate.sh` pass. The latter's isolated sync/diff/mode checks are the source/package freshness oracle.

## Functional Requirements

### FR-1: Ledger grammar and parser

Create `references/gate-ledger.md` and implement its only grammar in `scripts/gate-check.py`:

```markdown
- [ ] G1: full suite passes
  CHECK: bash scripts/validate.sh
  EXPECT: Skill is valid!
  EVIDENCE: pending
```

The port preserves the final upstream parser exactly: a header is `-` + optional whitespace + `[<one character>]` + optional whitespace + non-empty text before the first `:`; its trimmed pre-colon text is the ID. Until the next valid header, a line matching `^(\s*)(CHECK|EXPECT|EVIDENCE):( ?)(.*)$` belongs to that gate; field values are single-line, the optional single space after `:` is removed, and repeated fields use the last matching line. Other/intervening lines and multiline continuations are inert. A non-regex EXPECT is a literal substring; `/pattern/flags` supports only `i`, `m`, and `s`. Triple-backtick fences, including tagged fences, toggle documentation skipping; an unterminated fence closes at EOF. Fingerprints use the unmodified parsed CHECK and EXPECT values encoded as UTF-8, separated by one NUL; they never include field indentation or line terminators.

### FR-2: Modes, cache, and rewrite

Implement mutually exclusive `--status` / `--reverify` flags and one positional ledger path. `--status` only parses/reports and succeeds for a syntactically valid ledger even when a gate is PENDING or its recorded evidence is FAIL. Default execution is recovery-only: it skips only the exact AC4 PASS cache for unchanged CHECK+EXPECT. `--reverify` executes all runnable gates and is mandatory before a high-stakes runnable-ledger or accepted-subagent-artifact claim. For PR-ready, it is at most one evidence component: the existing ≥600-second poll, `--verify` head-SHA gate, CI, and PR-health evidence remain fresh and separate.

Serialize PASS/FAIL evidence on one line with exit result and JSON-safe decisive output. The final matching field is the effective field: replace the final effective EVIDENCE line, or insert after the final effective EXPECT line if EVIDENCE is absent. CHECK failure uses its integer process exit; timeout serializes `124`; output cap serializes `125`. Retain unrelated text and the input line-ending convention. Manual gates are never written. Do not claim concurrent-write safety.

### FR-3: Execution hardening

Run explicit CHECK text through Python 3 stdlib `subprocess.Popen(..., shell=True)`, collecting combined stdout/stderr only to 64 KiB and failing at the 120-second deadline or cap. Overflow output must not satisfy EXPECT. On POSIX use `start_new_session=True` and terminate then kill the complete process group on timeout/cap. Run regex matching in a separate `multiprocessing.Process` and kill it after the named five-second constant because Python `re` can block on catastrophic backtracking. The self-check copies source then replaces the named 120-second constant with one second for timeout/process-group fixtures. The checker is not a sandbox: documentation must require inspection of every inherited CHECK before execution.

### FR-4: Skill, eval, metadata, and locales

Extend `SKILL.md` additively after Step 6 with “Gate Ledger Escalation (Optional)”; retain existing six step numbers and the normal verification-block workflow. Add the upstream Common Mistakes about positive controls and recomputing supplied counts. Do not modify Claim Classification: the current PR-ready row already delegates to the shared polling/health contract, whose `--verify` checks `head_ref_oid` freshness.

Add one focused eval while retaining existing IDs/scenarios. All user-facing Skill/README/reference CLI examples use the installed form `python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" [--status|--reverify] <ledger>`; source tests resolve the sibling script with `Path(__file__)`, never a repository-relative help example. Update `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, and `README.es.md` with localized optional-ledger usage and the untrusted-CHECK warning. Leave `agents/openai.yaml` byte-identical unless validation finds its existing prompt inaccurate; do not add or modify custom agents.

### FR-5: Tests and package flow

Add stdlib-only `scripts/test_gate_check.py`, runnable directly by `python3`. Cover status read-only behavior and valid-ledger exit semantics, successful exact cache/fingerprint, reverify/invalidation, CHECK and EXPECT failures, literal/flagged regex, malformed input, repeated-field last-wins parsing and rewrite position, manual/fenced content, CRLF retention, output cap (`exit=125`), fingerprint byte distinctions, timeout (`exit=124`), POSIX SIGTERM-ignoring descendants, and catastrophic regex boundedness. Run `bash scripts/sync-codex-plugin.sh` only after source edits complete, then install into a temporary `CODEX_HOME` and execute each installed CLI mode.

## Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Security | Fail closed for malformed input; disclose arbitrary shell execution; bound time, output, descendants, and regex work. |
| Compatibility | Python 3 stdlib only; preserve skill frontmatter/metadata conventions; add no custom agent. |
| Maintainability | One grammar reference shared by docs and code; explicit cache/evidence format. |
| Distribution | Source-first marketplace sync retains executable files and all maintained locales. |

## Data Model / API Contract

N/A — no database or HTTP API. Stable CLI:

```text
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" --status <ledger.md>
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" <ledger.md>
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" --reverify <ledger.md>
```

For `--status`, exit 0 means valid parsing only; it does not claim runnable gates passed. For bare and `--reverify` execution, exit 0 means all runnable gates passed; manual gates are skipped. Exit nonzero means malformed/missing ledger or at least one runnable failure. A caller must separately prove any manual high-stakes prerequisite and any PR-ready prerequisite outside the ledger.

## Edge Cases

- A manual-only ledger exits 0 and reports skipped gates, including under `--reverify`; it cannot prove a human-only prerequisite.
- Changed CHECK or EXPECT invalidates a prior PASS and runs in bare mode; only reverify can replace a stale PASS with FAIL when the command environment changed.
- A PR-ready claim keeps the mandated 600-second poll and its independently fresh `--verify` artifact outside this 120-second checker; a ledger cannot substitute for that wait gate.
- A matching output with nonzero exit, or exit 0 without an EXPECT match, is FAIL.
- Fenced examples never become live gates; missing EVIDENCE inserts without changing unrelated LF/CRLF content.
- Timeout, output overflow, or malformed/empty decisive match never becomes PASS; cleanup must not leave a background descendant alive.

## Dependencies

- Python 3 standard library.
- Existing `scripts/sync-codex-plugin.sh`, `scripts/run-codex-skill-contract-evals.sh`, and `scripts/validate.sh`.
- N/A — no third-party library, service, database, or new Codex custom agent.

## Open Questions

N/A — none identified. The final state of merged PR #228, current polling artifact verification, and the installed-skill distribution rules resolve the port shape.

## Blind Spot Pass

- **Current approach:** Port final PR #228 checker as an optional per-skill utility and leave normal verification blocks unchanged.
- **Assumption most likely to break it:** A source-tree CLI example or a 120-second CHECK could be mistaken for a valid installed/PR-poll invocation.
- **Repo evidence:** `sync-codex-plugin.sh` does not rewrite `python3` source paths, while `validate.sh` already rebuilds/diffs a package; `poll-pr-reviews.sh --verify` records and checks `head_ref_oid` but its poll requires ≥600 seconds.
- **Action:** Use installed-path examples exclusively, run all three modes after temporary installation, rely on `validate.sh` for package freshness, and keep polling outside the ledger.

## Self-Consistency Pass

- **Pass A:** AC1–AC6 map to FR1–FR3; AC7–AC8 map to FR4; AC9 maps to FR5. Status semantics, cache syntax, path form, and PR-poll boundary agree across AC/FR/API/Edge Cases. No HTTP or data-model contract exists.
- **Pass B:** Existing skill, eval, metadata, validation, and package-sync paths are cited above. “No custom agent change” is scoped to this feature, not a claim that the catalog is empty.
- **Pass C:** N/A — no schema, database relation, migration, or persistence change.

## References

- [develop-with-llm PR #228](https://github.com/yongwoon/develop-with-llm/pull/228)
- `codex/skills/ywc-verify-done/SKILL.md`
- `codex/AGENTS.md`
- `AGENTS.md`

## Amendment Log

### Iteration 1 — 2026-09-17

Driven by: `ywc-spec-ready` iteration 1 validation (`DONE_WITH_CONCERNS`: 0 Critical, 7 Warning).

Signatures: `completeness:ledger-parser-and-evidence-contract`, `consistency:pr-poll-timeout-boundary`, `consistency:status-exit-semantics`, `feasibility:installed-cli-path`, `feasibility:package-freshness-oracle`

| Section edited | What changed | Why |
| --- | --- | --- |
| Outcome Oracle, Scope, Existing Constraints Touched | Separated ledger re-verification from the existing ≥600-second PR polling gate; cited local package and polling evidence. | The earlier wording implied the 120-second checker itself could prove PR readiness. |
| Acceptance Criteria, FR-1, FR-2, Data Model / API Contract | Defined final upstream header/field parsing, SHA-256 cache bytes, PASS/FAIL serialization, status exit behavior, and installed command form. | The prior contract allowed incompatible parsers/caches and an invalid installed path. |
| FR-3, FR-5, Edge Cases | Named shell invocation, production/test timeout constants, five-second regex deadline, process cleanup, repeated-field tests, and independent PR polling. | The former requirements were not fully testable and did not resolve long-poll behavior. |
| FR-4, Open Questions, Blind Spot Pass, Self-Consistency Pass | Removed unrelated Claim Classification expansion; made installed package and polling integration explicit. | Current local polling already owns `head_ref_oid` freshness, so changing the table would expand scope beyond PR #228. |
| Module Boundaries, Existing Constraints Touched | Reconciled the repeated exit-status and Claim Classification statements with the amended canonical contract. | Duplicate-claim sweep found two stale summary phrases after the targeted amendment. |

### Iteration 2 — 2026-09-17

Driven by: `ywc-spec-ready` re-validation (`DONE_WITH_CONCERNS`: 0 Critical, 2 Warning).

Signatures: `completeness:failure-exit-serialization`, `completeness:repeated-field-rewrite-anchor`

| Section edited | What changed | Why |
| --- | --- | --- |
| Acceptance Criteria, FR-2, FR-5 | Defined timeout/output-cap exit values (124/125), final-effective-field rewrite anchor, and exact regression coverage. | The first amendment left non-process failure serialization and repeated-field placement ambiguous. |
