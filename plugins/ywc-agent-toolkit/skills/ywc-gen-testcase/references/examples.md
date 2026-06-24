# ywc-gen-testcase Examples

## PR URL, default single file

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

## Force physical split

```text
/ywc-gen-testcase 250 --split --lang ja
```

## QA-only testsheet

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

## Force single file even at L tier

```text
/ywc-gen-testcase 250 --force-single
```

## Task-based with regression

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

## Task range

```text
/ywc-gen-testcase 000012-010..000019-010 --lang ja
```

Generates an inclusive testsheet from every ordered task directory between the two task prefixes. Positional task ranges are resolved before Git ranges; use `--range` to force Git range mode.

## Current diff with custom filename

```text
/ywc-gen-testcase --from-diff --filename smoke-before-release
```

## Range between two tags

```text
/ywc-gen-testcase v1.2..v1.3
```

Generates `range-v1.2-v1.3-<slug>.md`. Auto-suggest proposes PR mode if the range HEAD is in a PR.

## Pre-PR local range

```text
/ywc-gen-testcase HEAD~5..HEAD --lang ja
```

Use this when local commits are not yet pushed or PR'd and need a testsheet for review.

## Explicit `--range` flag

```text
/ywc-gen-testcase --range abc1234..def5678
```

## Dry run

```text
/ywc-gen-testcase 250 --dry-run
```
