#!/usr/bin/env python3
"""Mechanical (deterministic) scorer for ywc-toolkit-eval.

Scores the structural / token / integrity axes that need no model judgment:
  skills -> S2 (structure), S4 (token economy), S5 (integrity), S1-collision signal
  agents -> A3 (tool minimality), A4 (output contract), A5 (model present),
            A2-collision signal

Judgment axes (S1 precision/recall, S3, S6, A1, A2 precision, A6) are emitted as
null for the agent judge pass to fill. Usage:

  python3 score.py --target claude-code/skills --format json
  python3 score.py --target all --format markdown
  python3 score.py --ci          # regression gate vs history.mechanical.json

Stdlib only — no third-party dependencies (matches repo convention for skill scripts).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

# --- repo roots ------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOTS = ["claude-code/skills", "codex/skills"]
AGENT_ROOTS = ["claude-code/agents", "codex/agents"]
REQUIRED_LOCALES = ["README.md", "README.en.md", "README.ja.md", "README.ko.md"]
FULL_LOCALES = REQUIRED_LOCALES + ["README.es.md", "README.zh.md"]
COLLISION_JACCARD = 0.18  # word-trigram Jaccard above this = likely description collision
HISTORY_MECH = Path(__file__).resolve().parent.parent / "evals" / "history.mechanical.json"

HANGUL = re.compile(r"[가-힣]")
KANA = re.compile(r"[぀-ヿ]")
MUTATING_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit", "Bash"}
READONLY_HINT = re.compile(r"review|audit|analyst|reviewer|read-only", re.IGNORECASE)


# --- frontmatter / file parsing -------------------------------------------

def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter-dict, body) for a Markdown file with YAML frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip("\n")
    body = text[end + 4:]
    return parse_yaml_lite(fm_raw), body


def parse_yaml_lite(fm_raw: str) -> dict:
    """Minimal YAML reader: top-level `key:` plus folded (>-) multi-line values."""
    fields: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in fm_raw.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s?(.*)$", line)
        if m and not line.startswith(" "):
            if key is not None:
                fields[key] = " ".join(s.strip() for s in buf).strip()
            key, first = m.group(1), m.group(2).strip()
            buf = [] if first in (">-", ">", "|", "|-", "") else [first]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        fields[key] = " ".join(s.strip() for s in buf).strip()
    return fields


def parse_toml_lite(text: str) -> tuple[dict, str]:
    """Read top-level key = value pairs + the developer_instructions block from a Codex agent."""
    fields: dict[str, str] = {}
    for m in re.finditer(r'^([a-z_]+)\s*=\s*"([^"]*)"', text, re.MULTILINE):
        fields[m.group(1)] = m.group(2)
    block = re.search(r'developer_instructions\s*=\s*"""(.*?)"""', text, re.DOTALL)
    instructions = block.group(1) if block else ""
    return fields, instructions


# --- scoring helpers -------------------------------------------------------

def word_trigrams(desc: str) -> set:
    # Unicode-aware: capture Hangul / Kana / Latin tokens so collisions between
    # Korean/Japanese-heavy descriptions are detected, not silently dropped.
    words = re.findall(r"[^\W\d_]{3,}", desc.lower(), flags=re.UNICODE)
    return {tuple(words[i:i + 3]) for i in range(len(words) - 2)}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_collisions(items: list[dict]) -> dict:
    """Map item-name -> [(sibling, jaccard)] for description overlaps above threshold."""
    grams = {it["name"]: word_trigrams(it["description"]) for it in items}
    out: dict[str, list] = {}
    names = list(grams)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            j = jaccard(grams[a], grams[b])
            if j >= COLLISION_JACCARD:
                # only a real collision if neither names the other as an exclusion
                ad = next(x["description"] for x in items if x["name"] == a)
                bd = next(x["description"] for x in items if x["name"] == b)
                if b not in ad and a not in bd:
                    out.setdefault(a, []).append([b, round(j, 3)])
                    out.setdefault(b, []).append([a, round(j, 3)])
    return out


def band(n: int, thresholds: list[int]) -> int:
    """Map a count to a 0-5 score given ascending pass thresholds (len 5)."""
    score = 0
    for t in thresholds:
        if n >= t:
            score += 1
    return min(score, 5)


# --- skill scoring ---------------------------------------------------------

def score_skill(d: Path, collisions: dict) -> dict:
    fm, body = split_frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
    name = fm.get("name", d.name)
    desc = fm.get("description", "")
    body_lines = body.count("\n") + 1
    signals: dict = {}

    # S2 structure compliance (A1-A14 subset)
    checks = {
        "A1_name_prefix": name.startswith("ywc-") and name == d.name,
        "A2_use_when": desc.startswith("(ywc) Use when"),
        "A3_anti_trigger": "Do not use for" in desc,
        "A4_multilingual": bool(HANGUL.search(desc) and KANA.search(desc)),
        "A6_announce": "**Announce at start:**" in body[:400],
        "A7_rationalization": "## Rationalization Defense" in body
        and body.count("\n|", body.find("## Rationalization Defense"),
                       body.find("## Rationalization Defense") + 2000) >= 6,
        "A8_body_cap": body_lines <= 500,
        "A9_no_force_load": not re.search(r"@ywc-[\w-]+", body),
        "A11_locales": all((d / loc).exists() for loc in REQUIRED_LOCALES),
        "A14_ref_pointers": _refs_have_pointers(d, body),
    }
    s2 = round(sum(checks.values()) / len(checks) * 5)
    signals["structure_checks"] = {k: bool(v) for k, v in checks.items()}

    # S4 token economy
    over_extracted = _over_extracted_refs(d)
    desc_is_lean = len(desc) < 900 and not re.search(r"\bStep \d", desc)
    s4 = 5
    if body_lines > 500:
        s4 -= 2
    if body_lines > 700:
        s4 -= 1
    if not desc_is_lean:
        s4 -= 1
    if over_extracted:
        s4 -= 1
    s4 = max(0, min(5, s4))
    signals["body_lines"] = body_lines
    signals["over_extracted_refs"] = over_extracted

    # S5 consistency & integrity
    missing_required = [loc for loc in REQUIRED_LOCALES if not (d / loc).exists()]
    missing_full = [loc for loc in FULL_LOCALES if not (d / loc).exists()]
    dangling = _dangling_ref_links(d, body)
    bad_pointers = _unresolved_sibling_pointers(desc)
    s5 = 5
    if missing_full and not missing_required:
        s5 -= 1
    if dangling:
        s5 -= 2
    if bad_pointers:
        s5 -= 1
    if missing_required:
        s5 = 0
    s5 = max(0, min(5, s5))
    signals["missing_locales"] = missing_full
    signals["dangling_ref_links"] = dangling
    signals["unresolved_anti_trigger_pointers"] = bad_pointers

    # S1 collision sub-signal (judge fills precision/recall)
    coll = collisions.get(name, [])
    signals["collision_pairs"] = coll

    return {
        "name": name,
        "kind": "skill",
        "axes": {"S1": None, "S2": s2, "S3": None, "S4": s4, "S5": s5, "S6": None},
        "s1_collision_cap": 3 if coll else None,
        "signals": signals,
    }


def _refs_have_pointers(d: Path, body: str) -> bool:
    ref_dir = d / "references"
    if not ref_dir.is_dir():
        return True
    for ref in ref_dir.glob("*.md"):
        if ref.name not in body:
            return False
    return True


def _over_extracted_refs(d: Path) -> list:
    ref_dir = d / "references"
    if not ref_dir.is_dir():
        return []
    return [r.name for r in ref_dir.glob("*.md")
            if r.read_text(encoding="utf-8").count("\n") < 30]


def _dangling_ref_links(d: Path, body: str) -> list:
    out = []
    for m in re.finditer(r"\(references/([\w.-]+)\)", body):
        if not (d / "references" / m.group(1)).exists():
            out.append(m.group(1))
    return out


def _unresolved_sibling_pointers(desc: str) -> list:
    out = []
    for m in re.finditer(r"use (ywc-[\w-]+)", desc):
        sib = m.group(1)
        if not any((REPO_ROOT / r / sib).is_dir() for r in SKILL_ROOTS):
            out.append(sib)
    return out


# --- agent scoring ---------------------------------------------------------

def score_agent(path: Path, collisions: dict) -> dict:
    if path.suffix == ".toml":
        fm, instr = parse_toml_lite(path.read_text(encoding="utf-8"))
        name = fm.get("name", path.stem)
        desc = fm.get("description", "")
        tools_raw = ""
        sandbox = fm.get("sandbox_mode", "")
        model = fm.get("model", "")
        is_codex = True
    else:
        fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
        name = fm.get("name", path.stem)
        desc = fm.get("description", "")
        tools_raw = fm.get("tools", "")
        instr = body
        sandbox = ""
        model = fm.get("model", "")
        is_codex = False

    readonly_role = bool(READONLY_HINT.search(name) or READONLY_HINT.search(desc))
    signals: dict = {}

    # A3 tool minimality
    if is_codex:
        a3 = 5 if sandbox == "read-only" else (3 if readonly_role else 4)
    else:
        tools = set(re.findall(r"[A-Z]\w+", tools_raw))
        mutating = tools & MUTATING_TOOLS
        if "*" in tools_raw:
            a3 = 1
        elif readonly_role and mutating:
            a3 = 3
        elif mutating and not readonly_role:
            a3 = 4
        else:
            a3 = 5
        signals["tools"] = sorted(tools)
        signals["mutating_tools"] = sorted(mutating)
    signals["sandbox_mode"] = sandbox
    signals["readonly_role"] = readonly_role

    # A4 output contract. Claude Code agents satisfy the contract either by an
    # inline Status: block or by referencing the canonical Return Contract
    # (subagent-status-actions.md §3.5) — an inline-invented format does not.
    has_status = "Status:" in instr or "Status :" in instr
    has_contract_ref = "subagent-status-actions" in instr
    states = sum(s in instr for s in ("DONE", "BLOCKED", "NEEDS_CONTEXT", "DONE_WITH_CONCERNS"))
    if is_codex:
        a4 = 5 if (has_status and states >= 3) else (3 if has_status else 0)
    else:
        a4 = 5 if (has_status or has_contract_ref) else (2 if re.search(r"output|format|return", instr, re.I) else 1)
    signals["has_status_contract"] = has_status
    signals["has_contract_ref"] = has_contract_ref
    signals["contract_states"] = states

    # A5 model present (judge refines tier fit)
    a5 = 4 if model else 0
    signals["model"] = model

    # A2 collision sub-signal
    coll = collisions.get(name, [])
    signals["collision_pairs"] = coll

    return {
        "name": name,
        "kind": "agent",
        "axes": {"A1": None, "A2": None, "A3": a3, "A4": a4, "A5": a5, "A6": None},
        "a2_collision_cap": 3 if coll else None,
        "signals": signals,
    }


# --- orchestration ---------------------------------------------------------

def collect_skills(root: Path) -> list:
    return [d for d in sorted(root.iterdir())
            if d.is_dir() and (d / "SKILL.md").exists()]


def collect_agents(root: Path) -> list:
    return sorted([p for p in root.glob("ywc-*.md")] + [p for p in root.glob("ywc-*.toml")])


def evaluate(target: str) -> dict:
    results: dict[str, list] = {}
    roots = []
    if target == "all":
        roots = SKILL_ROOTS + AGENT_ROOTS
    else:
        roots = [target]
    for rel in roots:
        root = REPO_ROOT / rel
        if not root.is_dir():
            continue
        if "agents" in rel:
            items = collect_agents(root)
            descs = []
            for p in items:
                if p.suffix == ".toml":
                    fm, _ = parse_toml_lite(p.read_text(encoding="utf-8"))
                else:
                    fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
                descs.append({"name": fm.get("name", p.stem),
                              "description": fm.get("description", "")})
            collisions = find_collisions(descs)
            results[rel] = [score_agent(p, collisions) for p in items]
        else:
            dirs = collect_skills(root)
            descs = []
            for d in dirs:
                fm, _ = split_frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
                descs.append({"name": fm.get("name", d.name),
                              "description": fm.get("description", "")})
            collisions = find_collisions(descs)
            results[rel] = [score_skill(d, collisions) for d in dirs]
    return results


def mechanical_table(results: dict) -> str:
    lines = []
    for rel, items in results.items():
        lines.append(f"\n## {rel}  ({len(items)} items)\n")
        axes = list(items[0]["axes"].keys()) if items else []
        lines.append("| Item | " + " | ".join(axes) + " | collisions |")
        lines.append("|------|" + "----|" * (len(axes) + 1))
        for it in items:
            cells = []
            for a in axes:
                v = it["axes"][a]
                cells.append("·" if v is None else str(v))
            ncoll = len(it["signals"].get("collision_pairs", []))
            lines.append(f"| {it['name']} | " + " | ".join(cells) + f" | {ncoll} |")
    lines.append("\n(· = judgment axis, filled by the agent judge pass)")
    return "\n".join(lines)


def flatten_mech(results: dict) -> dict:
    flat = {}
    for rel, items in results.items():
        for it in items:
            flat[f"{rel}/{it['name']}"] = {a: v for a, v in it["axes"].items() if v is not None}
    return flat


def ci_gate(results: dict) -> int:
    current = flatten_mech(results)
    if not HISTORY_MECH.exists():
        HISTORY_MECH.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_MECH.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print("[ci] baseline written, no prior mechanical scores to compare. PASS")
        return 0
    prior = json.loads(HISTORY_MECH.read_text(encoding="utf-8"))
    regressions = []
    for key, axes in current.items():
        for axis, val in axes.items():
            old = prior.get(key, {}).get(axis)
            if old is not None and val < old:
                regressions.append(f"{key} {axis}: {old} -> {val}")
    if regressions:
        print("[ci] MECHANICAL REGRESSION DETECTED:")
        for r in regressions:
            print("  ▼ " + r)
        print(f"[ci] {len(regressions)} regression(s). FAIL")
        return 1
    HISTORY_MECH.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(f"[ci] {len(current)} items, no mechanical regression. PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="all")
    ap.add_argument("--item", default=None)
    ap.add_argument("--format", choices=["json", "markdown"], default="json")
    ap.add_argument("--ci", action="store_true")
    args = ap.parse_args()

    results = evaluate(args.target)
    if args.item:
        results = {rel: [it for it in items if it["name"] == args.item]
                   for rel, items in results.items()}
        results = {rel: items for rel, items in results.items() if items}

    if args.ci:
        return ci_gate(results)

    if args.format == "markdown":
        stamp = datetime.date.today().isoformat()
        print(f"# Mechanical Scorecard — {stamp}")
        print(mechanical_table(results))
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
