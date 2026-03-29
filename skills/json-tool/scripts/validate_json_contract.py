#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(schema_path: Path, data_path: Path) -> list[str]:
    schema = load_json(schema_path)
    data = load_json(data_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = '/'.join(str(p) for p in error.path) or '<root>'
        errors.append(f'{data_path}: {loc}: {error.message}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate JSON files against JSON Schema 2020-12 contracts.')
    parser.add_argument('schema', help='Schema path')
    parser.add_argument('files', nargs='+', help='One or more JSON files to validate')
    args = parser.parse_args()

    schema_path = Path(args.schema).expanduser().resolve()
    all_errors: list[str] = []
    for file_arg in args.files:
        all_errors.extend(validate(schema_path, Path(file_arg).expanduser().resolve()))

    if all_errors:
        print('FAIL')
        for err in all_errors:
            print(f'- {err}')
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
