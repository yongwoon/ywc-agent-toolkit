# Plan: Claude Code Skill Eval 고도화 (ywc-toolkit-eval)

> Scale: **Small** — 3개의 독립 PR 로 분할 실행. 실행형 runner(가이드 §5)와 ablation(§4)은 범위 밖이며 별도 spec.
> Target evaluator: `.claude/skills/ywc-toolkit-eval/`
> Target bundle: `claude-code/skills`, `claude-code/agents`
> Source: `docs/studies/insights/PHILIPP_SCHMID_SKILL_EVAL_DESIGN_GUIDE.md` (Philipp Schmid, Google DeepMind)
> Counterpart: `docs/ywc-plans/codex-skill-eval-upgrade.md` (Codex 측 동일 가이드 대응 spec, Confidence 93/100 PROCEED)
> Precedent: `docs/ywc-plans/old/toolkit-eval-backlog-2026-07-06.md` (coverage 신호를 구현한 spec — 그 결정사항을 계승)

## Purpose

Philipp Schmid 가이드의 5개 제안을 `ywc-toolkit-eval` 에 반영하되, **이 저장소에서 실제로 결손인 항목만** 선별한다. 5개 중 2개는 이미 구현되어 있고, 2개는 Codex 측 spec 이 설계를 확정해 두었으므로 재설계하지 않는다.

## Ground Truth (2026-07-22 실측)

`python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` (읽기 전용, 파일 변경 없음 확인):

| 항목 | 값 |
|---|---|
| 평가 대상 | **60 items** (`claude-code/skills` 47 + `claude-code/agents` 13) |
| trigger-cases | **312건** — positive 211 / collision 91 / negative 10 |
| in-domain negative | **0건** (10건 전부 off-domain: 날씨·레시피·수학·번역·일정·스포츠·요리·지리·상식) |
| coverage 미달 | **6건** — 전부 `positives=0, collisions=0` (fixture 전무) |

미달 6건: `ywc-auth-implement`, `ywc-iac-author`, `ywc-infra-design`, `ywc-infra-optimize`, `ywc-infra-review`, `ywc-cloud-engineer`

## 가이드 5개 제안 대응표

| 가이드 항목 | 이 저장소 상태 | 처리 |
|---|---|---|
| §1 테스트 케이스 설계 | JSON 구조화 **완료**. coverage 최소치(`COVERAGE_MIN_POSITIVES=3` / `COVERAGE_MIN_COLLISIONS=2`)도 `score.py:59-61,235-274` 에 **구현 완료**. 단 in-domain negative 0건이고, **judge 가 이 신호를 존중하라는 규칙이 어디에도 없음** | **Phase 1 + 2** |
| §2 하이브리드 검증 | 2-tier 구조 **완료** (`SKILL.md:22-25`) | 작업 없음 |
| §3 스킬 파일 Linter | 길이 제한 **완료** (`A8_body_cap` + S4 누진 감점). No-ops / 비명령형 문체 **미구현** | **Phase 3** |
| §4 Ablation & 은퇴 | 미구현. Codex spec 이 설계 확정(6회 paired trial, 사람 승인 필수, fixture 는 은퇴 후에도 보존) | **retired 보존 규칙만** 채택(Phase 1). 실행은 범위 밖 |
| §5 격리 실행 · 다중 시도 | 격리 실행 **미구현** — 이 저장소에 Python runner 인프라가 전무(`scripts/` 는 bash). 다중 시도도 미구현 | **judge 다중 시도만** Phase 1. 격리 실행은 범위 밖 |

## Scope

1. **Phase 1 (문서 전용)** — judge 가 `coverage.sufficient` 를 존중하도록 강제, judge 다중 시도, negative 작성 지침, retired 보존 규칙
2. **Phase 2 (fixture)** — coverage 미달 6건 백필 + in-domain negative 추가
3. **Phase 3 (코드)** — prose lint 를 warning-only signal 로 추가

각 Phase 는 독립 PR. Phase 1 은 코드 변경이 없어 CI 위험 0, Phase 2 는 fixture 만, Phase 3 만 `score.py` 를 건드린다.

## Out of Scope

- **격리 실행 runner (가이드 §5 전반)** — 이 저장소에는 dispatch adapter / eval runner 가 존재하지 않는다. 신규 구축이며, Codex spec 의 확정 계약(temporary home 격리, verifier registry, 상태 enum)을 이식하는 별도 spec 으로 분리한다.
- **Ablation 실행 (가이드 §4)** — 위와 동일. Codex spec `Iteration 1 Amendments` AC14(6회 paired trial, `CANDIDATE_FOR_REVIEW`, 사람 승인)를 계승할 것.
- **`prose_lint` 의 axis 편입** — Phase 3 은 관측만. Codex spec AC8 도 "no-op/문체만으로 CI 실패를 만들지 않는다" 로 못박고 있다.
- **negative 를 coverage 최소치에 편입** — `COVERAGE_MIN_*` 는 변경하지 않는다. coverage 는 `signals` 전용이며 axis 를 움직이지 않는다는 현행 계약(`score.py:340-342`)을 유지한다.
- **S1/A2 점수의 실제 상승** — 선례 §AC12′ 에 따라, 점수 이동은 **완료 게이트가 아니라 다음 회차 eval 의 기대치**다. 본 계획의 완료 조건은 `coverage.sufficient` 와 문서 규칙까지다.
- **`--ci` 의 baseline 자기 갱신 동작 변경** — `ci_gate()` 는 PASS 시 baseline 을 다시 쓴다. `validate.yml:33-34` 에 문서화된 **의도된 ratchet 설계**이므로 건드리지 않는다.
- **Codex 측 변경** — `codex/skills`, `.codex/skills/ywc-codex-toolkit-eval` 은 별도 소유.

## Existing Constraints Touched

| 위치 | 확인된 사실 | 계획상 처리 |
|---|---|---|
| `score.py:59-61` | `COVERAGE_MIN_POSITIVES=3`, `COVERAGE_MIN_COLLISIONS=2` | 값 변경 없음. Phase 1 은 이 신호를 **소비하는 규칙**만 추가 |
| `score.py:235-274` `load_coverage()` | item 별 `{positives, collisions, sufficient}` 산출. 중복 case id 는 카운트 제외 | 재사용만 |
| `score.py:340-342`, `:460-462` | `signals["coverage"]` 주입 + 주석 "signals-only; S1 stays null in axes (Amendment A2)" | `prose_lint` 도 **동일 선례**를 따른다. 새 패턴 금지 |
| `score.py:596-600` | coverage 미달 수를 stderr 로 요약 (stdout JSON 오염 방지) | 유지 |
| `score.py:535-541` `flatten_mech()` | `axes` 의 non-null 값만 baseline 에 저장. `signals` 는 저장 대상 아님 | → `prose_lint` 추가는 `history.mechanical.json` 무영향, `--ci` 회귀 위험 구조적으로 0 |
| `score.py:543-570` `ci_gate()` | PASS 시 baseline 을 **다시 쓴다** | 변경 않음. 단 Verification 에 git diff 가드 필수 |
| `SKILL.md:109-116` Step 3 judge | activation judge 절차에 coverage 언급이 **전무** | **Phase 1 의 핵심 수정 지점** |
| `references/trigger-eval-method.md:15` | "≥3 positives and ≥2 collisions" 를 **산문으로만** 규정. 기계 신호와 미연결 | Phase 1 에서 연결 |
| `references/trigger-eval-method.md:74-76` | Determinism Note — ±1 case 만 언급, 반복 실행 규정 없음 | Phase 1 에서 다중 시도 규정 추가 |
| `SKILL.md:18` | internal-only, locale-exempt | README 로케일 작업 불필요 |
| **선례 §AC1′** | `score.py` 는 **S1 을 산출하지 않는다**. S1 은 판단-tier 활성화 판정관의 몫 | Phase 1 의 unmeasured 규율은 **판정관 규칙**으로 기술한다. score.py 는 손대지 않는다 |
| **선례 W3 (검증됨)** | `scripts/validate.sh` 는 **claude-code eval 픽스처를 커버하지 않는다** | Phase 2 의 게이트는 **`score.py` coverage 단독**. `validate.sh` 를 fixture 게이트로 쓰지 말 것 |
| **선례 §OQ1′ / EC2** | collision 은 **실재 경합 형제**를 지목해야 한다. 경합 형제가 없으면 소유자 승인 하에 예외를 문서화하며, **negative 로 대체하지 않는다** | **해소 완료** — 아래 §경합 형제 확정 참조. 예외 승인 불필요 |
| `score.py:260-262` `load_coverage()` | collision case 는 `expected` 와 `impostor` **양쪽 모두에** +1 가산한다 (`for name in {expected, impostor}`). 선례 §AC1′ 의 "owner/impostor 합산 collision ≥2" 와 일치 | Phase 2 의 물량 산정에 반영. collision 1건이 두 item 의 coverage 를 동시에 올린다 |
| `trigger-eval-method.md:47-50` | 판정관은 **동일 root 의 형제 description 만** 받는다 | collision 형제는 반드시 같은 root 에서 고른다. skill↔agent 교차 collision 은 판정 불가 |
| `.github/workflows/validate.yml:37` | `score.py --ci` 실행 | Phase 3 만 이 게이트에 영향 |
| **변경 없음 (열거만)** | `claude-code/skills/**`, `claude-code/agents/**` 본문 | 평가 대상일 뿐 수정하지 않음 |

## 경합 형제 확정 (§OQ1′ 해소 — 2026-07-22 승인)

선례 §OQ1′ 은 collision 이 **실재 경합 형제**를 지목할 것을 요구한다. 6건 전부 해소되었으므로 소유자 예외 승인은 불필요하다. 근거는 각 항목이 **자신의 description anti-trigger 에 스스로 선언한 경계**이며, 추정이 아니다.

**infra 4종** (`ywc-iac-author`, `ywc-infra-design`, `ywc-infra-optimize`, `ywc-infra-review`) — 서로가 최근접 이웃이므로 상호 collision 으로 구성한다.

**`ywc-auth-implement`** (skill root):

| 경합 형제 | 근거 (anti-trigger 원문) | collision prompt |
|---|---|---|
| `ywc-security-audit` | "Do not use for security code review after implementation" | "방금 구현한 로그인 인증 로직에 취약점 없는지 검토해줘" |
| `ywc-e2e-test-strategy` | "Do not use for E2E test authoring outside auth flows" | "로그인/로그아웃 플로우 E2E 테스트 전략 잡아줘" |

`ywc-plan` 은 anti-trigger 에 있으나 조건이 "unrelated to auth" 라 실제 경합이 아니므로 제외.

**`ywc-cloud-engineer`** (agent root):

| 경합 형제 | 근거 | collision prompt |
|---|---|---|
| `ywc-security-engineer` | cloud-engineer 는 reliability-lens review 만 소유. IAM 과도 권한은 security 축 | "terraform IAM 정책에 과도한 권한 없는지 봐줘" |
| `ywc-architect` | "Do not use for architecture / module-boundary judgment" | "인프라를 멀티리전으로 갈지 단일리전으로 갈지 판단해줘" |

`ywc-backend-coder` 는 경계가 선명(앱 로직 vs IaC)해 난이도가 낮으므로 예비 후보로만 둔다. `ywc-infra-design` 은 skill root 라 제외 — 판정관은 동일 root 형제만 받는다(`trigger-eval-method.md:47-50`).

**확인 사항**: `ywc-infra-engineer` 는 이 저장소에 **존재하지 않는다**. Terraform 저작은 `ywc-cloud-engineer` 단독 소유이므로 중복 우려 없음. 두 항목 모두 mechanical Jaccard collision 은 `[]` 로, 어휘 중복이 아닌 **의미 경합**이다.

## Done When

- `SKILL.md` Step 3 이 `signals.coverage.sufficient == false` 인 item 의 S1/A2 를 `"unmeasured"` 로 강제하고, 이전 run 값 carry-forward 를 금지한다.
- `score.py --target all --format json` 의 stderr 가 `[coverage] 0 items below minimum (of 60; ...)` 을 출력한다.
- `trigger-cases.json` 의 negative 가 **10 → 22건 이상**이며 그중 **12건 이상이 in-domain** 이다.
- 중복 case id 가 0건이다.
- `score.py --format json` 출력의 각 item 에 `signals.prose_lint` 가 존재한다.
- `score.py --ci` 가 exit 0 이고 **`history.mechanical.json` 에 git diff 가 없다**.
- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` 전량 통과, `bash scripts/validate.sh` exit 0.

> 선례 §AC12′ 에 따라 **S1/A2 점수 상승은 완료 조건이 아니다.** 백필된 6건의 S1 산출은 후속 `ywc-toolkit-eval` 판단-tier 실행에서 확인한다.

## Implementation Steps

### Phase 1 — 판정 규율 (문서 전용, PR 1)

파일: `SKILL.md`, `references/trigger-eval-method.md`

- [ ] `SKILL.md` Step 3 activation judge 에 **unmeasured 규율** 추가: 먼저 `signals.coverage.sufficient` 를 읽고, `false` 면 S1/A2 를 숫자가 아닌 `"unmeasured"` 로 반환하며 사유 1줄을 붙인다. precision/recall 을 지어내지 말고 이전 run 값을 가져오지도 말 것. unmeasured item 은 총점과 무관하게 backlog 에 진입한다
- [ ] `SKILL.md` Step 3 에 **judge 다중 시도** 추가(가이드 §5): activation judge 를 동일 입력으로 3회 실행하고 다수결. 3회가 갈리면 평균내지 말고 "descriptions genuinely ambiguous" 로 기록한다 — 격리 실행이 없는 현 단계에서 비결정성에 대응하는 유일한 수단
- [ ] `SKILL.md` Validation 체크리스트에 2줄 추가: (a) coverage 미달 item 의 S1/A2 가 `"unmeasured"` 인가, (b) activation judge 가 3회 실행되었는가
- [ ] `trigger-eval-method.md` 에 **Mechanical Coverage Signal** 절 신설: `COVERAGE_MIN_*` 상수와 `signals.coverage.sufficient` 를 명시하고, 산문 규칙(`:15`)과 기계 신호가 동일한 것임을 연결. **`score.py` 는 S1 을 산출하지 않는다**(선례 §AC1′)는 점을 함께 못박아 오해를 차단
- [ ] `trigger-eval-method.md` Case Taxonomy 에 **negative 작성 지침**: negative 는 off-domain(날씨·상식)이 아니라 **in-domain** 으로 쓸 것. off-domain 은 난이도가 낮아 precision 을 측정하지 못한다. 권장 유형 — 단순 설명 요청, 사소한 편집, 도구 조회, 개념 질문, 환경 오류 해석
- [ ] `trigger-eval-method.md` 에 **retired 보존 규칙**(가이드 §4): 은퇴 skill 의 case 는 삭제하지 말고 `"retired": true` 로 보존한다. model update 시 성능 저하를 감시하는 회귀 테스트로 남는다. Codex spec 의 "fixture 는 은퇴 후에도 regression suite 에 남긴다" 와 동일 정책임을 명시
- [ ] 본문 500줄 cap 유지 확인 (현재 `SKILL.md` 170줄)

### Phase 2 — fixture 보강 (PR 2)

파일: `evals/trigger-cases.json`

- [ ] coverage 미달 6건 백필 — item 당 positive 3 + collision 2. **collision 은 `expected`/`impostor` 양쪽에 가산되므로**(`score.py:260-262`) 실제 신규 case 수는 30건보다 적다. infra 4종은 상호 collision 으로 서로의 coverage 를 채운다
- [ ] 확정된 경합 형제(아래 §경합 형제 확정)로 collision 을 작성한다. **negative 로 대체하지 않는다**(선례 EC2)
- [ ] collision 은 **쌍으로** 작성 — 동일 prompt 가 owner 에게는 `positive`, impostor 에게는 `collision` 으로 등장해야 한다(`trigger-eval-method.md:15`)
- [ ] in-domain negative **12건 이상** 추가. `expected: null`, `kind: "negative"`, `note` 1줄(어떤 skill 이 오발동하기 쉬운지)
- [ ] 언어 분배 — 한국어/영어/일본어 혼합 (A4 multilingual 정책과 정합)
- [ ] **id 충돌 검사** — 기존 312건과 겹치지 않는지 스크립트로 확인(육안 불가)
- [ ] 백필 후 `[coverage] 0 items below minimum` 확인. **게이트는 `score.py` coverage 단독** — `validate.sh` 는 eval 픽스처를 커버하지 않는다(선례 W3)

### Phase 3 — prose lint (코드, PR 3)

파일: `scripts/score.py`, `scripts/test_score.py`, `SKILL.md`(1줄)

- [ ] 상수 3종 선언: `NOOP_PHRASES`(행동 무변화 exhortation — `write clean code`, `follow best practices`, `읽기 쉽게`, `가독성 좋게`, `適切に`), `NONDIRECTIVE_PHRASES`(권고체 — `is recommended`, `you may want to`, `권장됩니다`, `하는 것이 좋습니다`, `が望ましい`), `CONCRETE_ANCHOR_RE`(백틱 식별자 / 경로 / 숫자 / 대문자 도구명)
- [ ] **스캔 제외 규칙을 먼저 구현**(오탐 통제의 핵심): fenced code block 토글, 표 행(`|`), blockquote(`>`), heading(`#`), 링크 전용 라인. **Rationalization Defense 표는 "핑계"를 인용하는 구조**라 no-op 문구가 정상적으로 등장하므로 표 제외는 필수
- [ ] 판정: phrase 매치 **AND** 구체 anchor 부재
- [ ] `_prose_lint(text, line_offset)` → `{"noop_lines":[{line,text,phrase}], "nondirective_lines":[...]}`. line 번호는 **파일 기준**(frontmatter offset 보정) — backlog 가 `file:line` citation 을 요구
- [ ] `score_skill()` / `score_agent()` 에 `signals["prose_lint"]` 주입. **axis 계산식은 한 줄도 건드리지 않는다**
- [ ] `signals["coverage"]` 와 동일 톤의 주석: "informational only, never feeds an axis or the CI baseline"
- [ ] **오탐 calibration 게이트** — 히트를 item 별 집계, 상위 5개 육안 확인. 표본 정밀도 < 50% 이거나 60개 중 30% 초과 히트면 phrase bank / anchor 규칙을 조여 재실행. 통과 전 PR 금지. 최종 히트 수를 PR 본문에 기록
- [ ] `test_score.py` 추가: (a) no-op 검출, (b) 구체 anchor 있는 문장 **미**검출, (c) 표 행 / code fence 내부 **미**검출, (d) `prose_lint` 가 어떤 axis 값도 바꾸지 않음(동일 fixture 로 axes 스냅샷 비교)
- [ ] `SKILL.md` Step 2 signal 나열에 `prose_lint` 1줄 + "warning-only, never gates an axis"

## Verification

```bash
cd /Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit
E=.claude/skills/ywc-toolkit-eval

# --- Phase 2: coverage 0건 도달 (stderr 확인) ---
python3 $E/scripts/score.py --target all --format json >/dev/null

# --- Phase 2: 개별 item 확인 (선례 §AC1′ 의 검증 문법) ---
python3 $E/scripts/score.py --target claude-code/skills --item ywc-infra-design --format json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['claude-code/skills'][0]['signals']['coverage'])"

# --- Phase 2: negative 건수 + id 충돌 ---
python3 -c "
import json;from collections import Counter
c=json.load(open('$E/evals/trigger-cases.json'))['cases']
print('negatives:',sum(1 for x in c if x['kind']=='negative'))
print('dup ids:',[k for k,v in Counter(x['id'] for x in c).items() if v>1])"

# --- Phase 3: signal 존재 ---
python3 $E/scripts/score.py --target claude-code/skills --format json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(sum(1 for i in d['claude-code/skills'] if 'prose_lint' in i['signals']))"

# --- Phase 3: warning-only 계약의 기계적 증거 ---
#     주의: --ci 는 PASS 시 baseline 을 다시 쓴다 (validate.yml:33-34 의 의도된 동작).
#     exit code 만으로는 불충분 — baseline 무변경을 git 으로 확인해야 한다.
python3 $E/scripts/score.py --ci; echo "exit=$?"
git diff --exit-code $E/evals/history.mechanical.json \
  && echo "baseline UNCHANGED — warning-only 계약 충족" \
  || echo "baseline CHANGED — axis 를 건드렸다는 뜻. 즉시 원인 규명"

# --- 전체 (validate.sh 는 eval 픽스처를 커버하지 않음 — 선례 W3) ---
python3 $E/scripts/test_score.py
bash scripts/validate.sh
```

## Risks / Rollback

| Risk | 완화 |
|---|---|
| **Phase 2 이후 judge run 에서 S1 광범위 하락** | 의도된 **측정 정상화**. 현재 6건은 fixture 없이 점수가 매겨지고, in-domain negative 는 precision 을 처음으로 실측하게 만든다. scorecard 에 "coverage 백필 + in-domain negative 반영" 주석 필수. S1 은 judgment axis 라 baseline 밖 → CI 무영향 |
| ~~§OQ1′ 미해결로 Phase 2 착수 불가~~ | **해소됨** — 6건 전부 실재 경합 형제 확정. 소유자 예외 승인 불필요 |
| Prose lint 오탐이 backlog 오염 | Phase 3 calibration 게이트가 차단. axis 미반영이라 오탐이 점수를 훼손하지 않음 |
| `--ci` 가 baseline 을 조용히 갱신해 회귀 은폐 | Verification 의 `git diff --exit-code` 가드가 유일한 탐지 수단. **반드시 실행** |
| collision 쌍 한쪽만 추가 | coverage 가 positives/collisions 를 각각 세므로 누락 시 `sufficient=false` 로 드러남 |
| id 충돌로 fixture 파손 | Verification 의 중복 id 스크립트. 312건 규모라 육안 불가 |

**Rollback**: 세 Phase 는 독립 PR 이므로 개별 revert 가능.
- Phase 1: 문서 되돌리기 (코드/CI 영향 없음)
- Phase 2: 추가된 case 만 제거
- Phase 3: `_prose_lint()` 와 주입 2줄 삭제

## Handoff

Phase 1 → 2 → 3 순서. Phase 1 이 먼저인 이유는, 백필이 없는 상태에서도 **unmeasured 규율이 먼저 서 있어야** 6건의 허위 S1 이 즉시 멈추기 때문이다. 백필을 기다리는 동안에도 점수가 정직해진다.

격리 실행 runner(§5)와 ablation(§4)은 `docs/ywc-plans/codex-skill-eval-upgrade.md` 의 `Iteration 1~3 Amendments` 에서 확정된 계약(temporary home 격리, verifier registry, 상태 enum `PASS|FAIL|SKIPPED_UNAVAILABLE|ERROR|INCONCLUSIVE`, 6회 paired trial, 사람 승인 필수)을 claude-code 측으로 이식하는 별도 spec 으로 작성한다. **설계를 다시 하지 말 것.**
