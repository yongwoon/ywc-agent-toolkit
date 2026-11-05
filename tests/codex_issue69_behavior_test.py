#!/usr/bin/env python3
"""Offline helper/recipe execution and source expected traces, never live agents."""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'tests/fixtures/codex-issue69/upstream-behavior/operational-safety'
FIXTURE = ROOT / 'tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json'
SETUP = ROOT / 'codex/skills/ywc-docker-isolate/scripts/setup-docker-ports.sh'


def run(argv, **kwargs):
    return subprocess.run(argv, text=True, capture_output=True, **kwargs)


class OperationalSafetyTests(unittest.TestCase):
    def test_each_source_clause_has_negative_control(self):
        """Exercise the real shared contract assertion against temporary mutations."""
        spec = importlib.util.spec_from_file_location('issue69_contract', ROOT / 'tests/codex_issue69_contract_test.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        case = json.loads(FIXTURE.read_text())
        originals = {check['source']: (ROOT / check['source']).read_text() for check in case['checks']}
        with tempfile.TemporaryDirectory(prefix='ywc-operational-contract-') as raw:
            temp = Path(raw).resolve()
            fixture_dir = temp / 'fixtures/upstream-adoption'
            fixture_dir.mkdir(parents=True)
            (fixture_dir / 'operational-safety.json').write_text(json.dumps(case))
            for source, text in originals.items():
                target = temp / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            with patch.object(module, 'ROOT', temp), patch.object(module, 'FIXTURES', fixture_dir.parent):
                oracle = module.ContractTests('test_source_contract_scenarios')
                oracle.test_source_contract_scenarios()
                for check in case['checks']:
                    source = check['source']
                    for clause in check['required']:
                        with self.subTest(source=source, removed=clause):
                            (temp / source).write_text(originals[source].replace(clause, ''))
                            with self.assertRaises(AssertionError):
                                oracle.test_source_contract_scenarios()
                            (temp / source).write_text(originals[source])

    def test_existing_setup_helper_failure_duplicate_and_git_preservation(self):
        """Existing helper runs; worker admission remains an expected trace only."""
        with tempfile.TemporaryDirectory(prefix='ywc-operational-setup-') as raw:
            repo = Path(raw) / 'repo'
            repo.mkdir()
            self.assertEqual(run(['git', 'init', '-b', 'feature/safety'], cwd=repo).returncode, 0)
            self.assertEqual(run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                                  'commit', '--allow-empty', '-m', 'fixture'], cwd=repo).returncode, 0)
            head = run(['git', 'rev-parse', 'HEAD'], cwd=repo).stdout
            argv = ['bash', str(SETUP), '--task-name', 'safety', '--worktree-path', str(repo)]
            no_docker = run(argv)
            self.assertEqual(no_docker.returncode, 0, no_docker.stderr)
            self.assertIn('no docker', no_docker.stdout)
            self.assertFalse((repo / '.env').exists())
            compose = repo / 'compose.yml'
            compose.write_text('services:\n  api:\n    image: test\n    ports:\n      - "8080:80"\n')
            rejected = run(argv)
            self.assertEqual(rejected.returncode, 1, rejected.stderr)
            self.assertIn('hardcoded', rejected.stderr)
            self.assertFalse((repo / '.env').exists())
            # No host ports reaches the existing atomic .env rename without Docker.
            compose.write_text('services:\n  api:\n    image: test\n')
            fake_bin = Path(raw) / 'bin'
            fake_bin.mkdir()
            fake_mv = fake_bin / 'mv'
            for status in (2, 127):
                fake_mv.write_text(f'#!/bin/sh\nexit {status}\n')
                fake_mv.chmod(0o700)
                failed = run(argv, env=dict(os.environ, PATH=str(fake_bin) + os.pathsep + os.environ['PATH']))
                self.assertEqual(failed.returncode, status, failed.stderr)
                self.assertFalse((repo / '.env').exists(), 'partial .env promoted after failed rename')
                self.assertEqual(run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo).stdout.strip(), 'feature/safety')
                self.assertEqual(run(['git', 'rev-parse', 'HEAD'], cwd=repo).stdout, head)
                self.assertTrue((repo / '.git').is_dir())
            # Retry and duplicate success converge to one managed block.
            for _ in range(2):
                result = run(argv)
                self.assertEqual(result.returncode, 0, result.stderr)
                content = (repo / '.env').read_text()
                self.assertEqual(content.count('# >>> ywc-docker-isolate (managed) >>>'), 1)
            self.assertEqual(run(['git', 'rev-parse', 'HEAD'], cwd=repo).stdout, head)

    def test_extracted_dockerfile_recipe(self):
        """Execute original runnable fenced source, not a test reimplementation."""
        source = (ROOT / 'codex/skills/ywc-merge-dependabot/SKILL.md').read_text()
        bounded = source.split('<!-- operational-safety:dockerfile-detector:start -->', 1)[1].split('<!-- operational-safety:dockerfile-detector:end -->', 1)[0]
        recipe = re.search(r'```bash\n(.*?)\n```', bounded, re.S).group(1)
        with tempfile.TemporaryDirectory(prefix='ywc-operational-diff-') as raw:
            temp = Path(raw)
            gh = temp / 'gh'
            gh.write_text('#!/bin/sh\ncat "$PATCH_FILE"\nexit "$GH_STATUS"\n')
            gh.chmod(0o700)
            patch_file = temp / 'patch'
            for case in json.loads((CASES / 'dockerfile-diffs.json').read_text()):
                with self.subTest(case=case['id']):
                    patch_file.write_text(case['patch'])
                    env = dict(os.environ, PATH=str(temp) + os.pathsep + os.environ['PATH'],
                               PATCH_FILE=str(patch_file), GH_STATUS=str(case.get('gh_status', 0)), pr='123')
                    result = run(['bash', '-c', recipe], env=env)
                    self.assertEqual(result.returncode, case['exit'], result.stderr)

    def test_expected_traces_are_bound_to_source(self):
        """Validate supplied traces and clause links; no simulated dispatcher oracle."""
        case = json.loads(FIXTURE.read_text())
        allowed = {clause for check in case['checks'] for clause in check['required']}
        traces = json.loads((CASES / 'expected-traces.json').read_text())
        self.assertGreaterEqual(len(traces), 20)
        identities = set()
        for trace in traces:
            with self.subTest(case=trace['id']):
                self.assertNotIn(trace['id'], identities)
                identities.add(trace['id'])
                self.assertEqual(trace['evidence_kind'], 'source assertion / fixture expectation')
                self.assertEqual(trace['live_evidence'], 'UNVERIFIED — instruction contract only')
                self.assertIn(trace['source_clause'], allowed)
                self.assertTrue(trace['input'])
                self.assertTrue(trace['expected_trace'])
                self.assertTrue(trace['expected_status'])
        for denied in ('open-pr', 'nonparseable', 'api-failure', 'invalid-branch', 'wrong-base', 'moved-tip', 'lease-race'):
            self.assertEqual(next(t for t in traces if t['id'] == denied)['remote_deletions'], 0)
        for status in (1, 2, 127):
            item = next(t for t in traces if t['id'] == f'isolation-{status}')
            self.assertEqual(item['expected_status'], 'BLOCKED')
            self.assertEqual(item['worker_starts'], 0)
        for denied in ('deadline-exact', 'deadline-late'):
            self.assertEqual(next(t for t in traces if t['id'] == denied)['expected_status'], 'FAILED')
        resumed = next(t for t in traces if t['id'] == 'chunk-resume')
        self.assertEqual(resumed['deadlines'], [1800, 1800, 1800])


class PrWorktreeTests(unittest.TestCase):
    CASES = ROOT / 'tests/fixtures/codex-issue69/upstream-behavior/pr-worktrees'
    FIXTURE = ROOT / 'tests/fixtures/codex-issue69/upstream-adoption/pr-worktrees.json'
    PROVIDER = ROOT / 'codex/skills/ywc-worktrees/references/existing-branch.md'
    CONSUMER = ROOT / 'codex/skills/ywc-handle-pr-reviews/references/pr-worktree-identity.md'

    def recipe(self, source, marker):
        bounded = source.read_text().split(f'<!-- pr-worktrees:{marker}:start -->', 1)[1].split(f'<!-- pr-worktrees:{marker}:end -->', 1)[0]
        return re.search(r'```bash\n(.*?)\n```', bounded, re.S).group(1)

    def git(self, repo, *args):
        result = run(['git', *args], cwd=repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def repository(self, temp):
        remote, seed, client = (temp / name for name in ('origin.git', 'seed', 'client'))
        self.git(temp, 'init', '--bare', '-q', str(remote))
        self.git(temp, 'init', '-q', '-b', 'main', str(seed))
        self.git(seed, 'config', 'user.name', 'Fixture')
        self.git(seed, 'config', 'user.email', 'fixture@example.invalid')
        (seed / '.gitignore').write_text('.worktrees/\n')
        (seed / 'README.md').write_text('base\n')
        self.git(seed, 'add', '.')
        self.git(seed, 'commit', '-q', '-m', 'base')
        self.git(seed, 'remote', 'add', 'origin', str(remote))
        self.git(seed, 'branch', 'feature/review')
        self.git(seed, 'push', '-q', 'origin', 'main', 'feature/review')
        self.git(temp, 'clone', '-q', '-b', 'main', str(remote), str(client))
        self.git(client, 'config', 'user.name', 'Fixture')
        self.git(client, 'config', 'user.email', 'fixture@example.invalid')
        (client / '.worktrees').mkdir()
        return seed, client

    def wrapper(self, temp, fail=''):
        bindir, log = temp / 'bin', temp / 'git-calls.jsonl'
        bindir.mkdir(exist_ok=True)
        real_git = shutil.which('git')
        wrapper = bindir / 'git'
        wrapper.write_text(
            '#!/usr/bin/env python3\nimport json, os, sys\n'
            'args=sys.argv[1:]\n'
            'with open(os.environ["GIT_LOG"], "a") as f: f.write(json.dumps(args)+"\\n")\n'
            'if "ls-remote" in args and os.environ.get("LOOKUP_ROWS"):\n'
            '    print(os.environ["LOOKUP_ROWS"]); sys.exit(0)\n'
            'if os.environ.get("FAIL_GIT_OP") and os.environ["FAIL_GIT_OP"] in args:\n'
            '    print("fixture transport failure", file=sys.stderr); sys.exit(17)\n'
            f'os.execv({real_git!r}, [{real_git!r}, *args])\n')
        wrapper.chmod(0o700)
        env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.environ['PATH'],
                   GIT_LOG=str(log), FAIL_GIT_OP=fail)
        return env, log

    def calls(self, log):
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    def test_pr_source_clauses_and_scenario_bindings(self):
        """Each documented scenario binds to its own clause and removal oracle."""
        spec = importlib.util.spec_from_file_location('issue69_pr_contract', ROOT / 'tests/codex_issue69_contract_test.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        case = json.loads(self.FIXTURE.read_text())
        originals = {check['source']: (ROOT / check['source']).read_text() for check in case['checks']}
        allowed = {(check['source'], clause) for check in case['checks'] for clause in check['required']}
        for scenario in case['scenarios']:
            self.assertIn((scenario['source'], scenario['source_clause']), allowed)
        with tempfile.TemporaryDirectory(prefix='ywc-pr-contract-') as raw:
            temp = Path(raw).resolve()
            fixture_dir = temp / 'fixtures/upstream-adoption'
            fixture_dir.mkdir(parents=True)
            (fixture_dir / 'pr-worktrees.json').write_text(json.dumps(case))
            for source, text in originals.items():
                target = temp / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            with patch.object(module, 'ROOT', temp), patch.object(module, 'FIXTURES', fixture_dir.parent):
                oracle = module.ContractTests('test_source_contract_scenarios')
                oracle.test_source_contract_scenarios()
                for check in case['checks']:
                    for clause in check['required']:
                        with self.subTest(source=check['source'], removed=clause):
                            target = temp / check['source']
                            target.write_text(originals[check['source']].replace(clause, ''))
                            with self.assertRaises(AssertionError):
                                oracle.test_source_contract_scenarios()
                            target.write_text(originals[check['source']])

    def test_extracted_existing_branch_recipe(self):
        """Run the original fenced recipe against local Git and failing transport."""
        recipe = self.recipe(self.PROVIDER, 'existing-branch')
        for case in json.loads((self.CASES / 'recipe-cases.json').read_text())['provider']:
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory(prefix='ywc-pr-provider-') as raw:
                temp = Path(raw).resolve()
                _, client = self.repository(temp)
                target = client / '.worktrees/pr-123'
                setup = case['setup']
                if setup == 'local':
                    self.git(client, 'branch', 'feature/review', 'refs/remotes/origin/feature/review')
                elif setup in ('checked-out', 'dirty', 'locked'):
                    other = client / '.worktrees/other'
                    self.git(client, 'worktree', 'add', '-q', '-b', 'feature/review', str(other), 'refs/remotes/origin/feature/review')
                    if setup == 'dirty': (other / 'untracked').write_text('preserve\n')
                    if setup == 'locked': self.git(client, 'worktree', 'lock', str(other))
                elif setup == 'existing-target': target.mkdir()
                head = case.get('head', 'feature/missing' if setup == 'absent' else 'feature/review')
                env, log = self.wrapper(temp, case.get('fail', ''))
                env.update(EXISTING_BRANCH=head, BRANCH=case.get('branch', head),
                           BASE_BRANCH=case.get('base', ''), RESOLVED_PATH=str(target))
                if case.get('lookup_rows'):
                    oid = self.git(client, 'rev-parse', 'refs/remotes/origin/feature/review')
                    env['LOOKUP_ROWS'] = (oid + '\trefs/heads/feature/other' if case['lookup_rows'] == 'wrong'
                                          else (oid + '\trefs/heads/feature/review\n') * 2)
                result = run(['bash', '-c', recipe], cwd=client, env=env)
                self.assertEqual(result.returncode, case['exit'], result.stderr)
                self.assertIn(case['diagnostic'], result.stdout + result.stderr)
                calls = self.calls(log)
                if result.returncode == 0:
                    self.assertEqual(self.git(target, 'branch', '--show-current'), head)
                    self.assertEqual(self.git(target, 'status', '--porcelain'), '')
                    self.assertIn('branch refs/heads/' + head, self.git(client, 'worktree', 'list', '--porcelain'))
                else:
                    self.assertFalse(any(call[:2] == ['worktree', 'add'] for call in calls))
                if setup == 'remote' and result.returncode == 0:
                    self.assertEqual(self.git(target, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'), 'origin/feature/review')
                    self.assertIn(['fetch', '--no-tags', 'origin', '+refs/heads/feature/review:refs/remotes/origin/feature/review'], calls)
                if case.get('fail'):
                    self.assertIn('fixture transport failure', result.stderr)
                self.assertFalse((client / 'sentinel').exists())

    def test_extracted_exact_refresh_recipe(self):
        recipe = self.recipe(self.CONSUMER, 'refresh')
        for case in json.loads((self.CASES / 'recipe-cases.json').read_text())['refresh']:
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory(prefix='ywc-pr-refresh-') as raw:
                temp = Path(raw).resolve()
                seed, client = self.repository(temp)
                wt = client / '.worktrees/pr-123'
                self.git(client, 'worktree', 'add', '-q', '-b', 'feature/review', str(wt), 'refs/remotes/origin/feature/review')
                initial = self.git(wt, 'rev-parse', 'HEAD')
                if case['setup'] in ('local-ahead', 'diverged'):
                    (wt / 'local.txt').write_text('local\n')
                    self.git(wt, 'add', '.')
                    self.git(wt, 'commit', '-q', '-m', 'local')
                    initial = self.git(wt, 'rev-parse', 'HEAD')
                if case['setup'] in ('remote-ahead', 'diverged'):
                    self.git(seed, 'checkout', '-q', 'feature/review')
                    (seed / 'remote.txt').write_text('remote\n')
                    self.git(seed, 'add', '.')
                    self.git(seed, 'commit', '-q', '-m', 'remote')
                    self.git(seed, 'push', '-q', 'origin', 'feature/review')
                if case['setup'] == 'dirty': (wt / 'untracked').write_text('preserve\n')
                if case['setup'] == 'locked': self.git(client, 'worktree', 'lock', str(wt))
                env, log = self.wrapper(temp, case.get('fail', ''))
                env.update(WT_PATH=str(wt), H=case.get('head', 'feature/review'))
                result = run(['bash', '-c', recipe], cwd=client, env=env)
                self.assertEqual(result.returncode, case['exit'], result.stderr)
                self.assertIn(case['diagnostic'], result.stdout + result.stderr)
                calls = self.calls(log)
                if result.returncode == 0:
                    self.assertEqual(self.git(wt, 'rev-parse', 'HEAD'), self.git(seed, 'rev-parse', 'feature/review'))
                    self.assertIn(['fetch', '--no-tags', 'origin', '+refs/heads/feature/review:refs/remotes/origin/feature/review'], calls)
                    self.assertIn(['merge', '--ff-only', 'refs/remotes/origin/feature/review'], calls)
                else:
                    self.assertEqual(self.git(wt, 'rev-parse', 'HEAD'), initial)
                    self.assertFalse(any(call[:1] == ['merge'] for call in calls))

    def test_existing_cleanup_guards_and_branch_preservation(self):
        cleanup = ROOT / 'codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh'
        baseline = run(['bash', str(cleanup.with_name('test-cleanup-worktree.sh'))], cwd=ROOT)
        self.assertEqual(baseline.returncode, 0, baseline.stderr)
        with tempfile.TemporaryDirectory(prefix='ywc-pr-cleanup-') as raw:
            _, client = self.repository(Path(raw).resolve())
            wt = client / '.worktrees/pr-123'
            self.git(client, 'worktree', 'add', '-q', '-b', 'feature/review', str(wt), 'refs/remotes/origin/feature/review')
            argv = ['bash', str(cleanup), '--branch', 'feature/review', '--keep-branch', 'pr-123']
            (wt / 'untracked').write_text('preserve\n')
            dirty = run(argv, cwd=client)
            self.assertEqual(dirty.returncode, 1)
            self.assertTrue(wt.exists())
            (wt / 'untracked').unlink()
            self.git(client, 'worktree', 'lock', str(wt))
            locked = run(argv, cwd=client)
            self.assertEqual(locked.returncode, 1)
            self.assertTrue(wt.exists())
            self.git(client, 'worktree', 'unlock', str(wt))
            clean = run(argv, cwd=client)
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)
            self.assertFalse(wt.exists())
            self.git(client, 'show-ref', '--verify', 'refs/heads/feature/review')

    def test_existing_audit_classifications(self):
        audit = ROOT / 'codex/skills/ywc-worktrees/scripts/audit-worktrees.sh'
        with tempfile.TemporaryDirectory(prefix='ywc-pr-audit-') as raw:
            _, client = self.repository(Path(raw).resolve())
            wt = client / '.worktrees/pr-123'
            self.git(client, 'worktree', 'add', '-q', '-b', 'feature/review', str(wt), 'refs/remotes/origin/feature/review')
            self.assertEqual(run(['bash', str(audit), '--expect', 'pr-123'], cwd=client).returncode, 0)
            mismatch = run(['bash', str(audit), '--expect', 'missing-task'], cwd=client)
            self.assertEqual(mismatch.returncode, 1)
            self.assertIn('MISSING:', mismatch.stdout)
            self.assertIn('LEAKED:', mismatch.stdout)
            (client / '.worktrees/unregistered').mkdir()
            drift = run(['bash', str(audit), '--expect', 'pr-123'], cwd=client)
            self.assertIn('DRIFT:', drift.stdout)
            shutil.rmtree(wt)
            stale = run(['bash', str(audit), '--expect', 'pr-123'], cwd=client)
            self.assertEqual(stale.returncode, 1)
            self.assertIn('STALE:', stale.stdout)

    def test_expected_pr_traces_bind_to_the_specific_scenario(self):
        """Static API/cwd/dispatch decisions are not simulated runtime evidence."""
        case = json.loads(self.FIXTURE.read_text())
        scenarios = {item['id']: item for item in case['scenarios']}
        traces = json.loads((self.CASES / 'expected-traces.json').read_text())
        self.assertEqual({trace['id'] for trace in traces}, {'invalid-pr', 'foreign-closed', 'invalid-head', 'selection', 'cwd-once', 'cwd-repeat', 'head-move', 'push', 'required-failure', 'cleanup', 'audit'})
        for trace in traces:
            with self.subTest(trace=trace['id']):
                scenario = scenarios[trace['id']]
                self.assertEqual(trace['source'], scenario['source'])
                self.assertEqual(trace['source_clause'], scenario['source_clause'])
                self.assertEqual(trace['expected_trace'], scenario['expected'])
                self.assertEqual(trace['evidence_kind'], 'source assertion / fixture expectation')
                self.assertEqual(trace['live_evidence'], 'UNVERIFIED — instruction contract only')


if __name__ == '__main__':
    unittest.main(verbosity=2)
