# Codex Custom Agents

이 디렉터리는 portable `ywc-*` skills를 보완하는 Codex custom agent 정의를 담습니다.

Codex package inventory: 54 skills and 10 custom agents. See [codex/README.md](../README.md) for the full catalog and installation commands.

이 파일들은 `scripts/install.sh --codex` 실행 시 skills와 함께
`${CODEX_HOME:-~/.codex}/agents`에 설치됩니다. Agents만 설치하려면
`scripts/install.sh --codex-agents`를 사용합니다.

## 포함 Agents

| Agent | 목적 | Sandbox |
| --- | --- | --- |
| `ywc-architect` | Architecture 결정과 trade-off 자문 | `read-only` |
| `ywc-security-engineer` | Static security review와 threat-model triage | `read-only` |
| `ywc-root-cause-analyst` | Root-cause와 incident-cause 분석 | `read-only` |
| `ywc-performance-engineer` | Performance review, profiling 권고와 근거 기반의 bounded FinOps 비교 | `read-only` |
| `ywc-cloud-engineer` | Terraform 기반 IaC reliability와 misconfiguration review | `read-only` |
| `ywc-typescript-reviewer` | TypeScript / JavaScript 언어별 review | `read-only` |
| `ywc-python-reviewer` | Python 언어별 review | `read-only` |
| `ywc-go-reviewer` | Go 언어별 review | `read-only` |
| `ywc-complexity-cleaner` | Task-owned production complexity reduction | `workspace-write` |
| `ywc-test-hardener` | Task-owned test/fixture assertion hardening | `workspace-write` |

## 작성 Notes

- 이 파일들은 TOML 형식을 유지합니다. Codex는 파일 하나당 custom agent 하나를 로드합니다.
- 필수 필드는 `name`, `description`, `developer_instructions`입니다.
- Specialist agents는 명시적인 구현 역할과 제한된 edit contract가 있는 경우가 아니면 `read-only`로 유지합니다.
- `workspace-write`는 `ywc-complexity-cleaner.toml`과 `ywc-test-hardener.toml`에만 허용됩니다. Cleaner는 packet의 production Ownership만, Hardener는 packet의 test/fixture Ownership만 수정합니다.
- 두 worker 모두 완전한 Quality Gate Contract packet, immutable command ID/digest, sanitized evidence boundary를 요구하며, packet이 없거나 범위를 벗어나면 `NEEDS_CONTEXT`를 반환합니다.
- 두 worker 모두 raw command/output/transcript/secret/full diff를 보존하거나 반환하지 않으며, staging, commit, push, PR, merge, release, delivery 권한이 없습니다.
- Hardener의 시도 횟수는 최대 three attempts이며 residual survivor를 equivalent로 판정하지 않습니다. 상태 집계는 `BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`입니다.
- `tools`, `permissionMode`, `Task(subagent_type=...)` 같은 Claude Code 전용 필드를 Codex TOML에 복사하지 않습니다.
- Codex CLI `0.144.0` 이상에서는 GPT-5.6 Terra profile을 설치합니다. 더 이전 버전이거나 버전을 확인할 수 없으면 installer가 agent 복사본의 model만 GPT-5.4로 낮춰 설치합니다.
- Skills는 모델을 직접 고정하지 않습니다. 이 agent profile은 specialist delegation에만 적용되며, 일반 skill 실행은 호출한 Codex 세션의 model과 reasoning effort를 따릅니다.

## Root-cause analyst 계약

| Caller | analysis_mode | Inline evidence |
| --- | --- | --- |
| `ywc-debug-rootcause` | `debug_hypotheses` | 3–5개 ranked falsifiable 가설, 각각 찬반 근거; 한 번에 한 변수 실험 |
| `ywc-incident-postmortem` | `incident_five_whys` | 근거를 인용한 정확히 다섯 Why, primary cause와 contributing factors 분리 |
| `ywc-confidence-gate` | `confidence_root_cause` | 단일 cause candidate의 찬반 근거; 최종 band는 caller 소유 |

`Caller`와 `analysis_mode`를 명시하며 누락/unknown/mismatch는 추론 없이 `NEEDS_CONTEXT`입니다. 응답은 Status → Summary → Finding counts → 유효한 Analysis mode 순서이며 각 finding은 severity와 근거를 포함합니다. Caller는 owner/input/output/status 불일치를 `NEEDS_CONTEXT`로 처리하고 기존 판정 gate와 dispatch budget을 유지합니다. Analyst는 inline read-only이며 파일 작성, probe 실행, 최종 architecture 판정을 하지 않습니다.

Debug는 최소 feedback loop와 catches/misses를 먼저 기록합니다. 세 번의 fix 실패 후 기본 중단하며, 유효한 debug 응답의 별도 evidence-linked `Fix #4 signal: fix harder`와 `Next fix worth attempting: <one concrete minimal change>`가 모두 있을 때만 마지막 한 번을 허용합니다. 한 필드 누락·근거 없음·다른 mode·analyst 사용 불가는 중단을 유지하며, 네 번째 실패 후 추가 시도는 없습니다. 실제 runtime trace가 없으면 `UNVERIFIED — instruction contract only`입니다.

## Bounded FinOps 계약

`ywc-performance-engineer`는 단일 escalated FinOps finding과 Evidence Snapshot v1 performance slice를 받습니다. 입력은 finding ID/요약, resource/workload, 증거 출처·시각, 제공된 비용·사용량과 budget/constraints입니다. 제공된 근거로 option별 비용·risk trade-off와 권고를 inline으로 반환하며, 필수 근거 누락·truncation은 정확한 입력을 지목한 `NEEDS_CONTEXT`입니다. 가격·사용량·절약률을 추정하거나 provider/state/apply system 조회, apply, applied-environment sweep을 수행하지 않습니다. 보고서 파일은 caller/aggregator 소유입니다.

`ywc-infra-review`는 fresh plan/diff와 기존 scoped IaC를 구분하고, 기존 scope는 `evidence_type=state_backend|apply_record|applied_commit`, 정확한 `binding_target`, `applied=yes|no`의 one-time 사용자 attestation으로 입장을 결정합니다. 부적격 scoped-only 입력은 `BLOCKED`/reviewer 0회, 적격 binding의 content 누락은 `NEEDS_CONTEXT`/0회이며, 통과한 입력만 세 lens에 동일 전달합니다. 이는 사용자 attestation 계약이며 live runtime 근거가 없으면 `UNVERIFIED — instruction contract only`입니다.
