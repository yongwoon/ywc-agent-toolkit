# 000057-010-test-pilot-sample-frame — Implementation Checklist

## Prerequisites

- [ ] Phase 000056이 완료·merge되었다 (hard gate).
- [ ] `enumerate-rd-rows.sh --self-check` → `PARITY OK: 46/46`.
- [ ] 부모 spec의 report-only audit이 착지한 커밋을 식별했고 그 git SHA를 확보했다 (AC8).

## Allowed Edit Scope

- [ ] `docs/ywc-plans/prune-report-rationalization-defense.md` (신규) 만 쓴다.
- [ ] `claude-code/skills/**`는 **읽기 전용**이다. variant는 `build-variant.sh`가 temp path에만 쓴다.

## Stop Conditions

- [ ] 부모 audit의 SHA를 확보할 수 없으면 **run을 시작하지 않는다** (AC8 — SHA 없이는 시작 거부).
- [ ] 층화 추출 제약(skill·stratum 당 ≤1행, stratum 당 ≥40개 skill)을 만족하는 80개 후보를 만들 수 없으면 멈추고 보고한다.
- [ ] 후보를 뽑기 위해 어떤 skill 파일이든 편집해야 한다면 멈춘다.

## Implementation Steps

- [ ] `docs/ywc-plans/prune-report-rationalization-defense.md`를 만들고 header에 **부모 audit의 git SHA**를 기록한다 (AC8).
- [ ] 46개 skill 전체에 `enumerate-rd-rows.sh`를 돌려 419개 행의 전체 프레임을 만든다.
- [ ] 프레임을 Stratum A(행 위치 1–4, pool 184)와 Stratum B(위치 5+, pool 235)로 나눈다.
- [ ] Stratum A에서 40개, Stratum B에서 40개를 뽑는다. 제약: **skill·stratum 당 최대 1행**, 각 stratum이 ≥40개 서로 다른 skill에 걸칠 것.
- [ ] 후보 80개를 `<file>:<start>-<end>` key로 report에 **dispatch 이전에** 기록한다.
- [ ] 후보별 시나리오를 결속한다: `evals/evals.json`이 있으면 그 `prompt`를 축자 재사용, 없으면 `description` trigger에서 합성. report에 기록한다. **`expected_output`은 읽지 않는다.**
- [ ] 80개 후보 각각에 `build-variant.sh`를 한 번씩 돌려 exit 0을 확인한다. exit 1(마지막 data row → header orphan)이 나온 후보는 같은 stratum·같은 제약으로 다시 뽑고, 교체 사실을 report에 기록한다.
- [ ] report에 `INCONCLUSIVE` 가능성과 ceiling(0.25) 규칙을 header에 명시해, dispatch task가 그것을 다시 판단하지 않게 한다.

## Task Verify

- [ ] `git cat-file -t <SHA>` → `commit` (header의 SHA가 실제 커밋)
- [ ] report의 후보 행 수 == 80, Stratum A 40 / Stratum B 40
- [ ] 어떤 `<file>`도 한 stratum 안에서 2번 나타나지 않는다
- [ ] 각 stratum의 distinct `<file>` 수 ≥ 40
- [ ] 80개 후보 전부에 대해 `build-variant.sh` exit 0
- [ ] 80개 후보 전부에 시나리오가 기록되어 있다

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `git diff --name-only`가 `docs/ywc-plans/prune-report-rationalization-defense.md` 외의 파일을 보이지 않는다 (AC2).
