import json
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).with_name("fetch-pr-review-artifacts.sh")
REPO = "example/project"
PR_NUMBER = "223"
EXPECTED_CALLS = (
    "api user --jq .login\n"
    "api repos/example/project/pulls/223/comments --paginate\n"
    "api repos/example/project/issues/223/comments --paginate\n"
    "api repos/example/project/pulls/223/reviews --paginate\n"
    "pr view 223 --repo example/project --json url,mergeable,mergeStateStatus,statusCheckRollup\n"
)


class CollectorContractTest(unittest.TestCase):
    """RED-first contract coverage for the current collector interface."""

    def _fake_gh(self, directory, fixtures, failure_stage=None):
        fixture_dir = directory / "fixtures"
        fixture_dir.mkdir()
        for name, value in fixtures.items():
            (fixture_dir / name).write_text(value, encoding="utf-8")

        log = directory / "gh.log"
        script = directory / "gh"
        script.write_text(
            """#!/usr/bin/env bash
set -eu
log=${FAKE_GH_LOG}
fixture_dir=${FAKE_GH_FIXTURES}
stage=${FAKE_GH_FAIL:-}
args=("$@")
matches() {
  local -a expected=("$@")
  [ "${#args[@]}" -eq "${#expected[@]}" ] || return 1
  local index
  for index in "${!expected[@]}"; do
    [ "${args[$index]}" = "${expected[$index]}" ] || return 1
  done
}
if matches api user --jq .login; then
  fixture=user.json; expected="api user --jq .login"; fail_stage=user
elif matches api repos/example/project/pulls/223/comments --paginate; then
  fixture=comments.json; expected="api repos/example/project/pulls/223/comments --paginate"; fail_stage=comments
elif matches api repos/example/project/issues/223/comments --paginate; then
  fixture=issue_comments.json; expected="api repos/example/project/issues/223/comments --paginate"; fail_stage=issue_comments
elif matches api repos/example/project/pulls/223/reviews --paginate; then
  fixture=reviews.json; expected="api repos/example/project/pulls/223/reviews --paginate"; fail_stage=reviews
elif matches pr view 223 --repo example/project --json url,mergeable,mergeStateStatus,statusCheckRollup; then
  fixture=pr.json; expected="pr view 223 --repo example/project --json url,mergeable,mergeStateStatus,statusCheckRollup"; fail_stage=pr
else
  printf 'unexpected gh argv:' >&2
  printf ' %q' "${args[@]}" >&2
  printf '\n' >&2
  exit 97
fi
printf '%s\n' "${args[*]}" >> "$log"
line=$(wc -l < "$log")
expected_line=$(sed -n "${line}p" "$FAKE_GH_EXPECTED")
if [ "$expected_line" != "$expected" ]; then
  echo "unexpected gh order: expected $expected_line, got $expected" >&2
  exit 98
fi
if [ "$stage" = "$fail_stage" ]; then
  echo "fake gh failure at $fail_stage" >&2
  exit 99
fi
cat "$fixture_dir/$fixture"
""",
            encoding="utf-8",
        )
        script.chmod(0o755)
        (directory / "expected.calls").write_text(
            "api user --jq .login\n"
            "api repos/example/project/pulls/223/comments --paginate\n"
            "api repos/example/project/issues/223/comments --paginate\n"
            "api repos/example/project/pulls/223/reviews --paginate\n"
            "pr view 223 --repo example/project --json url,mergeable,mergeStateStatus,statusCheckRollup\n",
            encoding="utf-8",
        )
        return script, log

    def _run(self, fixtures, failure_stage=None):
        directory_context = tempfile.TemporaryDirectory()
        directory = pathlib.Path(directory_context.name)
        try:
            fake_gh, log = self._fake_gh(directory, fixtures, failure_stage)
            path_result = subprocess.run(
                ["bash", str(SCRIPT), REPO, PR_NUMBER],
                cwd=str(directory),
                env={
                    "PATH": str(directory) + ":/usr/bin:/bin",
                    "FAKE_GH_LOG": str(log),
                    "FAKE_GH_FIXTURES": str(directory / "fixtures"),
                    "FAKE_GH_EXPECTED": str(directory / "expected.calls"),
                    **({"FAKE_GH_FAIL": failure_stage} if failure_stage else {}),
                },
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            calls = log.read_text(encoding="utf-8") if log.exists() else ""
            return path_result, calls, fake_gh
        finally:
            directory_context.cleanup()
            self.assertFalse(directory.exists(), "temporary fixture state leaked")

    def _assert_artifact(self, artifacts, fingerprint, artifact_type, **fields):
        matching = [item for item in artifacts if item.get("fingerprint") == fingerprint]
        self.assertEqual(1, len(matching), "%s %s" % (artifact_type, fingerprint))
        artifact = matching[0]
        self.assertEqual(artifact_type, artifact.get("artifact_type"), fingerprint)
        for key, expected in fields.items():
            self.assertEqual(expected, artifact.get(key), "%s %s field=%s" % (artifact_type, fingerprint, key))
        return artifact

    def _fixtures(self, pr):
        return {
            "user.json": "bot\n",
            "comments.json": json.dumps([
                {"id": 101, "user": {"login": "alice"}, "body": "unanswered", "path": "a.py", "line": 7, "created_at": "2026-01-01T01:00:00Z"},
                {"id": 102, "user": {"login": "alice"}, "body": "address me", "path": "b.py", "original_line": 8, "created_at": "2026-01-01T02:00:00Z"},
                {"id": 103, "in_reply_to_id": 102, "user": {"login": "bot"}, "body": "fixed", "path": "b.py", "line": 8, "created_at": "2026-01-01T03:00:00Z"},
                {"id": 104, "in_reply_to_id": 102, "user": {"login": "alice"}, "body": "reopened", "path": "b.py", "line": 9, "created_at": "2026-01-01T04:00:00Z"},
                {"id": 105, "user": {"login": "alice"}, "body": "already handled", "path": "c.py", "line": 10, "created_at": "2026-01-01T05:00:00Z"},
                {"id": 106, "in_reply_to_id": 105, "user": {"login": "bot"}, "body": "handled", "path": "c.py", "line": 10, "created_at": "2026-01-01T06:00:00Z"},
            ]),
            "issue_comments.json": json.dumps([
                {"id": 201, "user": {"login": "alice"}, "body": "<!-- <review_comment_addressed:pr_comment-201> -->"},
                {"id": 202, "user": {"login": "alice"}, "body": "<!-- <review_comment_addressed> -->"},
                {"id": 203, "user": {"login": "alice"}, "body": "external PR comment", "created_at": "2026-01-01T05:00:00Z"},
                {"id": 204, "user": {"login": "bot"}, "body": "self comment"},
                {"id": 307, "user": {"login": "alice"}, "body": "<!-- <review_comment_addressed:review_submission-307> -->"},
            ]),
            "reviews.json": json.dumps([
                {"id": 301, "user": {"login": "alice"}, "body": "commented review", "state": "COMMENTED", "submitted_at": "2026-01-01T06:00:00Z"},
                {"id": 302, "user": {"login": "carol"}, "body": "changes requested", "state": "CHANGES_REQUESTED", "submitted_at": "2026-01-01T07:00:00Z"},
                {"id": 303, "user": {"login": "alice"}, "body": "approved", "state": "APPROVED"},
                {"id": 304, "user": {"login": "alice"}, "body": "", "state": "COMMENTED"},
                {"id": 305, "user": {"login": "bot"}, "body": "self review", "state": "COMMENTED"},
                {"id": 306, "user": {"login": "alice"}, "body": "<!-- <review_comment_addressed> -->", "state": "COMMENTED"},
                {"id": 307, "user": {"login": "alice"}, "body": "addressed review", "state": "COMMENTED", "submitted_at": "2026-01-01T08:00:00Z"},
            ]),
            "pr.json": json.dumps(pr),
        }

    def test_review_and_health_contract(self):
        pr = {
            "url": "https://github.com/example/project/pull/223",
            "mergeable": "CONFLICTING",
            "mergeStateStatus": "DIRTY",
            "statusCheckRollup": [
                {"name": "unit", "conclusion": "FAILURE", "detailsUrl": "https://ci/unit"},
                {"workflowName": "integration", "status": "IN_PROGRESS", "targetUrl": "https://ci/integration"},
                {"context": "legacy", "state": "FAILURE"},
                {"name": "success", "conclusion": "SUCCESS"},
                {"name": "skipped", "conclusion": "SKIPPED"},
                {"name": "neutral", "conclusion": "NEUTRAL"},
                {"name": "precedence", "conclusion": "FAILURE", "status": "SUCCESS", "state": "SUCCESS"},
                {"name": "unknown"},
            ],
        }
        result, calls, _ = self._run(self._fixtures(pr))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertEqual(
            EXPECTED_CALLS,
            calls,
        )
        artifacts = json.loads(result.stdout)
        self._assert_artifact(artifacts, "review_thread-101", "review_thread", reply_api="review_comment_reply", id=101, body="unanswered", path="a.py", line=7, user="alice", state="unresolved", in_reply_to_id=101, thread_comment_count=1)
        self._assert_artifact(artifacts, "review_thread-102", "review_thread", body="reopened", line=9, thread_comment_count=3)
        self.assertFalse(any(item["fingerprint"] == "review_thread-105" for item in artifacts), "self-authored latest response")
        self._assert_artifact(artifacts, "pr_comment-203", "pr_comment", reply_api="pr_comment", id=203, body="external PR comment", path=None, line=None, user="alice", state="open")
        self._assert_artifact(artifacts, "review_submission-301", "review_submission", reply_api="pr_comment", id=301, body="commented review", user="alice", state="COMMENTED")
        self._assert_artifact(artifacts, "review_submission-302", "review_submission", id=302, body="changes requested", user="carol", state="CHANGES_REQUESTED")
        self.assertFalse(any(item["fingerprint"] in {"pr_comment-201", "review_submission-307"} for item in artifacts))
        self._assert_artifact(
            artifacts,
            "status_check-unit",
            "status_check",
            reply_api="none",
            id="unit",
            body="unit",
            path=None,
            line=None,
            user="github",
            state="FAILURE",
            details_url="https://ci/unit",
        )
        self._assert_artifact(
            artifacts,
            "status_check-integration",
            "status_check",
            reply_api="none",
            id=None,
            body="integration",
            path=None,
            line=None,
            user="github",
            state="IN_PROGRESS",
            details_url="https://ci/integration",
        )
        self._assert_artifact(
            artifacts,
            "status_check-legacy",
            "status_check",
            reply_api="none",
            id="legacy",
            body="legacy",
            path=None,
            line=None,
            user="github",
            state="FAILURE",
            details_url=None,
        )
        self._assert_artifact(
            artifacts,
            "status_check-precedence",
            "status_check",
            reply_api="none",
            id="precedence",
            body="precedence",
            path=None,
            line=None,
            user="github",
            state="FAILURE",
            details_url=None,
        )
        self._assert_artifact(
            artifacts,
            "status_check-unknown",
            "status_check",
            reply_api="none",
            id="unknown",
            body="unknown",
            path=None,
            line=None,
            user="github",
            state="UNKNOWN",
            details_url=None,
        )
        self._assert_artifact(
            artifacts,
            "merge_readiness-CONFLICTING-DIRTY",
            "merge_readiness",
            reply_api="none",
            id="merge_readiness",
            body="mergeable=CONFLICTING, mergeStateStatus=DIRTY",
            path=None,
            line=None,
            user="github",
            state="DIRTY",
            pr_url=pr["url"],
        )
        for suppressed in ("review_thread-102-old", "pr_comment-202", "review_submission-303", "review_submission-304", "review_submission-305", "review_submission-306", "status_check-success", "status_check-skipped", "status_check-neutral"):
            self.assertFalse(any(item["fingerprint"] == suppressed for item in artifacts), suppressed)

    def test_api_failure_is_exit_three(self):
        result, calls, _ = self._run(self._fixtures({"url": "url", "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN", "statusCheckRollup": []}), "user")
        self.assertEqual(3, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertEqual("ERROR: gh CLI not authenticated or API unreachable\n", result.stderr)
        self.assertEqual("api user --jq .login\n", calls)

    def test_later_api_failures_are_exit_three_with_exact_call_prefix(self):
        fixtures = self._fixtures({
            "url": "url",
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "CLEAN",
            "statusCheckRollup": [],
        })
        failures = (
            ("comments", "ERROR: unable to fetch PR review comments\n", EXPECTED_CALLS.splitlines(True)[:2]),
            ("issue_comments", "ERROR: unable to fetch PR comments\n", EXPECTED_CALLS.splitlines(True)[:3]),
            ("reviews", "ERROR: unable to fetch PR reviews\n", EXPECTED_CALLS.splitlines(True)[:4]),
            ("pr", "ERROR: unable to fetch PR status and merge readiness\n", EXPECTED_CALLS.splitlines(True)[:5]),
        )
        for failure_stage, expected_stderr, expected_calls in failures:
            with self.subTest(failure_stage=failure_stage):
                result, calls, _ = self._run(fixtures, failure_stage)
                self.assertEqual(3, result.returncode, failure_stage)
                self.assertEqual("", result.stdout, failure_stage)
                self.assertEqual(expected_stderr, result.stderr, failure_stage)
                self.assertEqual("".join(expected_calls), calls, failure_stage)

    def test_merge_readiness_clean_suppression_and_unknown_fallback(self):
        clean_result, _, _ = self._run(self._fixtures({
            "url": "https://github.com/example/project/pull/223",
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "CLEAN",
            "statusCheckRollup": [],
        }))
        self.assertEqual(0, clean_result.returncode, clean_result.stderr)
        clean_artifacts = json.loads(clean_result.stdout)
        self.assertFalse(
            any(item["artifact_type"] == "merge_readiness" for item in clean_artifacts),
            "merge_readiness-clean suppression",
        )

        unknown_result, _, _ = self._run(self._fixtures({
            "url": "https://github.com/example/project/pull/223",
            "mergeable": "MERGEABLE",
            "statusCheckRollup": [],
        }))
        self.assertEqual(0, unknown_result.returncode, unknown_result.stderr)
        unknown_artifacts = json.loads(unknown_result.stdout)
        self._assert_artifact(
            unknown_artifacts,
            "merge_readiness-MERGEABLE-UNKNOWN",
            "merge_readiness",
            reply_api="none",
            id="merge_readiness",
            body="mergeable=MERGEABLE, mergeStateStatus=UNKNOWN",
            path=None,
            line=None,
            user="github",
            state="UNKNOWN",
            pr_url="https://github.com/example/project/pull/223",
        )


if __name__ == "__main__":
    unittest.main()
