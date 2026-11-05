#!/usr/bin/env python3
"""Offline helper/recipe execution and source expected traces, never live agents."""
import importlib.util
import json
import os
from pathlib import Path
import re
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
