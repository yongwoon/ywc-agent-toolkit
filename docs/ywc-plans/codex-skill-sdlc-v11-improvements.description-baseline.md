# Codex Skill Description Baseline

Generated from source Codex skills with:

```bash
bash scripts/check-codex-skill-descriptions.sh --report
```

- Scope: `codex/skills/ywc-*/SKILL.md`
- Limit: `500` Unicode characters after folded-description whitespace normalization
- Skills scanned: `46`
- Within limit: `13`
- Over limit: `33`
- Frontmatter errors: `0`

| Skill | Unicode chars | Status |
|---|---:|---|
| `ywc-agentic` | 564 | over-limit |
| `ywc-brainstorm` | 759 | over-limit |
| `ywc-changelog-release-notes` | 598 | over-limit |
| `ywc-code-gen` | 354 | ok |
| `ywc-commit` | 348 | ok |
| `ywc-confidence-gate` | 551 | over-limit |
| `ywc-create-pr` | 329 | ok |
| `ywc-debug-rootcause` | 745 | over-limit |
| `ywc-design-renew` | 1000 | over-limit |
| `ywc-docker-isolate` | 890 | over-limit |
| `ywc-e2e-test-strategy` | 624 | over-limit |
| `ywc-finish-branch` | 643 | over-limit |
| `ywc-gen-testcase` | 431 | ok |
| `ywc-handle-pr-reviews` | 665 | over-limit |
| `ywc-iac-author` | 797 | over-limit |
| `ywc-impl-review` | 643 | over-limit |
| `ywc-incident-postmortem` | 676 | over-limit |
| `ywc-infra-design` | 839 | over-limit |
| `ywc-infra-optimize` | 670 | over-limit |
| `ywc-infra-review` | 797 | over-limit |
| `ywc-merge-dependabot` | 376 | ok |
| `ywc-onboard-repo` | 579 | over-limit |
| `ywc-parallel-executor` | 449 | ok |
| `ywc-plan` | 623 | over-limit |
| `ywc-product-review` | 398 | ok |
| `ywc-project-docs` | 827 | over-limit |
| `ywc-project-scaffold` | 640 | over-limit |
| `ywc-receive-review` | 882 | over-limit |
| `ywc-refactor-clean` | 761 | over-limit |
| `ywc-release-pr-list` | 474 | ok |
| `ywc-review-learnings` | 855 | over-limit |
| `ywc-security-audit` | 455 | ok |
| `ywc-sequential-executor` | 513 | over-limit |
| `ywc-setup` | 285 | ok |
| `ywc-skill-author` | 505 | over-limit |
| `ywc-spec-ready` | 521 | over-limit |
| `ywc-spec-validate` | 485 | ok |
| `ywc-spec-writer` | 748 | over-limit |
| `ywc-task-generator` | 418 | ok |
| `ywc-tdd-ritual` | 756 | over-limit |
| `ywc-team-assemble` | 488 | ok |
| `ywc-tech-research` | 544 | over-limit |
| `ywc-ubiquitous-language` | 532 | over-limit |
| `ywc-ui-ux-review` | 569 | over-limit |
| `ywc-verify-done` | 690 | over-limit |
| `ywc-worktrees` | 987 | over-limit |

## Re-run

```bash
bash scripts/check-codex-skill-descriptions.sh --report
```
