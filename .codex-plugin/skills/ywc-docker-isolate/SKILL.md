---
name: ywc-docker-isolate
description: >-
  (ywc) Use when parallel Git worktrees each run their own Docker stack and
  collide on host ports ("port is already allocated") — derives a deterministic
  per-worktree host-port block + COMPOSE_PROJECT_NAME, tears down only that
  worktree's stack, and audits stale stacks. Primarily a delegated callable from
  `ywc-parallel-executor` (Pre-flight audit, Step 4a setup, Step 4g teardown).
  Triggers: "docker port 격리", "worktree docker 충돌", "port is already
  allocated", "compose 포트 충돌", "ywc-docker-isolate", "docker isolate",
  "worktree docker stack", "Docker ポート分離", "コンテナ ポート衝突".
  Do not use for projects without Docker / docker-compose (no-op), non-Docker
  workspace isolation (local process ports, devcontainer), `ywc-sequential-executor`
  (runs one task at a time, no worktrees, no parallel host-port collision), or as
  a standalone container manager — it only allocates/tears down isolation ports.
---

# ywc-docker-isolate

**Announce at start:** "I'm using the ywc-docker-isolate skill to isolate this worktree's Docker host ports."

Deterministic, per-worktree Docker host-port isolation for parallel Git worktree
development. Each worktree derives a unique port block **purely from its task
name** — no central registry, no runtime coordination — and writes it to a
worktree-local env-file plus a `.ywc-docker-ports` persist file. The committed
compose / env-file is never mutated (per-worktree namespacing, not save/restore).
The deterministic engine lives in bundled scripts; this skill is the one-line
interface to them.

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--mode setup` | yes | Allocate and write a deterministic Docker host-port map for one task worktree. |
| `--mode teardown` | yes | Tear down one scoped Docker compose project and remove the persist file on success. |
| `--mode audit` | yes | Report residual Docker compose projects for expected task names. |
| `--task-name <task>` | setup/teardown | Task name used to derive `COMPOSE_PROJECT_NAME` and the deterministic port block. |
| `--worktree-path <dir>` | setup/teardown | Worktree directory where `.env` and `.ywc-docker-ports` live. |
| `--compose-file <file>` | no | Explicit compose file for setup; otherwise common compose filenames are auto-detected. |
| `--port-vars <vars>` | no | Comma-separated `VAR` or `VAR=PORT` entries; values are accepted for compatibility but allocation uses VAR names. |
| `--project-name <proj>` | teardown alternative | Explicit compose project to tear down instead of deriving from `--task-name`. |
| `--keep-volumes` | no | Omit `--volumes` during teardown. |
| `--expect <tasks>` | audit | Comma-separated task names whose Docker projects should not be left behind. |
| `--prune` | no | In audit mode, remove detected residual stacks instead of only reporting them. |

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Only one worktree is active right now — isolation is unnecessary" | Isolation is unconditional in the executor hook. A second worktree may start at any time, and the deterministic block is what guarantees they never collide. Run `setup` for every task worktree. |
| "Just edit the compose `ports:` / committed `.env` to free the port" | The original compose and committed env-file are immutable (NFR-1). Isolation writes only a worktree-local env-file managed block + `.ywc-docker-ports`; mutating tracked files pollutes `git diff` and breaks the other worktrees. |
| "`ss` is enough to check whether a port is free" | `ss` is Linux-only and absent on macOS. Port checks go through the cross-platform `check_port_in_use` (`ss`→`lsof`→`netstat`, fail-safe when none exist) — never call `ss` directly. |
| "Re-running setup can just re-compute the hash to get the same ports" | Reproducibility (AC2) comes from reading back `.ywc-docker-ports`, not from re-hashing. A re-hash would drift if an external process transiently held a port. Always read back the persist file; re-hash only on first allocation. |
| "`audit` returned exit 0, so there are no leftover stacks" | `audit` exit is **always 0** — residual stacks are signalled by **non-empty stdout**, not the exit code. Parse stdout; never gate on the audit exit code. |
| "A leftover stack from a prior run is harmless — proceed" | A stale `ywc-<task>_*` stack occupies the *same deterministic port* the next run derives, so resume is guaranteed to collide. Pre-flight `audit` must fail-loud (or `--prune`) before setup. |

## Modes

The deterministic logic is in `scripts/` — invoke it with a single line per mode.
The CLI contract (arguments, writes, exit codes) is authoritative and is what
`ywc-parallel-executor` integrates against.

### `setup` — allocate and apply the port block

```bash
ywc-docker-isolate --mode setup --task-name <task> --worktree-path <dir> \
  [--compose-file <file>] [--port-vars VAR1,VAR2]
```

- Writes a worktree-local env-file managed block (`COMPOSE_PROJECT_NAME=ywc-<sanitized-task>` + each `*_PORT`) and the `.ywc-docker-ports` persist file.
- Stdout: the resolved port map (`COMPOSE_PROJECT_NAME` + `VAR=port` lines).
- **Exit 0** = isolation applied, or no-op (no compose → "no docker — skipping isolation"). **Exit 1** = ports hardcoded (cannot isolate) / salt chain exhausted / corrupt persist / squatter live-check / sanitize-empty.
- Re-run on the same worktree reads back `.ywc-docker-ports` (deterministic, AC2) and live-checks every port before returning — a squatted port fails loud (AC13).

### `teardown` — remove only this worktree's stack

```bash
ywc-docker-isolate --mode teardown \
  (--task-name <task> | --project-name <proj>) --worktree-path <dir> [--keep-volumes]
```

- Runs `docker compose -p <project> down --volumes` (default; `--keep-volumes` preserves data), idempotent (exit 0 even with no running stack), deletes `.ywc-docker-ports` on success.
- **Exit 0** = teardown verified / nothing to do. **Exit 1** = `compose down` failed (`LEAKED_DOCKER_STACK` marker, wave **non-blocking**) or sanitize/malformed project (`SANITIZE_ERROR` marker, wave **blocking**). Both markers are written to **stderr** — distinguish the two by the marker string, not the exit code.

### `audit` — report leftover stacks for expected tasks

```bash
ywc-docker-isolate --mode audit --expect <task1,task2,...> [--prune]
```

- Detects residual `ywc-<task>` stacks. **Stdout non-empty = residual present** (each line `RESIDUAL_DOCKER_STACK: <project> (<n> container(s))`); **exit is always 0**.
- `--prune` tears residual stacks down (`down --volumes`) and confirms each on stdout (`pruned residual stack: <project>`). Without `--prune`, the caller (parallel-executor Pre-flight) must fail-loud and abort the run on any residual. **Gate on stdout non-empty only when `--prune` is not passed** — the prune confirmation lines would otherwise read as residuals.

## Integration (ywc-parallel-executor)

One-line pointers only (no inline prose in the executor body):

- **Pre-flight** (after worktree audit): `audit --expect <wave tasks>` — non-empty stdout → abort run with the printed stacks + `--prune` remediation.
- **Step 4a** (after 4a-verify, per task): `setup --task-name <t> --worktree-path <wt>` — exit 1 → task BLOCKED + worktree preserved, wave continues.
- **Step 4g** (before `cleanup-worktree.sh`, inside the 4e-DONE loop): `teardown --task-name <t> --worktree-path <wt>` — preserved (BLOCKED) worktrees skip 4g, so teardown is skipped automatically.

## Common Mistakes

- Calling `ss` directly instead of the cross-platform helper — breaks on macOS.
- Gating on the `audit` exit code instead of stdout non-empty — misses every residual stack.
- Re-hashing on re-run instead of reading back `.ywc-docker-ports` — breaks AC2 determinism under transient external port use.
- Placing the teardown pointer outside the 4e-DONE loop — would tear down BLOCKED-preserved worktrees.
- Writing isolation values into the committed compose/env-file instead of the worktree-local env-file managed block — pollutes `git diff` (NFR-1).

## Output Format

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Mode: audit | setup | teardown
Task: <task-name-or-none>
Worktree: <path-or-none>
Compose project: <name-or-none>
Port map: <host-port-map-or-none>
Residual stacks: <list-or-none>
```

Use `DONE_WITH_CONCERNS` when teardown leaves preserved resources that the caller intentionally keeps for a BLOCKED task. Use `BLOCKED` when residual stacks or missing compose metadata prevent safe setup.

## Validation

- `bash -n` clean on all `scripts/*.sh`.
- `setup` twice with the same `--task-name` yields an identical port map (AC2).
- Three distinct task names yield three distinct port blocks and `COMPOSE_PROJECT_NAME` values (AC1).
- `bash scripts/validate.sh` PASS; README locale set (`.md` / `.en.md` / `.ja.md` / `.ko.md`) present.

## References

> **Action required**: Read [references/port-allocation.md](references/port-allocation.md) for the hash formula, `var_index` sort rule, salt chain, modulo bias, and the AC2 determinism guarantee.

> **Action required**: Read [references/preconditions.md](references/preconditions.md) for compose detection, env-var mapping limits (short vs long syntax), the YAML parser priority, the platform port-check tool table, and the env-file vs shell-export precedence.
