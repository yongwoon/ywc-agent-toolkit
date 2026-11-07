#!/usr/bin/env bash
# test-scan-secrets.sh — assert-based, no framework.
# Checks that scan-secrets.sh never reports "clean" when it could not scan:
# outside a git work tree and in a bare repository it must exit 2, and an
# unresolved script path must surface as a non-0/1 exit the caller reads as
# BLOCKED.
#
# Every git and scan call runs through no_git_env: the pre-commit hook runs
# scripts/validate.sh with GIT_DIR / GIT_INDEX_FILE / GIT_WORK_TREE set, and an
# inherited GIT_DIR would point these checks at the hook's repository.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/scan-secrets.sh"

PASS=0
FAIL=0

# Every throwaway directory lives under TMP_ROOT, removed on any exit.
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

no_git_env() {
  env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE "$@"
}

assert_eq() {
  local desc="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "FAIL: $desc — expected [$expected], got [$actual]" >&2
  fi
}

# Runs the scan from directory $1; GIT_CEILING_DIRECTORIES stops git from
# discovering a repository above TMP_ROOT (e.g. when TMPDIR is inside one).
run_scan() {
  (cd "$1" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --staged >/dev/null 2>&1)
  echo $?
}

# Fails if the not-a-work-tree guard is removed: every git call errors
# silently and the scan reports "OK" with exit 0.
NOREPO="$(mktemp -d "$TMP_ROOT/norepo.XXXXXX")"
assert_eq "outside a git work tree" "2" "$(run_scan "$NOREPO")"

# Fails if the guard only checks rev-parse's exit status: in a bare repo it
# exits 0 but prints "false".
BARE="$(mktemp -d "$TMP_ROOT/bare.XXXXXX")"
no_git_env git init -q --bare "$BARE/r.git"
assert_eq "bare repository" "2" "$(run_scan "$BARE/r.git")"

# Fails if callers could mistake an unresolved script path for a scan result:
# bash must exit 127 (not 0/1), which SKILL.md treats as BLOCKED. A nonexistent
# directory under TMP_ROOT stands in for the unresolved variable — an empty one
# would expand to /scan-secrets.sh, which depends on the host root.
UNRESOLVED="$TMP_ROOT/unresolved-skill-dir"
assert_eq "unresolved script path" "127" "$( (no_git_env bash "$UNRESOLVED/scan-secrets.sh" --staged >/dev/null 2>&1); echo $?)"

# --committed <base>: a base that cannot be scanned must exit 2, never "OK".
# Fixture: main has a clean commit; branch "feat" adds an AWS-key-shaped line
# (assembled at runtime so this file itself never contains the pattern).
REPO="$(mktemp -d "$TMP_ROOT/repo.XXXXXX")"
# A failed fixture step aborts the suite: a half-built repo would let the
# exit-2 cases pass without testing anything.
g() {
  (cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env git -c user.name=t -c user.email=t@example.invalid "$@" >/dev/null 2>&1) \
    || { echo "FIXTURE FAIL: git $*" >&2; exit 1; }
}
g init -q -b main
echo clean > "$REPO/a.txt"; g add a.txt; g commit -q -m base
g checkout -q -b clean-feat
echo "still clean" >> "$REPO/a.txt"; g commit -q -am clean
g checkout -q -b feat main
echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/b.txt"; g add b.txt; g commit -q -m secret

# The three guards (allowlist, rev-parse --verify, checked diff) back each
# other up, so each is isolated with a `git` shim on PATH:
#   SHIM_MODE=faildiff  — only the Phase 3 `git diff <base>...HEAD` fails
#   SHIM_MODE=passdiff  — only that diff always succeeds (empty output)
#   SHIM_MODE=passall   — `rev-parse --verify` and that diff always succeed
# Phase 1/2 git failures must not read as "clean" either:
#   SHIM_MODE=failstatus   — `git status` fails
#   SHIM_MODE=failcached   — `git diff --cached` fails
#   SHIM_MODE=failworktree — the unstaged `git diff` fails (`--cached` still works)
#   SHIM_MODE=failuntracked — `git ls-files --others` fails
#   SHIM_MODE=failcat       — `cat` (reading untracked files) fails
#   SHIM_MODE=failgrep      — `grep` exits 2 (an error, not "no match")
#   SHIM_MODE=failnames     — the Phase 3 `git log --name-only <base>..HEAD` fails
# A failing added-line filter must not read as "secrets found" (exit 1):
#   SHIM_MODE=failawk      — `awk` fails
SHIM="$TMP_ROOT/shim"; mkdir -p "$SHIM"
REAL_GIT="$(command -v git)"
cat > "$SHIM/git" <<EOF
#!/usr/bin/env bash
case "\${SHIM_MODE:-}:\$1:\$*" in
  faildiff:diff:*...HEAD*) exit 1 ;;
  passall:diff:*...HEAD*|passdiff:diff:*...HEAD*) exit 0 ;;
  passall:rev-parse:*--verify*) exit 0 ;;
  failstatus:status:*) exit 1 ;;
  failcached:diff:*--cached*) exit 1 ;;
  failworktree:diff:*--cached*) ;;
  failuntracked:ls-files:*--others*) exit 1 ;;
  failnames:log:*--name-only*) exit 1 ;;
  failworktree:diff:*) exit 1 ;;
esac
exec "$REAL_GIT" "\$@"
EOF
chmod +x "$SHIM/git"
REAL_AWK="$(command -v awk)"
cat > "$SHIM/awk" <<EOF
#!/usr/bin/env bash
[ "\${SHIM_MODE:-}" = failawk ] && exit 1
exec "$REAL_AWK" "\$@"
EOF
chmod +x "$SHIM/awk"
REAL_CAT="$(command -v cat)"
cat > "$SHIM/cat" <<EOF
#!/usr/bin/env bash
[ "\${SHIM_MODE:-}" = failcat ] && { echo "cat: injected failure" >&2; exit 1; }
exec "$REAL_CAT" "\$@"
EOF
chmod +x "$SHIM/cat"
REAL_GREP="$(command -v grep)"
cat > "$SHIM/grep" <<EOF
#!/usr/bin/env bash
[ "\${SHIM_MODE:-}" = failgrep ] && { echo "grep: memory exhausted" >&2; exit 2; }
exec "$REAL_GREP" "\$@"
EOF
chmod +x "$SHIM/grep"

ERR="$TMP_ROOT/scan.err"
# run_args <shim-mode> [args...] — prints the exit code; stderr kept in $ERR.
run_args() {
  local mode="$1"; shift
  (cd "$REPO" && SHIM_MODE="$mode" PATH="$SHIM:$PATH" GIT_CEILING_DIRECTORIES="$TMP_ROOT" \
    no_git_env bash "$TARGET" "$@" >/dev/null 2>"$ERR")
  echo $?
}
run_committed() { local mode="$1"; shift; run_args "$mode" --committed "$@"; }
assert_args() {
  local desc="$1" expected="$2"; shift 2
  local before=$FAIL
  assert_eq "$desc" "$expected" "$(run_args "$@")"
  [ "$FAIL" -eq "$before" ] || sed 's/^/    stderr: /' "$ERR" >&2
}
assert_committed() {
  local desc="$1" expected="$2"; shift 2
  local before=$FAIL
  assert_eq "$desc" "$expected" "$(run_committed "$@")"
  [ "$FAIL" -eq "$before" ] || sed 's/^/    stderr: /' "$ERR" >&2
}

# Fails if `shift 2` with a missing value exits 1 ("secrets found") under set -e.
assert_committed "--committed without a base" "2" ""
assert_committed "--committed unknown base" "2" "" no-such-branch
# Fails only if the rev-parse --verify guard is removed (passdiff diffs nothing).
assert_committed "--committed unknown base, diff succeeds" "2" passdiff no-such-branch
# Fails if Phase 3 swallows the diff error (`|| true`) again.
assert_committed "--committed diff failure" "2" faildiff main
# Each fails only if its own allowlist clause is removed (passall bypasses git).
assert_committed "--committed leading-dash base" "2" passall -x
assert_committed "--committed dot-dot base" "2" passall 'main..feat'
# shellcheck disable=SC2016  # the literal `$(id)` is the input under test
assert_committed "--committed shell-metachar base" "2" passall 'main$(id)'
# Positive cases: a resolvable base still detects (1) and still passes (0).
assert_committed "--committed secret vs valid base" "1" "" main
g checkout -q clean-feat
assert_committed "--committed clean vs valid base" "0" "" main
# Fails if the Phase 3 name-list walk swallows its error.
assert_committed "--committed name-list failure" "2" failnames main
# Phase 1 sees only the work tree: a .env committed on the branch (harmless
# content, clean tree) is caught only by the Phase 3 name check.
g checkout -q -b committed-env main
echo "X=1" > "$REPO/.env"; g add -f .env; g commit -q -m env
assert_committed "--committed .env file in the range" "1" "" main
# Deleting a .env that the base still has is a cleanup, not a leak: the name
# check skips deleted paths (--diff-filter=d).
g checkout -q -b drop-env
g rm -q .env; g commit -q -m drop-env
assert_committed "--committed deletion of a base .env" "0" "" committed-env
# A .env added and then deleted on the branch is absent from the net diff but
# still in the pushed history; only a per-commit walk catches it.
g checkout -q -b add-drop-env main
echo "X=1" > "$REPO/.env"; g add -f .env; g commit -q -m add-env
g rm -q .env; g commit -q -m drop-env
assert_committed "--committed .env added then deleted in the range" "1" "" main
# A file added only in a merge commit's resolution is flagged, while a base
# .env merged in unchanged is not (base-env is the base for both cases).
g checkout -q -b base-env main
echo "X=1" > "$REPO/.env.base"; g add -f .env.base; g commit -q -m base-env
g checkout -q -b merge-in-base main
echo y > "$REPO/side.txt"; g add side.txt; g commit -q -m side
g merge -q --no-ff --no-edit base-env
assert_committed "--committed base .env merged in unchanged" "0" "" base-env
g checkout -q -b evil-merge main
echo y > "$REPO/side.txt"; g add side.txt; g commit -q -m side
g merge -q --no-ff --no-commit base-env
echo "X=1" > "$REPO/.env"; g add -f .env; g commit -q -m evil-merge
assert_committed "--committed .env added in a merge resolution" "1" "" base-env
g checkout -q clean-feat

# Flag order: a later --staged must not downgrade --committed (Phase 3 would be
# skipped and the committed key reported as OK).
g checkout -q feat
assert_args "--committed then --staged keeps the committed scan" "1" "" --committed main --staged
assert_args "--staged then --committed" "1" "" --staged --committed main
# Phase 1/2: a failing git call means nothing was scanned (exit 2), not "clean".
g checkout -q clean-feat
assert_args "git status failure" "2" failstatus --staged
assert_args "git diff --cached failure" "2" failcached --staged
assert_args "unstaged git diff failure" "2" failworktree --staged
assert_args "added-line filter failure" "2" failawk --staged

# The user's git config must not hide changes from the scan.
g checkout -q feat
# Color codes before "+" stop the `^+` match.
g config color.ui always
assert_args "--committed with color.ui=always" "1" "" --committed main
g config --unset color.ui
# An external diff driver replaces the patch text.
g config diff.external true
assert_args "--committed with diff.external" "1" "" --committed main
g config --unset diff.external
# A textconv driver rewrites the file content before diffing.
echo "b.txt diff=hide" > "$REPO/.git/info/attributes"
g config diff.hide.textconv "sh -c :"
assert_args "--committed with a textconv driver" "1" "" --committed main
g config --remove-section diff.hide
: > "$REPO/.git/info/attributes"
g checkout -q clean-feat
# A staged secret, scanned with color forced on.
echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/c.txt"; g add c.txt
g config color.diff always
assert_args "--staged with color.diff=always" "1" "" --staged
g rm -q --cached c.txt; rm -f "$REPO/c.txt"
# An unstaged secret in a tracked file, same config.
echo "key=AKIA""ABCDEFGHIJKLMNOP" >> "$REPO/a.txt"
assert_args "unstaged change with color.diff=always" "1" "" --staged
g config --unset color.diff
g checkout -q -- a.txt
# Hidden untracked files would hide a new .env from Phase 1.
: > "$REPO/.env"
g config status.showUntrackedFiles no
assert_args "untracked .env with status.showUntrackedFiles=no" "1" "" --staged
g config --unset status.showUntrackedFiles
rm -f "$REPO/.env"
# A path marked binary (-diff) prints "Binary files differ" with no "+" lines.
echo "c.json -diff" > "$REPO/.git/info/attributes"
echo "{\"key\": \"AKIA""ABCDEFGHIJKLMNOP\"}" > "$REPO/c.json"; g add c.json
assert_args "--staged secret in a -diff (binary) path" "1" "" --staged
g rm -q --cached c.json; rm -f "$REPO/c.json"; : > "$REPO/.git/info/attributes"
# An added line whose content starts with "++" reads "+++" in the diff; a
# filter that drops every "+++" line as a file header misses it.
echo "++key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/d.txt"; g add d.txt
assert_args "--staged secret on a line starting with ++" "1" "" --staged
g rm -q --cached d.txt; rm -f "$REPO/d.txt"
g checkout -q -b plusplus main
echo "++key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/d.txt"; g add d.txt; g commit -q -m plusplus
assert_args "--committed secret on a line starting with ++" "1" "" --committed main
g checkout -q clean-feat
# "++ " content reads "+++ " — exactly a header — so dropping only "+++ "
# lines still misses it.
echo "++ key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/d.txt"; g add d.txt
assert_args "--staged secret on a line starting with '++ '" "1" "" --staged
g rm -q --cached d.txt; rm -f "$REPO/d.txt"
g checkout -q -b plusplus-space main
echo "++ key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/d.txt"; g add d.txt; g commit -q -m plusplus-space
assert_args "--committed secret on a line starting with '++ '" "1" "" --committed main
g checkout -q clean-feat
# The password pattern must match both quote styles (assembled at runtime so
# this file never contains the pattern).
echo "pass""word = 'hunter22x'" > "$REPO/p.txt"; g add p.txt
assert_args "--staged single-quoted password" "1" "" --staged
echo 'pass''word = "hunter22x"' > "$REPO/p.txt"; g add p.txt
assert_args "--staged double-quoted password" "1" "" --staged
g rm -q -f --cached p.txt; rm -f "$REPO/p.txt"
# More matches than a pipe buffer holds: `head` closing the pipe early made the
# preview exit 141 under pipefail, read as "not scanned" instead of "found".
for _ in $(seq 1 5000); do echo "key=AKIA""ABCDEFGHIJKLMNOP"; done > "$REPO/many.txt"; g add many.txt
assert_args "--staged secret matches larger than a pipe buffer" "1" "" --staged
g rm -q -f --cached many.txt; rm -f "$REPO/many.txt"
# Quoted paths (space, non-ASCII) must still match the dangerous-name patterns.
mkdir -p "$REPO/x y"; : > "$REPO/x y/server.pem"
assert_args "untracked dangerous file under a path with a space" "1" "" --staged
rm -rf "$REPO/x y"
mkdir -p "$REPO/日本"; : > "$REPO/日本/.env"
assert_args "untracked .env under a non-ASCII path" "1" "" --staged
rm -rf "${REPO:?}/日本"
# Untracked file content: Step 3 runs before the commit stages new files, so
# each fails if the untracked-content scan is removed (the names are harmless).
mkdir -p "$REPO/src"; echo "const k = 'AKIA""ABCDEFGHIJKLMNOP';" > "$REPO/src/config.ts"
assert_args "untracked file with a secret" "1" "" --staged
rm -rf "${REPO:?}/src"
mkdir -p "$REPO/x y"; echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/x y/設定.ts"
assert_args "untracked secret under a space / non-ASCII path" "1" "" --staged
# Fails if an untracked-scan failure reads as "clean" (needs a file to diff).
echo "plain" > "$REPO/x y/設定.ts"
assert_args "clean untracked file" "0" "" --staged
assert_args "untracked enumeration failure" "2" failuntracked --staged
assert_args "untracked file read failure" "2" failcat --staged
assert_args "grep error is not 'no match'" "2" failgrep --staged
rm -rf "$REPO/x y"
# A nested repository or a directory symlink is skipped, never an error; a
# symlink contributes its target path, as git would commit it.
mkdir -p "$REPO/nested"; (cd "$REPO/nested" && no_git_env git init -q)
echo "plain" > "$REPO/nested/f.txt"; ln -s nested "$REPO/dirlink"
assert_args "untracked nested repo and directory symlink" "0" "" --staged
ln -s "AKIA""ABCDEFGHIJKLMNOP" "$REPO/keylink"
assert_args "untracked symlink whose target is a secret" "1" "" --staged
rm -rf "${REPO:?}/nested" "$REPO/dirlink" "$REPO/keylink"
# `cat -- -` reads stdin, so a file named `-` must be passed as `./-`.
echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/-"
assert_args "untracked file named '-'" "1" "" --staged
rm -f -- "$REPO/-"
# Fails if each untracked file costs its own process again: ~1,800 files used to
# hit the 120 s Bash timeout. 2,000 files must finish well inside 30 s.
mkdir -p "$REPO/many"
for i in $(seq 1 2000); do echo "line $i" > "$REPO/many/f$i.txt"; done
STARTED=$(date +%s)
assert_args "2,000 untracked clean files" "0" "" --staged
assert_eq "2,000 untracked files scanned in under 30 s" "1" "$(( $(date +%s) - STARTED < 30 ? 1 : 0 ))"
echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/many/f2000.txt"
assert_args "secret in the last of 2,000 untracked files" "1" "" --staged
rm -rf "${REPO:?}/many"
# Every SECRET_PATTERNS entry needs a positive case, and the report must never
# echo the value. Samples are assembled at runtime so this file never contains
# a pattern; each tail is the part that must be redacted.
rep() { local out="" i; for ((i = 0; i < $2; i++)); do out="$out$1"; done; printf '%s' "$out"; }
SAMPLES=(
  "AK""IA$(rep A 16)"
  "sk""-$(rep a 40)"
  "sk""-ant-api03-$(rep a 30)"
  "sk""-proj-$(rep a 30)"
  "gh""p_$(rep a 36)" "gh""o_$(rep a 36)" "gh""u_$(rep a 36)" "gh""s_$(rep a 36)" "gh""r_$(rep a 36)"
  "github""_pat_$(rep a 82)"
  "gl""pat-$(rep a 20)"
  "sk""_live_$(rep a 30)"
  "xo""xb-$(rep 1 11)-$(rep 2 11)-$(rep a 24)"
  "xo""xp-$(rep 1 11)-$(rep a 10)"
  "AI""za$(rep a 35)"
  "-----BEGIN RSA PRI""VATE KEY-----"
  "-----BEGIN PRI""VATE KEY-----"
  "pass""word = \"hunter22x\""
  "DATABASE""_URL=postgres://u:hunter22x@db/app"
)
OUT="$TMP_ROOT/scan.out"
for SAMPLE in "${SAMPLES[@]}"; do
  echo "x=$SAMPLE" > "$REPO/sample.txt"
  RC=0
  (cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --staged >"$OUT" 2>&1) || RC=$?
  assert_eq "pattern detects ${SAMPLE:0:12}" "1" "$RC"
  # The secret's tail (last 8 chars) must not appear outside the pattern header
  # lines; [REDACTED] must.
  assert_eq "report redacts ${SAMPLE:0:12}" "0:1" \
    "$(grep -v '^SECRET DETECTED' "$OUT" | grep -cF -- "${SAMPLE: -8}" | tr -d ' '):$(grep -c '\[REDACTED\]' "$OUT" | sed 's/^[1-9][0-9]*$/1/')"
done
# Two secrets on one line: redacting from one pattern's match must not leave
# the other, earlier secret in the printed prefix.
TWO_A="AK""IA$(rep Q 16)"; TWO_B="DATABASE""_URL=postgres://u:zz9@db"
echo "a=$TWO_A $TWO_B" > "$REPO/sample.txt"
(cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --staged >"$OUT" 2>&1)
assert_eq "two secrets on one line are both redacted" "0" \
  "$(grep -v '^SECRET DETECTED' "$OUT" | grep -cF -e "$(rep Q 16)" -e "zz9@db" | tr -d ' ')"
rm -f "$REPO/sample.txt"
# A conflicted merge's unstaged diff is combined (`diff --cc`): a line kept from
# HEAD's side reads " +line" and must count as added like "++" and "+ ".
g checkout -q -b cc-theirs main
echo "theirs" > "$REPO/cc.txt"; g add cc.txt; g commit -q -m theirs
g checkout -q -b cc-ours main
printf 'ours\nkey=%s\n' "AKIA""ABCDEFGHIJKLMNOP" > "$REPO/cc.txt"; g add cc.txt; g commit -q -m ours
(cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env git merge -q cc-theirs >/dev/null 2>&1) || true
assert_eq "conflicted merge leaves a combined diff" "1" \
  "$( (cd "$REPO" && no_git_env git diff | grep -c '^ +key=') )"
assert_args "--staged secret on a ' +' combined-diff line" "1" "" --staged
# Dropping that line in the resolution reads "- key=…": a removed line, not added.
printf '<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> cc-theirs\n' > "$REPO/cc.txt"
assert_eq "combined diff shows the dropped line as '- '" "1" \
  "$( (cd "$REPO" && no_git_env git diff | grep -c '^- key=') )"
assert_args "--staged secret only on a '- ' combined-diff line" "0" "" --staged
(cd "$REPO" && no_git_env git merge --abort >/dev/null 2>&1)
g checkout -q clean-feat
# Fails if a binary untracked file (NUL bytes, invalid UTF-8) breaks the
# filter under a UTF-8 locale (bash drops NULs, BSD awk aborts on multibyte
# input, GNU grep treats the stream as binary and prints no matching line).
# The locale must be installed or the shell silently falls back to C and the
# cases cannot fail; Ubuntu names it C.utf8, macOS en_US.UTF-8 / C.UTF-8.
UTF8_LOCALE=$(locale -a 2>/dev/null | grep -iE '^(C|en_US)\.utf-?8$' | sed -n 1p || true)
if [ -z "$UTF8_LOCALE" ]; then
  echo "SKIP: no UTF-8 locale installed; binary-file cases not run" >&2
else
  run_utf8() {
    (cd "$REPO" && LC_ALL="$UTF8_LOCALE" GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --staged >/dev/null 2>&1)
    echo $?
  }
  { printf '\000\377\376\200'; head -c 4096 /dev/urandom; } > "$REPO/img.bin"
  assert_eq "untracked binary file under $UTF8_LOCALE" "0" "$(run_utf8)"
  echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/notes.txt"
  assert_eq "untracked secret next to a binary file under $UTF8_LOCALE" "1" "$(run_utf8)"
  rm -f "$REPO/img.bin" "$REPO/notes.txt"
  # Invalid bytes and a secret in the same file.
  { printf '\377\376\200\n'; echo "key=AKIA""ABCDEFGHIJKLMNOP"; } > "$REPO/mixed.bin"
  assert_eq "invalid bytes followed by a secret under $UTF8_LOCALE" "1" "$(run_utf8)"
  rm -f "$REPO/mixed.bin"
fi
# diff.relative=true limits every diff to the current directory.
g checkout -q feat
mkdir -p "$REPO/sub"
g config diff.relative true
assert_eq "--committed from a subdirectory with diff.relative=true" "1" \
  "$( (cd "$REPO/sub" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --committed main >/dev/null 2>&1); echo $?)"
g config --unset diff.relative
rmdir "$REPO/sub"
g checkout -q clean-feat

echo ""
echo "test-scan-secrets.sh: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
