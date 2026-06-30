Fixture ID: architect-happy-module-boundary
Agent: ywc-architect
Capture date: 2026-06-23
Source commit: 8adbd54

Status: DONE

Keep `.codex/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py` in the local Codex skill scripts directory; promoting it to `codex/skills/*` would violate the Local Codex evaluator boundary and weaken the local-only contract.

| Option | Benefits | Costs |
|---|---|---|
| Keep internal | Preserves evaluator ownership, keeps validator local-file based, stays aligned with sibling artifacts `score.py`, `test_score.py`, and `inventory_gate.py` | Less discoverable to end users; some duplication versus distributed skills |
| Distribute as skill | Higher visibility and reuse through normal skill install paths | Blurs product vs evaluator concerns, invites live-agent/network expectations, and creates an irreversible public contract for an internal harness |

Project evidence: the spec says the local Codex evaluator owns local Codex skill/agent evaluation and that the validator "must be local-file based and must not invoke live agents or networks." The current structure already groups evaluator-only logic together under the same local skill scripts directory with `score.py`, `test_score.py`, and `inventory_gate.py`, which is the strongest signal for module ownership and dependency direction.
