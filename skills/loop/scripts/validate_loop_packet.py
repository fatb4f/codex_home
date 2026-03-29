#!/usr/bin/env python3
"""Validate loop packet section contract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQ = ['init', 'loop_context', 'phase_state', 'handoff', 'transition_gate', 'verification', 'terminate', 'rollback_path']
HEADING_RE = re.compile(r'^##\s+([A-Za-z0-9_ -]+)\s*$')


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('path', nargs='?', default='LOOP.md')
    args = p.parse_args()
    path = Path(args.path).expanduser()
    if not path.exists():
        raise SystemExit(f'file not found: {path}')
    lines = path.read_text(encoding='utf-8').splitlines()
    found = {m.group(1).strip() for ln in lines if (m := HEADING_RE.match(ln.strip()))}
    miss = [s for s in REQ if s not in found]
    if miss:
        print('FAIL')
        for m in miss:
            print(f'- missing section: ## {m}')
        return 1
    print('PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
