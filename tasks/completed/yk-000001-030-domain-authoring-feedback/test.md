# Authoring feedback loops — scenarios

## AC-3 — repository-first clarification
1. Ask a question whose answer is present in repository files; verify repository evidence is consulted first.
2. Ask a question that remains unresolved after repository inspection.
3. Supply multiple prerequisites and verify the first unresolved prerequisite is asked alone.

Expected: repository-answerable facts are not re-asked; only one unresolved prerequisite question is presented, and existing approval gates remain intact.

## AC-3 — feedback and TDD seam
1. Review a public interface that supports a behavior test and a private helper that is not a public seam.
2. Record one caught and one missed feedback signal; run one behavior RED/GREEN/REFACTOR cycle before proceeding to a second behavior.

Expected: feedback records are minimal, the public seam is used, private helpers are not exposed, and the next behavior does not begin before the cycle completes. Writing Levers remove no-op wording, express positive goals, put conditions first, define observable completion, and point to canonical references. No runtime behavior is claimed from static source checks.
