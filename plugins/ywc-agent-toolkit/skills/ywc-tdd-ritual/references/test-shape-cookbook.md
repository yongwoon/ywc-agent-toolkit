# Test Shape Cookbook

Pick the right shape of test for the behavior you are about to implement. The wrong shape produces tests that pass while the production code is broken (or tests that fail for reasons unrelated to the production code).

## State vs. Interaction

| Behavior class | Shape | Example |
|---|---|---|
| Pure function | **State assertion** — call the function, assert the return value | `expect(addTax(100, 0.1)).toBe(110)` |
| Side-effectful function with a return | **State + boundary** — call the function, assert return, assert the boundary received the expected payload | `await saveUser(u); expect(db.insert).toHaveBeenCalledWith({…})` |
| Side-effectful function with **no** return | **Interaction** — call the function, assert the boundary received the expected payload | `await logEvent('signup'); expect(transport.send).toHaveBeenCalledWith({type:'signup'})` |
| Object lifecycle (constructor, mutator, query) | **State after sequence** — drive the object through the sequence, assert the final state | `const cart=new Cart(); cart.add(item); expect(cart.total).toBe(100)` |
| Event listener / callback | **Interaction with explicit trigger** — wire the listener, fire the trigger, assert the callback received what was expected | `emitter.on('change', cb); emitter.emit('change', payload); expect(cb).toHaveBeenCalledWith(payload)` |

**Rule:** prefer state assertions to interaction assertions whenever the function returns a value. Interaction tests are coupled to the implementation's structure and break under harmless refactors.

## Unit vs. Integration

| Scope | When to pick | Trade-off |
|---|---|---|
| **Unit** (one module, real collaborators where cheap) | Logic-heavy code; pure algorithms; per-branch coverage | Fast, but boundary issues hide |
| **Integration** (multiple modules, real cross-module wiring) | Glue code; controller-service-repository chains; routing | Slower, but catches the bugs unit tests miss |
| **End-to-end** (real process, real HTTP, real DB) | Critical user flows; pre-merge smoke; release gates | Slowest and flakiest, but the only test that reflects production |

**Rule of thumb:** if the unit test passes a value through 3+ collaborators by mocking each, the test is reading too narrow a slice. Promote to integration.

## Snapshot vs. Assertion

| Shape | When | Risk |
|---|---|---|
| **Explicit assertion** (per-field equality) | Always preferred — every assertion is intentional | Verbose for large payloads |
| **Snapshot** (serialize and diff) | Only when the payload is large *and* every field is part of the contract | Snapshots that include incidental data (timestamps, ids) become noise that everyone re-blesses without reading |

**Rule:** snapshots are appropriate for rendered output that a human would visually compare (e.g., SVG, formatted markdown). Snapshots are not appropriate for object payloads — write the explicit assertion.

## Time, Randomness, Network

| Dependency | Test seam |
|---|---|
| Wall clock | Inject a clock interface; pass a fixed `Date` in the test |
| `Math.random` / UUID | Inject a generator; pass a deterministic sequence |
| HTTP client | Inject the client; pass a stub that returns canned responses, **not** a real HTTP server |
| Database | Use a real DB in integration tests; never mock at the ORM call level in unit tests of the service layer (use a fake repository instead) |
| Filesystem | Use `memfs` or a temp dir; never mock individual `fs.read` calls in business logic |

**Anti-pattern:** mocking `Date.now()` globally. It leaks across tests. Inject the dependency.

## What to test, what not to test

| Behavior | Test? | Why |
|---|---|---|
| The public contract (inputs → outputs) | **Yes** | This is what the test exists for |
| Branch coverage of decision points | **Yes** | One test per branch (happy + each error / edge) |
| Idempotency, ordering, retry behavior | **Yes** | The places production failures most often hide |
| Private helpers | **No, indirectly** | Test through the public contract that depends on them |
| Implementation details (e.g., which loop variant the function uses internally) | **No** | Couples the test to the implementation; breaks under refactor |
| Framework / library code (e.g., that `Array.map` works) | **No** | Wastes time; trust the platform |
| Configuration files (constants, env keys) | **No, unless logic** | Test the *logic that reads* the config, not the config values themselves |

## Test-naming convention

Pick one shape per project and stick to it. The Korean / Japanese / English mix is fine as long as the convention is consistent within a project.

| Convention | Example |
|---|---|
| `it("<does X> when <condition>")` | `it("rejects offset > total when paginating", …)` |
| `describe("<unit>") > it("<behavior>")` nesting | `describe("Pagination") > it("rejects offset > total", …)` |
| Korean intent-first | `it("offset 가 total 보다 크면 400 을 반환한다", …)` |

The test name must let a future reader infer the production behavior **without reading the test body**.

## When the test is hard to write

| Symptom | What the test is telling you |
|---|---|
| Need to mock 5+ collaborators | Module has too many responsibilities; split it |
| Setup is 50+ lines for a unit test | Setup is the actual API; expose a builder or factory |
| Need to mock the unit under test | The module is being tested through itself — find the seam |
| Test name needs "and" | Two behaviors — split into two tests |
| Test needs to assert ≥ 5 unrelated outputs | Function has too many side effects — split |

In every row, the test is correct and the production code design is the problem. Listen to the test.

## Anti-shapes

| Anti-shape | Why bad |
|---|---|
| `it('works', …)` | No intent; future readers cannot infer the behavior |
| Test that calls the function and never asserts anything | Passes regardless; gives false coverage |
| Test that mocks `console.log` and asserts the log message | Couples to implementation; first refactor that changes the log breaks the test |
| Test that loops over an array of inputs without per-input naming | First failure obscures which input caused it; split into one test per case (or use parameterized table tests with explicit names) |
| Test that depends on test order (uses module-level `let` mutated by previous tests) | Flaky under parallel execution; first reorder breaks it. Move state into the test or a `beforeEach`. |
