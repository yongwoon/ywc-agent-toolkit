#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)
resolver="$script_dir/resolve-bundle-executable.py"

if [ ! -f "$resolver" ]; then
  echo "BLOCKED: resolver launcher is missing its Python resolver: $resolver. Expected an installed Codex bundle or an authorized development source root." >&2
  exit 3
fi

exec python3 "$resolver" "$@"
