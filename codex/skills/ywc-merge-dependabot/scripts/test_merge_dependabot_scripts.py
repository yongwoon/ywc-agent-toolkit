#!/usr/bin/env python3
"""Tests for the Codex copy of check-base-required-checks.sh, the Step 3a gate
block of SKILL.md (run through the shared Codex resolver), and the SKILL.md
merge-safety contract.

Stdlib only. `gh` and `sleep` are shimmed onto PATH: the gh stub answers from
the GH_STUB_MODE environment variable and appends every call to GH_STUB_LOG,
so no network is touched and no real time is slept.
"""
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_CHECK = HERE / "check-base-required-checks.sh"
SHARED_SCRIPTS = HERE.parents[1] / "scripts"
RESOLVER_FILES = ("select-resolver-launcher.sh", "resolve-bundle-executable.sh", "resolve-bundle-executable.py")
GATE_MARKER = "gh pr checks {number} --required 2>&1"
RESOLVER_SELECT = ('RESOLVER_LAUNCHER="$(bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/select-resolver-launcher.sh" '
                   '2>&1)" || { echo "BLOCKED: ${RESOLVER_LAUNCHER#BLOCKED: }" >&2; exit 3; }')
RESOLVER_RESOLVE = ('BASE_CHECK_SCRIPT="$(bash "$RESOLVER_LAUNCHER" '
                    '"ywc-merge-dependabot/scripts/check-base-required-checks.sh" bash)" || exit $?')

OLD_SHA = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

GH_STUB = r"""#!/usr/bin/env bash
echo "$*" >> "$GH_STUB_LOG"
case "$GH_STUB_MODE:$*" in
  base:"pr view "*"headRefOid"*)
    echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;
  base:"pr checks "*"--required"*)
    printf '%s\n' "${GH_STUB_REQ_OUT:-}" >&2
    exit "${GH_STUB_REQ_RC:-0}" ;;
  base:"pr checks "*)
    printf '%s\n' "${GH_STUB_ALL_OUT:-}" >&2
    exit "${GH_STUB_ALL_RC:-0}" ;;
  base:"pr merge "*)
    exit 0 ;;
  base:"pr view "*"baseRefName"*)
    [ -n "${GH_STUB_BASE+x}" ] || exit 1
    printf '%s\n' "$GH_STUB_BASE" ;;
  base:"api "*"/protection/required_status_checks"*)
    [ -z "${GH_STUB_PROTECTION_ERR+x}" ] || { printf '%s\n' "$GH_STUB_PROTECTION_ERR" >&2; exit 1; }
    [ -n "${GH_STUB_PROTECTION:-}" ] || { echo '{"message":"Branch not protected"}'; echo "gh: Branch not protected (HTTP 404)" >&2; exit 1; }
    echo "$GH_STUB_PROTECTION" ;;
  base:"api "*"/rules/branches/"*)
    [ -z "${GH_STUB_RULES_ERR+x}" ] || { printf '%s\n' "$GH_STUB_RULES_ERR" >&2; exit 1; }
    [ -n "${GH_STUB_RULES:-}" ] || { echo '{"message":"Not Found"}'; echo "gh: Not Found (HTTP 404)" >&2; exit 1; }
    echo "$GH_STUB_RULES" ;;
  *)
    exit 1 ;;
esac
"""


def skill_text():
    """SKILL.md plus references/lane-state.md when the state rules were moved there."""
    text = (HERE.parent / "SKILL.md").read_text(encoding="utf-8")
    lane_state = HERE.parent / "references" / "lane-state.md"
    if lane_state.exists():
        text += "\n" + lane_state.read_text(encoding="utf-8")
    return text


def fenced_blocks(text):
    """Bodies of the ```bash fenced blocks, in source order."""
    return re.findall(r"```bash\n(.*?)```", text, re.S)


class StubbedTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(GH_STUB)
        (bin_dir / "sleep").write_text("#!/usr/bin/env bash\nexit 0\n")
        for f in bin_dir.iterdir():
            f.chmod(0o755)
        self.log = self.tmp / "gh.log"
        self.env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}", GH_STUB_LOG=str(self.log))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_cmd(self, mode, *cmd, **extra_env):
        env = dict(self.env, GH_STUB_MODE=mode, **extra_env)
        return subprocess.run(list(map(str, cmd)), capture_output=True, text=True, env=env)

    def gh_calls(self, needle):
        if not self.log.exists():
            return 0
        return sum(needle in line for line in self.log.read_text().splitlines())


class CheckBaseRequiredChecksTest(StubbedTest):
    """baseRefName is remote-controlled: it must be validated before any `gh api` call."""

    def check(self, **env):
        return self.run_cmd("base", "bash", BASE_CHECK, "42", **env)

    def test_hostile_base_names_are_rejected_before_gh_api(self):
        # Fails if any allowlist / leading-dash / `..` / check-ref-format guard is dropped,
        # or if the base value is ever expanded by a shell.
        pwned = self.tmp / "PWNED"
        hostile = [f"$(touch {pwned})", f"`touch {pwned}`", f"main;touch {pwned}",
                   "a/../b", "..", "--x", "-x", "a b", "a\nb", "main|id", "x.lock", "a/", "/a", "HEAD", "@"]
        for base in hostile:
            with self.subTest(base=base):
                r = self.check(GH_STUB_BASE=base, GH_STUB_PROTECTION="1", GH_STUB_RULES="1")
                self.assertEqual(r.returncode, 1, r.stderr)
                self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=")
                self.assertIn("cannot confirm", r.stderr)
        self.assertEqual(self.gh_calls("api "), 0)
        self.assertFalse(pwned.exists())

    def test_valid_base_with_protection_check_is_confirmed(self):
        # Fails if the confirmation path or the quoted API path changes.
        r = self.check(GH_STUB_BASE="release/1.2", GH_STUB_PROTECTION="1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=1 BASE=release/1.2")
        self.assertEqual(self.gh_calls(
            "api repos/{owner}/{repo}/branches/release/1.2/protection/required_status_checks"), 1)

    def test_ruleset_check_confirms_when_protection_lookup_fails(self):
        # Fails if the rulesets fallback is removed, or if a failed protection lookup
        # overrides a positive ruleset count.
        for env in ({}, {"GH_STUB_PROTECTION_ERR": "gh: Resource not accessible by integration (HTTP 403)"}):
            with self.subTest(env=env):
                r = self.check(GH_STUB_BASE="main", GH_STUB_RULES="2", **env)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=1 BASE=main")
        self.assertEqual(self.gh_calls("api repos/{owner}/{repo}/rules/branches/main"), 2)

    def test_zero_required_checks_cannot_confirm(self):
        # Fails if a count of 0 is treated as a required check (instant --auto merge).
        r = self.check(GH_STUB_BASE="main", GH_STUB_PROTECTION="0", GH_STUB_RULES="0")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=main")

    def test_non_numeric_count_is_unresolved(self):
        # Fails if non-numeric gh output is trusted as a count, or read as "zero required checks".
        r = self.check(GH_STUB_BASE="main", GH_STUB_PROTECTION="null", GH_STUB_RULES="1;x")
        self.assertEqual(r.returncode, 3)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=main")

    def test_not_found_lookups_mean_zero_required_checks(self):
        # Fails if HTTP 404 (branch not protected, no rulesets) is read as "confirmed" or
        # as a failed lookup: an unprotected base would lose its all-checks gate.
        r = self.check(GH_STUB_BASE="main")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=main")

    def test_failed_lookup_is_unresolved_not_zero(self):
        # Fails if a 403 / rate limit / server error / silent gh failure on either lookup is
        # read as "base has zero required checks" (exit 1 → all-checks fallback).
        errors = ["gh: API rate limit exceeded for installation ID 1. (HTTP 403)",
                  "gh: Resource not accessible by integration (HTTP 403)",
                  "gh: Server Error (HTTP 502)", ""]
        for err in errors:
            for env in ({"GH_STUB_PROTECTION_ERR": err, "GH_STUB_RULES": "0"},
                        {"GH_STUB_PROTECTION": "0", "GH_STUB_RULES_ERR": err}):
                with self.subTest(env=env):
                    r = self.check(GH_STUB_BASE="main", **env)
                    self.assertEqual(r.returncode, 3, r.stderr)
                    self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=main")
                    self.assertIn("unresolved", r.stderr)
                    # Fails if exit 3 stops naming the failed endpoint and its first output line.
                    endpoint = ("protection/required_status_checks" if "GH_STUB_PROTECTION_ERR" in env
                                else "rules/branches/main")
                    self.assertIn(f"{endpoint} failed", r.stderr)
                    self.assertIn(err or "(no output)", r.stderr)

    def test_unreadable_base_cannot_confirm(self):
        # Fails if an empty / failed baseRefName lookup reaches `gh api`.
        for env in ({}, {"GH_STUB_BASE": ""}):
            with self.subTest(env=env):
                r = self.check(GH_STUB_PROTECTION="1", **env)
                self.assertEqual(r.returncode, 1)
        self.assertEqual(self.gh_calls("api "), 0)

    def test_usage_error(self):
        self.assertEqual(self.run_cmd("base", "bash", BASE_CHECK, "1;x").returncode, 2)
        self.assertEqual(self.run_cmd("base", "bash", BASE_CHECK).returncode, 2)


class SequentialCiGateTest(StubbedTest):
    """Runs the Step 3a gate snippet from SKILL.md against the stubbed gh and the real resolver."""

    NO_REQ = "no required checks reported on the 'dependabot/x' branch"

    def gate(self, bundle=True, **env):
        block = next(b for b in fenced_blocks(skill_text()) if GATE_MARKER in b)
        script = self.tmp / "gate.sh"
        script.write_text(block.replace("{number}", "7"))
        codex_home = self.tmp / "codex-home"
        codex_home.mkdir(exist_ok=True)
        if bundle:
            # Plain copies (never symlinks) of the shared resolver and this skill's script,
            # laid out like an installed bundle, so the real resolver selects the script.
            shared = codex_home / "skills" / "scripts"
            own = codex_home / "skills" / "ywc-merge-dependabot" / "scripts"
            shared.mkdir(parents=True, exist_ok=True)
            own.mkdir(parents=True, exist_ok=True)
            for name in RESOLVER_FILES:
                shutil.copyfile(SHARED_SCRIPTS / name, shared / name)
            shutil.copyfile(BASE_CHECK, own / BASE_CHECK.name)
        self.env.pop("CLAUDE_SKILL_DIR", None)
        # Empty, so a developer shell's source fallback cannot turn BLOCKED into a pass.
        return self.run_cmd("base", "bash", script, CODEX_HOME=str(codex_home),
                            YWC_BUNDLE_DEVELOPMENT="", YWC_BUNDLE_SOURCE_ROOT="", **env)

    def last(self, r):
        return r.stdout.strip().splitlines()[-1]

    def test_required_checks_pass_merges_pinned(self):
        # Fails if a passing gate no longer reaches the pinned merge.
        r = self.gate()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.last(r), "Merged")
        self.assertEqual(self.gh_calls(f"pr merge 7 --merge --match-head-commit {OLD_SHA}"), 1)

    def test_pending_exit_8_is_skipped_not_failed(self):
        # Fails if exit 8 is collapsed into the failure branch.
        r = self.gate(GH_STUB_REQ_RC="8")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.last(r), "Skipped (CI pending)")
        self.assertEqual(self.gh_calls("pr merge"), 0)

    def test_failed_required_checks_never_merge(self):
        # Fails if a non-zero, non-8 exit without the message stops being a failure.
        r = self.gate(GH_STUB_REQ_RC="1", GH_STUB_REQ_OUT="X build fail")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.last(r), "Failed (CI not passing)")
        self.assertEqual(self.gh_calls("pr merge"), 0)

    def test_unregistered_required_checks_are_pending_not_fallback(self):
        # Fails if the message triggers the fallback while the base has a required check.
        r = self.gate(GH_STUB_REQ_RC="1", GH_STUB_REQ_OUT=self.NO_REQ, GH_STUB_BASE="main", GH_STUB_PROTECTION="1")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.last(r), "Skipped (CI pending)")
        self.assertEqual(self.gh_calls("pr merge"), 0)
        self.assertEqual(sum(l.startswith("pr checks") and "--required" not in l
                             for l in self.log.read_text().splitlines()), 0)

    def test_base_without_required_checks_falls_back_to_all_checks(self):
        # Fails if the fallback, its label, or its gate on every check is dropped.
        env = dict(GH_STUB_REQ_RC="1", GH_STUB_REQ_OUT=self.NO_REQ, GH_STUB_BASE="main", GH_STUB_RULES="0")
        r = self.gate(**env)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.last(r), "Merged (no required checks)")
        r = self.gate(GH_STUB_ALL_RC="1", GH_STUB_ALL_OUT="X lint fail", **env)
        self.assertEqual(self.last(r), "Failed (CI not passing) (no required checks)")
        r = self.gate(GH_STUB_ALL_RC="1", GH_STUB_ALL_OUT="no checks reported on the 'dependabot/x' branch", **env)
        self.assertEqual(self.last(r), "Skipped (no CI checks)")
        self.assertEqual(self.gh_calls("pr merge"), 1)

    def test_failed_base_lookup_is_skipped_never_fallback(self):
        # Fails if exit 3 (lookup failed) reaches the all-checks fallback or any merge.
        r = self.gate(GH_STUB_REQ_RC="1", GH_STUB_REQ_OUT=self.NO_REQ, GH_STUB_BASE="main",
                      GH_STUB_PROTECTION_ERR="gh: API rate limit exceeded (HTTP 403)", GH_STUB_RULES="0")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.last(r), "Skipped (required checks unconfirmed)")
        self.assertEqual(self.gh_calls("pr merge"), 0)
        self.assertEqual(sum(l.startswith("pr checks") and "--required" not in l
                             for l in self.log.read_text().splitlines()), 0)

    def test_unreadable_base_keeps_fail_safe(self):
        # Fails if an unreadable/invalid base is treated as "no required checks".
        r = self.gate(GH_STUB_REQ_RC="1", GH_STUB_REQ_OUT=self.NO_REQ)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.last(r), "Skipped (no required check confirmed)")
        self.assertEqual(self.gh_calls("pr merge"), 0)

    def test_unresolvable_bundle_blocks_the_run(self):
        # Fails if the gate falls back to a placeholder / repo path, treats the resolver
        # failure as a per-PR result, or reaches the base check or a merge without it.
        r = self.gate(bundle=False, GH_STUB_REQ_RC="1", GH_STUB_REQ_OUT=self.NO_REQ, GH_STUB_BASE="main",
                      GH_STUB_PROTECTION="1")
        self.assertEqual(r.returncode, 3, r.stdout)
        self.assertTrue(r.stderr.startswith("BLOCKED:"), r.stderr)
        self.assertEqual(self.gh_calls("pr merge"), 0)
        self.assertEqual(self.gh_calls("api "), 0)


class SkillContractTest(unittest.TestCase):
    """Source assertions on the Codex SKILL.md merge-safety contract (prose guards)."""

    LABELS = [
        "Skipped (CI pending)", "Skipped (head unreadable)", "Skipped (no required check confirmed)",
        "Skipped (required checks unconfirmed)", "Skipped (no CI checks)", "Failed (head kept moving)",
        "Failed (merge refused)", "Failed (CI timeout)", "Skipped (deadline reached)",
        "Failed (auto-merge possibly still enabled)", "Skipped (run blocked)",
        "Skipped (run blocked) — auto-merge still enabled",
    ]

    @classmethod
    def setUpClass(cls):
        cls.text = skill_text()

    def section(self, start, end):
        self.assertIn(start, self.text)
        body = self.text.split(start, 1)[1]
        self.assertIn(end, body)
        return body.split(end, 1)[0]

    def test_stage1_confirms_the_base_before_auto(self):
        # Fails if Stage 1 enables --auto without the base check, or runs the check after it.
        stage1 = self.section("**Stage 1", "**Stage 2")
        self.assertIn("check-base-required-checks.sh", stage1)
        self.assertIn("gh pr merge {number} --auto", stage1)
        self.assertLess(stage1.index("check-base-required-checks.sh"), stage1.index("gh pr merge {number} --auto"))
        # W1: the live pre-start read replaces a persisted auto intent.
        self.assertIn("gh pr view {number} --json state,autoMergeRequest,headRefOid", stage1)
        self.assertLess(stage1.index("autoMergeRequest"), stage1.index("check-base-required-checks.sh"))

    def test_stage2_lane_start_runs_the_base_check(self):
        # Fails if a next-in-lane start may skip the base check.
        stage2 = self.section("**Stage 2", "**Stage 3")
        self.assertIn("Stage 1 lane start block", stage2)
        self.assertIn("a lane start never skips the base check", stage2)

    def test_stage3_takes_unconfirmed_base_prs_from_the_persisted_list(self):
        # Fails if Stage 3 handles only the mixed group, or forgets the persisted `stage3` list.
        stage3 = self.section("**Stage 3", "### 4. Final Summary")
        self.assertIn("base was not confirmed", stage3)
        self.assertIn("`stage3`", stage3)
        self.assertIn("run-wide deadline", stage3)

    def test_every_merge_command_is_pinned_or_a_disable(self):
        # Fails if any `gh pr merge` with a PR operand lacks the head pin (at any indentation).
        merges = [l for l in self.text.splitlines() if re.search(r'gh pr merge (\{number\}|"\$)', l)]
        self.assertGreaterEqual(len(merges), 3, merges)
        for line in merges:
            with self.subTest(line=line):
                self.assertTrue("--match-head-commit" in line or "--disable-auto" in line, line)

    def test_conflict_path_is_rebase_only_and_waits_under_the_run_wide_deadline(self):
        # Fails if the manual fallback returns, the path triggers on other mergeable values,
        # or the post-rebase CI wait loses its deadline or its timeout label.
        self.assertIn("The conflict path is entered only when `gh pr view {number} --json mergeable` reads "
                      "`CONFLICTING`", self.text)
        for gone in ("gh pr checkout", "git push", "git commit", "hand-resolving"):
            self.assertNotIn(gone, self.text)
        self.assertIn("is `MERGEABLE`", self.text)
        self.assertIn("fresh CI inside the same run-wide deadline", self.text)
        self.assertIn("`Failed (CI timeout)`", self.text)
        # This skill ships only the grouper and the base check (shape, not a file name).
        helpers = set(re.findall(r"ywc-merge-dependabot/scripts/([A-Za-z0-9_.-]+\.(?:sh|py))", self.text))
        self.assertEqual(helpers, {"group-by-ecosystem.py", "check-base-required-checks.sh"}, helpers)

    def test_base_check_runs_before_every_auto_and_is_never_persisted(self):
        # Fails if a resume may reuse an earlier base-check result, or an auto intent key returns
        # without a reader (W1).
        self.assertIn("runs before every `--auto` call, including on resume", self.text)
        self.assertIn("The base-check result is never persisted", self.text)
        self.assertNotIn("base_check", self.text)
        self.assertNotIn("auto_intent", self.text)
        self.assertIn("No required status checks confirmed on the base branch — falling back to sequential mode",
                      self.text)

    def test_label_set_is_complete(self):
        # Fails if a gate outcome loses its report label, or the no-CI precedence is dropped.
        for label in self.LABELS:
            with self.subTest(label=label):
                self.assertIn(f"`{label}`", self.text)
        self.assertIn("`Skipped (no CI checks)`, which takes precedence over `Failed (CI timeout)`", self.text)

    def test_failed_auto_is_reread_and_only_left_after_a_verified_disable(self):
        # Fails if a non-zero --auto skips the re-read, an uncertain PR enters Stage 3 (W2),
        # or an uncertain PR lets its lane start another same-lockfile PR (W4).
        self.assertIn("After any non-zero `--auto` result, re-read `autoMergeRequest`", self.text)
        self.assertIn("An empty re-read removes the PR from its lane and adds it to `stage3`", self.text)
        self.assertNotIn("Any non-zero result removes the PR from its lane", self.text)
        self.assertIn('status[pr] = "auto-merge-uncertain"', self.text)
        self.assertIn("only when that re-read shows auto-merge enabled or fails", self.text)
        self.assertIn("only after `gh pr merge {number} --disable-auto` succeeds and a re-read shows "
                      "`autoMergeRequest` empty", self.text)
        self.assertIn("An `auto-merge-uncertain` PR closes its lane: the lane's remaining PRs move to `stage3`",
                      self.text)
        self.assertIn("never in `stage3`", self.text)

    def test_persisted_set_adds_ci_wait_and_stage3(self):
        # Fails if the restart cap or the Stage 3 queue is lost across chunks.
        persist = [s for s in re.split(r"(?<=\.)\s+", self.text) if s.startswith("Also persist")]
        self.assertTrue(persist, "missing the `Also persist` sentence")
        self.assertIn("`ci_wait[pr] = {head, restarts}`", persist[0])
        self.assertIn("`stage3`", persist[0])
        # The fixture-pinned sentence stays unchanged.
        self.assertIn("Persist `deadline`, `active`, `lanes`, `status`, and `rebase_commented`", self.text)

    def test_resume_records_merged_or_closed_prs_as_terminal(self):
        # Fails if a resume restarts a PR that merged or closed during the crash window (W3).
        self.assertIn("for every PR in `active`, `stage3` and `ci_wait`", self.text)
        self.assertIn("`MERGED` or `CLOSED` is recorded as terminal", self.text)

    def test_run_blocked_keeps_recorded_terminal_labels(self):
        # Fails if a resolver failure overwrites labels already recorded or is read per PR.
        self.assertIn("keeps its recorded terminal label", self.text)
        self.assertIn("never a per-PR result", self.text)

    def test_base_is_reread_immediately_before_auto(self):
        # Fails if a retargeted base can slip between the check and --auto.
        self.assertIn("Re-read `baseRefName` immediately before `--auto`", self.text)

    def test_values_are_compared_in_process_never_in_jq(self):
        # Fails if a persisted or remote value is spliced into a --jq filter.
        self.assertIn("compared in-process on parsed JSON, never interpolated into `--jq`", self.text)
        self.assertFalse(re.search(r"--jq[^\n]*\$", self.text))

    def test_run_wide_deadline_replaces_per_wait_deadlines(self):
        # Fails if a wait or the lane illustration computes its own 1800 s deadline (W6), or
        # never-started PRs are marked failed/stalled at the deadline (W7).
        self.assertIn("once at the start of Step 3", self.text)
        self.assertFalse(re.search(r"deadline=\$\(\(.*1800", self.text))
        self.assertIn("never-started PRs are `Skipped (deadline reached)`", self.text)

    def test_resolver_lines_directly_precede_every_base_check_call(self):
        # Fails if a block calls the script without resolving it, or through a placeholder path.
        calls = 0
        for block in fenced_blocks(self.text):
            lines = [l.strip() for l in block.splitlines()]
            for i, line in enumerate(lines):
                if 'bash "$BASE_CHECK_SCRIPT"' in line:
                    calls += 1
                    self.assertGreaterEqual(i, 2)
                    self.assertEqual(lines[i - 2], RESOLVER_SELECT)
                    self.assertEqual(lines[i - 1], RESOLVER_RESOLVE)
            if "check-base-required-checks.sh" in block:
                for bad in ("CLAUDE_SKILL_DIR", "/path/to/", "codex/skills/"):
                    self.assertNotIn(bad, block)
        self.assertEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
