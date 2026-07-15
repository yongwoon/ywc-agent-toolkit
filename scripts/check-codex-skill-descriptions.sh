#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILLS_ROOT="$ROOT/codex/skills"
FIXTURE_ROOT="$ROOT/scripts/fixtures/codex-description-limit"
BASELINE_DOC="$ROOT/docs/ywc-plans/codex-skill-sdlc-v11-improvements.description-baseline.md"
LIMIT=500

MODE=""
PATH_FILTER=""
WRITE_BASELINE=0

usage() {
  cat <<'EOF'
Usage:
  bash scripts/check-codex-skill-descriptions.sh --fixtures
  bash scripts/check-codex-skill-descriptions.sh --report [--write-baseline]
  bash scripts/check-codex-skill-descriptions.sh --paths a-m|n-z
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --fixtures)
      MODE="fixtures"
      shift
      ;;
    --report)
      MODE="report"
      shift
      ;;
    --paths)
      MODE="paths"
      PATH_FILTER="${2:-}"
      [ -n "$PATH_FILTER" ] || { echo "ERROR: --paths requires a value" >&2; exit 2; }
      shift 2
      ;;
    --write-baseline)
      WRITE_BASELINE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[ -n "$MODE" ] || {
  usage >&2
  exit 2
}

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

count_unicode_chars() {
  perl -CSDA -Mutf8 -e '
    use open qw(:std :utf8);
    local $/;
    my $text = <STDIN>;
    print length($text);
  '
}

extract_description() {
  local file="$1"

  awk '
    function fail(msg, code) {
      failed = 1
      failure_code = code
      print msg
      exit code
    }

    NR == 1 {
      if ($0 != "---") {
        fail("missing frontmatter fence", 11)
      }
      in_frontmatter = 1
      next
    }

    in_frontmatter && $0 == "---" {
      closed_frontmatter = 1
      in_frontmatter = 0
      if (!saw_description) {
        fail("missing description field", 12)
      }
      if (collecting_block && !saw_block_line) {
        fail("malformed description block", 13)
      }
      gsub(/[[:space:]]+/, " ", description)
      sub(/^ /, "", description)
      sub(/ $/, "", description)
      print description
      exit 0
    }

    in_frontmatter {
      if (collecting_block) {
        if ($0 ~ /^[A-Za-z_][A-Za-z0-9_-]*:[[:space:]]*/) {
          collecting_block = 0
        } else if ($0 ~ /^[[:space:]]*$/) {
          description = description "\n"
          saw_block_line = 1
          next
        } else if ($0 ~ /^[[:space:]]+/) {
          line = $0
          sub(/^[[:space:]]+/, "", line)
          description = description "\n" line
          saw_block_line = 1
          next
        } else {
          fail("malformed description block", 13)
        }
      }

      if ($0 ~ /^description:[[:space:]]*/) {
        saw_description = 1
        rest = $0
        sub(/^description:[[:space:]]*/, "", rest)

        if (rest == ">" || rest == ">-" || rest == ">+") {
          collecting_block = 1
          saw_block_line = 0
          next
        }

        if (rest ~ /^\|/) {
          fail("unsupported description scalar style", 14)
        }

        description = rest
      }
      next
    }

    END {
      if (failed) {
        exit failure_code
      }
      if (!closed_frontmatter && !saw_description) {
        fail("missing description field", 12)
      }
      if (!closed_frontmatter && collecting_block && !saw_block_line) {
        fail("malformed description block", 13)
      }
      if (!closed_frontmatter) {
        fail("unclosed frontmatter fence", 15)
      }
    }
  ' "$file"
}

collect_skill_dirs() {
  find "$SKILLS_ROOT" -mindepth 1 -maxdepth 1 -type d -name 'ywc-*' | sort
}

in_partition() {
  local skill_name="$1"
  local short_name="${skill_name#ywc-}"
  local first_char="${short_name%%${short_name#?}}"

  case "$PATH_FILTER" in
    a-m) [[ "$first_char" =~ [a-m] ]] ;;
    n-z) [[ "$first_char" =~ [n-z] ]] ;;
    *)
      echo "ERROR: unsupported --paths range: $PATH_FILTER" >&2
      exit 2
      ;;
  esac
}

scan_skills() {
  local dir skill file desc count status rc

  while IFS= read -r dir; do
    [ -n "$dir" ] || continue
    skill="$(basename "$dir")"
    if [ "$MODE" = "paths" ] && ! in_partition "$skill"; then
      continue
    fi

    file="$dir/SKILL.md"
    set +e
    desc="$(extract_description "$file" 2>&1)"
    rc=$?
    set -e

    if [ "$rc" -ne 0 ]; then
      printf 'ERROR\t%s\t-\t%s\n' "$skill" "$desc"
      continue
    fi

    count="$(printf '%s' "$desc" | count_unicode_chars)"
    status="OK"
    if [ "$count" -gt "$LIMIT" ]; then
      status="OVER_LIMIT"
    fi
    printf '%s\t%s\t%s\t%s\n' "$status" "$skill" "$count" "$file"
  done < <(collect_skill_dirs)
}

fixture_case() {
  local name="$1"
  local expected="$2"
  local file="$FIXTURE_ROOT/$name/SKILL.md"
  local desc count rc

  set +e
  desc="$(extract_description "$file" 2>&1)"
  rc=$?
  set -e

  if [ "$rc" -ne 0 ]; then
    if [ "$expected" = "$desc" ]; then
      printf 'PASS fixture %s -> %s\n' "$name" "$desc"
      return 0
    fi
    printf 'FAIL fixture %s -> expected %s, got %s\n' "$name" "$expected" "$desc" >&2
    return 1
  fi

  count="$(printf '%s' "$desc" | count_unicode_chars)"
  if [ "$expected" = "$count" ]; then
    printf 'PASS fixture %s -> %s chars\n' "$name" "$count"
    return 0
  fi

  printf 'FAIL fixture %s -> expected %s, got %s\n' "$name" "$expected" "$count" >&2
  return 1
}

render_baseline() {
  local rows total ok_count over_count error_count

  rows="$(scan_skills)"
  total="$(printf '%s\n' "$rows" | sed '/^$/d' | wc -l | tr -d ' ')"
  ok_count="$(printf '%s\n' "$rows" | awk -F '\t' '$1 == "OK" { count++ } END { print count + 0 }')"
  over_count="$(printf '%s\n' "$rows" | awk -F '\t' '$1 == "OVER_LIMIT" { count++ } END { print count + 0 }')"
  error_count="$(printf '%s\n' "$rows" | awk -F '\t' '$1 == "ERROR" { count++ } END { print count + 0 }')"

  cat <<EOF
# Codex Skill Description Baseline

Generated from source Codex skills with:

\`\`\`bash
bash scripts/check-codex-skill-descriptions.sh --report
\`\`\`

- Scope: \`codex/skills/ywc-*/SKILL.md\`
- Limit: \`${LIMIT}\` Unicode characters after folded-description whitespace normalization
- Skills scanned: \`${total}\`
- Within limit: \`${ok_count}\`
- Over limit: \`${over_count}\`
- Frontmatter errors: \`${error_count}\`

| Skill | Unicode chars | Status |
|---|---:|---|
EOF

  printf '%s\n' "$rows" | while IFS=$'\t' read -r status skill count _path; do
    case "$status" in
      OK) printf '| `%s` | %s | ok |\n' "$skill" "$count" ;;
      OVER_LIMIT) printf '| `%s` | %s | over-limit |\n' "$skill" "$count" ;;
      ERROR) printf '| `%s` | - | frontmatter-error |\n' "$skill" ;;
    esac
  done

  cat <<'EOF'

## Re-run

```bash
bash scripts/check-codex-skill-descriptions.sh --report
```
EOF
}

run_report() {
  local actual
  actual="$(render_baseline)"

  if [ "$WRITE_BASELINE" -eq 1 ]; then
    mkdir -p "$(dirname "$BASELINE_DOC")"
    printf '%s\n' "$actual" > "$BASELINE_DOC"
    echo "WROTE: $BASELINE_DOC"
    return 0
  fi

  [ -f "$BASELINE_DOC" ] || {
    echo "ERROR: baseline document missing: $BASELINE_DOC" >&2
    echo "Run: bash scripts/check-codex-skill-descriptions.sh --report --write-baseline" >&2
    exit 1
  }

  if ! diff -u "$BASELINE_DOC" <(printf '%s\n' "$actual") >/dev/null; then
    echo "ERROR: baseline document drift detected: $BASELINE_DOC" >&2
    diff -u "$BASELINE_DOC" <(printf '%s\n' "$actual") || true
    exit 1
  fi

  printf '%s\n' "$actual"
  echo "PASS: baseline report matches $BASELINE_DOC"
}

run_paths() {
  local rows over_count error_count

  rows="$(scan_skills)"
  over_count="$(printf '%s\n' "$rows" | awk -F '\t' '$1 == "OVER_LIMIT" { count++ } END { print count + 0 }')"
  error_count="$(printf '%s\n' "$rows" | awk -F '\t' '$1 == "ERROR" { count++ } END { print count + 0 }')"

  printf '%s\n' "$rows"

  if [ "$over_count" -gt 0 ] || [ "$error_count" -gt 0 ]; then
    echo "FAIL: path partition $PATH_FILTER has $over_count over-limit skill(s) and $error_count frontmatter error(s)" >&2
    exit 1
  fi

  echo "PASS: path partition $PATH_FILTER is within the ${LIMIT}-character limit"
}

run_fixtures() {
  local failed=0

  fixture_case "500-pass" "500" || failed=1
  fixture_case "501-fail" "501" || failed=1
  fixture_case "missing-frontmatter" "missing frontmatter fence" || failed=1
  fixture_case "malformed-frontmatter" "unclosed frontmatter fence" || failed=1

  if [ "$failed" -ne 0 ]; then
    exit 1
  fi

  echo "PASS: all fixtures matched expected counts and errors"
}

case "$MODE" in
  fixtures) run_fixtures ;;
  report) run_report ;;
  paths) run_paths ;;
esac
