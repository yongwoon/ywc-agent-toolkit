#!/usr/bin/env python3
"""
build-pr-title.py <task-name> [--lang <lang>] [--format parts|title]

Deterministically extracts the task number and description slug from a task
directory name. Eliminates the need for the LLM to parse task-name regex rules
on every invocation — saves tokens on every PR-based task delivery.

Output modes:
  parts (default): prints TASK_NUMBER= and SLUG_EN= lines.
    The LLM constructs the final title as "[TASK_NUMBER] <translated SLUG_EN>"
    — only the short slug phrase needs translation, not the full task name format.

  title: prints the complete English PR title "[TASK_NUMBER] Slug Phrase".
    For English PRs no further LLM work is needed.

Supported task-name formats:
  New:    000001-010-db-create-users-table  → TASK_NUMBER=000001-010, SLUG_EN=Db Create Users Table
  Legacy: 001010-db-create-users-table     → TASK_NUMBER=001010,     SLUG_EN=Db Create Users Table

Exit codes:
  0  Parsed successfully
  1  Task name format not recognised (falls back to empty TASK_NUMBER)

Usage:
  # Default (parts mode) — LLM translates SLUG_EN to target language
  python claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py \\
    000001-010-db-create-users-table
  # TASK_NUMBER=000001-010
  # SLUG_EN=Db Create Users Table

  # Full English title (no LLM translation needed)
  python claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py \\
    000001-010-db-create-users-table --format title
  # [000001-010] Db Create Users Table
"""

import re
import sys
import argparse


def parse_task_name(task_name: str) -> tuple[str, str]:
    """Return (task_number, slug). Falls back to ('', task_name) if unrecognised."""
    # New format: 000001-010-<slug>
    m = re.match(r'^(\d{6}-\d{3})-(.+)$', task_name)
    if m:
        return m.group(1), m.group(2)
    # Legacy format: 001010-<slug>
    m = re.match(r'^(\d{6})-(.+)$', task_name)
    if m:
        return m.group(1), m.group(2)
    # Flexible N-M format: any digit counts for both segments (e.g., 1-010-slug, 000001-10-slug)
    m = re.match(r'^(\d+-\d+)-(.+)$', task_name)
    if m:
        print(f"INFO: using flexible N-M format for '{task_name}'", file=sys.stderr)
        return m.group(1), m.group(2)
    # Most permissive: single numeric prefix (e.g., 001-slug)
    m = re.match(r'^(\d+)-(.+)$', task_name)
    if m:
        print(f"INFO: using single-prefix format for '{task_name}'", file=sys.stderr)
        return m.group(1), m.group(2)
    return "", task_name


def slug_to_english(slug: str) -> str:
    """Convert hyphenated slug to title-cased English phrase."""
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build PR title components from a task directory name"
    )
    parser.add_argument(
        "task_name",
        help="Task directory name (e.g. 000001-010-db-create-users-table)"
    )
    parser.add_argument(
        "--format",
        choices=["parts", "title"],
        default="parts",
        help=(
            "parts (default): output TASK_NUMBER= and SLUG_EN= for LLM translation; "
            "title: output complete English title string"
        ),
    )
    args = parser.parse_args()

    task_number, slug = parse_task_name(args.task_name)
    slug_en = slug_to_english(slug)

    if not task_number:
        print(
            f"WARNING: Could not detect task-number prefix in '{args.task_name}'",
            file=sys.stderr,
        )
        print("TASK_NUMBER=")
        print(f"SLUG_EN={slug_en}")
        sys.exit(1)

    if args.format == "title":
        print(f"[{task_number}] {slug_en}")
    else:
        print(f"TASK_NUMBER={task_number}")
        print(f"SLUG_EN={slug_en}")


if __name__ == "__main__":
    main()
