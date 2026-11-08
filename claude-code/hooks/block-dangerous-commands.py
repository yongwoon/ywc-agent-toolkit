#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Block Dangerous Commands - PreToolUse Hook for Bash
Blocks dangerous shell patterns before execution.
Logs to: ~/.claude/hooks-logs/YYYY-MM-DD.jsonl

SAFETY_LEVEL: 'critical' | 'high' | 'strict'
  critical - Only catastrophic: rm -rf ~, dd to disk, fork bombs
  high     - + risky: force push main, secrets exposure, git reset --hard
  strict   - + cautionary: any force push, sudo rm, docker prune
"""

import json
import re
import shlex
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

SAFETY_LEVEL = "high"


@dataclass(frozen=True)
class Pattern:
    level: str
    id: str
    regex: re.Pattern
    reason: str


PATTERNS: list[Pattern] = [
    # CRITICAL — catastrophic, unrecoverable
    Pattern("critical", "rm-home",          re.compile(r'\brm\s+(?:-\S+\s+)*["\']?~(?:\/[^;&|]*)?["\']?(?:\s|$|[;&|])'),          "rm targeting home directory"),
    Pattern("critical", "rm-home-var",      re.compile(r'\brm\s+(?:-\S+\s+)*["\']?\$HOME(?:\/[^;&|]*)?["\']?(?:\s|$|[;&|])'),     "rm targeting $HOME"),
    Pattern("critical", "rm-home-trailing", re.compile(r'\brm\s+.+\s+["\']?(~\/?|\$HOME)["\']?(\s*$|[;&|])'),                      "rm with trailing ~/ or $HOME"),
    Pattern("critical", "rm-root",          re.compile(r'\brm\s+(-.+\s+)*\/(\*|\s|$|[;&|])'),                                      "rm targeting root filesystem"),
    Pattern("critical", "rm-system",        re.compile(r'\brm\s+(-.+\s+)*\/(etc|usr|var|bin|sbin|lib|boot|dev|proc|sys)(\/|\s|$)'), "rm targeting system directory"),
    Pattern("critical", "rm-cwd",           re.compile(r'\brm\s+(-.+\s+)*(\.\/?|\*|\.\/\*)(\s|$|[;&|])'),                          "rm deleting current directory contents"),
    Pattern("critical", "dd-disk",          re.compile(r'\bdd\b.+of=\/dev\/(sd[a-z]|nvme|hd[a-z]|vd[a-z]|xvd[a-z])'),             "dd writing to disk device"),
    Pattern("critical", "mkfs",             re.compile(r'\bmkfs(\.\w+)?\s+\/dev\/(sd[a-z]|nvme|hd[a-z]|vd[a-z])'),                "mkfs formatting disk"),
    Pattern("critical", "fork-bomb",        re.compile(r':\(\)\s*\{.*:\s*\|\s*:.*&'),                                              "fork bomb detected"),
    # HIGH — significant risk, data loss, security
    Pattern("high", "curl-pipe-sh",         re.compile(r'\b(curl|wget)\b.+\|\s*(?:sudo\s+)?(?:\S+/)?(ba)?sh\b'),                   "piping URL to shell (RCE risk)"),
    Pattern("high", "git-force-main",       re.compile(r'\bgit\s+push\b(?!.+--force-with-lease)(?=.+(--force|-f)\b)(?=.+\b(main|master)\b)'), "force push to main/master"),
    Pattern("high", "git-reset-hard",       re.compile(r'\bgit\s+reset\s+--hard'),                                                 "git reset --hard loses uncommitted work"),
    Pattern("high", "git-clean-f",          re.compile(r'\bgit\s+clean\s+(-\w*f|-f)'),                                             "git clean -f deletes untracked files"),
    Pattern("high", "chmod-777",            re.compile(r'\bchmod\b.+\b777\b'),                                                     "chmod 777 is a security risk"),
    Pattern("high", "cat-env",              re.compile(r'\b(cat|less|head|tail|more)\s+\.env\b'),                                  "reading .env file exposes secrets"),
    Pattern("high", "cat-secrets",          re.compile(r'\b(cat|less|head|tail|more)\b.+(credentials|secrets?|\.pem|\.key|id_rsa|id_ed25519)', re.IGNORECASE), "reading secrets file"),
    Pattern("high", "env-dump",             re.compile(r'\b(printenv|env)\b\s*([;&|]|$)'),                                         "env dump may expose secrets"),
    Pattern("high", "echo-secret",          re.compile(r'\becho\b.+\$\w*(SECRET|KEY|TOKEN|PASSWORD|API_|PRIVATE)', re.IGNORECASE), "echoing secret variable"),
    Pattern("high", "docker-vol-rm",        re.compile(r'\bdocker\s+volume\s+(rm|prune)'),                                         "docker volume deletion loses data"),
    Pattern("high", "rm-ssh",               re.compile(r'\brm\b.+\.ssh\/(id_|authorized_keys|known_hosts)'),                       "deleting SSH keys"),
    # STRICT — cautionary, context-dependent
    Pattern("strict", "git-force-any",      re.compile(r'\bgit\s+push\b(?!.+--force-with-lease).+(--force|-f)\b'),                 "force push (use --force-with-lease)"),
    Pattern("strict", "git-checkout-dot",   re.compile(r'\bgit\s+checkout\s+\.'),                                                  "git checkout . discards changes"),
    Pattern("strict", "sudo-rm",            re.compile(r'\bsudo\s+rm\b'),                                                          "sudo rm has elevated privileges"),
    Pattern("strict", "docker-prune",       re.compile(r'\bdocker\s+(system|image)\s+prune'),                                      "docker prune removes images"),
    Pattern("strict", "crontab-r",          re.compile(r'\bcrontab\s+-r'),                                                         "removes all cron jobs"),
]

LEVELS: dict[str, int] = {"critical": 1, "high": 2, "strict": 3}
EMOJIS: dict[str, str] = {"critical": "🚨", "high": "⛔", "strict": "⚠️"}
LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log(data: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps({"ts": datetime.now().isoformat(), "hook": "block-dangerous-commands", **data}) + "\n")
    except Exception:
        pass


def check_command(cmd: str, safety_level: str = SAFETY_LEVEL) -> Pattern | None:
    threshold = LEVELS.get(safety_level, 2)
    for p in PATTERNS:
        if LEVELS[p.level] <= threshold and p.regex.search(cmd):
            return p
    return None


# ---- Segment-scoped rules ----------------------------------------------------
# Whole-string regexes match a flag anywhere on the line, so `grep -n` next to
# `git commit` looks like `git commit -n`. These rules tokenize each command
# segment and look only at the argv of the command they target.

@dataclass(frozen=True)
class Rule:
    level: str
    id: str
    decision: str  # "deny" | "ask"
    reason: str


NO_VERIFY = Rule("high", "git-no-verify", "deny", "skipping git hooks (--no-verify / commit -n)")
GH_ADMIN = Rule("high", "gh-merge-admin", "deny", "gh pr merge --admin bypasses branch protection")
GIT_ADD_ALL = Rule("high", "git-add-all", "ask", "git add -A / . stages every file; stage explicit paths")

HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
SEPARATOR_CHARS = set(";&|()\n")
REDIRECT_CHARS = set("<>&")
SUBSTITUTION = re.compile(r"\$\((.*)\)|`([^`]*)`", re.S)
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--config-env"}
GH_OPTS_WITH_VALUE = {"-R", "--repo"}
COMMIT_SHORT_WITH_VALUE = set("mFCct")  # the rest of the cluster (or the next word) is the value
COMMIT_SHORT_OPTIONAL_VALUE = set("Su")  # only an attached value: -S<keyid>, -u<mode>
# wrapper → its options that take a separate value
WRAPPERS: dict[str, set[str]] = {
    "env": {"-u", "-C", "-S", "--unset", "--chdir", "--split-string"},
    "sudo": {"-u", "-g", "-h", "-p", "-C", "-D", "-U", "--user", "--group"},
    "command": set(), "time": set(), "nohup": set(), "exec": set(),
    "nice": {"-n"}, "xargs": {"-I", "-n", "-L", "-P", "-d", "-E", "-s", "-a"},
    "timeout": {"-s", "-k", "--signal", "--kill-after"}, "stdbuf": {"-i", "-o", "-e"},
    "ionice": {"-c", "-n", "-p"}, "doas": {"-u", "-C"}, "chronic": set(), "caffeinate": set(),
}
WRAPPER_POSITIONALS = {"timeout": 1}  # `timeout 5 git ...`: the duration precedes the command
# Shell words that can precede a command in the same segment.
RESERVED_WORDS = {"{", "}", "!", "if", "then", "else", "elif", "fi", "do", "done", "while", "until", "time"}


def strip_heredocs(cmd: str) -> str:
    """Drop heredoc bodies; their text is data, not argv."""
    out: list[str] = []
    pending: list[str] = []
    for line in cmd.split("\n"):
        if pending:
            if line.strip() == pending[0]:
                pending.pop(0)
            continue
        out.append(line)
        pending = [m.group(2) for m in HEREDOC.finditer(line)]
    return "\n".join(out)


ANSI_C_ESCAPE = re.compile(r"\\(x[0-9A-Fa-f]{1,2}|u[0-9A-Fa-f]{1,4}|U[0-9A-Fa-f]{1,8}|[0-7]{1,3}|c.|.)", re.S)
ANSI_C_SIMPLE = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n", "r": "\r",
                 "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"', "?": "?"}


def decode_ansi_c(body: str) -> str | None:
    """Decode a `$'...'` body by bash's rules; None when it cannot be decoded (caller fails closed)."""
    def repl(m: re.Match) -> str:
        e = m.group(1)
        if e[0] in "xuU" and len(e) > 1:
            n = int(e[1:], 16)
            return chr(n) if n <= 0x10FFFF and not 0xD800 <= n <= 0xDFFF else "�"
        if e[0] in "01234567":
            return chr(int(e, 8) & 0xFF)
        if e[0] == "c" and len(e) > 1:
            c = e[1].upper() if "a" <= e[1] <= "z" else e[1]
            return chr((ord(c) ^ 0x40) % 0x110000)
        return ANSI_C_SIMPLE.get(e, "\\" + e)  # unknown escapes (and bare \x) stay literal, as in bash
    try:
        return ANSI_C_ESCAPE.sub(repl, body).split("\0", 1)[0]  # bash stops at NUL
    except Exception:  # the decoder is total; this only guards against a bug in it
        return None


COMMENT_PRECEDERS = " \t\r\n;&|()<>"  # characters after which an unquoted `#` starts a comment in bash


def drop_dollar_quotes(text: str) -> str | None:
    """`$'...'` / `$"..."` → plain quotes wherever bash would read them (`--$'no-verify'` too),
    but not inside single or double quotes, where `$'` is literal text."""
    out: list[str] = []
    quote = ""
    escaped_end = -1  # index just after a backslash escape: a `#` there is not at a word start
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and quote != "'":
            out.append(text[i:i + 2])
            i += 2
            escaped_end = i
            continue
        if not quote and ch == "#" and i != escaped_end and (i == 0 or text[i - 1] in COMMENT_PRECEDERS):
            # A comment runs to the newline, which stays as the command separator. Dropping it here
            # keeps its quotes (`don't`) out of the quote tracking and leaves mid-word `#` alone.
            nl = text.find("\n", i)
            i = len(text) if nl == -1 else nl
            continue
        if not quote and text[i:i + 2] == "$'":
            # ANSI-C quoting: decode escapes the way bash does (`$'\x2dn'` → `-n`), re-quote literally.
            j = i + 2
            while j < len(text) and text[j] != "'":
                j += 2 if text[j] == "\\" else 1
            body = decode_ansi_c(text[i + 2:j])
            if body is None:
                return None
            out.append("'" + body.replace("'", "'\\''") + "'")
            i = j + 1
            continue
        if not quote and text[i:i + 2] == '$"':
            i += 1
            continue
        if ch in ("'", '"') and quote in ("", ch):
            quote = "" if quote else ch
        out.append(ch)
        i += 1
    return "".join(out)


def segments(cmd: str) -> list[list[str]] | None:
    """argv per command segment, or None when the command cannot be tokenized.

    The whole command is tokenized at once, so a quoted string may span lines;
    an unquoted newline separates commands like `;` does.
    """
    text = strip_heredocs(cmd).replace("\\\n", " ")  # line continuations
    text = drop_dollar_quotes(text)
    if text is None:
        return None  # undecodable $'...' → caller uses the whole-string fallback
    lex = shlex.shlex(text, posix=True, punctuation_chars="();<>|&\n")
    lex.whitespace = " \t\r"
    lex.commenters = ""  # comments are removed in drop_dollar_quotes; shlex would also eat mid-word `#` and the newline
    lex.whitespace_split = True
    result: list[list[str]] = []
    argv: list[str] = []
    try:
        for tok in lex:
            chars = set(tok)
            is_operator = bool(tok) and chars <= SEPARATOR_CHARS | REDIRECT_CHARS
            if is_operator and chars & set("<>") and not chars & set("()"):
                continue  # redirection operator; `<(` / `>(` start a process substitution
            if is_operator:
                if argv:
                    result.append(argv)
                argv = []
                continue
            argv.append(tok)
    except ValueError:
        return None
    if argv:
        result.append(argv)
    return result


def strip_prefix(argv: list[str]) -> list[str]:
    """Skip leading VAR=value assignments and wrappers (env, sudo, xargs, ...) with their options."""
    i = 0
    while i < len(argv):
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", argv[i]) or argv[i] in RESERVED_WORDS:
            i += 1
        elif argv[i].rsplit("/", 1)[-1] in WRAPPERS:
            name = argv[i].rsplit("/", 1)[-1]
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in WRAPPERS[name] else 1
            i += WRAPPER_POSITIONALS.get(name, 0)
        else:
            break
    return argv[i:]


def skip_options(argv: list[str], with_value: set[str]) -> list[str]:
    """argv after the command name, minus leading options (and their separate values)."""
    i = 1
    while i < len(argv) and argv[i].startswith("-"):
        i += 2 if argv[i] in with_value else 1
    return argv[i:]


def is_no_verify(arg: str) -> bool:
    # git accepts any unambiguous prefix; `--no-ve` would also match `--no-verbose`.
    return arg.startswith("--no-veri") and "--no-verify".startswith(arg)


def commit_skips_hooks(args: list[str]) -> bool:
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            return False
        if is_no_verify(a):
            return True
        if re.match(r"^-[A-Za-z]", a):
            for j, ch in enumerate(a[1:]):
                if ch == "n":
                    return True
                if ch in COMMIT_SHORT_OPTIONAL_VALUE:
                    break
                if ch in COMMIT_SHORT_WITH_VALUE:
                    if j == len(a) - 2:  # the value is the next word
                        i += 1
                    break
        i += 1
    return False


def adds_everything(args: list[str]) -> bool:
    cut = args.index("--") if "--" in args else len(args)
    opts, paths = args[:cut], args[cut + 1:] if cut < len(args) else args
    return "--all" in opts or any(re.match(r"^-[A-Za-z]*A", a) for a in opts) or "." in paths


ENV_SHORT_WITH_VALUE = set("uCS")


def env_split_strings(argv: list[str]) -> list[str]:
    """Split strings of every `env` word (`sudo env -S ...`, `timeout 5 env -S ...`)."""
    return [s for k, w in enumerate(argv) if w.rsplit("/", 1)[-1] == "env"
            for s in [env_split_string(argv, k + 1)] if s is not None]


def env_split_string(argv: list[str], i: int) -> str | None:
    """The command line an `env -S` / `--split-string` runs, parsed like getopt from
    env's own options starting at argv[i] (`-iS'...'`, `--split=...` prefixes)."""
    while i < len(argv) and argv[i].startswith("-") and argv[i] != "--":
        a = argv[i]
        if a.startswith("--"):
            opt, _, val = a.partition("=")
            if len(opt) >= 3 and "--split-string".startswith(opt):
                value = val if "=" in a else (argv[i + 1] if i + 1 < len(argv) else "")
                return env_unescape(value) + " " + " ".join(argv[i + (1 if "=" in a else 2):])
            # getopt_long: --u and --c are already unique among env's long options
            takes_value = len(opt) >= 3 and ("--unset".startswith(opt) or "--chdir".startswith(opt))
            i += 2 if takes_value and "=" not in a else 1
            continue
        for j, ch in enumerate(a[1:], 1):
            if ch in ENV_SHORT_WITH_VALUE:
                attached = a[j + 1:]
                value = attached or (argv[i + 1] if i + 1 < len(argv) else "")
                if ch == "S":
                    return env_unescape(value) + " " + " ".join(argv[i + (1 if attached else 2):])
                i += 0 if attached else 1
                break
        i += 1
    return None


ENV_ESCAPES = {"_": " ", "t": "\t", "n": "\n", "r": "\r", "f": "\f", "v": "\v",
               "\\": "\\\\", "#": "#", "$": "\\$", '"': '\\"', "'": "\\'"}


def env_unescape(s: str) -> str:
    """env -S escapes, left to right: `\\_` → space, `\\c` stops, `\\\\` stays one escaped
    backslash for the tokenizer; unknown escapes are kept as written."""
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            ch = s[i + 1]
            if ch == "c":
                break
            out.append(ENV_ESCAPES.get(ch, s[i:i + 2]))
            i += 2
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def nested_commands(argv: list[str]) -> list[str]:
    """Command text this segment runs indirectly: `bash -c`, `eval`, `$(...)`, backticks."""
    nested = [m.group(1) or m.group(2) or "" for m in SUBSTITUTION.finditer(" ".join(argv))]
    nested.extend(env_split_strings(argv))
    cmd = strip_prefix(argv)
    name = cmd[0].rsplit("/", 1)[-1] if cmd else ""
    if name in SHELLS:
        # -c may sit in a cluster (`bash -lc`); the script is the first non-option word after it
        flags = [i for i, a in enumerate(cmd[1:], 1) if re.match(r"^-[A-Za-z]*c[A-Za-z]*$", a)]
        j = flags[0] + 1 if flags else len(cmd)
        while j < len(cmd) and cmd[j][:1] in ("-", "+") and cmd[j] != "--":  # `bash -c -e 'cmd'`
            j += 2 if cmd[j] in ("-o", "+o", "-O", "+O") else 1
        j += 1 if j < len(cmd) and cmd[j] == "--" else 0
        if j < len(cmd):
            nested.append(cmd[j])
    if name == "eval":
        nested.append(" ".join(cmd[1:]))
    return nested


def check_segment(argv: list[str], depth: int) -> list[Rule]:
    hits = [r for text in nested_commands(argv) if (r := check_text(text, depth + 1))]
    cmd = strip_prefix(argv)
    name = cmd[0].rsplit("/", 1)[-1] if cmd else ""
    if name == "git":
        rest = skip_options(cmd, GIT_OPTS_WITH_VALUE)
        sub, args = (rest[0], rest[1:]) if rest else ("", [])
        if sub == "commit" and commit_skips_hooks(args):
            hits.append(NO_VERIFY)
        elif sub == "push" and any(is_no_verify(a) for a in args):  # push -n is --dry-run
            hits.append(NO_VERIFY)
        elif sub == "add" and adds_everything(args):
            hits.append(GIT_ADD_ALL)
    elif name == "gh":
        rest = skip_options(cmd, GH_OPTS_WITH_VALUE)
        if rest[:2] == ["pr", "merge"] and any(a == "--admin" or a.startswith("--admin=") for a in rest[2:]):
            hits.append(GH_ADMIN)
    return hits


FALLBACK = [  # used only when the command cannot be tokenized
    (NO_VERIFY, re.compile(r"\bgit\b[^;&|]*\b(commit\b[^;&|]*(--no-veri|\s-[A-Za-z]*n)|push\b[^;&|]*--no-veri)")),
    (GH_ADMIN, re.compile(r"\bgh\b[^;&|]*\bpr\s+merge\b[^;&|]*--admin")),
    (GIT_ADD_ALL, re.compile(r"\bgit\s+add\s+(-A\b|--all\b|\.(\s|$))")),
]
MAX_DEPTH = 3


def pick(hits: list[Rule]) -> Rule | None:
    """Deny beats ask; within a decision, the first hit wins."""
    return next((r for r in hits if r.decision == "deny"), hits[0] if hits else None)


def check_text(cmd: str, depth: int = 0) -> Rule | None:
    segs = segments(cmd) if depth <= MAX_DEPTH else None
    if segs is None:
        return pick([r for r, rx in FALLBACK if rx.search(cmd)])
    return pick([r for argv in segs for r in check_segment(argv, depth)])


def check_rules(cmd: str, safety_level: str = SAFETY_LEVEL) -> Rule | None:
    rule = check_text(cmd)
    return rule if rule and LEVELS[rule.level] <= LEVELS.get(safety_level, 2) else None


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
        if data.get("tool_name") != "Bash":
            print("{}")
            return

        cmd = data.get("tool_input", {}).get("command", "")
        matched = check_command(cmd)
        rule = None if matched else check_rules(cmd)

        if rule:
            log({
                "level": "BLOCKED" if rule.decision == "deny" else "ASK", "id": rule.id, "priority": rule.level,
                "cmd": cmd, "session_id": data.get("session_id"), "cwd": data.get("cwd"),
            })
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": rule.decision,
                    "permissionDecisionReason": f"{EMOJIS[rule.level]} [{rule.id}] {rule.reason}",
                }
            }))
        elif matched:
            log({
                "level": "BLOCKED", "id": matched.id, "priority": matched.level,
                "cmd": cmd, "session_id": data.get("session_id"), "cwd": data.get("cwd"),
            })
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"{EMOJIS[matched.level]} [{matched.id}] {matched.reason}",
                }
            }))
        else:
            print("{}")

    except Exception:
        print("{}")


if __name__ == "__main__":
    main()
