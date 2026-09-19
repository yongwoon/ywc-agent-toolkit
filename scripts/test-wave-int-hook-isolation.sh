#!/usr/bin/env bash
# Regression coverage: the disposable repositories created by the wave-int
# suite must not inherit a caller's pre-commit hook. Otherwise the repository
# validation hook recursively invokes itself through those fixture commits.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

HOOK_DIR="$TMP_ROOT/hooks"
GLOBAL_CONFIG="$TMP_ROOT/gitconfig"
mkdir -p "$HOOK_DIR"

cat > "$HOOK_DIR/pre-commit" <<'EOF'
#!/usr/bin/env bash
exit 1
EOF
chmod +x "$HOOK_DIR/pre-commit"
git config --file "$GLOBAL_CONFIG" core.hooksPath "$HOOK_DIR"

if ! GIT_CONFIG_GLOBAL="$GLOBAL_CONFIG" GIT_CONFIG_NOSYSTEM=1 \
  bash "$REPO_ROOT/scripts/test-wave-int-checkpoint-ownership.sh"; then
  echo "FAIL: disposable fixture commits inherited the configured hook" >&2
  exit 1
fi

echo "PASS: wave-int fixture commits bypass inherited hooks"
