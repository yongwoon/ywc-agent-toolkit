# Gate Ledger Format

Full format spec for the optional Executable Gate Ledger escalation ([../SKILL.md](../SKILL.md#optional-escalation-executable-gate-ledger)), checked by `../scripts/gate-check.py`.

## Security warning

`CHECK:` lines execute arbitrary shell commands with the invoking user's own permissions. There is no approval-record or allowlist enforcement layer in this project's `gate-check.py` (that layer is explicitly out of scope — a deliberate trade-off, not an oversight). **Read every `CHECK:` line before running a ledger you did not author yourself.** A malicious or corrupted ledger can run destructive commands with your own permissions.

## Gate structure

A ledger is a caller-supplied markdown file — no hardcoded discovery path, always an explicit CLI argument — containing one or more gates:

```markdown
- [ ] G1: <outcome>
  CHECK: <shell command>
  EXPECT: <substring or /regex/flags>
  EVIDENCE: pending
```

- **`id`** (`G1` above) must be non-empty and unique within the file.
- **Runnable vs. manual**: a gate with **both** `CHECK:` and `EXPECT:` is *runnable* — `gate-check.py` can execute and judge it. A gate with **neither** is *manual/non-runnable* — a human-verified step that is never auto-marked met and is reported `manual (skipped)`. A gate with **exactly one** of the two is a malformed ledger and fails closed (`gate-check.py` exits non-zero, naming the gate id and the missing field).
- **`EVIDENCE:`** is auto-inserted if missing when a gate is executed, preserving the file's original LF/CRLF line-ending style. An empty `EVIDENCE:` line before the first run reads as `pending`.
- **`EXPECT:`** matching is plain substring by default. When the value both starts and ends with `/` (`/pattern/flags`), it is compiled as a Python regular expression. Only these flag letters are recognized: `i` → `re.IGNORECASE`, `m` → `re.MULTILINE`, `s` → `re.DOTALL`. Any other flag letter (including JS-only `g`/`u`/`y`) is a parse error reported at `--status` time. An empty `EXPECT:` value is rejected as a parse error — it can never fail to "match" a non-empty output, which would defeat the gate silently.

## Fenced-code-block skip

A line that **starts with** a triple-backtick fence marker — bare, or followed by a language tag such as `` ```markdown `` — toggles a "skip parsing" state, so a ledger's own documentation examples (like the gate structure shown above) are not parsed as live gates. If the ledger contains an odd number of fence-toggle lines — a fenced block opened but never closed before EOF — the parser treats the fence as implicitly closed at EOF; content inside stays skipped as documentation, and no error is raised solely for the unterminated fence.

## Modes and exit codes

```bash
python3 claude-code/skills/ywc-verify-done/scripts/gate-check.py --status <ledger.md>    # parse + report only; executes nothing
python3 claude-code/skills/ywc-verify-done/scripts/gate-check.py <ledger.md>              # execute every unmet runnable gate
python3 claude-code/skills/ywc-verify-done/scripts/gate-check.py --reverify <ledger.md>   # force re-execute every runnable gate
```

- `--status`: parses and reports every gate's id/CHECK/EXPECT/current status. Exit 0 for a well-formed ledger, non-zero for a malformed one. Executes zero `CHECK:` commands.
- Default run (no flag): executes every runnable gate whose `EVIDENCE:` is not a **cached PASS**. A cached PASS is trusted only when its recorded SHA-256 fingerprint (`sha256:<hex>`, computed over the gate's current `CHECK` bytes, one NUL byte, and current `EXPECT` bytes) matches the gate's current `CHECK:`/`EXPECT:` text — editing either after a PASS invalidates the cache and forces re-execution, even though the stale line still reads `PASS`. A gate passes only when its `CHECK:` command exits 0 **and** its combined stdout+stderr matches `EXPECT:`.
- `--reverify`: executes every runnable gate regardless of its current `EVIDENCE:` state — never trusts stale or cached evidence.
- Exit 0 = all runnable gates met (well-formed ledger on `--status`). Exit 1 = at least one unmet gate, or a malformed/missing ledger. A nonexistent ledger path produces a distinct "file not found" message, never conflated with a malformed-but-present ledger.

## Bounds

Per-gate timeout: 120 seconds. Combined stdout+stderr capture per gate: 64 KB, streamed incrementally rather than buffered in full — output exceeding the cap fails the gate closed (`EVIDENCE: FAIL; exit=output_limit; decisive="OUTPUT_LIMIT exceeded (65536 bytes)"`) instead of silently matching within a truncated slice. Each `CHECK:` runs in its own process group on POSIX (`start_new_session=True`); a timeout or output-cap breach terminates the whole subtree via `SIGTERM` then `SIGKILL`, not just the top-level shell. Concurrent invocation against the same ledger file is unsupported and undocumented — this is a single-session local tool, not a multi-tenant orchestration primitive.
