#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Protect Secrets - PreToolUse Hook for Read|Edit|Write|Bash|Grep|Glob
Prevents reading, modifying, or exfiltrating sensitive files.
Logs to: ~/.claude/hooks-logs/YYYY-MM-DD.jsonl

SAFETY_LEVEL: 'critical' | 'high' | 'strict'
  critical - SSH keys, AWS creds, .env files only
  high     - + secrets files, env dumps, exfiltration attempts
  strict   - + database configs, any config that might contain secrets
"""

import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

SAFETY_LEVEL = "high"

ALLOWLIST: list[re.Pattern] = [
    re.compile(r'\.env\.example$', re.IGNORECASE),
    re.compile(r'\.env\.sample$', re.IGNORECASE),
    re.compile(r'\.env\.template$', re.IGNORECASE),
    re.compile(r'\.env\.schema$', re.IGNORECASE),
    re.compile(r'\.env\.defaults$', re.IGNORECASE),
    re.compile(r'env\.example$', re.IGNORECASE),
    re.compile(r'example\.env$', re.IGNORECASE),
]


@dataclass(frozen=True)
class Pattern:
    level: str
    id: str
    regex: re.Pattern
    reason: str


SENSITIVE_FILES: list[Pattern] = [
    # CRITICAL
    Pattern("critical", "env-file",          re.compile(r'(?:^|\/)\.env(?:\.[^/]*)?$'),                                  ".env file contains secrets"),
    Pattern("critical", "envrc",             re.compile(r'(?:^|\/)\.envrc$'),                                            ".envrc (direnv) contains secrets"),
    Pattern("critical", "ssh-private-key",   re.compile(r'(?:^|\/)\.ssh\/id_[^/]+$'),                                   "SSH private key"),
    Pattern("critical", "ssh-private-key-2", re.compile(r'(?:^|\/)(id_rsa|id_ed25519|id_ecdsa|id_dsa)$'),               "SSH private key"),
    Pattern("critical", "ssh-authorized",    re.compile(r'(?:^|\/)\.ssh\/authorized_keys$'),                            "SSH authorized_keys"),
    Pattern("critical", "aws-credentials",   re.compile(r'(?:^|\/)\.aws\/credentials$'),                                "AWS credentials file"),
    Pattern("critical", "aws-config",        re.compile(r'(?:^|\/)\.aws\/config$'),                                     "AWS config may contain secrets"),
    Pattern("critical", "kube-config",       re.compile(r'(?:^|\/)\.kube\/config$'),                                    "Kubernetes config contains credentials"),
    Pattern("critical", "pem-key",           re.compile(r'\.pem$', re.IGNORECASE),                                      "PEM key file"),
    Pattern("critical", "key-file",          re.compile(r'\.key$', re.IGNORECASE),                                      "Key file"),
    Pattern("critical", "p12-key",           re.compile(r'\.(p12|pfx)$', re.IGNORECASE),                                "PKCS12 key file"),
    # HIGH
    Pattern("high", "credentials-json",      re.compile(r'(?:^|\/)credentials\.json$', re.IGNORECASE),                  "Credentials file"),
    Pattern("high", "secrets-file",          re.compile(r'(?:^|\/)(secrets?|credentials?)\.(json|ya?ml|toml)$', re.IGNORECASE), "Secrets configuration file"),
    Pattern("high", "service-account",       re.compile(r'service[_-]?account.*\.json$', re.IGNORECASE),                "GCP service account key"),
    Pattern("high", "gcloud-creds",          re.compile(r'(?:^|\/)\.config\/gcloud\/.*(credentials|tokens)', re.IGNORECASE), "GCloud credentials"),
    Pattern("high", "azure-creds",           re.compile(r'(?:^|\/)\.azure\/(credentials|accessTokens)', re.IGNORECASE), "Azure credentials"),
    Pattern("high", "docker-config",         re.compile(r'(?:^|\/)\.docker\/config\.json$'),                            "Docker config may contain registry auth"),
    Pattern("high", "netrc",                 re.compile(r'(?:^|\/)\.netrc$'),                                           ".netrc contains credentials"),
    Pattern("high", "npmrc",                 re.compile(r'(?:^|\/)\.npmrc$'),                                           ".npmrc may contain auth tokens"),
    Pattern("high", "pypirc",                re.compile(r'(?:^|\/)\.pypirc$'),                                          ".pypirc contains PyPI credentials"),
    Pattern("high", "gem-creds",             re.compile(r'(?:^|\/)\.gem\/credentials$'),                                "RubyGems credentials"),
    Pattern("high", "vault-token",           re.compile(r'(?:^|\/)(\.vault-token|vault-token)$'),                       "Vault token file"),
    Pattern("high", "keystore",              re.compile(r'\.(keystore|jks)$', re.IGNORECASE),                           "Java keystore"),
    Pattern("high", "htpasswd",              re.compile(r'(?:^|\/)\.?htpasswd$'),                                       "htpasswd contains hashed passwords"),
    Pattern("high", "pgpass",                re.compile(r'(?:^|\/)\.pgpass$'),                                          "PostgreSQL password file"),
    Pattern("high", "my-cnf",                re.compile(r'(?:^|\/)\.my\.cnf$'),                                         "MySQL config may contain password"),
    # STRICT
    Pattern("strict", "database-config",     re.compile(r'(?:^|\/)(?:config\/)?database\.(json|ya?ml)$', re.IGNORECASE), "Database config may contain passwords"),
    Pattern("strict", "ssh-known-hosts",     re.compile(r'(?:^|\/)\.ssh\/known_hosts$'),                                "SSH known_hosts reveals infrastructure"),
    Pattern("strict", "gitconfig",           re.compile(r'(?:^|\/)\.gitconfig$'),                                       ".gitconfig may contain credentials"),
    Pattern("strict", "curlrc",              re.compile(r'(?:^|\/)\.curlrc$'),                                          ".curlrc may contain auth"),
]

BASH_PATTERNS: list[Pattern] = [
    # CRITICAL
    Pattern("critical", "cat-env",           re.compile(r'\b(cat|less|head|tail|more|bat|view)\s+[^|;]*\.env\b', re.IGNORECASE),                                    "Reading .env file exposes secrets"),
    Pattern("critical", "cat-ssh-key",       re.compile(r'\b(cat|less|head|tail|more|bat)\s+[^|;]*(id_rsa|id_ed25519|id_ecdsa|id_dsa|\.pem|\.key)\b', re.IGNORECASE), "Reading private key"),
    Pattern("critical", "cat-aws-creds",     re.compile(r'\b(cat|less|head|tail|more)\s+[^|;]*\.aws\/credentials', re.IGNORECASE),                                  "Reading AWS credentials"),
    # HIGH — environment exposure
    Pattern("high", "env-dump",              re.compile(r'\bprintenv\b|(?:^|[;&|]\s*)env\s*(?:$|[;&|])'),                                                           "Environment dump may expose secrets"),
    Pattern("high", "echo-secret-var",       re.compile(r'\becho\b[^;|&]*\$\{?[A-Za-z_]*(?:SECRET|KEY|TOKEN|PASSWORD|PASSW|CREDENTIAL|API_KEY|AUTH|PRIVATE)[A-Za-z_]*\}?', re.IGNORECASE), "Echoing secret variable"),
    Pattern("high", "cat-secrets-file",      re.compile(r'\b(cat|less|head|tail|more)\s+[^|;]*(credentials?|secrets?)\.(json|ya?ml|toml)', re.IGNORECASE),           "Reading secrets file"),
    Pattern("high", "source-env",            re.compile(r'\bsource\s+[^|;]*\.env\b|(?:^|[;&|]\s*)\.\s+[^|;]*\.env\b|^\.\s+[^|;]*\.env\b', re.IGNORECASE),         "Sourcing .env loads secrets"),
    # HIGH — exfiltration
    Pattern("high", "curl-upload-env",       re.compile(r'\bcurl\b[^;|&]*(-d\s*@|-F\s*[^=]+=@|--data[^=]*=@)[^;|&]*(\.env|credentials|secrets|id_rsa|\.pem|\.key)', re.IGNORECASE), "Uploading secrets via curl"),
    Pattern("high", "scp-secrets",           re.compile(r'\bscp\b[^;|&]*(\.env|credentials|secrets|id_rsa|\.pem|\.key)[^;|&]+:', re.IGNORECASE),                   "Copying secrets via scp"),
    Pattern("high", "rsync-secrets",         re.compile(r'\brsync\b[^;|&]*(\.env|credentials|secrets|id_rsa)[^;|&]+:', re.IGNORECASE),                             "Syncing secrets via rsync"),
    Pattern("high", "nc-secrets",            re.compile(r'\bnc\b[^;|&]*<[^;|&]*(\.env|credentials|secrets|id_rsa)', re.IGNORECASE),                                "Exfiltrating secrets via netcat"),
    # HIGH — copy/move/delete secrets
    Pattern("high", "cp-env",                re.compile(r'\bcp\b[^;|&]*\.env\b', re.IGNORECASE),                                                                   "Copying .env file"),
    Pattern("high", "cp-ssh-key",            re.compile(r'\bcp\b[^;|&]*(id_rsa|id_ed25519|\.pem|\.key)\b', re.IGNORECASE),                                         "Copying private key"),
    Pattern("high", "mv-env",                re.compile(r'\bmv\b[^;|&]*\.env\b', re.IGNORECASE),                                                                   "Moving .env file"),
    Pattern("high", "rm-ssh-key",            re.compile(r'\brm\b[^;|&]*(id_rsa|id_ed25519|id_ecdsa|authorized_keys)', re.IGNORECASE),                              "Deleting SSH key"),
    Pattern("high", "rm-env",                re.compile(r'\brm\b.*\.env\b', re.IGNORECASE),                                                                        "Deleting .env file"),
    Pattern("high", "rm-aws-creds",          re.compile(r'\brm\b[^;|&]*\.aws\/credentials', re.IGNORECASE),                                                        "Deleting AWS credentials"),
    Pattern("high", "proc-environ",          re.compile(r'\/proc\/[^/]*\/environ'),                                                                                "Reading process environment"),
    # STRICT
    Pattern("strict", "grep-password",       re.compile(r'\bgrep\b[^|;]*(-r|--recursive)[^|;]*(password|secret|api.?key|token|credential)', re.IGNORECASE),        "Grep for secrets may expose them"),
    Pattern("strict", "base64-secrets",      re.compile(r'\bbase64\b[^|;]*(\.env|credentials|secrets|id_rsa|\.pem)', re.IGNORECASE),                               "Base64 encoding secrets"),
]

LEVELS: dict[str, int] = {"critical": 1, "high": 2, "strict": 3}
EMOJIS: dict[str, str] = {"critical": "🔐", "high": "🛡️", "strict": "⚠️"}
LOG_DIR = Path.home() / ".claude" / "hooks-logs"


def log(data: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps({"ts": datetime.now().isoformat(), "hook": "protect-secrets", **data}) + "\n")
    except Exception:
        pass


def is_allowlisted(path: str) -> bool:
    return bool(path and any(p.search(path) for p in ALLOWLIST))


def check_file_path(file_path: str, safety_level: str = SAFETY_LEVEL) -> Pattern | None:
    if not file_path or is_allowlisted(file_path):
        return None
    threshold = LEVELS.get(safety_level, 2)
    for p in SENSITIVE_FILES:
        if LEVELS[p.level] <= threshold and p.regex.search(file_path):
            return p
    return None


def check_bash_command(cmd: str, safety_level: str = SAFETY_LEVEL) -> Pattern | None:
    if not cmd:
        return None
    threshold = LEVELS.get(safety_level, 2)
    for p in BASH_PATTERNS:
        if LEVELS[p.level] <= threshold and p.regex.search(cmd):
            return p
    return None


# Grep / Glob search a directory, so a directory that only holds secrets is
# itself sensitive. Matched anywhere in the path, critical level.
SENSITIVE_DIRS: list[Pattern] = [
    Pattern("critical", "ssh-dir",    re.compile(r'(?:^|\/)\.ssh(?:\/|$)'),               "SSH key directory"),
    Pattern("critical", "aws-dir",    re.compile(r'(?:^|\/)\.aws(?:\/|$)'),               "AWS credentials directory"),
    Pattern("critical", "gnupg-dir",  re.compile(r'(?:^|\/)\.gnupg(?:\/|$)'),             "GnuPG key directory"),
    Pattern("critical", "kube-dir",   re.compile(r'(?:^|\/)\.kube(?:\/|$)'),              "Kubernetes credentials directory"),
    Pattern("high",     "gcloud-dir", re.compile(r'(?:^|\/)\.config\/gcloud(?:\/|$)'),    "GCloud credentials directory"),
    Pattern("high",     "azure-dir",  re.compile(r'(?:^|\/)\.azure(?:\/|$)'),             "Azure credentials directory"),
]
GLOB_CHARS = re.compile(r'\*+|\?|\[[^\]]*\]')
BRACE = re.compile(r'\{([^{}]*)\}')
TYPE_FILTER = re.compile(r'^\*+(\.(\*|[^*?\[\]{}]+))?$')
MAX_EXPANSIONS = 256
# Concrete names that SENSITIVE_FILES catches; a glob that matches one of them
# (`**/.[e]nv`, `**/id_*`) reaches secrets even when its literal part does not.
SAMPLE_NAMES = [".env", ".env.local", ".env.production", ".envrc", "id_rsa", "id_ed25519", "id_ecdsa",
                "server.pem", "server.key", "cert.p12", "credentials.json", "secrets.yaml", "secret.toml",
                ".netrc", ".npmrc", ".pypirc", ".pgpass", ".my.cnf", ".htpasswd", ".vault-token",
                "app.keystore", "service-account.json"]
BROAD_SEARCH = Pattern("critical", "broad-search", re.compile(r'$^'),
                       "content search over the home or root directory reaches secret files; narrow the path or add a glob/type")
GLOB_TOO_COMPLEX = Pattern("critical", "glob-too-complex", re.compile(r'$^'),
                           "brace expansion too large to check; use a simpler glob")


BRACKET = re.compile(r'\[([^\]!^][^\]]*)\]')
MAX_CLASS_CHARS = 32


def bracket_to_braces(pattern: str) -> str:
    """`[.]env` → `{.}env`, `[a-c]` → `{a,b,c}`, so the literal file rules see every spelling.
    Negated or very wide classes are left alone; the sample-name check still covers them."""
    def repl(m: re.Match) -> str:
        body, chars, i = m.group(1), [], 0
        while i < len(body):
            if i + 2 < len(body) and body[i + 1] == "-":
                chars.extend(chr(c) for c in range(ord(body[i]), ord(body[i + 2]) + 1))
                i += 3
            else:
                chars.append(body[i])
                i += 1
        if len(chars) > MAX_CLASS_CHARS or any(c in ",{}" for c in chars):
            return m.group(0)
        return "{" + ",".join(dict.fromkeys(chars)) + "}"
    return BRACKET.sub(repl, pattern)


def expand_braces(pattern: str) -> list[str] | None:
    """`a{b,c}d` → [abd, acd]; innermost braces first. None when over MAX_EXPANSIONS (fail closed)."""
    out, todo = [], [bracket_to_braces(pattern)]
    while todo:
        if len(out) + len(todo) > MAX_EXPANSIONS:
            return None
        p = todo.pop()
        m = BRACE.search(p)
        if not m:
            out.append(p)
            continue
        todo.extend(p[:m.start()] + alt + p[m.end():] for alt in m.group(1).split(","))
    return out


def name_glob_hits_secret(name_glob: str, safety_level: str) -> Pattern | None:
    base = name_glob.rsplit("/", 1)[-1]
    # `*`, `*.*`, `*.json`: a plain type filter whose literal suffix is already checked
    # (`*.pem` → `.pem`); sampling it would deny every `**/*.json` listing.
    # Anything else (`*env`, `*_rsa`, `*.[e]nv`, `?env`) is sampled.
    if not base or TYPE_FILTER.match(base):
        return None
    for sample in SAMPLE_NAMES:
        if fnmatch.fnmatchcase(sample, base) and not is_allowlisted(sample):
            hit = check_file_path(sample, safety_level)
            if hit:
                return hit
    return None


def is_broad(base: str) -> bool:
    if not base:
        return False
    home = Path.home().resolve(strict=False)
    p = Path(os.path.expanduser(base)).resolve(strict=False)
    return p == Path("/") or p == home or p == home.parent


def check_search(base: str | None, name: str | None, safety_level: str = SAFETY_LEVEL) -> Pattern | None:
    """Check the searched directory and the file-name filter (Grep `glob`, Glob `pattern`)."""
    base, name = base or "", name or ""
    threshold = LEVELS.get(safety_level, 2)
    names = expand_braces(name) if name else [""]
    if names is None:
        return GLOB_TOO_COMPLEX
    for n in names:
        for c in (base, f"{base.rstrip('/')}/{n}" if base and n else n):
            if not c or is_allowlisted(c):
                continue
            for p in SENSITIVE_DIRS:
                if LEVELS[p.level] <= threshold and p.regex.search(c):
                    return p
            # `**/.env*` → `/.env`: drop glob syntax so the file patterns can match the literal part.
            hit = (check_file_path(c, safety_level) or check_file_path(GLOB_CHARS.sub("", c), safety_level)
                   or name_glob_hits_secret(c, safety_level))
            if hit:
                return hit
    return None


def check_grep(tool_input: dict, safety_level: str = SAFETY_LEVEL, cwd: str = "") -> Pattern | None:
    """Grep's `pattern` is a content regex, so only the place and the file filter are checked."""
    path, glob = tool_input.get("path"), tool_input.get("glob")
    # A glob narrows only if every brace expansion keeps a literal name part (`*.md` → `md`);
    # `*`, `**/*`, `?`, `[a-z]*` narrow nothing.
    expansions = expand_braces(glob) if glob else None
    # `!*.ts` excludes files, so a negated glob widens rather than narrows.
    narrows = bool(expansions) and all(not e.startswith("!") and re.sub(r'[/.]', "", GLOB_CHARS.sub("", e))
                                       for e in expansions)
    narrows = narrows or bool(tool_input.get("type"))
    if is_broad(path or cwd) and not narrows:  # no path → Grep searches the session cwd
        return BROAD_SEARCH
    return check_search(path, glob, safety_level)


def check(tool_name: str, tool_input: dict, safety_level: str = SAFETY_LEVEL, cwd: str = "") -> Pattern | None:
    if tool_name in ("Read", "Edit", "Write"):
        return check_file_path(tool_input.get("file_path", ""), safety_level)
    if tool_name == "Bash":
        return check_bash_command(tool_input.get("command", ""), safety_level)
    if tool_name == "Grep":
        return check_grep(tool_input, safety_level, cwd)
    if tool_name == "Glob":
        return check_search(tool_input.get("path"), tool_input.get("pattern"), safety_level)
    return None


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name not in ("Read", "Edit", "Write", "Bash", "Grep", "Glob"):
            print("{}")
            return

        matched = check(tool_name, tool_input, cwd=data.get("cwd") or "")

        if matched:
            search_keys = ("path", "glob") if tool_name == "Grep" else ("path", "pattern")  # Grep pattern may hold a secret
            target = tool_input.get("file_path") or tool_input.get("command", "")[:100] or " ".join(str(tool_input.get(k) or "") for k in search_keys).strip()
            log({
                "level": "BLOCKED", "id": matched.id, "priority": matched.level,
                "tool": tool_name, "target": target,
                "session_id": data.get("session_id"), "cwd": data.get("cwd"),
            })
            action = {"Read": "read", "Edit": "modify", "Write": "write to", "Bash": "execute", "Grep": "search", "Glob": "search"}[tool_name]
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"{EMOJIS[matched.level]} [{matched.id}] Cannot {action}: {matched.reason}",
                }
            }))
        else:
            print("{}")

    except Exception:
        print("{}")


if __name__ == "__main__":
    main()
