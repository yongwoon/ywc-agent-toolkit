# HOL Plugin Scanner — FILE_MAGIC_MISMATCH 근본 억제

## Goal

`HOL Plugin Scanner / scan` CI 체크가 `skills/ywc-security-audit/agents/openai.yaml`에 대한
`FILE_MAGIC_MISMATCH` finding으로 반복 실패하는 문제를, 스캐너 액션이 공식 지원하는
저장소 소유 설정(`trust_repository_policy` + `.plugin-scanner.toml`)을 통해 이 규칙 하나만
좁게 억제함으로써 근본 해결한다.

## Why

- 이 alert는 `refs/heads/main`에 2026-06-25 04:38부터 존재했고, 과거 PR #144~#174 30개 이상에서
  동일하게 재현된 안정적 오탐이다.
- 구조가 동일한 다른 `openai.yaml` 파일들(`ywc-verify-done`, `ywc-setup`, `ywc-create-pr` 등)은
  전혀 flag되지 않아, Magika(ML 파일타입 분류기)가 이 파일의 특정 바이트 패턴만 오분류하는 것으로
  판단된다.
- `plugin.json`의 나머지 6개 finding(`PLUGIN_JSON_INTERFACE_ASSET_*`, `PLUGIN_JSON_RECOMMENDED_HOMEPAGE`)은
  `hol-guard` 소스(`checks/manifest.py:420`)에서 `severity=Severity.INFO`로 정의되어 있어
  `fail_on_severity: high` 게이트 실패의 원인이 될 수 없음을 코드로 확인했다 — 실제 게이트 실패의
  유일한 high-severity 원인은 `FILE_MAGIC_MISMATCH`다.
- PR #177에서는 이 실패를 PR #175 선례에 따라 "노이즈로 간주하고 병합"으로 우회했으나, 매 PR마다
  동일한 판단을 반복하는 것은 지속 가능하지 않다.

## Existing Constraints Touched

- **`hashgraph-online/ai-plugin-scanner-action` 설정 로딩 경로** (`hol-guard` 저장소,
  `src/codex_plugin_scanner/config.py`) — `load_scanner_config(plugin_dir, config_path, auto_discover)`는
  `config_path`가 없을 때 `plugin_dir` 내부에서 `.plugin-scanner.toml` 또는
  `.codex-plugin-scanner.toml`을 자동 탐색한다 (`DEFAULT_CONFIG_FILES`, `config.py:27`). 이 저장소의
  워크플로는 `plugin_dir: "plugins/ywc-agent-toolkit"`(`.github/workflows/hol-plugin-scanner.yml:23`)이므로,
  설정 파일은 반드시 `plugins/ywc-agent-toolkit/.plugin-scanner.toml`에 위치해야 한다(저장소 루트 아님).
- **`trust_repository_policy` 게이팅** (`src/codex_plugin_scanner/_scanner_commands.py:66-76`,
  함수 `_resolve_policy_profile`) — `trust_repository_policy=False`일 때는
  `auto_discover=False`로 강제되어 `.plugin-scanner.toml`이 존재해도 전혀 로드되지 않는다.
  액션의 `action.yml` 기본값은 `trust_repository_policy: "false"`이며, 현재 워크플로
  (`.github/workflows/hol-plugin-scanner.yml`)는 이 입력을 지정하지 않아 기본값(`false`)이
  적용되고 있다 — 이것이 기존에 `.plugin-scanner.toml`을 추가해도 무시될 근본 이유다.
- **`disabled_rules` 적용 방식** (`src/codex_plugin_scanner/suppressions.py:9-33`, 함수
  `apply_suppressions`) — `config.disabled_rules`에 포함된 `rule_id`는 `include_finding()`에서
  완전히 필터링되며, 해당 check의 findings가 전부 제거되면 `passed=True`로 재기록된다
  (`suppressions.py:31-38`). **다른 rule_id에는 영향을 주지 않는다** — 좁은 스코프의 억제임을
  소스로 확인했다.
- **`plugins/ywc-agent-toolkit` 자동 동기화** (`scripts/sync-codex-plugin.sh`) — 이 스크립트는
  `$DEST_DIR`(`plugin_root/skills`)를 `rm -rf` 후 재생성하고, `.codex-plugin/plugin.json` 및
  `README.md`/`LICENSE`/`SECURITY.md`/`.codexignore`만 개별 복사한다(`sync-codex-plugin.sh:47-56`,
  `:59-68`). `plugin_root` 루트에 새로 추가하는 `.plugin-scanner.toml`은 이 스크립트가 건드리는
  경로 목록에 없으므로 **동기화 시 삭제되거나 덮어써지지 않는다** — 충돌 없음을 확인했다.

## Out of Scope

- `plugin.json`의 INFO 심각도 6개 항목(`PLUGIN_JSON_INTERFACE_ASSET_SCREENSHOTS`,
  `_LOGO`, `_COMPOSERICON`, `_TERMSOFSERVICEURL`, `_PRIVACYPOLICYURL`,
  `PLUGIN_JSON_RECOMMENDED_HOMEPAGE`) — 이번 게이트 실패의 원인이 아니므로 처리하지 않는다.
  (원한다면 `homepage` 필드 추가만 별도의 위생 개선 작업으로 처리 가능하나, 이 계획에는 포함하지 않는다.)
- `FILE_MAGIC_MISMATCH` 이외의 다른 rule을 `disabled`/`severity_overrides`에 추가하는 것 —
  향후 실제 high-severity 위반을 놓치지 않기 위해, 이번에는 검증된 오탐 1건만 좁게 억제한다.
- `openai.yaml` 파일 내용 자체를 수정해 Magika 분류를 바꾸려는 시도 — 내용을 임의로 바꿔
  ML 분류기의 판정을 우회하는 것은 근거 없는 도박이며, 의미 없는 diff를 만든다.
- 액션의 다른 입력값(`min_score`, `fail_on_severity`, `profile`, `cisco_skill_scan` 등) 변경.
- `.plugin-scanner.toml`을 저장소 루트에 두는 방식 — `plugin_dir` 기준 자동 탐색 경로이므로 대상이
  아니다.

## Security Consideration

`trust_repository_policy: true`는 액션 공식 설명상 "저장소가 소유한 스캐너 설정/baseline이
Action 판정에 영향을 주도록 허용"하는 신뢰 범위 확장이다. 즉 이 값을 켜면 이후
`plugins/ywc-agent-toolkit/.plugin-scanner.toml`에 추가되는 어떤 `disabled`/`severity_overrides`
항목도 CI 판정에 그대로 반영된다. 이번 계획은 그 파일의 억제 대상을 `FILE_MAGIC_MISMATCH`
단일 rule로 명시적으로 제한하지만, **향후 이 파일에 대한 변경은 일반 코드 리뷰에서 "왜 이
rule을 추가로 억제하는지" 근거를 반드시 확인**해야 한다는 점을 남겨둔다. (자동 강제 장치는
이번 계획 범위 밖 — 필요 시 별도로 CODEOWNERS 지정 등을 검토할 수 있다.)

## Files to Touch

1. `.github/workflows/hol-plugin-scanner.yml` — `scan` job의 `HOL Plugin Scanner` step `with:`에
   `trust_repository_policy: "true"` 추가.
2. `plugins/ywc-agent-toolkit/.plugin-scanner.toml` (신규) — `[rules] disabled = ["FILE_MAGIC_MISMATCH"]`
   와, 왜 이 규칙만 억제하는지 근거를 남기는 TOML 주석.

## Implementation Steps

- [ ] 1. `.github/workflows/hol-plugin-scanner.yml`의 `HOL Plugin Scanner` step `with:` 블록에
      `trust_repository_policy: "true"`를 추가한다 (다른 입력값은 변경하지 않음).
- [ ] 2. `plugins/ywc-agent-toolkit/.plugin-scanner.toml`을 새로 작성한다:
      ```toml
      # HOL Plugin Scanner 저장소 소유 설정.
      # FILE_MAGIC_MISMATCH만 좁게 억제한다 — skills/ywc-security-audit/agents/openai.yaml에 대한
      # Magika(ML 파일타입 분류기) 오탐으로, 구조가 동일한 다른 openai.yaml 파일들은 flag되지 않는다.
      # 2026-06-25부터 main에 존재했고 과거 PR #144~#174 30개 이상에서 동일 재현됨.
      # 다른 rule을 이 목록에 추가하기 전에 반드시 실제 오탐임을 근거로 확인할 것.
      [rules]
      disabled = ["FILE_MAGIC_MISMATCH"]
      ```
- [ ] 3. 로컬에서 스캐너를 직접 실행해 두 변경을 사전 검증한다 (CI 대기 없이 실패 여부를 먼저 확인):
      ```bash
      python3 -m venv /tmp/plugin-scanner-venv
      /tmp/plugin-scanner-venv/bin/pip install plugin-scanner
      /tmp/plugin-scanner-venv/bin/plugin-scanner scan plugins/ywc-agent-toolkit \
        --trust-repository-policy \
        --fail-on high --min-score 80 --format text
      ```
      (CLI 플래그명이 다를 경우 `plugin-scanner scan --help`로 정확한 플래그를 확인 후 실행 —
      action.yml의 `TRUST_REPOSITORY_POLICY` env var가 CLI에서 어떤 플래그/옵션으로 매핑되는지
      로컬 실행 전에 `--help` 출력으로 재확인할 것.) 성공 조건: `FILE_MAGIC_MISMATCH`가 결과에서
      사라지고, 종료 코드가 0이며, 다른 6개 INFO finding은 여전히 보고되지만 게이트 실패를
      유발하지 않는지 확인한다.
- [ ] 4. 두 파일을 커밋한다 (커밋 메시지 예: `ci: suppress known FILE_MAGIC_MISMATCH false positive in HOL Plugin Scanner`).
- [ ] 5. 브랜치를 push하고 draft PR을 열어 `HOL Plugin Scanner / scan` 체크가 그린으로 통과하는지
      실제 GitHub Actions 실행으로 확인한다. `gh pr checks <pr>`로 확인.
- [ ] 6. 같은 PR의 SARIF/Job Summary 또는 `gh run view --log`로, `FILE_MAGIC_MISMATCH`는 사라지고
      나머지 rule(예: 의도적으로 존재하는 INFO 항목들)은 여전히 보고됨을 재확인해, 억제 범위가
      좁게 유지되었는지 검증한다.
- [ ] 7. 확인 후 PR을 병합한다 (이 작업은 스코프상 자체 PR로 별도 진행 — 사용자 승인 하에).

## Verification Commands

- `bash scripts/validate.sh` — 저장소 구조/신택스 회귀 없는지 확인 (이번 변경은 `codex/skills`나
  `.codex-plugin/plugin.json`을 건드리지 않으므로 pre-commit 훅의 sync 로직은 트리거되지 않지만,
  전체 검증은 습관적으로 실행).
- `gh pr checks <pr-number>` — 새 PR에서 `HOL Plugin Scanner / scan`이 `pass`로 전환되는지 확인.
- `gh api repos/yongwoon/ywc-agent-toolkit/code-scanning/alerts --paginate -q '.[] | select(.rule.id=="FILE_MAGIC_MISMATCH" and .state=="open")'` —
  병합 후 해당 alert가 더 이상 새로 열리지 않는지 후속 확인(기존 7개 alert 자체를 자동으로
  닫지는 않으므로, 기존 open alert는 GitHub UI에서 수동으로 "Dismiss"하거나 다음 스캔에서
  자연 소멸하는지 별도 확인 필요 — Out of Scope로 명시했던 항목은 아니지만 참고용 후속 조치).

## Risks / Rollback

- **Risk 1 — 신뢰 범위 확장.** `trust_repository_policy: true`는 저장소 소유 설정이 CI 판정에
  영향을 주도록 허용한다. 완화: `.plugin-scanner.toml`의 `disabled` 목록을 `FILE_MAGIC_MISMATCH`
  하나로 제한하고, 이후 이 파일을 건드리는 모든 PR은 일반 코드 리뷰에서 억제 사유를 확인한다.
- **Risk 2 — CLI 플래그명 불일치로 로컬 사전 검증 실패.** Implementation Step 3에서
  `--trust-repository-policy`는 추정 플래그명이며 실제 CLI 옵션명과 다를 수 있다. 완화:
  `plugin-scanner scan --help`로 사전 확인 후 실행 — 이는 계획 문서 안의 방어적 지시사항이며,
  실행 시점에 실제 옵션을 확인하는 것으로 충분히 완화된다.
- **Rollback**: 두 파일(`hol-plugin-scanner.yml`의 추가 입력값, `.plugin-scanner.toml`)을
  되돌리면 즉시 이전 상태(매번 실패, PR #175/#177 선례로 수동 우회)로 복귀한다. 삭제만으로
  롤백이 완료되며 부수 효과 없음.

## Acceptance Criteria

- `.github/workflows/hol-plugin-scanner.yml`에 `trust_repository_policy: "true"`가 명시적으로
  설정되어 있다.
- `plugins/ywc-agent-toolkit/.plugin-scanner.toml`이 존재하고 `[rules] disabled = ["FILE_MAGIC_MISMATCH"]`
  만 포함한다(다른 rule을 disable하지 않음).
- 새 PR에서 `HOL Plugin Scanner / scan` 체크가 `pass`로 전환됨을 실제 CI 실행으로 확인했다.
- 같은 실행에서 `FILE_MAGIC_MISMATCH` 이외의 finding(INFO 6종)은 여전히 보고되어, 억제 범위가
  하나의 rule로 한정되었음을 확인했다.

## Confidence Gate

Aggregate: 91/100 — PROCEED
(Scope 95 / Architecture 85 / Evidence 95 / Reuse 90 / Root cause 90 — weakest: Architecture, 이
저장소 최초의 `.plugin-scanner.toml`이지만 액션이 공식 지원하는 메커니즘을 그대로 사용)
