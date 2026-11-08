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

import json
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
GLOB_CHARS = re.compile(r'\*+|\?|\[[^\]]*\]|\{[^}]*\}')


def check_search(base: str | None, name: str | None, safety_level: str = SAFETY_LEVEL) -> Pattern | None:
    """Check the searched directory and the file-name filter (Grep `glob`, Glob `pattern`)."""
    base, name = base or "", name or ""
    threshold = LEVELS.get(safety_level, 2)
    candidates = [base, f"{base.rstrip('/')}/{name}" if base and name else name]
    for c in candidates:
        if not c or is_allowlisted(c):
            continue
        for p in SENSITIVE_DIRS:
            if LEVELS[p.level] <= threshold and p.regex.search(c):
                return p
        # `**/.env*` → `/.env`: drop glob syntax so the file patterns can match the literal part.
        hit = check_file_path(c, safety_level) or check_file_path(GLOB_CHARS.sub("", c), safety_level)
        if hit:
            return hit
    return None


def check(tool_name: str, tool_input: dict, safety_level: str = SAFETY_LEVEL) -> Pattern | None:
    if tool_name in ("Read", "Edit", "Write"):
        return check_file_path(tool_input.get("file_path", ""), safety_level)
    if tool_name == "Bash":
        return check_bash_command(tool_input.get("command", ""), safety_level)
    if tool_name == "Grep":  # Grep's `pattern` is a content regex, not a file name
        return check_search(tool_input.get("path"), tool_input.get("glob"), safety_level)
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

        matched = check(tool_name, tool_input)

        if matched:
            target = tool_input.get("file_path") or tool_input.get("command", "")[:100] or " ".join(str(tool_input.get(k) or "") for k in ("path", "glob", "pattern")).strip()
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
