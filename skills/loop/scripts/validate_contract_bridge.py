#!/usr/bin/env python3
"""Validate the request/response bridge against the shared contract layer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f'file not found: {path}')
    return json.loads(path.read_text(encoding='utf-8'))


def resolve(base: Path, ref: str) -> Path:
    p = Path(ref)
    return p if p.is_absolute() else (base / ref).resolve()


def validate_schema(instance_path: Path, schema_path: Path) -> list[str]:
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    resolver = jsonschema.validators.RefResolver(base_uri=schema_path.resolve().as_uri(), referrer=schema)
    validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    return [e.message for e in validator.iter_errors(instance)]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--wt', required=True)
    p.add_argument('--contract-root', required=True)
    args = p.parse_args()

    wt = Path(args.wt).expanduser().resolve()
    contract_root = Path(args.contract_root).expanduser().resolve()
    plan_dir = wt / 'PLAN'
    impl_dir = wt / 'IMPLEMENT'

    bindings_path = plan_dir / 'contract.bindings.json'
    request_path = plan_dir / 'request.instance.json'
    request_validation_path = plan_dir / 'request.validation.json'
    batch_manifest_path = plan_dir / 'batch.manifest.json'
    gate_plan_path = plan_dir / 'integration_gate.plan.json'
    promotion_plan_path = plan_dir / 'promotion.plan.json'
    response_instance_path = impl_dir / 'response.instance.json'
    response_manifest_path = impl_dir / 'response.manifest.json'
    response_validation_path = impl_dir / 'response.validation.json'

    errors = []
    for req in [bindings_path, request_path, request_validation_path, batch_manifest_path, gate_plan_path, promotion_plan_path, response_instance_path, response_manifest_path, response_validation_path]:
        if not req.exists():
            errors.append(f'missing artifact: {req}')
    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        return 1

    bindings = load_json(bindings_path)
    bindings_schema = load_json(contract_root / 'schemas/contract_bindings.schema.json')
    jsonschema.Draft202012Validator(bindings_schema).validate(bindings)

    checks = [
        (request_path, resolve(contract_root, bindings['request_schema_ref']), 'request.instance.json'),
        (batch_manifest_path, resolve(contract_root, bindings['batch_manifest_schema_ref']), 'batch.manifest.json'),
        (gate_plan_path, resolve(contract_root, bindings['integration_gate_plan_schema_ref']), 'integration_gate.plan.json'),
        (promotion_plan_path, resolve(contract_root, bindings['promotion_plan_schema_ref']), 'promotion.plan.json'),
        (response_instance_path, resolve(contract_root, bindings['review_response_schema_ref']), 'response.instance.json'),
        (response_manifest_path, resolve(contract_root, bindings['response_schema_ref']), 'response.manifest.json'),
    ]
    for inst, schema, label in checks:
        for msg in validate_schema(inst, schema):
            errors.append(f'{label}: {msg}')

    request_validation = load_json(request_validation_path)
    response_validation = load_json(response_validation_path)
    if not request_validation.get('valid'):
        errors.append('request.validation.json reports valid=false')
    if not response_validation.get('canonical_response_valid'):
        errors.append('response.validation.json reports canonical_response_valid=false')
    if not response_validation.get('response_manifest_valid'):
        errors.append('response.validation.json reports response_manifest_valid=false')

    response_manifest = load_json(response_manifest_path)
    content_paths = {entry.get('path') for entry in response_manifest.get('bundle', {}).get('contents', []) if isinstance(entry, dict)}
    if 'IMPLEMENT/response.manifest.json' in content_paths or response_manifest_path.name in content_paths:
        errors.append('response manifest bundle must not include the response manifest itself')
    if response_manifest.get('request_ref') != 'PLAN/request.instance.json':
        errors.append('response.manifest.json request_ref must be PLAN/request.instance.json')

    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        return 1
    print('PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
