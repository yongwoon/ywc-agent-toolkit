# Spec: Claude Code Skill Eval — 격리 실행 Runner 와 Ablation

> Status: **Phase 0 완료 · PROCEED (88/100)** — 노선 N1 확정, `ywc-task-generator` 분해 가능
>
> **Operative Sections:** Amendment 가 원본보다 우선하며, **뒤 회차가 앞 회차보다 우선한다**.
> - `## Iteration 4 Amendments` — **최종 권위.** 노선 N1 확정과 Phase 0 종결, 실행 계약, §AC2″(귀속 한계), §Phase 5″(CI 2계층), §NFR1″(비용), Confidence Gate. catalog/workspace 격리 층위 구분을 도입한다.
> - `## Iteration 3 Amendments` — Phase 0 spike 결과. §AC1′, §Phase 2 확정 사항. 원본의 오염 규모(40여 개→**243개**)와 비용 전제를 정정한다. §AC2′·§NFR1′·Confidence Gate 는 Iteration 4 가 대체한다.
> - `## Iteration 2 Amendments` — §AC17′, §AC20′, Test Strategy 3행. `scripts/validate.sh` 사실 정정을 포함한다. Confidence Gate 는 Iteration 3 이 대체한다.
> - `## Iteration 1 Amendments` — 출력 계약(D1 총점 정직성 / D2 표기 / D3 아티팩트 경로), AC16·AC18·AC19, NFR1~3 에 대해 권위. 단 §AC17·AC20 과 Confidence Gate 는 Iteration 2 가 대체한다.
> - `⚠️ SUPERSEDED` 로 표시된 섹션은 이력용이다. `ywc-task-generator` 는 위 우선순위를 따른다.
>
> Scale: **Medium** — 신규 runner, fixture 스키마, S3 배선, CI 계층을 함께 변경
> Target evaluator: `.claude/skills/ywc-toolkit-eval/` (local-only, 배포 금지)
> Target bundle: `claude-code/skills`, `claude-code/agents`
> Counterpart: `docs/ywc-plans/codex-skill-eval-upgrade.md` — **계약의 원천**. Iteration 1~3 에서 확정된 결정은 재설계하지 않고 인용한다.
> Predecessor: `docs/ywc-plans/claude-skill-eval-upgrade.md` (Phase 1~3 완료 — 커밋 `d1748f3`, `a80b0e6`, `c864658`)

## Purpose

`ywc-toolkit-eval` 의 S3(Behavioral efficacy, weight 20)는 지금도 **SKILL.md 본문을 읽고** "이대로 하면 될 것 같은가"를 판정한다. Philipp Schmid 가이드 §2 의 "과정이 아닌 결과(Outcome) 중심 평가"와 정면으로 어긋나며, 실제로 측정되는 것은 문서 품질이지 skill 이 목표를 달성하는지가 아니다.

이 spec 은 skill/agent 를 **격리 환경에서 실제 실행**하고 산출물을 결정적으로 채점하는 runner 를 도입하여 S3 를 독해 기반에서 실행 기반으로 전환하고, with/without ablation 으로 은퇴 근거를 만든다.

## 선행 조건: 격리 수단이 미확정이다 (Phase 0 blocking)

Codex 측은 temporary `CODEX_HOME` 으로 격리를 확정했다. **claude-code 에는 대응물이 확인되지 않았다.** 조사 결과를 사실과 미확인으로 나눠 기록한다.

**확인된 사실 (VERIFIED)**

| 사실 | 근거 |
|---|---|
| 프로젝트 로컬 `.claude/skills/` 는 로드 경로다 | 본 세션에서 `.claude/skills/ywc-toolkit-eval` 이 Skill 목록에 노출됨 |
| `--output-format` 은 `text` / `json` / `stream-json` (`--print` 전용) | `claude --help:127-130` |
| `--disable-slash-commands` = "Disable all skills" | `claude --help` |
| `--plugin-dir <path>` 는 세션 한정으로 플러그인을 **추가** 로드한다 | `claude --help:136-139` |
| `--settings <file-or-json>` 은 **추가** 설정을 로드한다 ("load additional settings") | `claude --help:185-186` |
| `--agents <json>` 으로 custom agent 를 인라인 정의할 수 있다 | `claude --help` |
| `install.sh` 는 `CLAUDE_SKILLS_DIR` 로 설치 경로를 override 한다 (기본 `~/.claude/skills`) | `scripts/install.sh:33` |
| `plugins/ywc-agent-toolkit` 는 **Codex 전용** 플러그인이다 (`.codex-plugin/plugin.json`, `.claude-plugin/` 없음) | 디렉터리 확인 |
| 이 저장소에는 Python eval runner 인프라가 **전무**하다 | `scripts/` 는 bash; evaluator scripts 는 `score.py`/`test_score.py` 뿐 |
| Codex runner 도 **아직 미구현**이다 (task 000064~000066 생성 단계) | `.codex/skills/ywc-codex-toolkit-eval/scripts/` 에 runner 없음 |

**미확인 (UNVERIFIED — Phase 0 이 해소해야 함)**

1. `CLAUDE_CONFIG_DIR` 환경변수의 존재 여부와, 그것이 user-level 설정/skill 루트를 재배치하는지. `claude --help` 에 표기가 없다.
2. "선택한 skill 하나만 로드"를 만드는 **지원되는 수단**이 있는가. `--plugin-dir` 과 `--settings` 는 문언상 **추가(additive)** 이므로 단독으로는 격리가 되지 않는다.
3. `--disable-slash-commands` 가 plugin skill 까지 끄는가. 끈다면 "전부 끄기"는 되지만 "하나만 켜기"는 불가하다.
4. `claude -p "/<skill-name> ..."` 이 비대화 모드에서 실제로 skill 을 발동시키는가. description 기반 자동 활성화도 `-p` 에서 동작하는가.
5. `ANTHROPIC_API_KEY` 로 `claude -p` 가 인증되는가, 아니면 config dir 의 OAuth 자격증명이 필요한가. 임시 config dir 사용 시 인증이 유지되는가.
6. `--output-format json` 이 **어떤 skill 이 활성화되었는지**를 나타내는 신호를 포함하는가.

**오염원**: `install.sh` 가 `claude-code/skills` 를 `~/.claude/skills` 로 설치하므로, 평가 실행 시 사용자의 설치본 40여 개가 함께 로드된다. 이를 억제하지 못하면 "이 skill 덕분에 성공했다"는 귀속이 불가능하다.

## Scope

1. **Phase 0 — Adapter Spike (blocking)**: 위 6개 미확인 항목을 실측으로 해소하고 격리 계약을 확정한다.
2. **Phase 1 — Fixture v2 스키마 + verifier registry**: 결정적 채점 어휘를 정의한다.
3. **Phase 2 — 격리 runner + 상태/아티팩트**: 케이스마다 새 workspace, 상태 enum, 리댁션/보존 정책.
4. **Phase 3 — S3 배선**: reliability → S3 밴드, fixture 부재 시 `"unmeasured"`.
5. **Phase 4 — Ablation + 은퇴 근거**: with/without 6회 paired trial, 사람 승인.
6. **Phase 5 — CI 계층화**: PR fast / scheduled deterministic / manual expensive.

## Out of Scope

- **60개 항목 전량 fixture 작성** — Phase 1~2 는 대표 소수만 migrate 한다. 나머지는 `"unmeasured"` 로 남고 backlog 가 회수한다.
- **평가 결과만으로 자동 은퇴** — Codex spec AC14 를 계승: 사람 승인 없이는 `CANDIDATE_FOR_REVIEW` 를 넘지 않는다.
- **`claude-code/skills` 본문 수정** — 평가 대상일 뿐이다.
- **Codex 측 변경** — `.codex/skills/ywc-codex-toolkit-eval` 은 별도 소유.
- **evaluator 배포** — runner 는 `.claude/skills/` 하위 local-only 로 유지한다 (`SKILL.md:18` internal-only 정책).
- **API 기반 실행 (프로젝트 방침, 2026-07-22 확정)** — Anthropic REST API 직접 호출과 `ANTHROPIC_API_KEY` 를 요구하는 경로는 **채택하지 않는다.** 평가는 Claude 구독으로만 동작한다. 결과적으로 `--bare`(OAuth 미독해)와 노선 N3 는 선택지에서 제외된다. 상세는 `## Iteration 3 Amendments` §AC1′ 참조.
- **S3 를 mechanical baseline 에 편입** — 아래 AC7 참조. LLM 비결정성이 `--ci` 게이트를 흔드는 것을 금지한다.

## Existing Constraints Touched

| 위치 | 확인된 사실 | 계획상 처리 |
|---|---|---|
| `score.py:374` / `:544` | `axes.S3` / `axes.A1,A2,A6` 는 `None` (judgment axis) | **유지**. runner 결과는 axes 에 넣지 않는다 |
| `score.py:612-617` `flatten_mech()` | `axes` 의 non-null 만 baseline 에 저장 | S3 를 숫자로 넣는 순간 `--ci` 가 LLM 비결정성에 종속된다 → AC7 이 금지 |
| `score.py:620-648` `ci_gate()` | PASS 시 baseline 을 다시 쓴다 (`validate.yml:33-34` 의 의도된 ratchet) | 변경하지 않음 |
| `SKILL.md:113-114` | activation judge 에 unmeasured 규율 + 3회 반복이 **이미 도입됨** (커밋 `d1748f3`) | S3 도 **동일 규율**을 따른다. 새 패턴 금지 |
| `references/trigger-eval-method.md` `## Retired Items` | `retired: true` 보존 규칙 **이미 도입됨** | Phase 4 의 은퇴 근거가 이 규칙을 소비한다 |
| `references/skill-rubric.md` S3 절 | 현재 독해 기반 밴드 | Phase 3 이 reliability 기반으로 교체하되, fixture 미보유 시 독해 기반을 `(read-only)` 태그와 함께 fallback 으로 남긴다 |
| `scripts/validate.sh:598` | ⚠️ **정정 (Iteration 2)** — 원본은 이 블록이 "evaluator 의 `score.py`/`test_score.py` 존재를 강제" 한다고 적었으나 **틀렸다.** 블록은 `local skill_dir=".codex/skills/ywc-codex-toolkit-eval"` 로 시작하는 **Codex 전용**이며(claude 쪽에는 `inventory_gate.py` 자체가 없다), `grep "\.claude/skills/ywc-toolkit-eval" scripts/validate.sh` 는 결과가 없다. **claude evaluator 는 어떤 존재 검사도 받지 않으며, 지금은 `score.py` 를 지워도 `bash scripts/validate.sh` 가 통과한다.** | §AC20′ 가 claude 측 검사를 **신설**한다 (확장 아님) |
| `.github/workflows/validate.yml:37` | PR 마다 `score.py --ci` 실행 | live runner 는 여기에 **절대 넣지 않는다** (Phase 5) |
| **변경 없음(열거만)** | `plugins/**`, `codex/**`, `claude-code/skills/**` 본문 | 각각 별도 소유 또는 평가 대상 |

## Critical Surfaces

| Surface | 이유 |
|---|---|
| 격리 workspace 와 config 루트 | 실패 시 평가가 개발자의 실제 `~/.claude` 나 저장소를 오염시킨다. `ywc-commit` / `ywc-sequential-executor` 처럼 commit·push 하는 skill 이 평가 대상이다 |
| 자격증명 취급 | 임시 config dir + CI secret. 유출 시 과금·계정 위험 |
| verifier 실행 | fixture 가 임의 shell 을 지정하면 평가가 임의 코드 실행 경로가 된다 → registry 전용 |

## Acceptance Criteria

1. **AC1 (Phase 0 게이트)** — 미확인 6개 항목 각각에 대해 실측 근거(명령·출력)를 기록한 spike 리포트가 존재하고, 격리 계약이 `isolated` / `best-effort` / `unavailable` 중 하나로 확정된다. 확정 전에는 Phase 2 이후를 착수하지 않는다.
2. **AC2 (격리 등급 정직성)** — 확정된 등급이 `best-effort` 이면 문서·리포트는 **container/VM 급 비관측성을 주장하지 않는다**. Codex spec Iteration 1 의 동일 문언을 따른다.
3. **AC3 (fixture v2)** — v2 케이스는 `schema: 2` 와 `id`, `prompt`, `language`, `category`, `should_trigger`, `expected_checks` 를 가진다. `category` 는 정확히 `happy_path` | `negative` | `boundary` 중 하나다.
4. **AC4 (shell 금지)** — `expected_checks` 는 `stdout_regex`, `stderr_regex`, `file_exists`, `file_regex`, `json_path_equals`, `verifier` 만 지원한다. fixture 는 임의 명령이나 실행 파일 경로를 지정할 수 없다. `verifier` 는 evaluator 가 소유·리뷰하는 registry 항목만 지목한다.
5. **AC5 (경계 봉쇄)** — runner 는 절대경로, `..` 상향, `fixture_root` 밖으로 나가는 symlink, 선언되지 않은 output 경로를 거부한다. 실행 전후로 workspace 를 스냅샷하여 미선언 변경을 `FAIL` 로 처리한다.
6. **AC6 (상태 enum)** — 모든 실행은 `PASS` | `FAIL` | `SKIPPED_UNAVAILABLE` | `ERROR` | `INCONCLUSIVE` 중 정확히 하나를 반환한다. `SKIPPED_UNAVAILABLE` 와 `ERROR` 는 **품질 통과가 아니며 baseline 을 갱신하지 않는다**.
7. **AC7 (CI 결정성 보존)** — 실행 기반 S3 는 `axes` 에 숫자로 들어가지 않으며 `history.mechanical.json` 에 도달하지 않는다. `score.py --ci` 의 exit code 는 runner 실행 여부와 무관하게 동일하다. 테스트로 증명한다.
8. **AC8 (S3 unmeasured 일관성)** — fixture 미보유 항목의 S3 는 숫자가 아니라 `"unmeasured"` 이며 이전 run 값을 carry-forward 하지 않는다. 이미 시행 중인 S1/A2 규율(`SKILL.md:113`)과 동일 문언을 쓴다.
9. **AC9 (해상도 명시)** — reliability 는 `passes/trials` 의 이산값이다. 채택한 trial 수에서 **도달 불가능한 밴드가 있으면 문서에 명시**하고, runner 가 시작 시 경고를 1회 출력한다.
10. **AC10 (ablation)** — with/without 을 동일 fixture·동일 격리에서 **6회 paired** 실행하고 pass rate·차이·비용을 보고한다. 일반 PR CI 에서는 실행하지 않는다.
11. **AC11 (은퇴 근거)** — without 팔의 실패가 with 팔보다 1회 이하로 많고 양쪽 비용 근거가 완비된 경우에만 `CANDIDATE_FOR_REVIEW` 로 표시하며, 최종 은퇴는 **사람 승인**이 필요하다. 그 외에는 `INCONCLUSIVE`.
12. **AC12 (fixture 존속)** — 은퇴한 항목의 케이스는 삭제하지 않고 `retired: true` 로 남긴다 (`trigger-eval-method.md` `## Retired Items` 를 소비).
13. **AC13 (아티팩트 위생)** — 결과는 gitignore 된 루트에 리댁션하여 기록한다. 성공 workspace 는 즉시 삭제, 실패분은 명시 플래그로만 보존하며 run 당 10MB 상한·7일 후 정리. 원시 자격증명과 무제한 트랜스크립트는 저장하지 않는다.
14. **AC14 (CI 계층)** — PR fast 는 스키마·lint·mock verifier 만 실행한다. live 결정적 실행은 schedule 또는 manual dispatch 에서만, 비싼 ablation 은 manual 전용이다.
15. **AC15 (전체 회귀)** — `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` 와 `bash scripts/validate.sh` 가 모두 성공한다.

## Functional Requirements and Execution Plan

### Phase 0 — Adapter Spike (blocking, 다른 Phase 착수 금지)

1. 미확인 1~3(격리): 임시 디렉터리에 `.claude/skills/<target>` 만 둔 workspace 를 만들고 `cwd` 를 그곳으로 하여 `claude -p` 를 1회 실행한다. 사용자 설치본이 함께 로드되는지 관측한다. `CLAUDE_CONFIG_DIR` 후보를 실측하고, `--disable-slash-commands` + 단일 skill 조합이 "하나만 켜기"를 만드는지 확인한다.
2. 미확인 4(발동): `claude -p "/<skill> ..."` 로 skill 이 실제 발동하는지, description 자동 활성화가 `-p` 에서 동작하는지 확인한다.
3. 미확인 5(인증): `ANTHROPIC_API_KEY` 단독으로 동작하는지, 임시 config dir 에서 인증이 유지되는지 확인한다. 불가하면 credential-provider 핸드오프를 `unavailable` / `injected_ci_secret` / `ephemeral_session_material` 중에서 고른다 (Codex spec Iteration 2 의 동일 선택지).
4. 미확인 6(관측): `--output-format json` 페이로드에 활성화 신호가 있는지 확인한다. 없으면 `activation_observability: unavailable` 로 기록하고 **최종 outcome 만으로 평가**한다 (Codex spec Iteration 1 AC12 계승).
5. 산출물: `docs/skill-agent-eval/claude/spike-<date>.md` — 명령·출력·확정 등급.

**Phase 0 이 `unavailable` 로 끝나면** 이 spec 은 거기서 멈추고, S3 는 현행 독해 기반을 유지한다. 그것도 정당한 결론이다.

### Phase 1 — Fixture v2 와 verifier registry

1. stdlib 검증기로 v2 케이스 shape 를 정의한다 (AC3/AC4). v1 은 읽기 전용 호환으로 통과시킨다.
2. evaluator 소유 verifier registry 를 만든다. 각 항목은 `argv`, runner 소유 cwd, timeout, 허용 env, 기대 exit code, 선택적 출력 regex 를 선언한다. shell 인터프리터·상속 자격증명·네트워크는 기본 차단.
3. workspace manifest 를 정의한다: `fixture_root`(저장소 상대, `evals/fixtures/` 하위), `fixture_files`, `output_paths`, `target_skill`, `skill_dependencies`, `verifier_ids`.

### Phase 2 — 격리 runner 와 결과 계약

1. 케이스마다 새 임시 workspace + Phase 0 이 확정한 격리 수단으로 실행한다.
2. 실행 전후 workspace 스냅샷을 비교하여 미선언 변경을 `FAIL` 로 처리한다 (AC5).
3. 결정적 check 를 먼저 돌리고, 미해결 항목만 judge 로 보낸다 (가이드 §2 하이브리드).
4. 결과 레코드: run id, case id, attempt, 상태(AC6), duration, 비용(가능할 때), 아티팩트 경로, verdict. 리댁션·보존은 AC13.

### Phase 3 — S3 배선

1. `reliability = passes / trials` → S3 밴드. 밴드표와 도달 불가 구간을 `references/skill-rubric.md` 에 기록한다 (AC9).
2. fixture 미보유 → `"unmeasured"` (AC8). 독해 기반은 `(read-only)` 태그와 함께 fallback 으로 남긴다.
3. **`axes.S3` 는 계속 `None`** 이며 runner 결과는 scorecard 와 backlog 에만 반영된다 (AC7).

### Phase 4 — Ablation 과 은퇴 근거

1. `--suite expensive` 등 명시 플래그에서만 with/without 을 활성화한다. without 팔은 Phase 0 이 확정한 수단(유력 후보: `--disable-slash-commands`)을 쓴다.
2. 6회 paired trial, pass rate 와 불확실성 표기 (AC10).
3. `CANDIDATE_FOR_REVIEW` 판정과 사람 승인 (AC11). fixture 는 존속 (AC12).

### Phase 5 — CI 계층화

1. PR fast: 스키마·lint·mock verifier 만. 기존 `validate.yml` 의 `score.py --ci` 는 그대로 둔다.
2. scheduled: live 결정적 실행. `workflow_dispatch` + 주기 실행.
3. manual: ablation/judge. 비용 상한과 아티팩트 보존 기간을 정한 뒤에만 활성화.

## Test Strategy

| Layer | 증거 | 통과 조건 |
|---|---|---|
| Spike | Phase 0 리포트 | 6개 미확인 항목 각각에 실측 근거와 확정 등급 |
| v2 validator | valid/invalid fixture | 미지원 category, v1/v2 혼동, 경로 traversal, 자유형 command 가 실패 |
| Verifier registry | 가짜 registry 항목 + shell 유사 값 | registry 소유 argv 만 고정 cwd/timeout/env 로 실행 |
| 격리 | 연속 2회 fake-adapter 실행 | 직전 workspace·config·아티팩트가 다음 실행에 없음. **호스트 비관측성은 주장하지 않음** |
| 미선언 쓰기 | symlink escape / 범위 밖 쓰기 fixture | `FAIL` + diff 요약 |
| 상태 집계 | 초과 크기·리댁션·보존 fixture | 상태 enum 과 보존 정책이 강제됨 |
| CI 결정성 | runner 실행 전후 `score.py --ci` | exit code 와 `history.mechanical.json` 이 동일 (AC7) |
| S3 unmeasured | fixture 미보유 항목 + 직전 run 값이 남아 있는 상태 | S3 가 `"unmeasured"` 이고 carry-forward 가 없음 (AC8) |
| 밴드 해상도 | 채택 trial 수로 `passes/trials` 전수 열거 | 도달 불가 밴드가 문서와 일치하고 시작 경고가 1회 출력됨 (AC9) |
| Ablation | 6회 paired fake-adapter | candidate vs inconclusive 규칙과 비용 완비 요구가 정확 (AC10/AC11) |
| Retired 존속 | 카탈로그에서 제거된 항목의 `retired: true` 케이스 | 케이스가 남아 있고 orphan 경고나 coverage 기여가 없음 (AC12) |
| CI 계층 | `pull_request` 이벤트로 트리거한 run | live/ablation job 이 skip 으로 기록되고 PR fast 만 실행됨 (AC14) |
| 회귀 | `test_score.py`, `bash scripts/validate.sh` | exit 0 (AC15) |

## Rollout and Dependencies

1. **Phase 0 을 단독 PR 로 먼저 제출한다.** 확정 등급이 나오기 전에는 runner 코드를 쓰지 않는다.
2. Phase 1(스키마·registry)과 fake-adapter 테스트를 다음 PR 로. live 실행 없음.
3. Phase 2 를 local/manual 로 검증한 뒤 scheduled CI 에 연결.
4. Phase 3 S3 배선은 Phase 2 결과가 재현 가능해진 뒤.
5. Phase 4 ablation 은 비용 상한·모델·보존 기간을 정한 뒤 opt-in 으로만.

**의존**: Codex 측 task 000064-020(isolated runner adapter)이 먼저 착수되면 그 구현 경험이 Phase 0/2 를 크게 단축한다. 다만 **차단 의존은 아니다** — 두 evaluator 는 별도 런타임(Codex CLI vs Claude Code CLI)을 대상으로 하므로 어댑터는 공유되지 않는다.

## Risks and Mitigations

| Risk | 완화 |
|---|---|
| **격리 불가로 spec 전체가 무산** | Phase 0 이 blocking 게이트. `unavailable` 결론도 정당한 산출물이며 그 경우 S3 는 현행 유지. 코드를 먼저 쓰지 않는다 |
| 개발자 실제 환경 오염 (commit/push 하는 skill 이 대상) | AC5 의 전후 스냅샷 + remote 없는 workspace. 최초 검증은 `ywc-commit` 같은 파괴적 skill 로 먼저 수행 |
| 자격증명 유출·과금 | 임시 config dir, 프로세스 한정 주입, 아티팩트·명령 메타데이터에서 제외. live 는 schedule/manual 전용 |
| skill 미발동을 S3 하락으로 오귀속 | 활성화 신호가 없으면 `activation_observability: unavailable` 로 기록하고 outcome 만 평가. 미발동은 S1 소관임을 runner 가 별도 표기 |
| LLM 비결정성이 CI 를 흔듦 | AC7 이 구조적으로 차단 — S3 는 axes/baseline 에 진입하지 않는다 |
| 6회 trial 의 비용 | ablation 은 manual 전용, 대상은 선별된 소수 케이스 |
| 두 evaluator 정책 drift | 계약 문언을 Codex spec 에서 인용하고 출처를 명시. 재작성 금지 |

## Open Questions

1. Phase 0 이 `best-effort` 로 끝날 경우, 사용자 설치본 40여 개가 함께 로드되는 상태에서 **outcome 귀속을 어디까지 주장할 수 있는가.** 후보 답: ablation 의 with/without 차이로만 귀속을 주장하고 단일 실행 결과로는 주장하지 않는다.
2. trial 수를 6(Codex AC14 계승)으로 할지, S3 밴드 해상도에 맞춰 조정할지. 6회면 reliability 는 1/6 단위이며 일부 밴드가 도달 불가일 수 있다 (AC9 가 명시를 강제).
3. Claude Code 플러그인 매니페스트(`.claude-plugin/plugin.json`)를 임시 생성하여 `--plugin-dir` 로 단일 skill 을 주입하는 방식이 유효한가. Phase 0 미확인 2번의 하위 질문.
4. 비용 상한과 아티팩트 보존 기간을 누가 정하는가.

## Confidence Gate

> ⚠️ SUPERSEDED by Iteration 1 — see §개정된 Confidence Gate.

Confidence: **72/100 — REVIEW**

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 88 | Phase 경계, 비목표, AC 가 명확하고 계약은 Codex spec 에서 인용 |
| Architecture compliance | 84 | 기존 evaluator 구조(local-only, signals-only, judgment axis null)를 확장하며 새 패턴을 만들지 않음 |
| Evidence quality | 80 | CLI 플래그·설치 경로·플러그인 성격·runner 부재를 실측 확인. 다만 격리 수단은 미확인 |
| Reuse verified | 74 | Codex spec 의 계약은 재사용 가능하나, 어댑터는 런타임이 달라 공유 불가 |
| **Root cause identified** | **58** | **격리 수단이 미확인이다.** claude-code 에 `CODEX_HOME` 대응물이 있는지 확인되지 않았고, spec 의 실현 가능성이 여기에 전적으로 달려 있다 |

Weakest dimension: **Root cause identified (58)** — 필수 차원이 70 미만이므로 밴드는 REVIEW 이며, **Phase 0 완료 전에는 구현에 착수할 수 없다.**

What would raise it: Phase 0 spike 로 미확인 6개 항목을 해소하고 격리 등급을 확정하면 Root cause 는 85+ 로 오른다. 그 시점에 이 spec 을 Iteration 1 로 개정한다.

## Step 4b.5 Self-Consistency Pass

- **Pass A — 교차 일관성**: AC1~AC15 가 Phase 0~5 에 각각 대응하고, 모든 Phase 가 최소 1개 AC 에 의해 동기부여됨을 확인. **검출 1건**: AC8·AC9·AC12·AC14 에 대응하는 Test Strategy 행이 누락되어 있었고 4개 행을 추가함. ✓
- **Pass B — 주장↔현실**: 인용을 실측 대조. **검출 4건** — Phase 3 이 `score.py` 에 +72줄을 추가하면서 라인이 밀려 `axes` 는 `:320`→`:374`/`:523`→`:544`, `flatten_mech` 는 `:535-541`→`:612-617`, `ci_gate` 는 `:543-570`→`:620-648`, `SKILL.md` activation judge 는 `:111`→`:113` 으로 교정. `## Retired Items`, 커밋 해시 3건은 정확했음. ✓
  > ⚠️ **Iteration 2 정정** — 이 Pass B 는 `validate.sh:610-621` 을 "정확" 으로 판정했으나 **라인 범위의 존재만 확인하고 소유자를 확인하지 않았다.** 해당 블록은 Codex 전용이다. 인용의 정확성은 "그 줄에 무엇이 있는가" 만이 아니라 "그것이 내가 주장한 것인가" 까지 확인해야 한다.
- **Pass C — 스키마 불변식**: DB·migration·`@relation` 이 없으므로 관계형 스키마 관점은 **N/A**. fixture v2 와 workspace manifest 의 불변식은 AC3(필수 필드·category 도메인)·AC4(check type 화이트리스트)·AC5(realpath 봉쇄, 미선언 output 거부)가 검증 가능한 형태로 규정함. ✓

## Handoff

이 spec 은 `ywc-spec-validate` 로 검토한 뒤 `ywc-task-generator` 로 분해한다. 단 **분해 대상은 Phase 0 뿐이다** — Phase 1~5 는 Phase 0 의 확정 등급을 입력으로 받으므로, spike 결과를 Iteration 1 Amendment 로 반영한 뒤에 분해한다.

Codex 측 계약(`codex-skill-eval-upgrade.md` Iteration 1~3)은 인용 대상이며 재설계 금지다. 두 문서가 갈라지면 Codex 쪽이 원천이다.

## Iteration 1 Amendments

`ywc-spec-validate` Iteration 1 결과(Critical 4, Warning 4, Suggestion 2)와 사용자 승인 결정을 반영한다. 실패 항목만 보강하며 원본 섹션은 그대로 둔다.

### 사실 정정 (원본 작성 시 오독)

`evals/history.json` 은 per-item **총점**을 담고 있다 — 실측 shape 는 `{schema:1, runs:[{date, mode, roots:{<root>:{count, mean_total, below_threshold, items:{<name>: <total>}}}}]}` 이며 `SKILL.md` Step 6 의 기술은 정확하다. 따라서 쟁점은 "S3 를 어디에 저장할까"가 아니라 **"축 하나가 unmeasured 일 때 `/100` 총점이 무엇을 의미하는가"** 이다. S3 는 가중치 20 이므로, 미측정 항목의 총점은 만점이 80 인 점수이고 완전 측정 항목의 총점과 나란히 놓이면 거짓이 된다.

### 확정된 결정 (사용자 승인)

**D1 — 미측정은 숫자로 내보내지 않는다.** 축 하나라도 unmeasured 인 항목은 `items.<name>` 을 `null` 로 기록한다. 부분 총점을 숫자로 쓰지 않는다. run row 에 `unmeasured: [<name>, ...]` 와 `measured: "<k>/<n>"` 를 함께 남기고, `mean_total` 과 `below_threshold` 는 **측정 완료 항목만으로** 산출한다. S3 의 출처를 `s3_source: "runner" | "read-only"` 로 저장한다 — runner 가 낸 4 와 문서를 읽고 낸 4 는 같은 측정이 아니며, 구분하지 않은 추세선은 실행 기반 전환 자체를 은폐한다. `history.mechanical.json` 에는 **아무것도 쓰지 않는다**(현행 유지). `ci_gate()` 는 `HISTORY_MECH` 만 읽으므로 `--ci` 는 영향받지 않는다.

**D2 — `·` 를 재사용하지 않는다.** `evals/evals.json:15` 가 `·` 를 이미 "judgment-deferred(이번 run 에서 판단 tier 미실행)" 로 규정하고 있다. fixture 부재로 인한 **측정 불가**는 다른 상태이며 해소 방법도 다르다(`--mode full` 재실행 vs fixture 백필). 스코어카드 `S3` 열의 미측정은 **`?`** 로 표기하고, 해당 행의 `Total` 은 **`—`** 로 비운다. 별표를 단 부분 총점(`64*`)은 정렬·비교에서 그대로 숫자로 취급되어 오해를 부르므로 채택하지 않는다. `references/scorecard-format.md` 에 범례를 추가한다.

**D3 — 아티팩트 경로는 Codex 결정을 미러링한다.** `docs/skill-agent-eval/` 는 이미 추적되고 있고 무시 규칙이 없으며 codex sweep 리포트 8건이 커밋되어 있다. 즉 "사람이 검토한 리포트는 커밋, 기계 산출물은 별도" 관례가 이미 존재한다. 이를 따른다.

| 대상 | 위치 | 추적 |
|---|---|---|
| 사람이 검토한 리포트 | `docs/skill-agent-eval/claude/<YYYY-MM-DD>-<name>.md` | 커밋 |
| Phase 0 spike 리포트 | `docs/skill-agent-eval/claude/spike-<YYYY-MM-DD>.md` | 커밋 |
| 기계 run 산출물 | `docs/skill-agent-eval/claude/runs/<run-id>/` | **gitignore** |

`.gitignore` 규칙은 `docs/skill-agent-eval/*/runs/` **한 줄**로 둔다 — 두 런타임을 동시에 덮어 Risks 의 "두 evaluator 정책 drift" 를 원천 차단한다.

### 개정된 Acceptance Criteria

- **§AC8′** (AC8 확장) — fixture 미보유 항목의 S3 는 `"unmeasured"` 이며 carry-forward 하지 않는다(원본 유지). **추가**: 그 항목의 `items.<name>` 은 `null` 이고, run row 는 `unmeasured[]` 와 `measured` 를 담으며, `mean_total`/`below_threshold` 는 측정 완료 항목만으로 계산된다. 부분 총점이 숫자로 기록되면 실패다 (D1).
- **§AC13′** (AC13 확장) — 아티팩트 루트는 `docs/skill-agent-eval/claude/runs/<run-id>/` 이고 `.gitignore` 의 `docs/skill-agent-eval/*/runs/` 규칙으로 제외된다. 사람이 검토한 리포트와 spike 리포트는 같은 디렉터리의 형제로 **커밋된다** (D3). 나머지(10MB 상한·7일 정리·리댁션)는 원본 유지.
- **AC16 (신규, Critical 1 대응)** — `SKILL.md:115` 의 Behavioral judge 항목이 runner 결과를 소비하도록 교체된다. fixture 가 있으면 runner 의 reliability 를, 없으면 독해 기반 fallback 을 `(read-only)` 태그와 함께 쓴다. **이 교체 없이는 runner 산출물의 소비처가 없다.**
- **AC17 (신규, Critical 3 대응)** — `references/scorecard-format.md` 가 `?`(측정 불가)와 `·`(판단 tier 미실행)를 구분하는 범례를 담고, `Total` 이 `—` 가 되는 조건을 명시한다 (D2).
- **AC18 (신규, Warning 5 대응)** — 6회 paired trial 의 상태 집계 규칙: 한 팔에서 `ERROR` 또는 `SKIPPED_UNAVAILABLE` 이 1회라도 나오면 그 쌍은 집계에서 제외하고 `paired_valid` 를 감소시킨다. `paired_valid < 6` 이면 결과는 `INCONCLUSIVE` 이며 은퇴 판정에 쓰지 않는다.
- **AC19 (신규, Warning 6 대응)** — 동시 실행 안전: run id 는 충돌 불가능해야 하고, 아티팩트 루트 쓰기는 run id 로 분리된다. 진행 중인 다른 run 의 workspace 를 읽거나 지우지 않는다.
- **AC20 (신규, Warning 8 대응)** — `scripts/validate.sh` 의 evaluator 존재 검사가 runner 파일과 그 테스트까지 포함하도록 확장된다. runner 가 삭제되면 CI 가 실패해야 한다.

### 신규 Non-Functional Requirements (Warning 7 대응)

- **NFR1 (비용)** — live 실행의 상한은 `cases × trials × arms` 이다. runner 는 시작 시 예상 dispatch 수와 예상 비용 구간을 stderr 로 출력하여 중단 기회를 준다. ablation 은 manual 전용이므로 PR 비용은 0 이다.
- **NFR2 (실행 시간)** — case 당 timeout 을 명시적으로 설정하고, workspace 생성·회수 오버헤드는 case 당 1초 미만을 목표로 한다.
- **NFR3 (해상도)** — 6회 trial 에서 `reliability` 는 1/6 단위이므로 일부 S3 밴드가 도달 불가일 수 있다. AC9 에 따라 도달 불가 구간을 문서화하고 시작 시 1회 경고한다.

### 개정된 Functional Requirements

- **§Phase 2 추가** — AC9 의 시작 경고는 **Phase 2(runner) 의 책임**이다. 밴드표는 Phase 3 이 소유하되 경고 출력은 runner 가 한다 (Suggestion 9).
- **§Phase 3 추가** — `SKILL.md:115` Behavioral judge 항목 교체(AC16), `references/scorecard-format.md` 범례 추가(AC17), `history.json` 기록 규칙 구현(§AC8′).
- **§Phase 5 확정** — `scripts/validate.sh` 존재 검사 확장을 "결정" 이 아니라 **필수 작업**으로 승격한다(AC20).
- **§AC7 근거 인용** — `references/scorecard-format.md:68` 이 이미 *"Mechanical sub-scores are stored in a sibling `history.mechanical.json` ... so the judgment tier's natural variance never trips the gate"* 를 문서화하고 있다. AC7 은 이 규칙을 재유도하지 말고 이 문장을 인용한다 (Suggestion 10).

### 개정된 Test Strategy (추가 행)

| Layer | 증거 | 통과 조건 |
|---|---|---|
| 총점 정직성 | 축 하나가 unmeasured 인 항목 | `items.<name>` 이 `null`, `mean_total` 이 해당 항목을 제외, 부분 총점이 숫자로 없음 (§AC8′) |
| 표기 구분 | 판단 tier 미실행 run + fixture 부재 항목 | 전자는 `·`, 후자는 `?`, 후자의 `Total` 은 `—` (AC17) |
| 아티팩트 경계 | run 1회 실행 후 `git status` | `runs/` 산출물이 untracked 로도 나타나지 않음(무시됨), 리포트는 추적됨 (§AC13′) |
| 쌍 집계 | 6쌍 중 2쌍에 `ERROR` 주입 | `paired_valid=4` → `INCONCLUSIVE`, 은퇴 판정 미사용 (AC18) |
| 동시 실행 | 동일 skill 2개 run 동시 기동 | run id 충돌 없음, 서로의 workspace 를 건드리지 않음 (AC19) |
| validate.sh | runner 파일 삭제 후 `bash scripts/validate.sh` | exit != 0 (AC20) |

### 개정된 Confidence Gate

> ⚠️ SUPERSEDED — 최종본은 `## Iteration 3 Amendments` §개정된 Confidence Gate 다.
> (원본 `## Confidence Gate` → Iteration 1 → Iteration 2 → **Iteration 3** 순으로 대체되었다.)

Confidence: **74/100 — REVIEW** (변동 +2)

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 92 | 미해결 3개 결정이 D1~D3 로 확정되어 출력 계약이 닫힘 |
| Architecture compliance | 88 | `·` 관례 보존, `history.mechanical.json` 불가침, Codex 아티팩트 레이아웃 미러링 |
| Evidence quality | 86 | `history.json` 실측 shape, `evals.json:15` 의 `·` 관례, `docs/skill-agent-eval` 추적 상태를 직접 확인 |
| Reuse verified | 78 | Codex 계약 재사용 가능. 어댑터는 런타임이 달라 여전히 공유 불가 |
| **Root cause identified** | **58** | **변동 없음 — 격리 수단은 여전히 미확인이다.** Phase 0 만이 이를 움직일 수 있다 |

Weakest dimension: **Root cause identified (58)** — 이번 Amendment 는 출력 계약과 누락 통합 지점을 닫았을 뿐 **격리 가능성을 검증하지 않았다.** 따라서 밴드는 REVIEW 로 유지되며, Phase 0 완료 전 구현 착수 금지는 그대로다. 이 항목이 움직이지 않는 것이 정상이다 — Amendment 로 올릴 수 있는 성질의 점수가 아니다.

### Step 4b.5 재실행 (원본 + Amendment 전체)

- **Pass A — 교차 일관성**: 신규 AC16~AC20 과 NFR1~3 이 각각 Phase 2/3/5 에 대응하고, 추가된 Test Strategy 6행이 §AC8′·AC17·§AC13′·AC18·AC19·AC20 를 각각 커버함을 확인. Iteration 1 의 Pass A 결함(AC8·AC9·AC12·AC14 무커버)은 이미 해소됨. ✓
- **Pass B — 주장↔현실**: `history.json` 실측 shape, `evals/evals.json:15` 의 `·` 규정, `docs/skill-agent-eval/` 추적·무규칙 상태, `references/scorecard-format.md:68` 문장, `SKILL.md:115` Behavioral judge 위치를 모두 직접 확인. Iteration 1 에서 교정한 라인 인용(`score.py:374`/`:544`/`:612-617`/`:620-648`, `SKILL.md:113-114`)은 이후 코드 변경이 없어 유효. ✓
- **Pass C — 스키마**: DB 없음. `history.json` 의 `items.<name>: number|null` 과 run row 의 `unmeasured[]`/`measured` 는 §AC8′ 가 검증 가능한 불변식으로 규정. fixture v2·workspace manifest 불변식은 AC3~AC5 유지. ✓

## Iteration 2 Amendments

`ywc-spec-validate` Iteration 2 결과(Critical 2, Warning 1)를 반영한다. 이번 회차의 두 Critical 은 **이 spec 자신의 사실 오류**였다.

### 사실 정정 — `scripts/validate.sh` 는 claude evaluator 를 검사하지 않는다

원본 Existing Constraints 는 `scripts/validate.sh:610-621` 이 "evaluator 의 `score.py`/`test_score.py` 존재를 강제" 한다고 적었다. **틀렸다.** 해당 블록은 `:598` 에서 `local skill_dir=".codex/skills/ywc-codex-toolkit-eval"` 로 시작하는 **Codex 전용** 검사이며, 그 안의 `inventory_gate.py` 검사가 그 증거다 — claude evaluator 에는 그 파일이 없다. `grep "\.claude/skills/ywc-toolkit-eval" scripts/validate.sh` 는 결과가 없다.

원인은 같은 파일에 두 evaluator 검사가 있으리라 가정하고 `skill_dir` 할당을 확인하지 않은 것이다. 해당 Existing Constraints 행은 위에서 정정했다.

**파급 1** — Iteration 1 의 Warning 8("runner 가 삭제돼도 CI 가 통과")은 **축소 보고였다.** 실제 노출면은 더 넓다: 오늘 기준 claude `score.py` 나 `test_score.py` 를 지워도 `bash scripts/validate.sh` 는 통과한다. `validate.yml:37` 의 `score.py --ci` 가 파일 부재 시 실패하므로 CI 전체가 조용히 통과하지는 않지만, **로컬 `validate.sh` 는 이를 잡지 못한다.**

**파급 2** — AC20 의 "확장" 은 성립하지 않는다. 확장할 대상이 없다.

### 개정된 Acceptance Criteria

- **§AC17′** (AC17 대체) — `?`(측정 불가)와 `·`(판단 tier 미실행)를 구분하는 범례가 **두 곳 모두**에 반영된다: `references/scorecard-format.md` 의 표 규약과 **`SKILL.md` 의 `## Output Format` 예시 표**. 한쪽만 고치면 두 문서가 서로를 반박한다. `Total` 이 `—` 가 되는 조건도 양쪽에 동일하게 기술한다.
- **§AC20′** (AC20 대체) — `scripts/validate.sh` 에 **claude evaluator 용 존재 검사를 신설**한다(확장 아님). 최소 범위: `.claude/skills/ywc-toolkit-eval/scripts/score.py`, `test_score.py`, 그리고 Phase 2 가 추가하는 runner 와 그 테스트. 삭제 시 `bash scripts/validate.sh` 가 exit != 0 이어야 한다. Codex 블록과 대칭 구조로 작성하되 `inventory_gate.py` 처럼 claude 측에 없는 파일을 요구하지 않는다.

### 개정된 Test Strategy (추가 행 — Warning 3 대응)

| Layer | 증거 | 통과 조건 |
|---|---|---|
| S3 소비 경로 | fixture 보유 항목 1건으로 `--mode behavioral` 실행 | `SKILL.md` Behavioral judge 가 runner 의 reliability 를 사용하고, fixture 미보유 항목에서만 독해 fallback 이 `(read-only)` 태그와 함께 쓰임 (AC16) |
| 표기 일관성 | `scorecard-format.md` 와 `SKILL.md` Output Format 을 대조 | 두 문서의 `?` / `·` / `—` 규약이 동일 (§AC17′) |
| validate.sh 신설 검사 | claude `score.py` 를 임시 삭제 후 `bash scripts/validate.sh` | exit != 0 (§AC20′) |

### 개정된 Confidence Gate

> ⚠️ SUPERSEDED by Iteration 3 — 최종본은 `## Iteration 3 Amendments` §개정된 Confidence Gate 다.
> (이 절은 Iteration 1 의 gate 를 대체했으나, 그 자신도 Iteration 3 에 의해 대체되었다.)

Confidence: **75/100 — REVIEW** (변동 +1)

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 92 | 변동 없음 |
| Architecture compliance | 88 | 변동 없음 |
| Evidence quality | 90 | `validate.sh` 의 실제 소유자와 claude 측 검사 부재를 실측 확인하여 거짓 전제 1건을 제거 (+4) |
| Reuse verified | 78 | 변동 없음 |
| **Root cause identified** | **58** | **변동 없음.** 격리 수단은 여전히 미확인이며, 사실 정정으로는 움직이지 않는다 |

Weakest dimension: **Root cause identified (58)**. 이 spec 은 **amendment 로 DONE 에 도달할 수 없다** — 남은 blocker 가 문서 결함이 아니라 경험적 미지이기 때문이다. Phase 0 spike 만이 이 숫자를 움직인다. 두 회차 연속 `NEEDS_CONTEXT` 는 게이트가 설계대로 작동한 결과다.

### Step 4b.5 재실행 (원본 + Iteration 1 + Iteration 2)

- **Pass A — 교차 일관성**: §AC17′·§AC20′ 가 각각 Phase 3·Phase 5 에 대응하고, 신규 Test Strategy 3행이 AC16·§AC17′·§AC20′ 를 각각 커버함을 확인. Iteration 1 이 남긴 AC16 무커버 결함 해소. 잔여 무커버 AC 없음. ✓
- **Pass B — 주장↔현실**: `scripts/validate.sh:598` 의 `skill_dir` 할당, claude 측 검사 부재(grep 무결과), 두 evaluator 의 `scripts/` 구성 차이(`inventory_gate.py` 유무), `SKILL.md` `## Output Format` 의 스코어카드 표 존재를 모두 직접 확인. `.gitignore` 와일드카드 동작은 일회용 저장소에서 실측 검증. ✓
- **Pass C — 스키마**: 변동 없음 — DB 없음, fixture/manifest 불변식은 AC3~AC5 유지. ✓

## Iteration 3 Amendments — Phase 0 Spike 결과 반영

근거: `docs/skill-agent-eval/claude/spike-2026-07-22.md` (실지출 $0.5409).

### Phase 0 판정: `best-effort, credential-gated`

미확인 6건 중 **4건이 닫혔고 2건이 남았으며, 예상하지 못한 제약 1건이 추가되었다.**

| # | 항목 | 결과 |
|---|---|---|
| 1 | `CLAUDE_CONFIG_DIR` | **VERIFIED** — 존재하며 user-level 설정 루트를 재배치한다 (`doctor` 비교, API 호출 0) |
| 2 | 단일 skill 격리 | **PARTIAL** — 프로젝트 로컬 `.claude/skills/` 로드 확인. 인증 실패로 억제 효과는 미입증 |
| 3 | `--disable-slash-commands` | **VERIFIED** — 프로젝트 로컬까지 끄고 **$0 로 단락**. without-arm 유효 |
| 4 | `-p` 발동 | **VERIFIED(slash)** — `result` 가 정확히 sentinel 문자열. 자동 활성화는 미검증 |
| 5 | 인증 | **VERIFIED(부정)** — 임시 config dir 은 `Not logged in`. 자격증명은 `~/.claude.json` 소재 |
| 6 | 활성화 신호 | **VERIFIED(부정)** — json 20개 키에 skill 필드 없음 |
| 7 | **(신규) `--bare`** | **격리와 구독이 배타적** — 아래 참조 |

### 원본 전제 2건 정정

**정정 1 — 오염 규모.** 원본 `## 선행 조건` 은 "사용자의 설치본 40여 개" 라 적었다. 실측은 **243개**(`~/.claude/skills`)다. 이 저장소 외 다수 플러그인 skill 이 설치되어 있다.

**정정 2 — 오염은 비용 문제이기도 하다.** 프롬프트 한 줄·응답 17자짜리 dispatch 가 **$0.5409** 였다. 243개 description 이 매 호출 컨텍스트에 실리기 때문이다. 6회 paired × 2 arm 이면 **케이스당 약 $6.5**다. NFR1 은 이 수치를 기준으로 다시 읽어야 하며, **격리는 정확성 장치이자 비용 절감 장치**라는 관점이 원본에 없었다.

### 신규 제약 — `--bare` 는 격리를 주지만 구독을 뺏는다

`claude --help` 의 `--bare` 설명: *"skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery ... **Anthropic auth is strictly `ANTHROPIC_API_KEY` or `apiKeyHelper` via `--settings` (OAuth and keychain are never read)** ... **Skills still resolve via `/skill-name`**."*

`--bare` 는 이 spec 이 원하던 격리에 가장 근접한 도구지만 **OAuth 를 절대 읽지 않는다.** 현재 계정은 `authMethod: "claude.ai"`, `subscriptionType: "max"` 이며 Test A 의 $0.5409 는 **이미 구독으로 결제되었다** — 즉 비격리 실행에는 API key 가 필요 없다.

따라서 자격증명 문제는 "어느 핸드오프를 고를까" 가 아니라 **"격리를 살릴 것인가 구독을 살릴 것인가"** 라는 노선 선택이다.

### §AC1′ (AC1 대체) — Phase 0 종결 조건 재정의

Phase 0 은 **노선 확정**으로 종결한다. 아래 중 하나를 선택하고 근거를 spike 리포트에 남기면 Phase 0 은 완료다.

| 노선 | 격리 | 구독 | 상태 |
|---|---|---|---|
| **N1. 비격리 + ablation 귀속** | ✗ | ○ | **검증 완료 — 즉시 채택 가능** |
| **N2. `setup-token` + 격리** | ○ | ○(추정) | 미검증 — 최우선 확인 대상 |
| ~~N3. `ANTHROPIC_API_KEY` + `--bare`~~ | ○ | ✗ | **프로젝트 방침상 배제** (아래 참조) |
| ~~N4. 자격증명 파일 복사~~ | ○ | ○ | **금지** — `/tmp` 에 OAuth 토큰 노출 |

**선택지는 N2 와 N1 둘뿐이다.** 권장 순서는 **N2 → (실패 시) N1**. N1 을 택하는 것도 **정당한 종결**이며, 그 경우 등급을 `best-effort` 로 확정하고 §AC2′ 로 귀속 주장 범위를 좁힌다.

> **프로젝트 방침 (2026-07-22 확정)** — 이 저장소의 평가 작업은 **Claude 구독 기반으로만 동작**한다. Anthropic REST API 를 직접 호출하거나 `ANTHROPIC_API_KEY` 를 요구하는 경로는 채택하지 않는다. 따라서 N3 는 기술적으로 가능하더라도 **선택지가 아니다.** 이 방침은 격리보다 우선한다 — 격리를 얻기 위해 구독을 포기하지 않는다.
>
> 파급: `--bare` 는 OAuth 를 읽지 않으므로 **이 방침 아래에서는 사용할 수 없다.** 격리 수단 후보는 `CLAUDE_CONFIG_DIR` + N2 조합으로 한정된다.
>
> (참고 — 방침의 유일한 기존 예외는 `scripts/translate.sh` 다. README 다국어 생성을 위해 `curl` 로 `api.anthropic.com/v1/messages` 를 호출하며 `ANTHROPIC_API_KEY` 를 요구한다. 이번 평가 작업과 무관한 선행 도구이므로 이 spec 의 범위 밖이지만, 방침을 저장소 전체로 확장하려면 `claude -p` 기반으로 전환해야 할 유일한 지점이다.)

### §AC2′ (AC2 확장) — 귀속 주장의 한계

등급이 `best-effort` 이면 container/VM 급 비관측성을 주장하지 않는다(원본 유지). **추가**: 노선 N1 에서는 **단일 실행 결과로 특정 skill 에 성과를 귀속하지 않는다.** 243개 sibling 이 함께 로드되므로, 귀속은 오직 **with/without ablation 의 차이**로만 주장한다. 리포트는 로드된 skill 수를 함께 기록한다.

### §NFR1′ (NFR1 대체) — 실측 기반 비용

- 비격리 dispatch 실측 단가: **$0.54** (243 skill 로드 기준)
- 케이스당 ablation 비용: `6 trials × 2 arms × $0.54 ≈ $6.5`
- runner 는 시작 시 **예상 dispatch 수와 예상 비용을 stderr 로 출력**하고 중단 기회를 준다
- `--disable-slash-commands` 를 slash 호출과 함께 쓰면 $0 로 단락되므로, ablation 의 without-arm 은 **반드시 자연어 프롬프트**로 수행한다(그렇지 않으면 두 팔이 비대칭)

### §Phase 2 확정 사항

- 발동: `claude -p "/<skill-name> <prompt>" --output-format json`
- 판정: `result` 에 대한 outcome 검사. **`activation_observability: unavailable` 이 실제 경로다** — json 페이로드에 skill 필드가 없음이 확인되었다
- 미발동 판별은 sentinel 방식(고유 마커 출력)을 쓴다. spike 가 이 방식으로 판정의 주관성을 제거했다

### 개정된 Confidence Gate

> Iteration 2 의 `### 개정된 Confidence Gate` 는 ⚠️ SUPERSEDED — 아래가 유효하다.

Confidence: **79/100 — REVIEW** (변동 +4)

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 94 | Phase 0 종결 조건이 노선 선택으로 명확해짐 (§AC1′) |
| Architecture compliance | 88 | 변동 없음 |
| Evidence quality | 95 | 6개 항목 중 4개를 실측으로 종결, 원본 전제 2건 정정, 비용 실측 확보 |
| Reuse verified | 82 | Codex 계약 재사용 유지. `--disable-slash-commands` 가 without-arm 으로 실증됨 |
| **Root cause identified** | **72** | **58 → 72.** 격리 수단이 실재함을 입증했고 차단 요소를 "인증 미상" 에서 **"격리 대 구독 노선 선택"** 이라는 결정 가능한 문제로 좁혔다. 다만 N2 미검증이라 `isolated` 는 아니다 |

Weakest dimension: **Root cause identified (72)** — 필수 차원 임계 70 을 **넘겼다.** 밴드는 여전히 REVIEW(총점 79)지만, 이제 남은 것은 미지가 아니라 **사용자 결정**이다. N1 을 채택하면 즉시 구현 착수가 가능하고, N2 를 시도하려면 `claude setup-token` 1회 실행이 필요하다.

### Step 4b.5 재실행 (원본 + Iteration 1~3)

- **Pass A — 교차 일관성**: §AC1′·§AC2′·§NFR1′ 가 Phase 0·Phase 2·Phase 4 에 대응. §NFR1′ 가 원본 NFR1 을 대체하며 AC10 의 6회 paired 와 수치가 일치(6×2×$0.54). without-arm 의 $0 단락 함정이 §NFR1′ 와 §Phase 2 양쪽에 기록됨. ✓
- **Pass B — 주장↔현실**: 인용 전량이 spike 리포트의 실행 기록에 대응 — `doctor` 비교 출력, `Not logged in` 결과, `Unknown command` 결과, json 20개 키, `~/.claude.json` 85키/`oauthAccount`, `claude auth status` 의 `max` 구독, `--help` 의 `--bare` 문언. 원본의 "40여 개" 는 §정정 1 로 교정. ✓
- **Pass C — 스키마**: 변동 없음 — DB 없음. ✓

## Iteration 4 Amendments — 노선 N1 확정, **Phase 0 종결**

### 결정 (2026-07-22, 사용자 확정)

노선 **N1 — 비격리 + ablation 귀속**을 채택한다. §AC1′ 이 규정한 "노선 확정으로 Phase 0 을 종결한다" 는 조건이 충족되었으므로 **Phase 0 은 완료다.** 이 spec 은 더 이상 spike 로 막혀 있지 않다.

N2(`setup-token` + 격리)는 미검증인 채 남는다. 후일 catalog 격리가 필요해지면 재개할 수 있도록 절차를 spike 리포트에 남겨 두었다.

### 확정된 실행 계약

| 항목 | 확정값 |
|---|---|
| 인증 | 개발자 머신의 **기존 구독 세션** — Test A 로 검증 완료 |
| catalog 격리 | **없음** — 설치된 skill 전량(현재 243개)이 함께 로드된다 |
| `CLAUDE_CONFIG_DIR` 임시화 | **사용하지 않음** (인증 상실) |
| `--bare` | **사용하지 않음** (OAuth 미독해 — 프로젝트 방침상 배제) |
| with-arm | `claude -p "/<skill> <prompt>" --output-format json` |
| without-arm | 동일 프롬프트 + `--disable-slash-commands` |
| 판정 | `result` 에 대한 outcome 검사 (`activation_observability: unavailable`) |

### 격리의 두 층위 — N1 이 포기하는 것은 하나뿐이다

원본은 "격리" 를 한 덩어리로 다뤘으나 실제로는 두 층위이고, **N1 은 그중 하나만 포기한다.**

- **catalog 격리** (어떤 skill 이 로드되는가) — **포기.** 인증과 맞물려 있어 구독 방침과 양립하지 않는다.
- **workspace 격리** (파일이 어디에 쓰이는가) — **유지하며 필수.** 인증과 **무관**하고 `mktemp` / git worktree 로 달성된다.

따라서 **AC5(경계 봉쇄)와 AC13(아티팩트 위생)은 그대로 유효하다.** `ywc-commit` / `ywc-sequential-executor` 처럼 commit·push 하는 skill 을 평가하려면 workspace 격리가 없으면 안 된다. 이 구분을 놓치면 "격리를 포기했으니 workspace 도 대충" 이라는 잘못된 결론에 이른다.

### §AC2″ (§AC2′ 대체) — 귀속 주장의 확정 한계

N1 에서 성과 귀속은 **with/without ablation 의 차이로만** 주장한다. 단일 실행 결과를 근거로 "이 skill 덕분에 됐다" 고 말하지 않는다.

무엇을 측정하는지 정확히 적는다.

- with-arm 은 `/name` **명시 호출**이므로 대상 skill 이 실행된다는 사실 자체는 보장된다.
- without-arm 의 `--disable-slash-commands` 는 **모든** skill 을 끈다.
- 그러므로 측정 대상은 **"대상 skill 의 지시가 모델의 기본 행동보다 나은가"** 이며, 이는 가이드 §4 가 요구한 ablation 과 정확히 일치한다.
- **잔여 위험**: with-arm 실행 도중 형제 skill 이 끼어들어 기여할 수 있다. 명시 호출이 위험을 줄이지만 제거하지는 못한다. 리포트는 **로드된 skill 수를 함께 기록**하여 이 한계를 드러낸다.

### §Phase 5″ (Phase 5 대체) — CI 계층이 3단에서 2단으로 줄어든다

**live 평가를 CI 에서 실행할 수 없다.** 구독 인증은 개발자 머신의 세션에 있고 GitHub Actions 러너에는 없다. API key 는 방침상 배제되었다. 이는 N1 채택의 직접적 파급이며 원본 Phase 5 가 전제한 3계층을 무너뜨린다.

| 계층 | 원본 | N1 확정 후 |
|---|---|---|
| PR fast (스키마·lint·mock verifier, 모델 호출 0) | 유지 | **유지** |
| scheduled live deterministic | `workflow_dispatch` + 주기 실행 | **불가 — 삭제** |
| manual expensive (ablation) | manual 전용 | **local manual 로 이동** — 사람이 로컬에서 실행 |

축소이지 결함이 아니다. 평가는 **릴리스 주기마다 사람이 로컬에서 돌리는 활동**이 된다. `.github/workflows/` 에 live 평가 job 을 추가하지 않는다.

### §NFR1″ (§NFR1′ 대체) — 비용 확정

- dispatch 당 **$0.54** (243 skill 로드 상태에서의 실측)
- 케이스당 ablation: `6 trials × 2 arms ≈ $6.5`
- 격리로 이 비용을 낮출 여지는 **의도적으로 포기했다.** 대신 **대상 케이스를 소수로 엄선**하여 총액을 통제한다
- runner 는 시작 시 예상 dispatch 수와 예상 비용을 stderr 로 출력하고 중단 기회를 준다

### 개정된 Confidence Gate

> Iteration 3 의 `### 개정된 Confidence Gate` 는 ⚠️ SUPERSEDED — 아래가 유효하다.

Confidence: **88/100 — PROCEED** (변동 +9)

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 95 | Phase 0 종결, 실행 계약 전 항목 확정, CI 계층 축소까지 명시 |
| Architecture compliance | 90 | workspace/catalog 격리 층위 분리로 AC5·AC13 이 유효하게 보존됨 |
| Evidence quality | 95 | 실행 경로 전체가 실측 검증된 요소로만 구성 — 구독 인증, `/name` 발동, `--disable-slash-commands`, outcome 판정 |
| Reuse verified | 84 | Codex 계약 재사용 유지. 다만 Codex 는 격리를 유지하므로 두 evaluator 의 격리 모델이 갈라진다 |
| **Root cause identified** | **88** | **72 → 88.** 차단 요소가 **결정으로 해소**되었다. 남은 미지는 자동 활성화 여부뿐이며, `/name` 명시 호출을 쓰므로 실행 경로에 영향이 없다 |

Weakest dimension: **Reuse verified (84)** — 필수 차원 둘(Scope clarity 95, Root cause identified 88)이 모두 임계를 크게 상회한다. 밴드는 **PROCEED** 이며, **이 spec 은 `ywc-task-generator` 로 분해 가능한 상태가 되었다.**

### Step 4b.5 재실행 (원본 + Iteration 1~4)

- **Pass A — 교차 일관성**: §AC2″·§Phase 5″·§NFR1″ 가 각각 §AC2′·Phase 5·§NFR1′ 를 대체하며 상호 모순이 없음을 확인. AC5·AC13 이 workspace 격리 층위에서 계속 유효함을 명시하여 "격리 포기 = 이들 무효" 오독을 차단. AC1(Phase 0 게이트)은 **충족되어 종결**. ✓
- **Pass B — 주장↔현실**: 인용 전량이 `docs/skill-agent-eval/claude/spike-2026-07-22.md` 의 실행 기록에 대응. 신규 주장인 "CI 에 구독 인증이 없다" 는 `.github/workflows/` 에 Anthropic 자격증명이 존재하지 않음(`GITHUB_TOKEN`·release-please 앱 자격증명뿐)으로 뒷받침된다. ✓
- **Pass C — 스키마**: 변동 없음 — DB 없음. fixture v2·workspace manifest 불변식은 AC3~AC5 유지. ✓
