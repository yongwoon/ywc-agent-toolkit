# Bundle distribution integration — scenarios

## AC-10 — catalogs, locale, and plugin sync
1. Add the completed new-skill/agent bundle to root and Codex skill/agent catalogs, localized README files, and actual counts.
2. Check Tier 1 locales, openai.yaml metadata, unique numeric skill evaluation IDs with upstream `source_id`, and non-empty agent `expectations`.
3. Regenerate the plugin from source and compare generated contents with source.

Expected: new entries appear exactly once, counts match actual inventory, required locale/metadata/eval fields validate, and plugin output is synchronized rather than copied from upstream.

## AC-10 — install and evidence boundary
1. Use temporary `CODEX_HOME` to list and selected-install each new skill and perform agent-only installation.
2. Run contract and behavior fixtures plus repository validation. Keep source assertions, expected traces, extracted runnable recipe execution, existing helper execution, and live model evidence separately labeled.

Expected: selected installs do not touch user directories; supported deterministic checks pass; unavailable runtime tools/model traces are UNVERIFIED rather than runtime PASS. Failure modes covered here are missing upstream paths/locales and unavailable tools; behavior-specific remote deletion, handoff safety, worktree, mission, scope-evidence, and convergence failures stay with their owning tasks.
