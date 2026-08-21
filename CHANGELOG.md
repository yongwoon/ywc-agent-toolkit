# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

### Added

* **ywc-architecture-invariants:** distribute the optional architecture contract validator and normalized-evidence audit skill.
* **ywc-create-pr:** cite related task or plan design background in generated PR bodies, with explicit `--plan-doc` and `--no-plan-ref` controls.
* **ywc-task-generator:** automatically compact completed phases and resolved execution notes in `tasks/dependency-graph.md`.

## [1.34.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.34.0...v1.34.1) (2026-08-21)


### Documentation

* trim READMEs to a landing page and link the guidebook ([#167](https://github.com/yongwoon/ywc-agent-toolkit/issues/167)) ([421b41e](https://github.com/yongwoon/ywc-agent-toolkit/commit/421b41e9a7b44dbb4aade9bcd4064b110f8877db))

## [1.34.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.33.0...v1.34.0) (2026-08-17)


### Added

* **ywc-create-pr:** cite related task/plan design background in PR bodies ([#165](https://github.com/yongwoon/ywc-agent-toolkit/issues/165)) ([110f10a](https://github.com/yongwoon/ywc-agent-toolkit/commit/110f10a417c589f0e9ac2211545501e0f864eeac))
* **ywc-task-generator:** auto-compact completed phases in dependency-graph.md ([#164](https://github.com/yongwoon/ywc-agent-toolkit/issues/164)) ([6ec3d36](https://github.com/yongwoon/ywc-agent-toolkit/commit/6ec3d366ab67e16354454e78e8c3699b5631f146))

## [1.33.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.32.0...v1.33.0) (2026-08-13)


### Added

* add 7 hook scripts and hooks-registry.json to claude-code/hooks ([25981d7](https://github.com/yongwoon/ywc-agent-toolkit/commit/25981d7aed7b653e20a4f241a48058b0691344a2))
* add architecture invariants, context safety, and agentic transition hardening ([#161](https://github.com/yongwoon/ywc-agent-toolkit/issues/161)) ([dbeda7d](https://github.com/yongwoon/ywc-agent-toolkit/commit/dbeda7d03c5f784ab021372f8d57349bb3845d0f))
* add Codex plugin distribution support ([#67](https://github.com/yongwoon/ywc-agent-toolkit/issues/67)) ([de823a3](https://github.com/yongwoon/ywc-agent-toolkit/commit/de823a3c6094d7f3682be36a1175347a429dd2af))
* add Codex shared skill support ([#20](https://github.com/yongwoon/ywc-agent-toolkit/issues/20)) ([7ce11e4](https://github.com/yongwoon/ywc-agent-toolkit/commit/7ce11e4c58d4a15f295148176d6104f6159994e7))
* add deterministic scripts replacing LLM-prose steps across skills ([#63](https://github.com/yongwoon/ywc-agent-toolkit/issues/63)) ([b3f6572](https://github.com/yongwoon/ywc-agent-toolkit/commit/b3f6572b81e2bd8402466bcf50c59df23efa37f5))
* add deterministic skill helper scripts ([#66](https://github.com/yongwoon/ywc-agent-toolkit/issues/66)) ([63c4ae5](https://github.com/yongwoon/ywc-agent-toolkit/commit/63c4ae5df4d028808c817a86216665dc3da91bb3))
* add hook installer to install.sh with idempotent settings.json merge ([6216c3d](https://github.com/yongwoon/ywc-agent-toolkit/commit/6216c3d6b4f043339c4150c822a94e4a22aa6809))
* add HTML output mode to 8 review and report skills ([#28](https://github.com/yongwoon/ywc-agent-toolkit/issues/28)) ([c33e698](https://github.com/yongwoon/ywc-agent-toolkit/commit/c33e698f321abfd82834c1977cc5193a09d0284a))
* add infrastructure design/review/optimize skill suite ([#131](https://github.com/yongwoon/ywc-agent-toolkit/issues/131)) ([43194ac](https://github.com/yongwoon/ywc-agent-toolkit/commit/43194ac3a7c6ff72667adb125685fbe97a0a7bba))
* add internal Codex toolkit eval skill ([#68](https://github.com/yongwoon/ywc-agent-toolkit/issues/68)) ([64ec48e](https://github.com/yongwoon/ywc-agent-toolkit/commit/64ec48e815673ed6f1b3877ebb432e330d003ddb))
* add isolated evaluation runners for Claude Code and Codex skills ([#151](https://github.com/yongwoon/ywc-agent-toolkit/issues/151)) ([0e8cee7](https://github.com/yongwoon/ywc-agent-toolkit/commit/0e8cee7210700922a3ac8f1f6754c07b9b8e7d57))
* add language setup skills ([#125](https://github.com/yongwoon/ywc-agent-toolkit/issues/125)) ([995d69d](https://github.com/yongwoon/ywc-agent-toolkit/commit/995d69dd957531904d60a4dc4607a93839315e84))
* add marketplace.json for Claude Code plugin marketplace support ([6fa7b4b](https://github.com/yongwoon/ywc-agent-toolkit/commit/6fa7b4bcbc60825d6f19c1d1f4497275d29277ec))
* add process-discipline skill suite (8 new skills + 6 existing skill updates) ([#32](https://github.com/yongwoon/ywc-agent-toolkit/issues/32)) ([8b34d0d](https://github.com/yongwoon/ywc-agent-toolkit/commit/8b34d0d3e0d129e0658fdcbeaac3a6ef20c45d77))
* add recurring defect review guidance to ywc skills ([#55](https://github.com/yongwoon/ywc-agent-toolkit/issues/55)) ([f0425ac](https://github.com/yongwoon/ywc-agent-toolkit/commit/f0425ac4ec300804e0af0b3ee8f220b3097ffd70))
* add review learnings, design renew, and schema guide ([#80](https://github.com/yongwoon/ywc-agent-toolkit/issues/80)) ([eedc4d5](https://github.com/yongwoon/ywc-agent-toolkit/commit/eedc4d558f1f07642a9ed1dd67dfdc0b4e4dc1e8))
* add spec-to-html exporter and tighten ywc-plan spec planning rigor ([#30](https://github.com/yongwoon/ywc-agent-toolkit/issues/30)) ([8719f6f](https://github.com/yongwoon/ywc-agent-toolkit/commit/8719f6f3a80c8253d95f2ef4d8dd7dc1a4dc6c11))
* add ywc-adr, ywc-implement skills and Codex SDLC v1.1 gap closure ([#155](https://github.com/yongwoon/ywc-agent-toolkit/issues/155)) ([39b68a5](https://github.com/yongwoon/ywc-agent-toolkit/commit/39b68a59e1e4b5e7180efbc471c75a382e53c8e5))
* add ywc-agentic skill and mitigate fan-out ctx saturation ([#25](https://github.com/yongwoon/ywc-agent-toolkit/issues/25)) ([ca838cf](https://github.com/yongwoon/ywc-agent-toolkit/commit/ca838cf36ea72970f0318b3f3efc1daf87aa18b5))
* add ywc-auth-implement skill for Claude Code and Codex ([#144](https://github.com/yongwoon/ywc-agent-toolkit/issues/144)) ([da29d14](https://github.com/yongwoon/ywc-agent-toolkit/commit/da29d1436be97847ec0ade92b6c04a12976f5825))
* add ywc-toolkit-eval harness; repair refs and tighten skill/agent specs ([#60](https://github.com/yongwoon/ywc-agent-toolkit/issues/60)) ([aaf0dd6](https://github.com/yongwoon/ywc-agent-toolkit/commit/aaf0dd6eebd5308348ea16e7a1b60d25efc60f07))
* adopt GPT-5.6 Terra for Codex agents and clean up stale model references ([#146](https://github.com/yongwoon/ywc-agent-toolkit/issues/146)) ([915983a](https://github.com/yongwoon/ywc-agent-toolkit/commit/915983aafc904880ee14e68fc64b744ef257cb4b))
* agent catalog (12 agents) + ywc-worktrees skill + advisor dispatch ([#34](https://github.com/yongwoon/ywc-agent-toolkit/issues/34)) ([1ab5545](https://github.com/yongwoon/ywc-agent-toolkit/commit/1ab5545fc3becff82cc54d889d0a4804cbf81537))
* apply develop-with-llm PRs [#75](https://github.com/yongwoon/ywc-agent-toolkit/issues/75), [#76](https://github.com/yongwoon/ywc-agent-toolkit/issues/76), [#77](https://github.com/yongwoon/ywc-agent-toolkit/issues/77) ([#46](https://github.com/yongwoon/ywc-agent-toolkit/issues/46)) ([abd0985](https://github.com/yongwoon/ywc-agent-toolkit/commit/abd0985ad06afc0de7b1241f9b61fde8086f6dd5))
* apply Fable agent-engineering insights across Claude Code and Codex skills ([#133](https://github.com/yongwoon/ywc-agent-toolkit/issues/133)) ([6fce4b0](https://github.com/yongwoon/ywc-agent-toolkit/commit/6fce4b0a9c8c99a081154daba1e8ff1d5fddf94f))
* **code-gen:** add --review flag and force critical-path review ([#137](https://github.com/yongwoon/ywc-agent-toolkit/issues/137)) ([f64dba0](https://github.com/yongwoon/ywc-agent-toolkit/commit/f64dba0eb5928a942f66f2beaa93d74caa13a297))
* **codex:** add 7 specialist agents and --codex-agents installer mode ([#36](https://github.com/yongwoon/ywc-agent-toolkit/issues/36)) ([f6a1daf](https://github.com/yongwoon/ywc-agent-toolkit/commit/f6a1daf8d8d21073790aa05e7bb264530861689e))
* **codex:** mirror claude skills ([#18](https://github.com/yongwoon/ywc-agent-toolkit/issues/18)) ([032dbc1](https://github.com/yongwoon/ywc-agent-toolkit/commit/032dbc1bf36d115a69170b3aeec13ce13af63553))
* improve skill contracts and eval coverage ([#96](https://github.com/yongwoon/ywc-agent-toolkit/issues/96)) ([3121af2](https://github.com/yongwoon/ywc-agent-toolkit/commit/3121af2d859753b52ff0021798402485a804c1ed))
* initial release v1.0.0 ([89dc2cf](https://github.com/yongwoon/ywc-agent-toolkit/commit/89dc2cfdfa1891227082e31da3b5007381c67a56))
* **plugin:** add .claude-plugin/plugin.json for Claude Code marketplace ([#16](https://github.com/yongwoon/ywc-agent-toolkit/issues/16)) ([b7f8dd3](https://github.com/yongwoon/ywc-agent-toolkit/commit/b7f8dd39655d63527c14bb8c9992693849893096))
* SDLC v1.1 skill and Codex bundle improvements ([#140](https://github.com/yongwoon/ywc-agent-toolkit/issues/140)) ([3a2ea69](https://github.com/yongwoon/ywc-agent-toolkit/commit/3a2ea690e4ab15ab39ad6cdf4304d96f942320f8))
* **skill-author:** audit workflow, deletion-test pilot, and 80-word description cap enforcement ([#135](https://github.com/yongwoon/ywc-agent-toolkit/issues/135)) ([940b5d7](https://github.com/yongwoon/ywc-agent-toolkit/commit/940b5d7c53b91c9ec6ecb2844d0c67423c8a2a83))
* **skills:** add --aggregate-pr to claude-code & codex executors ([#85](https://github.com/yongwoon/ywc-agent-toolkit/issues/85)) ([95ab0e1](https://github.com/yongwoon/ywc-agent-toolkit/commit/95ab0e19aa2cd7b9cc77a7582a3d5cbc05de83c6))
* **skills:** add English/Chinese/Spanish support to ywc-project-docs ([#118](https://github.com/yongwoon/ywc-agent-toolkit/issues/118)) ([1ed4e52](https://github.com/yongwoon/ywc-agent-toolkit/commit/1ed4e5254b57ff5681f6ae52adbc915621a12fa8))
* **skills:** add PR conflict resolution and merge-readiness gate ([#82](https://github.com/yongwoon/ywc-agent-toolkit/issues/82)) ([f3a2384](https://github.com/yongwoon/ywc-agent-toolkit/commit/f3a23848a5f8b7549e16bb275348ffc1b640eaa5))
* **skills:** review quality — ywc-review-learnings + CodeRabbit methodology + DB schema SoT ([#74](https://github.com/yongwoon/ywc-agent-toolkit/issues/74)) ([3e7a2b7](https://github.com/yongwoon/ywc-agent-toolkit/commit/3e7a2b7883fffb588ea7f70705836fb410ab2d4c))
* **skills:** toolkit-eval harness fixes + catalog activation/boundary resolution ([#88](https://github.com/yongwoon/ywc-agent-toolkit/issues/88)) ([561943a](https://github.com/yongwoon/ywc-agent-toolkit/commit/561943acc978981037df6b21ec6b0f7ae0ac1dec))
* **skills:** UL hook for ywc-commit, socratic mode for ywc-spec-validate, and flag propagation patterns ([#12](https://github.com/yongwoon/ywc-agent-toolkit/issues/12)) ([3e65dc7](https://github.com/yongwoon/ywc-agent-toolkit/commit/3e65dc7b601496cbad34647b514c8bc5ec161f90))
* **skills:** worktree 실행 및 Codex 평가 계약 개선 ([#87](https://github.com/yongwoon/ywc-agent-toolkit/issues/87)) ([8383883](https://github.com/yongwoon/ywc-agent-toolkit/commit/8383883bdf353cc11b37ac0d3adb5b30e42e04a5))
* **toolkit-eval:** expand trigger-case coverage and tighten skill boundary rules ([#163](https://github.com/yongwoon/ywc-agent-toolkit/issues/163)) ([ec7860e](https://github.com/yongwoon/ywc-agent-toolkit/commit/ec7860e7676fa68865451aa62da54fd665c344f5))
* ywc 스킬 zh/es 언어 지원 추가 ([#120](https://github.com/yongwoon/ywc-agent-toolkit/issues/120)) ([e2e3cf5](https://github.com/yongwoon/ywc-agent-toolkit/commit/e2e3cf5e9b22c21fed72adb4e881979cc46a7e8e))
* **ywc-brainstorm:** add self-review pass and existing-code guidance ([#158](https://github.com/yongwoon/ywc-agent-toolkit/issues/158)) ([b3bb65d](https://github.com/yongwoon/ywc-agent-toolkit/commit/b3bb65d188f1daa581130649b78baa4cfb9f67d7))
* **ywc-gen-testcase:** support task range input ([#37](https://github.com/yongwoon/ywc-agent-toolkit/issues/37)) ([da2fe0d](https://github.com/yongwoon/ywc-agent-toolkit/commit/da2fe0d4b59a048493de64a4ca298239169c197e))
* **ywc-merge-dependabot:** parallel-auto mode (ecosystem grouping) ([#38](https://github.com/yongwoon/ywc-agent-toolkit/issues/38)) ([dd1fe8d](https://github.com/yongwoon/ywc-agent-toolkit/commit/dd1fe8dc28890dc71bdc90dc6ce4a497dfe24d66))
* **ywc-parallel-executor:** convert --per-task-pr to full PR-merge lifecycle ([#59](https://github.com/yongwoon/ywc-agent-toolkit/issues/59)) ([26eb6fa](https://github.com/yongwoon/ywc-agent-toolkit/commit/26eb6fa543ed372fcb7959a3724a2c29b59b38b2))
* **ywc-plan:** add Codebase-Fact Pre-check and Global Constraints/Interfaces sections ([#157](https://github.com/yongwoon/ywc-agent-toolkit/issues/157)) ([a0d885b](https://github.com/yongwoon/ywc-agent-toolkit/commit/a0d885b27c1ece3b483b66d3652487179f529f22))
* **ywc-security-engineer:** promote to Opus tier, remove Phase 2 escalation ([#159](https://github.com/yongwoon/ywc-agent-toolkit/issues/159)) ([7158da9](https://github.com/yongwoon/ywc-agent-toolkit/commit/7158da91cae4443e28ee8c3ee09453ce134dfb8d))
* **ywc-spec-validate:** Step 3.5 Precedent-Completeness Re-grounding (omission check) ([#49](https://github.com/yongwoon/ywc-agent-toolkit/issues/49)) ([79a707a](https://github.com/yongwoon/ywc-agent-toolkit/commit/79a707a941d20755f446e10d44771b671b9cd412))
* **ywc-spec-writer:** add task-range and PR-based update modes (v1.1.0) ([#43](https://github.com/yongwoon/ywc-agent-toolkit/issues/43)) ([2894746](https://github.com/yongwoon/ywc-agent-toolkit/commit/28947467d6803d427597d1a9aa446973faf25931))
* **ywc-spec-writer:** align with ywc-spec-validate rubric (v1.3.1) ([#45](https://github.com/yongwoon/ywc-agent-toolkit/issues/45)) ([ec7b467](https://github.com/yongwoon/ywc-agent-toolkit/commit/ec7b46766cc915a217b44d20dfd801f8e5b25cc3))


### Fixed

* add ywc-setup evals and resolve Phase 000043 toolkit-eval backlog ([#127](https://github.com/yongwoon/ywc-agent-toolkit/issues/127)) ([a6140e7](https://github.com/yongwoon/ywc-agent-toolkit/commit/a6140e7f7986d5f1ec0df1a560fa9642067e2b0c))
* address CodeRabbit review - atomic tmp, env override, orphan settings cleanup, jq guard ([b346409](https://github.com/yongwoon/ywc-agent-toolkit/commit/b34640950230bdddf35d9d8f3a28b3cf2d920df7))
* address CodeRabbit review — permissions completeness and deduplication ([714972c](https://github.com/yongwoon/ywc-agent-toolkit/commit/714972c1d1b829bbab45e68c5bbfd36e123ff768))
* **agents:** clarify performance-engineer &lt;-&gt; language-reviewer boundary ([#112](https://github.com/yongwoon/ywc-agent-toolkit/issues/112)) ([e5f737f](https://github.com/yongwoon/ywc-agent-toolkit/commit/e5f737f318740c5c4f5028c719f17d6e83fb0003))
* **agents:** resolve A1 body-level idiom/magnitude ownership overlap ([#113](https://github.com/yongwoon/ywc-agent-toolkit/issues/113)) ([7c3a251](https://github.com/yongwoon/ywc-agent-toolkit/commit/7c3a25144d76d885636ad046c8e331b710cf2cdc))
* allow git push at start of command in tag-only heuristic sed pattern ([ae29702](https://github.com/yongwoon/ywc-agent-toolkit/commit/ae29702d25bbb39953db82eff35a67c8e8a5d905))
* **codex:** improve toolkit eval quality ([#69](https://github.com/yongwoon/ywc-agent-toolkit/issues/69)) ([dad0081](https://github.com/yongwoon/ywc-agent-toolkit/commit/dad0081bfb702a58eca5485a821aa9542d2fd6b6))
* **codex:** PR health sweep 계약 정합화 및 plugin listing 준비 ([#106](https://github.com/yongwoon/ywc-agent-toolkit/issues/106)) ([ecab49c](https://github.com/yongwoon/ywc-agent-toolkit/commit/ecab49c00ff4aefbaf8ea9f3d4076409636e224a))
* **codex:** support marketplace package workflow ([#89](https://github.com/yongwoon/ywc-agent-toolkit/issues/89)) ([1b08f66](https://github.com/yongwoon/ywc-agent-toolkit/commit/1b08f66b8a386fe90e82e477e6c82fec6a9f7909))
* **codex:** use Codex handoff commands in ywc-plan ([#57](https://github.com/yongwoon/ywc-agent-toolkit/issues/57)) ([14b1049](https://github.com/yongwoon/ywc-agent-toolkit/commit/14b1049c102e2970bd89dbe6e5a5796f68c6e6e6))
* correct codex skill validation and add local validate script ([a17cdcc](https://github.com/yongwoon/ywc-agent-toolkit/commit/a17cdcc4f5d1acaa045af1de793b85bd3ca714d3))
* correct codex skill validation and add local validate script ([c2fb076](https://github.com/yongwoon/ywc-agent-toolkit/commit/c2fb076ede6f47e1c6e3f423ac437d21dd4ff694))
* correct table separator spacing and code block blank line in hooks README ([19b5057](https://github.com/yongwoon/ywc-agent-toolkit/commit/19b50574f38b96b1644d1e63655552730fa409a2))
* extend curl-pipe-sh pattern to catch sudo and absolute path shell variants ([73dd7b4](https://github.com/yongwoon/ywc-agent-toolkit/commit/73dd7b49173a3acb3d78941e23ab946b6ff4fc03))
* extend rm-home/rm-home-var patterns to match trailing path and glob variants ([6f53783](https://github.com/yongwoon/ywc-agent-toolkit/commit/6f537837246b156aca5da2f710698258c4776657))
* pin release-please-action to full commit SHA for supply-chain security ([10f57b7](https://github.com/yongwoon/ywc-agent-toolkit/commit/10f57b73cb9bd8b7e03eaa9371bf94deaa65a0c9))
* **release:** sync Codex plugin versions ([#91](https://github.com/yongwoon/ywc-agent-toolkit/issues/91)) ([a6120b1](https://github.com/yongwoon/ywc-agent-toolkit/commit/a6120b10cb48e8377438f2abcd749181b24abf5b))
* remove allowlist check from bash command path to prevent bypass ([13792cf](https://github.com/yongwoon/ywc-agent-toolkit/commit/13792cfb0d778e843e84fe52b298136018d381c3))
* remove duplicate ### markdown heading in changelog-sections ([#142](https://github.com/yongwoon/ywc-agent-toolkit/issues/142)) ([0ba4d03](https://github.com/yongwoon/ywc-agent-toolkit/commit/0ba4d0398d9c355019a15d9dc3f0fcd27d5067ac))
* remove Write/Edit/MultiEdit from auto-allow and block shell metachar chaining ([714de62](https://github.com/yongwoon/ywc-agent-toolkit/commit/714de62c4c451b903d262d87e82d2b6e439502a3))
* **skills:** improve activation accuracy for confidence-gate, receive-review, project-docs ([#71](https://github.com/yongwoon/ywc-agent-toolkit/issues/71)) ([bcc4098](https://github.com/yongwoon/ywc-agent-toolkit/commit/bcc40984f412077df15b270d91f6cd6419c1beb4))
* **skills:** make three S3 workflow steps decidable ([#110](https://github.com/yongwoon/ywc-agent-toolkit/issues/110)) ([d26f11e](https://github.com/yongwoon/ywc-agent-toolkit/commit/d26f11e6778e0a9c954c0ae61099ec8779d2320d))
* **skills:** strengthen dependency graph validation in task numbering ([#114](https://github.com/yongwoon/ywc-agent-toolkit/issues/114)) ([#116](https://github.com/yongwoon/ywc-agent-toolkit/issues/116)) ([d817cf6](https://github.com/yongwoon/ywc-agent-toolkit/commit/d817cf60464d5c58eb5475b709a01ff0827872dc))
* suppress SC2016 for intentional jq --arg single-quoted filter ([61b5ecf](https://github.com/yongwoon/ywc-agent-toolkit/commit/61b5ecfeeda41f52749c5242f5ff1261813887a3))
* **toolkit-eval:** correct Codex path, A3 heuristic, and project-mission trigger coverage ([#109](https://github.com/yongwoon/ywc-agent-toolkit/issues/109)) ([c75cdda](https://github.com/yongwoon/ywc-agent-toolkit/commit/c75cdda35e59f639025c41547424165028975ccc))
* **toolkit-eval:** reject description-derived trigger fixtures from the coverage floor ([#153](https://github.com/yongwoon/ywc-agent-toolkit/issues/153)) ([6c73da7](https://github.com/yongwoon/ywc-agent-toolkit/commit/6c73da7431836bd374cb77ec1bdec07639d76ba7))
* treat an unfinished bot-review poll as blocking instead of zero bots ([#147](https://github.com/yongwoon/ywc-agent-toolkit/issues/147)) ([2b33fbc](https://github.com/yongwoon/ywc-agent-toolkit/commit/2b33fbc878b4bf24e2cbc0b00b65be38bb7a1fa5))
* use GitHub App token to allow release-please tags to trigger release.yml ([a970c21](https://github.com/yongwoon/ywc-agent-toolkit/commit/a970c2119b17956197a990c3c71bf5de77cf6877))
* use lookaheads for order-independent force-push-to-main detection ([cb8d67b](https://github.com/yongwoon/ywc-agent-toolkit/commit/cb8d67b755d8ab91f59dd98f60c87e0c6cde4543))
* use word boundary for env-dump pattern to catch chained env calls ([7df6d06](https://github.com/yongwoon/ywc-agent-toolkit/commit/7df6d0693cc8faa5df001ae9de1d1013071b0744))
* validate webhook scheme (https-only) and use project basename for cwd in Slack payload ([366c40f](https://github.com/yongwoon/ywc-agent-toolkit/commit/366c40f9af567e0162e7208ceb1aad289a99e6ce))
* **ywc-create-pr:** use AskUserQuestion for language selection prompt ([#14](https://github.com/yongwoon/ywc-agent-toolkit/issues/14)) ([7edd043](https://github.com/yongwoon/ywc-agent-toolkit/commit/7edd0439003724bb6641e348c019679c91421be7))
* **ywc-toolkit-eval:** recognize security-engineer as Opus-tier role ([#160](https://github.com/yongwoon/ywc-agent-toolkit/issues/160)) ([66b1a9e](https://github.com/yongwoon/ywc-agent-toolkit/commit/66b1a9e3af86f316c94ec1347f5b557ed747421f))


### Changed

* add .entire/ to .gitignore ([81072e5](https://github.com/yongwoon/ywc-agent-toolkit/commit/81072e5876043a577125c230c42812a3501d81d9))
* add check-readme-freshness hook for skill directory changes ([f4d7341](https://github.com/yongwoon/ywc-agent-toolkit/commit/f4d7341317ad835bd4ac72af6bb208a61ccac815))
* add CLAUDE.md freshness check hook ([5ba79c4](https://github.com/yongwoon/ywc-agent-toolkit/commit/5ba79c49155b3d7dbfeea3452351b59e9df649ff))
* add CodeRabbit configuration ([f27ccbf](https://github.com/yongwoon/ywc-agent-toolkit/commit/f27ccbfc89ca1ccf78d897ecc21ec15245a82ef1))
* add comprehensive permissions and model config to claude settings ([661eb74](https://github.com/yongwoon/ywc-agent-toolkit/commit/661eb74cfbff826b30601e74db6eabee690fbb3f))
* add comprehensive permissions and model config to claude settings ([7fc06fd](https://github.com/yongwoon/ywc-agent-toolkit/commit/7fc06fda29c7fe8e838f96dd95d8396fe8b6fd8d))
* add README freshness hook and fix codex skill count ([6df2c94](https://github.com/yongwoon/ywc-agent-toolkit/commit/6df2c94a36973a82ad5e84e2daddd094db7e1a74))
* fix .gitignore typo and ignore tasks/ and docs/ywc-plans ([fa28491](https://github.com/yongwoon/ywc-agent-toolkit/commit/fa284919edd477ac0d468ffd272798286a34e7d4))
* ignore ywc executor state files in .gitignore ([475ac1a](https://github.com/yongwoon/ywc-agent-toolkit/commit/475ac1ab7577e416e1a5044463078281b8b53987))
* **main:** release 1.0.1 ([22c708a](https://github.com/yongwoon/ywc-agent-toolkit/commit/22c708a91a5a5db9670045be5e85d13f7710177f))
* **main:** release 1.0.1 ([b39cb6f](https://github.com/yongwoon/ywc-agent-toolkit/commit/b39cb6ff84d820b0ecbef86ebde78da089597b11))
* **main:** release 1.1.0 ([#11](https://github.com/yongwoon/ywc-agent-toolkit/issues/11)) ([f253032](https://github.com/yongwoon/ywc-agent-toolkit/commit/f2530326fb5b79604223644779d31182dcd207e6))
* **main:** release 1.10.0 ([#33](https://github.com/yongwoon/ywc-agent-toolkit/issues/33)) ([efaabdd](https://github.com/yongwoon/ywc-agent-toolkit/commit/efaabdd84c1f111505826e6189d3b102015e9693))
* **main:** release 1.11.0 ([#35](https://github.com/yongwoon/ywc-agent-toolkit/issues/35)) ([ceb90f9](https://github.com/yongwoon/ywc-agent-toolkit/commit/ceb90f91aa74b6f84a1aedf01230ed60b0b56596))
* **main:** release 1.12.0 ([#39](https://github.com/yongwoon/ywc-agent-toolkit/issues/39)) ([8b6def1](https://github.com/yongwoon/ywc-agent-toolkit/commit/8b6def14d0014600963f21eed1334fdf9fb3d917))
* **main:** release 1.12.1 ([#42](https://github.com/yongwoon/ywc-agent-toolkit/issues/42)) ([cd0b8e6](https://github.com/yongwoon/ywc-agent-toolkit/commit/cd0b8e60f401f32f83fc2a1dd0ca0fa217b2cabb))
* **main:** release 1.13.0 ([#44](https://github.com/yongwoon/ywc-agent-toolkit/issues/44)) ([cc12744](https://github.com/yongwoon/ywc-agent-toolkit/commit/cc12744ced51c1243efd292b1c4e58c5681a60f6))
* **main:** release 1.14.0 ([#47](https://github.com/yongwoon/ywc-agent-toolkit/issues/47)) ([e70cedc](https://github.com/yongwoon/ywc-agent-toolkit/commit/e70cedcbf13bbd650e1c44d720bcbbd310a8286b))
* **main:** release 1.15.0 ([#50](https://github.com/yongwoon/ywc-agent-toolkit/issues/50)) ([c26e62e](https://github.com/yongwoon/ywc-agent-toolkit/commit/c26e62ee825ffa355c5be1fe25124643bf5ecb4e))
* **main:** release 1.15.1 ([c275dec](https://github.com/yongwoon/ywc-agent-toolkit/commit/c275dec118a1b8156eb9fde281f40db98cb2cada))
* **main:** release 1.16.0 ([#56](https://github.com/yongwoon/ywc-agent-toolkit/issues/56)) ([0b1954a](https://github.com/yongwoon/ywc-agent-toolkit/commit/0b1954a6077b35fdd12146466d4c356d09d8bb57))
* **main:** release 1.17.0 ([#58](https://github.com/yongwoon/ywc-agent-toolkit/issues/58)) ([35acb5b](https://github.com/yongwoon/ywc-agent-toolkit/commit/35acb5b36341ab604101e964729e937bca58ea36))
* **main:** release 1.18.0 ([#61](https://github.com/yongwoon/ywc-agent-toolkit/issues/61)) ([2741120](https://github.com/yongwoon/ywc-agent-toolkit/commit/2741120de02b390e6108f02f4f223a31fe188276))
* **main:** release 1.19.0 ([#73](https://github.com/yongwoon/ywc-agent-toolkit/issues/73)) ([75c871a](https://github.com/yongwoon/ywc-agent-toolkit/commit/75c871a052d81477b4aea7474ddb8c442edcf12b))
* **main:** release 1.2.0 ([#13](https://github.com/yongwoon/ywc-agent-toolkit/issues/13)) ([af15d6e](https://github.com/yongwoon/ywc-agent-toolkit/commit/af15d6e9525dbbbee874c5e6bf1fe5a20ffec39b))
* **main:** release 1.2.1 ([#15](https://github.com/yongwoon/ywc-agent-toolkit/issues/15)) ([e77e260](https://github.com/yongwoon/ywc-agent-toolkit/commit/e77e260be8e1739d819869383aac7f1df51cb406))
* **main:** release 1.20.0 ([#81](https://github.com/yongwoon/ywc-agent-toolkit/issues/81)) ([86ce382](https://github.com/yongwoon/ywc-agent-toolkit/commit/86ce382d3d53ffe5434f9ed2390fbf49de765034))
* **main:** release 1.21.0 ([#86](https://github.com/yongwoon/ywc-agent-toolkit/issues/86)) ([6256ce3](https://github.com/yongwoon/ywc-agent-toolkit/commit/6256ce39cbb67a846d8a8e7c07a76e6b787b5fb6))
* **main:** release 1.21.1 ([#90](https://github.com/yongwoon/ywc-agent-toolkit/issues/90)) ([09893d4](https://github.com/yongwoon/ywc-agent-toolkit/commit/09893d4fdc33465a614be3966a594906a84a60d8))
* **main:** release 1.21.2 ([#92](https://github.com/yongwoon/ywc-agent-toolkit/issues/92)) ([32814d9](https://github.com/yongwoon/ywc-agent-toolkit/commit/32814d992cfa8b2377bb262f381d0b05ba74433f))
* **main:** release 1.21.3 ([#95](https://github.com/yongwoon/ywc-agent-toolkit/issues/95)) ([990111f](https://github.com/yongwoon/ywc-agent-toolkit/commit/990111fac4afe2fda75c440d2b3cd840475bf714))
* **main:** release 1.22.0 ([#97](https://github.com/yongwoon/ywc-agent-toolkit/issues/97)) ([5f8aa2e](https://github.com/yongwoon/ywc-agent-toolkit/commit/5f8aa2eb2395e63cb4097bd92c4b38431426c223))
* **main:** release 1.22.1 ([#99](https://github.com/yongwoon/ywc-agent-toolkit/issues/99)) ([4e4fcab](https://github.com/yongwoon/ywc-agent-toolkit/commit/4e4fcaba1007f504b4233fb675a4c6987885dbc0))
* **main:** release 1.22.2 ([#107](https://github.com/yongwoon/ywc-agent-toolkit/issues/107)) ([7e153db](https://github.com/yongwoon/ywc-agent-toolkit/commit/7e153db0bdd7a010a6d13df97d7be808ce9e35c0))
* **main:** release 1.22.3 ([#111](https://github.com/yongwoon/ywc-agent-toolkit/issues/111)) ([86f668f](https://github.com/yongwoon/ywc-agent-toolkit/commit/86f668fed22789f5f0786ef9a2066e469095bd4e))
* **main:** release 1.22.4 ([#117](https://github.com/yongwoon/ywc-agent-toolkit/issues/117)) ([d10dd74](https://github.com/yongwoon/ywc-agent-toolkit/commit/d10dd745af8b02738ea5ad8220c6ce845512af88))
* **main:** release 1.23.0 ([#119](https://github.com/yongwoon/ywc-agent-toolkit/issues/119)) ([b8c9e46](https://github.com/yongwoon/ywc-agent-toolkit/commit/b8c9e4695aa6544f08cd476015c7b5c207822065))
* **main:** release 1.23.1 ([#122](https://github.com/yongwoon/ywc-agent-toolkit/issues/122)) ([2e7f82d](https://github.com/yongwoon/ywc-agent-toolkit/commit/2e7f82ddb276e390e9854f47ec6767ecef9cb6f0))
* **main:** release 1.23.2 ([#124](https://github.com/yongwoon/ywc-agent-toolkit/issues/124)) ([fab4a14](https://github.com/yongwoon/ywc-agent-toolkit/commit/fab4a144f55fc9f4fb717db4ced72f6458e3155d))
* **main:** release 1.24.0 ([#126](https://github.com/yongwoon/ywc-agent-toolkit/issues/126)) ([2435471](https://github.com/yongwoon/ywc-agent-toolkit/commit/24354712a1a65c071e2e2c40702eed7b953f73af))
* **main:** release 1.24.1 ([#128](https://github.com/yongwoon/ywc-agent-toolkit/issues/128)) ([87e3455](https://github.com/yongwoon/ywc-agent-toolkit/commit/87e3455283dbe7fd403fca73c0ff3958c54b63b3))
* **main:** release 1.24.2 ([#130](https://github.com/yongwoon/ywc-agent-toolkit/issues/130)) ([dcb18ac](https://github.com/yongwoon/ywc-agent-toolkit/commit/dcb18ac62705a7a13076e5d2b601c174a460dbee))
* **main:** release 1.25.0 ([#132](https://github.com/yongwoon/ywc-agent-toolkit/issues/132)) ([2222e3d](https://github.com/yongwoon/ywc-agent-toolkit/commit/2222e3d90adcc31da5dede75f1c289d98bb3ff48))
* **main:** release 1.26.0 ([#134](https://github.com/yongwoon/ywc-agent-toolkit/issues/134)) ([84f2a46](https://github.com/yongwoon/ywc-agent-toolkit/commit/84f2a4682397fa14fba7760a25f41886495835a9))
* **main:** release 1.27.0 ([#136](https://github.com/yongwoon/ywc-agent-toolkit/issues/136)) ([beaab09](https://github.com/yongwoon/ywc-agent-toolkit/commit/beaab0972dd7092ea5b22ca573bfd2faa5a26a1c))
* **main:** release 1.28.1 ([#143](https://github.com/yongwoon/ywc-agent-toolkit/issues/143)) ([9627bad](https://github.com/yongwoon/ywc-agent-toolkit/commit/9627bad841705d31aaf24691aaeaf73d00cad190))
* **main:** release 1.29.0 ([#145](https://github.com/yongwoon/ywc-agent-toolkit/issues/145)) ([0aa6396](https://github.com/yongwoon/ywc-agent-toolkit/commit/0aa63967fc4bb80bb6cf22f4d4ff337bccc2788a))
* **main:** release 1.3.0 ([#17](https://github.com/yongwoon/ywc-agent-toolkit/issues/17)) ([2327d67](https://github.com/yongwoon/ywc-agent-toolkit/commit/2327d6729f559ff87f2805fb14d8a43295a20f1a))
* **main:** release 1.30.0 ([#149](https://github.com/yongwoon/ywc-agent-toolkit/issues/149)) ([2bdbb05](https://github.com/yongwoon/ywc-agent-toolkit/commit/2bdbb05b10bcf6e278e0ca615c274bbe05da4b16))
* **main:** release 1.30.1 ([#154](https://github.com/yongwoon/ywc-agent-toolkit/issues/154)) ([cab1446](https://github.com/yongwoon/ywc-agent-toolkit/commit/cab14469f2dcd0410342c67058b2c2e191e50e5d))
* **main:** release 1.31.0 ([#156](https://github.com/yongwoon/ywc-agent-toolkit/issues/156)) ([d983bc2](https://github.com/yongwoon/ywc-agent-toolkit/commit/d983bc2f2a80facefc8215cfa5c14a06fd283d7e))
* **main:** release 1.4.0 ([#19](https://github.com/yongwoon/ywc-agent-toolkit/issues/19)) ([50b28b4](https://github.com/yongwoon/ywc-agent-toolkit/commit/50b28b401b7ec22b9e44a4a99456fb34de7810e9))
* **main:** release 1.5.0 ([#21](https://github.com/yongwoon/ywc-agent-toolkit/issues/21)) ([90e21f0](https://github.com/yongwoon/ywc-agent-toolkit/commit/90e21f019abcb97e58819c8aabfac3797a40f137))
* **main:** release 1.5.1 ([#23](https://github.com/yongwoon/ywc-agent-toolkit/issues/23)) ([a2c682b](https://github.com/yongwoon/ywc-agent-toolkit/commit/a2c682b4b6269f653acbccfc9a5a73b5cbb304c2))
* **main:** release 1.6.0 ([#24](https://github.com/yongwoon/ywc-agent-toolkit/issues/24)) ([a772f36](https://github.com/yongwoon/ywc-agent-toolkit/commit/a772f36bf4fe108719566dc3ccc1108d3f9bd835))
* **main:** release 1.7.0 ([#26](https://github.com/yongwoon/ywc-agent-toolkit/issues/26)) ([3fa5ad5](https://github.com/yongwoon/ywc-agent-toolkit/commit/3fa5ad5402d1231cd6e5cb631c64d2a42967eaf1))
* **main:** release 1.8.0 ([#29](https://github.com/yongwoon/ywc-agent-toolkit/issues/29)) ([bc280db](https://github.com/yongwoon/ywc-agent-toolkit/commit/bc280dbd982e697eeb2775462a05f0d701d0e418))
* **main:** release 1.9.0 ([#31](https://github.com/yongwoon/ywc-agent-toolkit/issues/31)) ([3f5c055](https://github.com/yongwoon/ywc-agent-toolkit/commit/3f5c055397f6b7d1c9d672a6db6a2f778b3e276f))
* mark 000001-010-infra-add-hook-source-assets as completed ([b039b3a](https://github.com/yongwoon/ywc-agent-toolkit/commit/b039b3a03633d7dda939b12a67224080bbd2451d))
* mark 000002-010-infra-implement-hook-installer as completed ([660ab86](https://github.com/yongwoon/ywc-agent-toolkit/commit/660ab864f4fd476e468ee9fd432407df68f7cc6a))
* mark 000003-010-infra-update-toolkit-readme as completed ([c75a8d6](https://github.com/yongwoon/ywc-agent-toolkit/commit/c75a8d6b7f868fec88e82cea29dcbefcfe1b5b68))
* remove non-ywc codex skill files ([ce1e0e6](https://github.com/yongwoon/ywc-agent-toolkit/commit/ce1e0e66053f789552407c24eec63d8f2c7d6a93))
* retrigger release-please after app installation fix ([a4249f0](https://github.com/yongwoon/ywc-agent-toolkit/commit/a4249f090432983f4b250df59caadb454f709d25))
* retrigger release-please after label fix ([49725ba](https://github.com/yongwoon/ywc-agent-toolkit/commit/49725bad31f483f78ce3e3b4353897a0406664a2))
* retrigger release-please with correct app credentials ([ae3acd1](https://github.com/yongwoon/ywc-agent-toolkit/commit/ae3acd1793d62ee06e7e494e357a67c3ed6b78eb))
* retrigger release-please with correct app id ([7e64450](https://github.com/yongwoon/ywc-agent-toolkit/commit/7e64450e55c4e28f72f96adcc6c07e7435a12f8f))
* trigger release-please for v1.1.0 ([cabd9e1](https://github.com/yongwoon/ywc-agent-toolkit/commit/cabd9e11b80c1484cafdfb1b01c19765546dab94))
* trigger release-please workflow ([e5454f8](https://github.com/yongwoon/ywc-agent-toolkit/commit/e5454f829388302ef64fd297a3938baf59bea514))


### Documentation

* add CLAUDE.md for Claude Code project guidance ([607a7eb](https://github.com/yongwoon/ywc-agent-toolkit/commit/607a7ebc4e2c81f05565cea220d334b347f1e942))
* add Hook installation section to root README.md ([86d4dce](https://github.com/yongwoon/ywc-agent-toolkit/commit/86d4dce4fd33173101580aed2d071becade3109f))
* add plugin install step to README installation guide ([#129](https://github.com/yongwoon/ywc-agent-toolkit/issues/129)) ([94e7712](https://github.com/yongwoon/ywc-agent-toolkit/commit/94e77121a4ae65b0783261fa551088e994e7f7cd))
* **codex:** align skill guidance with Codex runtime ([#48](https://github.com/yongwoon/ywc-agent-toolkit/issues/48)) ([ee5093a](https://github.com/yongwoon/ywc-agent-toolkit/commit/ee5093acd861d8223797fdca6e1be0a08b6d5763))
* document release-please PR title requirement ([c858959](https://github.com/yongwoon/ywc-agent-toolkit/commit/c858959afca5ca02e50bb2f4b68e3b8d19cbea19))
* fix codex skill count and update install example ([cc1fe4b](https://github.com/yongwoon/ywc-agent-toolkit/commit/cc1fe4b1503067f2ee02f97842dcbc087126375f))
* fix marketplace install commands and add to translated READMEs ([fc060b1](https://github.com/yongwoon/ywc-agent-toolkit/commit/fc060b1901388700ac73f6f14d6106904720f343))
* harden data-integrity guidance across Codex and Claude Code skills ([#121](https://github.com/yongwoon/ywc-agent-toolkit/issues/121)) ([c7da68b](https://github.com/yongwoon/ywc-agent-toolkit/commit/c7da68b3405ed9fbedd8f3073f80c70620efa7a9))
* **impl-review:** sync README agent model and locale list ([#139](https://github.com/yongwoon/ywc-agent-toolkit/issues/139)) ([89cc11a](https://github.com/yongwoon/ywc-agent-toolkit/commit/89cc11a99d78fca72c9efa0d658c41bfc315c2d4))
* improve README navigation ([#79](https://github.com/yongwoon/ywc-agent-toolkit/issues/79)) ([f270126](https://github.com/yongwoon/ywc-agent-toolkit/commit/f270126ec77a6405aed614d8e8b0fe755fd31b4c))
* **readme:** improve navigation with quick-start, goal table, skill links, and pipeline diagram ([#72](https://github.com/yongwoon/ywc-agent-toolkit/issues/72)) ([3fdea6f](https://github.com/yongwoon/ywc-agent-toolkit/commit/3fdea6f0881b551473dc39a04430e39eff4700a3))
* rewrite recommended development pipeline from real usage patterns ([#51](https://github.com/yongwoon/ywc-agent-toolkit/issues/51)) ([b79da80](https://github.com/yongwoon/ywc-agent-toolkit/commit/b79da80b297d1a27339f14d8285ac9dcd398bf88))
* streamline repository documentation ([#22](https://github.com/yongwoon/ywc-agent-toolkit/issues/22)) ([8029d78](https://github.com/yongwoon/ywc-agent-toolkit/commit/8029d7823e03ef166621ef5460b66ade0ea601b7))
* strengthen executor contract gates ([#93](https://github.com/yongwoon/ywc-agent-toolkit/issues/93)) ([40cb990](https://github.com/yongwoon/ywc-agent-toolkit/commit/40cb990571d7e31946aa0d22c0c5d6a21816eee1))
* sync documentation and improve skill/agent authoring rules ([#41](https://github.com/yongwoon/ywc-agent-toolkit/issues/41)) ([2169f75](https://github.com/yongwoon/ywc-agent-toolkit/commit/2169f750860fd57712553030117082ade629012f))
* sync skill counts and add spec-ready + Other pipelines to README ([#98](https://github.com/yongwoon/ywc-agent-toolkit/issues/98)) ([798258e](https://github.com/yongwoon/ywc-agent-toolkit/commit/798258eea4d765689b659ba18c8ddf6ba78c108e))
* **task-generator:** standardize options and triggers ([#123](https://github.com/yongwoon/ywc-agent-toolkit/issues/123)) ([0d424d5](https://github.com/yongwoon/ywc-agent-toolkit/commit/0d424d502e452b81072d74e056bd2dbc1c364cda))
* update CHANGELOG.md for v1.0.0 ([7c8d9f3](https://github.com/yongwoon/ywc-agent-toolkit/commit/7c8d9f3e0578eb9f30d28d22c9a227e5d86864dd))


### Translations

* add es/zh translations for all skills and translation infrastructure ([db9a7e1](https://github.com/yongwoon/ywc-agent-toolkit/commit/db9a7e14b56788fa15173abdff37c6c4c55fd64e))

## [1.32.0] (2026-08-12)

### Added

* **context safety:** add executable evaluation coverage for verified artifact authority, non-interactive closure, context handoff, claim isolation, and privacy boundaries across the affected Codex skills.

### Changed

* **Codex distribution:** synchronize the eight affected skills, release metadata, and generated plugin bundle for the context-safety contract.

## [1.31.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.30.1...v1.31.0) (2026-07-30)


### Added

* add ywc-adr, ywc-implement skills and Codex SDLC v1.1 gap closure ([#155](https://github.com/yongwoon/ywc-agent-toolkit/issues/155)) ([39b68a5](https://github.com/yongwoon/ywc-agent-toolkit/commit/39b68a59e1e4b5e7180efbc471c75a382e53c8e5))
* **ywc-brainstorm:** add self-review pass and existing-code guidance ([#158](https://github.com/yongwoon/ywc-agent-toolkit/issues/158)) ([b3bb65d](https://github.com/yongwoon/ywc-agent-toolkit/commit/b3bb65d188f1daa581130649b78baa4cfb9f67d7))
* **ywc-plan:** add Codebase-Fact Pre-check and Global Constraints/Interfaces sections ([#157](https://github.com/yongwoon/ywc-agent-toolkit/issues/157)) ([a0d885b](https://github.com/yongwoon/ywc-agent-toolkit/commit/a0d885b27c1ece3b483b66d3652487179f529f22))
* **ywc-security-engineer:** promote to Opus tier, remove Phase 2 escalation ([#159](https://github.com/yongwoon/ywc-agent-toolkit/issues/159)) ([7158da9](https://github.com/yongwoon/ywc-agent-toolkit/commit/7158da91cae4443e28ee8c3ee09453ce134dfb8d))


### Fixed

* **ywc-toolkit-eval:** recognize security-engineer as Opus-tier role ([#160](https://github.com/yongwoon/ywc-agent-toolkit/issues/160)) ([66b1a9e](https://github.com/yongwoon/ywc-agent-toolkit/commit/66b1a9e3af86f316c94ec1347f5b557ed747421f))

## [1.30.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.30.0...v1.30.1) (2026-07-24)


### Fixed

* **toolkit-eval:** reject description-derived trigger fixtures from the coverage floor ([#153](https://github.com/yongwoon/ywc-agent-toolkit/issues/153)) ([6c73da7](https://github.com/yongwoon/ywc-agent-toolkit/commit/6c73da7431836bd374cb77ec1bdec07639d76ba7))

## [1.30.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.29.0...v1.30.0) (2026-07-22)


### Added

* add isolated evaluation runners for Claude Code and Codex skills ([#151](https://github.com/yongwoon/ywc-agent-toolkit/issues/151)) ([0e8cee7](https://github.com/yongwoon/ywc-agent-toolkit/commit/0e8cee7210700922a3ac8f1f6754c07b9b8e7d57))


### Fixed

* treat an unfinished bot-review poll as blocking instead of zero bots ([#147](https://github.com/yongwoon/ywc-agent-toolkit/issues/147)) ([2b33fbc](https://github.com/yongwoon/ywc-agent-toolkit/commit/2b33fbc878b4bf24e2cbc0b00b65be38bb7a1fa5))

## [1.29.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.28.1...v1.29.0) (2026-07-16)


### Added

* add ywc-auth-implement skill for Claude Code and Codex ([#144](https://github.com/yongwoon/ywc-agent-toolkit/issues/144)) ([da29d14](https://github.com/yongwoon/ywc-agent-toolkit/commit/da29d1436be97847ec0ade92b6c04a12976f5825))
* adopt GPT-5.6 Terra for Codex agents and clean up stale model references ([#146](https://github.com/yongwoon/ywc-agent-toolkit/issues/146)) ([915983a](https://github.com/yongwoon/ywc-agent-toolkit/commit/915983aafc904880ee14e68fc64b744ef257cb4b))

## [1.28.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.28.0...v1.28.1) (2026-07-15)


### Fixed

* remove duplicate ### markdown heading in changelog-sections ([#142](https://github.com/yongwoon/ywc-agent-toolkit/issues/142)) ([0ba4d03](https://github.com/yongwoon/ywc-agent-toolkit/commit/0ba4d0398d9c355019a15d9dc3f0fcd27d5067ac))

## [1.28.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.27.0...v1.28.0) (2026-07-15)


### ### Added

* **codex:** add wayfinder routing, task preview approval, agentic preview flow, and persisted tech-research handoff contracts.
* **codex:** port PR conflict and merge-readiness handling to Codex PR workflow skills from develop-with-llm PR #101.
* **codex:** sync planning, PR health, spec validation, onboarding, and parity workflow updates into the Codex plugin package.
* **eval:** detect removed mechanical baseline keys and document the baseline cleanup.


### ### Documentation

* **release:** add Codex validation, smell review, install safety, and plugin parity evidence for the SDLC v1.1 release gate.

## [1.27.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.26.0...v1.27.0) (2026-07-14)


### ### Added

* **code-gen:** add --review flag and force critical-path review ([#137](https://github.com/yongwoon/ywc-agent-toolkit/issues/137)) ([f64dba0](https://github.com/yongwoon/ywc-agent-toolkit/commit/f64dba0eb5928a942f66f2beaa93d74caa13a297))
* **skill-author:** audit workflow, deletion-test pilot, and 80-word description cap enforcement ([#135](https://github.com/yongwoon/ywc-agent-toolkit/issues/135)) ([940b5d7](https://github.com/yongwoon/ywc-agent-toolkit/commit/940b5d7c53b91c9ec6ecb2844d0c67423c8a2a83))


### ### Documentation

* **impl-review:** sync README agent model and locale list ([#139](https://github.com/yongwoon/ywc-agent-toolkit/issues/139)) ([89cc11a](https://github.com/yongwoon/ywc-agent-toolkit/commit/89cc11a99d78fca72c9efa0d658c41bfc315c2d4))

## [1.26.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.25.0...v1.26.0) (2026-07-10)


### ### Added

* apply Fable agent-engineering insights across Claude Code and Codex skills ([#133](https://github.com/yongwoon/ywc-agent-toolkit/issues/133)) ([6fce4b0](https://github.com/yongwoon/ywc-agent-toolkit/commit/6fce4b0a9c8c99a081154daba1e8ff1d5fddf94f))

## [1.25.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.24.2...v1.25.0) (2026-07-08)


### ### Added

* add infrastructure design/review/optimize skill suite ([#131](https://github.com/yongwoon/ywc-agent-toolkit/issues/131)) ([43194ac](https://github.com/yongwoon/ywc-agent-toolkit/commit/43194ac3a7c6ff72667adb125685fbe97a0a7bba))

## [1.24.2](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.24.1...v1.24.2) (2026-07-06)


### ### Documentation

* add plugin install step to README installation guide ([#129](https://github.com/yongwoon/ywc-agent-toolkit/issues/129)) ([94e7712](https://github.com/yongwoon/ywc-agent-toolkit/commit/94e77121a4ae65b0783261fa551088e994e7f7cd))

## [1.24.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.24.0...v1.24.1) (2026-07-06)


### ### Fixed

* add ywc-setup evals and resolve Phase 000043 toolkit-eval backlog ([#127](https://github.com/yongwoon/ywc-agent-toolkit/issues/127)) ([a6140e7](https://github.com/yongwoon/ywc-agent-toolkit/commit/a6140e7f7986d5f1ec0df1a560fa9642067e2b0c))

## [1.24.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.23.2...v1.24.0) (2026-07-03)


### ### Added

* add language setup skills ([#125](https://github.com/yongwoon/ywc-agent-toolkit/issues/125)) ([995d69d](https://github.com/yongwoon/ywc-agent-toolkit/commit/995d69dd957531904d60a4dc4607a93839315e84))

## [1.23.2](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.23.1...v1.23.2) (2026-07-03)


### ### Documentation

* **task-generator:** standardize options and triggers ([#123](https://github.com/yongwoon/ywc-agent-toolkit/issues/123)) ([0d424d5](https://github.com/yongwoon/ywc-agent-toolkit/commit/0d424d502e452b81072d74e056bd2dbc1c364cda))

## [1.23.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.23.0...v1.23.1) (2026-07-03)


### ### Documentation

* harden data-integrity guidance across Codex and Claude Code skills ([#121](https://github.com/yongwoon/ywc-agent-toolkit/issues/121)) ([c7da68b](https://github.com/yongwoon/ywc-agent-toolkit/commit/c7da68b3405ed9fbedd8f3073f80c70620efa7a9))

## [1.23.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.22.4...v1.23.0) (2026-07-02)


### ### Added

* **skills:** add English/Chinese/Spanish support to ywc-project-docs ([#118](https://github.com/yongwoon/ywc-agent-toolkit/issues/118)) ([1ed4e52](https://github.com/yongwoon/ywc-agent-toolkit/commit/1ed4e5254b57ff5681f6ae52adbc915621a12fa8))
* ywc 스킬 zh/es 언어 지원 추가 ([#120](https://github.com/yongwoon/ywc-agent-toolkit/issues/120)) ([e2e3cf5](https://github.com/yongwoon/ywc-agent-toolkit/commit/e2e3cf5e9b22c21fed72adb4e881979cc46a7e8e))

## [1.22.4](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.22.3...v1.22.4) (2026-07-01)


### ### Fixed

* **skills:** strengthen dependency graph validation in task numbering ([#114](https://github.com/yongwoon/ywc-agent-toolkit/issues/114)) ([#116](https://github.com/yongwoon/ywc-agent-toolkit/issues/116)) ([d817cf6](https://github.com/yongwoon/ywc-agent-toolkit/commit/d817cf60464d5c58eb5475b709a01ff0827872dc))

## [1.22.3](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.22.2...v1.22.3) (2026-07-01)


### ### Fixed

* **agents:** clarify performance-engineer &lt;-&gt; language-reviewer boundary ([#112](https://github.com/yongwoon/ywc-agent-toolkit/issues/112)) ([e5f737f](https://github.com/yongwoon/ywc-agent-toolkit/commit/e5f737f318740c5c4f5028c719f17d6e83fb0003))
* **agents:** resolve A1 body-level idiom/magnitude ownership overlap ([#113](https://github.com/yongwoon/ywc-agent-toolkit/issues/113)) ([7c3a251](https://github.com/yongwoon/ywc-agent-toolkit/commit/7c3a25144d76d885636ad046c8e331b710cf2cdc))
* **skills:** make three S3 workflow steps decidable ([#110](https://github.com/yongwoon/ywc-agent-toolkit/issues/110)) ([d26f11e](https://github.com/yongwoon/ywc-agent-toolkit/commit/d26f11e6778e0a9c954c0ae61099ec8779d2320d))
* **toolkit-eval:** correct Codex path, A3 heuristic, and project-mission trigger coverage ([#109](https://github.com/yongwoon/ywc-agent-toolkit/issues/109)) ([c75cdda](https://github.com/yongwoon/ywc-agent-toolkit/commit/c75cdda35e59f639025c41547424165028975ccc))

## [1.22.2](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.22.1...v1.22.2) (2026-06-25)


### ### Fixed

* **codex:** PR health sweep 계약 정합화 및 plugin listing 준비 ([#106](https://github.com/yongwoon/ywc-agent-toolkit/issues/106)) ([ecab49c](https://github.com/yongwoon/ywc-agent-toolkit/commit/ecab49c00ff4aefbaf8ea9f3d4076409636e224a))

## [1.22.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.22.0...v1.22.1) (2026-06-24)


### ### Documentation

* sync skill counts and add spec-ready + Other pipelines to README ([#98](https://github.com/yongwoon/ywc-agent-toolkit/issues/98)) ([798258e](https://github.com/yongwoon/ywc-agent-toolkit/commit/798258eea4d765689b659ba18c8ddf6ba78c108e))

## [1.22.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.21.3...v1.22.0) (2026-06-23)


### ### Added

* improve skill contracts and eval coverage ([#96](https://github.com/yongwoon/ywc-agent-toolkit/issues/96)) ([3121af2](https://github.com/yongwoon/ywc-agent-toolkit/commit/3121af2d859753b52ff0021798402485a804c1ed))

## [1.21.3](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.21.2...v1.21.3) (2026-06-18)


### ### Documentation

* strengthen executor contract gates ([#93](https://github.com/yongwoon/ywc-agent-toolkit/issues/93)) ([40cb990](https://github.com/yongwoon/ywc-agent-toolkit/commit/40cb990571d7e31946aa0d22c0c5d6a21816eee1))

## [1.21.2](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.21.1...v1.21.2) (2026-06-17)


### ### Fixed

* **release:** sync Codex plugin versions ([#91](https://github.com/yongwoon/ywc-agent-toolkit/issues/91)) ([a6120b1](https://github.com/yongwoon/ywc-agent-toolkit/commit/a6120b10cb48e8377438f2abcd749181b24abf5b))

## [1.21.1](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.21.0...v1.21.1) (2026-06-17)


### ### Fixed

* **codex:** support marketplace package workflow ([#89](https://github.com/yongwoon/ywc-agent-toolkit/issues/89)) ([1b08f66](https://github.com/yongwoon/ywc-agent-toolkit/commit/1b08f66b8a386fe90e82e477e6c82fec6a9f7909))

## [1.21.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.20.0...v1.21.0) (2026-06-16)


### ### Added

* **skills:** add --aggregate-pr to claude-code & codex executors ([#85](https://github.com/yongwoon/ywc-agent-toolkit/issues/85)) ([95ab0e1](https://github.com/yongwoon/ywc-agent-toolkit/commit/95ab0e19aa2cd7b9cc77a7582a3d5cbc05de83c6))
* **skills:** toolkit-eval harness fixes + catalog activation/boundary resolution ([#88](https://github.com/yongwoon/ywc-agent-toolkit/issues/88)) ([561943a](https://github.com/yongwoon/ywc-agent-toolkit/commit/561943acc978981037df6b21ec6b0f7ae0ac1dec))
* **skills:** worktree 실행 및 Codex 평가 계약 개선 ([#87](https://github.com/yongwoon/ywc-agent-toolkit/issues/87)) ([8383883](https://github.com/yongwoon/ywc-agent-toolkit/commit/8383883bdf353cc11b37ac0d3adb5b30e42e04a5))

## [1.20.0](https://github.com/yongwoon/ywc-agent-toolkit/compare/v1.19.0...v1.20.0) (2026-06-13)


### ### Added

* add review learnings, design renew, and schema guide ([#80](https://github.com/yongwoon/ywc-agent-toolkit/issues/80)) ([eedc4d5](https://github.com/yongwoon/ywc-agent-toolkit/commit/eedc4d558f1f07642a9ed1dd67dfdc0b4e4dc1e8))
* **skills:** add PR conflict resolution and merge-readiness gate ([#82](https://github.com/yongwoon/ywc-agent-toolkit/issues/82)) ([f3a2384](https://github.com/yongwoon/ywc-agent-toolkit/commit/f3a23848a5f8b7549e16bb275348ffc1b640eaa5))


### ### Documentation

* improve README navigation ([#79](https://github.com/yongwoon/ywc-agent-toolkit/issues/79)) ([f270126](https://github.com/yongwoon/ywc-agent-toolkit/commit/f270126ec77a6405aed614d8e8b0fe755fd31b4c))

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
