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
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCKER = HERE / "detect-dockerfile-from.sh"
REBASE = HERE / "wait-dependabot-rebase.sh"
BASE_CHECK = HERE / "check-base-required-checks.sh"
QUEUE = HERE / "poll-merge-queue.py"

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
  rebased:"pr view "*"--json headRefOid --jq"*|stuck:"pr view "*"--json headRefOid --jq"*|unknown:"pr view "*"--json headRefOid --jq"*|commentfail:"pr view "*"--json headRefOid --jq"*)
    echo oldsha ;;
  no-head:"pr view "*"--json headRefOid --jq"*)
    exit 1 ;;
  rebased:"pr view "*"headRefOid,mergeable"*)
    echo "newsha MERGEABLE" ;;
  stuck:"pr view "*"headRefOid,mergeable"*)
    echo "oldsha CONFLICTING" ;;
  unknown:"pr view "*"headRefOid,mergeable"*)
    echo "newsha UNKNOWN" ;;
  commentfail:"pr comment"*)
    exit 1 ;;
  *:"pr comment"*)
    exit 0 ;;
  queue:"pr view 1 "*)
    echo '{"state":"MERGED","mergeStateStatus":"CLEAN"}' ;;
  queue:"pr view 2 "*)
    echo '{"state":"OPEN","mergeStateStatus":"DIRTY"}' ;;
  queue:"pr view 3 "*)
    echo '{"state":"CLOSED","mergeStateStatus":"CLEAN"}' ;;
  queue:"pr view 4 "*)
    exit 1 ;;
  base:"pr view "*"baseRefName"*)
    [ -n "${GH_STUB_BASE+x}" ] || exit 1
    printf '%s\n' "$GH_STUB_BASE" ;;
  base:"api "*"/protection/required_status_checks"*)
    [ -n "${GH_STUB_PROTECTION:-}" ] || exit 1
    echo "$GH_STUB_PROTECTION" ;;
  base:"api "*"/rules/branches/"*)
    [ -n "${GH_STUB_RULES:-}" ] || exit 1
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
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=1 ATTEMPTS=1 NEW_HEAD=newsha")
        self.assertEqual(self.gh_calls("pr comment 7 --body @dependabot rebase"), 1)

    def test_unchanged_head_exhausts_nine_attempts(self):
        r = self.run_cmd("stuck", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_unknown_mergeable_is_not_rebased(self):
        r = self.run_cmd("unknown", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=9 NEW_HEAD=")

    def test_unreadable_head_fails_before_requesting_rebase(self):
        r = self.run_cmd("no-head", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=0 NEW_HEAD=")
        self.assertEqual(self.gh_calls("pr comment"), 0)

    def test_failed_rebase_comment_exits_before_polling(self):
        r = self.run_cmd("commentfail", "bash", REBASE, "7")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "REBASED=0 ATTEMPTS=0 NEW_HEAD=")
        self.assertIn("failed to post", r.stderr)
        self.assertEqual(self.gh_calls("headRefOid,mergeable"), 0)


class CheckBaseRequiredChecksTest(StubbedTest):
    """baseRefName is remote-controlled: it must be validated before any `gh api` call."""

    def check(self, **env):
        return self.run_cmd("base", "bash", BASE_CHECK, "42", **env)

    def test_hostile_base_names_are_rejected_before_gh_api(self):
        # Fails if any allowlist / leading-dash / `..` / check-ref-format guard is dropped,
        # or if the base value is ever expanded by a shell.
        pwned = self.tmp / "PWNED"
        hostile = [f"$(touch {pwned})", f"`touch {pwned}`", f"main;touch {pwned}",
                   "a/../b", "..", "--x", "-x", "a b", "a\nb", "main|id", "x.lock", "a/", "/a"]
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
        # Fails if the rulesets fallback is removed.
        r = self.check(GH_STUB_BASE="main", GH_STUB_RULES="2")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.gh_calls("api repos/{owner}/{repo}/rules/branches/main"), 1)

    def test_zero_required_checks_cannot_confirm(self):
        # Fails if a count of 0 is treated as a required check (instant --auto merge).
        r = self.check(GH_STUB_BASE="main", GH_STUB_PROTECTION="0", GH_STUB_RULES="0")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=main")

    def test_non_numeric_count_cannot_confirm(self):
        # Fails if non-numeric gh output is trusted as a count.
        r = self.check(GH_STUB_BASE="main", GH_STUB_PROTECTION="null", GH_STUB_RULES="1;x")
        self.assertEqual(r.returncode, 1)

    def test_gh_failures_cannot_confirm(self):
        # Fails if a 404 / permission error is read as "confirmed".
        r = self.check(GH_STUB_BASE="main")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "CONFIRMED=0 BASE=main")

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


class PollMergeQueueTest(StubbedTest):
    def queue(self, *args, **extra_env):
        return self.run_cmd("queue", sys.executable, QUEUE, "--state", self.tmp / "state.json", *args, **extra_env)

    def test_merged_pr_drains_queue(self):
        r = self.queue("--prs", "1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"1": "merged"})

    def test_chunk_end_persists_state_and_comments_rebase_once(self):
        r = self.queue("--prs", "1", "2", YWC_MQ_CHUNK_SECONDS="2", YWC_MQ_POLL_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        state = json.loads((self.tmp / "state.json").read_text())
        self.assertEqual(state["remaining"], [2])
        self.assertEqual(state["status"], {"1": "merged"})
        self.assertEqual(state["rebase_commented"], [2])
        self.assertEqual(self.gh_calls("pr comment 2"), 1)

    def test_resume_after_deadline_marks_remaining_stalled(self):
        (self.tmp / "state.json").write_text(json.dumps(
            {"deadline": int(time.time()) - 1, "remaining": [2], "status": {"1": "merged"},
             "rebase_commented": [2]}))
        r = self.queue()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"1": "merged", "2": "stalled"})
        self.assertEqual(self.gh_calls("pr "), 0)

    def test_missing_state_without_prs_is_usage_error(self):
        self.assertEqual(self.queue().returncode, 2)

    def test_closed_pr_is_terminal(self):
        r = self.queue("--prs", "3")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], {"3": "closed"})

    def test_failed_query_requeues_without_terminal_status(self):
        r = self.queue("--prs", "4", YWC_MQ_CHUNK_SECONDS="1", YWC_MQ_POLL_SECONDS="1")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads(r.stdout), {"done": False, "deadline": json.loads(r.stdout)["deadline"],
                                                "remaining": [4], "status": {}})

    def test_prs_with_existing_state_is_refused(self):
        self.assertEqual(self.queue("--prs", "1").returncode, 0)
        before = (self.tmp / "state.json").read_text()
        r = self.queue("--prs", "2")
        self.assertEqual(r.returncode, 2)
        self.assertIn("fresh --state path", r.stderr)
        self.assertEqual((self.tmp / "state.json").read_text(), before)

    def test_corrupt_state_with_prs_keeps_given_deadline(self):
        (self.tmp / "state.json").write_text("{not json")
        past = int(time.time()) - 1
        r = self.queue("--prs", "2", "--deadline", str(past))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual((out["deadline"], out["status"]), (past, {"2": "stalled"}))

    def test_fresh_mktemp_state_file_starts_without_warning(self):
        (self.tmp / "state.json").write_text("")
        r = self.queue("--prs", "1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("unparsable", r.stderr)

    def test_corrupt_state_without_deadline_warns(self):
        (self.tmp / "state.json").write_text("{not json")
        r = self.queue("--prs", "1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("unparsable", r.stderr)


if __name__ == "__main__":
    unittest.main()
