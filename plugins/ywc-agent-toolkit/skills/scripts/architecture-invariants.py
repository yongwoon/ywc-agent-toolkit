#!/usr/bin/env python3
"""Closed, validation-only architecture invariants contract helper."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


VERSION = 1
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
MANIFEST_KEYS = {"version", "owner", "enforcement", "components", "rules"}
COMPONENT_KEYS = {"id", "paths", "owner", "shared"}
RULE_KEYS = {"id", "source", "target", "policy", "rationale"}
EVIDENCE_KEYS = {"version", "scope_paths", "scope_digest", "covered_rule_ids", "edges"}
EDGE_KEYS = {"rule_id", "source_component", "target_component", "evidence_path", "line"}
RESULT_KEYS = {"version", "aggregate_verdict", "rule_results"}
RESULT_ITEM_KEYS = {"rule_id", "verdict", "evidence_paths"}


class ContractError(ValueError):
    pass


def _fail(message):
    raise ContractError(message)


def _object(value, keys, label):
    if not isinstance(value, dict) or set(value) != keys:
        _fail("%s must have exactly these fields: %s" % (label, ", ".join(sorted(keys))))


def _path(value, root, glob=False):
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        _fail("invalid repository-relative path")
    if value.startswith("/") or value.startswith("./") or "//" in value:
        _fail("unsafe path")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        _fail("unsafe path")
    if glob:
        for index, part in enumerate(parts):
            if part == "**" and index != len(parts) - 1:
                _fail("** is only valid as a terminal glob segment")
            if part == "**":
                continue
            if part == "*":
                continue
            if "*" in part or any(char in part for char in "?[]{}"):
                _fail("unsupported glob syntax")
    candidate = root.joinpath(*parts)
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except ValueError:
        _fail("path escapes repository root")
    if candidate.exists():
        try:
            candidate.resolve().relative_to(root.resolve())
        except ValueError:
            _fail("symlink escapes repository root")
    return "/".join(parts)


def normalize_paths(values, root, glob=False):
    if not isinstance(values, list) or not values:
        _fail("paths must be a non-empty array")
    result = [_path(value, root, glob=glob) for value in values]
    if len(set(result)) != len(result):
        _fail("duplicate paths")
    return sorted(result)


def validate_manifest(manifest, root):
    _object(manifest, MANIFEST_KEYS, "manifest")
    if not isinstance(manifest["version"], int) or isinstance(manifest["version"], bool) or manifest["version"] != VERSION:
        _fail("manifest version must be 1")
    if not isinstance(manifest["owner"], str) or not manifest["owner"].strip():
        _fail("manifest owner is required")
    if manifest["enforcement"] not in ("advisory", "enforced"):
        _fail("invalid enforcement")
    components = manifest["components"]
    rules = manifest["rules"]
    if not isinstance(components, list) or not components or not isinstance(rules, list) or not rules:
        _fail("components and rules must be non-empty arrays")
    normalized = {"version": 1, "owner": manifest["owner"], "enforcement": manifest["enforcement"], "components": [], "rules": []}
    component_ids = set()
    for item in components:
        _object(item, COMPONENT_KEYS, "component")
        if not isinstance(item["id"], str) or not ID_RE.fullmatch(item["id"]):
            _fail("invalid component id")
        if item["id"] in component_ids:
            _fail("duplicate component id")
        component_ids.add(item["id"])
        if not isinstance(item["owner"], str) or not item["owner"].strip() or not isinstance(item["shared"], bool):
            _fail("invalid component metadata")
        normalized["components"].append({"id": item["id"], "paths": normalize_paths(item["paths"], root, glob=True), "owner": item["owner"], "shared": item["shared"]})
    pairs = set()
    rule_ids = set()
    for item in rules:
        _object(item, RULE_KEYS, "rule")
        if not isinstance(item["id"], str) or not ID_RE.fullmatch(item["id"]):
            _fail("invalid rule id")
        if item["id"] in rule_ids:
            _fail("duplicate rule id")
        if item["source"] not in component_ids or item["target"] not in component_ids or item["source"] == item["target"]:
            _fail("invalid rule endpoint")
        pair = (item["source"], item["target"])
        if pair in pairs:
            _fail("duplicate rule endpoint")
        pairs.add(pair)
        if item["policy"] not in ("allow", "forbid") or not isinstance(item["rationale"], str) or not item["rationale"].strip():
            _fail("invalid rule")
        rule_ids.add(item["id"])
        normalized["rules"].append(dict(item))
    normalized["components"].sort(key=lambda item: item["id"])
    normalized["rules"].sort(key=lambda item: item["id"])
    return normalized


def path_matches(pattern, path):
    pattern_parts, path_parts = pattern.split("/"), path.split("/")
    if pattern_parts[-1] == "**":
        if len(path_parts) < len(pattern_parts) - 1:
            return False
        pattern_parts = pattern_parts[:-1]
        path_parts = path_parts[:len(pattern_parts)]
    if len(pattern_parts) != len(path_parts):
        return False
    return all(expected == actual or expected == "*" for expected, actual in zip(pattern_parts, path_parts))


def component_matches(manifest, path):
    matches = [component for component in manifest["components"] if any(path_matches(pattern, path) for pattern in component["paths"])]
    non_shared = [component for component in matches if not component["shared"]]
    return matches, non_shared


def scope_digest(paths):
    return "sha256:" + hashlib.sha256("\n".join(paths).encode("utf-8")).hexdigest()


def validate_evidence(evidence, manifest, root):
    _object(evidence, EVIDENCE_KEYS, "evidence")
    if not isinstance(evidence["version"], int) or isinstance(evidence["version"], bool) or evidence["version"] != VERSION:
        _fail("evidence version must be 1")
    scope = normalize_paths(evidence["scope_paths"], root)
    covered = evidence["covered_rule_ids"]
    if not isinstance(covered, list) or any(not isinstance(item, str) for item in covered) or covered != sorted(set(covered)):
        _fail("covered_rule_ids must be sorted and duplicate-free")
    rule_map = {rule["id"]: rule for rule in manifest["rules"]}
    if any(item not in rule_map for item in covered):
        _fail("unknown covered rule")
    if not isinstance(evidence["scope_digest"], str) or not SHA_RE.fullmatch(evidence["scope_digest"]):
        _fail("invalid scope digest")
    if evidence["scope_digest"] != scope_digest(scope):
        _fail("scope digest mismatch")
    edges = evidence["edges"]
    if not isinstance(edges, list):
        _fail("edges must be an array")
    normalized_edges = []
    seen = set()
    for edge in edges:
        _object(edge, EDGE_KEYS, "edge")
        if edge["rule_id"] not in rule_map or edge["source_component"] not in {c["id"] for c in manifest["components"]} or edge["target_component"] not in {c["id"] for c in manifest["components"]}:
            _fail("edge references unknown id")
        if not isinstance(edge["line"], int) or isinstance(edge["line"], bool) or edge["line"] <= 0:
            _fail("edge line must be positive")
        path = _path(edge["evidence_path"], root)
        if path not in scope:
            _fail("edge path is outside scope")
        key = (edge["rule_id"], path, edge["line"])
        if key in seen:
            _fail("duplicate edge")
        seen.add(key)
        rule = rule_map[edge["rule_id"]]
        if (rule["source"], rule["target"]) != (edge["source_component"], edge["target_component"]):
            _fail("edge endpoint does not match rule")
        normalized_edges.append(dict(edge, evidence_path=path))
    normalized_edges.sort(key=lambda edge: (edge["rule_id"], edge["evidence_path"], edge["line"]))
    return {"version": 1, "scope_paths": scope, "scope_digest": scope_digest(scope), "covered_rule_ids": sorted(covered), "edges": normalized_edges}


def audit(manifest, evidence, changed_paths, root):
    manifest = validate_manifest(manifest, root)
    evidence = validate_evidence(evidence, manifest, root)
    changed = normalize_paths(changed_paths, root)
    if changed != evidence["scope_paths"]:
        _fail("changed scope does not equal evidence scope")
    mapping = {}
    for path in changed:
        _, non_shared = component_matches(manifest, path)
        if len(non_shared) != 1:
            _fail("ambiguous component mapping")
        mapping[path] = non_shared[0]["id"]
    affected = []
    for rule in manifest["rules"]:
        if any(mapping[path] in (rule["source"], rule["target"]) for path in changed):
            affected.append(rule)
    affected_ids = sorted(rule["id"] for rule in affected)
    if sorted(evidence["covered_rule_ids"]) != affected_ids:
        _fail("incomplete or extraneous rule coverage")
    edges_by_rule = {rule_id: [] for rule_id in affected_ids}
    for edge in evidence["edges"]:
        if edge["rule_id"] in edges_by_rule:
            _, non_shared = component_matches(manifest, edge["evidence_path"])
            if len(non_shared) != 1 or non_shared[0]["id"] != edge["source_component"]:
                _fail("evidence source mapping is ambiguous or mismatched")
            edges_by_rule[edge["rule_id"]].append(edge["evidence_path"])
    results = []
    for rule in sorted(affected, key=lambda item: item["id"]):
        paths = sorted(set(edges_by_rule[rule["id"]]))
        if paths:
            verdict = "VIOLATED" if rule["policy"] == "forbid" else "MAINTAINED"
        elif rule["policy"] == "forbid":
            verdict = "MAINTAINED"
        else:
            verdict = "N/A"
        results.append({"rule_id": rule["id"], "verdict": verdict, "evidence_paths": paths})
    order = {"VIOLATED": 0, "NEEDS_CONTEXT": 1, "MAINTAINED": 2, "N/A": 3}
    aggregate = min((item["verdict"] for item in results), key=lambda verdict: order[verdict], default="N/A")
    return {"version": 1, "aggregate_verdict": aggregate, "rule_results": results}


def _load(path, root):
    normalized = _path(path, root)
    try:
        return json.loads(root.joinpath(*normalized.split("/")).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail("cannot read JSON: %s" % exc)


def _manifest(args, root):
    if args.manifest:
        return validate_manifest(_load(args.manifest, root), root)
    path = root / "architecture-invariants.json"
    if not path.exists():
        return None
    return validate_manifest(json.loads(path.read_text(encoding="utf-8")), root)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ywc-architecture-invariants")
    parser.add_argument("--mode", choices=("draft", "validate", "audit"), required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--proposal")
    parser.add_argument("--output")
    parser.add_argument("--approve-write", action="store_true")
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--evidence")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    try:
        if args.mode == "draft":
            if args.manifest or not args.proposal or not args.output or not args.approve_write:
                _fail("draft requires proposal, output, and --approve-write; --manifest is invalid")
            output = _path(args.output, root)
            destination = root.joinpath(*output.split("/"))
            if destination.exists():
                _fail("draft output already exists")
            manifest = validate_manifest(_load(args.proposal, root), root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            result = {"status": "DONE", "contract_state": "MAINTAINED", "evidence_path": output}
        elif args.mode == "validate":
            if args.proposal or args.output or args.approve_write or args.evidence or args.changed_path:
                _fail("invalid validate arguments")
            manifest = _manifest(args, root)
            if manifest is None:
                result = {"status": "N/A", "contract_state": "N/A — no architecture contract"}
            elif manifest["enforcement"] == "advisory":
                result = {"status": "DONE", "contract_state": "ADVISORY", "invariant_verdict": "ADVISORY"}
            else:
                result = {"status": "BLOCKED", "contract_state": "enforced", "invariant_verdict": "NEEDS_CONTEXT", "next_action": "v1 has no verifier executor"}
        else:
            if args.manifest is None and not args.evidence:
                result = {"status": "N/A", "aggregate_verdict": "N/A", "contract_state": "N/A — no architecture contract"}
            elif not args.changed_path or not args.evidence:
                _fail("audit requires changed paths and evidence")
            else:
                manifest = _manifest(args, root)
                if manifest is None:
                    result = {"status": "N/A", "aggregate_verdict": "N/A", "contract_state": "N/A — no architecture contract"}
                else:
                    result = {"status": "DONE", **audit(manifest, _load(args.evidence, root), args.changed_path, root)}
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "NEEDS_CONTEXT", "contract_state": "NEEDS_CONTEXT", "next_action": str(exc)}, sort_keys=True))
        return 0


if __name__ == "__main__":
    sys.exit(main())
