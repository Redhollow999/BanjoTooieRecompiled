"""Read-only verification of the captured project inputs; never generates assets."""
import argparse
import hashlib
import json
from pathlib import Path


def verify(root, records):
    root = root.resolve()
    failures = []
    for record in records:
        relative = Path(record['path'])
        target = (root / relative).resolve()
        if relative.is_absolute() or not target.is_relative_to(root):
            failures.append((record['path'], 'unsafe path'))
        elif not target.is_file():
            failures.append((record['path'], 'missing'))
        elif hashlib.sha256(target.read_bytes()).hexdigest() != record['sha256']:
            failures.append((record['path'], 'hash differs'))
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest', type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source', action='store_true')
    group.add_argument('--resources', action='store_true')
    args = parser.parse_args()
    manifest = args.manifest or args.root / 'docs/alpha/verified-build.json'
    records = json.loads(manifest.read_text())['source' if args.source else 'resources']
    if not records:
        raise SystemExit('Empty manifest is not a successful verification.')
    failures = verify(args.root, records)
    for path, reason in failures:
        print(f'{reason}: {path}')
    print(f'{len(records)} inputs checked; {len(failures)} failures. '
          'Hash matching does not establish rights or playable correctness.')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
