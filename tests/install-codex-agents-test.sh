#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEMP_ROOT"' EXIT

install_with_version() {
  local version="$1"
  local expected_model="$2"
  local name="$3"
  local fake_bin="$TEMP_ROOT/$name/bin"
  local codex_home="$TEMP_ROOT/$name/codex-home"

  mkdir -p "$fake_bin"
  printf '#!/usr/bin/env bash\nprintf "codex-cli %%s\\n" "%s"\n' "$version" > "$fake_bin/codex"
  chmod +x "$fake_bin/codex"

  PATH="$fake_bin:$PATH" CODEX_HOME="$codex_home" bash "$REPO_ROOT/scripts/install.sh" --codex-agents >/dev/null
  grep -q "^model = \"$expected_model\"$" "$codex_home/agents/ywc-architect.toml"
  grep -q "^model = \"$expected_model\"$" "$codex_home/agents/ywc-typescript-reviewer.toml"
}

install_with_version "0.143.9" "gpt-5.4" "unsupported"
install_with_version "0.144.0" "gpt-5.6-terra" "supported"
install_with_version "0.144.4" "gpt-5.6-terra" "current"

echo "PASS: Codex agent model selection honors the GPT-5.6 CLI version threshold"
