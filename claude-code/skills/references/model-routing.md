# Model Hint Routing Contract

`Model Hint` is an optional task field (`haiku` | `sonnet` | `opus`) recorded by `ywc-task-generator` as the first bullet under `## Parallel Execution Metadata` in each task's README.md. `ywc-parallel-executor` passes it as the Agent tool `model` parameter when dispatching the implementer.

This file is the single contract shared by `ywc-task-generator` (assignment) and `ywc-parallel-executor` (consumption). Each consumer links here rather than restating the rules.

## Values

`- Model Hint: <haiku|sonnet|opus> — <one-line rationale naming the rule (M1/M2/M3)>`

- Placed as the first bullet directly under `## Parallel Execution Metadata`, before `### Ownership`. No new heading.
- Optional. Absent = no hint.
- Values are the three Agent tool aliases only. `fable` and pinned model IDs are not Model Hint values.
- Parse rule: the value is the first whitespace-delimited token after `Model Hint:` and before the em dash `—`; a missing em dash is tolerated. Only a bullet inside `## Parallel Execution Metadata` is read — a `Model Hint` line elsewhere in the README is ignored, and duplicate detection is scoped to that section.

## Assignment Rules

Applied by `ywc-task-generator` when it writes each task's README (Step 9), after `Depended By`, `### Ownership` and `### Owned Interface` are final. First match wins:

| Rule | Condition | Hint |
|---|---|---|
| M1 | `### Depended By` lists ≥2 tasks and `### Owned Interface` is not `(None …)` | `opus` |
| M2 | Task Category (the category segment of the task name, e.g. `docs`, `infra`) is not `infra`, AND every `### Ownership` entry matches the include list (`**/*.md`, `docs/**`, `*.json`, `*.yaml`, `*.yml`, `*.toml`, `.env.example`) and none matches the exclusion list: `.github/**`, `.circleci/**`, `.gitlab-ci.yml`, `azure-pipelines*.y*ml`, `**/docker-compose*.y*ml`, `**/compose*.y*ml`, `**/k8s/**`, `**/helm/**`, `**/Chart.yaml`, `**/openapi*`, `**/schema*`, `package.json`, `tsconfig*.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` | `haiku` |
| M3 | otherwise | `sonnet` |

This repository has no per-task `Criticality` field, so M1 is adapted to the dependency-fan-out signal alone: a task that two or more downstream tasks build on, through a published interface, is the one whose mistakes cost the most. Treat this as a provisional rule until a Criticality concept exists.

Determinism rules:

- **M1 counting**: count only real task bullets under `### Depended By` (exclude a `(None …)` line). `### Owned Interface` is "present" when it has ≥1 bullet that does not start with `(None`.
- **M2 matching**: each `### Ownership` entry (a repo-relative path) is matched as a glob where `*` matches within one path segment and never crosses `/`, `**/` matches zero or more directories, and a trailing `/**` matches all descendants at any depth. A pattern without `/` matches root-level files only (`*.json` matches `tsconfig.json`-style root files, not `src/data.json`). Markdown is the exception: `**/*.md` matches a `.md` file at any depth, because this repository's docs-only tasks edit skill and reference markdown nested under `claude-code/` (`docs/**` still covers non-markdown files under `docs/`). Both lists are exhaustive: an entry matching no include pattern (module subtree glob, `Dockerfile`, `API contract: …`, `Database schema: …`) does not satisfy M2 → M3. Mixed docs + code/test → M3.
- The generator records which rule fired in the rationale. A user may edit the hint by hand afterwards; the executor trusts the README value after it has been normalized and validated (see Absent or Invalid Value).

## Consumption

| Consumer | Behavior |
|---|---|
| `ywc-parallel-executor` Step 4b (implementer dispatch only) | hint present → pass as `model`; absent + named agent → omit `model` (frontmatter default); absent + inline implementer (`general-purpose`) → pass `sonnet` |
| `ywc-sequential-executor` | ignores the hint (implementation runs in the main session) |
| others | do not read the field |

**Version floor**: a per-invocation `model` outranks the `CLAUDE_CODE_SUBAGENT_MODEL` environment variable only on Claude Code ≥ `v2.1.251`. On older versions the variable overrides the hint; this is not an error and the executor does not detect it. The version figure comes from the upstream `develop-with-llm` project and has not been independently verified in this repository. The Completion Report records the value passed.

**Named vs inline classification**: decided from the `subagent_type` resolved after the Agent Hint override in `ywc-parallel-executor` Step 3. A named agent is any `ywc-*` agent `subagent_type`; the inline implementer is `general-purpose`. Category alone is never used.

**Effective model** (what the task's current dispatch runs on). First match wins:

1. Normalized hint → source `hint`.
2. Named agent's frontmatter `model` → source `frontmatter`.
3. Named agent whose frontmatter `model` is absent (not `inherit`), with `CLAUDE_CODE_SUBAGENT_MODEL` non-empty (read once in Step 1, re-read on resume) → that value, source `env`.
4. Inline implementer → `sonnet`, source `default`.

A named agent with `inherit` frontmatter, or absent frontmatter and no such variable, keeps source `frontmatter` and is written `inherit (frontmatter)` (it runs on the session model). A frontmatter value that is a pinned model ID is reported verbatim. An `env` value is reported only when it is a plain model-id token (`^[A-Za-z0-9._:/-]{1,64}$`); anything else is written `env (unrecognized)` so a free-form variable is never echoed into a report.

Source labels used everywhere (Completion Report included): `hint` / `frontmatter` / `env` / `default`. A dispatch is written `<model> (<source>)`, for example `sonnet (hint)`. When a user's environment sets `CLAUDE_CODE_SUBAGENT_MODEL` on an older Claude Code, the report still shows the value that was *passed* (`hint`), so the label is how a reader spots that the hint may have been overridden.

**Pass vs omit**: pass the alias for sources `hint` / `default`; always omit `model` for `frontmatter` / `env` (a pinned ID is never passed).

**Re-dispatch**: every re-dispatch of the same task — NEEDS_CONTEXT, correctness-level DONE_WITH_CONCERNS fix, BLOCKED Context problem, Task Verify fix-and-re-verify — repeats the original pass/omit handling, so the task keeps its effective model. Those re-dispatches change the input, never the model.

**Resume**: the effective model is not persisted (`.ywc-run-state.json` schema unchanged). On resume a pending task's effective model is re-derived from the rules above.

## Absent or Invalid Value

- Normalize: trim and lowercase the parsed token, then validate against `haiku|sonnet|opus`.
- An empty value, a value outside the three, or a duplicated `Model Hint` bullet → treat as absent and add an `Invalid Model Hint` note to the Completion Report (Step 5 of `ywc-parallel-executor`). The note carries the task name and the fixed text `unrecognized value`; the offending token is omitted or truncated to 20 characters, never echoed whole. Never block.
- Field absent → current behavior (named agent: frontmatter; inline implementer: `sonnet`). Task sets generated before this field existed run unchanged; absence is never an error.

## Worked Examples

| Row | Inputs | Rule | Output |
|---|---|---|---|
| (a) | `Depended By` lists 2 tasks; `Owned Interface` has a signature bullet | M1 | `opus` |
| (b) | `Depended By` lists 2 tasks; `Owned Interface` is `(None — …)`; Ownership `claude-code/skills/ywc-x/SKILL.md` | M1 does not fire (no interface); M2 (nested markdown) | `haiku` |
| (c) | Ownership `docs/guide/setup.md` + root `README.md` + `src/README.md` | M2 | `haiku` |
| (d) | Ownership root `.gitlab-ci.yml` only (include match `*.yml`, then exclusion) | M2 exclusion → M3 | `sonnet` |
| (e) | Ownership `src/features/auth/**` | M3 | `sonnet` |
| (f) | Ownership `docs/x.md` + `tests/x.test.ts` | M3 | `sonnet` |
| (g) | Hint absent, inline implementer (`general-purpose`) | Consumption | `model: sonnet`, Dispatch model `sonnet (default)` |
| (h) | Hint absent, named agent `ywc-backend-coder` | Consumption | `model` omitted, Dispatch model `sonnet (frontmatter)` |
| (i) | Ownership `Dockerfile` only (not in include list) | M3 | `sonnet` |
| (j) | Ownership `docker-compose.yml` only (include `*.yml`, then exclusion) | M2 exclusion → M3 | `sonnet` |
| (k) | Ownership `compose.yaml` only (include `*.yaml`, then exclusion) | M2 exclusion → M3 | `sonnet` |
| (l) | Category `infra` + Ownership root `app.yaml` (include match, then Category guard) | M2 guard → M3 | `sonnet` |
