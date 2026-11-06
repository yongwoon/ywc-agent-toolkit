# Codex distribution evidence

Evidence kind: source assertion and local helper execution. The source inventory contains 54 Codex skills and 10 TOML agents; the five root README locales and Codex catalogs report these counts and link the three Codex-only skills (`ywc-mission`, `ywc-retro`, `ywc-handoff`) and `ywc-cloud-engineer`.

The behavior suite runs selected-skill installs and agent-only installation with isolated temporary `CODEX_HOME` directories. These are local installer execution results and do not touch the user's installation directories. Eval IDs are checked for numeric uniqueness; upstream `source_id` references are checked where a fixture binds them to a bundle. Plugin files are regenerated from `codex/skills` by `scripts/sync-codex-plugin.sh` and compared with the source inventory.

Live Codex, model, and tool invocation behavior remains **UNVERIFIED**. Fixture expected traces and source assertions are not evidence of live agent behavior.
