# ywc-agent-toolkit

> 이 문서는 현재 번역 중입니다. 전체 문서는 [English](README.md) 를 참조하세요.
>
> 번역에 기여하고 싶으신 분은 [Translation Issue](../../issues/new?template=translation.md) 를 작성해 주세요.

---

Claude Code 및 Codex 용 개발 워크플로우 자동화 스킬 모음입니다.
계획 수립, 사양서 작성, 태스크 분해, 코드 생성, 리뷰, 릴리스까지 전 과정을 지원합니다.

현재 Claude Code skill 36개, Codex skill 37개, Claude Code agent 12개, Codex custom agent 7개를 제공합니다.

## 설치

### Claude Code 플러그인 마켓플레이스 (권장)

```bash
# 마켓플레이스 소스 추가 (최초 1회)
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

명령 실행 후 Plugin UI의 **Marketplaces** 탭에서 **ywc-agent-toolkit**을 설치하세요.
클론이나 bash 없이 `~/.claude/skills/`에 자동 설치됩니다.

### bash 스크립트

```bash
git clone https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit

# Claude Code
bash scripts/install.sh --cc

# Codex
bash scripts/install.sh --codex

# 양쪽 모두
bash scripts/install.sh --all
```

자세한 내용은 [README.md](README.md) 를 참조하세요.

---

## Review Skill HTML 출력 모드

8개의 Review / Report skill이 opt-in `--format html` flag를 지원합니다. 이 flag는 Markdown 대신 브라우저에서 바로 열리는 self-contained HTML report를 생성합니다.

**지원 Skill:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`

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
