from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

MIN_TOTAL_BYTES = 200_000  # rough guardrail

def main() -> int:
    files = [p for p in ROOT.rglob('*') if p.is_file()]
    if not files:
        print('ERROR: no files found')
        return 2

    empty = [p for p in files if p.stat().st_size == 0]
    if empty:
        print('ERROR: empty files detected:')
        for p in empty[:50]:
            print(' -', p.relative_to(ROOT))
        print(f'Total empty files: {len(empty)}')
        return 3

    total = sum(p.stat().st_size for p in files)
    if total < MIN_TOTAL_BYTES:
        print(f'ERROR: total size too small ({total} bytes); expected >= {MIN_TOTAL_BYTES}')
        return 4

    print(f'OK: {len(files)} files, {total} bytes, no empty files')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
