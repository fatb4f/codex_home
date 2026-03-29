#!/usr/bin/env python3
"""Validate implement packet structure and response-contract outputs."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

import jsonschema

REQUIRED_SECTIONS = [
    'artifact_paths',
    'execution_context',
    'scope_lock',
    'issue_map',
    'work_queue',
    'evidence_required',
    'gates',
    'execution',
    'results',
    'rollback',
    'closeout_decision',
]
HEADING_RE = re.compile(r'^##\s+([A-Za-z0-9_ -]+)\s*$')


def validate_json(instance_path: Path, schema_path: Path) -> list[str]:
    instance = json.loads(instance_path.read_text(encoding='utf-8'))
    schema = json.loads(schema_path.read_text(encoding='utf-8'))
    resolver = jsonschema.validators.RefResolver(base_uri=schema_path.resolve().as_uri(), referrer=schema)
    validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    return [e.message for e in validator.iter_errors(instance)]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('path', nargs='?', default='IMPLEMENT.md')
    p.add_argument('--wt', default=None)
    p.add_argument('--contract-root', default='.')
    args = p.parse_args()

    path = Path(args.path).expanduser().resolve()
    wt = Path(args.wt or os.environ.get('WT') or path.parent.parent).expanduser().resolve()
    contract_root = Path(args.contract_root).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f'file not found: {path}')

    lines = path.read_text(encoding='utf-8').splitlines()
    found = {m.group(1).strip() for ln in lines if (m := HEADING_RE.match(ln.strip()))}
    errors: list[str] = []
    for sec in REQUIRED_SECTIONS:
        if sec not in found:
            errors.append(f'missing section: ## {sec}')

    impl_dir = wt / 'IMPLEMENT'
    response_instance_path = impl_dir / 'response.instance.json'
    response_manifest_path = impl_dir / 'response.manifest.json'
    response_validation_path = impl_dir / 'response.validation.json'
    for req in (response_instance_path, response_manifest_path, response_validation_path):
        if not req.exists():
            errors.append(f'missing artifact: {req}')

    if response_instance_path.exists():
        for err in validate_json(response_instance_path, contract_root / 'schemas/review_response.schema.json'):
            errors.append(f'response.instance.json: {err}')
    if response_manifest_path.exists():
        for err in validate_json(response_manifest_path, contract_root / 'schemas/response.schema.json'):
            errors.append(f'response.manifest.json: {err}')
        manifest = json.loads(response_manifest_path.read_text(encoding='utf-8'))
        paths = {entry.get('path') for entry in manifest.get('bundle', {}).get('contents', []) if isinstance(entry, dict)}
        if 'IMPLEMENT/response.manifest.json' in paths or response_manifest_path.name in paths:
            errors.append('response manifest bundle must not include the response manifest itself')
        if manifest.get('request_ref') != 'PLAN/request.instance.json':
            errors.append('response.manifest.json request_ref must be PLAN/request.instance.json')
    if response_validation_path.exists():
        val = json.loads(response_validation_path.read_text(encoding='utf-8'))
        if not val.get('canonical_response_valid'):
            errors.append('response.validation.json reports canonical_response_valid=false')
        if not val.get('response_manifest_valid'):
            errors.append('response.validation.json reports response_manifest_valid=false')

    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        return 1
    print('PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
