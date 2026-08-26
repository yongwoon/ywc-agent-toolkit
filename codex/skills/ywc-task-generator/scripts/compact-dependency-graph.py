#!/usr/bin/env python3
"""Compact fully-completed sections of tasks/dependency-graph.md.

Heading-based, no markers required — this also retrofits files written
before this script existed. `tasks/dependency-graph.md` is split on every
top-level `## ` heading:

- `## Phase NNNNNN — ...`: if every task id *owned by this phase* (its
  bullets' own id, i.e. matching the heading's own `NNNNNN` prefix — a
  bullet may also reference another phase's id as a dependency, which is
  deliberately excluded from this phase's own completeness check) exists
  under `<tasks-dir>/completed/`, the section collapses to a single
  `## Phase NNNNNN — done` line plus one `- Completed: ...` bullet.
  Already-compacted phases (heading already ends in "— done") are left
  alone.
- `## Parallel Execution Notes ...` / `## Visual Dependency Graph ...`:
  if every task id mentioned inside — full form (`NNNNNN-NNN-slug`) or
  short form (bare `NNNNNN-NNN`, common in prose and Mermaid node labels)
  — resolves to a completed task, the whole section (heading + Mermaid
  diagram + prose) is dropped. Short ids resolve against the actual
  `<tasks-dir>/completed/` (and `<tasks-dir>/`) directory listing first,
  falling back to full-form ids found elsewhere in the document; an id
  that resolves neither way makes the section undecidable, so it is left
  untouched rather than guessed at.
- Any other section (title preamble, `## Open Questions ...`, a section
  with no recognizable task id) is left untouched.

A section referencing even one incomplete or unresolvable task id is left
exactly as-is — this never removes information about outstanding work.

Usage: compact-dependency-graph.py <tasks-dir>
Exit 0 always (no-op is not an error); prints how many sections were
compacted or dropped, and the resulting line-count delta.
"""
from __future__ import annotations  # `list[str] | None` annotations on py3.9
import os
import re
import sys
import tempfile
from pathlib import Path

SECTION_SPLIT_RE = re.compile(r"(?m)^(?=## )")
# Explicit lookarounds prevent a prefixed ID from being partially matched as
# its numeric suffix; a word boundary is not sufficient next to hyphens.
PHASE_HEADING_RE = re.compile(r"^##\s*Phase\s+((?:[a-z0-9]{2,4}-)?\d{6})\b(.*)$")
DROPPABLE_HEADING_RE = re.compile(r"^##\s*(Parallel Execution Notes|Visual Dependency Graph)\b")
FULL_ID_RE = re.compile(
    r"(?<![A-Za-z0-9-])((?:[a-z0-9]{2,4}-)?\d{6}-\d{3}-[A-Za-z0-9][A-Za-z0-9-]*)(?![A-Za-z0-9-])"
)
SHORT_ID_RE = re.compile(
    r"(?<![A-Za-z0-9-])((?:[a-z0-9]{2,4}-)?\d{6}-\d{3})(?![A-Za-z0-9-])"
)


def _short_id(full_id: str) -> str:
    """Return the phase/sequence portion, retaining an initials namespace."""
    parts = full_id.split("-")
    if len(parts) >= 4 and not parts[0].isdigit():
        return "-".join(parts[:3])
    return "-".join(parts[:2])


def _build_short_to_full(content: str, tasks_dir: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for base in (tasks_dir, tasks_dir / "completed"):
        if not base.is_dir():
            continue
        for entry in base.iterdir():
            if entry.is_dir() and FULL_ID_RE.fullmatch(entry.name):
                mapping.setdefault(_short_id(entry.name), entry.name)
    for full_id in FULL_ID_RE.findall(content):
        mapping.setdefault(_short_id(full_id), full_id)
    return mapping


def _resolve_ids(section_text: str, short_to_full: dict[str, str]) -> list[str] | None:
    shorts = sorted(set(SHORT_ID_RE.findall(section_text)))
    if not shorts:
        return None
    fulls = []
    for short_id in shorts:
        full_id = short_to_full.get(short_id)
        if full_id is None:
            return None
        fulls.append(full_id)
    return sorted(set(fulls))


def _all_completed(ids: list[str] | None, completed_dir: Path) -> bool:
    return bool(ids) and all((completed_dir / task_id).is_dir() for task_id in ids)


def compact(content: str, tasks_dir: Path) -> tuple[str, int, int]:
    completed_dir = tasks_dir / "completed"
    short_to_full = _build_short_to_full(content, tasks_dir)
    blocks = SECTION_SPLIT_RE.split(content)
    kept = [blocks[0]]
    compacted_phases = 0
    dropped_sections = 0

    for block in blocks[1:]:
        heading_line = block.split("\n", 1)[0]
        phase_match = PHASE_HEADING_RE.match(heading_line)
        if phase_match:
            phase_key, rest = phase_match.groups()
            if rest.strip().lower() == "— done":
                kept.append(block)
                continue
            owned_ids = sorted({i for i in FULL_ID_RE.findall(block) if i.startswith(f"{phase_key}-")})
            if _all_completed(owned_ids, completed_dir):
                id_list = ", ".join(f"`{i}`" for i in owned_ids)
                kept.append(f"## Phase {phase_key} — done\n- Completed: {id_list}\n\n")
                compacted_phases += 1
            else:
                kept.append(block)
            continue

        if DROPPABLE_HEADING_RE.match(heading_line):
            ids = _resolve_ids(block, short_to_full)
            if _all_completed(ids, completed_dir):
                dropped_sections += 1
                continue
        kept.append(block)

    return "".join(kept), compacted_phases, dropped_sections


def _atomic_write(path: Path, text: str) -> None:
    """Write via a same-directory temp file + os.replace so a crash mid-write
    can never leave the execution-order graph truncated."""
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as tmp:
        tmp.write(text)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: compact-dependency-graph.py <tasks-dir>", file=sys.stderr)
        return 2
    tasks_dir = Path(sys.argv[1])
    graph_path = tasks_dir / "dependency-graph.md"
    if not graph_path.is_file():
        print(f"no dependency-graph.md at {graph_path}, nothing to do")
        return 0
    original = graph_path.read_text(encoding="utf-8")
    updated, compacted_phases, dropped_sections = compact(original, tasks_dir)
    if compacted_phases or dropped_sections:
        before_lines = original.count("\n")
        after_lines = updated.count("\n")
        _atomic_write(graph_path, updated)
        print(f"compacted {compacted_phases} phase(s), dropped {dropped_sections} notes/diagram section(s); {before_lines} -> {after_lines} lines")
    else:
        print("nothing to compact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
