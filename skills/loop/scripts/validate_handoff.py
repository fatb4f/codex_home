#!/usr/bin/env python3
"""Validate loop handoff/workflow/init/terminate asset shapes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f'file not found: {path}')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise SystemExit(f'invalid JSON object in {path}')
    return data


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--contract', default='assets/handoff.contract.json')
    p.add_argument('--workflow', default='assets/workflow.json')
    p.add_argument('--init', default='assets/init.asset.json')
    p.add_argument('--terminate', default='assets/terminate.asset.json')
    args = p.parse_args()
    base = Path(__file__).resolve().parent.parent
    contract = _load_json(base / args.contract)
    workflow = _load_json(base / args.workflow)
    init = _load_json(base / args.init)
    term = _load_json(base / args.terminate)
    errors = []
    for key in ('version', 'id', 'required_fields', 'boundary_contracts'):
        if key not in contract:
            errors.append(f'contract missing top-level key: {key}')
    node_ids = {n.get('id') for n in workflow.get('nodes', []) if isinstance(n, dict)}
    for node_id in ('N0_initialize', 'N1_plan', 'N3_implement', 'N4_verify', 'N5_terminate'):
        if node_id not in node_ids:
            errors.append(f'workflow missing required node: {node_id}')
    for key in ('outputs', 'gates', 'rollback'):
        if key not in init:
            errors.append(f'init asset missing top-level key: {key}')
    for key in ('outputs', 'rollback'):
        if key not in term:
            errors.append(f'terminate asset missing top-level key: {key}')
    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        return 1
    print('PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
