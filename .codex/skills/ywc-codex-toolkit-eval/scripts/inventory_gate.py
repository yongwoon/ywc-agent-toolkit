#!/usr/bin/env python3
"""Inventory and structural gate for Codex skill/agent evaluation.

This script is intentionally project-local. It evaluates only:
  - codex/skills/*/SKILL.md
  - codex/agents/*.toml

It does not score subjective quality. It emits evidence for the LLM rubric pass.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from fixture_validator import FixtureValidationError, validate_fixture

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback message
    tomllib = None  # type: ignore[assignment]


REQUIRED_AGENT_KEYS = ("name", "description", "developer_instructions")
VALID_SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}


def find_repo_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if (candidate / "codex" / "skills").is_dir() or (candidate / "codex" / "agents").is_dir():
            return candidate
    return None


def count_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return -1


def locale_readmes(skill_dir: Path) -> dict[str, bool]:
    return {
        "ko_default": (skill_dir / "README.md").is_file(),
        "en": (skill_dir / "README.en.md").is_file(),
        "ja": (skill_dir / "README.ja.md").is_file(),
        "ko": (skill_dir / "README.ko.md").is_file(),
    }


def lint_skill(skill_md: Path) -> list[dict[str, object]]:
    """Return warning-only, suppressible SKILL.md quality signals."""
    warnings: list[dict[str, object]] = []
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    def finding(rule_id: str, line: int, reason: str) -> dict[str, object]:
        context = "\n".join(lines[max(0, line - 3) : line - 1])
        suppressed = any(
            candidate.strip().startswith(f"eval-lint: suppress={rule_id} reason=")
            and bool(candidate.strip().split("reason=", 1)[1].strip())
            for candidate in context.splitlines()
        )
        return {"rule_id": rule_id, "line": line, "reason": reason, "suppressed": suppressed}

    if len(lines) > 500:
        warnings.append(finding("SKILL-L001", 1, "SKILL.md exceeds 500 lines"))
    seen: dict[str, int] = {}
    for number, line in enumerate(lines, start=1):
        normalized = line.strip()
        if normalized and normalized in seen and not normalized.startswith(("#", "|")):
            warnings.append(finding("SKILL-L002", number, f"duplicate instruction; first appears on line {seen[normalized]}"))
        elif normalized:
            seen[normalized] = number
        if normalized.lower().startswith(("note:", "information:", "참고:")):
            warnings.append(finding("SKILL-L003", number, "non-imperative guidance candidate"))
    return warnings


def enumerate_skills(repo_root: Path) -> list[dict]:
    root = repo_root / "codex" / "skills"
    skills: list[dict] = []
    if not root.is_dir():
        return skills

    for skill_dir in sorted(root.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_dir.is_dir() or not skill_md.is_file():
            continue
        skills.append(
            {
                "kind": "skill",
                "name": skill_dir.name,
                "path": str(skill_dir.relative_to(repo_root)),
                "skill_md": str(skill_md.relative_to(repo_root)),
                "body_lines": count_lines(skill_md),
                "locale_readmes": locale_readmes(skill_dir),
                "has_references": (skill_dir / "references").is_dir(),
                "has_evals": (skill_dir / "evals").is_dir(),
                "has_openai_yaml": (skill_dir / "agents" / "openai.yaml").is_file(),
                "linter_warnings": lint_skill(skill_md),
            }
        )
    return skills


def parse_agent_toml(path: Path) -> tuple[dict | None, list[str]]:
    if tomllib is None:
        return None, ["Python tomllib is unavailable; use Python 3.11 or newer."]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report parse error to gate payload
        return None, [f"TOML parse error: {exc}"]
    return data, []


def validate_agent(path: Path) -> dict:
    data, errors = parse_agent_toml(path)
    warnings: list[str] = []
    if data is None:
        return {"passed": False, "errors": errors, "warnings": warnings}

    for key in REQUIRED_AGENT_KEYS:
        if not isinstance(data.get(key), str) or not data.get(key, "").strip():
            errors.append(f"missing or empty required key: {key}")

    if data.get("name") != path.stem:
        errors.append(f"name '{data.get('name')}' does not match filename stem '{path.stem}'")

    sandbox_mode = data.get("sandbox_mode")
    if sandbox_mode not in VALID_SANDBOX_MODES:
        errors.append(f"invalid or missing sandbox_mode: {sandbox_mode}")

    if not isinstance(data.get("model"), str) or not data.get("model", "").strip():
        warnings.append("missing model; score A5 manually")

    instructions = data.get("developer_instructions", "")
    if isinstance(instructions, str):
        for marker in ("Mission:", "Boundaries:", "Output:"):
            if marker not in instructions:
                warnings.append(f"developer_instructions missing marker: {marker}")
        if "Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>" not in instructions:
            warnings.append("output contract does not show the shared Status line")

    return {"passed": not errors, "errors": errors, "warnings": warnings}


def enumerate_agents(repo_root: Path) -> list[dict]:
    root = repo_root / "codex" / "agents"
    agents: list[dict] = []
    if not root.is_dir():
        return agents

    for path in sorted(root.glob("*.toml")):
        data, parse_errors = parse_agent_toml(path)
        agent = {
            "kind": "agent",
            "name": path.stem,
            "path": str(path.relative_to(repo_root)),
            "body_lines": count_lines(path),
            "toml_keys": sorted(data.keys()) if data else [],
            "sandbox_mode": data.get("sandbox_mode") if data else None,
            "model": data.get("model") if data else None,
            "model_reasoning_effort": data.get("model_reasoning_effort") if data else None,
            "gate": validate_agent(path) if not parse_errors else {
                "passed": False,
                "errors": parse_errors,
                "warnings": [],
            },
        }
        agents.append(agent)
    return agents


def fixture_diagnostics(repo_root: Path) -> list[dict[str, object]]:
    """Expose read-only V1/V2 validation evidence to evaluator callers."""
    evaluator_root = repo_root / ".codex" / "skills" / "ywc-codex-toolkit-eval" / "evals"
    diagnostics: list[dict[str, object]] = []
    for path in (evaluator_root / "evals.json", evaluator_root / "agent-smoke-fixtures.json",
                 evaluator_root / "agent-smoke-fixtures.v2.json"):
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            normalized = validate_fixture(
                payload,
                fixture_root=evaluator_root / "fixtures",
                available_skills={skill["name"] for skill in enumerate_skills(repo_root)},
            )
            diagnostics.append({"path": str(path.relative_to(repo_root)), "passed": True, "schema": normalized["schema"], "v1_remaining": normalized["v1_remaining"]})
        except (OSError, json.JSONDecodeError, FixtureValidationError) as exc:
            diagnostics.append({"path": str(path.relative_to(repo_root)), "passed": False, "error": str(exc)})
    return diagnostics


def run_skill_validator(repo_root: Path) -> dict:
    script = repo_root / "scripts" / "validate.sh"
    if not script.is_file():
        return {"available": False, "passed": None, "detail": "missing scripts/validate.sh"}

    try:
        proc = subprocess.run(
            ["bash", str(script)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return {
            "available": True,
            "passed": False,
            "returncode": None,
            "detail": "scripts/validate.sh timed out after 300s",
        }
    return {
        "available": True,
        "passed": proc.returncode == 0,
        "returncode": proc.returncode,
        "detail": (proc.stderr or proc.stdout).strip()[-4000:],
    }


def summarize(skills: list[dict], agents: list[dict], skill_gate: dict) -> dict:
    agent_failures = [a for a in agents if not a["gate"]["passed"]]
    missing_openai = [s["name"] for s in skills if not s["has_openai_yaml"]]
    incomplete_readmes = [
        s["name"]
        for s in skills
        if not all(s["locale_readmes"].values())
    ]
    return {
        "skill_count": len(skills),
        "agent_count": len(agents),
        "skill_gate_passed": skill_gate.get("passed"),
        "agent_gate_failures": len(agent_failures),
        "skills_missing_openai_yaml": missing_openai,
        "skills_incomplete_locale_readmes": incomplete_readmes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--only", choices=["skills", "agents"], default=None)
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    parser.add_argument("--skip-gate", action="store_true", help="skip structural validators")
    args = parser.parse_args()

    start = (args.repo_root or Path(__file__).resolve()).resolve()
    repo_root = find_repo_root(start if start.is_dir() else start.parent)
    if repo_root is None:
        print("error: could not locate repository root", file=sys.stderr)
        return 1

    skills = [] if args.only == "agents" else enumerate_skills(repo_root)
    agents = [] if args.only == "skills" else enumerate_agents(repo_root)
    skill_gate = (
        {"available": False, "passed": None, "detail": "skipped"}
        if args.skip_gate or args.only == "agents"
        else run_skill_validator(repo_root)
    )

    payload = {
        "repo_root": str(repo_root),
        "scope": args.only or "all",
        "skills": skills,
        "agents": agents,
        "fixture_diagnostics": fixture_diagnostics(repo_root),
        "gate": {
            "skills_structural": skill_gate,
            "agents_structural": {
                "available": True,
                "passed": not any(not a["gate"]["passed"] for a in agents),
                "detail": "project-local TOML gate embedded in inventory_gate.py",
            },
        },
        "summary": summarize(skills, agents, skill_gate),
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    summary = payload["summary"]
    print(f"repo_root: {repo_root}")
    print(f"scope: {payload['scope']}")
    print(f"skills: {summary['skill_count']}   agents: {summary['agent_count']}")
    print(f"skill gate: {summary['skill_gate_passed']}")
    print(f"agent gate failures: {summary['agent_gate_failures']}")
    print(f"skills missing openai.yaml: {len(summary['skills_missing_openai_yaml'])}")
    print(f"skills incomplete locale README set: {len(summary['skills_incomplete_locale_readmes'])}")
    print("\nRun with --json for the scoring evidence payload.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
