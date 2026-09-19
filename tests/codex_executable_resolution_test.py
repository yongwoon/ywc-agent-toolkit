#!/usr/bin/env python3
"""Regression coverage for the shipped Codex executable resolver contract."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "codex/skills/scripts/resolve-bundle-executable.py"
LAUNCHER = ROOT / "codex/skills/scripts/resolve-bundle-executable.sh"
SELECT_LAUNCHER = ROOT / "codex/skills/scripts/select-resolver-launcher.sh"
MARK_COMPLETE = ROOT / "codex/skills/scripts/mark-complete.sh"
CALLER_FILES = [
    ROOT / "codex/skills/scripts/mark-complete.sh",
    *(
        ROOT / "codex/skills" / name / "SKILL.md"
        for name in (
            "ywc-code-gen",
            "ywc-create-pr",
            "ywc-finish-branch",
            "ywc-handle-pr-reviews",
            "ywc-onboard-repo",
            "ywc-parallel-executor",
            "ywc-release-pr-list",
            "ywc-skill-author",
            "ywc-spec-writer",
            "ywc-task-generator",
        )
    ),
]


def run(command: list[str], *, env: dict[str, str] | None = None, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=30)


def resolver_env(**overrides: str) -> dict[str, str]:
    env = os.environ.copy()
    env.update(overrides)
    return env


def assert_blocked(result: subprocess.CompletedProcess[str], needle: str | None = None) -> None:
    assert result.returncode == 3, (result.returncode, result.stdout, result.stderr)
    assert result.stderr.startswith("BLOCKED:"), result.stderr
    if needle:
        assert needle in result.stderr, result.stderr


def make_installed_bundle(root: Path) -> Path:
    skills = root / "skills"
    scripts = skills / "scripts"
    scripts.mkdir(parents=True)
    shutil.copy2(RESOLVER, scripts / RESOLVER.name)
    shutil.copy2(LAUNCHER, scripts / LAUNCHER.name)
    return skills


def make_source_bundle(root: Path) -> Path:
    skills = root / "codex/skills"
    scripts = skills / "scripts"
    scripts.mkdir(parents=True)
    shutil.copy2(RESOLVER, scripts / RESOLVER.name)
    shutil.copy2(LAUNCHER, scripts / LAUNCHER.name)
    assert run(["git", "init", "-q"], cwd=root).returncode == 0
    assert run(["git", "config", "user.name", "fixture"], cwd=root).returncode == 0
    assert run(["git", "config", "user.email", "fixture@example.test"], cwd=root).returncode == 0
    assert run(
        ["git", "config", "remote.origin.url", "https://github.com/yongwoon/ywc-agent-toolkit.git"],
        cwd=root,
    ).returncode == 0
    return skills


def test_installed_first_and_launcher() -> None:
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        skills = make_installed_bundle(home)
        candidate = skills / "installed.py"
        candidate.write_text("# installed\n", encoding="utf-8")
        source = home / "source"
        source_skills = make_source_bundle(source)
        (source_skills / "installed.py").write_text("# source must lose\n", encoding="utf-8")
        env = resolver_env(CODEX_HOME=str(home), YWC_BUNDLE_DEVELOPMENT="1", YWC_BUNDLE_SOURCE_ROOT=str(source))
        result = run([sys.executable, str(RESOLVER), "installed.py", "python3"], env=env)
        assert result.returncode == 0
        assert Path(result.stdout.strip()) == candidate.resolve()
        launcher_result = run(["bash", str(skills / "scripts/resolve-bundle-executable.sh"), "installed.py", "python3"], env=env)
        assert launcher_result.returncode == 0
        assert Path(launcher_result.stdout.strip()) == candidate.resolve()


def test_authorized_source_and_interpreter_mode() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        home = root / "home"
        source = root / "source"
        source_skills = make_source_bundle(source)
        source_candidate = source_skills / "source-only.py"
        source_candidate.write_text("# interpreter-only\n", encoding="utf-8")
        env = resolver_env(CODEX_HOME=str(home), YWC_BUNDLE_DEVELOPMENT="1", YWC_BUNDLE_SOURCE_ROOT=str(source))
        source_resolver = source_skills / "scripts/resolve-bundle-executable.py"
        result = run([sys.executable, str(source_resolver), "scripts/resolve-bundle-executable.py", "python3"], env=env)
        assert result.returncode == 0
        assert Path(result.stdout.strip()) == (source / "codex/skills/scripts/resolve-bundle-executable.py").resolve()
        source_result = run([sys.executable, str(source_resolver), "source-only.py", "python3"], env=env)
        assert source_result.returncode == 0
        assert Path(source_result.stdout.strip()) == source_candidate.resolve()
        launcher_result = run(
            ["bash", str(source_skills / "scripts/resolve-bundle-executable.sh"), "source-only.py", "python3"],
            env=env,
        )
        assert launcher_result.returncode == 0
        assert Path(launcher_result.stdout.strip()) == source_candidate.resolve()
        direct = run([sys.executable, str(source_resolver), "source-only.py", "direct"], env=env)
        assert_blocked(direct, "unusable")


def test_hostile_target_origin_and_missing_candidates() -> None:
    with tempfile.TemporaryDirectory() as raw:
        target = Path(raw)
        target_skills = make_source_bundle(target)
        marker = target_skills / "lookalike.py"
        marker.write_text(
            "import os\nfrom pathlib import Path\n"
            "Path(os.environ['YWC_TEST_MARKER']).write_text('ran\\n', encoding='utf-8')\n",
            encoding="utf-8",
        )
        assert run(["git", "config", "remote.origin.url", "https://example.invalid/attacker.git"], cwd=target).returncode == 0
        env = resolver_env(
            CODEX_HOME=str(target / "empty-home"),
            YWC_BUNDLE_DEVELOPMENT="1",
            YWC_BUNDLE_SOURCE_ROOT=str(target),
            YWC_TEST_MARKER=str(target / "marker-created"),
        )
        hostile = run(["bash", str(target_skills / "scripts/resolve-bundle-executable.sh"), "lookalike.py", "python3"], env=env)
        assert_blocked(hostile, "expected origin")
        missing = run([sys.executable, str(RESOLVER), "scripts/missing.py", "python3"], env=resolver_env(CODEX_HOME=str(target / "empty-home")))
        assert_blocked(missing, "Expected installed path")
        assert not (target / "marker-created").exists()


def test_installed_symlink_escape() -> None:
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        skills = make_installed_bundle(home)
        outside = home / "outside.py"
        outside.write_text("# outside\n", encoding="utf-8")
        (skills / "escape.py").symlink_to(outside)
        result = run([sys.executable, str(RESOLVER), "escape.py", "python3"], env=resolver_env(CODEX_HOME=str(home)))
        assert_blocked(result, "Expected installed path")


def test_mark_complete_does_not_mutate_when_blocked() -> None:
    with tempfile.TemporaryDirectory() as raw, tempfile.TemporaryDirectory() as raw_home:
        repo = Path(raw)
        empty_home = Path(raw_home)
        task = repo / "tasks/pending-task"
        task.mkdir(parents=True)
        (task / "task.md").write_text("pending\n", encoding="utf-8")
        assert run(["git", "init", "-q"], cwd=repo).returncode == 0
        assert run(["git", "config", "user.name", "fixture"], cwd=repo).returncode == 0
        assert run(["git", "config", "user.email", "fixture@example.test"], cwd=repo).returncode == 0
        assert run(["git", "add", "tasks"], cwd=repo).returncode == 0
        assert run(["git", "commit", "-qm", "fixture"], cwd=repo).returncode == 0
        before_result = run(["git", "rev-parse", "HEAD"], cwd=repo)
        assert before_result.returncode == 0
        before = before_result.stdout.strip()
        # select-resolver-launcher.sh is installed (as it always is alongside
        # the rest of codex/skills/scripts/ via scripts/install.sh) but
        # resolve-bundle-executable.sh is not, and dev fallback is not
        # opted in — this exercises select-resolver-launcher.sh's own
        # "installed launcher missing, dev mode off" BLOCKED path.
        empty_home_scripts = empty_home / "skills/scripts"
        empty_home_scripts.mkdir(parents=True)
        shutil.copy2(SELECT_LAUNCHER, empty_home_scripts / SELECT_LAUNCHER.name)
        result = run(
            ["bash", str(MARK_COMPLETE), "tasks", "pending-task"],
            env=resolver_env(
                CODEX_HOME=str(empty_home),
                YWC_BUNDLE_DEVELOPMENT="",
                YWC_BUNDLE_SOURCE_ROOT="",
            ),
            cwd=repo,
        )
        assert_blocked(result, "development source fallback")
        assert task.is_dir()
        assert not (repo / "tasks/completed").exists()
        assert not (repo / "tasks/completed/pending-task").exists()
        after_result = run(["git", "rev-parse", "HEAD"], cwd=repo)
        status_result = run(["git", "status", "--porcelain"], cwd=repo)
        assert after_result.returncode == 0
        assert status_result.returncode == 0
        assert after_result.stdout.strip() == before
        assert not status_result.stdout.strip()


def test_closed_set_complement() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in CALLER_FILES)
    assert combined.count('bash "$RESOLVER_LAUNCHER"') == 20
    assert all(path.is_file() for path in CALLER_FILES)
    source_files = [
        path
        for path in (ROOT / "codex/skills").rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".sh"}
        and "codex/skills/references" not in str(path)
    ]
    all_source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    assert all_source.count('bash "$RESOLVER_LAUNCHER"') == 20
    unsafe = [
        line
        for line in all_source.splitlines()
        if "`" not in line
        and re.search(
            r"(?:\b(?:bash|python3?|exec)\s+[\"']?(?:\./)?codex/skills/|(?:^|[\s;])\w+=[\"']?(?:\./)?codex/skills/)",
            line,
        )
        and "compact-dependency-graph.py" not in line
    ]
    assert not unsafe, unsafe


def main() -> None:
    tests = [
        test_installed_first_and_launcher,
        test_authorized_source_and_interpreter_mode,
        test_hostile_target_origin_and_missing_candidates,
        test_installed_symlink_escape,
        test_mark_complete_does_not_mutate_when_blocked,
        test_closed_set_complement,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"PASS: {len(tests)} executable-resolution regression scenarios")


if __name__ == "__main__":
    main()
