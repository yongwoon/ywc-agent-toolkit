# Port Allocation Strategy

`ywc-docker-isolate` 가 worktree 별 host port block 을 **결정론적으로** 도출하는 규칙을 정의한다. 모든 값은 task 명의 순수 함수이며, 중앙 registry 나 runtime coordination 이 없다.

## Formula

```text
port = 20000 + (hash(sanitized_task_name [+ salt]) % 100) * 100 + var_index
```

| 요소 | 값 | 근거 |
|---|---|---|
| `PORT_BASE` | `20000` | ephemeral high-range — well-known port 충돌 최소 (FR-3.2) |
| block | `hash % 100` → `0..99`, `* 100` | 동시 worktree 최대 100개 수용 |
| block width | `100` | stack 당 격리 대상 port 최대 100개 |
| `var_index` | 정렬된 target VAR 의 0-based index | 같은 block 내 port 분리 |

결과 범위는 `20000`–`29999`. block `k` 는 `20000 + k×100` 부터 `20000 + k×100 + 99` 까지를 차지한다.

## `var_index` — 정렬 규칙

격리 대상 port VAR 을 **`LC_ALL=C sort`** (ASCII, 대소문자 구분) 한 0-based index 를 `var_index` 로 쓴다. 예: VAR `APP_PORT`, `DB_PORT` → `APP_PORT=...+0`, `DB_PORT=...+1` (`A` < `D`).

- spec §A1.4 의 "service_index" 와의 관계: compose 가 service 당 port VAR 하나를 노출하는 전형적 형태에서는 정렬된 VAR index 가 정렬된 service index 와 일치한다. 본 구현은 **VAR 명 정렬**을 1차 기준으로 삼아 multi-VAR service 에서도 index 충돌이 없도록 한다(persist 예시 `APP_PORT=20300 / DB_PORT=20301` 와 동일 결과).
- 격리 대상 VAR 수가 **block width(100)를 초과**하면 인접 block 침범을 막기 위해 **fail-loud** 한다 (§A1.4 off-by-one 방지).

`LC_ALL=C` 정렬 예시: 대소문자 혼재 시 ASCII 코드 순서이므로 대문자가 앞선다 — `WebApp`(`W`=0x57) < `db`(`d`=0x64).

## Salt chain (first-allocation collision)

도출한 block 의 어떤 port 라도 이미 점유돼 있으면(`check_port_in_use`, §A4.1), **task 명 파생 고정 salt sequence** 로 다음 후보를 결정론적으로 고른다.

```text
hash(task), hash(task-alt1), hash(task-alt2), hash(task-alt3), hash(task-alt4)
```

- chain depth 는 **최소 5** (`SALT_CHAIN` 상수). 두 task 가 연속 salt level 에서 동시에 충돌할 확률은 각 단계 독립 가정 시 약 `(1/100)^n` 로 급감한다.
- sequence 를 모두 소진하면 **fail-loud** (runtime 에서 발견한 "다음 빈 block" 으로 이동 금지 — 이는 NFR-2/AC2 를 위반한다).
- salt 는 **first-allocation 에서만** 관여한다. 재실행 reproducibility 는 `.ywc-docker-ports` persist read-back 이 보장하며(§A3.1), 이때 hash/salt 는 재도출되지 않는다.

## Hex hash 와 modulo bias

hash 는 `md5`(macOS) / `md5sum`(Linux) / `cksum`(fallback) 의 hex digest 앞 8자리를 십진 변환해 `% 100` 한다.

- `2^32 % 100 = 96` 이므로 `0..95` 가 `96..99` 보다 미세하게 더 자주 선택되는 **modulo bias 가 잔존**한다. hex digest 사용으로 완화되나 완전 제거되지는 않는다.
- block 충돌은 드물고, 충돌 시 salt chain 이 결정론적으로 분리하므로 실무 영향은 무시할 수준이다.

## Determinism guarantee (AC2)

- **first allocation**: block = `hash(task)`; 충돌 시 salt chain.
- **re-run**: `.ywc-docker-ports` 를 verbatim read-back → 항상 동일 port (외부 squatter 와 무관). 반환 전 모든 `*_PORT` 를 live-check 하여 squatter 점유 시 fail-loud (AC13).
- 서로 다른 task 명은 서로 다른 순수 함수 입력이므로 동시 worktree 가 절대 수렴하지 않는다 (NFR-2).
