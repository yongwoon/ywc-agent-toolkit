# task: 000045-010-infra-agent-lens-extensions

## Prerequisites
- [ ] `000044-020` 완료(lens 문서 존재)

## Allowed Edit Scope
security-engineer / performance-engineer 에이전트 파일(CC+Codex)과 신규 reference 2종만.

## Stop Conditions
- 기존 description 트리거를 덮어써 앱-보안/앱-성능 라우팅이 깨질 위험이 있으면 중단 후 보고.

## Implementation Steps
- [ ] `references/iac-security.md` 저작 — IaC 오구성 taxonomy(공개 버킷·개방 SG·IAM 와일드카드·state 시크릿), lenses/security.md와 정합
- [ ] `references/finops.md` 저작 — right-sizing·예약/스팟·미사용 리소스·데이터 전송 비용
- [ ] `claude-code/agents/ywc-security-engineer.md` description에 IaC 트리거 append + iac-security.md 링크
- [ ] `claude-code/agents/ywc-performance-engineer.md` description에 FinOps 트리거 append + finops.md 링크
- [ ] Codex .toml 2종 동기 반영

## Task Verify
- [ ] `test -f references/iac-security.md && test -f references/finops.md`

## Verification
- [ ] `bash scripts/validate.sh` exit 0
