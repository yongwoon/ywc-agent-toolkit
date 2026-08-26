#!/usr/bin/env bash
# Atomically update one project or user YWC configuration field set.
set -euo pipefail

SCOPE=""
LANG_VALUE=""
INITIALS_VALUE=""
HAS_LANG=0
HAS_INITIALS=0

usage() {
  echo "usage: write-config.sh --scope <project|user> [--lang <value>] [--initials <value>]" >&2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --scope)
      [ "$#" -ge 2 ] || { echo "error: --scope requires an operand" >&2; usage; exit 2; }
      SCOPE="$2"
      shift 2
      ;;
    --lang)
      [ "$#" -ge 2 ] || { echo "error: --lang requires an operand" >&2; usage; exit 2; }
      LANG_VALUE="$2"
      HAS_LANG=1
      shift 2
      ;;
    --initials)
      [ "$#" -ge 2 ] || { echo "error: --initials requires an operand" >&2; usage; exit 2; }
      INITIALS_VALUE="$2"
      HAS_INITIALS=1
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown option or operand: $1" >&2
      usage
      exit 2
      ;;
  esac
done

case "$SCOPE" in
  project) TARGET="$(pwd -P)/.codex/ywc.json" ;;
  user) TARGET="${HOME:?}/.codex/ywc.json" ;;
  '') echo "error: --scope is required" >&2; usage; exit 2 ;;
  *) echo "error: scope must be project or user: $SCOPE" >&2; exit 2 ;;
esac

if [ "$HAS_LANG" -eq 0 ] && [ "$HAS_INITIALS" -eq 0 ]; then
  echo "error: at least one of --lang or --initials is required" >&2
  usage
  exit 2
fi

export YWC_CONFIG_TARGET="$TARGET"
export YWC_CONFIG_SCOPE="$SCOPE"
export YWC_CONFIG_LANG="$LANG_VALUE"
export YWC_CONFIG_INITIALS="$INITIALS_VALUE"
export YWC_CONFIG_HAS_LANG="$HAS_LANG"
export YWC_CONFIG_HAS_INITIALS="$HAS_INITIALS"

python3 - <<'PY'
import fcntl
import json
import os
import re
import tempfile

target = os.environ["YWC_CONFIG_TARGET"]
parent = os.path.dirname(target)
os.makedirs(parent, exist_ok=True)
lock_path = target + ".lock"
language_aliases = {
    "ko": "ko", "kr": "ko", "korean": "ko", "한국어": "ko",
    "ja": "ja", "japanese": "ja", "日本語": "ja",
    "en": "en", "english": "en",
    "zh": "zh", "chinese": "zh", "中文": "zh",
    "es": "es", "spanish": "es", "espanol": "es", "español": "es",
}

has_lang = os.environ["YWC_CONFIG_HAS_LANG"] == "1"
has_initials = os.environ["YWC_CONFIG_HAS_INITIALS"] == "1"
requested_lang = os.environ["YWC_CONFIG_LANG"]
requested_initials = os.environ["YWC_CONFIG_INITIALS"]

if has_lang and requested_lang not in language_aliases:
    raise SystemExit("error: unsupported language; use ko, ja, en, zh, or es")
if has_initials and re.fullmatch(r"[a-z0-9]{2,4}", requested_initials) is None:
    raise SystemExit("error: initials must match ^[a-z0-9]{2,4}$")

with open(lock_path, "a+", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    if os.path.exists(target):
        try:
            with open(target, encoding="utf-8") as source:
                config = json.load(source)
        except (OSError, json.JSONDecodeError) as exc:
            raise SystemExit(f"error: existing config is not valid JSON: {exc}")
        if not isinstance(config, dict):
            raise SystemExit("error: existing config must contain a JSON object")
    else:
        config = {}

    if has_lang:
        config["lang"] = language_aliases[requested_lang]
    if has_initials:
        config["initials"] = requested_initials

    fd, temporary = tempfile.mkstemp(prefix=f".{os.path.basename(target)}.", suffix=".tmp", dir=parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as destination:
            json.dump(config, destination, ensure_ascii=False, indent=2)
            destination.write("\n")
            destination.flush()
            os.fsync(destination.fileno())
        os.replace(temporary, target)
        dir_fd = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
        with open(target, encoding="utf-8") as result:
            written = json.load(result)
        if not isinstance(written, dict):
            raise SystemExit("error: replaced config is not a JSON object")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

print("Status: DONE")
print(f"Scope: {os.environ['YWC_CONFIG_SCOPE']}")
print(f"Path: {target}")
if has_lang:
    print(f"Language: {language_aliases[requested_lang]}")
if has_initials:
    print(f"Initials: {requested_initials}")
PY
