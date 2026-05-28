#!/usr/bin/env bash
# Creates the docs/specification/ directory with empty section files.
# Usage: bash init-spec-structure.sh [lang] [project_name]
#   lang         : ko (default) | ja | en
#   project_name : used in README.md title (default: "Project")
# Exit 0: created successfully
# Exit 1: docs/specification/ already exists

set -euo pipefail

LANG="${1:-ko}"
PROJECT="${2:-Project}"
SPEC_DIR="docs/specification"
TODAY=$(date +%Y-%m-%d)

if [ -d "$SPEC_DIR" ]; then
  echo "[spec-writer] $SPEC_DIR already exists. Use --update to refresh." >&2
  exit 1
fi

mkdir -p "$SPEC_DIR"

case "$LANG" in
  ja) LANG_LABEL="Japanese" ;;
  en) LANG_LABEL="English" ;;
  *)  LANG_LABEL="Korean" ;;
esac

cat > "$SPEC_DIR/README.md" << EOF
# $PROJECT Specification
**Last updated**: $TODAY
**Language**: $LANG_LABEL

## Sections
- [Overview](01-overview.md)
- [Features](02-features.md)
- [Data](03-data.md)
- [Interfaces](04-interfaces.md)
- [User Flows](05-user-flows.md)
- [Requirements](06-requirements.md)
- [Glossary](07-glossary.md)

## Change Log
| Date | Section | Source | Summary |
|------|---------|--------|---------|
| $TODAY | All | --full | Initial structure created |
EOF

for section in 01-overview 02-features 03-data 04-interfaces 05-user-flows 06-requirements 07-glossary; do
  echo "# (To be written)" > "$SPEC_DIR/${section}.md"
done

echo "[spec-writer] Created $SPEC_DIR/ with 8 files (language: $LANG_LABEL)"
exit 0
