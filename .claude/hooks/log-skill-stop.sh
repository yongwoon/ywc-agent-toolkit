#!/usr/bin/env bash
#
# PostToolUse hook — record Skill tool invocations to .claude/logs/skill-stops.ndjson.
#
# Diagnostic logger for the "ctx 100%" / "stop right after LLM answer" symptoms.
# Each Skill invocation is captured as one NDJSON line so the next occurrence
# can be triaged to a specific skill + arg + response-snippet without
# re-instrumenting the harness.
#
# Failures are silent (exit 0) — this must never block tool execution.
# Output schema: { ts, event, tool, skill, args, response_snippet }
#
set -u

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}" 2>/dev/null || exit 0

log_dir=".claude/logs"
log_file="$log_dir/skill-stops.ndjson"

mkdir -p "$log_dir" 2>/dev/null || exit 0

input=$(cat 2>/dev/null) || exit 0
[[ -z "$input" ]] && exit 0

# Use jq if available; otherwise emit a minimal line so logging still works.
if command -v jq >/dev/null 2>&1; then
  printf '%s' "$input" \
    | jq -c '{
        ts: (now | todate),
        event: "PostToolUse:Skill",
        tool: (.tool_name // null),
        skill: (.tool_input.skill // null),
        args: ((.tool_input.args // "") | tostring | .[0:200]),
        response_snippet: ((.tool_response // "") | tostring | .[0:400])
      }' 2>/dev/null >> "$log_file" || true
else
  printf '{"ts":"%s","event":"PostToolUse:Skill","raw_input_bytes":%d}\n' \
    "$(date -u +%FT%TZ)" "${#input}" >> "$log_file" 2>/dev/null || true
fi

exit 0
