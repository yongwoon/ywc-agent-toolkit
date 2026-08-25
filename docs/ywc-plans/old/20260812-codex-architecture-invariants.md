# Codex Architecture Invariants

> Status: Draft
> Scale: Large
> Created: 2026-08-12
> Author: Codex
> Spec Reference: PR #206의 architecture-invariants 제안 및 현재 Codex bundle 검토

> **Operative Sections:** The original specification applies except where
> `## Iteration 1 Amendments — Spec-readiness validation` refines it. In particular,
> that amendment's Sections A–E govern v1 execution, schemas, audit results,
> consumer propagation, run evidence, and verification.

## Global Constraints

- 변경 대상은 Codex bundle의 skills, references, custom agents뿐이다.
- architecture contract는 optional이다. manifest가 없다는 사실만으로 generation, task generation, review를 실패시키지 않는다.
- verifier 실행 권한은 repository manifest가 아니라 user-controlled ignored local configuration에서만 얻는다.
- v1은 Python standard library만 사용한다. 따라서 manifest는 JSON 파일이며 arbitrary YAML parser dependency를 추가하지 않는다.
- LLM verdict는 configured verifier와 bounded edge evidence를 보완할 수 있지만, 그 evidence를 대체하거나 만들어내지 않는다.

## Purpose

프로젝트가 선언한 component boundary와 allowed/forbidden dependency를 Codex skill과 `ywc-architect`가 동일한 contract로 이해하게 한다. 이 contract는 no-manifest workflow를 깨지 않으면서도, 신뢰되지 않은 PR content가 verifier command를 실행시키는 위험과 evidence 없이 architecture violation을 단정하는 문제를 막는다.

## Scope

- `ywc-architecture-invariants` skill, JSON schema validator, safe verifier registry reference를 새로 추가한다.
- `ywc-code-gen`, `ywc-task-generator`, `ywc-impl-review`, `ywc-architect`가 optional contract evidence를 소비하도록 한다.
- contract state와 sanitized verifier result를 agentic run evidence에 기록할 수 있게 한다.
- normal/boundary/non-use eval과 isolated install validation을 추가한다.

## Out of Scope

- TypeScript, Python 등의 import-graph adapter를 v1 bundle에 포함하는 일.
- manifest에 shell command를 저장하거나 agent가 PR의 command text를 실행하는 일.
- `ywc-agent-legibility-audit`의 D6 추가. 현재 Codex bundle에 해당 skill이 없으므로 별도 feature로 다룬다.
- Mermaid visualization을 CI authority로 만들거나 자동 생성하는 일.

## Existing Constraints Touched

| Existing artifact | Verified behavior | Required interaction |
|---|---|---|
| `codex/agents/ywc-architect.toml:12` | architect는 bounded evidence만 다루고, evidence가 부족하면 `NEEDS_CONTEXT`를 반환한다. | invariant packet과 verdict fields를 이 discipline에 맞춰 추가한다. |
| `codex/skills/ywc-impl-review/SKILL.md:124` | Architecture worker는 bounded diff와 project evidence로 review한다. | verifier output은 primary evidence로 제공하되, output 부재를 violation으로 바꾸지 않는다. |
| `codex/skills/ywc-code-gen/SKILL.md:112` | worker는 bounded prompt packet을 받는다. | impacted components/rules만 packet에 넣는다. |
| `codex/skills/ywc-task-generator/SKILL.md:45` | task preview와 non-interactive contracts가 존재한다. | component ownership 및 affected rules를 task metadata에 추가한다. |

## Acceptance Criteria

- [ ] **AC1 — Contract validity:** repository-root `architecture-invariants.json`이 v1 schema를 통과할 때만 contract로 사용된다. malformed, duplicate id, dangling endpoint, invalid glob, invalid policy는 `NEEDS_CONTEXT`다.
- [ ] **AC2 — No arbitrary execution:** manifest는 verifier id만 참조한다. local registry에 등록되지 않은 verifier, shell string, interpolated arguments, timeout/working-directory policy 위반은 실행하지 않고 `NEEDS_CONTEXT`다.
- [ ] **AC3 — Evidence-bound audit:** `MAINTAINED` 또는 `VIOLATED`는 normalized edge evidence가 있을 때만 반환된다. changed path mapping만 있는 경우는 `N/A` 또는 `NEEDS_CONTEXT`다.
- [ ] **AC4 — No-manifest fallback:** manifest가 없고 caller가 `--manifest`를 주지 않으면 consumers는 현재 behavior를 보존하고 contract state를 `N/A — no architecture contract`로 기록한다.
- [ ] **AC5 — Consumer propagation:** manifest가 유효하면 generation/task/review packet은 affected component ids, rule ids, contract state, sanitized evidence path만 전달한다.
- [ ] **AC6 — Architect verdict:** `ywc-architect`가 `MAINTAINED`, `VIOLATED`, `N/A`, `NEEDS_CONTEXT` 중 하나를 rule/evidence/next action과 함께 300 words 이내에 반환한다.
- [ ] **AC7 — Safe run evidence:** verifier id, command digest, exit code, sanitized evidence artifact만 기록하고 raw command/output, transcript, source, full diff는 거부한다.
- [ ] **AC8 — Distribution quality:** new skill/agent metadata, focused evals, bundle validation, isolated install smoke가 통과한다.

## Functional Requirements

### FR-1: Canonical manifest and schema

> ⚠️ SUPERSEDED by Iteration 1 — see §iteration-1-amendments--spec-readiness-validation.

v1 manifest location은 repository root의 `architecture-invariants.json`이다. JSON을 선택한 이유는 isolated install에서 Python standard-library `json`으로 deterministic parse를 보장하기 위해서다.

Required fields:

- `version`: integer `1`
- `components`: unique kebab-case `id`, one-or-more repository-relative `paths`, non-empty `owner`
- `rules`: unique kebab-case `id`, defined `source` and `target`, `policy` (`allow` or `forbid`), non-empty `rationale`
- `enforcement`: `advisory` or `enforced`
- `owner`: non-empty contract owner
- optional `verifier`: one kebab-case `id` only

No self-edge, duplicate ID, outside-root path/glob, or multi-component mapping is silently accepted. A changed path matching zero or more than one non-shared component produces an ambiguous mapping. A component may explicitly set `shared: true`; shared matches are reported as context but do not decide an edge by themselves.

### FR-2: Trusted local verifier registry

> ⚠️ SUPERSEDED by Iteration 1 — see §iteration-1-amendments--spec-readiness-validation.

The manifest never contains executable text. A verifier id resolves only in ignored `.codex/settings.local.json` at `ywcArchitectureInvariants.verifiers.<id>`.

Each registry entry requires:

- `argv`: non-empty array of literal executable and arguments; no shell, variable expansion, command substitution, or caller-provided interpolation
- `cwd`: repository root only
- `timeout_seconds`: integer from 1 through 60
- `network`: `false` for v1
- `output_path`: optional repository-relative path where the verifier writes normalized evidence

`enforced` contract requires a registered safe verifier. `advisory` contract can omit one. The runner uses an empty/minimal environment, does not print raw stdout/stderr, and records only the sanitized result defined in FR-5. A runtime that cannot enforce these controls returns `NEEDS_CONTEXT` rather than executing.

### FR-3: Normalized edge evidence and audit modes

> ⚠️ SUPERSEDED by Iteration 1 — see §iteration-1-amendments--spec-readiness-validation.

`ywc-architecture-invariants` provides `--mode draft|audit|validate`.

- `draft` performs bounded reconnaissance and writes a schema-valid manifest only at a caller-approved repository-relative path.
- `audit` accepts a bounded changed-path scope and either a normalized evidence artifact or safe verifier result. Evidence entries identify `source_component`, `target_component`, `evidence_path`, and optional line. It evaluates only direct declared edges; it does not infer imports/calls from prose or paths.
- `validate` validates schema and runs a safe registered verifier when configured. It validates the normalized evidence schema before consuming it.

| Mode | Allowed terminal result |
|---|---|
| draft | `DONE`, `NEEDS_CONTEXT`, `BLOCKED` |
| audit with mapped evidence | `MAINTAINED`, `VIOLATED`, `NEEDS_CONTEXT` |
| audit without edge evidence | `N/A` or `NEEDS_CONTEXT` |
| validate advisory/no verifier | `DONE` with `ADVISORY` verdict |
| validate enforced/no safe verifier or non-zero verifier | `BLOCKED` |

### FR-4: Consumer and agent integration

- `ywc-code-gen` discovers only root `architecture-invariants.json`, unless the caller supplied an explicit repository-relative `--manifest`. It forwards only affected components/rules and evidence paths.
- `ywc-task-generator` records component ownership, affected rule ids, and verifier requirement in task metadata/checklists; it does not reimplement verifier logic per task.
- `ywc-impl-review` Architecture lane uses evidence as a finding source. Missing verifier output is reported as `N/A` or a contract configuration issue, never as a fabricated dependency violation.
- `ywc-architect` adds `Invariant Verdict`, `Rules`, `Evidence`, and `Next action` after its existing `Status`. It must return `NEEDS_CONTEXT` when component mapping or normalized evidence is absent.

### FR-5: Sanitized run evidence

> ⚠️ SUPERSEDED by Iteration 1 — see §iteration-1-amendments--spec-readiness-validation.

The context-safety run evidence mechanism may record an invariant tuple containing `contract_state`, verifier `id`, SHA-256 of the local `argv` representation, exit code, normalized evidence artifact path, and rule ids.

The validator rejects `raw_command`, `raw_command_output`, `transcript`, `chain_of_thought`, `generated_source`, and `full_diff` recursively in this entry. Paths outside root or paths that cannot be safely normalized are recorded as `N/A — unsafe evidence omitted`.

### FR-6: Evaluation and release

Fixtures cover valid contract, malformed JSON, duplicate/dangling IDs, invalid glob, no-manifest fallback, ambiguous mapping, advisory/no verifier, enforced/unregistered verifier, forbidden edge evidence, safe argv enforcement, raw-field rejection, and architect verdict states.

The bundle adds all required READMEs, `agents/openai.yaml`, release metadata, and validation inventory entries for the new skill.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Security | Repository/PR content cannot select executable commands or introduce a shell execution path. |
| Determinism | Parser, schema validation, path resolution, registry lookup, and rule evaluation are mechanical. |
| Compatibility | No manifest preserves current workflows. Existing direct skill use needs no new configuration. |
| Privacy | Evidence logs contain identifiers/digests/status only, never raw command or output. |

## Data Model

This adds a documentation contract only: `architecture-invariants.json` and local ignored verifier registry. It does not change application data schemas.

## API Contract

`ywc-architecture-invariants --mode <draft|audit|validate> [--manifest <repository-relative-path>]` follows FR-3. `--manifest` never triggers fallback discovery if supplied but invalid or missing.

## Edge Cases

- manifest absent: `N/A`; no consumer behavior changes.
- explicit manifest outside root or absent: `NEEDS_CONTEXT`; do not fallback.
- overlapping component path: report shared context only when declared; otherwise `NEEDS_CONTEXT`.
- verifier produces malformed evidence: `BLOCKED` in enforced mode and `NEEDS_CONTEXT` in advisory mode.
- verifier times out or runtime cannot disable network: do not retry with weaker controls; return `BLOCKED` or `NEEDS_CONTEXT` respectively.
- Mermaid diagram exists but disagrees: mark it stale documentation; JSON contract remains authority.

## Dependencies

- Python standard-library `json`, `hashlib`, and safe process-control capability.
- Context-safety Result/run-evidence contract from `20260812-codex-agentic-context-safety.md`.
- Project-local user configuration for an opted-in verifier.

## Open Questions

N/A for v1. Language-specific import graph adapters and legibility measurement are explicitly deferred until adoption evidence establishes their required interfaces.

## Verification Plan

- `bash scripts/validate.sh`
- schema/runner unit fixtures using only Python standard library
- targeted skill and agent eval fixture validation
- `bash scripts/install.sh --list`
- `CODEX_HOME=<isolated-temp-dir> bash scripts/install.sh --codex ywc-architecture-invariants`
- static check that no manifest field named `command`, `shell`, `script`, or equivalent reaches the runner

## References

- `codex/agents/ywc-architect.toml`
- `codex/skills/ywc-code-gen/SKILL.md`
- `codex/skills/ywc-impl-review/SKILL.md`
- `codex/skills/ywc-task-generator/SKILL.md`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md`

## Iteration 1 Amendments — Spec-readiness validation

> This section is operative for every requirement it refines. It resolves the v1
> portability, schema, evidence-coverage, and consumer-routing findings below.

### A. Outcome Oracle and v1 boundary

| Element | Definition |
|---|---|
| Target | Codex consumers can deterministically validate and use an optional, repository-root architecture contract without executing repository- or user-supplied verifier programs. |
| Quality threshold | All AC1–AC8 have a mapped positive and negative executable fixture; malformed, ambiguous, unsafe, incomplete, or out-of-scope inputs never yield `MAINTAINED`; no fixture permits process execution from manifest or local registry data. |
| Evidence required | `python3 tests/architecture_invariants_test.py`, `bash scripts/run-codex-skill-contract-evals.sh`, `bash scripts/validate.sh`, `bash scripts/install.sh --list`, and an isolated `bash scripts/install.sh --codex ywc-architecture-invariants` smoke, with the generated plugin synchronized. |
| Stop condition | The work is ready for task generation only when every mapped fixture passes, the listed bundle checks pass, and inspection confirms that no v1 path launches a verifier process or forwards raw evidence/output. |

V1 is **validation-only**. It does not execute a configured verifier, including one
listed in `.codex/settings.local.json`; `network: false` is therefore not claimed as
a portable subprocess control. A later version may add execution only with an
explicitly supported OS-sandbox backend, platform matrix, and test coverage. The
v1 local registry is out of scope; it is not read, logged, or distributed.

### B. Normative data contracts and path rules

The implementation adds `codex/skills/ywc-architecture-invariants/references/contracts.md`
as the single normative source for the following **closed** JSON shapes. Unknown
properties are rejected at every level. All paths use `/`, are non-empty,
repository-relative POSIX paths, contain no `.` or `..` segment, contain no NUL,
and resolve beneath the canonical repository root without following an escaping
symlink. A `glob` is a path with only literal segments, `*`, and terminal `**`;
braces, character classes, `?`, absolute paths, and empty matches are invalid.

```json
{
  "version": 1,
  "owner": "team-or-owner",
  "enforcement": "advisory",
  "components": [
    {"id": "api", "paths": ["src/api/**"], "owner": "platform", "shared": false},
    {"id": "ui", "paths": ["src/ui/**"], "owner": "web", "shared": false}
  ],
  "rules": [
    {"id": "api-forbids-ui", "source": "api", "target": "ui", "policy": "forbid", "rationale": "layering"}
  ]
}
```

`components` and `rules` are non-empty arrays. Component and rule IDs match
`^[a-z][a-z0-9-]*$`; `shared` defaults to `false`; component IDs and rule IDs are
unique; every rule endpoint exists; self edges and duplicate `(source, target)`
pairs are rejected. A manifest has no `verifier`, `command`, `shell`, `script`, or
other executable field in v1.

The evidence artifact is a closed, versioned JSON object:

```json
{
  "version": 1,
  "scope_paths": ["src/api/route.ts"],
  "scope_digest": "sha256:<64-lowercase-hex>",
  "covered_rule_ids": ["api-forbids-ui"],
  "edges": [
    {"rule_id": "api-forbids-ui", "source_component": "api", "target_component": "ui", "evidence_path": "src/api/route.ts", "line": 12}
  ]
}
```

`scope_paths`, `covered_rule_ids`, and `edges` are deterministic-order, duplicate-free
arrays. Every edge has a unique `(rule_id, evidence_path, line)` tuple, names its
declared rule and matching endpoints, and its path is in `scope_paths`; `line` is a
positive integer. The SHA-256 digest is of the UTF-8, newline-joined normalized
`scope_paths`. Coverage is complete only when every declared rule whose source or
target has a non-shared component matching a changed path is present once in
`covered_rule_ids`; otherwise its verdict is `NEEDS_CONTEXT`, never `MAINTAINED`.
An observed edge violates a `forbid` rule and maintains an `allow` rule. An absent
edge maintains a `forbid` rule only with complete coverage; absent allow-edge evidence
is `N/A`. Unsafe edge paths are omitted from the sanitized record, and every affected
rule is `NEEDS_CONTEXT`; unaffected, demonstrably out-of-scope rules are `N/A`.

### C. Public interface, modes, and terminal semantics

The exact v1 interface is:

```text
ywc-architecture-invariants --mode draft [--manifest <repository-relative-path>]
ywc-architecture-invariants --mode validate [--manifest <repository-relative-path>]
ywc-architecture-invariants --mode audit --changed-path <repository-relative-path> [--changed-path <...>] --evidence <repository-relative-json-path> [--manifest <repository-relative-path>]
```

`--changed-path` is repeatable, required for `audit`, normalized and deduplicated
before component mapping; an empty list, an escaping/symlink path, or ambiguous
non-shared mapping returns `NEEDS_CONTEXT`. `draft` writes only after the caller
approves the supplied root-relative output and returns `DONE`, `NEEDS_CONTEXT`, or
`BLOCKED`. `validate` parses only the manifest and returns `DONE` with
`Invariant Verdict: ADVISORY` for a valid advisory contract, `BLOCKED` for a valid
enforced contract because v1 has no executor, and `NEEDS_CONTEXT` for invalid input.
It does not accept evidence. `audit` evaluates the supplied evidence and returns
`MAINTAINED`, `VIOLATED`, `N/A`, or `NEEDS_CONTEXT` per Section B. An explicit missing
or invalid `--manifest` never falls back to discovery. A discovered missing manifest
returns `N/A — no architecture contract` without changing consumer behavior.

### D. Consumer authority and agent output

`codex/skills/scripts/architecture-invariants.py` is the one shared stdlib resolver
and evaluator. Each direct consumer (`ywc-code-gen`, `ywc-task-generator`, and
`ywc-impl-review`) exposes the same optional repository-relative `--manifest` and
uses that helper; omitted `--manifest` permits root-only discovery, while supplied
invalid/missing input is `NEEDS_CONTEXT` with no fallback. Consumers derive audit
`--changed-path` values only from their already-bounded feature/task/diff file list,
never from a broad scan. They forward only `{contract_state, component_ids, rule_ids,
evidence_artifact_path, invariant_verdict}`; they neither forward evidence contents
nor reimplement contract evaluation. This packet is absent for no-manifest fallback.

`ywc-architect` retains its existing status vocabulary. Its contract becomes
`Status: <DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT>` followed by
`Invariant Verdict: <MAINTAINED|VIOLATED|N/A|NEEDS_CONTEXT>`, `Rules:`, `Evidence:`,
and `Next action:` within 300 words. It emits `N/A — no architecture contract` when
no contract was discovered, and emits `NEEDS_CONTEXT` only for a selected valid
contract whose required mapping or coverage is missing.

### E. Sanitized run evidence and executable coverage

The invariant tuple is owned by a new ignored, atomic-replacement artifact
`.ywc-architecture-invariants-evidence.json` beside the authoritative
`.ywc-run-state.json`; it is not added to the closed context-handoff schema. Its
closed version-1 entry has only `contract_state`, `invariant_verdict`, `rule_ids`,
`evidence_artifact_path`, and optional `evidence_digest`. No verifier ID, command,
exit code, raw output, transcript, source, full diff, or unknown key is permitted.
The architecture-invariants helper writes it only after a successful bounded audit;
agentic may read it as non-authoritative diagnostic evidence and checkpoint/task
state remains authoritative.

`tests/architecture_invariants_test.py` is a standard-library `unittest` runner and
is invoked by `scripts/validate.sh`. Its fixtures map AC1–AC8 to named cases covering
valid/no-manifest contracts, malformed and closed-schema failures, duplicate/dangling
IDs, invalid globs, explicit-manifest no-fallback, ambiguous mapping, changed-scope
normalization, full/partial coverage, allow/forbid outcomes, unsafe-path omission,
v1 no-execution, bounded consumer packets, architect status/verdict pairs, forbidden
run-evidence fields, and isolated-install inventory. Each case records expected
terminal status and zero process launches. Skill `evals/evals.json` cases reference
the same fixture IDs; `scripts/run-codex-skill-contract-evals.sh` remains a contract
shape check, not proof of runtime semantics.

### F. Superseded requirements

FR-2, all verifier-execution clauses in FR-3, the `verifier` field in FR-1, and the
verifier ID/argv/exit-code portion of FR-5 are superseded by Sections A–E. The
original acceptance and verification requirements remain operative only as refined
by the explicit v1 result, schema, consumer, evidence, and test contracts above.

## Iteration 2 Amendments — Final readiness closure

> This section prevails over both the original text and Iteration 1 wherever it
> refines v1 behavior.

### A. Scope and acceptance-criteria replacements

The allowed change scope includes `codex/skills/`, `codex/agents/`,
`plugins/ywc-agent-toolkit/skills/` as generated packaging, `.gitignore`,
`scripts/validate.sh`, `tests/architecture_invariants_test.py`, and the release
metadata/inventory files actually discovered during implementation.

AC2 is replaced with: **No arbitrary execution:** v1 accepts no verifier, command,
shell, script, argv, registry, or interpolated executable field in a manifest,
evidence artifact, consumer packet, or run-evidence record; it launches zero child
processes from contract data and rejects such fields with `NEEDS_CONTEXT`.

AC7 is replaced with: **Safe run evidence:** the closed invariant-evidence artifact
contains only the Section C audit result fields and rejects raw command/output,
transcript, source, generated source, chain of thought, full diff, and all unknown
fields recursively.

### B. Draft and deterministic path/glob semantics

`draft` is v1 metadata scaffolding, not reconnaissance. Its exact interface is
`ywc-architecture-invariants --mode draft --proposal <repository-relative-json-path>
--output <repository-relative-json-path> --approve-write`; it rejects omitted
approval, invalid proposal, existing output, or an output outside root with
`NEEDS_CONTEXT` and writes only a schema-valid manifest on `DONE`. `--manifest` is
invalid in draft mode.

For matching, split normalized paths and globs on `/`. A literal segment matches the
identical segment; `*` matches exactly one non-empty segment; a terminal `**` matches
zero or more remaining segments; no other wildcard is recognized. A component matches
when one of its patterns consumes all path segments. Boundary fixtures cover literal,
`*`, terminal `**`, zero-segment `**`, and non-matches.

### C. Audit scope, result schema, and aggregate verdict

Before evaluation, the helper requires the normalized, sorted, deduplicated CLI
`--changed-path` set to equal evidence `scope_paths` exactly and recomputes
`scope_digest`; either mismatch is `NEEDS_CONTEXT`. That one verified set is the only
input to component mapping and affected-rule coverage.

Audit returns this closed version-1 result (arrays are sorted by `rule_id`):

```json
{
  "version": 1,
  "aggregate_verdict": "MAINTAINED",
  "rule_results": [
    {"rule_id": "api-forbids-ui", "verdict": "MAINTAINED", "evidence_paths": ["src/api/route.ts"]}
  ]
}
```

Each result has only `rule_id`, `verdict` (`MAINTAINED`, `VIOLATED`, `N/A`, or
`NEEDS_CONTEXT`), and normalized `evidence_paths`; duplicate/missing affected rules
are invalid. Aggregate precedence is `VIOLATED` > `NEEDS_CONTEXT` > `MAINTAINED` >
`N/A`; no affected rules yields `N/A`. The invariant packet and optional run-evidence
artifact use this aggregate plus rule IDs, never the raw evidence.

### D. Consumer evidence interface and no-evidence behavior

Each direct consumer exposes optional `--manifest <path>` and
`--architecture-evidence <repository-relative-json-path>` as a paired input: evidence
without a resolved valid manifest is `NEEDS_CONTEXT`; a manifest without evidence
preserves the consumer's existing behavior and supplies no invariant packet. When both
are supplied, the consumer derives its bounded changed-path set, invokes the shared
audit helper, and forwards the Section C aggregate result plus affected IDs and the
evidence path only. `VIOLATED` is surfaced in that consumer's normal finding/error
channel; `NEEDS_CONTEXT` is propagated before dispatch; `N/A` and `MAINTAINED` permit
the existing flow. Fixtures include positive and no-evidence/invalid-evidence cases
for code generation, task generation, and implementation review.

### E. Final invariant evidence and architect adapter

This section replaces Iteration 1 Section E's invariant-artifact field list. The
ignored atomic-replacement artifact remains beside `.ywc-run-state.json`, but its
closed version-1 shape is exactly the Section C audit result object; it contains no
additional fields. `contract_state` is represented by `aggregate_verdict`, and the
artifact is written only for a completed audit. It rejects raw command/output,
transcript, source, generated source, chain of thought, full diff, and unknown keys
recursively.

Before an architecture consultation, the caller supplies the `ywc-architect` bounded
packet through the same shared helper: optional resolved manifest identity, bounded
changed paths, optional evidence artifact path, and the resulting Section C audit
result. No manifest yields `Invariant Verdict: N/A — no architecture contract`; a
valid manifest without evidence or complete coverage yields `Invariant Verdict:
NEEDS_CONTEXT`; otherwise the architect receives only rule results and cited paths,
not raw evidence contents. The architect never discovers manifests, runs audits, or
infers edges itself.

Each evidence edge's `evidence_path` must unambiguously map to its declared
`source_component` under Section B matching; a shared-only or zero/multi non-shared
mapping is `NEEDS_CONTEXT`. This mapping is checked before any rule outcome is
computed, with fixtures for mismatched-source and shared paths.
