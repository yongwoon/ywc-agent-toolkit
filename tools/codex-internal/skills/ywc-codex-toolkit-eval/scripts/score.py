#!/usr/bin/env python3
"""Mechanical scorer for this repository's Codex skill/agent evaluation.

This script intentionally scores only deterministic axes. Judgment axes stay
null so a model judge can fill them without pretending the mechanical pass is a
final quality verdict.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


SKILL_ROOT = Path("codex/skills")
AGENT_ROOT = Path("codex/agents")
REQUIRED_READMES = ("README.md", "README.en.md", "README.ja.md", "README.ko.md")
DEFAULT_HISTORY = Path(__file__).resolve().parent.parent / "evals" / "history.mechanical.json"

SKILL_WEIGHTS = {
    "S1": 0.18,
    "S2": 0.14,
    "S3": 0.10,
    "S4": 0.17,
    "S5": 0.13,
    "S6": 0.10,
    "S7": 0.10,
    "S8": 0.08,
}
AGENT_WEIGHTS = {
    "A1": 0.16,
    "A2": 0.14,
    "A3": 0.16,
    "A4": 0.13,
    "A5": 0.10,
    "A6": 0.14,
    "A7": 0.09,
    "A8": 0.08,
}

CLAUDE_ONLY_PATTERNS = (
    r"tools/claude-code/skills",
    r"tools/claude-code/agents",
    r"Task\(subagent_type=",
    r"allowed-tools:",
    r"(?<![\w/-])/ywc-[a-z0-9-]+\b",
)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    return parse_yaml_lite(text[4:end]), text[end + 4 :]


def parse_yaml_lite(raw: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match and not line.startswith((" ", "\t")):
            if key is not None:
                fields[key] = " ".join(part.strip() for part in buf).strip().strip("'\"")
            key = match.group(1)
            first = match.group(2).strip()
            buf = [] if first in (">", ">-", "|", "|-", "") else [first]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        fields[key] = " ".join(part.strip() for part in buf).strip().strip("'\"")
    return fields


def parse_agent_toml(path: Path) -> tuple[dict[str, object], str, list[str]]:
    if tomllib is None:
        return {}, "", ["Python tomllib is unavailable; use Python 3.11 or newer."]
    try:
        text = path.read_text(encoding="utf-8")
        data = tomllib.loads(text)
    except Exception as exc:  # noqa: BLE001 - surfaced as mechanical evidence
        return {}, "", [f"TOML parse error: {exc}"]
    instructions = data.get("developer_instructions", "")
    return data, instructions if isinstance(instructions, str) else "", []


def score_from_checks(checks: dict[str, bool]) -> int:
    if not checks:
        return 0
    return round(sum(1 for passed in checks.values() if passed) / len(checks) * 4)


def line_count(text: str) -> int:
    return len(text.splitlines())


def relative_key(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root))


def find_repo_root(start: Path) -> Path:
    probe = start if start.is_dir() else start.parent
    for candidate in [probe, *probe.parents]:
        if (candidate / SKILL_ROOT).is_dir() or (candidate / AGENT_ROOT).is_dir():
            return candidate
    raise RuntimeError(
        f"could not locate repository root containing {SKILL_ROOT} or {AGENT_ROOT} from {start}"
    )


def readme_checks(skill_dir: Path) -> dict[str, bool]:
    return {name: (skill_dir / name).is_file() for name in REQUIRED_READMES}


def has_openai_yaml(skill_dir: Path) -> bool:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return all(marker in text for marker in ("interface:", "display_name:", "short_description:", "default_prompt:"))


def referenced_files_exist(skill_dir: Path, body: str) -> list[str]:
    missing: list[str] = []
    for match in re.finditer(r"\((references/[^)#\s]+)\)", body):
        rel = match.group(1)
        if not (skill_dir / rel).is_file():
            missing.append(rel)
    return sorted(set(missing))


def reference_files_are_linked(skill_dir: Path, body: str) -> bool:
    ref_dir = skill_dir / "references"
    if not ref_dir.is_dir():
        return True
    return all(ref.name in body for ref in ref_dir.glob("*.md"))


def score_progressive_disclosure(skill_dir: Path, body: str) -> int:
    lines = line_count(body)
    linked = reference_files_are_linked(skill_dir, body)
    if lines <= 500 and linked:
        return 4
    if lines <= 550 and linked:
        return 3
    if lines <= 700:
        return 2
    return 1 if lines <= 1000 else 0


def score_output_contract(skill_dir: Path, body: str) -> int:
    checks = {
        "output_format": "## Output Format" in body or "Output:" in body,
        "validation": "## Validation" in body or "Validation Checklist" in body,
        "evals_or_scripts": (skill_dir / "evals").is_dir() or (skill_dir / "scripts").is_dir(),
        "status_or_template": "Status:" in body or "```text" in body,
    }
    return score_from_checks(checks)


def score_bundle_maintainability(skill_dir: Path, body: str) -> int:
    missing_links = referenced_files_exist(skill_dir, body)
    checks = {
        "readmes": all(readme_checks(skill_dir).values()),
        "openai_yaml": has_openai_yaml(skill_dir),
        "reference_links": not missing_links,
        "references_linked": reference_files_are_linked(skill_dir, body),
    }
    return score_from_checks(checks)


def score_runtime_fit(frontmatter: dict[str, str], body: str) -> int:
    combined = json.dumps(frontmatter, ensure_ascii=False) + "\n" + body
    hits = [pattern for pattern in CLAUDE_ONLY_PATTERNS if re.search(pattern, combined)]
    if not hits:
        return 4
    if len(hits) == 1:
        return 3
    if len(hits) == 2:
        return 2
    return 1


def score_skill(skill_dir: Path, repo_root: Path) -> dict[str, object]:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    declared_name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    schema_checks = {
        "frontmatter_name": declared_name == skill_dir.name,
        "frontmatter_description": bool(description),
        "strict_frontmatter_keys": set(frontmatter).issubset({"name", "description"}),
        "required_readmes": all(readme_checks(skill_dir).values()),
        "openai_yaml": has_openai_yaml(skill_dir),
    }
    axes: dict[str, int | None] = {
        "S1": None,
        "S2": score_from_checks(schema_checks),
        "S3": score_progressive_disclosure(skill_dir, body),
        "S4": None,
        "S5": score_output_contract(skill_dir, body),
        "S6": score_bundle_maintainability(skill_dir, body),
        "S7": score_runtime_fit(frontmatter, body),
        "S8": None,
    }
    return with_totals(
        {
            "kind": "skill",
            "name": skill_dir.name,
            "path": relative_key(skill_dir, repo_root),
            "axes": axes,
            "final_total": None,
            "signals": {
                "body_lines": line_count(body),
                "structure_checks": schema_checks,
                "missing_readmes": [name for name, ok in readme_checks(skill_dir).items() if not ok],
                "missing_reference_links": referenced_files_exist(skill_dir, body),
            },
        },
        SKILL_WEIGHTS,
    )


def score_agent(path: Path, repo_root: Path, skill_text_index: str) -> dict[str, object]:
    data, instructions, errors = parse_agent_toml(path)
    name = data.get("name")
    description = data.get("description")
    sandbox_mode = data.get("sandbox_mode")
    model = data.get("model")
    reasoning = data.get("model_reasoning_effort")
    structural_checks = {
        "toml_parse": not errors,
        "name_matches_file": name == path.stem,
        "description": isinstance(description, str) and bool(description.strip()),
        "developer_instructions": bool(instructions.strip()),
        "sandbox_mode": sandbox_mode in {"read-only", "workspace-write", "danger-full-access"},
        "model": isinstance(model, str) and bool(model.strip()),
        "reasoning_effort": isinstance(reasoning, str) and bool(reasoning.strip()),
        "no_claude_fields": not any(key in data for key in ("tools", "permissionMode")),
    }
    readonly_role = bool(re.search(r"review|audit|analyst|reviewer|read-only", f"{path.stem} {description}", re.I))
    sandbox_score = 4
    if sandbox_mode != "read-only" and readonly_role:
        sandbox_score = 1
    elif sandbox_mode not in {"read-only", "workspace-write"}:
        sandbox_score = 2
    output_checks = {
        "output_marker": "Output:" in instructions,
        "status_line": "Status:" in instructions,
        "shared_states": all(
            state in instructions
            for state in ("DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT")
        ),
    }
    caller_refs = len(re.findall(rf"(?<![\w-]){re.escape(path.stem)}(?![\w-])", skill_text_index))
    axes: dict[str, int | None] = {
        "A1": None,
        "A2": score_from_checks(structural_checks) if not errors else 0,
        "A3": None,
        "A4": sandbox_score,
        "A5": 4 if model and reasoning else (2 if model else 0),
        "A6": score_from_checks(output_checks),
        "A7": 4 if caller_refs else 1,
        "A8": None,
    }
    return with_totals(
        {
            "kind": "agent",
            "name": path.stem,
            "path": relative_key(path, repo_root),
            "axes": axes,
            "final_total": None,
            "signals": {
                "toml_errors": errors,
                "structural_checks": structural_checks,
                "sandbox_mode": sandbox_mode,
                "model": model,
                "caller_reference_count": caller_refs,
            },
        },
        AGENT_WEIGHTS,
    )


def with_totals(item: dict[str, object], weights: dict[str, float]) -> dict[str, object]:
    axes = item["axes"]
    assert isinstance(axes, dict)
    mechanical_points = 0.0
    mechanical_max = 0.0
    for axis, score in axes.items():
        if score is None:
            continue
        weight = weights[axis]
        mechanical_points += (int(score) / 4) * weight * 100
        mechanical_max += weight * 100
    item["mechanical_points"] = round(mechanical_points, 2)
    item["mechanical_max_points"] = round(mechanical_max, 2)
    return item


def collect_skill_text(repo_root: Path) -> str:
    parts: list[str] = []
    root = repo_root / SKILL_ROOT
    if not root.is_dir():
        return ""
    for path in root.glob("*/SKILL.md"):
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def evaluate(repo_root: Path, target: str, item: str | None) -> dict[str, object]:
    roots: dict[str, list[dict[str, object]]] = {}
    if target in ("all", str(SKILL_ROOT)):
        skill_root = repo_root / SKILL_ROOT
        skills = []
        if skill_root.is_dir():
            for skill_dir in sorted(skill_root.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
                    if item is None or skill_dir.name == item:
                        skills.append(score_skill(skill_dir, repo_root))
        roots[str(SKILL_ROOT)] = skills
    if target in ("all", str(AGENT_ROOT)):
        agent_root = repo_root / AGENT_ROOT
        agents = []
        skill_text_index = collect_skill_text(repo_root)
        if agent_root.is_dir():
            for agent_path in sorted(agent_root.glob("*.toml")):
                if item is None or agent_path.stem == item:
                    agents.append(score_agent(agent_path, repo_root, skill_text_index))
        roots[str(AGENT_ROOT)] = agents
    return {
        "schema": 1,
        "mode": "mechanical",
        "generated_at": dt.date.today().isoformat(),
        "repo_root": str(repo_root),
        "roots": roots,
        "note": "Judgment axes are null; final_total is intentionally unavailable in mechanical mode.",
    }


def flatten_mechanical(payload: dict[str, object]) -> dict[str, dict[str, int]]:
    flat: dict[str, dict[str, int]] = {}
    roots = payload["roots"]
    assert isinstance(roots, dict)
    for items in roots.values():
        assert isinstance(items, list)
        for item in items:
            assert isinstance(item, dict)
            axes = item["axes"]
            assert isinstance(axes, dict)
            path = item["path"]
            assert isinstance(path, str)
            flat[path] = {axis: int(score) for axis, score in axes.items() if score is not None}
    return flat


def write_baseline(history_file: Path, payload: dict[str, object]) -> None:
    history_file.parent.mkdir(parents=True, exist_ok=True)
    history = {
        "schema": 1,
        "updated_at": dt.date.today().isoformat(),
        "items": flatten_mechanical(payload),
    }
    history_file.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_ci(history_file: Path, payload: dict[str, object]) -> int:
    if not history_file.is_file():
        print(f"[ci] missing mechanical baseline: {history_file}")
        print("[ci] run with --update-baseline after reviewing the current mechanical scores.")
        return 2
    prior = json.loads(history_file.read_text(encoding="utf-8"))
    prior_items = prior.get("items", {})
    current = flatten_mechanical(payload)
    regressions: list[str] = []
    for path, axes in current.items():
        old_axes = prior_items.get(path, {})
        for axis, new_score in axes.items():
            old_score = old_axes.get(axis)
            if isinstance(old_score, int) and new_score < old_score:
                regressions.append(f"{path} {axis}: {old_score} -> {new_score}")
    if regressions:
        print("[ci] MECHANICAL REGRESSION DETECTED:")
        for regression in regressions:
            print(f"  - {regression}")
        return 1
    print(f"[ci] {len(current)} items, no mechanical regression. PASS")
    return 0


def markdown(payload: dict[str, object]) -> str:
    lines = [f"# Codex Mechanical Scorecard - {payload['generated_at']}", "", "Mode: mechanical (partial)"]
    roots = payload["roots"]
    assert isinstance(roots, dict)
    for root, items in roots.items():
        assert isinstance(items, list)
        lines.extend(["", f"## {root} ({len(items)} items)", ""])
        if not items:
            lines.append("_No items found._")
            continue
        axes = list(items[0]["axes"].keys())
        lines.append("| Item | " + " | ".join(axes) + " | Mechanical points | Final |")
        lines.append("|---|" + "|".join("---:" for _ in axes) + "|---:|---|")
        for item in items:
            axis_values = [
                "·" if item["axes"][axis] is None else str(item["axes"][axis])
                for axis in axes
            ]
            lines.append(
                f"| `{item['name']}` | "
                + " | ".join(axis_values)
                + f" | {item['mechanical_points']}/{item['mechanical_max_points']} | partial |"
            )
    lines.append("")
    lines.append("`·` means the axis requires the judgment pass.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--mode", choices=["mechanical", "judge", "full"], default="mechanical")
    parser.add_argument("--target", choices=["all", str(SKILL_ROOT), str(AGENT_ROOT)], default="all")
    parser.add_argument("--item", default=None)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--history-file", type=Path, default=DEFAULT_HISTORY)
    parser.add_argument("--ci", action="store_true", help="compare against baseline without rewriting it")
    parser.add_argument("--update-baseline", action="store_true", help="write the current mechanical baseline")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode != "mechanical":
        print(
            f"error: score.py only supports --mode mechanical; {args.mode} is skill-mediated",
            file=sys.stderr,
        )
        return 2
    repo_root = find_repo_root((args.repo_root or Path(__file__).resolve()).resolve())
    payload = evaluate(repo_root, args.target, args.item)
    if args.item is not None:
        roots = payload["roots"]
        assert isinstance(roots, dict)
        if not any(items for items in roots.values()):
            print(f"error: item not found: {args.item} in {args.target}", file=sys.stderr)
            return 2
    if args.update_baseline:
        write_baseline(args.history_file, payload)
        print(f"[baseline] wrote {args.history_file}")
        return 0
    if args.ci:
        return run_ci(args.history_file, payload)
    if args.format == "markdown":
        print(markdown(payload))
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
