# Report-Only Skill Audit Workflow

## Contract

`ywc-skill-author --audit` is a bounded, read-only entry point. It can inspect
one skill, a selected group, or a bundle, but it never creates a second audit
skill, changes an audited target, authorizes deletion, or invokes an executor.

Run the mechanical report first:

```bash
bash scripts/audit-skills.sh --root <bundle-skills-root> \
  --counterpart-root <other-bundle-skills-root> [--near-line-cap 1..500]
```

The command exits `2` for invalid input and `0` for every valid audit, even
when findings are present. It always emits these sorted sections: Inventory,
Near Line Cap, Unpointed Local References, Force-load References, Declared
Sibling Calls, and Counterpart Coverage. Empty sections print `none`.

## Evidence Before Judgment

Treat script output as a queue, not a verdict. A near-line-cap result can be a
necessary ordered procedure; an unpointed reference can be test-only; a missing
counterpart can be platform-specific. Record the evidence, inspect the target
context, then choose one of: retain, investigate with a deletion test, or a
documented exception. Text similarity never proves semantic duplication.

## Deletion-Test Protocol

1. Select one bounded instruction and representative prompt(s).
2. Record baseline procedure adherence, safety gates, and artifact shape.
3. Remove only that instruction in an isolated change.
4. Run the same prompt(s) and compare observable results.
5. Retain, revert, or escalate; never apply a removal automatically.

Reject a removal when it changes trigger precision, required verification,
handoff behavior, or safety gates. A failed experiment is useful evidence and
must be reverted before another candidate is tested.

## Role and Parity Review

Classify every changed skill as interface, orchestrator, or discipline.
Interface skills may hand off to orchestrators or discipline skills;
orchestrators may delegate to discipline skills; discipline skills must not
invent peer orchestration. A same-tier call is allowed only when documented as
an exception in the cross-skill graph.

Compare Claude Code and Codex by user-visible workflow, safety and verification
gates, and handoff conditions. Invocation syntax, required Codex metadata, and
localized README language are intentional platform differences. All other
differences require a documented reason.
