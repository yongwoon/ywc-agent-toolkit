# Codex Custom Agents

이 디렉터리는 portable `ywc-*` skills를 보완하는 Codex custom agent 정의를 담습니다.

이 파일들은 `scripts/install.sh --codex` 실행 시 skills와 함께
`${CODEX_HOME:-~/.codex}/agents`에 설치됩니다. Agents만 설치하려면
`scripts/install.sh --codex-agents`를 사용합니다.

## 포함 Agents

| Agent | 목적 | Sandbox |
| --- | --- | --- |
| `ywc-architect` | Architecture 결정과 trade-off 자문 | `read-only` |
| `ywc-security-engineer` | Static security review와 threat-model triage | `read-only` |
| `ywc-root-cause-analyst` | Root-cause와 incident-cause 분석 | `read-only` |
| `ywc-performance-engineer` | Performance review와 profiling 권고 | `read-only` |
| `ywc-cloud-engineer` | Terraform 기반 IaC reliability와 misconfiguration review | `read-only` |
| `ywc-typescript-reviewer` | TypeScript / JavaScript 언어별 review | `read-only` |
| `ywc-python-reviewer` | Python 언어별 review | `read-only` |
| `ywc-go-reviewer` | Go 언어별 review | `read-only` |

## 작성 Notes

- 이 파일들은 TOML 형식을 유지합니다. Codex는 파일 하나당 custom agent 하나를 로드합니다.
- 필수 필드는 `name`, `description`, `developer_instructions`입니다.
- Specialist agents는 명시적인 구현 역할과 제한된 edit contract가 있는 경우가 아니면 `read-only`로 유지합니다.
- `tools`, `permissionMode`, `Task(subagent_type=...)` 같은 Claude Code 전용 필드를 Codex TOML에 복사하지 않습니다.
- Codex CLI `0.144.0` 이상에서는 GPT-5.6 Terra profile을 설치합니다. 더 이전 버전이거나 버전을 확인할 수 없으면 installer가 agent 복사본의 model만 GPT-5.4로 낮춰 설치합니다.
- Skills는 모델을 직접 고정하지 않습니다. 이 agent profile은 specialist delegation에만 적용되며, 일반 skill 실행은 호출한 Codex 세션의 model과 reasoning effort를 따릅니다.
