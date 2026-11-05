"""Fail closed on obvious private payloads in a proposed public diff.

Screens changed/new files only. Existing history, encoded payloads, rights and
manual provenance need separate review. Never prints detected secret values.
"""
import argparse
import re
import subprocess
from pathlib import Path

FORBIDDEN = {'.z64', '.n64', '.v64', '.rom', '.bin', '.zip', '.7z', '.dls',
             '.sf2', '.mid', '.midi', '.wav', '.flac', '.ogg', '.mp4', '.exe',
             '.dll', '.obj', '.pdb', '.dmp', '.eep', '.sra', '.fla', '.sav',
             '.png', '.jpg', '.jpeg', '.ico', '.ttf', '.glb', '.gltf', '.mode'}
SECRETS = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}'
                     rb'|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'
                     rb'|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
ARRAYS = re.compile(rb'(?:unsigned\s+char|uint8_t|u8|char|uint16_t|uint32_t)\s+'
                    rb'\w+\s*\[[^;=]*?\]\s*=\s*\{([^}]+)\}', re.S)


def issues(path, data):
    found = []
    name = Path(path)
    if name.suffix.lower() in FORBIDDEN:
        found.append('payload/binary extension requires private generation or rights review')
    if any(p.lower() in {'private', 'checkpoints', 'candidates'} for p in name.parts):
        found.append('private development directory')
    if name.name.startswith('.env') and name.name != '.env.example':
        found.append('environment file')
    if data[:4] in (b'\x80\x37\x12\x40', b'\x37\x80\x40\x12', b'\x40\x12\x37\x80'):
        found.append('ROM signature')
    if b'\0' in data or data.startswith(b'MZ'):
        found.append('binary content')
    if SECRETS.search(data):
        found.append('possible secret; value withheld')
    if re.search(rb'[A-Za-z]:[\\/]Users[\\/]|' + rb'/' + rb'home/[^\s/]+/', data):
        found.append('personal absolute path')
    for array in ARRAYS.findall(data):
        if len(re.findall(rb'\b(?:0x[\da-fA-F]+|\d+)\b', array)) > 256:
            found.append('large numeric payload array requires provenance review')
            break
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, help='reviewed base commit/ref')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    def git(*arguments):
        return subprocess.check_output(['git', *arguments], cwd=root)
    base = git('rev-parse', '--verify', args.base + '^{commit}').decode().strip()
    changed = git('diff', '--name-only', '--diff-filter=ACMR', '-z', base).split(b'\0')
    untracked = git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0')
    paths = sorted({p.decode('utf8') for p in changed + untracked if p})
    failures = []
    for path in paths:
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            failures.append((path, ['unsafe or unavailable file']))
            continue
        # Reject tracked symlinks; resolving one must not import outside content.
        if (root / path).is_symlink():
            failures.append((path, ['symlink needs separate review']))
            continue
        found = issues(path, target.read_bytes())
        if found:
            failures.append((path, found))
    for path, found in failures:
        print(path + ': ' + '; '.join(found))
    print(f'{len(paths)} proposed files screened; {len(failures)} blocked. '
          'This is a publication boundary check, not rights approval.')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
