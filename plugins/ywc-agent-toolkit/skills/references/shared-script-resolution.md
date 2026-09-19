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

## Exact launcher-selection block

Every caller must use this block, changing only `BUNDLE_EXECUTABLE` and the
fixed invocation kind/path passed to the launcher. The block validates the
launcher source before invoking it; it must not be replaced with a
target-relative fallback.

```bash
RESOLVER_LAUNCHER="${CODEX_HOME:-$HOME/.codex}/skills/scripts/resolve-bundle-executable.sh"
if [ -f "$RESOLVER_LAUNCHER" ]; then
  INSTALLED_SKILLS="$(cd -- "$(dirname -- "$RESOLVER_LAUNCHER")/.." 2>/dev/null && pwd -P)" || {
    echo "BLOCKED: installed resolver root is not accessible" >&2
    exit 3
  }
  INSTALLED_LAUNCHER="$(cd -- "$(dirname -- "$RESOLVER_LAUNCHER")" 2>/dev/null && pwd -P)/$(basename -- "$RESOLVER_LAUNCHER")" || {
    echo "BLOCKED: installed resolver launcher cannot be canonicalized" >&2
    exit 3
  }
  case "$INSTALLED_LAUNCHER" in
    "$INSTALLED_SKILLS"/*) RESOLVER_LAUNCHER="$INSTALLED_LAUNCHER" ;;
    *) echo "BLOCKED: installed resolver launcher escapes the installed skills tree" >&2; exit 3 ;;
  esac
else
  [ "${YWC_BUNDLE_DEVELOPMENT:-}" = "1" ] || {
    echo "BLOCKED: installed Codex resolver launcher is missing" >&2
    exit 3
  }
  : "${YWC_BUNDLE_SOURCE_ROOT:?BLOCKED: YWC_BUNDLE_SOURCE_ROOT is required for development fallback}"
  SOURCE_ROOT="$(cd -- "$YWC_BUNDLE_SOURCE_ROOT" 2>/dev/null && pwd -P)" || {
    echo "BLOCKED: source root is not accessible" >&2
    exit 3
  }
  SOURCE_ORIGIN="$(git -C "$SOURCE_ROOT" config --get remote.origin.url)" || {
    echo "BLOCKED: source origin cannot be read" >&2
    exit 3
  }
  case "$SOURCE_ORIGIN" in
    https://github.com/yongwoon/ywc-agent-toolkit.git|https://github.com/yongwoon/ywc-agent-toolkit|git@github.com:yongwoon/ywc-agent-toolkit.git|git@github.com:yongwoon/ywc-agent-toolkit|ssh://git@github.com/yongwoon/ywc-agent-toolkit.git|ssh://git@github.com/yongwoon/ywc-agent-toolkit) : ;;
    *) echo "BLOCKED: source origin is not the authorized repository" >&2; exit 3 ;;
  esac
  SOURCE_ROOT="$(git -C "$SOURCE_ROOT" rev-parse --show-toplevel)" || {
    echo "BLOCKED: source Git root cannot be resolved" >&2
    exit 3
  }
  RESOLVER_LAUNCHER="$SOURCE_ROOT/codex/skills/scripts/resolve-bundle-executable.sh"
  [ -f "$RESOLVER_LAUNCHER" ] || {
    echo "BLOCKED: source resolver launcher is missing" >&2
    exit 3
  }
  SOURCE_SKILLS="$(cd -- "$SOURCE_ROOT/codex/skills" 2>/dev/null && pwd -P)" || {
    echo "BLOCKED: source codex/skills layout is missing" >&2
    exit 3
  }
  SOURCE_LAUNCHER="$(cd -- "$(dirname -- "$RESOLVER_LAUNCHER")" 2>/dev/null && pwd -P)/$(basename -- "$RESOLVER_LAUNCHER")" || {
    echo "BLOCKED: source resolver launcher cannot be canonicalized" >&2
    exit 3
  }
  case "$SOURCE_LAUNCHER" in
    "$SOURCE_SKILLS"/*) RESOLVER_LAUNCHER="$SOURCE_LAUNCHER" ;;
    *) echo "BLOCKED: source resolver launcher escapes the source skills tree" >&2; exit 3 ;;
  esac
fi
BUNDLE_EXECUTABLE="$(bash "$RESOLVER_LAUNCHER" <bundle-relative-path> <bash|python|python3|direct>)" || exit $?
```

The Python resolver repeats the trust and containment checks for the requested
candidate, so a trusted launcher cannot authorize an untrusted target path.
