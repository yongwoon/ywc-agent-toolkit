#!/usr/bin/env python3
"""Tests for detect-dockerfile-from.sh, wait-dependabot-rebase.sh,
check-base-required-checks.sh and poll-merge-queue.py.

Stdlib only. `gh` and `sleep` are shimmed onto PATH: the gh stub answers from
the GH_STUB_MODE environment variable and appends every call to GH_STUB_LOG,
so no network is touched and no real time is slept.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCKER = HERE / "detect-dockerfile-from.sh"
REBASE = HERE / "wait-dependabot-rebase.sh"
BASE_CHECK = HERE / "check-base-required-checks.sh"
QUEUE = HERE / "poll-merge-queue.py"
MAJOR = HERE / "detect-major-bump.py"

OLD_SHA = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
NEW_SHA = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

GH_STUB = r"""#!/usr/bin/env bash
echo "$*" >> "$GH_STUB_LOG"
case "$GH_STUB_MODE:$*" in
  docker-from:"pr diff"*)
    printf 'diff --git a/Dockerfile b/Dockerfile\n-FROM node:18\n+FROM node:20\n' ;;
  readme-from:"pr diff"*)
    printf 'diff --git a/README.md b/README.md\n+FROM node:20\n' ;;
  docker-space:"pr diff"*)
    printf 'diff --git a/my dir/Dockerfile b/my dir/Dockerfile\n+FROM node:20\n' ;;
  docker-ext:"pr diff"*)
    printf 'diff --git a/build/app.dockerfile b/build/app.dockerfile\n-FROM alpine:3.19\n' ;;
  diff-fail:"pr diff"*)
    exit 1 ;;
  rebased:"pr view "*"--json headRefOid --jq"*|stuck:"pr view "*"--json headRefOid --jq"*|unknown:"pr view "*"--json headRefOid --jq"*|emptyhead:"pr view "*"--json headRefOid --jq"*|newconflict:"pr view "*"--json headRefOid --jq"*|commentfail:"pr view "*"--json headRefOid --jq"*|nullnew:"pr view "*"--json headRefOid --jq"*|shortnew:"pr view "*"--json headRefOid --jq"*|oddnull:"pr view "*"--json headRefOid --jq"*|oddempty:"pr view "*"--json headRefOid --jq"*)
    echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;
  nullhead:"pr view "*"--json headRefOid --jq"*)
    echo null ;;
  shorthead:"pr view "*"--json headRefOid --jq"*)
    echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;
  nullnew:"pr view "*"headRefOid,mergeable"*)
    echo "null MERGEABLE" ;;
  shortnew:"pr view "*"headRefOid,mergeable"*)
    echo "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb MERGEABLE" ;;
  no-head:"pr view "*"--json headRefOid --jq"*)
    exit 1 ;;
  rebased:"pr view "*"headRefOid,mergeable"*)
    echo "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb MERGEABLE" ;;
  stuck:"pr view "*"headRefOid,mergeable"*)
    echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa CONFLICTING" ;;
  unknown:"pr view "*"headRefOid,mergeable"*)
    echo "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb UNKNOWN" ;;
  emptyhead:"pr view "*"headRefOid,mergeable"*)
    echo " MERGEABLE" ;;
  oddnull:"pr view "*"headRefOid,mergeable"*)
    echo "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb null" ;;
  oddempty:"pr view "*"headRefOid,mergeable"*)
    echo "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb " ;;
  newconflict:"pr view "*"headRefOid,mergeable"*)
    echo "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb CONFLICTING" ;;
  pollfail:"pr view "*"--json headRefOid --jq"*)
    echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;
  pollfail:"pr view "*"headRefOid,mergeable"*)
    echo "HTTP 401: Bad credentials" >&2
    exit 1 ;;
  commentfail:"pr comment"*)
    exit 1 ;;
  *:"pr comment"*)
    exit "${GH_STUB_COMMENT_RC:-0}" ;;
  queue:"pr view 1 "*)
    echo '{"state":"MERGED","mergeStateStatus":"CLEAN","headRefOid":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}' ;;
  queue:"pr view 2 "*)
    echo '{"state":"OPEN","mergeStateStatus":"DIRTY","headRefOid":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}' ;;
  queue:"pr view 3 "*)
    echo '{"state":"CLOSED","mergeStateStatus":"CLEAN","headRefOid":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}' ;;
  queue:"pr view 4 "*)
    echo "HTTP 401: Bad credentials" >&2
    exit 1 ;;
  queue:"pr view 5 "*)
    echo '{"state":"OPEN","mergeStateStatus":"BLOCKED","headRefOid":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}' ;;
  queue:"pr view 6 "*)
    /bin/sleep 3 ;;
  queue:"pr merge 5 --disable-auto"*)
    exit "${GH_STUB_DISABLE_RC:-0}" ;;
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


class DetectDockerfileFromTest(StubbedTest):
    def test_from_change_in_dockerfile_exits_0(self):
        self.assertEqual(self.run_cmd("docker-from", "bash", DOCKER, "12").returncode, 0)

    def test_from_line_outside_dockerfile_exits_1(self):
        self.assertEqual(self.run_cmd("readme-from", "bash", DOCKER, "12").returncode, 1)

    def test_dockerfile_path_with_spaces_is_detected(self):
        self.assertEqual(self.run_cmd("docker-space", "bash", DOCKER, "12").returncode, 0)

    def test_dot_dockerfile_suffix_is_detected(self):
        self.assertEqual(self.run_cmd("docker-ext", "bash", DOCKER, "12").returncode, 0)

    def test_gh_failure_is_unresolved_not_clean(self):
        r = self.run_cmd("diff-fail", "bash", DOCKER, "12")
        self.assertEqual(r.returncode, 3)
        self.assertIn("UNRESOLVED", r.stderr)

    def test_usage_error(self):
        self.assertEqual(self.run_cmd("docker-from", "bash", DOCKER).returncode, 2)


class WaitDependabotRebaseTest(StubbedTest):
    def test_new_head_and_mergeable_counts_as_rebased(self):
        r = self.run_cmd("rebased", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip().splitlines()[-1], f"REBASED=1 ATTEMPTS=1 NEW_HEAD={NEW_SHA}")
        self.assertEqual(self.gh_calls("pr comment 7 --body @dependabot rebase"), 1)

    def test_unchanged_head_exhausts_nine_attempts(self):
        r = self.run_cmd("stuck", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_unknown_mergeable_is_not_rebased(self):
        r = self.run_cmd("unknown", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_empty_polled_head_is_not_rebased(self):
        # Fails if the non-empty NEW_HEAD guard is dropped: "" differs from the recorded head.
        r = self.run_cmd("emptyhead", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_new_head_still_conflicting_is_not_rebased(self):
        # Fails if the CONFLICTING guard is dropped: the head moved but the conflict remains.
        r = self.run_cmd("newconflict", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_mergeable_outside_allowlist_is_not_rebased(self):
        # Fails if `mergeable` is checked with a deny-list: `null` or an empty value is not
        # CONFLICTING/UNKNOWN and would be reported as a finished rebase.
        for mode in ("oddnull", "oddempty"):
            with self.subTest(mode=mode):
                r = self.run_cmd(mode, "bash", REBASE, "7")
                self.assertEqual(r.returncode, 1)
                self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_unreadable_head_fails_before_requesting_rebase(self):
        r = self.run_cmd("no-head", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=0 NEW_HEAD=")
        self.assertEqual(self.gh_calls("pr comment"), 0)

    def test_non_sha_recorded_head_fails_before_requesting_rebase(self):
        # Fails if OLD_HEAD is accepted without the 40-hex check: "null" or a 39-char value would
        # be recorded and any later head would look "new".
        for mode in ("nullhead", "shorthead"):
            with self.subTest(mode=mode):
                r = self.run_cmd(mode, "bash", REBASE, "7")
                self.assertEqual(r.returncode, 1)
                self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=0 NEW_HEAD=")
                self.assertIn("cannot read the current head", r.stderr)
                self.assertEqual(self.gh_calls("pr comment"), 0)

    def test_non_sha_polled_head_is_not_rebased(self):
        # Fails if NEW_HEAD is accepted without the 40-hex check: "null" or a 39-char value differs
        # from the recorded head and would be reported as a finished rebase.
        for mode in ("nullnew", "shortnew"):
            with self.subTest(mode=mode):
                r = self.run_cmd(mode, "bash", REBASE, "7")
                self.assertEqual(r.returncode, 1)
                self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_every_failed_status_query_is_reported_not_hidden(self):
        # Fails if a persistent gh failure is swallowed and reported like a slow rebase.
        r = self.run_cmd("pollfail", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")
        self.assertIn("every status query for PR 7 failed", r.stderr)
        self.assertIn("Bad credentials", r.stderr)

    def test_failed_rebase_comment_exits_before_polling(self):
        r = self.run_cmd("commentfail", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=0 NEW_HEAD=")
        self.assertIn("failed to post", r.stderr)
        self.assertEqual(self.gh_calls("headRefOid,mergeable"), 0)


class DetectMajorBumpClassifyTest(unittest.TestCase):
    """The leftmost-non-zero rule decides which PRs are never merged."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("detect_major_bump", MAJOR)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_classify_table(self):
        table = [
            ("1.2.3", "2.0.0", True), ("1.2.3", "1.3.0", False),
            ("0.2.0", "0.3.0", True), ("0.2.0", "0.2.5", False),
            ("0.9.0", "1.0.0", True), ("0.0.3", "0.0.4", True),
            ("v4.46.0", "v5.90.0", True), ("1.2", "1.2.1", False),
            ("1.2.0-rc.1", "1.2.0", False), ("abc1234", "def5678", None),
        ]
        for from_v, to_v, expected in table:
            with self.subTest(from_v=from_v, to_v=to_v):
                self.assertIs(self.mod.classify(from_v, to_v)[0], expected)


class DetectMajorBumpStdinTest(unittest.TestCase):
    def test_hash_prefixed_number_is_parsed_not_a_crash(self):
        # Fails if "#N<TAB>title" crashes on int("#N") (it used to exit 1 with a traceback).
        r = subprocess.run([sys.executable, str(MAJOR)], capture_output=True, text=True,
                           input="#130\tBump webpack from 4.46.0 to 5.90.0\nabc\tBump a from 1.0.0 to 1.1.0\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = [json.loads(l) for l in r.stdout.splitlines()]
        self.assertEqual([(x["number"], x["major_bump"]) for x in rows], [(130, True), (None, False)])


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
    """Runs the Step 3a gate snippet from SKILL.md against the stubbed gh."""

    NO_REQ = "no required checks reported on the 'dependabot/x' branch"

    def gate(self, **env):
        text = (HERE.parent / "SKILL.md").read_text(encoding="utf-8")
        blocks = [b.split("\n", 1)[1] for b in text.split("```bash")[1:]]
        block = next(b.split("```", 1)[0] for b in blocks if "gh pr checks {number} --required 2>&1" in b)
        script = self.tmp / "gate.sh"
        script.write_text(block.replace("{number}", "7"))
        return self.run_cmd("base", "bash", script, CLAUDE_SKILL_DIR=str(HERE.parent), **env)

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


class PollMergeQueueTest(StubbedTest):
    def queue(self, *args, **extra_env):
        return self.run_cmd("queue", sys.executable, QUEUE, "--state", self.tmp / "state.json", *args, **extra_env)

    def test_merged_pr_drains_queue(self):
        r = self.queue("--prs", f"1:{OLD_SHA}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"1": "merged"})

    def test_chunk_end_persists_state_and_comments_rebase_once(self):
        r = self.queue("--prs", f"1:{OLD_SHA}", f"2:{OLD_SHA}", YWC_MQ_CHUNK_SECONDS="2", YWC_MQ_POLL_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        state = json.loads((self.tmp / "state.json").read_text())
        self.assertEqual(state["remaining"], [2])
        self.assertEqual(state["status"], {"1": "merged"})
        self.assertEqual(state["rebase_commented"], [2])
        self.assertEqual(self.gh_calls("pr comment 2"), 1)

    def test_resume_after_deadline_marks_remaining_stalled(self):
        (self.tmp / "state.json").write_text(json.dumps(
            {"deadline": int(time.time()) - 1, "remaining": [2], "heads": {"1": OLD_SHA, "2": OLD_SHA},
             "status": {"1": "merged"}, "rebase_commented": [2]}))
        r = self.queue()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"1": "merged", "2": "stalled"})
        self.assertEqual(self.gh_calls("pr view 2 "), 1)  # the one final read
        self.assertEqual(self.gh_calls("pr comment"), 0)

    def test_pr_merged_by_the_deadline_is_merged_not_stalled(self):
        # Fails if the remaining PRs are marked without one final read at the deadline.
        (self.tmp / "state.json").write_text(json.dumps(
            {"deadline": int(time.time()) - 1, "remaining": [1], "heads": {"1": OLD_SHA}, "status": {}}))
        r = self.queue()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"1": "merged"})

    def test_missing_state_without_prs_is_usage_error(self):
        self.assertEqual(self.queue().returncode, 2)

    def test_closed_pr_is_terminal(self):
        r = self.queue("--prs", f"3:{OLD_SHA}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"3": "closed"})

    def test_failed_query_requeues_without_terminal_status(self):
        r = self.queue("--prs", f"4:{OLD_SHA}", YWC_MQ_CHUNK_SECONDS="1", YWC_MQ_POLL_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads(r.stdout), {"done": False, "deadline": json.loads(r.stdout)["deadline"],
                                                "remaining": [4], "status": {}, "requeues": {}})

    def test_prs_with_existing_state_is_refused(self):
        self.assertEqual(self.queue("--prs", f"1:{OLD_SHA}").returncode, 0)
        before = (self.tmp / "state.json").read_text()
        r = self.queue("--prs", f"2:{OLD_SHA}")
        self.assertEqual(r.returncode, 2)
        self.assertIn("fresh --state path", r.stderr)
        self.assertEqual((self.tmp / "state.json").read_text(), before)

    def test_corrupt_state_with_prs_keeps_given_deadline(self):
        (self.tmp / "state.json").write_text("{not json")
        past = int(time.time()) - 1
        r = self.queue("--prs", f"2:{OLD_SHA}", "--deadline", str(past))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual((out["deadline"], out["status"]), (past, {"2": "stalled"}))

    def test_fresh_mktemp_state_file_starts_without_warning(self):
        (self.tmp / "state.json").write_text("")
        r = self.queue("--prs", f"1:{OLD_SHA}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("unparsable", r.stderr)

    def test_moved_head_disables_auto_merge(self):
        # Fails if a head pushed after --auto stays queued: GitHub would merge it without the
        # Step 2 Dockerfile / major-bump checks.
        r = self.queue("--prs", f"5:{OLD_SHA}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"5": "head-moved"})
        self.assertEqual(self.gh_calls("pr merge 5 --disable-auto"), 1)

    def test_moved_head_ends_the_chunk_at_once(self):
        # Fails if the poller keeps polling (up to 540 s) before handing a moved head back.
        started = time.time()
        r = self.queue("--prs", f"5:{OLD_SHA}", f"2:{OLD_SHA}", YWC_MQ_CHUNK_SECONDS="60",
                       YWC_MQ_POLL_SECONDS="60")
        self.assertLess(time.time() - started, 10)
        self.assertEqual(r.returncode, 3, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual((out["status"], out["remaining"]), ({"5": "head-moved"}, [2]))
        self.assertEqual(self.gh_calls("pr view 2 "), 1)

    def test_requeue_resumes_on_the_new_head_up_to_the_cap(self):
        # Fails if a re-queued PR keeps its old head (it would be disabled again at once),
        # or if a head that keeps moving is re-queued forever.
        NEW = "b" * 40
        self.queue("--prs", f"5:{OLD_SHA}")
        r = self.queue("--requeue", f"5:{NEW}", YWC_MQ_CHUNK_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        state = json.loads((self.tmp / "state.json").read_text())
        self.assertEqual((state["remaining"], state["heads"]["5"], state["requeues"]), ([5], NEW, {"5": 1}))
        state["status"]["5"] = "head-moved"; state["remaining"] = []; state["requeues"]["5"] = 2
        (self.tmp / "state.json").write_text(json.dumps(state))
        r = self.queue("--requeue", f"5:{NEW}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("sequential pass", r.stderr)
        self.assertEqual(json.loads(r.stdout)["requeues"], {"5": 2})
        self.assertEqual(self.gh_calls("pr merge 5 --disable-auto"), 2)  # once moved, once at the cap
        self.assertEqual(json.loads(r.stdout)["status"], {"5": "head-moved"})

    def test_requeue_is_refused_for_a_pr_that_did_not_move(self):
        self.queue("--prs", f"1:{OLD_SHA}")
        self.assertEqual(self.queue("--requeue", f"1:{OLD_SHA}").returncode, 2)
        self.assertEqual(self.queue("--requeue", f"1:{OLD_SHA}", "--prs", f"2:{OLD_SHA}").returncode, 2)

    def test_duplicate_requeue_is_usage_error_not_a_crash(self):
        self.queue("--prs", f"5:{OLD_SHA}")
        r = self.queue("--requeue", f"5:{OLD_SHA}", f"5:{'b' * 40}")
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_failed_disable_is_retried_and_never_reported_moved(self):
        r = self.queue("--prs", f"5:{OLD_SHA}", YWC_MQ_CHUNK_SECONDS="2", YWC_MQ_POLL_SECONDS="1",
                       GH_STUB_DISABLE_RC="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads(r.stdout)["remaining"], [5])
        self.assertGreaterEqual(self.gh_calls("pr merge 5 --disable-auto"), 2)

    def test_failed_query_at_deadline_is_unreadable_not_stalled(self):
        # Fails if an auth or rate-limit outage is reported as a stalled queue.
        past = int(time.time()) + 3
        r = self.queue("--prs", f"4:{OLD_SHA}", f"2:{OLD_SHA}", "--deadline", str(past),
                       YWC_MQ_POLL_SECONDS="1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"4": "unreadable", "2": "stalled"})
        self.assertIn("Bad credentials", r.stderr)

    def test_timed_out_query_requeues_and_names_the_timeout(self):
        r = self.queue("--prs", f"6:{OLD_SHA}", YWC_MQ_CHUNK_SECONDS="1", YWC_MQ_POLL_SECONDS="1",
                       YWC_MQ_GH_TIMEOUT_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads(r.stdout)["remaining"], [6])
        self.assertIn("timed out", r.stderr)
        self.assertEqual(json.loads((self.tmp / "state.json").read_text())["query_failed"], [6])

    def test_failed_rebase_comment_is_retried_next_chunk(self):
        # Fails if a failed `@dependabot rebase` post is recorded as sent.
        r = self.queue("--prs", f"2:{OLD_SHA}", YWC_MQ_CHUNK_SECONDS="1", GH_STUB_COMMENT_RC="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads((self.tmp / "state.json").read_text())["rebase_commented"], [])
        r = self.queue(YWC_MQ_CHUNK_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads((self.tmp / "state.json").read_text())["rebase_commented"], [2])
        self.assertEqual(self.gh_calls("pr comment 2"), 2)

    def test_pr_without_head_is_usage_error(self):
        self.assertEqual(self.queue("--prs", "1").returncode, 2)
        self.assertEqual(self.queue("--prs", "1:null").returncode, 2)

    def test_state_without_heads_is_unusable(self):
        (self.tmp / "state.json").write_text(json.dumps(
            {"deadline": int(time.time()) + 60, "remaining": [2], "status": {}}))
        self.assertEqual(self.queue().returncode, 2)

    def test_corrupt_state_without_deadline_warns(self):
        (self.tmp / "state.json").write_text("{not json")
        r = self.queue("--prs", f"1:{OLD_SHA}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("unparsable", r.stderr)


if __name__ == "__main__":
    unittest.main()
