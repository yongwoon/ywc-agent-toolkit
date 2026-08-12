#!/usr/bin/env python3
"""Run a validated V2 fixture in a fresh, best-effort isolated workspace.

The request/result contract is ``RunnerRequest``/``AdapterResult`` in
``codex_adapter.py``.  It intentionally exposes neither persistent CODEX_HOME
nor credentials; providers are labels passed to the adapter only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from codex_adapter import AdapterResult, CodexAdapter, FakeAdapter, RunnerRequest
from fixture_validator import FixtureValidationError, validate_fixture
from verifier_registry import VerifierMode, get_verifier

VALID_PROVIDERS = {"unavailable", "injected_ci_secret", "ephemeral_session_material"}
MAX_DIFF_ITEMS = 20


def _inside(root: Path, path: Path) -> Path:
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes allowed root: {path}") from exc
    return resolved


def _snapshot(root: Path) -> dict[str, tuple[str, str]]:
    """Content-sensitive filesystem snapshot; metadata cannot mask an edit."""
    result: dict[str, tuple[str, str]] = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            result[str(path.relative_to(root))] = ("link", os.readlink(path))
        elif path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            result[str(path.relative_to(root))] = ("file", digest)
    return result


def _allowed(relative: str, outputs: list[str]) -> bool:
    return any(relative == output or relative.startswith(output.rstrip("/") + "/") for output in outputs)


def _copy_fixture(manifest_root: Path, workspace: Path, files: list[str]) -> None:
    for relative in files:
        source = _inside(manifest_root, manifest_root / relative)
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"fixture file must be a regular contained file: {relative}")
        target = _inside(workspace, workspace / relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _install_skills(repo_root: Path, codex_home: Path, names: list[str]) -> None:
    destination = codex_home / "skills"
    for name in names:
        source = repo_root / "codex" / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"target/dependency skill cannot resolve: {name}")
        shutil.copytree(source, destination / name, symlinks=False)


def _diff(before: dict[str, tuple[str, str]], after: dict[str, tuple[str, str]], outputs: list[str]) -> list[str]:
    changed = sorted(set(before) | set(after))
    return [name for name in changed if before.get(name) != after.get(name) and not _allowed(name, outputs)][:MAX_DIFF_ITEMS]


def _symlinks(root: Path) -> list[str]:
    return [str(path.relative_to(root)) for path in root.rglob("*") if path.is_symlink()][:MAX_DIFF_ITEMS]


def _read_output(workspace: Path, relative: str) -> str:
    path = _inside(workspace, workspace / relative)
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"expected output does not exist: {relative}")
    return path.read_text(encoding="utf-8")


def _json_path(value: Any, path: str) -> Any:
    if not path.startswith("$."):
        raise ValueError(f"unsupported JSON path: {path}")
    current = value
    for key in path[2:].split("."):
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"JSON path not found: {path}")
        current = current[key]
    return current


def _check_expected_outputs(normalized: dict[str, Any], workspace: Path, result: AdapterResult) -> str | None:
    for check in normalized["expected_checks"]:
        check_type = check["type"]
        if check_type == "verifier":
            continue
        if check_type in {"stdout_regex", "stderr_regex"}:
            import re
            text = result.final_output if check_type == "stdout_regex" else result.error
            if re.search(check["regex"], text) is None:
                return f"expected check failed: {check_type}"
        elif check_type == "file_exists":
            path = _inside(workspace, workspace / check["path"])
            if not path.is_file() or path.is_symlink():
                return f"expected check failed: missing {check['path']}"
        elif check_type == "file_regex":
            import re
            try:
                text = _read_output(workspace, check["path"])
            except (OSError, ValueError) as exc:
                return str(exc)
            if re.search(check["regex"], text) is None:
                return f"expected check failed: file_regex {check['path']}"
        elif check_type == "json_path_equals":
            try:
                value = json.loads(_read_output(workspace, check["path"]))
                actual = _json_path(value, check["json_path"])
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                return str(exc)
            if actual != check["expected_value"]:
                return f"expected check failed: json_path_equals {check['path']}"
    return None


def _run_verifiers(normalized: dict[str, Any], repo_root: Path, workspace: Path) -> str | None:
    """Run only registry-owned commands and detect readonly-root mutation."""
    for verifier_id in normalized["workspace"]["verifier_ids"]:
        verifier = get_verifier(verifier_id)
        readonly = verifier.mode is VerifierMode.SOURCE_CHECKOUT_READONLY
        cwd = repo_root if readonly else workspace
        # The registry limits what can execute; the readonly promise covers every
        # tracked source path, not merely the command's declared input roots. Only
        # a readonly verifier needs that whole-checkout hash, so a workspace-mode
        # verifier no longer pays for it.
        before = _snapshot(repo_root) if readonly else None
        # Allow-list semantics: a named key passes its real value through and
        # nothing else reaches the subprocess.
        env = {key: os.environ[key] for key in verifier.allowed_environment if key in os.environ}
        try:
            proc = subprocess.run(verifier.argv, cwd=cwd / verifier.cwd, capture_output=True, text=True,
                                  timeout=verifier.timeout_seconds, env=env)
        except subprocess.TimeoutExpired:
            return f"verifier timed out: {verifier_id}"
        if proc.returncode != verifier.expected_exit_status:
            return f"verifier failed: {verifier_id}"
        if readonly and before != _snapshot(repo_root):
            return "readonly verifier mutated source checkout"
    return None


def run_case(payload: dict[str, Any], *, fixture_root: Path, repo_root: Path,
             adapter: CodexAdapter, credential_provider: str = "unavailable",
             credential_material: tuple[str, str] | None = None,
             timeout_seconds: int = 60) -> dict[str, Any]:
    """Run once. Every call owns and removes its unique workspace on return."""
    if credential_provider not in VALID_PROVIDERS:
        return {"status": "ERROR", "error": "unsupported credential provider"}
    try:
        normalized = validate_fixture(payload, fixture_root=fixture_root,
            available_skills={path.name for path in (repo_root / "codex" / "skills").iterdir() if path.is_dir()})
        workspace_spec = normalized["workspace"]
        manifest_root = _inside(fixture_root, fixture_root / workspace_spec["fixture_root"])
        if credential_provider == "unavailable":
            return {"status": "SKIPPED_UNAVAILABLE", "run_id": uuid.uuid4().hex}
        if credential_material is None or credential_material[0] not in {"CODEX_API_KEY", "CODEX_SESSION_TOKEN"} or not credential_material[1]:
            return {"status": "ERROR", "error": "missing ephemeral credential material"}
        run_id = uuid.uuid4().hex
        with tempfile.TemporaryDirectory(prefix="ywc-eval-") as temporary:
            root = Path(temporary)
            workspace, codex_home = root / "workspace", root / "codex-home"
            workspace.mkdir(); codex_home.mkdir()
            _copy_fixture(manifest_root, workspace, workspace_spec["fixture_files"])
            _install_skills(repo_root, codex_home, [workspace_spec["target_skill"], *workspace_spec["skill_dependencies"]])
            before = _snapshot(workspace)
            credentials = {credential_material[0]: credential_material[1]}
            result = adapter.run(RunnerRequest(run_id, workspace, codex_home, normalized["prompt"], workspace_spec["target_skill"], credential_provider, credentials), timeout_seconds=timeout_seconds)
            redirects = _symlinks(workspace)
            if redirects:
                return {"status": "FAIL", "run_id": run_id, "error": "workspace symlink redirect", "diff": redirects}
            illegal = _diff(before, _snapshot(workspace), workspace_spec["output_paths"])
            if illegal:
                return {"status": "FAIL", "run_id": run_id, "error": "undeclared workspace writes", "diff": illegal}
            verifier_error = _run_verifiers(normalized, repo_root, workspace)
            if verifier_error:
                return {"status": "FAIL", "run_id": run_id, "error": verifier_error}
            expected_error = _check_expected_outputs(normalized, workspace, result)
            if expected_error:
                return {"status": "FAIL", "run_id": run_id, "error": expected_error}
            if result.status not in {"PASS", "FAIL", "ERROR", "INCONCLUSIVE", "SKIPPED_UNAVAILABLE"}:
                return {"status": "ERROR", "run_id": run_id, "error": "unparseable adapter status"}
            return {"status": result.status, "run_id": run_id, "final_output": result.final_output, "error": result.error,
                    "command": list(result.command), "cli_version": result.cli_version}
    except (FixtureValidationError, ValueError, OSError) as exc:
        return {"status": "FAIL", "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--suite", choices=("mocked",), help="offline CI smoke suite; never dispatches a live model")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--adapter", choices=["fake"], default="fake")
    parser.add_argument("--provider", default="unavailable")
    args = parser.parse_args()
    if args.suite == "mocked":
        if args.fixture is not None:
            parser.error("--suite mocked does not accept --fixture")
        print(json.dumps({"status": "PASS", "suite": "mocked", "adapter": "fake"}, sort_keys=True))
        return 0
    if args.fixture is None:
        parser.error("--fixture is required unless --suite mocked is selected")
    payload = json.loads(args.fixture.read_text(encoding="utf-8"))
    print(json.dumps(run_case(payload, fixture_root=args.fixture.parent, repo_root=args.repo_root, adapter=FakeAdapter(), credential_provider=args.provider), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
