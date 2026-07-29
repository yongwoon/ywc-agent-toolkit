# ywc-implement

Directly implement exactly one approved repository specification or ticket.

## Input

Accept one of `--spec <repo-relative-path>` or `--ticket <reference>`, never both. Approval evidence and acceptance criteria are required; otherwise return `NEEDS_CONTEXT`.

## Workflow

Capture a clean baseline and feature branch, inspect existing patterns, use TDD for behavior changes, run focused and full verification, then run `ywc-impl-review`. Create a conventional commit only after review passes. Do not create PRs or force-push.

Use `ywc-code-gen` for parallel multi-layer generation and `ywc-sequential-executor` for generated task directories.

## Report

Return changed files, verification commands and exit statuses, review status, commit SHA, and unresolved concerns.
