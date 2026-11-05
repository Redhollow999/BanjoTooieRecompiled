"""Fail closed on obvious private payloads in a proposed public diff.

Screens additions, modifications, deletions and mode changes. Existing history, encoded payloads, rights and
manual provenance need separate review. Never prints detected secret values.
"""
import argparse
import re
import subprocess
from pathlib import Path, PurePosixPath

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
    if any(p.lower() in {'private', 'research', 'checkpoints', 'candidates'} for p in name.parts):
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



# Changing a gate must never be reported as ordinary content approval. Ownership
# is also enforced through CODEOWNERS plus required repository review settings.
PROTECTED = {
    '.github/CODEOWNERS', '.gitignore', '.gitattributes',
    'tools/validate_public_additions.py', 'tools/alpha_preflight.py',
    'tools/test_alpha_preparation.py', 'docs/alpha/PUBLICATION_REVIEW.md',
}


def protected(path):
    path = path.casefold()
    return path.startswith('.github/workflows/') or path in {
        p.casefold() for p in PROTECTED
    }


def git(root, *arguments):
    return subprocess.check_output(['git', *arguments], cwd=root)


def changes(root, base, head=None):
    arguments = ['diff', '--raw', '--no-abbrev', '--no-renames',
                 '--no-ext-diff', '--no-textconv', '-z', base]
    if head is not None:
        arguments.append(head)
    fields = git(root, *arguments, '--').split(b'\0')
    result = []
    for i in range(0, len(fields) - 1, 2):
        metadata, path = fields[i], fields[i+1].decode('utf8')
        old_mode, new_mode, old_oid, new_oid, status = metadata.split()
        result.append({'path': path, 'status': status.decode(),
                       'old_mode': old_mode[1:].decode(),
                       'new_mode': new_mode.decode()})
    if head is None:
        known = {r['path'] for r in result}
        for path in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0'):
            if path and path.decode('utf8') not in known:
                result.append({'path': path.decode('utf8'), 'status': 'A',
                               'old_mode': '000000', 'new_mode': '100644'})
    return result


def validate(root, baseline, head=None):
    root = root.resolve()
    # A full immutable SHA is required. A caller cannot accidentally pass HEAD as
    # the approved baseline, and refs changing during a run cannot change scope.
    if not re.fullmatch(r'[0-9a-fA-F]{40}', baseline):
        raise ValueError('Approved baseline must be a full 40-character commit SHA.')
    base = git(root, 'rev-parse', '--verify', baseline+'^{commit}').decode().strip()
    target = git(root, 'rev-parse', '--verify', (head or 'HEAD')+'^{commit}').decode().strip()
    ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', base, target], cwd=root)
    if ancestor.returncode:
        raise ValueError('Approved baseline must be an ancestor of the reviewed commit.')
    records = changes(root, base, target if head is not None else None)
    if not records:
        raise ValueError('Zero files screened: choose an earlier approved baseline; empty diffs are not approval.')
    failures, review, deleted = [], [], []
    screened = 0
    for record in records:
        path, status = record['path'], record['status']
        parts = PurePosixPath(path)
        if parts.is_absolute() or '..' in parts.parts or '\\' in path:
            failures.append((path, ['unsafe Git path']))
            continue
        if protected(path):
            review.append((path, 'publication control changed ('+status+')'))
        if status == 'D':
            deleted.append(path)
            continue  # No payload to scan; protected deletions still need review.
        if status not in {'A', 'M', 'T'}:
            failures.append((path, ['unresolved or unsupported change status '+status]))
            continue
        if record['new_mode'] not in {'100644', '100755'}:
            failures.append((path, ['non-regular file mode '+record['new_mode']]))
            continue  # Never follow a symlink or silently accept a gitlink.
        if record['old_mode'] not in {'000000', record['new_mode']}:
            review.append((path, 'file mode changed '+record['old_mode']+' -> '+record['new_mode']))
        if head is not None:
            data = git(root, 'show', target+':'+path)
        else:
            source = root/path
            resolved = source.resolve()
            if source.is_symlink() or not resolved.is_relative_to(root) or not resolved.is_file():
                failures.append((path, ['unsafe or unavailable regular file']))
                continue
            data = resolved.read_bytes()
        screened += 1
        found = issues(path, data)
        if found:
            failures.append((path, found))
    return {'baseline': base, 'target': target, 'changes': len(records),
            'screened': screened, 'deleted': deleted, 'failures': failures,
            'review_required': review}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, help='approved immutable commit SHA')
    parser.add_argument('--head', help='committed target, e.g. HEAD; otherwise include working changes')
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        result = validate(root, args.base, args.head)
    except (ValueError, subprocess.CalledProcessError, OSError, UnicodeError) as error:
        print('Validation failed: '+str(error))
        return 1
    for path, found in result['failures']:
        print(path+': '+'; '.join(found))
    for path in result['deleted']:
        print('Deleted (no payload): '+path)
    for path, reason in result['review_required']:
        print('MAINTAINER REVIEW REQUIRED: '+path+': '+reason)
    print(f"{result['changes']} changes reviewed; {result['screened']} file contents screened; "
          f"{len(result['deleted'])} deletions; {len(result['failures'])} blocked; "
          f"{len(result['review_required'])} control/mode reviews required.")
    if result['failures']:
        return 1
    if result['review_required']:
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
