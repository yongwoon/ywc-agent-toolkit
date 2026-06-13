# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.19.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.18.0...v1.19.0) (2026-06-13)


### ### Added

* **skills:** review quality — ywc-review-learnings + CodeRabbit methodology + DB schema SoT ([#74](https://github.com/yongwoon/ywc-agent-toolkit/issues/74)) ([3e7a2b7](https://github.com/yongwoon/ywc-agent-toolkit/commit/3e7a2b7883fffb588ea7f70705836fb410ab2d4c))


### ### Documentation

* **readme:** improve navigation with quick-start, goal table, skill links, and pipeline diagram ([#72](https://github.com/yongwoon/ywc-agent-toolkit/issues/72)) ([3fdea6f](https://github.com/yongwoon/ywc-agent-toolkit/commit/3fdea6f0881b551473dc39a04430e39eff4700a3))

## [1.18.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.17.0...v1.18.0) (2026-06-12)


### ### Added

* add Codex plugin distribution support ([#67](https://github.com/yongwoon/ywc-agent-toolkit/issues/67)) ([de823a3](https://github.com/yongwoon/ywc-agent-toolkit/commit/de823a3c6094d7f3682be36a1175347a429dd2af))
* add deterministic scripts replacing LLM-prose steps across skills ([#63](https://github.com/yongwoon/ywc-agent-toolkit/issues/63)) ([b3f6572](https://github.com/yongwoon/ywc-agent-toolkit/commit/b3f6572b81e2bd8402466bcf50c59df23efa37f5))
* add deterministic skill helper scripts ([#66](https://github.com/yongwoon/ywc-agent-toolkit/issues/66)) ([63c4ae5](https://github.com/yongwoon/ywc-agent-toolkit/commit/63c4ae5df4d028808c817a86216665dc3da91bb3))
* add internal Codex toolkit eval skill ([#68](https://github.com/yongwoon/ywc-agent-toolkit/issues/68)) ([64ec48e](https://github.com/yongwoon/ywc-agent-toolkit/commit/64ec48e815673ed6f1b3877ebb432e330d003ddb))
* add ywc-toolkit-eval harness; repair refs and tighten skill/agent specs ([#60](https://github.com/yongwoon/ywc-agent-toolkit/issues/60)) ([aaf0dd6](https://github.com/yongwoon/ywc-agent-toolkit/commit/aaf0dd6eebd5308348ea16e7a1b60d25efc60f07))


### ### Fixed

* **codex:** improve toolkit eval quality ([#69](https://github.com/yongwoon/ywc-agent-toolkit/issues/69)) ([dad0081](https://github.com/yongwoon/ywc-agent-toolkit/commit/dad0081bfb702a58eca5485a821aa9542d2fd6b6))
* **skills:** improve activation accuracy for confidence-gate, receive-review, project-docs ([#71](https://github.com/yongwoon/ywc-agent-toolkit/issues/71)) ([bcc4098](https://github.com/yongwoon/ywc-agent-toolkit/commit/bcc40984f412077df15b270d91f6cd6419c1beb4))

## [1.17.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.16.0...v1.17.0) (2026-06-11)


### ### Added

* **ywc-parallel-executor:** convert --per-task-pr to full PR-merge lifecycle ([#59](https://github.com/yongwoon/ywc-agent-toolkit/issues/59)) ([26eb6fa](https://github.com/yongwoon/ywc-agent-toolkit/commit/26eb6fa543ed372fcb7959a3724a2c29b59b38b2))


### ### Fixed

* **codex:** use Codex handoff commands in ywc-plan ([#57](https://github.com/yongwoon/ywc-agent-toolkit/issues/57)) ([14b1049](https://github.com/yongwoon/ywc-agent-toolkit/commit/14b1049c102e2970bd89dbe6e5a5796f68c6e6e6))

## [1.16.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.15.1...v1.16.0) (2026-06-11)


### ### Added

* add recurring defect review guidance to ywc skills ([#55](https://github.com/yongwoon/ywc-agent-toolkit/issues/55)) ([f0425ac](https://github.com/yongwoon/ywc-agent-toolkit/commit/f0425ac4ec300804e0af0b3ee8f220b3097ffd70))

## [1.15.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.15.0...v1.15.1) (2026-06-10)


### ### Documentation

* **codex:** improve skill metadata and development pipeline docs ([#53](https://github.com/yongwoon/ywc-agent-toolkit/issues/53)) ([631e794](https://github.com/yongwoon/ywc-agent-toolkit/commit/631e7944d98362a52b6b8952e9b41e8b12ff5d84))
* document release-please PR title requirement ([c858959](https://github.com/yongwoon/ywc-agent-toolkit/commit/c858959afca5ca02e50bb2f4b68e3b8d19cbea19))
* rewrite recommended development pipeline from real usage patterns ([#51](https://github.com/yongwoon/ywc-agent-toolkit/issues/51)) ([b79da80](https://github.com/yongwoon/ywc-agent-toolkit/commit/b79da80b297d1a27339f14d8285ac9dcd398bf88))

## [1.15.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.14.0...v1.15.0) (2026-06-09)


### ### Added

* **ywc-spec-validate:** Step 3.5 Precedent-Completeness Re-grounding (omission check) ([#49](https://github.com/yongwoon/ywc-agent-toolkit/issues/49)) ([79a707a](https://github.com/yongwoon/ywc-agent-toolkit/commit/79a707a941d20755f446e10d44771b671b9cd412))

## [1.14.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.13.0...v1.14.0) (2026-06-02)


### ### Added

* apply develop-with-llm PRs [#75](https://github.com/yongwoon/ywc-agent-toolkit/issues/75), [#76](https://github.com/yongwoon/ywc-agent-toolkit/issues/76), [#77](https://github.com/yongwoon/ywc-agent-toolkit/issues/77) ([#46](https://github.com/yongwoon/ywc-agent-toolkit/issues/46)) ([abd0985](https://github.com/yongwoon/ywc-agent-toolkit/commit/abd0985ad06afc0de7b1241f9b61fde8086f6dd5))


### ### Documentation

* **codex:** align skill guidance with Codex runtime ([#48](https://github.com/yongwoon/ywc-agent-toolkit/issues/48)) ([ee5093a](https://github.com/yongwoon/ywc-agent-toolkit/commit/ee5093acd861d8223797fdca6e1be0a08b6d5763))

## [1.13.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.12.1...v1.13.0) (2026-05-28)


### ### Added

* **ywc-spec-writer:** add task-range and PR-based update modes (v1.1.0) ([#43](https://github.com/yongwoon/ywc-agent-toolkit/issues/43)) ([2894746](https://github.com/yongwoon/ywc-agent-toolkit/commit/28947467d6803d427597d1a9aa446973faf25931))
* **ywc-spec-writer:** align with ywc-spec-validate rubric (v1.3.1) ([#45](https://github.com/yongwoon/ywc-agent-toolkit/issues/45)) ([ec7b467](https://github.com/yongwoon/ywc-agent-toolkit/commit/ec7b46766cc915a217b44d20dfd801f8e5b25cc3))

## [1.12.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.12.0...v1.12.1) (2026-05-27)


### ### Documentation

* sync documentation and improve skill/agent authoring rules ([#41](https://github.com/yongwoon/ywc-agent-toolkit/issues/41)) ([2169f75](https://github.com/yongwoon/ywc-agent-toolkit/commit/2169f750860fd57712553030117082ade629012f))

## [1.12.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.11.0...v1.12.0) (2026-05-27)


### ### Added

* **codex:** add 7 specialist agents and --codex-agents installer mode ([#36](https://github.com/yongwoon/ywc-agent-toolkit/issues/36)) ([f6a1daf](https://github.com/yongwoon/ywc-agent-toolkit/commit/f6a1daf8d8d21073790aa05e7bb264530861689e))
* **ywc-gen-testcase:** support task range input ([#37](https://github.com/yongwoon/ywc-agent-toolkit/issues/37)) ([da2fe0d](https://github.com/yongwoon/ywc-agent-toolkit/commit/da2fe0d4b59a048493de64a4ca298239169c197e))
* **ywc-merge-dependabot:** parallel-auto mode (ecosystem grouping) ([#38](https://github.com/yongwoon/ywc-agent-toolkit/issues/38)) ([dd1fe8d](https://github.com/yongwoon/ywc-agent-toolkit/commit/dd1fe8dc28890dc71bdc90dc6ce4a497dfe24d66))

## [1.11.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.10.0...v1.11.0) (2026-05-23)


### ### Added

* agent catalog (12 agents) + ywc-worktrees skill + advisor dispatch ([#34](https://github.com/yongwoon/ywc-agent-toolkit/issues/34)) ([1ab5545](https://github.com/yongwoon/ywc-agent-toolkit/commit/1ab5545fc3becff82cc54d889d0a4804cbf81537))

## [1.10.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.9.0...v1.10.0) (2026-05-22)


### ### Added

* add process-discipline skill suite (8 new skills + 6 existing skill updates) ([#32](https://github.com/yongwoon/ywc-agent-toolkit/issues/32)) ([8b34d0d](https://github.com/yongwoon/ywc-agent-toolkit/commit/8b34d0d3e0d129e0658fdcbeaac3a6ef20c45d77))

## [1.9.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.8.0...v1.9.0) (2026-05-21)


### ### Added

* add spec-to-html exporter and tighten ywc-plan spec planning rigor ([#30](https://github.com/yongwoon/ywc-agent-toolkit/issues/30)) ([8719f6f](https://github.com/yongwoon/ywc-agent-toolkit/commit/8719f6f3a80c8253d95f2ef4d8dd7dc1a4dc6c11))

## [1.8.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.7.0...v1.8.0) (2026-05-17)


### ### Added

* add HTML output mode to 8 review and report skills ([#28](https://github.com/yongwoon/ywc-agent-toolkit/issues/28)) ([c33e698](https://github.com/yongwoon/ywc-agent-toolkit/commit/c33e698f321abfd82834c1977cc5193a09d0284a))

## [1.7.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.6.0...v1.7.0) (2026-05-15)


### ### Added

* add ywc-agentic skill and mitigate fan-out ctx saturation ([#25](https://github.com/yongwoon/ywc-agent-toolkit/issues/25)) ([ca838cf](https://github.com/yongwoon/ywc-agent-toolkit/commit/ca838cf36ea72970f0318b3f3efc1daf87aa18b5))

## [1.6.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.5.1...v1.6.0) (2026-05-14)


### ### Added

* add marketplace.json for Claude Code plugin marketplace support ([6fa7b4b](https://github.com/yongwoon/ywc-agent-toolkit/commit/6fa7b4bcbc60825d6f19c1d1f4497275d29277ec))


### ### Documentation

* fix marketplace install commands and add to translated READMEs ([fc060b1](https://github.com/yongwoon/ywc-agent-toolkit/commit/fc060b1901388700ac73f6f14d6106904720f343))

## [1.5.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.5.0...v1.5.1) (2026-05-14)


### ### Documentation

* streamline repository documentation ([#22](https://github.com/yongwoon/ywc-agent-toolkit/issues/22)) ([8029d78](https://github.com/yongwoon/ywc-agent-toolkit/commit/8029d7823e03ef166621ef5460b66ade0ea601b7))

## [1.5.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.4.0...v1.5.0) (2026-05-14)


### ### Added

* add Codex shared skill support ([#20](https://github.com/yongwoon/ywc-agent-toolkit/issues/20)) ([7ce11e4](https://github.com/yongwoon/ywc-agent-toolkit/commit/7ce11e4c58d4a15f295148176d6104f6159994e7))

## [1.4.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.3.0...v1.4.0) (2026-05-14)


### ### Added

* **codex:** mirror claude skills ([#18](https://github.com/yongwoon/ywc-agent-toolkit/issues/18)) ([032dbc1](https://github.com/yongwoon/ywc-agent-toolkit/commit/032dbc1bf36d115a69170b3aeec13ce13af63553))

## [1.3.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.2.1...v1.3.0) (2026-05-14)


### ### Added

* **plugin:** add .claude-plugin/plugin.json for Claude Code marketplace ([#16](https://github.com/yongwoon/ywc-agent-toolkit/issues/16)) ([b7f8dd3](https://github.com/yongwoon/ywc-agent-toolkit/commit/b7f8dd39655d63527c14bb8c9992693849893096))

## [1.2.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.2.0...v1.2.1) (2026-05-14)


### ### Fixed

* **ywc-create-pr:** use AskUserQuestion for language selection prompt ([#14](https://github.com/yongwoon/ywc-agent-toolkit/issues/14)) ([7edd043](https://github.com/yongwoon/ywc-agent-toolkit/commit/7edd0439003724bb6641e348c019679c91421be7))

## [1.2.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.1.0...v1.2.0) (2026-05-13)


### ### Added

* **skills:** UL hook for ywc-commit, socratic mode for ywc-spec-validate, and flag propagation patterns ([#12](https://github.com/yongwoon/ywc-agent-toolkit/issues/12)) ([3e65dc7](https://github.com/yongwoon/ywc-agent-toolkit/commit/3e65dc7b601496cbad34647b514c8bc5ec161f90))

## [1.1.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.0.1...v1.1.0) (2026-05-13)


### ### Added

* add 7 hook scripts and hooks-registry.json to claude-code/hooks ([25981d7](https://github.com/yongwoon/ywc-agent-toolkit/commit/25981d7aed7b653e20a4f241a48058b0691344a2))
* add hook installer to install.sh with idempotent settings.json merge ([6216c3d](https://github.com/yongwoon/ywc-agent-toolkit/commit/6216c3d6b4f043339c4150c822a94e4a22aa6809))


### ### Fixed

* address CodeRabbit review - atomic tmp, env override, orphan settings cleanup, jq guard ([b346409](https://github.com/yongwoon/ywc-agent-toolkit/commit/b34640950230bdddf35d9d8f3a28b3cf2d920df7))
* allow git push at start of command in tag-only heuristic sed pattern ([ae29702](https://github.com/yongwoon/ywc-agent-toolkit/commit/ae29702d25bbb39953db82eff35a67c8e8a5d905))
* correct table separator spacing and code block blank line in hooks README ([19b5057](https://github.com/yongwoon/ywc-agent-toolkit/commit/19b50574f38b96b1644d1e63655552730fa409a2))
* extend curl-pipe-sh pattern to catch sudo and absolute path shell variants ([73dd7b4](https://github.com/yongwoon/ywc-agent-toolkit/commit/73dd7b49173a3acb3d78941e23ab946b6ff4fc03))
* extend rm-home/rm-home-var patterns to match trailing path and glob variants ([6f53783](https://github.com/yongwoon/ywc-agent-toolkit/commit/6f537837246b156aca5da2f710698258c4776657))
* remove allowlist check from bash command path to prevent bypass ([13792cf](https://github.com/yongwoon/ywc-agent-toolkit/commit/13792cfb0d778e843e84fe52b298136018d381c3))
* remove Write/Edit/MultiEdit from auto-allow and block shell metachar chaining ([714de62](https://github.com/yongwoon/ywc-agent-toolkit/commit/714de62c4c451b903d262d87e82d2b6e439502a3))
* suppress SC2016 for intentional jq --arg single-quoted filter ([61b5ecf](https://github.com/yongwoon/ywc-agent-toolkit/commit/61b5ecfeeda41f52749c5242f5ff1261813887a3))
* use lookaheads for order-independent force-push-to-main detection ([cb8d67b](https://github.com/yongwoon/ywc-agent-toolkit/commit/cb8d67b755d8ab91f59dd98f60c87e0c6cde4543))
* use word boundary for env-dump pattern to catch chained env calls ([7df6d06](https://github.com/yongwoon/ywc-agent-toolkit/commit/7df6d0693cc8faa5df001ae9de1d1013071b0744))
* validate webhook scheme (https-only) and use project basename for cwd in Slack payload ([366c40f](https://github.com/yongwoon/ywc-agent-toolkit/commit/366c40f9af567e0162e7208ceb1aad289a99e6ce))


### ### Changed

* fix .gitignore typo and ignore tasks/ and docs/ywc-plans ([fa28491](https://github.com/yongwoon/ywc-agent-toolkit/commit/fa284919edd477ac0d468ffd272798286a34e7d4))
* ignore ywc executor state files in .gitignore ([475ac1a](https://github.com/yongwoon/ywc-agent-toolkit/commit/475ac1ab7577e416e1a5044463078281b8b53987))
* mark 000001-010-infra-add-hook-source-assets as completed ([b039b3a](https://github.com/yongwoon/ywc-agent-toolkit/commit/b039b3a03633d7dda939b12a67224080bbd2451d))
* mark 000002-010-infra-implement-hook-installer as completed ([660ab86](https://github.com/yongwoon/ywc-agent-toolkit/commit/660ab864f4fd476e468ee9fd432407df68f7cc6a))
* mark 000003-010-infra-update-toolkit-readme as completed ([c75a8d6](https://github.com/yongwoon/ywc-agent-toolkit/commit/c75a8d6b7f868fec88e82cea29dcbefcfe1b5b68))
* retrigger release-please after label fix ([49725ba](https://github.com/yongwoon/ywc-agent-toolkit/commit/49725bad31f483f78ce3e3b4353897a0406664a2))
* trigger release-please for v1.1.0 ([cabd9e1](https://github.com/yongwoon/ywc-agent-toolkit/commit/cabd9e11b80c1484cafdfb1b01c19765546dab94))


### ### Documentation

* add Hook installation section to root README.md ([86d4dce](https://github.com/yongwoon/ywc-agent-toolkit/commit/86d4dce4fd33173101580aed2d071becade3109f))

## [1.0.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.0.0...v1.0.1) (2026-05-13)


### ### Fixed

* address CodeRabbit review — permissions completeness and deduplication ([714972c](https://github.com/yongwoon/ywc-agent-toolkit/commit/714972c1d1b829bbab45e68c5bbfd36e123ff768))
* pin release-please-action to full commit SHA for supply-chain security ([10f57b7](https://github.com/yongwoon/ywc-agent-toolkit/commit/10f57b73cb9bd8b7e03eaa9371bf94deaa65a0c9))
* use GitHub App token to allow release-please tags to trigger release.yml ([a970c21](https://github.com/yongwoon/ywc-agent-toolkit/commit/a970c2119b17956197a990c3c71bf5de77cf6877))


### ### Changed

* add check-readme-freshness hook for skill directory changes ([f4d7341](https://github.com/yongwoon/ywc-agent-toolkit/commit/f4d7341317ad835bd4ac72af6bb208a61ccac815))
* add CodeRabbit configuration ([f27ccbf](https://github.com/yongwoon/ywc-agent-toolkit/commit/f27ccbfc89ca1ccf78d897ecc21ec15245a82ef1))
* add comprehensive permissions and model config to claude settings ([661eb74](https://github.com/yongwoon/ywc-agent-toolkit/commit/661eb74cfbff826b30601e74db6eabee690fbb3f))
* add comprehensive permissions and model config to claude settings ([7fc06fd](https://github.com/yongwoon/ywc-agent-toolkit/commit/7fc06fda29c7fe8e838f96dd95d8396fe8b6fd8d))
* add README freshness hook and fix codex skill count ([6df2c94](https://github.com/yongwoon/ywc-agent-toolkit/commit/6df2c94a36973a82ad5e84e2daddd094db7e1a74))
* retrigger release-please after app installation fix ([a4249f0](https://github.com/yongwoon/ywc-agent-toolkit/commit/a4249f090432983f4b250df59caadb454f709d25))
* retrigger release-please with correct app credentials ([ae3acd1](https://github.com/yongwoon/ywc-agent-toolkit/commit/ae3acd1793d62ee06e7e494e357a67c3ed6b78eb))
* retrigger release-please with correct app id ([7e64450](https://github.com/yongwoon/ywc-agent-toolkit/commit/7e64450e55c4e28f72f96adcc6c07e7435a12f8f))
* trigger release-please workflow ([e5454f8](https://github.com/yongwoon/ywc-agent-toolkit/commit/e5454f829388302ef64fd297a3938baf59bea514))


### ### Documentation

* fix codex skill count and update install example ([cc1fe4b](https://github.com/yongwoon/ywc-agent-toolkit/commit/cc1fe4b1503067f2ee02f97842dcbc087126375f))

## [1.0.0] - 2026-05-13

### Added
- 26 `ywc-*` Claude Code skills under `claude-code/skills/` covering planning, spec writing, code generation, review, testing, CI, release, and incident management
- 1 Codex skill (`ywc-ui-ux-review`) under `codex/skills/` with full reference assets
- Unified installer `scripts/install.sh` with `--cc`, `--codex`, `--all`, and `--list` flags
- Local validation script `scripts/validate.sh` mirroring CI checks
- Multilingual README support (en / ja / ko / es / zh) for all skills via tiered translation system
- `translations.json` configuration for language tier management (manual: en/ja/ko, AI-generated: es/zh)
- CI workflows: skill validation, markdownlint, translation-check, and automated GitHub Release on `v*` tags
- `claude-code/hooks/` and `codex/hooks/` directories for future hook extensions

### Fixed
- Codex skill validation in CI now treats `codex/skills/` as a single bundle, not per-subdirectory (#1)
- Added missing frontmatter checks and local `validate.sh` to mirror CI (#1)
- Resolved ShellCheck SC2115 warning and markdownlint configuration in CI

### Removed
- Non-`ywc-*` reference files, prompts, and scripts from `codex/skills/` that were unrelated to any `ywc-*` skill (#2)
  - 20 orphaned reference files (e.g., `backend-generation.md`, `automated-pr-review-loop.md`)
  - `prompts/implementer-base.md` (non-ywc code generation prompt)
  - `scripts/` directory (9 PR automation scripts)
