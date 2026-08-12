#!/usr/bin/env python3
"""Executable contract fixtures for the architecture-invariants helper."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "codex/skills/scripts/architecture-invariants.py"
SPEC = importlib.util.spec_from_file_location("architecture_invariants", HELPER_PATH)
HELPER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(HELPER)


RED_FIRST_CASES = {
    "closed-unknown-fields",
    "explicit-manifest-no-fallback",
    "glob-zero-segment",
    "glob-single-segment",
    "glob-terminal-multi-segment",
    "ambiguous-non-shared-mapping",
    "scope-digest-mismatch",
    "incomplete-rule-coverage",
    "forbid-observed-edge",
    "allow-observed-edge",
    "verdict-precedence",
    "no-manifest-fallback",
    "zero-child-processes",
    "component-shared-optional",
    "root-manifest-symlink-escape",
    "audit-projection-component-ids",
}

FIXTURE_REGISTRY = {
    "closed-unknown-fields": "test_closed_unknown_fields",
    "explicit-manifest-no-fallback": "test_explicit_manifest_no_fallback",
    "glob-zero-segment": "test_glob_zero_segment",
    "glob-single-segment": "test_glob_single_segment",
    "glob-terminal-multi-segment": "test_glob_terminal_multi_segment",
    "ambiguous-non-shared-mapping": "test_ambiguous_non_shared_mapping",
    "scope-digest-mismatch": "test_scope_digest_mismatch",
    "incomplete-rule-coverage": "test_incomplete_rule_coverage",
    "forbid-observed-edge": "test_forbid_observed_edge_is_violated",
    "allow-observed-edge": "test_allow_observed_edge_is_maintained",
    "verdict-precedence": "test_verdict_precedence",
    "no-manifest-fallback": "test_no_manifest_fallback",
    "zero-child-processes": "test_zero_child_processes",
    "component-shared-optional": "test_component_shared_defaults_to_false",
    "root-manifest-symlink-escape": "test_root_manifest_symlink_escape_is_not_absent",
    "audit-projection-component-ids": "test_audit_projection_exposes_component_ids",
}


def manifest(*, enforcement="advisory", components=None, rules=None):
    return {
        "version": 1,
        "owner": "platform",
        "enforcement": enforcement,
        "components": components or [
            {"id": "api", "paths": ["src/api/**"], "owner": "platform", "shared": False},
            {"id": "ui", "paths": ["src/ui/**"], "owner": "web", "shared": False},
        ],
        "rules": rules or [
            {"id": "api-forbids-ui", "source": "api", "target": "ui", "policy": "forbid", "rationale": "layering"},
        ],
    }


class ArchitectureInvariantFixtures(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def write_json(self, relative, value):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return relative

    def write_text(self, relative, value):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return relative

    def invoke(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = HELPER.main(["--root", str(self.repo), *args])
        self.assertEqual(code, 0)
        return json.loads(output.getvalue())

    def evidence(self, scope_paths, covered_rule_ids, edges=None, digest=None):
        paths = sorted(scope_paths)
        return {
            "version": 1,
            "scope_paths": paths,
            "scope_digest": digest or HELPER.scope_digest(paths),
            "covered_rule_ids": sorted(covered_rule_ids),
            "edges": edges or [],
        }

    def audit(self, manifest_value, evidence_value, *changed_paths):
        self.write_json("contract.json", manifest_value)
        self.write_json("evidence.json", evidence_value)
        return self.invoke(
            "--mode", "audit", "--manifest", "contract.json",
            *sum((["--changed-path", path] for path in changed_paths), []),
            "--evidence", "evidence.json",
        )

    def test_fixture_inventory_is_red_first_and_named(self):
        self.assertEqual(set(FIXTURE_REGISTRY), RED_FIRST_CASES)
        methods = list(FIXTURE_REGISTRY.values())
        self.assertEqual(len(methods), len(set(methods)))
        self.assertEqual(len(methods), len(RED_FIRST_CASES))
        for method_name in methods:
            self.assertTrue(callable(getattr(self, method_name)))

    def test_closed_unknown_fields(self):
        value = manifest()
        value["unexpected"] = True
        self.write_json("contract.json", value)
        result = self.invoke("--mode", "validate", "--manifest", "contract.json")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")

    def test_nested_closed_unknown_fields(self):
        value = manifest()
        value["components"][0]["command"] = "echo unsafe"
        self.write_json("contract.json", value)
        result = self.invoke("--mode", "validate", "--manifest", "contract.json")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")

    def test_malformed_json(self):
        self.write_text("contract.json", "{\"version\": 1,")
        result = self.invoke("--mode", "validate", "--manifest", "contract.json")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")

    def test_invalid_policy(self):
        value = manifest()
        value["rules"][0]["policy"] = "maybe"
        self.write_json("contract.json", value)
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_invalid_component_and_rule_ids(self):
        for field, value in (("component", "API"), ("rule", "api_forbids_ui")):
            candidate = manifest()
            if field == "component":
                candidate["components"][0]["id"] = value
            else:
                candidate["rules"][0]["id"] = value
            self.write_json("contract.json", candidate)
            self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_duplicate_and_dangling_ids_are_rejected(self):
        duplicate = manifest()
        duplicate["components"].append(dict(duplicate["components"][0]))
        dangling = manifest(rules=[{
            "id": "missing-target", "source": "api", "target": "missing",
            "policy": "forbid", "rationale": "invalid endpoint",
        }])
        for value in (duplicate, dangling):
            self.write_json("contract.json", value)
            self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_invalid_glob_is_rejected(self):
        value = manifest()
        value["components"][0]["paths"] = ["src/[api]/**"]
        self.write_json("contract.json", value)
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_explicit_manifest_no_fallback(self):
        self.write_json("architecture-invariants.json", manifest())
        result = self.invoke("--mode", "validate", "--manifest", "missing.json")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")

    def glob_manifest(self, pattern):
        return manifest(components=[
            {"id": "component", "paths": [pattern], "owner": "a", "shared": False},
            {"id": "sink", "paths": ["src/sink/**"], "owner": "b", "shared": False},
        ], rules=[{"id": "component-forbids-sink", "source": "component", "target": "sink", "policy": "forbid", "rationale": "test"}])

    def test_glob_zero_segment(self):
        value = HELPER.validate_manifest(self.glob_manifest("src/tree/**"), self.repo)
        matches, _ = HELPER.component_matches(value, "src/tree")
        self.assertEqual([item["id"] for item in matches], ["component"])

    def test_glob_single_segment(self):
        value = HELPER.validate_manifest(self.glob_manifest("src/*/file.py"), self.repo)
        matches, _ = HELPER.component_matches(value, "src/x/file.py")
        self.assertEqual([item["id"] for item in matches], ["component"])
        matches, _ = HELPER.component_matches(value, "src/x/y/file.py")
        self.assertEqual(matches, [])

    def test_glob_terminal_multi_segment(self):
        value = HELPER.validate_manifest(self.glob_manifest("src/tree/**"), self.repo)
        matches, _ = HELPER.component_matches(value, "src/tree/a/b.py")
        self.assertEqual([item["id"] for item in matches], ["component"])
        matches, _ = HELPER.component_matches(value, "src/other/file.py")
        self.assertEqual(matches, [])

    def test_literal_glob_semantics(self):
        value = HELPER.validate_manifest(self.glob_manifest("src/literal/file.py"), self.repo)
        matches, _ = HELPER.component_matches(value, "src/literal/file.py")
        self.assertEqual([item["id"] for item in matches], ["component"])
        matches, _ = HELPER.component_matches(value, "src/literal/other.py")
        self.assertEqual(matches, [])

    def test_ambiguous_non_shared_mapping(self):
        value = manifest(components=[
            {"id": "one", "paths": ["src/**"], "owner": "a", "shared": False},
            {"id": "two", "paths": ["src/api/**"], "owner": "b", "shared": False},
            {"id": "sink", "paths": ["sink/**"], "owner": "c", "shared": False},
        ], rules=[{"id": "one-forbids-sink", "source": "one", "target": "sink", "policy": "forbid", "rationale": "test"}])
        result = self.audit(value, self.evidence(["src/api/file.py"], ["one-forbids-sink"]), "src/api/file.py")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")

    def test_scope_digest_mismatch(self):
        value = manifest()
        valid = self.evidence(["src/api/file.py"], ["api-forbids-ui"])
        mismatch = dict(valid, scope_digest="sha256:" + "0" * 64)
        self.assertEqual(self.audit(value, mismatch, "src/api/file.py")["status"], "NEEDS_CONTEXT")

    def test_incomplete_rule_coverage(self):
        value = manifest()
        partial = self.evidence(["src/api/file.py"], [])
        self.assertEqual(self.audit(value, partial, "src/api/file.py")["status"], "NEEDS_CONTEXT")

    def test_forbid_observed_edge_is_violated(self):
        edge = {"rule_id": "api-forbids-ui", "source_component": "api", "target_component": "ui", "evidence_path": "src/api/file.py", "line": 12}
        result = self.audit(manifest(), self.evidence(["src/api/file.py"], ["api-forbids-ui"], [edge]), "src/api/file.py")
        self.assertEqual({key: result[key] for key in ("version", "aggregate_verdict", "rule_results")}, {"version": 1, "aggregate_verdict": "VIOLATED", "rule_results": [{"rule_id": "api-forbids-ui", "verdict": "VIOLATED", "evidence_paths": ["src/api/file.py"]}]})

    def test_allow_observed_edge_is_maintained(self):
        value = manifest(rules=[{"id": "api-allows-ui", "source": "api", "target": "ui", "policy": "allow", "rationale": "test"}])
        edge = {"rule_id": "api-allows-ui", "source_component": "api", "target_component": "ui", "evidence_path": "src/api/file.py", "line": 1}
        result = self.audit(value, self.evidence(["src/api/file.py"], ["api-allows-ui"], [edge]), "src/api/file.py")
        self.assertEqual(result["aggregate_verdict"], "MAINTAINED")

    def test_verdict_precedence(self):
        components = manifest()["components"] + [{"id": "db", "paths": ["src/db/**"], "owner": "data", "shared": False}]
        rules = [
            {"id": "api-allows-db", "source": "api", "target": "db", "policy": "allow", "rationale": "test"},
            {"id": "api-forbids-ui", "source": "api", "target": "ui", "policy": "forbid", "rationale": "test"},
        ]
        edge = {"rule_id": "api-forbids-ui", "source_component": "api", "target_component": "ui", "evidence_path": "src/api/file.py", "line": 1}
        result = self.audit(manifest(components=components, rules=rules), self.evidence(["src/api/file.py"], ["api-allows-db", "api-forbids-ui"], [edge]), "src/api/file.py")
        self.assertEqual(result["aggregate_verdict"], "VIOLATED")

    def test_no_manifest_fallback(self):
        self.assertEqual(self.invoke("--mode", "validate")["contract_state"], "N/A — no architecture contract")

    def test_component_shared_defaults_to_false(self):
        value = manifest()
        del value["components"][0]["shared"]
        self.write_json("contract.json", value)
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "DONE")
        normalized = HELPER.validate_manifest(value, self.repo)
        self.assertEqual([item["shared"] for item in normalized["components"]], [False, False])

    def test_component_shared_must_be_boolean_when_present(self):
        value = manifest()
        value["components"][0]["shared"] = "yes"
        self.write_json("contract.json", value)
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_component_unknown_field_rejected_when_shared_omitted(self):
        value = manifest()
        del value["components"][0]["shared"]
        value["components"][0]["command"] = "echo unsafe"
        self.write_json("contract.json", value)
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_root_manifest_symlink_escape_is_not_absent(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "contract.json"
            target.write_text(json.dumps(manifest()), encoding="utf-8")
            (self.repo / "architecture-invariants.json").symlink_to(target)
            result = self.invoke("--mode", "validate")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")
        self.assertNotEqual(result["contract_state"], "N/A — no architecture contract")

    def test_root_manifest_dangling_symlink_is_not_absent(self):
        (self.repo / "architecture-invariants.json").symlink_to(self.repo / "missing-contract.json")
        result = self.invoke("--mode", "validate")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")
        self.assertNotEqual(result["contract_state"], "N/A — no architecture contract")

    def test_audit_projection_exposes_component_ids(self):
        result = self.audit(manifest(), self.evidence(["src/api/file.py"], ["api-forbids-ui"]), "src/api/file.py")
        self.assertEqual(result["status"], "DONE")
        self.assertEqual(result["component_ids"], ["api"])
        self.assertEqual(result["contract_state"], "VALIDATED")
        self.assertEqual(result["evidence_artifact_path"], HELPER.ARCHITECTURE_EVIDENCE_PATH)

    def test_audit_artifact_projection_stays_closed(self):
        result = self.audit(manifest(), self.evidence(["src/api/file.py"], ["api-forbids-ui"]), "src/api/file.py")
        artifact = json.loads((self.repo / HELPER.ARCHITECTURE_EVIDENCE_PATH).read_text(encoding="utf-8"))
        self.assertEqual(set(artifact), HELPER.RESULT_KEYS)
        self.assertEqual(HELPER.validate_audit_result(artifact, root=self.repo)["aggregate_verdict"], result["aggregate_verdict"])

    def test_validate_advisory_terminal_state(self):
        self.write_json("contract.json", manifest())
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "DONE")

    def test_validate_enforced_terminal_state(self):
        self.write_json("contract.json", manifest(enforcement="enforced"))
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "BLOCKED")

    def test_absent_forbid_edge_is_maintained(self):
        result = self.audit(manifest(), self.evidence(["src/api/file.py"], ["api-forbids-ui"]), "src/api/file.py")
        self.assertEqual(result["aggregate_verdict"], "MAINTAINED")

    def test_absent_allow_edge_is_not_maintained(self):
        value = manifest(rules=[{"id": "api-allows-ui", "source": "api", "target": "ui", "policy": "allow", "rationale": "test"}])
        result = self.audit(value, self.evidence(["src/api/file.py"], ["api-allows-ui"]), "src/api/file.py")
        self.assertEqual(result["aggregate_verdict"], "N/A")

    def assert_nested_forbidden_field(self, field):
        value = self.evidence(["src/api/file.py"], ["api-forbids-ui"])
        value["metadata"] = {field: "secret"}
        result = self.audit(manifest(), value, "src/api/file.py")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")
        self.assertNotIn(field, json.dumps(result))

    def test_raw_command_rejected_recursively(self):
        self.assert_nested_forbidden_field("raw_command")

    def test_raw_command_output_rejected_recursively(self):
        self.assert_nested_forbidden_field("raw_command_output")

    def test_transcript_rejected_recursively(self):
        self.assert_nested_forbidden_field("transcript")

    def test_chain_of_thought_rejected_recursively(self):
        self.assert_nested_forbidden_field("chain_of_thought")

    def test_generated_source_rejected_recursively(self):
        self.assert_nested_forbidden_field("generated_source")

    def test_full_diff_rejected_recursively(self):
        self.assert_nested_forbidden_field("full_diff")

    def test_unsafe_manifest_path_rejected(self):
        value = manifest()
        value["components"][0]["paths"] = ["../outside/**"]
        self.write_json("contract.json", value)
        self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "NEEDS_CONTEXT")

    def test_unsafe_evidence_path_rejected_and_omitted(self):
        value = self.evidence(["src/api/file.py"], ["api-forbids-ui"])
        value["edges"] = [{"rule_id": "api-forbids-ui", "source_component": "api", "target_component": "ui", "evidence_path": "../escape", "line": 1}]
        result = self.audit(manifest(), value, "src/api/file.py")
        self.assertEqual(result["status"], "NEEDS_CONTEXT")
        self.assertNotIn("../escape", json.dumps(result))

    def launch_patches(self, launches):
        return [
            mock.patch.object(subprocess, name, side_effect=lambda *a, _name=name, **k: launches.append((_name, a, k)))
            for name in ("Popen", "run", "call", "check_call", "check_output")
        ] + [
            mock.patch.object(os, name, side_effect=lambda *a, _name=name, **k: launches.append((_name, a, k)))
            for name in ("system", "popen", "spawnv", "spawnve")
        ]

    def test_zero_child_processes(self):
        launches = []
        with contextlib.ExitStack() as stack:
            for patcher in self.launch_patches(launches):
                stack.enter_context(patcher)
            self.write_json("contract.json", manifest())
            self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "DONE")
            self.assertEqual(self.invoke("--mode", "validate", "--manifest", "contract.json")["status"], "DONE")
            edge = {"rule_id": "api-forbids-ui", "source_component": "api", "target_component": "ui", "evidence_path": "src/api/file.py", "line": 1}
            self.assertEqual(self.audit(manifest(), self.evidence(["src/api/file.py"], ["api-forbids-ui"], [edge]), "src/api/file.py")["status"], "DONE")
            self.write_json("proposal.json", manifest())
            self.assertEqual(self.invoke("--mode", "draft", "--proposal", "proposal.json", "--output", "draft.json", "--approve-write")["status"], "DONE")
            adversarial = manifest()
            adversarial["components"][0]["script"] = "echo unsafe"
            self.write_json("bad.json", adversarial)
            self.assertEqual(self.invoke("--mode", "validate", "--manifest", "bad.json")["status"], "NEEDS_CONTEXT")
            bad_evidence = self.evidence(["src/api/file.py"], ["api-forbids-ui"])
            bad_evidence["raw_command"] = "echo unsafe"
            self.write_json("bad-evidence.json", bad_evidence)
            self.write_json("contract.json", manifest())
            self.assertEqual(self.invoke("--mode", "audit", "--manifest", "contract.json", "--changed-path", "src/api/file.py", "--evidence", "bad-evidence.json")["status"], "NEEDS_CONTEXT")
            bad_proposal = manifest()
            bad_proposal["raw_command_output"] = "unsafe"
            self.write_json("bad-proposal.json", bad_proposal)
            self.assertEqual(self.invoke("--mode", "draft", "--proposal", "bad-proposal.json", "--output", "bad-draft.json", "--approve-write")["status"], "NEEDS_CONTEXT")
        self.assertEqual(launches, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
