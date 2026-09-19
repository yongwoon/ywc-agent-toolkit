# Trusted Codex executable resolution

This contract is normative for Codex skills that invoke a shipped helper. It
selects an executable only from the installed Codex bundle or from an
explicitly authorized development checkout. It never treats a target
repository's file existence as authority.

## Resolver contract

The shipped resolver is `scripts/resolve-bundle-executable.sh`; its Python
implementation is stdlib-only. It accepts a path relative to `codex/skills/`
and one fixed invocation kind: `bash`, `python`, `python3`, or `direct`.

- Installed resolution is first and uses `${CODEX_HOME:-$HOME/.codex}/skills/`.
- Source fallback requires `YWC_BUNDLE_DEVELOPMENT=1` and an absolute,
  canonical `YWC_BUNDLE_SOURCE_ROOT` that is the Git root of this repository,
  has the expected `yongwoon/ywc-agent-toolkit` origin, and contains
  `codex/skills/`.
- The candidate must resolve to a readable regular file contained by the
  authorized bundle tree. A symlink escaping that tree is rejected.
- `bash`, `python`, and `python3` candidates need not be executable because a
  fixed interpreter invokes them. `direct` candidates must be executable.
- Success prints exactly one absolute path on stdout and exits zero.
- Failure prints a deterministic `BLOCKED:` diagnostic to stderr, names the
  expected installed path and safe development remediation, and exits 3.

The resolver owns executable selection only. It does not authorize changed
arguments, shell evaluation, target-repository script discovery, or source
fallback based on file existence alone. Callers preserve their existing
interpreter, arguments, pipeline ordering, and exit-result handling.

## Launcher-selection contract

Selecting `RESOLVER_LAUNCHER` itself (installed bundle vs. authorized
development source) is not inlined per caller. `scripts/select-resolver-launcher.sh`
owns it exactly once so the trust checks below cannot drift or be duplicated
incorrectly at a new call site:

- Installed resolution is first, via `${CODEX_HOME:-$HOME/.codex}/skills/scripts/resolve-bundle-executable.sh`.
- Source fallback requires explicit `YWC_BUNDLE_DEVELOPMENT=1` and a
  `YWC_BUNDLE_SOURCE_ROOT` that is the canonical Git root of this repository
  with the expected `yongwoon/ywc-agent-toolkit` origin — checked *before*
  the source-root launcher is ever executed, not only for the executable it
  later resolves.
- Both branches fully resolve the launcher file's own symlink chain (not
  only its parent directory) before the containment check, so a launcher
  path whose final component is a symlink escaping the authorized tree is
  rejected rather than executed.
- Failure prints a deterministic `BLOCKED:` diagnostic to stderr and exits 3
  — never a bare parameter-expansion error, so the exit code and message are
  contractually stable for callers.

## Exact launcher-selection block

Every caller must use this block, changing only `BUNDLE_EXECUTABLE` and the
fixed invocation kind/path passed to the launcher. Re-run it at the start of
every code block that resolves an executable — a shell variable set in one
code block does not persist into a separately executed one, so a later block
reusing `$RESOLVER_LAUNCHER` without recomputing it would silently invoke
`bash` with an empty path.

```bash
RESOLVER_LAUNCHER="$(bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/select-resolver-launcher.sh" 2>&1)" || { echo "BLOCKED: ${RESOLVER_LAUNCHER#BLOCKED: }" >&2; exit 3; }
BUNDLE_EXECUTABLE="$(bash "$RESOLVER_LAUNCHER" <bundle-relative-path> <bash|python|python3|direct>)" || exit $?
```

The Python resolver repeats the trust and containment checks for the requested
candidate, so a trusted launcher cannot authorize an untrusted target path.
