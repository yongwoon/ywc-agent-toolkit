# ywc-agent-toolkit

> 이 문서는 현재 번역 중입니다. 전체 문서는 [English](README.md) 를 참조하세요.
>
> 번역에 기여하고 싶으신 분은 [Translation Issue](../../issues/new?template=translation.md) 를 작성해 주세요.

---

Claude Code 및 Codex 용 개발 워크플로우 자동화 스킬 모음입니다. 계획 수립, 사양서 작성, 태스크 분해, 코드 생성, 리뷰, 릴리스까지 전 과정을 지원합니다.

[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [Español](README.es.md)

> 📖 **[문서 & 가이드북](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/)** — 이 README는 짧은 소개입니다. 사전 요구사항, 설치, 전체 skill reference, 단계별 워크플로우 안내는 가이드북에 있습니다.

| 찾으시는 내용 | 가이드북 페이지 |
| ------------- | --------------- |
| 5분 만에 첫 기능 출시하기 | [03. 빠른 시작](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/03-quickstart/) |
| 어떤 skill을 어떤 순서로 실행할지 | [17. 전체 Skill Reference](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/14-skill-reference/) |
| 사전 요구사항, 설치 경로, 환경변수 | [18. 사전 요구사항 및 설치](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/15-prerequisites-installation/) |
| 소규모 변경 / 다중 태스크 / 자율 루프 | [04](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/04-general-cycle-small/) · [05](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/05-general-cycle-medium-large/) · [06](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/06-agentic-autonomous-loop/) |

## 지원 도구

| 도구        | Skills | Custom Agents | 설치 경로                                 |
| ----------- | ------ | ------------- | ---------------------------------------- |
| Claude Code | 42     | 12            | `~/.claude/skills/`, `~/.claude/agents/` |
| Codex       | 52     | 8             | `~/.codex/skills/`, `~/.codex/agents/`   |

---

## 빠른 시작

### Claude Code

플러그인 마켓플레이스로 설치합니다 — clone도, 사전 요구사항도 필요하지 않습니다:

```bash
/plugin marketplace add yongwoon/ywc-agent-toolkit    # 1. 소스 등록
/plugin install ywc-agent-toolkit@ywc-agent-toolkit   # 2. 플러그인 설치
```

`marketplace add`는 소스를 등록할 뿐이므로, 이어서 `/plugin install`을 실행하시거나 Plugin UI의 **Marketplaces** 탭에서 설치하셔야 합니다. 설치 후 Claude Code를 재시작하면 skill이 나타납니다.

### Codex

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit   # 1. 소스 등록
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit      # 2. 플러그인 설치
```

이미 마켓플레이스를 추가하신 경우에는 `codex plugin marketplace upgrade ywc-agent-toolkit`으로 Git 스냅샷을 먼저 갱신하시기 바랍니다. `codex` 실행 후 `/plugins`에서 **YWC Agent Toolkit** 탭을 통해 설치하실 수도 있습니다.

**Codex App**을 사용하시는 경우, 사이드바에서 **Plugins**를 열고 **YWC Agent Toolkit** 소스를 선택한 뒤, 소스가 `yongwoon/ywc-agent-toolkit`인지 확인하고 플러그인 상세 화면에서 설치하시면 됩니다.

### 이후 skill 실행

두 도구 모두 동일한 명령을 제공합니다:

```bash
/ywc-onboard-repo           # 낯선 코드베이스를 몇 분 만에 파악
/ywc-plan                   # 러프한 아이디어를 plan 또는 spec으로
/ywc-debug-rootcause        # 버그의 근본 원인 추적
/ywc-impl-review            # spec / 보안 / 품질 관점의 코드 리뷰
/ywc-agentic                # goal 하나로 전체 pipeline 자율 실행
```

→ 사전 요구사항, bash 스크립트 fallback, 설치 경로, `CLAUDE_SKILLS_DIR` / `CLAUDE_AGENTS_DIR` / `CODEX_HOME` 재정의는 [사전 요구사항 및 설치](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/15-prerequisites-installation/)를 참조하세요.

### 가이드북에서 다루지 않는 설치 옵션

```bash
# 특정 skill만 설치
bash scripts/install.sh --cc ywc-plan ywc-commit ywc-create-pr
bash scripts/install.sh --codex ywc-plan ywc-commit ywc-ui-ux-review

# 선택한 agent만 설치하거나, agent 없이 skill만 설치
bash scripts/install.sh --cc-agents ywc-backend-coder ywc-qa-engineer
bash scripts/install.sh --cc --skip-agents
```

### Codex 출력 언어 기본값

Codex 전용 `ywc-setup`은 Codex `ywc-*` skill의 artifact 언어 기본값을 설정합니다:

```bash
ywc-setup --scope project --lang ko
ywc-setup --scope user --lang ja
```

Resolution 순서는 explicit `--lang` > project `.codex/ywc.json` > project guidance(`AGENTS.md` / `CODEX.md` / `CLAUDE.md`) > user `~/.codex/ywc.json` > 사용자 질문입니다. Session default는 지원하지 않습니다.

---

## Skills

대부분의 `ywc-*` skill은 Claude Code와 Codex 양쪽에서 사용 가능합니다. 목적별로 정리된 전체 카탈로그는 [전체 Skill Reference](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/14-skill-reference/)에 있습니다. 여기서 시작하세요:

| 목적 | Skills |
| ---- | ------ |
| 아이디어를 plan 또는 spec으로 | [`ywc-plan`](claude-code/skills/ywc-plan/README.md) → [`ywc-spec-writer`](claude-code/skills/ywc-spec-writer/README.md) |
| 낯선 코드베이스 파악 | [`ywc-onboard-repo`](claude-code/skills/ywc-onboard-repo/README.md) |
| 의존성 안전한 task로 분해 | [`ywc-task-generator`](claude-code/skills/ywc-task-generator/README.md) |
| task를 end-to-end로 구현 | [`ywc-sequential-executor`](claude-code/skills/ywc-sequential-executor/README.md) / [`ywc-parallel-executor`](claude-code/skills/ywc-parallel-executor/README.md) |
| goal에서 전체 pipeline 실행 | [`ywc-agentic`](claude-code/skills/ywc-agentic/README.md) |
| 버그의 근본 원인 찾기 | [`ywc-debug-rootcause`](claude-code/skills/ywc-debug-rootcause/README.md) |
| 코드 품질 및 보안 리뷰 | [`ywc-impl-review`](claude-code/skills/ywc-impl-review/README.md), [`ywc-security-audit`](claude-code/skills/ywc-security-audit/README.md) |
| PR 생성 및 리뷰 코멘트 대응 | [`ywc-create-pr`](claude-code/skills/ywc-create-pr/README.md) → [`ywc-handle-pr-reviews`](claude-code/skills/ywc-handle-pr-reviews/README.md) |
| QA 테스트 시트 생성 | [`ywc-gen-testcase`](claude-code/skills/ywc-gen-testcase/README.md) |
| 릴리스 노트 작성 | [`ywc-release-pr-list`](claude-code/skills/ywc-release-pr-list/README.md) + [`ywc-changelog-release-notes`](claude-code/skills/ywc-changelog-release-notes/README.md) |
| 새 `ywc-*` skill 작성 | [`ywc-skill-author`](claude-code/skills/ywc-skill-author/README.md) |

모든 skill 디렉터리는 [`claude-code/skills/`](claude-code/skills)와 [`codex/skills/`](codex/skills)에서 확인하실 수 있으며, 각각 자체 README를 가지고 있습니다.

**연결 관계:** `ywc-plan` → (Medium/Large) `ywc-spec-writer` → `ywc-spec-ready` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor`가 각 task를 end-to-end로 전달합니다. Ad-hoc 변경은 executor를 건너뛰고 `ywc-create-pr` → `ywc-handle-pr-reviews`로 진행합니다. 각 경로의 명령과 flag는 [핵심 pipeline 가이드](https://yongwoon.github.io/ywc-agent-toolkit-lp/ko/guidebook/02-core-concepts/)에서 다룹니다.

### HTML 출력 모드

9개의 Review / Report skill이 `--format html` flag를 지원하며, Markdown 대신 브라우저에서 바로 열리는 self-contained HTML report를 생성합니다. 색상, severity coding, tab, 인터랙티브 control을 더해 결과물을 받는 사람이 실제로 읽고 행동하게 만듭니다.

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # localStorage sign-off가 포함된 인터랙티브 테스트시트
```

> **⚠️ Token 비용** — HTML 출력은 Markdown 대비 output token을 2~4배 사용합니다. 기본값은 `markdown`이며, 사람이 브라우저에서 읽을 report에 한해 활성화하시기 바랍니다.

지원 skill 목록과 상세: [`references/html-output.md`](claude-code/skills/references/html-output.md).

---

## Custom Agent

Claude Code에는 worker, reviewer, specialist dispatch용 12개의 custom agent가 포함되어 있습니다. `~/.claude/agents/`에 설치되며, 자세한 내용은 [`claude-code/agents/README.md`](claude-code/agents/README.md)를 참조하세요.

Codex에는 이에 대응하는 read-only specialist agent 7개가 `~/.codex/agents/`(`CODEX_HOME`으로 재정의 가능)에 agent당 TOML 파일 하나씩 설치됩니다:

| Agent | 용도 |
| ----- | ---- |
| [`ywc-architect`](claude-code/agents/ywc-architect.md) | 아키텍처 결정 및 트레이드오프 advisor |
| [`ywc-security-engineer`](claude-code/agents/ywc-security-engineer.md) | 정적 보안 리뷰 및 threat model 분류 |
| [`ywc-root-cause-analyst`](claude-code/agents/ywc-root-cause-analyst.md) | 근본 원인 및 장애 원인 분석 |
| [`ywc-performance-engineer`](claude-code/agents/ywc-performance-engineer.md) | 성능 리뷰 및 프로파일링 권장사항 |
| [`ywc-typescript-reviewer`](claude-code/agents/ywc-typescript-reviewer.md) | TypeScript / JavaScript 언어별 리뷰 |
| [`ywc-python-reviewer`](claude-code/agents/ywc-python-reviewer.md) | Python 언어별 리뷰 |
| [`ywc-go-reviewer`](claude-code/agents/ywc-go-reviewer.md) | Go 언어별 리뷰 |

모든 Codex agent는 read-only이며 파일을 편집하지 않습니다. 표준화된 `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`와 간결한 finding, 그리고 호출자가 적용하거나 확인해야 할 때 `Next action:`을 반환합니다. 원본 TOML은 [`codex/agents/`](codex/agents/)에 있습니다.

---

## Claude Code Hooks

Claude Code tool 호출 전후에 실행되는 자동화 hook입니다. `~/.claude/hooks/`(전역) 또는 `./.claude/hooks/`(프로젝트 로컬)에 설치되며 `settings.json`에 자동 등록됩니다. `jq`와 `uv`가 필요합니다.

```bash
bash scripts/install.sh --hooks                    # 전체 hook을 전역 설치
bash scripts/install.sh --hooks --local            # 현재 프로젝트에 설치
bash scripts/install.sh --hooks cost-tracker       # 특정 hook만 설치
bash scripts/install.sh --list --hooks             # 사용 가능한 hook 목록
```

| Hook                        | Event                  | 설명                                                                    |
| --------------------------- | ---------------------- | ----------------------------------------------------------------------- |
| `block-dangerous-commands`  | `PreToolUse`           | 위험한 shell 명령 차단(critical/high/strict 레벨)                        |
| `check-claude-md-freshness` | `PreToolUse`           | `git push` 전 CLAUDE.md 최신 여부 확인                                   |
| `cost-tracker`              | `PostToolUse` + `Stop` | tool 호출 통계를 기록하고 종료 시 세션 요약 출력                          |
| `notify-permission`         | `Notification`         | 권한 대기 시 Slack 알림 전송(`CCH_SLA_WEBHOOK` 필요)                     |
| `permission-request`        | `PermissionRequest`    | 안전한 tool(Read, Write, Edit) 자동 승인                                 |
| `protect-secrets`           | `PreToolUse`           | `.env`, SSH 키 등 시크릿 파일 접근 차단                                  |
| `session-start`             | `SessionStart`         | 세션 시작 시 git status, `CONTEXT.md`, TODO, GitHub Issue 주입           |

hook별 사용법: [`claude-code/hooks/README.md`](claude-code/hooks/README.md).

---

## 기여하기

기여를 환영합니다. PR 제출 전 [CONTRIBUTING.md](CONTRIBUTING.md)를 읽어주세요.

- **버그 리포트 및 skill 개선**: issue 또는 PR을 열어주세요
- **새 skill**: [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md) 가이드라인을 따라주세요
- **번역**: [번역 가이드](CONTRIBUTING.md#translations)를 참조하세요
- **Codex 패키지 동기화**: [Codex skill 유지보수 workflow](CONTRIBUTING.md#maintainer-workflow-for-codex-skills)를 참조하세요

## License

MIT
