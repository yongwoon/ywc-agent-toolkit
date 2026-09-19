#!/usr/bin/env python3
"""Resolve a trusted executable from the installed Codex bundle or source tree."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


BLOCKED = 3
EXPECTED_ORIGIN = re.compile(
    r"^(?:https://github\.com/yongwoon/ywc-agent-toolkit(?:\.git)?|"
    r"git@github\.com:yongwoon/ywc-agent-toolkit(?:\.git)?|"
    r"ssh://git@github\.com/yongwoon/ywc-agent-toolkit(?:\.git)?)$"
)
KINDS = ("bash", "python", "python3", "direct")


def blocked(relative: str, installed: Path, reason: str) -> int:
    print(
        "BLOCKED: cannot resolve "
        f"{relative!r}: {reason}. Expected installed path: {installed}. "
        "For development, set YWC_BUNDLE_DEVELOPMENT=1 and "
        "YWC_BUNDLE_SOURCE_ROOT to the canonical ywc-agent-toolkit Git root.",
        file=sys.stderr,
    )
    return BLOCKED


def contained_regular_file(candidate: Path, root: Path, kind: str) -> Path | None:
    try:
        resolved_root = root.resolve(strict=True)
        resolved = candidate.resolve(strict=True)
    except (OSError, ValueError):
        return None
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None
    if not resolved.is_file() or not os.access(resolved, os.R_OK):
        return None
    if kind == "direct" and not os.access(resolved, os.X_OK):
        return None
    return resolved


def origin_is_trusted(root: Path) -> bool:
    try:
        top = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        origin = subprocess.run(
            ["git", "-C", str(root), "config", "--get", "remote.origin.url"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return False
    return Path(top).resolve() == root and bool(EXPECTED_ORIGIN.fullmatch(origin))


def source_root() -> tuple[Path | None, str]:
    if os.environ.get("YWC_BUNDLE_DEVELOPMENT") != "1":
        return None, "development source fallback is not explicitly enabled"
    raw = os.environ.get("YWC_BUNDLE_SOURCE_ROOT", "")
    if not raw or not os.path.isabs(raw):
        return None, "YWC_BUNDLE_SOURCE_ROOT must be an absolute path"
    try:
        root = Path(raw).resolve(strict=True)
    except OSError:
        return None, "YWC_BUNDLE_SOURCE_ROOT does not resolve to a directory"
    if not root.is_dir() or not origin_is_trusted(root):
        return None, "source root is not the canonical repository with the expected origin"
    if not (root / "codex" / "skills").is_dir():
        return None, "source root is missing the expected codex/skills layout"
    return root, ""


def parse_relative(value: str) -> Path | None:
    path = Path(value)
    if "\x00" in value or path.is_absolute() or not value or any(part in ("", ".", "..") for part in path.parts):
        return None
    return path


def resolve(relative: str, kind: str) -> tuple[Path | None, Path, str]:
    rel = parse_relative(relative)
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    installed_root = (codex_home / "skills").resolve(strict=False)
    installed = installed_root / (rel if rel is not None else relative)
    if rel is None:
        return None, installed, "bundle-relative path is invalid"
    candidate = contained_regular_file(installed, installed_root, kind)
    if candidate is not None:
        return candidate, installed, ""

    root, reason = source_root()
    if root is None:
        return None, installed, reason
    source_skills = root / "codex" / "skills"
    candidate = contained_regular_file(source_skills / rel, source_skills, kind)
    if candidate is None:
        return None, installed, "authorized source candidate is missing, untrusted, or unusable"
    return candidate, installed, ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve a Codex bundle-relative executable without target-repository fallback"
    )
    parser.add_argument("path", help="path relative to the installed or source codex/skills directory")
    parser.add_argument("kind", choices=KINDS, help="fixed invocation kind")
    args = parser.parse_args()
    candidate, installed, reason = resolve(args.path, args.kind)
    if candidate is None:
        return blocked(args.path, installed, reason)
    print(candidate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
