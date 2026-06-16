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
SKILL_ROOTS = ["claude-code/skills"]
AGENT_ROOTS = ["claude-code/agents"]
REQUIRED_LOCALES = ["README.md", "README.en.md", "README.ja.md", "README.ko.md"]
FULL_LOCALES = REQUIRED_LOCALES + ["README.es.md", "README.zh.md"]
COLLISION_JACCARD = 0.18  # word-trigram Jaccard above this = likely description collision
HISTORY_MECH = Path(__file__).resolve().parent.parent / "evals" / "history.mechanical.json"

HANGUL = re.compile(r"[가-힣]")
KANA = re.compile(r"[぀-ヿ]")
MUTATING_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit", "Bash"}
READONLY_HINT = re.compile(r"review|audit|analyst|reviewer|read-only", re.IGNORECASE)

# A5 model-tier heuristic (FR3) — role keywords matched against the agent NAME,
# the canonical role id. Descriptions are deliberately NOT matched: they
# cross-reference sibling agents (e.g. "route to ywc-architect"), which would
# false-flag many agents as Opus-expected. Authoritative mapping and the pinned
# 12-agent table live in references/agent-rubric.md §A5 (Amendment A1).
A5_OPUS_ROLE_KW = ("architect", "root-cause", "root_cause", "rootcause", "critic")
A5_HAIKU_ROLE_KW = ("doc-writer", "documentation", "formatting",
                    "mechanical", "enumeration")
A5_TIER_RANK = {"haiku": 1, "sonnet": 2, "opus": 3}

# FR1b coverage gate — per-item trigger-case minimums (signals-only, never axes).
TRIGGER_CASES = Path(__file__).resolve().parent.parent / "evals" / "trigger-cases.json"
COVERAGE_MIN_POSITIVES = 3
COVERAGE_MIN_COLLISIONS = 2


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


def _excluded_in_anti_trigger(desc: str, sibling: str) -> bool:
    """True if `sibling` is named inside the description's 'Do not use for' clause (FR6).

    Clause-aware, not substring-anywhere: a sibling mentioned only in a
    cooperative/positive sentence no longer suppresses a real collision. All
    current catalog clauses are English (Amendment A4); localized clause
    detection is deferred.
    """
    m = re.search(r"Do not use for(?P<clause>.*?)(?:[.!?\n]|$)", desc, re.IGNORECASE)
    if not m:
        return False
    clause = m.group("clause").lower()
    target = sibling.lower()
    return re.search(rf"(?<![a-z0-9-]){re.escape(target)}(?![a-z0-9-])", clause) is not None


def find_collisions(items: list[dict]) -> dict:
    """Map item-name -> [(sibling, jaccard)] for description overlaps above threshold."""
    grams = {it["name"]: word_trigrams(it["description"]) for it in items}
    descs = {it["name"]: it["description"] for it in items}
    out: dict[str, list] = {}
    names = list(grams)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            j = jaccard(grams[a], grams[b])
            if j >= COLLISION_JACCARD:
                # real collision unless each names the other inside its own
                # "Do not use for" anti-trigger clause (FR6 — clause-aware)
                if not (_excluded_in_anti_trigger(descs[a], b)
                        or _excluded_in_anti_trigger(descs[b], a)):
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


def expected_model_tier(name: str) -> str:
    """Infer an agent's expected model tier from its role keywords (FR3).

    Matched against the agent NAME only — see the A5_*_ROLE_KW note above.
    Opus = frontier judgment (architecture, root-cause, critic);
    Haiku = doc / formatting / mechanical enumeration; everything else = Sonnet.
    """
    hay = name.lower()
    if any(k in hay for k in A5_OPUS_ROLE_KW):
        return "opus"
    if any(k in hay for k in A5_HAIKU_ROLE_KW):
        return "haiku"
    return "sonnet"


def declared_model_tier(model: str) -> str | None:
    """Normalize a declared `model:` value to a tier, or None if unrecognized."""
    m = model.lower()
    for tier in ("opus", "sonnet", "haiku"):
        if tier in m:
            return tier
    return None


def a5_model_band(name: str, model: str) -> int:
    """Band the declared model against the expected tier (FR3).

    match -> 5; over-provisioned -> 3; under-provisioned -> 2; no model -> 0;
    model present but tier unrecognized -> 4 (cannot verify). Bands are pinned
    by references/agent-rubric.md §A5 (Amendment A1: the 12 current agents all
    score 5).
    """
    if not model:
        return 0
    declared = declared_model_tier(model)
    if declared is None:
        return 4
    expected = expected_model_tier(name)
    if declared == expected:
        return 5
    return 3 if A5_TIER_RANK[declared] > A5_TIER_RANK[expected] else 2


def load_coverage() -> dict:
    """Per-item trigger-case coverage from trigger-cases.json (FR1b).

    Returns {item_name: {"positives": int, "collisions": int, "sufficient": bool}}.
    Collisions count cases where the item is the owner (`expected`) or the near
    sibling (`impostor`), per the paired convention; a single case id is not
    double-counted for the same item. Missing file -> empty map.
    """
    if not TRIGGER_CASES.exists():
        return {}
    data = json.loads(TRIGGER_CASES.read_text(encoding="utf-8"))
    pos: dict[str, int] = {}
    coll: dict[str, int] = {}
    seen_ids: set[str] = set()
    for c in data.get("cases", []):
        cid = c.get("id")
        if cid is not None:
            if cid in seen_ids:
                continue  # a duplicate case id must not inflate coverage counts
            seen_ids.add(cid)
        kind = c.get("kind")
        if kind == "positive":
            exp = c.get("expected")
            if exp:
                pos[exp] = pos.get(exp, 0) + 1
        elif kind == "collision":
            for name in {v for v in (c.get("expected"), c.get("impostor")) if v}:
                coll[name] = coll.get(name, 0) + 1
    out: dict[str, dict] = {}
    for name in set(pos) | set(coll):
        p, m = pos.get(name, 0), coll.get(name, 0)
        out[name] = {
            "positives": p,
            "collisions": m,
            "sufficient": p >= COVERAGE_MIN_POSITIVES and m >= COVERAGE_MIN_COLLISIONS,
        }
    return out


# --- skill scoring ---------------------------------------------------------

def score_skill(d: Path, collisions: dict, coverage: dict) -> dict:
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
        "A7_rationalization": _rationalization_data_rows(body) >= 5,
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

    # FR1b coverage — signals-only; S1 stays null in axes (Amendment A2)
    signals["coverage"] = coverage.get(
        name, {"positives": 0, "collisions": 0, "sufficient": False})

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


def _rationalization_data_rows(body: str) -> int:
    """Count data rows in the Rationalization Defense table (FR4).

    Data rows = table lines (lstripped, starting with '|') minus the separator
    row(s) and the header row. Returns 0 when the section is absent. The rubric
    (references/skill-rubric.md A7) requires >= 5 data rows.
    """
    idx = body.find("## Rationalization Defense")
    if idx == -1:
        return 0
    nxt = body.find("\n## ", idx + 1)
    section = body[idx:nxt if nxt != -1 else len(body)]
    rows = [ln for ln in section.splitlines() if ln.lstrip().startswith("|")]
    seps = [ln for ln in rows if set(ln.strip()) <= set("|-: ")]
    data = len(rows) - len(seps)
    if data > 0:
        data -= 1  # drop the header row
    return max(0, data)


def _unresolved_sibling_pointers(desc: str) -> list:
    """Flag `use ywc-<name>` pointers resolving to neither a skill dir nor an agent file (FR10)."""
    out = []
    for m in re.finditer(r"use (ywc-[\w-]+)", desc):
        sib = m.group(1)
        in_skill = any((REPO_ROOT / r / sib).is_dir() for r in SKILL_ROOTS)
        in_agent = any((REPO_ROOT / r / f"{sib}.md").is_file() for r in AGENT_ROOTS)
        if not (in_skill or in_agent):
            out.append(sib)
    return out


# --- agent scoring ---------------------------------------------------------

def score_agent(path: Path, collisions: dict, coverage: dict) -> dict:
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    name = fm.get("name", path.stem)
    desc = fm.get("description", "")
    tools_raw = fm.get("tools", "")
    instr = body
    sandbox = ""
    model = fm.get("model", "")

    # Read-only role must be inferred from the agent's OWN role statement (name
    # or the description prefix before "Triggers:"), not from incidental mentions
    # of "review"/"audit" in its dispatcher trigger list — otherwise a coder/test
    # agent dispatched BY a review skill is wrongly flagged read-only (A3 false-).
    role_text = desc.split("Triggers:")[0]
    readonly_role = bool(READONLY_HINT.search(name) or READONLY_HINT.search(role_text))
    signals: dict = {}

    # A3 tool minimality
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
    a4 = 5 if (has_status or has_contract_ref) else (2 if re.search(r"output|format|return", instr, re.I) else 1)
    signals["has_status_contract"] = has_status
    signals["has_contract_ref"] = has_contract_ref
    signals["contract_states"] = states

    # A5 model-tier appropriateness (FR3 — role<->tier heuristic, was constant 4)
    a5 = a5_model_band(name, model)
    signals["model"] = model
    signals["model_expected"] = expected_model_tier(name)

    # A2 collision sub-signal
    coll = collisions.get(name, [])
    signals["collision_pairs"] = coll

    # FR1b coverage — signals-only; A2 stays null in axes (Amendment A2)
    signals["coverage"] = coverage.get(
        name, {"positives": 0, "collisions": 0, "sufficient": False})

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
    return sorted(root.glob("ywc-*.md"))


def evaluate(target: str) -> dict:
    results: dict[str, list] = {}
    coverage = load_coverage()
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
                fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
                descs.append({"name": fm.get("name", p.stem),
                              "description": fm.get("description", "")})
            collisions = find_collisions(descs)
            results[rel] = [score_agent(p, collisions, coverage) for p in items]
        else:
            dirs = collect_skills(root)
            descs = []
            for d in dirs:
                fm, _ = split_frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
                descs.append({"name": fm.get("name", d.name),
                              "description": fm.get("description", "")})
            collisions = find_collisions(descs)
            results[rel] = [score_skill(d, collisions, coverage) for d in dirs]
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
    for key in sorted(set(prior) - set(current)):
        regressions.append(f"{key}: removed from current mechanical results")
    for key, axes in current.items():
        for axis in sorted(set(prior.get(key, {})) - set(axes)):
            regressions.append(f"{key} {axis}: removed from current mechanical results")
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

    # FR2: --ci writes the full-catalog regression baseline; combining it with
    # --item would overwrite history.mechanical.json with a single-item partial.
    # Reject before evaluate()/ci_gate() so no baseline write can happen.
    if args.ci and args.item:
        print("[error] --ci cannot be combined with --item: the regression "
              "baseline would be overwritten with a single-item partial. "
              "Run --ci without --item, or drop --ci to score one item.",
              file=sys.stderr)
        return 2

    results = evaluate(args.target)
    if args.item:
        results = {rel: [it for it in items if it["name"] == args.item]
                   for rel, items in results.items()}
        results = {rel: items for rel, items in results.items() if items}

    # FR1b: catalog-level coverage summary (stderr keeps stdout JSON-clean).
    below = sum(1 for items in results.values() for it in items
                if not it["signals"].get("coverage", {}).get("sufficient", False))
    total = sum(len(items) for items in results.values())
    print(f"[coverage] {below} items below minimum (of {total}; need "
          f">= {COVERAGE_MIN_POSITIVES} positives & "
          f">= {COVERAGE_MIN_COLLISIONS} collisions per item)", file=sys.stderr)

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
