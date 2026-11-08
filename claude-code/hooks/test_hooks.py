"""Stdin-driven tests for the PreToolUse hooks. Run: python3 claude-code/hooks/test_hooks.py"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
NV = "--no" + "-verify"  # keeps this file's own text from tripping no-verify guards


def run_hook(name: str, tool: str, tool_input: dict) -> dict:
    with tempfile.TemporaryDirectory() as home:  # logs go to $HOME/.claude/hooks-logs
        r = subprocess.run(
            [sys.executable, str(HERE / name)],
            input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
            capture_output=True, text=True, env={**os.environ, "HOME": home}, check=True,
        )
    return json.loads(r.stdout)


def decision(out: dict) -> str | None:
    return out.get("hookSpecificOutput", {}).get("permissionDecision")


def rule_id(out: dict) -> str:
    return out.get("hookSpecificOutput", {}).get("permissionDecisionReason", "")


class BlockDangerousCommandsTest(unittest.TestCase):
    def bash(self, cmd: str) -> dict:
        return run_hook("block-dangerous-commands.py", "Bash", {"command": cmd})

    def assert_denied(self, cmd: str, rid: str) -> None:
        out = self.bash(cmd)
        self.assertEqual(decision(out), "deny", cmd)
        self.assertIn(f"[{rid}]", rule_id(out), cmd)

    def assert_allowed(self, cmd: str) -> None:
        self.assertEqual(self.bash(cmd), {}, cmd)

    # AC4
    def test_skipping_hooks_is_denied(self):
        for cmd in ("git commit -n -m x", "git commit -nm x", "git commit -anm x", f"git push {NV}",
                    f"git commit {NV} -m x", "git -C repo commit -n -m x", "git -c a.b=c commit -n",
                    "cd x && git commit -n -m y", "FOO=1 git commit -n",
                    # multi-line forms: quoted strings span lines, unquoted newlines separate
                    f"git commit -m \"$(cat <<'EOF'\nmsg\nEOF\n)\" {NV}",
                    "git commit -m \"a\nb\" -n", f"git commit -m x \\\n {NV}",
                    "echo start\ngit commit -n -m x",
                    # abbreviations, wrappers, indirect execution
                    "git commit --no-veri -m x", "git push --no-verif origin x",
                    "env -u X git commit -n", "sudo -u me git commit -n", "xargs -n 1 git commit -n",
                    'bash -c "git commit -n -m x"', "eval git commit -n -m x",
                    "echo $(git commit -n -m x)", 'x="$(git commit -n -m y)"', "echo `git commit -n`",
                    # reserved words, more wrappers, shell option clusters, process substitution, $'...'
                    "{ git commit -n -m x; }", "if true; then git commit -n -m x; fi", "! git commit -n -m x",
                    "while true; do git commit -n; done", "timeout 5 git commit -n -m x",
                    "stdbuf -o0 git commit -n", "sudo bash -c 'git commit -n'", "bash -lc 'git commit -n -m x'",
                    "cat <(git commit -n -m x)", f"git commit $'{NV}' -m x",
                    "bash -c -e 'git commit -n'", "bash -c -o pipefail -- 'git commit -n'",
                    "git commit -m x --$'no-verify'", "git commit -m x -$'n'",
                    "git commit -m x $'\\x2dn'", "git commit -m x $'\\055\\055no-verify'",
                    "git commit -m x $'\\x2d\\x2dno-verify'", "git commit -m x $'-\\u6e'",
                    "git commit -m x $'\\x2d\\156'",
                    # decoder edge cases must not raise (a raise would fail open)
                    "git commit -m $'\\cß' -n", "git commit -m $'\\UFFFFFFFF' -n",
                    "git commit -m $'\\x' -n", "git commit -m $'end\\c' -n",
                    "env -S 'git commit -n -m x'", "env --split-string='git commit -n'",
                    "env -S'git commit -n'", "/usr/bin/env -S 'git' commit -n",
                    "env -iS'git commit -n'", "env --split='git commit -n'",
                    "env -S 'git\\_commit\\_-n'", "env -u X -S 'git commit -n'",
                    "sudo env -S 'git commit -n'", "timeout 5 env -S 'git commit -n'",
                    "nice -n 5 env -S 'git commit -n'", "env --un X -S 'git commit -n'", "env --u X -S 'git commit -n'", "env --c /tmp -S 'git commit -n'",
                    "env -S 'git commit -m a\\\\c -n'"):
            with self.subTest(cmd=cmd):
                self.assert_denied(cmd, "git-no-verify")

    def test_unrelated_n_flags_are_allowed(self):
        for cmd in ("git add foo && git commit -m x && grep -n y z",
                    "git push -n origin x", "git push -nu origin x",
                    'sed -n 1,3p f; git commit -m "x"',
                    '[ -n "$x" ] && git push origin main',
                    f'git commit -m "drop {NV}"',
                    "git commit -mnice", "git commit -m -n",
                    "git commit -F msg.txt",
                    f"git commit -F - <<'EOF'\nfix: x\n\nmention {NV} and -n here\nEOF",
                    f"cat > s.py <<EOF\nrun('git commit {NV}')\nEOF\npython3 s.py",
                    f"git commit -m \"$(cat <<'EOF'\nfix: x\n\nbody -n {NV}\nEOF\n)\"",
                    "git commit -Sn1234 -m x", "git commit -uno -m x",
                    "git commit --no-verbose -m x",
                    "git commit -- -n",
                    "git commit -m \"price is $'x -n'\"", "git commit -m 'a $\" -n'",
                    "git commit -m $'line1\\nline2 -n'", "git commit -m $'it\\'s -n'",
                    "env git commit -Sabc -m x",  # git's -S<keyid>, not env's split string
                    "env -S 'git commit -m x\\c -n'"):
            with self.subTest(cmd=cmd):
                self.assert_allowed(cmd)

    def test_shell_comments_neither_hide_flags_nor_merge_lines(self):
        for cmd in ("git commit -m fix#12 -n", "echo x # note\ngit commit -n -m y",
                    "git commit -m x # don't\ngit commit -n", "git commit -m x \\#y -n",
                    "git commit -m x;# c\ngit commit -n",
                    "git commit -m x\r#c -n", "git commit -m x ${y:- #} -n",
                    "echo } ${y:- #} ; git commit -m x -n",
                    "echo `true #`; git commit -m x -n",
                    "echo \\` `true #`; git commit -m x -n"):
            with self.subTest(cmd=cmd):
                self.assert_denied(cmd, "git-no-verify")
        for cmd in ('git commit -m "a#b -n"', "git commit -m x # -n",
                    "git commit -m x # don't\ngit status", "git commit -m 'a #b -n'"):
            with self.subTest(cmd=cmd):
                self.assert_allowed(cmd)

    def test_untokenizable_command_falls_back_to_regex(self):
        self.assert_denied("git commit -n -m 'unbalanced", "git-no-verify")
        self.assert_allowed("grep -n 'unbalanced")

    # AC5
    def test_gh_merge_admin(self):
        self.assert_denied("gh pr merge 12 --admin --merge", "gh-merge-admin")
        self.assert_denied("gh -R o/r pr merge 1 --admin", "gh-merge-admin")
        self.assert_denied("gh pr merge 1 --admin=true", "gh-merge-admin")
        self.assert_allowed("gh pr merge 12 --auto --merge --match-head-commit abc")
        self.assert_allowed('gh pr comment 12 --body "do not use --admin"')

    # AC6
    def test_git_add_all_asks(self):
        for cmd in ("git add -A", "git add .", "git add --all", "git add -Av", "git add -- ."):
            with self.subTest(cmd=cmd):
                out = self.bash(cmd)
                self.assertEqual(decision(out), "ask", cmd)
                self.assertIn("[git-add-all]", rule_id(out))
        for cmd in ("git add src/a.ts", "git add -p", "git add ./src", "git add -u"):
            with self.subTest(cmd=cmd):
                self.assert_allowed(cmd)

    def test_deny_beats_ask(self):
        self.assert_denied("git add -A && git commit -n -m x", "git-no-verify")

    def test_existing_patterns_still_apply(self):
        self.assert_denied("git push --force origin main", "git-force-main")
        self.assert_allowed("git push --force-with-lease=refs/heads/b: origin c:refs/heads/b")


class ProtectSecretsTest(unittest.TestCase):
    def check(self, tool: str, tool_input: dict) -> str | None:
        return decision(run_hook("protect-secrets.py", tool, tool_input))

    # AC6b
    def test_grep_and_glob_on_secret_places_are_denied(self):
        cases = [("Grep", {"pattern": "x", "path": "~/.ssh"}),
                 ("Grep", {"pattern": "x", "path": "/home/u/.aws/"}),
                 ("Grep", {"pattern": "x", "glob": ".env*"}),
                 ("Grep", {"pattern": "x", "path": "config/prod.pem"}),
                 ("Glob", {"pattern": "**/.env"}),
                 ("Glob", {"pattern": "**/.env*"}),
                 ("Glob", {"pattern": "**/*.pem"}),
                 ("Glob", {"pattern": "*", "path": "~/.ssh"}),
                 ("Glob", {"pattern": ".ssh/id_*", "path": "~"}),
                 ("Glob", {"pattern": "**/.{env,npmrc}"}),
                 ("Glob", {"pattern": "**/.[e]nv"}),
                 ("Glob", {"pattern": "**/id_{rsa,ed25519}"}),
                 ("Glob", {"pattern": "**/id_*"}),
                 ("Grep", {"pattern": "x", "glob": "{.env,a.ts}"}),
                 ("Grep", {"pattern": "BEGIN", "path": "~"}),
                 ("Grep", {"pattern": "x", "path": "/"}),
                 ("Grep", {"pattern": "x", "path": "~", "glob": "**/*"}),
                 ("Glob", {"pattern": "**/*env"}),
                 ("Glob", {"pattern": "**/*_rsa"}),
                 ("Glob", {"pattern": "**/*.[e]nv"}),
                 ("Glob", {"pattern": "**/?env"}),
                 ("Grep", {"pattern": "x", "path": "~", "glob": "[a-z]*"}),
                 ("Grep", {"pattern": "x", "path": "~", "glob": "?"}),
                 ("Grep", {"pattern": "x", "path": "~", "glob": "!*.ts"}),
                 ("Glob", {"pattern": "{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}{a,b}"})]
        for tool, ti in cases:
            with self.subTest(tool=tool, ti=ti):
                self.assertEqual(self.check(tool, ti), "deny")

    def test_ordinary_searches_are_allowed(self):
        cases = [("Grep", {"pattern": "password|token|\\.env", "path": "src/"}),
                 ("Grep", {"pattern": "x"}),
                 ("Grep", {"pattern": "x", "glob": "*.ts"}),
                 ("Glob", {"pattern": "**/*.md"}),
                 ("Glob", {"pattern": "**/.env.example"}),
                 ("Glob", {"pattern": "src/**/*.py", "path": "/repo"}),
                 ("Glob", {"pattern": "**/*.json"}),
                 ("Glob", {"pattern": "**/*.{ts,tsx}"}),
                 ("Glob", {"pattern": "**/*"}),
                 ("Glob", {"pattern": "**/package.json"}),
                 ("Glob", {"pattern": "**/README*.md"}),
                 ("Grep", {"pattern": "x", "path": "~", "glob": "*.md"}),
                 ("Grep", {"pattern": "x", "path": "~", "type": "py"})]
        for tool, ti in cases:
            with self.subTest(tool=tool, ti=ti):
                self.assertIsNone(self.check(tool, ti))

    def test_bracket_class_names_are_denied(self):
        self.assertEqual(self.check("Grep", {"pattern": "x", "glob": "**/[.]env"}), "deny")
        self.assertEqual(self.check("Glob", {"pattern": "**/[.]env"}), "deny")
        # not in the sample-name list: caught because the class expands to literals
        self.assertEqual(self.check("Glob", {"pattern": "**/[.]env.staging"}), "deny")
        self.assertEqual(self.check("Grep", {"pattern": "x", "glob": "**/.e[n-o]v.staging"}), "deny")
        self.assertIsNone(self.check("Glob", {"pattern": "**/[.]env.example"}))  # allowlisted
        self.assertIsNone(self.check("Glob", {"pattern": "src/[a-z]*.ts"}))

    def test_grep_without_path_uses_session_cwd(self):
        with tempfile.TemporaryDirectory() as home:
            out = subprocess.run([sys.executable, str(HERE / "protect-secrets.py")],
                                 input=json.dumps({"tool_name": "Grep", "cwd": home, "tool_input": {"pattern": "x"}}),
                                 capture_output=True, text=True, env={**os.environ, "HOME": home}, check=True)
        self.assertEqual(decision(json.loads(out.stdout)), "deny")
        self.assertIsNone(self.check("Grep", {"pattern": "x"}))  # no cwd given → not broad

    def test_block_log_omits_grep_content_pattern(self):
        secret = "AKIA" + "Z" * 16
        with tempfile.TemporaryDirectory() as home:
            subprocess.run([sys.executable, str(HERE / "protect-secrets.py")],
                           input=json.dumps({"tool_name": "Grep", "tool_input": {"pattern": secret, "path": "~/.ssh"}}),
                           capture_output=True, text=True, env={**os.environ, "HOME": home}, check=True)
            logs = "".join(p.read_text() for p in Path(home, ".claude", "hooks-logs").glob("*.jsonl"))
        self.assertIn("ssh-dir", logs)
        self.assertNotIn(secret, logs)

    def test_read_behavior_unchanged(self):
        self.assertEqual(self.check("Read", {"file_path": "/repo/.env"}), "deny")
        self.assertIsNone(self.check("Read", {"file_path": "/repo/.env.example"}))


if __name__ == "__main__":
    unittest.main(verbosity=1)
