#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_FAMILIES = {
    "git_implementation",
    "git_hydration",
}

ALLOWED_BACKENDS = {
    "gix": "git_implementation",
    "sem": "git_implementation",
    "marimo": "git_hydration",
}

ALLOWED_ARTIFACT_KINDS = {
    "state_projection",
    "enrichment_projection",
    "hydration_projection",
}

PRIMARY_OPERATOR_SURFACE = "control_realize_git_substrate_adapters_v1.py"


class RealizationError(Exception):
    pass


@dataclass(frozen=True)
class GitObject:
    ref: str
    object_kind: str
    title: str
    summary: str
    attributes: dict[str, Any]


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RealizationError(f"missing JSON artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RealizationError(f"invalid JSON in {path}: {exc}") from exc


def require_keys(obj: dict[str, Any], keys: list[str], ctx: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise RealizationError(f"{ctx} missing required keys: {', '.join(missing)}")


def resolve_artifact_ref(cwd: Path, ref: str) -> Path:
    if not ref.startswith("artifact:"):
        raise RealizationError(f"unsupported authority ref: {ref}")
    return cwd / ref.removeprefix("artifact:")


def normalize_objects(model: dict[str, Any]) -> dict[str, GitObject]:
    objects: dict[str, GitObject] = {}
    for raw in model.get("objects", []):
        require_keys(raw, ["ref", "object_kind", "title", "summary", "attributes"], "object")
        ref = str(raw["ref"])
        objects[ref] = GitObject(
            ref=ref,
            object_kind=str(raw["object_kind"]),
            title=str(raw["title"]),
            summary=str(raw["summary"]),
            attributes=dict(raw["attributes"]),
        )
    return objects


def validate_unified_document(document: dict[str, Any], schema: dict[str, Any], ctx: str) -> None:
    require_keys(document, list(schema.get("required", [])), ctx)
    properties = schema.get("properties", {})
    additional_allowed = schema.get("additionalProperties", True)
    if additional_allowed is False:
        extra = sorted(set(document) - set(properties))
        if extra:
            raise RealizationError(f"{ctx} has unexpected keys: {', '.join(extra)}")
    for key, prop in properties.items():
        if key not in document:
            continue
        value = document[key]
        if "const" in prop and value != prop["const"]:
            raise RealizationError(f"{ctx}.{key} must equal {prop['const']!r}")
        prop_type = prop.get("type")
        if prop_type == "string" and not isinstance(value, str):
            raise RealizationError(f"{ctx}.{key} must be a string")
        if prop_type == "boolean" and not isinstance(value, bool):
            raise RealizationError(f"{ctx}.{key} must be a boolean")
        if prop_type == "integer" and not isinstance(value, int):
            raise RealizationError(f"{ctx}.{key} must be an integer")
        if prop_type == "array":
            if not isinstance(value, list):
                raise RealizationError(f"{ctx}.{key} must be an array")
            item_schema = prop.get("items", {})
            if item_schema.get("type") == "object":
                for idx, item in enumerate(value):
                    if not isinstance(item, dict):
                        raise RealizationError(f"{ctx}.{key}[{idx}] must be an object")
                    validate_unified_document(item, item_schema, f"{ctx}.{key}[{idx}]")
            elif item_schema.get("type") == "string":
                for idx, item in enumerate(value):
                    if not isinstance(item, str):
                        raise RealizationError(f"{ctx}.{key}[{idx}] must be a string")
        if prop_type == "object" and isinstance(value, dict):
            nested_required = prop.get("required", [])
            for nested_key in nested_required:
                if nested_key not in value:
                    raise RealizationError(f"{ctx}.{key} missing required key: {nested_key}")


def git_run(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RealizationError(f"git command failed ({' '.join(args)}): {result.stderr.strip()}")
    return result.stdout


def parse_repository_ref(repo_ref: str) -> Path:
    if not repo_ref.startswith("repo:"):
        raise RealizationError(f"unsupported repository_ref: {repo_ref}")
    return Path(repo_ref.removeprefix("repo:"))


def emit_repo_state(obj: GitObject) -> dict[str, Any]:
    repo = parse_repository_ref(str(obj.attributes["repository_ref"]))
    head = git_run(repo, "rev-parse", "HEAD").strip()
    branch = git_run(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    status_lines = [line for line in git_run(repo, "status", "--porcelain").splitlines() if line.strip()]
    return {
        "document_type": "repo_state",
        "repository_path": str(repo),
        "head": head,
        "branch": branch,
        "clean": len(status_lines) == 0,
        "status_entries": status_lines,
        "state_kind": obj.attributes["state_kind"],
    }


def emit_diff_state(obj: GitObject) -> dict[str, Any]:
    repo = parse_repository_ref(str(obj.attributes["repository_ref"]))
    comparison_ref = str(obj.attributes["comparison_ref"])
    base_ref = git_run(repo, "merge-base", "HEAD", comparison_ref).strip()
    head = git_run(repo, "rev-parse", "HEAD").strip()
    raw_name_status = git_run(repo, "diff", "--name-status", f"{base_ref}..{head}")
    changed_files: list[dict[str, Any]] = []
    for line in raw_name_status.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            changed_files.append({"status": parts[0], "path": parts[-1]})
    raw_numstat = git_run(repo, "diff", "--numstat", f"{base_ref}..{head}")
    numstat: list[dict[str, Any]] = []
    for line in raw_numstat.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            numstat.append({"added": parts[0], "deleted": parts[1], "path": parts[2]})
    return {
        "document_type": "diff_state",
        "repository_path": str(repo),
        "comparison_ref": comparison_ref,
        "comparison_base": base_ref,
        "head": head,
        "changed_files": changed_files,
        "file_count": len(changed_files),
        "numstat": numstat,
        "state_kind": obj.attributes["state_kind"],
    }


def emit_semantic_diff(semantic_obj: GitObject, review_obj: GitObject, diff_state: dict[str, Any]) -> dict[str, Any]:
    changed_files = diff_state["changed_files"]
    by_status: dict[str, int] = {}
    by_extension: dict[str, int] = {}
    for item in changed_files:
        status = str(item["status"])
        path = str(item["path"])
        by_status[status] = by_status.get(status, 0) + 1
        ext = Path(path).suffix or "<none>"
        by_extension[ext] = by_extension.get(ext, 0) + 1
    return {
        "document_type": "semantic_diff",
        "repository_path": semantic_obj.attributes["repository_ref"],
        "upstream_diff_ref": semantic_obj.attributes["upstream_diff_ref"],
        "review_basis_rule": review_obj.attributes["basis_rule"],
        "change_summary": {
            "file_count": diff_state["file_count"],
            "by_status": by_status,
            "by_extension": by_extension,
        },
        "review_basis": {
            "requires_repo_state_and_diff_state": True,
            "comparison_ref": diff_state["comparison_ref"],
            "comparison_base": diff_state["comparison_base"],
        },
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_manifest(root: Path, payload: dict[str, Any], emitted: list[dict[str, Any]], cwd: Path) -> Path:
    manifest = {
        "document_type": "realization_manifest",
        "schema_version": "v2",
        "workflow_command": payload["workflow"]["command"],
        "deterministic": payload["workflow"]["deterministic"],
        "primary_operator_surface": PRIMARY_OPERATOR_SURFACE,
        "targets": emitted,
    }
    schema = load_json(cwd.parent / "cli_extension_v2" / "unified_realization_manifest.v2.schema.json")
    validate_unified_document(manifest, schema, "realization_manifest")
    path = root / "build" / "realization_manifest.json"
    write_json(path, manifest)
    return path


def build_report(
    root: Path,
    payload_path: Path,
    emitted: list[dict[str, Any]],
    backend_reports: dict[str, Any],
    cwd: Path,
) -> Path:
    report = {
        "document_type": "realization_report",
        "schema_version": "v2",
        "status": "success",
        "payload_path": str(payload_path),
        "primary_operator_surface": PRIMARY_OPERATOR_SURFACE,
        "realized_count": len(emitted),
        "targets": emitted,
        "backend_reports": backend_reports,
    }
    schema = load_json(cwd.parent / "cli_extension_v2" / "unified_realization_report.v2.schema.json")
    validate_unified_document(report, schema, "realization_report")
    path = root / "build" / "realization_report.json"
    write_json(path, report)
    return path


def validate_payload(cwd: Path, payload: dict[str, Any]) -> tuple[dict[str, GitObject], dict[str, Any]]:
    require_keys(payload, ["authority_inputs", "realization_scope", "targets", "workflow"], "payload")
    authority = payload["authority_inputs"]
    require_keys(authority, ["canonical_model_ref", "profile_ref", "projection_manifest_ref"], "authority_inputs")
    for key, ref in authority.items():
        path = resolve_artifact_ref(cwd, ref)
        if not path.exists():
            raise RealizationError(f"{key} does not resolve locally: {ref}")

    model = load_json(resolve_artifact_ref(cwd, authority["canonical_model_ref"]))
    objects = normalize_objects(model)
    object_refs = set(objects)

    scope = payload["realization_scope"]
    require_keys(scope, ["allowed_adapter_families", "allowed_backends"], "realization_scope")
    allowed_families = set(scope["allowed_adapter_families"])
    allowed_backends = set(scope["allowed_backends"])
    if allowed_families - ALLOWED_FAMILIES:
        raise RealizationError(f"unknown adapter families: {sorted(allowed_families - ALLOWED_FAMILIES)}")
    if allowed_backends - set(ALLOWED_BACKENDS):
        raise RealizationError(f"unknown backends: {sorted(allowed_backends - set(ALLOWED_BACKENDS))}")

    seen_ids: set[str] = set()
    for target in payload["targets"]:
        require_keys(
            target,
            ["target_id", "backend", "adapter_family", "projection_role", "inputs", "artifact_kind", "repo_path"],
            "target",
        )
        target_id = str(target["target_id"])
        if target_id in seen_ids:
            raise RealizationError(f"duplicate target_id: {target_id}")
        seen_ids.add(target_id)
        backend = str(target["backend"])
        family = str(target["adapter_family"])
        if backend not in allowed_backends:
            raise RealizationError(f"target {target_id}: backend '{backend}' not enabled")
        if family not in allowed_families:
            raise RealizationError(f"target {target_id}: adapter_family '{family}' not enabled")
        if ALLOWED_BACKENDS[backend] != family:
            raise RealizationError(f"target {target_id}: backend '{backend}' does not match adapter_family '{family}'")
        artifact_kind = str(target["artifact_kind"])
        if artifact_kind not in ALLOWED_ARTIFACT_KINDS:
            raise RealizationError(f"target {target_id}: unsupported artifact_kind '{artifact_kind}'")
        inputs = [str(x) for x in target["inputs"]]
        if not inputs:
            raise RealizationError(f"target {target_id}: inputs must not be empty")
        missing = sorted(set(inputs) - object_refs)
        if missing:
            raise RealizationError(f"target {target_id}: unresolved semantic inputs: {', '.join(missing)}")
        if backend == "sem":
            semantic_objects = [objects[ref] for ref in inputs]
            semantic_surface = next(
                (obj for obj in semantic_objects if obj.attributes.get("git_substrate_role") == "semantic_diff_surface"),
                None,
            )
            if semantic_surface is None:
                raise RealizationError(f"target {target_id}: sem target missing semantic_diff_surface input")
            upstream_diff_ref = str(semantic_surface.attributes.get("upstream_diff_ref", ""))
            if upstream_diff_ref not in object_refs:
                raise RealizationError(
                    f"target {target_id}: semantic_diff_surface upstream_diff_ref does not resolve: {upstream_diff_ref}"
                )

    workflow = payload["workflow"]
    require_keys(workflow, ["command", "deterministic", "overwrite_policy", "manifest_update"], "workflow")
    if workflow["command"] != "control realize git-substrate-adapters-v1":
        raise RealizationError("workflow.command must be exactly 'control realize git-substrate-adapters-v1'")
    if workflow["deterministic"] is not True:
        raise RealizationError("workflow.deterministic must be true")

    return objects, payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="control realize git-substrate-adapters-v1",
        description="Unified realization runner for the first Git-substrate adapter slice.",
    )
    parser.add_argument("--payload", default="realization_payload.v1.json")
    parser.add_argument("--root", default=".")
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    cwd = Path(__file__).resolve().parent
    payload_path = (cwd / args.payload).resolve() if not Path(args.payload).is_absolute() else Path(args.payload)
    root = Path(args.root).resolve()

    try:
        payload = load_json(payload_path)
        objects, payload = validate_payload(cwd, payload)
        if args.check_only:
            print(json.dumps({"status": "ok", "validated_targets": len(payload["targets"])}, indent=2))
            return 0

        emitted: list[dict[str, Any]] = []
        backend_reports: dict[str, Any] = {"gix": {"targets": []}, "sem": {"targets": []}}
        repo_state_doc: dict[str, Any] | None = None
        diff_state_doc: dict[str, Any] | None = None

        for target in payload["targets"]:
            backend = str(target["backend"])
            target_id = str(target["target_id"])
            output_path = root / str(target["repo_path"])
            input_objects = [objects[str(ref)] for ref in target["inputs"]]

            if backend == "gix":
                surface = input_objects[0]
                role = str(surface.attributes.get("git_substrate_role"))
                if role == "repo_state_surface":
                    repo_state_doc = emit_repo_state(surface)
                    write_json(output_path, repo_state_doc)
                    backend_reports["gix"]["targets"].append({"target_id": target_id, "status": "ok", "kind": role})
                elif role == "diff_state_surface":
                    diff_state_doc = emit_diff_state(surface)
                    write_json(output_path, diff_state_doc)
                    backend_reports["gix"]["targets"].append({"target_id": target_id, "status": "ok", "kind": role})
                else:
                    raise RealizationError(f"target {target_id}: unsupported gix role {role!r}")
                emitted.append(
                    {
                        "target_id": target_id,
                        "backend": backend,
                        "adapter_family": str(target["adapter_family"]),
                        "projection_role": str(target["projection_role"]),
                        "artifact_kind": str(target["artifact_kind"]),
                        "repo_path": str(target["repo_path"]),
                        "output_path": str(output_path),
                        "source_project_root": str(parse_repository_ref(str(surface.attributes["repository_ref"]))),
                        "semantic_inputs": [str(x) for x in target["inputs"]],
                        "generated_by": PRIMARY_OPERATOR_SURFACE,
                    }
                )
            elif backend == "sem":
                if diff_state_doc is None:
                    diff_source = next(
                        obj for obj in objects.values() if obj.attributes.get("git_substrate_role") == "diff_state_surface"
                    )
                    diff_state_doc = emit_diff_state(diff_source)
                semantic_obj = next(obj for obj in input_objects if obj.attributes.get("git_substrate_role") == "semantic_diff_surface")
                review_obj = next(obj for obj in input_objects if obj.attributes.get("git_substrate_role") == "review_basis_surface")
                semantic_diff_doc = emit_semantic_diff(semantic_obj, review_obj, diff_state_doc)
                write_json(output_path, semantic_diff_doc)
                backend_reports["sem"]["targets"].append({"target_id": target_id, "status": "ok", "kind": "semantic_diff_surface"})
                emitted.append(
                    {
                        "target_id": target_id,
                        "backend": backend,
                        "adapter_family": str(target["adapter_family"]),
                        "projection_role": str(target["projection_role"]),
                        "artifact_kind": str(target["artifact_kind"]),
                        "repo_path": str(target["repo_path"]),
                        "output_path": str(output_path),
                        "source_project_root": str(parse_repository_ref(str(semantic_obj.attributes["repository_ref"]))),
                        "upstream_deterministic_input": str(semantic_obj.attributes["upstream_diff_ref"]),
                        "semantic_inputs": [str(x) for x in target["inputs"]],
                        "generated_by": PRIMARY_OPERATOR_SURFACE,
                    }
                )

        manifest_path = build_manifest(root, payload, emitted, cwd)
        report_path = build_report(root, payload_path, emitted, backend_reports, cwd)
        print(
            json.dumps(
                {
                    "status": "success",
                    "realized_targets": len(emitted),
                    "manifest": str(manifest_path),
                    "report": str(report_path),
                },
                indent=2,
            )
        )
        return 0
    except RealizationError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
