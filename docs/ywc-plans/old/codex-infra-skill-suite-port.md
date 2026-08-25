# Codex Infra Skill Suite Port

> Status: Draft
> Scale: Large
> Created: 2026-07-08
> Author: Codex
> Spec Reference: `docs/ywc-plans/infra-skill-suite-design.md`

## Operative Sections

- Base spec body remains authoritative except where explicitly superseded by `## Iteration 1 Amendments`.
- `## Iteration 1 Amendments` supersedes the original write-enabled `ywc-cloud-engineer` worker concept with a Codex-compatible read-only specialist agent.
- `## Iteration 1 Amendments` also closes README locale scope and eval-scope decisions so `ywc-task-generator` can decompose a fixed v1 target.

## Purpose

`docs/ywc-plans/infra-skill-suite-design.md`는 Claude Code 기준으로 인프라 스킬 스위트의 구조를 정의하고 있다. 이 저장소에는 이미 Codex용 `ywc-*` 스킬과 custom agent 배포 구조가 있으므로, 동일한 의도를 Codex 번들 규약에 맞게 포팅하는 별도 구현 계획이 필요하다.

이번 작업의 목적은 Codex 번들에 인프라 설계, Terraform 작성, 인프라 리뷰, 인프라 최적화까지 연결되는 스킬 스위트를 추가하고, 이를 뒷받침하는 공용 reference와 infra 전용 worker agent를 함께 도입하는 것이다. 결과물은 `ywc-plan` 이후 `ywc-spec-validate`와 `ywc-task-generator`로 바로 분해 가능한 수준의 구현 스펙이어야 한다.

## Scope

- Codex용 신규 skill 4종을 추가한다.
- `ywc-infra-design`
- `ywc-iac-author`
- `ywc-infra-review`
- `ywc-infra-optimize`
- Codex용 신규 custom agent `codex/agents/ywc-cloud-engineer.toml`을 추가한다.
- Codex 공용 infra reference 집합을 `codex/skills/references/infra/` 아래에 추가한다.
- Terraform 단일 도구 기준으로 provider/lens/reference 구조를 Codex 번들용으로 재구성한다.
- 기존 Codex agent `ywc-security-engineer`와 `ywc-performance-engineer`의 설명 또는 지시문을 infra use case까지 수용하도록 확장한다.
- 각 신규 skill에 대해 `SKILL.md`, `agents/openai.yaml`, Tier 1 README 4종, 필요 시 Tier 2 README 2종을 준비한다.
- `plugins/ywc-agent-toolkit/skills/` 동기화와 `bash scripts/validate.sh` 통과를 최종 완료 기준에 포함한다.

## Out of Scope

- `claude-code/**` 아래의 기존 스킬 본문이나 agent를 이번 Codex 포트 작업에서 수정하지 않는다.
- Terraform 외의 IaC 도구인 CDK, Pulumi, CloudFormation, Bicep 전용 reference 또는 skill 분기를 이번 범위에 넣지 않는다.
- 실제 클라우드 계정에 apply 하는 실행 자동화는 넣지 않는다.
- `wrangler`, `cloudflare`, 앱 배포형 skill과 섞어서 범위를 확장하지 않는다.
- 인프라 스킬 출시 후의 eval 체계 신설이나 외부 benchmark 설계는 별도 작업으로 남긴다.

## Existing Constraints Touched

| Existing artifact | Behavior verified by reading the file | New code's interaction |
|---|---|---|
| `AGENTS.md:5` | Codex skill은 `codex/skills/<skill-name>/`에 위치하고, Tier 1 README 4종과 `agents/openai.yaml`이 필수다. | 신규 infra skill 4종 모두 이 구조를 그대로 따라야 한다. |
| `AGENTS.md:5` | Shared Codex material은 `codex/skills/references/` 또는 `codex/skills/scripts/`에 둬야 한다. | provider/lens/Terraform 공용 문서는 skill별 중복 대신 `codex/skills/references/infra/`로 중앙화한다. |
| `AGENTS.md:20` | Codex `SKILL.md` frontmatter는 `name`과 `description`만 허용한다. | Claude 설계안의 `category`, `phase`, `requires`, `advisor_budget`는 Codex 포트에서 본문으로만 표현하고 frontmatter에는 넣지 않는다. |
| `AGENTS.md:24` | 신규/수정 skill은 required locale README와 `agents/openai.yaml` 메타데이터 점검이 필요하다. | 계획의 완료 정의에 locale README와 YAML 생성을 포함한다. |
| `codex/AGENTS.md:7` | Codex skills는 flat 구조의 `codex/skills/<skill-name>/`가 source of truth다. | 신규 infra skill은 모두 이 경로에 직접 생성하고 generated plugin은 후속 sync로만 갱신한다. |
| `codex/AGENTS.md:9` | Codex custom agent는 `codex/agents/*.toml` 한 파일 단위다. | `ywc-cloud-engineer`는 Claude markdown agent가 아니라 TOML agent로 설계해야 한다. |
| `codex/AGENTS.md:12` | `plugins/ywc-agent-toolkit/skills/`는 generated package이며 직접 수정하면 안 된다. | 구현 순서를 source 편집 → plugin sync → validate로 고정한다. |
| `codex/AGENTS.md:23` | Codex plugin 동기화 명령은 `bash scripts/sync-codex-plugin.sh`다. | 신규 skill 4종 추가 후 반드시 sync를 실행한다. |
| `codex/AGENTS.md:24` | Codex 최종 검증 명령은 `bash scripts/validate.sh`다. | 최종 Verification과 Acceptance Criteria에 이 명령을 포함한다. |
| `scripts/validate.sh:47` | Codex skill은 `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`가 누락되면 실패한다. | 신규 infra skill마다 Tier 1 README 4종을 필수 산출물로 취급한다. |
| `scripts/validate.sh:55` | Codex skill은 `agents/openai.yaml`의 `interface.display_name`, `short_description`, `default_prompt`를 검사한다. | 신규 infra skill마다 OpenAI YAML 인터페이스 값을 생성하고 검증해야 한다. |
| `scripts/validate.sh:88` | Claude 전용 frontmatter 필드가 남아 있으면 Codex validation이 실패한다. | Claude 설계안 복사 시 frontmatter strip이 구현 체크리스트의 명시 항목이 된다. |
| `scripts/validate.sh:97` | `codex/skills/references`와 `codex/skills/scripts`는 validator가 공유 자산 루트로 본다. | infra 공용 reference를 이 루트 아래에 두고, SKILL.md에서는 상대 경로로 참조한다. |
| `scripts/validate.sh:112` | skill 본문이 참조하는 `../references/*`는 실제 shared reference 파일로 존재해야 한다. | 공용 infra reference 파일명과 SKILL.md 링크를 일치시켜 dangling reference를 방지한다. |
| `scripts/sync-codex-plugin.sh:5` | plugin sync는 `codex/skills`만 source로 복사한다. | shared reference와 skill 본문은 모두 `codex/skills` 아래에 있어야 plugin 패키지로 반영된다. |
| `scripts/sync-codex-plugin.sh:77` | sync는 generated package에서 `bash codex/skills/...` 같은 source 경로를 설치 경로로 rewrite한다. | skill 문서의 예시 명령은 source tree 기준으로 적어도 packaging 시 안전하게 rewrite되도록 유지한다. |
| `codex/agents/README.md:16` | 기존 specialist agent는 대부분 `read-only` 자문 역할이다. | `ywc-cloud-engineer`는 예외적으로 write-enabled worker로 추가하되 역할 경계를 명확히 해야 한다. |
| `codex/agents/ywc-architect.toml:1` | 아키텍처 판단용 read-only advisor가 이미 존재한다. | `ywc-infra-design`은 모호한 설계 분기에서 `ywc-architect`와 충돌하지 않도록 역할 분리를 명시한다. |
| `codex/agents/ywc-security-engineer.toml:1` | security agent는 bounded static review 전용이다. | `ywc-infra-review`는 인프라 misconfiguration lens로 이 agent를 호출하되 apply/author 역할은 넘기지 않는다. |
| `scripts/validate.sh:539` | 모든 `codex/agents/*.toml`은 `sandbox_mode = "read-only"`를 유지해야 한다. | 신규 `ywc-cloud-engineer`는 write-enabled worker가 아니라 read-only specialist로 정의해야 validator를 통과한다. |
| `CONTRIBUTING.md:119` | Codex custom agent는 read-only를 유지하고 bounded specialist mission만 가져야 한다. | 신규 infra agent는 advisory/review mission으로 제한하고 파일 쓰기 책임은 skill 본체에 둔다. |

> ⚠️ PARTIALLY SUPERSEDED by Iteration 1 — see §iteration-1-amendments for AC6, AC9, AC10, and AC11 scope clarifications.

## Acceptance Criteria

- [ ] **AC1 - 신규 Codex infra skill 4종이 source tree에 존재한다**: `find codex/skills -maxdepth 1 -type d | rg 'ywc-(infra-design|iac-author|infra-review|infra-optimize)$'`가 네 디렉터리를 모두 찾는다.
- [ ] **AC2 - 각 skill의 필수 파일 세트가 완비된다**: 각 신규 skill 디렉터리에 `SKILL.md`, `agents/openai.yaml`, `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`가 존재한다.
- [ ] **AC3 - Codex frontmatter 규칙을 지킨다**: `rg -n '^(category|phase|requires|advisor_budget|allowed tools):' codex/skills/ywc-infra-*/*`가 매치되지 않는다.
- [ ] **AC4 - 공용 infra reference가 중앙화된다**: `codex/skills/references/infra/` 아래에 provider 4종, lens 3종, Terraform reference가 존재하고, 신규 skill 본문은 이를 상대경로로 참조한다.
- [ ] **AC5 - Terraform 단일 전략이 명시된다**: `rg -n 'Terraform 단일|Terraform only|terraform validate|terraform plan' codex/skills/ywc-iac-author codex/agents/ywc-cloud-engineer.toml codex/skills/references/infra`가 일관된 단일 도구 전략을 보여준다.
- [ ] **AC6 - 신규 cloud engineer agent가 추가된다**: `codex/agents/ywc-cloud-engineer.toml`이 존재하고 역할 설명이 IaC 작성/수정, validate/plan, reliability review 범위를 포함한다.
- [ ] **AC7 - 기존 specialist agent 확장이 반영된다**: `codex/agents/ywc-security-engineer.toml`과 `codex/agents/ywc-performance-engineer.toml` 중 최소 description 또는 developer instructions가 infra review/cost lens use case를 언급한다.
- [ ] **AC8 - skill 간 anti-trigger 경계가 명시된다**: 신규 skill 4종의 `SKILL.md` description 또는 본문에 설계/작성/리뷰/최적화 경계와 `ywc-docker-isolate` 비대상 조건이 드러난다.
- [ ] **AC9 - README locale 세트가 본문 의미와 정합하다**: Tier 1 README 4종이 신규 skill의 purpose, 사용 시점, related skill을 동일한 구조로 설명한다.
- [ ] **AC10 - plugin package가 sync된다**: `bash scripts/sync-codex-plugin.sh` 후 `plugins/ywc-agent-toolkit/skills/`에 신규 infra skill 4종이 반영된다.
- [ ] **AC11 - 전체 validation이 통과한다**: `bash scripts/validate.sh` exit code가 0이다.
- [ ] **AC12 - Codex-only boundary를 지킨다**: 구현 diff에 `claude-code/skills/ywc-infra-*` 또는 `claude-code/agents/ywc-cloud-engineer.md`가 포함되지 않는다.

## Functional Requirements

### FR-1: Codex용 infra taxonomy를 신규 skill 4종으로 포트한다

Claude 설계안의 네 축을 Codex에도 동일하게 유지한다.

- `ywc-infra-design`: 클라우드/쿠버네티스 아키텍처 설계와 trade-off 기록
- `ywc-iac-author`: Terraform 중심 IaC 작성과 plan 기반 blast-radius 요약
- `ywc-infra-review`: security/cost/reliability lens 기반 인프라 리뷰
- `ywc-infra-optimize`: drift, right-sizing, unused resources, reliability hardening 실행 계획

각 skill의 description은 trigger 문구와 anti-trigger 문구를 포함해야 하며, Codex 규약에 맞춰 frontmatter에는 `name`과 `description`만 둔다.

### FR-2: Claude 전용 reference 구조를 Codex 공용 reference 구조로 재배치한다

`docs/ywc-plans/infra-skill-suite-design.md`의 shared provider architecture를 Codex 번들용으로 다음처럼 중앙화한다.

- `codex/skills/references/infra/providers/aws.md`
- `codex/skills/references/infra/providers/gcp.md`
- `codex/skills/references/infra/providers/azure.md`
- `codex/skills/references/infra/providers/k8s.md`
- `codex/skills/references/infra/lenses/security.md`
- `codex/skills/references/infra/lenses/cost.md`
- `codex/skills/references/infra/lenses/reliability.md`
- `codex/skills/references/infra/iac/terraform.md`

신규 skill들은 provider 확정 후 해당 reference 1개만 읽도록 Progressive Disclosure를 유지한다. 동일한 provider/lens 내용을 skill별 `references/`로 복제하지 않는다.

> ⚠️ SUPERSEDED by Iteration 1 — see §iteration-1-amendments.

### FR-3: `ywc-cloud-engineer` custom agent를 Codex worker로 추가한다

신규 agent `codex/agents/ywc-cloud-engineer.toml`은 기존 read-only specialist와 달리 IaC 작성/수정용 worker다. 최소 요구사항은 다음과 같다.

- Mission: Terraform 기반 인프라 코드 작성/수정, `terraform validate`, `terraform plan`, reliability lens review
- Boundary: 앱 비즈니스 로직, 순수 아키텍처 의사결정, 일반 보안 정적분석은 담당하지 않음
- Output contract: `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` + 변경 요약 + 다음 행동
- Provider scope: AWS, GCP, Azure, Kubernetes/Helm을 Terraform provider 관점으로 다룸

Codex TOML 형식과 기존 agent 문체를 따라야 하며, Claude agent 문법을 복사하지 않는다.

### FR-4: 기존 specialist agent를 infra review 흐름에 맞게 확장한다

`ywc-infra-review`의 3-lens 구조가 실질적으로 작동하도록 다음 조정을 한다.

- `ywc-security-engineer`: IaC misconfiguration, IAM/RBAC over-privilege, public exposure, secrets-in-state 맥락을 처리 가능하도록 설명 강화
- `ywc-performance-engineer`: FinOps, right-sizing, reserved/spot, transfer cost, idle resource 탐지 맥락을 처리 가능하도록 설명 강화

이 변경은 기존 agent의 주 역할을 깨지 않으면서 infra use case를 수용하는 수준이어야 한다.

### FR-5: 각 skill에 Codex용 UI metadata와 locale README를 추가한다

신규 skill마다 다음을 생성한다.

- `agents/openai.yaml` with `display_name`, `short_description`, `default_prompt`
- `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`
- 기존 관례상 중국어/스페인어 문서를 함께 shipping할지 여부를 결정하고, 생성한다면 `README.zh.md`, `README.es.md`도 동기화한다

README는 사용자용 설명이고 `SKILL.md`는 에이전트용 instructions라는 역할 구분을 유지한다.

### FR-6: 신규 skill 간 dispatch 경계와 anti-trigger를 Codex 스타일로 명시한다

각 skill은 다음 라우팅 원칙을 본문에 포함한다.

- `ywc-infra-design`은 토폴로지/서비스 선택/예산/가용성 설계를 맡고, 실제 Terraform 작성은 `ywc-iac-author`로 넘긴다.
- `ywc-iac-author`는 설계 입력을 기반으로 Terraform 코드를 작성하고, 완료 후 `ywc-infra-review`를 권유한다.
- `ywc-infra-review`는 security/cost/reliability lens fan-out을 수행하고, CRITICAL/HIGH 결과는 apply 차단 권고를 내린다.
- `ywc-infra-optimize`는 SAFE/CAUTION/DANGER 분류 기반으로 보수적으로 실행한다.
- `ywc-docker-isolate`는 local worktree 포트 충돌 전용이므로 모든 신규 skill에서 anti-trigger로 명시한다.

### FR-7: plugin sync 및 validator 친화적인 rollout 순서를 제공한다

구현 순서는 다음을 기준으로 한다.

1. `ywc-cloud-engineer` agent 추가
2. 공용 infra references 추가
3. `ywc-iac-author`
4. `ywc-infra-design`
5. `ywc-infra-review`
6. `ywc-infra-optimize`
7. 기존 specialist agent 확장
8. plugin sync
9. validation

이 순서는 worker와 reference가 먼저 준비되어 downstream skill 본문에서 안정적으로 참조 가능하도록 만든다.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Compatibility | 신규 Codex skill은 기존 validator와 install flow를 깨지 않아야 한다. |
| Maintainability | provider/lens 문서는 skill별 복제가 아니라 shared reference로 유지한다. |
| Clarity | `SKILL.md`는 concise하게 유지하고 provider 세부는 reference 파일로 분리한다. |
| Safety | skill 본문은 실제 클라우드 apply를 기본 동작으로 요구하지 않고 validate/plan/review 중심으로 설계한다. |
| Packaging | source tree와 generated plugin package가 `bash scripts/sync-codex-plugin.sh` 이후 정합해야 한다. |
| Localization | Tier 1 README 4종의 구조와 의미가 크게 어긋나지 않아야 한다. |

## Data Model

N/A - 애플리케이션 데이터 모델 변경은 없다.

## API Contract

N/A - 런타임 애플리케이션 API 계약 변경은 없다.

## Edge Cases

- **Claude 설계안의 frontmatter 오염**: Claude 스펙 예시에 있는 `category`, `phase`, `requires`, `advisor_budget`를 그대로 복사하면 `scripts/validate.sh`에서 실패한다.
- **공용 reference의 중복 배치**: skill별 `references/`와 `codex/skills/references/infra/`에 내용을 중복 저장하면 유지보수 비용이 급증하고 sync 후 diff noise가 커진다.
- **Terraform 외 IaC 도구 혼입**: `Pulumi`, `Bicep`, `CloudFormation` 등을 description이나 README 예시로 남기면 도구 전략이 흔들린다.
- **write-enabled worker의 과도한 역할 확장**: `ywc-cloud-engineer`가 아키텍처 자문이나 보안 전담까지 맡기 시작하면 기존 specialist agent 경계와 충돌한다.
- **plugin sync 누락**: source tree만 수정하고 generated package를 sync하지 않으면 validation이 stale plugin으로 실패한다.
- **locale README 미동기화**: `SKILL.md`만 완성하고 README locale이 비거나 의미가 어긋나면 validator 또는 후속 문서 검토에서 걸린다.

## Dependencies

- 기준 설계 문서: `docs/ywc-plans/infra-skill-suite-design.md`
- 저장소 규약: `AGENTS.md`, `codex/AGENTS.md`
- 검증 스크립트: `scripts/validate.sh`
- plugin sync 스크립트: `scripts/sync-codex-plugin.sh`
- 기존 specialist agent prior art:
  - `codex/agents/ywc-architect.toml`
  - `codex/agents/ywc-security-engineer.toml`
  - `codex/agents/ywc-performance-engineer.toml`
- `N/A — 외부 서비스 의존성은 구현 단계에서 추가되지 않음`

> ⚠️ SUPERSEDED by Iteration 1 — see §iteration-1-amendments.

## Open Questions

- [ ] `ywc-cloud-engineer`를 `read-write` worker로 둘 때, 기존 Codex agent 집합의 권한 모델과 충돌하지 않도록 어떤 최소 도구 세트를 허용할지 최종 문구를 정할 필요가 있다.
- [ ] 신규 infra skill에 `README.zh.md`, `README.es.md`를 첫 릴리스부터 포함할지, Tier 1만 먼저 ship할지 결정이 필요하다.
- [ ] `ywc-infra-review`의 cost/reliability lens를 위해 별도 eval fixture가 즉시 필요한지, 1차 포트에서는 문서/validation까지만 완료할지 결정이 필요하다.

## References

- [docs/ywc-plans/infra-skill-suite-design.md](/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/docs/ywc-plans/infra-skill-suite-design.md)
- [AGENTS.md](/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/AGENTS.md)
- [codex/AGENTS.md](/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/codex/AGENTS.md)
- [scripts/validate.sh](/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/scripts/validate.sh)
- [scripts/sync-codex-plugin.sh](/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/scripts/sync-codex-plugin.sh)

## Implementation Steps

1. 신규 infra skill/agent 이름과 책임 경계를 확정한다.
2. `codex/skills/references/infra/` 아래 공용 provider/lens/Terraform reference를 먼저 작성한다.
3. `codex/agents/ywc-cloud-engineer.toml`을 추가하고 기존 specialist agent 확장 범위를 결정한다.
4. `ywc-iac-author`를 먼저 작성해 worker와 reference 연결이 실제로 성립하는지 본다.
5. `ywc-infra-design`, `ywc-infra-review`, `ywc-infra-optimize`를 순서대로 추가한다.
6. 각 skill의 `agents/openai.yaml`과 README locale 세트를 채운다.
7. `bash scripts/sync-codex-plugin.sh`를 실행해 generated package를 동기화한다.
8. `bash scripts/validate.sh`와 필요한 install smoke test를 실행한다.
9. validation 결과에 따라 `ywc-spec-validate`와 `ywc-task-generator`로 후속 분해 또는 보정 작업을 진행한다.

## Iteration 1 Amendments

### Requirements Failed

- `codex/agents/*.toml`의 `sandbox_mode`는 validator가 `read-only`만 허용하는데, 원안은 `ywc-cloud-engineer`를 write-enabled worker로 정의했다.
- v1 산출물 범위에 `README.zh.md` / `README.es.md`와 eval fixture가 포함되는지 명시되지 않아 task 범위가 고정되지 않았다.

### Amended Approach

1. `ywc-cloud-engineer`는 v1에서 write-enabled worker가 아니라 read-only infra specialist agent로 구현한다.
   역할은 Terraform/IaC feasibility, reliability review, blast-radius sanity check, provider-specific advisory로 제한한다.
   실제 파일 작성과 수정은 `ywc-iac-author`를 수행하는 상위 Codex 세션이 담당한다.
   TOML은 기존 specialist agent와 동일하게 `sandbox_mode = "read-only"`를 사용하고, bounded mission + `Next action:` 출력 계약을 따른다.

2. v1 문서 범위는 Tier 1 README 4종으로 고정한다.
   `README.zh.md`와 `README.es.md`는 첫 포트 범위에서 제외한다.
   번역 롤아웃은 follow-up docs/i18n 작업으로 분리한다.

3. v1 포트 범위에서는 신규 eval fixture를 필수로 요구하지 않는다.
   구현 완료 기준은 skill/agent/source package/plugin sync/validator 통과까지로 한정한다.
   eval 추가는 follow-up quality 작업으로 분리한다.

4. agent 카탈로그와 install smoke test를 명시 산출물에 추가한다.
   `codex/agents/README.md`에 `ywc-cloud-engineer`를 추가한다.
   검증에는 `bash scripts/install.sh --list --codex-agents`와 필요 시 `CODEX_HOME="$(mktemp -d)" bash scripts/install.sh --codex-agents`를 포함한다.

### Updated Acceptance Criteria for Affected Items

- **AC6 replacement**: `codex/agents/ywc-cloud-engineer.toml`이 존재하고 `sandbox_mode = "read-only"`이며, description/developer instructions가 Terraform/IaC advisory, reliability review, blast-radius sanity check 범위를 포함한다.
- **AC9 replacement**: 각 신규 skill에는 `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`가 존재하고, v1 범위에서는 `README.zh.md` / `README.es.md`를 요구하지 않는다.
- **AC10 replacement**: `bash scripts/sync-codex-plugin.sh` 후 plugin package에 신규 infra skill 4종이 반영되고, `codex/agents/README.md`에도 `ywc-cloud-engineer`가 목록화된다.
- **AC11 replacement**: `bash scripts/validate.sh`와 `bash scripts/install.sh --list --codex-agents`가 모두 성공한다.

### Additional Implementation Notes

- `Existing Constraints Touched`에 있는 `scripts/validate.sh:539`와 `CONTRIBUTING.md:119`를 infra agent 설계의 최상위 제약으로 취급한다.
- `ywc-infra-design`과 `ywc-infra-review`는 `ywc-cloud-engineer`를 read-only advisory fan-out 대상으로 사용하고, `ywc-iac-author`는 parent session write flow를 유지한다.
- `Out of Scope`에 "v1에서는 신규 eval fixture를 도입하지 않는다"를 추가 해석으로 적용한다.

### Updated Open Questions

N/A — none identified for v1 scope after the amendments above.
