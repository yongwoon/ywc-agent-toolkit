# Preconditions and Detection

`--mode setup` 이 격리를 적용하기 전에 확인하는 precondition 과, port VAR / service 추출의 지원 범위·한계를 정의한다.

## Compose file 탐지 (FR-1.1)

worktree 디렉토리에서 다음 순서로 첫 번째 존재 파일을 compose 로 사용한다:

1. `docker-compose.yml`
2. `docker-compose.yaml`
3. `compose.yml`
4. `compose.yaml`

`--compose-file <path>` 로 명시 override 가능. compose 가 없으면 **no-op (exit 0)** — "no docker — skipping isolation" 출력, `.env` 미작성 (AC4). 이전 persist 가 남아 있으면 삭제한다("compose removed — clearing port record").

## Port-var source 우선순위 (FR-2)

1. `--port-vars VAR1,VAR2` 또는 `--port-vars VAR1=PORT,VAR2=PORT` (명시 인자) — 최우선. 현재 allocation 은 값의 base port 를 재사용하지 않고 VAR 이름만 사용한다.
2. compose `${VAR:-NNNN}` short-syntax auto-detect — 기본.

> ⚠️ **override 시 hardcoded-port(AC5) 검사 생략:** `--port-vars` 로 VAR 을
> 명시하면 auto-detect 의 hardcoded-port fail-loud(AC5) 분기를 거치지 않는다.
> 호출자가 격리 대상을 책임진다. 명시한 VAR 외에 compose 에 hardcode 된 port 가
> 남아 있으면 그 port 는 격리되지 않으니 주의한다.

## env-var 매핑 지원 범위 (§A1.W)

| 형태 | 예시 | 지원 |
|---|---|---|
| short-syntax env-var | `"${APP_PORT:-3000}:3000"` | ✅ auto-detect |
| hardcoded | `"3000:3000"` | ❌ → **fail-loud** (AC5) |
| long-syntax | `published: "${APP_PORT:-3000}"` | ❌ 미탐지 — `--port-vars` 로 명시 |
| default 없는 var | `"${APP_PORT}:3000"` | ❌ base port 추출 불가 — 별도 경고 |
| override 파일 | `docker-compose.override.yml` | ❌ 미탐지 |

hardcode 된 port 가 감지되면 **절대 silent 하게 진행하지 않고** exit 1 로 보고한다 — 사용자가 격리 없이 진행할지 / compose 를 고칠지 결정한다 (AC5).

## YAML 파서 우선순위 (§A2.2 / §A3.W)

service 명 추출과 port 탐지는 동일한 파서 우선순위를 따른다:

1. **primary**: `python3 -c "import yaml"` (macOS / Ubuntu 기본 설치).
2. **fallback**: section-aware awk — `services:` 블록 진입 후 2-space 들여쓰기 키만 추출하고 다음 root 키에서 중단. bare `grep '^  [a-z]'` 는 `x-extension` 의 `restart:` 등을 service 로 오인하므로 금지.
3. **파서 불가**: persist 의 stale 검사를 skip 하고 persisted map 을 신뢰하되, stdout 에 WARN 출력("YAML parser unavailable — skipping stale check, trusting persisted port map") — silent 아님 (§A4.W).

## 플랫폼 port-check 도구 (§A4.1)

`check_port_in_use` 는 다음 우선순위로 분기한다:

| 도구 | 플랫폼 | 비고 |
|---|---|---|
| `ss` | Linux (`iproute2`) | 1순위 |
| `lsof` | macOS / Linux | 2순위 — 이 repo 환경(darwin) 기본 |
| `netstat` | fallback | 최후 |

boundary-safe 매칭(`:PORT(\s|$)`)으로 `20300` 이 `203000` 에 오탐되지 않게 한다.

## `.env` vs shell export 우선순위 (§A1.W)

- setup 은 worktree-local `.env` 에 marker block 으로 `COMPOSE_PROJECT_NAME` + port VAR 을 기록한다(다른 줄은 보존).
- shell 에 `COMPOSE_PROJECT_NAME` 이 export 되어 있으면 `.env` 를 **override** 한다(특히 CI). setup 은 이를 감지해 WARN 한다. teardown 은 `-p` 를 명시하므로 영향받지 않는다.

## gitignore 보장 (FR-4.2)

`.env` 와 `.ywc-docker-ports` 는 commit 되면 안 된다. setup 은 이 둘이 git 추적 대상인지 `git check-ignore` 로 확인하고, ignore 되어 있지 않으면 **경고만** 한다 — 추적 `.gitignore` 를 수정하면 git diff 가 오염되므로(NFR-1) 자동 수정하지 않는다.
