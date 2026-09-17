# Gate Ledger reference

The Gate Ledger is an optional escalation for multi-command or accepted-subagent-artifact claims. It does not replace the normal `ywc-verify-done` workflow or the separately required CI, PR-health, and `poll-pr-reviews.sh --verify` evidence.

## Grammar

```markdown
- [ ] G1: full suite passes
  CHECK: bash scripts/validate.sh
  EXPECT: Skill is valid!
  EVIDENCE: pending
```

A gate header is a hyphen, optional whitespace, one character in brackets, optional whitespace, and non-empty text before the first colon. The text before that colon is the gate ID. Until the next valid header, only lines matching `CHECK:`, `EXPECT:`, or `EVIDENCE:` are fields. Field values are single-line; one optional space after the colon is removed. Repeated fields use the final matching field. Other lines and continuation lines are inert.

Triple-backtick fences, including tagged fences, toggle documentation skipping. An unterminated fence remains documentation through end of file. A fenced example is never executed.

`EXPECT: text` is a literal substring match. A value starting with `/` and containing another `/` is instead parsed as `/pattern/flags`, a regular expression accepting only `i`, `m`, and `s` flags; the last `/` in the value is the closing delimiter, so the pattern itself need not end with `/`. A literal substring that begins with `/` and contains another `/` (e.g. a path such as `/usr/bin/tool not found`) is misparsed as a regex — avoid a leading `/` in plain-substring `EXPECT:` values. Regex matching is isolated and bounded by the checker.

A gate with neither `CHECK` nor `EXPECT` is `MANUAL`; manual gates are reported and skipped, and the checker never writes their evidence. A runnable gate must have both fields and non-empty values. The checker is not a sandbox: inspect every inherited `CHECK` before running it because checks execute through the caller's shell.

## Modes and evidence

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" --status <ledger.md>
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" <ledger.md>
python3 "${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py" --reverify <ledger.md>
```

`--status` parses and reports without starting subprocesses or changing bytes. It exits zero for valid syntax even when runnable gates are pending or have failed evidence. Bare mode is recovery-only: it runs runnable gates without an exact cached PASS for the unchanged `CHECK` and `EXPECT`. `--reverify` runs every runnable gate and is the only ledger mode that supplies fresh runnable-ledger evidence.

The cache fingerprint is SHA-256 over UTF-8 `CHECK` bytes, one NUL byte, then UTF-8 `EXPECT` bytes. A valid cached PASS is:

```text
PASS; exit=0; fingerprint=sha256:<64 lowercase hex>; decisive=<JSON string>
```

The decisive JSON string is a bounded summary containing the exit code, match result, and SHA-256 digest of captured combined-output bytes; raw command output is never persisted into the ledger. Executed gates replace the final effective `EVIDENCE` field. If it is absent, evidence is inserted immediately after the final effective `EXPECT` field. LF and CRLF are retained. FAIL evidence uses `FAIL; exit=<integer|124|125>; decisive=<JSON string>`. Exit `124` means timeout and `125` means the combined 64-KiB output cap was exceeded. Manual gates are never rewritten.

Each `CHECK` has a 120-second deadline, a combined stdout/stderr cap of 64 KiB, and POSIX process-group cleanup. Regex matching has a separate five-second deadline. For a PR-ready claim, this ledger is at most one evidence component: the existing 600-second poll, `--verify` head-SHA check, CI, and PR-health proof remain separate and fresh.
