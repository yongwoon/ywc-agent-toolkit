# ywc-agent-toolkit

> 이 문서는 현재 번역 중입니다. 전체 문서는 [English](README.md) 를 참조하세요.
>
> 번역에 기여하고 싶으신 분은 [Translation Issue](../../issues/new?template=translation.md) 를 작성해 주세요.

---

Claude Code 및 Codex 용 개발 워크플로우 자동화 스킬 모음입니다.
계획 수립, 사양서 작성, 태스크 분해, 코드 생성, 리뷰, 릴리스까지 전 과정을 지원합니다.

현재 Claude Code skill 38개, Codex skill 37개, Claude Code agent 12개, Codex custom agent 7개를 제공합니다.

## 사전 요구사항

플러그인 마켓플레이스 및 Codex 플러그인 설치는 **사전 요구사항 없음** — 도구가 자동으로 처리합니다.

**bash 스크립트 fallback** 사용 시, `install.sh` 실행 전에 다음이 필요합니다:

| 도구 | 필요한 이유 | 설치 방법 |
| ---- | ----------- | --------- |
| `git` | 저장소 클론 | 대부분의 시스템에 기본 설치됨 |
| `bash ≥ 3.2` | `install.sh` 실행 | macOS / Linux에 기본 설치됨 |
| `jq` | 훅 등록 | `brew install jq` / `apt-get install jq` |

**스킬 런타임** (설치에는 불필요):

| 도구 | 사용 스킬 | 설치 방법 |
| ---- | --------- | --------- |
| `python3 ≥ 3.9` | 스킬 런타임 보조 기능: `ywc-parallel-executor`, `ywc-finish-branch`, `ywc-merge-dependabot`; Claude Code hooks는 Python ≥ 3.11 필요 | macOS 12.3+에 기본 설치; `brew install python3` |
| `gh` CLI | PR 기반 및 GitHub release 스킬/모드: `ywc-handle-pr-reviews`, `ywc-spec-writer --from-pr/--from-prs`, `ywc-release-pr-list`, `ywc-create-pr`, `ywc-finish-branch` PR 모드, `ywc-merge-dependabot`, `ywc-sequential-executor`/`ywc-parallel-executor`, `ywc-gen-testcase` | `brew install gh` / [cli.github.com](https://cli.github.com) |

---

## 설치

### Claude Code 플러그인 마켓플레이스 (권장)

```bash
# 마켓플레이스 소스 추가 (최초 1회)
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

명령 실행 후 Plugin UI의 **Marketplaces** 탭에서 **ywc-agent-toolkit**을 설치하세요.
클론이나 bash 없이 `~/.claude/skills/`에 자동 설치됩니다.

### Codex CLI 플러그인 디렉터리

이 저장소는 Superpowers와 같은 multi-harness 패키징 방식을 따릅니다. Claude Code 메타데이터는 [`.claude-plugin/`](.claude-plugin/) 아래에, Codex 메타데이터는 [`.codex-plugin/`](.codex-plugin/) 아래에 분리되어 있습니다. Codex의 source of truth는 [codex/skills](codex/skills)입니다. repo 범위 Codex marketplace catalog인 [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json)은 generated plugin package인 `plugins/ywc-agent-toolkit`을 노출하며, 그 안의 `skills/` 디렉터리는 `bash scripts/sync-codex-plugin.sh`가 `codex/skills`에서 생성하고 `bash scripts/validate.sh`가 최신 상태를 검사합니다.

이 저장소를 Codex plugin marketplace source로 추가하면 Codex에서 `ywc-agent-toolkit`을 설치할 수 있지만, 공식 OpenAI curated marketplace에 등록되었다는 의미는 아닙니다.

이 저장소를 Codex plugin marketplace source로 추가하세요:

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit
```

이미 marketplace를 추가한 상태라면 Git snapshot을 먼저 갱신하세요:

```bash
codex plugin marketplace upgrade ywc-agent-toolkit
```

그다음 설정된 marketplace에서 바로 설치하세요:

```bash
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit
```

또는 플러그인 디렉터리를 여세요:

```text
codex
/plugins
```

인터랙티브 Codex 세션 안에서 **YWC Agent Toolkit** marketplace 탭을 선택하고 **ywc-agent-toolkit**을 검색한 뒤 **Install plugin**을 선택하세요.

### Codex App Plugins 사이드바

Codex App에서는 사이드바의 **Plugins**를 열고 **YWC Agent Toolkit** source를 선택한 뒤 **ywc-agent-toolkit**을 검색하거나 찾으세요. 플러그인 소스가 `yongwoon/ywc-agent-toolkit`인지 확인하고 플러그인 상세 화면에서 설치하세요.

사용 중인 환경에서 marketplace source 설치를 사용할 수 없다면 아래 bash fallback을 사용하세요.

### Codex skill 유지보수 workflow

Codex skill은 [codex/skills](codex/skills)에서 수정하세요. `plugins/ywc-agent-toolkit/skills`는 `codex plugin add`가 사용하는 generated marketplace package이므로 primary source로 직접 수정하지 마세요.

Codex marketplace package가 자동으로 최신 상태를 유지되도록 repository Git hook을 한 번 설치하세요:

```bash
bash scripts/install-git-hooks.sh
```

Hook이 설치되어 있으면 `codex/skills` 변경이 staged된 commit에서 `bash scripts/sync-codex-plugin.sh`를 실행하고, generated package인 `plugins/ywc-agent-toolkit`을 자동 stage한 뒤 `bash scripts/validate.sh`를 실행합니다. Codex skill/package 변경이 포함된 push에서도 stale package 검사와 validation을 실행합니다.

Hook을 설치하지 않은 환경에서는 commit 전에 같은 명령을 수동으로 실행하세요:

```bash
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
```

bash fallback(`bash scripts/install.sh --codex`)은 `codex/skills`에서 직접 설치합니다. marketplace flow(`codex plugin add ywc-agent-toolkit@ywc-agent-toolkit`)는 generated package인 `plugins/ywc-agent-toolkit`에서 설치합니다.

### bash 스크립트 fallback

```bash
YWC_REF=<release-tag-or-reviewed-commit>
git clone --branch "$YWC_REF" --depth 1 https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit
git remote get-url origin
git rev-parse --verify HEAD

# Claude Code
bash scripts/install.sh --cc

# Codex
bash scripts/install.sh --codex

# 양쪽 모두
bash scripts/install.sh --all
```

자세한 내용은 [README.md](README.md) 를 참조하세요.

---

## Skills

### Planning & Spec

| Skill | 설명 |
| ----- | ---- |
| [`ywc-plan`](claude-code/skills/ywc-plan/README.md) | 러프한 아이디어를 `plan.md`(Small) 또는 Spec 문서(Medium/Large)로 변환합니다 |
| [`ywc-spec-writer`](claude-code/skills/ywc-spec-writer/README.md) | Spec 문서(`docs/specification/`)를 작성하고 업데이트합니다 |
| [`ywc-spec-validate`](claude-code/skills/ywc-spec-validate/README.md) | Spec 품질(Completeness / Consistency / Feasibility)을 검증합니다 |
| [`ywc-tech-research`](claude-code/skills/ywc-tech-research/README.md) | 라이브러리를 조사하고 기술 접근 방식을 비교합니다 |
| [`ywc-ubiquitous-language`](claude-code/skills/ywc-ubiquitous-language/README.md) | 도메인 ubiquitous language 사전을 만들고 유지합니다 |
| [`ywc-project-mission`](claude-code/skills/ywc-project-mission/README.md) | 프로젝트의 지속적인 Mission / Success Criteria / Out-of-Scope를 `docs/project-mission.md`에 저장합니다(ywc-plan이 계획의 프레임으로 읽음) |
| [`ywc-brainstorm`](claude-code/skills/ywc-brainstorm/README.md) | 공식 plan 또는 spec을 작성하기 전에 러프한 아이디어를 정리합니다 |
| [`ywc-confidence-gate`](claude-code/skills/ywc-confidence-gate/README.md) | 규모 있는 구현을 시작하기 전에 준비 상태와 리스크를 확인합니다 |
| [`ywc-onboard-repo`](claude-code/skills/ywc-onboard-repo/README.md) | 익숙하지 않은 저장소를 위한 온보딩 컨텍스트를 생성합니다 |
| [`ywc-spec-ready`](claude-code/skills/ywc-spec-ready/README.md) | spec을 ywc-spec-validate DONE 상태까지 재귀적으로 수렴시킵니다(validate ↔ ywc-plan --update-spec 루프, 기본 최대 5회) |

---

## Review Skill HTML 출력 모드

9개의 Review / Report skill이 opt-in `--format html` flag를 지원합니다. 이 flag는 Markdown 대신 브라우저에서 바로 열리는 self-contained HTML report를 생성합니다.

**지원 Skill:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`, `ywc-design-renew`

**도입 배경:** AI가 생성한 100줄 이상의 Markdown 문서는 끝까지 읽히지 않는 경향이 있으며, 읽히지 않는 report는 의사결정을 이끌지 못합니다. HTML은 색상, severity coding, tab, 인터랙티브 control(체크박스, `Copy as Markdown`)을 더해, 결과물을 받는 사람이 실제로 읽고 행동하게 만듭니다.

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-security-audit --code api/src/ --format html
/ywc-gen-testcase 250 --format html   # localStorage sign-off가 포함된 인터랙티브 테스트시트
```

> **⚠️ Token 비용** — HTML 출력은 Markdown 대비 output token을 2~4배 사용하며 생성 시간도 더 깁니다. 기본값은 `markdown`이며, 사람이 브라우저에서 읽을 report에 한해 HTML을 활성화하시기 바랍니다.

---

## Custom Agent

Claude Code에는 worker, reviewer, specialist dispatch용 **12개**의 custom agent가 포함되어 있습니다. `~/.claude/agents/`에 설치되며, 자세한 내용은 [`claude-code/agents/README.md`](claude-code/agents/README.md)를 참조하세요.

Codex에는 `ywc-*` skill을 보완하는 **7개**의 read-only specialist agent가 포함됩니다. `~/.codex/agents/`에 설치됩니다.

| Agent | 용도 | Sandbox |
|-------|------|---------|
| `ywc-architect` | 아키텍처 결정 및 트레이드오프 advisor | `read-only` |
| `ywc-security-engineer` | 정적 보안 리뷰 및 threat model 분류 | `read-only` |
| `ywc-root-cause-analyst` | 근본 원인 및 장애 원인 분석 | `read-only` |
| `ywc-performance-engineer` | 성능 리뷰 및 프로파일링 권장사항 | `read-only` |
| `ywc-typescript-reviewer` | TypeScript / JavaScript 언어별 리뷰 | `read-only` |
| `ywc-python-reviewer` | Python 언어별 리뷰 | `read-only` |
| `ywc-go-reviewer` | Go 언어별 리뷰 | `read-only` |

자세한 내용은 [README.md](README.md)를 참조하세요.
