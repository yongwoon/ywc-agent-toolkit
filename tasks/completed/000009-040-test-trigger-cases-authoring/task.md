# 000009-040-test-trigger-cases-authoring — 구현 체크리스트

## Prerequisites
- [ ] `000009-010` 완료(커버리지 게이트 존재)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` 만

## Stop Conditions
- `expected`/`impostor` 가 실존하지 않는 항목명을 가리키면 중단·수정
- 어떤 항목이 최소치를 못 채우면 보고(누락 0 이 목표)

## Implementation Steps
- [ ] 50항목 인벤토리 확보: `ls -d claude-code/skills/ywc-*/ ; ls claude-code/agents/ywc-*.md`
- [ ] reviewer 계열(typescript/python/go reviewer 등) 페어 collision 우선 작성
- [ ] executor 계열(sequential/parallel) 및 PR 라이프사이클(commit/create-pr/finish-branch/handle-pr-reviews) 페어 작성
- [ ] 나머지 전 항목에 positive ≥3, collision ≥2(impostor 명시), 클러스터별 negative ≥1
- [ ] 각 collision 은 owner positive 와 페어(동일 프롬프트)로 구성

## Task Verify
- [ ] `python3 -c "import json;json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))"` 유효 JSON
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` 커버리지 요약 "0 items below minimum"

## Verification
- [ ] `bash scripts/validate.sh` 통과
