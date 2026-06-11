# Codex Plugin Distribution

> Status: Draft
> Scale: Medium
> Created: 2026-06-11
> Author: Codex
> Spec Reference: N/A - standalone distribution feature

## Purpose

This repository already supports local Codex installation through `scripts/install.sh --codex`, but it does not expose the `obra/superpowers`-style Codex plugin surface used by Codex CLI and Codex App plugin installation. Add the Codex plugin metadata and validation needed so the repository can be packaged and reviewed as a Codex plugin without disrupting the existing bash or Claude Code install paths.

## Scope

- Add a `.codex-plugin/plugin.json` manifest for Codex CLI/App plugin distribution.
- Point the Codex plugin manifest at the existing `codex/skills/` skill bundle.
- Include Codex App display metadata under the manifest `interface` object, following the observed `obra/superpowers` pattern.
- Add or reuse a local plugin icon asset only if the manifest needs one for Codex App presentation.
- Update root installation documentation so Codex users can distinguish plugin-based install from bash install.
- Extend local validation so missing or structurally broken Codex plugin metadata fails `bash scripts/validate.sh`.

## Out of Scope

- Submitting the plugin to the official Codex marketplace is out of scope; this plan prepares repository metadata only.
- Changing skill bodies, `agents/openai.yaml`, or Codex agent TOML behavior is out of scope.
- Changing `scripts/install.sh` local copy behavior is out of scope unless validation proves plugin packaging requires it.
- Changing Claude Code marketplace behavior under `.claude-plugin/` is out of scope.
- Guaranteeing Codex marketplace approval is out of scope because marketplace review policy is external to this repository.

## Existing Constraints Touched

| Existing artifact | Behavior verified by reading the file | New code's interaction |
|---|---|---|
| `plugin.json:1` | Root manifest currently names `ywc-agent-toolkit` and points `skills` / `agents` at Claude Code paths. | Do not repurpose this file for Codex plugin distribution; add `.codex-plugin/plugin.json` instead. |
| `.claude-plugin/plugin.json:1` | Claude Code plugin manifest already exists and points `skills` at `./claude-code/skills/`. | Use it as a local naming and metadata reference, but do not change Claude Code plugin behavior. |
| `README.md:16` | Installation docs currently document the Claude Code plugin marketplace first. | Add a separate Codex CLI/App plugin install section so Codex users do not infer bash-only install. |
| `README.md:26` | Bash install remains the documented fallback for both Claude Code and Codex. | Preserve this section as the fallback path after plugin install instructions. |
| `scripts/validate.sh:55` | Codex validation currently checks each skill directory and `agents/openai.yaml`. | Extend validation with a Codex plugin manifest check without weakening existing skill checks. |
| `scripts/validate.sh:175` | Validation ends by running `bash scripts/install.sh --list`. | Keep this dry run and add plugin manifest validation before final success output. |
| `.github/workflows/validate.yml:10` | CI executes `bash scripts/validate.sh`; changes to that script automatically affect CI. | No workflow change is required if validation remains inside `scripts/validate.sh`. |
| `codex/skills/ywc-plan/agents/openai.yaml:1` | Codex skill UI metadata uses an `interface` root with display fields. | Do not confuse per-skill `agents/openai.yaml` metadata with repository-level `.codex-plugin/plugin.json` metadata. |

## Acceptance Criteria

- [ ] **AC1 - Codex plugin manifest exists**: When a reviewer opens `.codex-plugin/plugin.json`, the manifest declares `name`, `version`, `description`, `author`, `repository`, `license`, `keywords`, `skills`, and `interface`, observable as valid JSON parseable by `jq`.
- [ ] **AC2 - Manifest points at Codex skills**: When the manifest `skills` value is inspected, it resolves to the existing `codex/skills/` bundle, observable as a path that exists in this repository and contains `ywc-plan/SKILL.md`.
- [ ] **AC3 - Codex App display metadata is present**: When the manifest `interface` object is inspected, it includes display name, short description, long description, developer name, category, capabilities, default prompts, website URL, brand color, and optional icon/logo paths that resolve if present.
- [ ] **AC4 - Existing install paths are preserved**: When `bash scripts/install.sh --list` runs after the change, it still lists Claude Code and Codex skills/agents without requiring `.codex-plugin` to be installed locally.
- [ ] **AC5 - Validation catches manifest regressions**: When `.codex-plugin/plugin.json` is missing or invalid in a temporary negative check, `bash scripts/validate.sh` reports a Codex plugin metadata error; when restored, the script exits 0.
- [ ] **AC6 - Documentation covers Codex CLI/App install**: When a user reads `README.md`, the Installation section includes Codex CLI `/plugins` and Codex App Plugins sidebar guidance, with bash install still documented as the fallback.

## Functional Requirements

### FR-1: Add Codex plugin manifest

Create `.codex-plugin/plugin.json` using the same repository identity as `plugin.json` (`name`, `version`, author, repository, license, keywords) while changing the installation target to the Codex bundle. The `skills` field must point to `./codex/skills/` or another path that the actual Codex plugin loader can resolve from the plugin root.

### FR-2: Add Codex App interface metadata

Populate the manifest `interface` object for Codex App presentation. Follow the observed `obra/superpowers` shape: display name, short/long descriptions, developer name, category, capabilities, default prompts, website URL, brand color, optional icon/logo, and screenshots array. If icon/logo fields are included, the referenced files must exist under `.codex-plugin/`.

### FR-3: Preserve existing local installers

Do not alter the semantics of `scripts/install.sh --codex`, `--codex-agents`, `--cc`, or `--all`. Plugin packaging is an additional install surface, not a replacement for direct copy installs into `${CODEX_HOME}`.

### FR-4: Validate Codex plugin metadata

Extend `scripts/validate.sh` with a focused `check_codex_plugin_manifest` function. It must verify that `.codex-plugin/plugin.json` exists, is valid JSON, has required top-level fields, has an `interface` object with required display fields, and references paths that exist in the repository.

### FR-5: Document Codex plugin installation

Update `README.md` Installation with separate subsections for Codex CLI and Codex App plugin install, then keep the existing bash install section as the manual fallback. Keep wording conservative: "prepared for" or "install via plugin marketplace once available" unless the plugin is already accepted into a marketplace.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Compatibility | Existing Claude Code plugin metadata and bash install behavior must remain unchanged. |
| Maintainability | Manifest field values should duplicate root metadata only where needed; avoid introducing scripts or generators for one JSON file. |
| Portability | Validation additions must remain portable Bash and work in CI's Ubuntu shell environment. |
| User clarity | Documentation must not imply marketplace availability until the plugin is actually listed there. |

## Data Model

N/A - no data model change.

## API Contract

N/A - no API contract change.

## Edge Cases

- **Codex manifest path resolution**: If Codex expects paths relative to `.codex-plugin/`, a manifest value like `./codex/skills/` may not resolve. Implementation must verify loader expectations before finalizing the path; if uncertain, mirror or symlink-free copy the required plugin content under `.codex-plugin/skills/` and validate that choice.
- **No existing asset files**: This repository currently has no icon/image asset discovered under the top three levels. If the manifest includes `composerIcon` or `logo`, implementation must add a small committed asset under `.codex-plugin/assets/` or omit optional asset fields.
- **Invalid JSON tooling availability**: If `jq` is unavailable in a contributor environment, validation must either use a portable fallback or clearly require `jq`. Prefer `python3 -m json.tool` only if Python availability is already accepted by CI; otherwise keep checks shell-compatible where possible.
- **Marketplace status wording**: README must not say "available in the official Codex marketplace" until that is true. Use future-safe wording for repository preparation.
- **Version drift**: Manifest `version` should match root `VERSION` or `plugin.json` version at implementation time. If the repository has multiple version sources, document which one is authoritative rather than silently choosing a stale value.

## Dependencies

- Existing repository layout: `codex/skills/`, `codex/agents/`, `.claude-plugin/`, `scripts/validate.sh`, and `.github/workflows/validate.yml`.
- Public reference: `obra/superpowers` repository's `.codex-plugin/plugin.json` pattern.
- External submission/review to Codex marketplace is a post-implementation dependency, not part of this plan.

## Open Questions

- [ ] Does Codex plugin manifest `skills` resolve relative to `.codex-plugin/` or repository root? The implementation must verify this before deciding whether to point at `./codex/skills/` or mirror plugin-ready skills under `.codex-plugin/skills/`.
- [ ] Are icon/logo fields required for Codex App marketplace review, or optional? If required, add `.codex-plugin/assets/` with minimal brand assets.
- [ ] Should localized README files (`README.ko.md`, `README.ja.md`, `README.es.md`, `README.zh.md`) be updated in the same PR, or should translation regeneration run after the English README change?

## Implementation Tasks

1. Add `.codex-plugin/plugin.json` with repository metadata, Codex skill path, and Codex App `interface` metadata.
2. If required by the manifest, add `.codex-plugin/assets/` with small icon/logo assets and reference them from the manifest.
3. Add `check_codex_plugin_manifest` to `scripts/validate.sh`, called before the final install-script dry run.
4. Update `README.md` Installation with Codex CLI and Codex App plugin install guidance, keeping marketplace-status wording accurate.
5. Decide translation handling for localized README files; either update them in the same PR or explicitly run the repository translation workflow/tooling.
6. Run verification commands and fix any validation or markdown issues.

## Verification

```bash
bash scripts/validate.sh
bash scripts/install.sh --list
bash scripts/install.sh --codex ywc-plan
bash scripts/translate.sh --dry-run
```

Expected outcome: all commands exit 0. The targeted Codex install should continue copying `ywc-plan` into the configured Codex skills directory without relying on plugin metadata.

## Self-Consistency Pass

### Pass A - Cross-section consistency

- AC1 maps to FR-1 and verification via JSON parsing.
- AC2 maps to FR-1 and the path-resolution edge case.
- AC3 maps to FR-2 and the asset-required edge case.
- AC4 maps to FR-3 and `bash scripts/install.sh --list` / `--codex ywc-plan` verification.
- AC5 maps to FR-4 and `bash scripts/validate.sh` verification.
- AC6 maps to FR-5 and README update task.
- Data Model and API Contract are both `N/A`, and no AC depends on DB or HTTP behavior.

### Pass B - Claim-to-reality verification

- Existing root manifest behavior is cited at `plugin.json:1`.
- Existing Claude plugin behavior is cited at `.claude-plugin/plugin.json:1`.
- Existing README install guidance is cited at `README.md:16` and `README.md:26`.
- Existing Codex validation behavior is cited at `scripts/validate.sh:55` and `scripts/validate.sh:175`.
- Existing CI validation entry point is cited at `.github/workflows/validate.yml:10`.
- No closure claim is made without the repository search result that `.codex-plugin` is currently absent.

### Pass C - Schema invariants

- N/A - this plan introduces no database schema, migrations, relations, enums, indexes, or API delete behavior.

## References

- `README.md`
- `plugin.json`
- `.claude-plugin/plugin.json`
- `scripts/validate.sh`
- `.github/workflows/validate.yml`
- `https://github.com/obra/superpowers`
- `https://raw.githubusercontent.com/obra/superpowers/main/.codex-plugin/plugin.json`
