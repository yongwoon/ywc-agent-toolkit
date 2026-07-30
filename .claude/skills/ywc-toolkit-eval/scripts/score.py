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
# Japanese evidence for A4: kana OR a CJK ideograph. Trigger phrases are often
# kanji-only compounds ("自律実行", "並列実行") with no kana; a kana-only check
# wrongly fails them. HANGUL is required separately, so a CJK ideograph
# alongside Hangul reliably indicates a Japanese (not Chinese) trigger here.
JAPANESE = re.compile(r"[぀-ヿ一-鿿]")
MUTATING_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit", "Bash"}
READONLY_HINT = re.compile(r"review|audit|analyst|reviewer|read-only", re.IGNORECASE)
# An implementer verb in the role's OPENING clause vetoes a read-only classification.
# Scoped to the opening clause (before the first em-dash) on purpose: scanning the whole
# role statement also matches negations and routing notes ("does NOT execute", "fixes go
# to X"), which would wrongly clear genuinely read-only agents.
IMPL_ROLE_HINT = re.compile(
    r"\b(implement|implementing|author|authoring|writ(?:e|ing)|modif(?:y|ying)"
    r"|provision|scaffold)\b",
    re.IGNORECASE,
)

# A5 model-tier heuristic (FR3) — role keywords matched against the agent NAME,
# the canonical role id. Descriptions are deliberately NOT matched: they
# cross-reference sibling agents (e.g. "route to ywc-architect"), which would
# false-flag many agents as Opus-expected. Authoritative mapping and the pinned
# 12-agent table live in references/agent-rubric.md §A5 (Amendment A1).
# "security" added per the CRITICAL-severity static-analysis judgment that
# ywc-security-engineer now runs on Opus for (#159) — same frontier-judgment
# bucket as architect/root-cause/critic.
A5_OPUS_ROLE_KW = ("architect", "root-cause", "root_cause", "rootcause", "critic",
                   "security")
A5_HAIKU_ROLE_KW = ("doc-writer", "documentation", "formatting",
                    "mechanical", "enumeration")
A5_TIER_RANK = {"haiku": 1, "sonnet": 2, "opus": 3}

# FR1b coverage gate — per-item trigger-case minimums (signals-only, never axes).
TRIGGER_CASES = Path(__file__).resolve().parent.parent / "evals" / "trigger-cases.json"
COVERAGE_MIN_POSITIVES = 3
COVERAGE_MIN_COLLISIONS = 2

# FR1c independence condition — where a case's *prompt* came from.
#
# A prompt written by reading the item's own `description` is then judged by a
# judge that reads that same description, so the case cannot fail: it measures
# the description against itself. Counting those toward the floor is what made
# S1/A2 unfailable — the 2026-07-22 sweep scored 5/5 for all 60 items with the
# three judge runs disagreeing on 0 of 353 cases. Only independently-sourced
# prompts count toward the floor.
#
# Provenance describes the prompt, not the label. Deciding which sibling *should*
# win a mined prompt is authoring work and does not re-introduce the circularity,
# so a `collision` can be independently sourced as long as its prompt is.
# Vocabulary is shared with the Codex-side scorer so one repo does not carry two
# contradictory provenance schemas.
CASE_SOURCE_DESCRIPTION = "description-derived"  # authored from the item's own description
CASE_SOURCE_SESSION_TRACE = "session-trace"      # mined from a real session transcript
CASE_SOURCE_USER_PROMPT = "user-prompt"          # verbatim prompt a user actually sent
CASE_SOURCES = (
    CASE_SOURCE_DESCRIPTION,
    CASE_SOURCE_SESSION_TRACE,
    CASE_SOURCE_USER_PROMPT,
)
INDEPENDENT_CASE_SOURCES = tuple(s for s in CASE_SOURCES if s != CASE_SOURCE_DESCRIPTION)
# An unlabeled case is not a claim of independence. Defaulting the other way
# would let every legacy case keep propping up the floor it was added to test.
DEFAULT_CASE_SOURCE = CASE_SOURCE_DESCRIPTION

# Prose lint — informational only, never feeds an axis or the CI baseline (same
# contract as signals["coverage"]). Detects instructions that cost tokens without
# changing agent behaviour: no-op exhortations and non-directive (advisory) phrasing.
# Promotion into S2/S4 is a separate PR, gated on a measured false-positive rate.
NOOP_PHRASES = (
    r"\b(?:write|keep|make)\s+(?:clean|readable|high[- ]quality|maintainable)\s+code\b",
    r"\b(?:follow|use)\s+best\s+practices\b",
    r"\bbe\s+(?:careful|thorough|diligent)\b",
    r"읽기\s*쉽게|가독성\s*(?:좋게|있게)",
    r"모범\s*사례|최선의\s*방법",
    r"(?:適切に|丁寧に)\s*\S*(?:実装|対応|記述)",
)
NONDIRECTIVE_PHRASES = (
    r"\b(?:is|are)\s+recommended\b",
    r"\bit\s+is\s+a\s+good\s+idea\b",
    r"\byou\s+may\s+want\s+to\b",
    r"\bshould\s+generally\b",
    r"권장됩니다|권장된다|하는\s*것이\s*좋습니다|바람직합니다",
    r"が望ましい|することを推奨",
)
# A line carrying any of these is treated as actionable, not an empty exhortation.
CONCRETE_ANCHOR_RE = re.compile(r"`[^`]+`|\b(?:Read|Grep|Glob|Bash|Edit|Write|Task)\b|/|\d")


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


def _unquote_scalar(value: str) -> str:
    """Strip surrounding YAML quotes and unescape, so a double-quoted
    `"(ywc) Use when ... \"trigger\""` scalar yields the same plain text a
    folded/plain scalar would. Without this, structure checks that match the
    leading `(ywc) Use when` prefix get a spurious `"` at position 0."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("\"", "'"):
        inner = value[1:-1]
        if value[0] == "\"":
            return inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner.replace("''", "'")
    return value


def parse_yaml_lite(fm_raw: str) -> dict:
    """Minimal YAML reader: top-level `key:` plus folded (>-) multi-line values."""
    fields: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in fm_raw.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s?(.*)$", line)
        if m and not line.startswith(" "):
            if key is not None:
                fields[key] = _unquote_scalar(" ".join(s.strip() for s in buf).strip())
            key, first = m.group(1), m.group(2).strip()
            buf = [] if first in (">-", ">", "|", "|-", "") else [first]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        fields[key] = _unquote_scalar(" ".join(s.strip() for s in buf).strip())
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


def a3_tool_band(tools_raw: str, readonly_role: bool) -> int:
    """Band an agent's tool grant for least privilege (A3).

    `*` (all tools) for any role -> 1. A read-only-by-role agent (reviewer /
    auditor / analyst) holding any mutating tool -> 3 (a real least-privilege
    violation). Every other bounded, explicit grant -> 5: an implementer agent
    (coder / worker) legitimately needs Write / Edit / Bash, so a bounded
    mutating grant on a non-read-only role is minimal-for-role, NOT an
    over-grant. The mechanical tier cannot tell "exactly needed" (band 5) from
    "one tool broader than needed" (band 4) without role knowledge, so it
    defaults to 5 and the judgment tier demotes to 4 when it spots a specific
    unused/extraneous tool. (Previously any mutating non-reviewer was capped at
    4, which under-scored every legitimately-mutating coder — see
    references/agent-rubric.md §A3.)
    """
    if "*" in tools_raw:
        return 1
    mutating = set(re.findall(r"[A-Z]\w+", tools_raw)) & MUTATING_TOOLS
    if readonly_role and mutating:
        return 3
    return 5


def load_coverage() -> dict:
    """Per-item trigger-case coverage from trigger-cases.json (FR1b + FR1c).

    Returns, per item::

        {"positives": int, "collisions": int,              # independent only
         "positives_total": int, "collisions_total": int,  # every case
         "sufficient": bool}

    Only cases whose `source` is in `INDEPENDENT_CASE_SOURCES` count toward the
    floor; description-derived cases are still reported in the `_total` counts so
    the gap between "cases we have" and "cases that can fail" stays visible. The
    counts are equal only when every case for that item is independently sourced.

    Collisions count cases where the item is the owner (`expected`) or the near
    sibling (`impostor`), per the paired convention; a single case id is not
    double-counted for the same item. Missing file -> empty map.

    Raises ValueError on an unrecognised `source` — a typo must not silently
    demote a case to description-derived, nor silently promote one.
    """
    if not TRIGGER_CASES.exists():
        return {}
    data = json.loads(TRIGGER_CASES.read_text(encoding="utf-8"))
    pos: dict[str, int] = {}
    coll: dict[str, int] = {}
    pos_all: dict[str, int] = {}
    coll_all: dict[str, int] = {}
    seen_ids: set[str] = set()
    for c in data.get("cases", []):
        cid = c.get("id")
        if cid is not None:
            if cid in seen_ids:
                continue  # a duplicate case id must not inflate coverage counts
            seen_ids.add(cid)
        source = c.get("source", DEFAULT_CASE_SOURCE)
        if source not in CASE_SOURCES:
            raise ValueError(
                f"{cid}: source must be one of {CASE_SOURCES}, got {source!r}")
        independent = source in INDEPENDENT_CASE_SOURCES
        kind = c.get("kind")
        if kind == "positive":
            exp = c.get("expected")
            if exp:
                pos_all[exp] = pos_all.get(exp, 0) + 1
                if independent:
                    pos[exp] = pos.get(exp, 0) + 1
        elif kind == "collision":
            for name in {v for v in (c.get("expected"), c.get("impostor")) if v}:
                coll_all[name] = coll_all.get(name, 0) + 1
                if independent:
                    coll[name] = coll.get(name, 0) + 1
    out: dict[str, dict] = {}
    for name in set(pos_all) | set(coll_all):
        p, m = pos.get(name, 0), coll.get(name, 0)
        out[name] = {
            "positives": p,
            "collisions": m,
            "positives_total": pos_all.get(name, 0),
            "collisions_total": coll_all.get(name, 0),
            "sufficient": p >= COVERAGE_MIN_POSITIVES and m >= COVERAGE_MIN_COLLISIONS,
        }
    return out


# --- skill scoring ---------------------------------------------------------

def score_skill(d: Path, collisions: dict, coverage: dict) -> dict:
    text = (d / "SKILL.md").read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    name = fm.get("name", d.name)
    desc = fm.get("description", "")
    body_lines = body.count("\n") + 1
    signals: dict = {}

    # S2 structure compliance (A1-A14 subset)
    checks = {
        "A1_name_prefix": name.startswith("ywc-") and name == d.name,
        "A2_use_when": desc.startswith("(ywc) Use when"),
        "A3_anti_trigger": bool(re.search(r"Do not use (?:for|during|when|in)\b", desc)),
        "A4_multilingual": bool(HANGUL.search(desc) and JAPANESE.search(desc)),
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

    # S5 consistency & integrity. Only the required locale set (md/en/ja/ko) is
    # scored; es/zh are officially optional (they match neither validate.sh nor
    # the project locale policy) and their absence no longer deducts — the
    # missing-es/zh list stays as an informational signal only.
    missing_required = [loc for loc in REQUIRED_LOCALES if not (d / loc).exists()]
    missing_optional = [loc for loc in FULL_LOCALES
                        if loc not in REQUIRED_LOCALES and not (d / loc).exists()]
    dangling = _dangling_ref_links(d, body)
    bad_pointers = _unresolved_sibling_pointers(desc)
    s5 = 5
    if dangling:
        s5 -= 2
    if bad_pointers:
        s5 -= 1
    if missing_required:
        s5 = 0
    s5 = max(0, min(5, s5))
    signals["missing_optional_locales"] = missing_optional
    signals["dangling_ref_links"] = dangling
    signals["unresolved_anti_trigger_pointers"] = bad_pointers

    # S1 collision sub-signal (judge fills precision/recall)
    coll = collisions.get(name, [])
    signals["collision_pairs"] = coll

    # FR1b coverage — signals-only; S1 stays null in axes (Amendment A2)
    signals["coverage"] = coverage.get(
        name, {"positives": 0, "collisions": 0, "positives_total": 0,
               "collisions_total": 0, "sufficient": False})

    # Prose lint — informational only, never feeds any axis or the CI baseline.
    signals["prose_lint"] = _prose_lint(body, _body_line_offset(text, body))

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


def _prose_lint(text: str, line_offset: int = 0) -> dict:
    """Flag no-op exhortations and non-directive phrasing in a body.

    Informational only — never feeds an axis or the CI baseline, exactly like
    signals["coverage"]. A "no-op" is an instruction that costs Tier-1 tokens on
    every invocation without changing what the agent does ("write clean code");
    "non-directive" is advisory phrasing where a skill body should command
    ("X is recommended" instead of "use X when Y").

    Lines that *quote* guidance rather than instruct are skipped: fenced code,
    table rows, block quotes, headings, and link-only lines. The table exclusion
    is load-bearing — the Rationalization Defense table quotes excuses verbatim,
    so no-op phrases legitimately appear there. A line carrying a concrete anchor
    (backtick identifier, path, digit, tool name) is treated as actionable.

    Line numbers are file-based (add `line_offset` for the frontmatter) because
    the prioritized backlog requires a `file:line` citation.
    """
    findings: dict = {"noop_lines": [], "nondirective_lines": []}
    in_fence = False
    for index, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not line or in_fence or line.startswith(("#", ">", "|")):
            continue
        if re.fullmatch(r"[-*]?\s*\[[^]]+\]\([^)]*\)", line):
            continue
        if CONCRETE_ANCHOR_RE.search(line):
            continue
        for bucket, phrases in (("noop_lines", NOOP_PHRASES),
                                ("nondirective_lines", NONDIRECTIVE_PHRASES)):
            for pat in phrases:
                if re.search(pat, line, re.IGNORECASE):
                    findings[bucket].append(
                        {"line": line_offset + index, "text": line, "phrase": pat})
                    break
    return findings


def _body_line_offset(text: str, body: str) -> int:
    """Lines consumed by the frontmatter, so prose-lint numbers are file-based."""
    return text[:len(text) - len(body)].count("\n")


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
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
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
    # ...and stripping the trigger list is not enough on its own. An implementer can
    # mention reviewing INSIDE its own role statement — ywc-cloud-engineer authors
    # Terraform "including ... a reliability-lens review of the change" — and was
    # scored A3=3 as a read-only agent holding Write/Edit/Bash. The role is declared
    # by its opening clause, so an implementer verb there vetoes the classification.
    role_head = re.split(r"—|--", role_text)[0]
    readonly_role = bool(
        (READONLY_HINT.search(name) or READONLY_HINT.search(role_text))
        and not IMPL_ROLE_HINT.search(role_head)
    )
    signals: dict = {}

    # A3 tool minimality (band logic in a3_tool_band — implementer agents that
    # legitimately mutate are minimal-for-role, not over-granted)
    tools = set(re.findall(r"[A-Z]\w+", tools_raw))
    mutating = tools & MUTATING_TOOLS
    a3 = a3_tool_band(tools_raw, readonly_role)
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
        name, {"positives": 0, "collisions": 0, "positives_total": 0,
               "collisions_total": 0, "sufficient": False})

    # Prose lint — informational only, never feeds any axis or the CI baseline.
    signals["prose_lint"] = _prose_lint(body, _body_line_offset(text, body))

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


# --------------------------------------------------------------------------
# History record rules (judgment tier)
#
# These functions shape `history.json` only. They deliberately touch nothing in
# the axes computation above: `axes.S3` stays `None`, `flatten_mech()` keeps
# storing only non-null axes, and so `--ci` stays a pure function of the
# mechanical tier. Putting a runner-derived S3 into `axes` would make the CI
# gate depend on LLM nondeterminism, which AC7 forbids.
# --------------------------------------------------------------------------

UNMEASURED = "unmeasured"

# Trials adopted for a reliability measurement (spec AC10: 6 paired trials).
DEFAULT_TRIALS = 6

# reliability -> S3 band, as (minimum ratio, score), highest first.
S3_RELIABILITY_BANDS: tuple[tuple[float, int], ...] = (
    (1.00, 5),
    (0.90, 4),
    (0.75, 3),
    (0.50, 2),
    (0.25, 1),
    (0.00, 0),
)

# An item's S3 came from one of two places, and they are not interchangeable:
# a 4 from observed runs and a 4 from reading the body are different claims.
S3_SOURCES = ("runner", "read-only")


def reliability_band(passes: int, trials: int) -> int | str:
    """Map `passes / trials` onto an S3 band.

    Returns `"unmeasured"` for zero trials rather than inventing a 0 — no
    evidence is not the same finding as evidence of failure.
    """
    if trials <= 0:
        return UNMEASURED
    ratio = passes / trials
    for minimum, score in S3_RELIABILITY_BANDS:
        if ratio >= minimum:
            return score
    return 0


def unreachable_bands(trials: int = DEFAULT_TRIALS) -> list[int]:
    """Bands that `passes / trials` cannot produce at this trial count (AC9).

    Reliability is discrete, so some bands simply have no attainable ratio.
    At the adopted 6 trials, band 4 is one of them: 5/6 = 0.833 lands in band
    3 and 6/6 = 1.0 lands in band 5, with nothing in between. Callers surface
    this instead of letting a reader assume every band is achievable.
    """
    all_bands = {score for _, score in S3_RELIABILITY_BANDS}
    if trials <= 0:
        return sorted(all_bands)
    attainable = {reliability_band(p, trials) for p in range(trials + 1)}
    return sorted(all_bands - attainable)


def is_measured(axes: dict) -> bool:
    """True when every axis of an item carries a number.

    `None` (this run skipped the judgment tier) and `"unmeasured"` (no fixture
    exists to measure with) both disqualify an item from having a total.
    """
    return all(isinstance(v, (int, float)) and not isinstance(v, bool)
               for v in axes.values())


def item_total(axes: dict, weights: dict) -> int | None:
    """Weighted `/100` total, or `None` when any axis is unmeasured.

    A total computed over 80 available weight is a score out of 80 wearing a
    `/100` label. Emitting `null` is the honest alternative — the reader is
    told the number does not exist rather than handed a quiet understatement.
    """
    if not is_measured(axes):
        return None
    return round(sum(axes[a] / 5 * w for a, w in weights.items() if a in axes))


def unmeasured_axes(axes: dict) -> list[str]:
    """Names of the axes blocking a total, in rubric order."""
    return [a for a, v in axes.items()
            if not (isinstance(v, (int, float)) and not isinstance(v, bool))]


def build_history_row(scored: dict, weights: dict,
                      below_threshold_at: int = 70) -> dict:
    """Build one root's `history.json` entry from judged items.

    `scored` maps item name -> {"axes": {...}, "s3_source": "runner"|"read-only"}.
    Unmeasured items are recorded as `null` and excluded from `mean_total` and
    `below_threshold`, so neither statistic silently absorbs a missing axis.
    """
    items: dict[str, int | None] = {}
    unmeasured: list[str] = []
    s3_source: dict[str, str] = {}

    for name, entry in scored.items():
        axes = entry.get("axes", {})
        total = item_total(axes, weights)
        items[name] = total
        if total is None:
            unmeasured.append(name)
        source = entry.get("s3_source")
        if source is not None:
            if source not in S3_SOURCES:
                raise ValueError(
                    f"{name}: s3_source must be one of {S3_SOURCES}, got {source!r}")
            s3_source[name] = source

    measured_totals = [t for t in items.values() if t is not None]
    return {
        "count": len(items),
        "measured": len(measured_totals),
        "unmeasured": sorted(unmeasured),
        "mean_total": (round(sum(measured_totals) / len(measured_totals), 1)
                       if measured_totals else None),
        "below_threshold": sum(1 for t in measured_totals if t < below_threshold_at),
        "items": items,
        "s3_source": s3_source,
    }


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
          f">= {COVERAGE_MIN_COLLISIONS} collisions per item, counting only "
          f"independently-sourced cases: {', '.join(INDEPENDENT_CASE_SOURCES)})",
          file=sys.stderr)

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
