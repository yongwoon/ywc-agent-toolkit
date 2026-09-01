#!/usr/bin/env bash
# Verdict checks for resolve-language.sh; no network access required.
#
# Fixture CLAUDE.md files live in a temp dir and are injected via
# YWC_PROJECT_CLAUDE_MD / YWC_USER_CLAUDE_MD so real project/user files are
# never touched.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SCRIPT_DIR/resolve-language.sh"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

NO_PROJECT="$TEMP_DIR/no-project-CLAUDE.md"
NO_USER="$TEMP_DIR/no-user-CLAUDE.md"

resolve() {
  YWC_PROJECT_CLAUDE_MD="${YWC_PROJECT_CLAUDE_MD:-$NO_PROJECT}" \
    YWC_USER_CLAUDE_MD="${YWC_USER_CLAUDE_MD:-$NO_USER}" \
    bash "$SCRIPT" "$@"
}

# AC1: --lang flag normalizes a full name (case-insensitive) and wins outright.
OUTPUT="$(resolve --lang Japanese)"
[ "$OUTPUT" = "ja" ] || { echo "AC1 failed: expected ja, got: $OUTPUT" >&2; exit 1; }

# AC2: no --lang, no policy anywhere -> UNRESOLVED, never a hardcoded 'en'.
OUTPUT="$(resolve)"
[ "$OUTPUT" = "UNRESOLVED" ] || { echo "AC2 failed: expected UNRESOLVED, got: $OUTPUT" >&2; exit 1; }

# AC3: project policy (ko) and user policy (ja) both present -> project wins.
cat > "$TEMP_DIR/project-CLAUDE.md" <<'EOF'
# Project

## Language Policy

- **Output language**: ko   <!-- one of: ko | ja | en | es | zh -->
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
EOF
cat > "$TEMP_DIR/user-CLAUDE.md" <<'EOF'
# User

## Language Policy

- **Output language**: ja   <!-- one of: ko | ja | en | es | zh -->
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
EOF
OUTPUT="$(YWC_PROJECT_CLAUDE_MD="$TEMP_DIR/project-CLAUDE.md" YWC_USER_CLAUDE_MD="$TEMP_DIR/user-CLAUDE.md" resolve)"
[ "$OUTPUT" = "ko" ] || { echo "AC3 failed: expected ko (project wins), got: $OUTPUT" >&2; exit 1; }

# User-only policy resolves when project has none.
OUTPUT="$(YWC_USER_CLAUDE_MD="$TEMP_DIR/user-CLAUDE.md" resolve)"
[ "$OUTPUT" = "ja" ] || { echo "user-only fallback failed: expected ja, got: $OUTPUT" >&2; exit 1; }

# E1: malformed Output-language value falls through to the next rung
# instead of erroring (here, all the way to UNRESOLVED).
cat > "$TEMP_DIR/malformed-CLAUDE.md" <<'EOF'
## Language Policy

- **Output language**: xx
EOF
OUTPUT="$(YWC_PROJECT_CLAUDE_MD="$TEMP_DIR/malformed-CLAUDE.md" resolve)"
[ "$OUTPUT" = "UNRESOLVED" ] || { echo "malformed-policy fallthrough failed: got: $OUTPUT" >&2; exit 1; }

# E3: a second '## Language Policy' heading in the same file is treated as
# absent, not as "first one wins".
cat > "$TEMP_DIR/duplicate-CLAUDE.md" <<'EOF'
## Language Policy

- **Output language**: ko

## Language Policy

- **Output language**: ja
EOF
OUTPUT="$(YWC_PROJECT_CLAUDE_MD="$TEMP_DIR/duplicate-CLAUDE.md" resolve)"
[ "$OUTPUT" = "UNRESOLVED" ] || { echo "duplicate-section fallthrough failed: got: $OUTPUT" >&2; exit 1; }

# --emit-section reproduces the canonical block from language-resolution.md:47-53.
EXPECTED="## Language Policy

- **Output language**: es   <!-- one of: ko | ja | en | es | zh -->
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms."
OUTPUT="$(bash "$SCRIPT" --emit-section es)"
[ "$OUTPUT" = "$EXPECTED" ] || { echo "--emit-section mismatch, got:" >&2; echo "$OUTPUT" >&2; exit 1; }

echo "resolve-language.sh verdict checks passed"
