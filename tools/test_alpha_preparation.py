"""Positive and negative controls without ROMs, game assets or network access."""
import hashlib
import tempfile
import subprocess
import unittest
import re
import sys
from pathlib import Path
from alpha_preflight import verify
from validate_public_additions import issues, validate, protected


class GitPublicationTests(unittest.TestCase):
    """Real Git trees exercise forced adds, deletions, renames and file modes."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Publication fixture')
        self.git('config', 'user.email', 'fixture@invalid.local')
        self.git('config', 'core.autocrlf', 'false')
        for path in ['notes.md', '.github/workflows/check.yml',
                     'tools/validate_public_additions.py', '.github/CODEOWNERS']:
            self.write(path, 'fixture\n')
        self.write('.gitignore', 'research/\n')
        self.git('add', '.')
        self.commit()
        self.base = self.git('rev-parse', 'HEAD').decode().strip()

    def git(self, *args, data=None):
        return subprocess.check_output(['git', *args], cwd=self.root, input=data,
                                       stderr=subprocess.PIPE)

    def write(self, path, text):
        target = self.root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self):
        self.git('commit', '-qm', 'fixture')

    def report(self):
        return validate(self.root, self.base, 'HEAD')

    def test_zero_files_screened_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Zero files screened'):
            self.report()

    def run_validator(self):
        # Execute the real CLI in the disposable repository. --head HEAD keeps
        # this copied runner out of the committed diff under examination.
        runner = self.root/'tools/validate_public_additions.py'
        runner.write_bytes((Path(__file__).parent/'validate_public_additions.py').read_bytes())
        return subprocess.run([sys.executable, str(runner), '--base', self.base,
                               '--head', 'HEAD'], cwd=self.root, capture_output=True, text=True)

    def test_zero_files_cli_does_not_report_success(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn('Zero files screened', result.stdout)

    def test_symbolic_baseline_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'full 40-character'):
            validate(self.root, 'HEAD', 'HEAD')

    def test_force_added_research_file_is_rejected(self):
        self.write('research/forced.txt', 'private research\n')
        self.git('add', '-f', 'research/forced.txt')
        self.commit()
        self.assertEqual(self.report()['failures'], [
            ('research/forced.txt', ['private development directory'])])

    def test_ordinary_addition_passes(self):
        self.write('contributor.md', 'original contribution\n')
        self.git('add', 'contributor.md'); self.commit()
        report = self.report()
        self.assertEqual(report['screened'], 1)
        self.assertFalse(report['failures'] or report['review_required'])

    def test_ordinary_deletion_is_reported(self):
        self.git('rm', 'notes.md'); self.commit()
        report = self.report()
        self.assertEqual(report['deleted'], ['notes.md'])
        self.assertEqual(report['changes'], 1)
        self.assertEqual(report['screened'], 0)
        self.assertFalse(report['failures'] or report['review_required'])

    def test_workflow_deletion_requires_review(self):
        self.git('rm', '.github/workflows/check.yml'); self.commit()
        report = self.report()
        self.assertEqual(report['review_required'][0][0], '.github/workflows/check.yml')
        self.assertEqual(report['deleted'], ['.github/workflows/check.yml'])

    def test_protected_change_cli_requires_review(self):
        self.git('rm', '.github/workflows/check.yml'); self.commit()
        result = self.run_validator()
        self.assertEqual(result.returncode, 2)
        self.assertIn('MAINTAINER REVIEW REQUIRED', result.stdout)

    def test_validator_deletion_requires_review(self):
        self.git('rm', 'tools/validate_public_additions.py'); self.commit()
        self.assertEqual(self.report()['review_required'][0][0], 'tools/validate_public_additions.py')

    def test_validator_edit_requires_review(self):
        self.write('tools/validate_public_additions.py', 'edited fixture\n')
        self.git('add', '.'); self.commit()
        self.assertTrue(self.report()['review_required'])

    def test_new_workflow_requires_review(self):
        self.write('.github/workflows/new.yml', 'name: fixture\n')
        self.git('add', '.github/workflows/new.yml'); self.commit()
        self.assertEqual(self.report()['review_required'][0][0], '.github/workflows/new.yml')

    def test_renamed_validator_still_requires_review(self):
        self.git('mv', 'tools/validate_public_additions.py', 'tools/ordinary.py')
        self.commit()
        report = self.report()
        self.assertIn('tools/validate_public_additions.py', report['deleted'])
        self.assertEqual(report['review_required'][0][0], 'tools/validate_public_additions.py')

    def test_codeowners_deletion_requires_review(self):
        self.git('rm', '.github/CODEOWNERS'); self.commit()
        self.assertTrue(self.report()['review_required'])

    def test_rename_into_research_is_rejected(self):
        content = (self.root/'notes.md').read_text()
        self.git('rm', 'notes.md')
        self.write('research/renamed.md', content)
        self.git('add', '-f', 'research/renamed.md'); self.commit()
        self.assertIn(b'R100', self.git('diff', '--name-status', '-M', self.base, 'HEAD'))
        report = self.report()
        self.assertEqual(report['deleted'], ['notes.md'])
        self.assertEqual(report['failures'][0][0], 'research/renamed.md')

    def test_symlink_type_change_is_rejected_without_following(self):
        blob = self.git('hash-object', '-w', '--stdin', data=b'outside-target').decode().strip()
        self.git('update-index', '--cacheinfo', '120000', blob, 'notes.md')
        self.commit()
        self.assertEqual(self.report()['failures'], [('notes.md', ['non-regular file mode 120000'])])

    def test_gitlink_addition_is_rejected(self):
        self.git('update-index', '--add', '--cacheinfo', '160000', self.base, 'fake-module')
        self.commit()
        self.assertEqual(self.report()['failures'][0][1], ['non-regular file mode 160000'])

    def test_executable_mode_change_requires_review(self):
        self.git('update-index', '--chmod=+x', 'notes.md'); self.commit()
        self.assertIn('100644 -> 100755', self.report()['review_required'][0][1])

    def test_unrelated_baseline_is_rejected(self):
        tree = self.git('write-tree').decode().strip()
        unrelated = self.git('commit-tree', tree, data=b'other root\n').decode().strip()
        with self.assertRaisesRegex(ValueError, 'ancestor'):
            validate(self.root, unrelated, 'HEAD')

    def test_dirty_worktree_is_screened(self):
        self.write('local.md', 'new original documentation\n')
        report = validate(self.root, self.base)
        self.assertEqual(report['screened'], 1)
        self.assertFalse(report['failures'])


class PreparationDocumentTests(unittest.TestCase):
    def test_archive_relative_links_resolve(self):
        root = Path(__file__).resolve().parents[1]
        archive = root/'docs/BASE_PORT_README.md'
        targets = re.findall(r'\]\(([^)]+)\)', archive.read_text())
        relative = [t.split('#', 1)[0] for t in targets
                    if not t.startswith(('https:', 'http:', '#'))]
        for target in relative:
            self.assertTrue((archive.parent/target).exists(), target)
        for target in ['../patches/', '../.github/workflows/build.yml', '../AGENTS.md', '../COPYING']:
            self.assertIn(target, relative)

    def test_manual_workflow_has_approved_baseline(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root/'.github/workflows/build.yml').read_text()
        self.assertIn('inputs.approved_baseline', workflow)
        self.assertIn('f017902a90252c276107ce177ccc12c75d297482', workflow)
        self.assertNotIn('|| github.sha', workflow)
        self.assertIn('--head HEAD', workflow)

    def test_protected_paths_have_owner_entries(self):
        root = Path(__file__).resolve().parents[1]
        owners = (root/'.github/CODEOWNERS').read_text()
        for path in ['.github/CODEOWNERS', 'tools/validate_public_additions.py',
                     'tools/alpha_preflight.py', 'tools/test_alpha_preparation.py',
                     'docs/alpha/PUBLICATION_REVIEW.md', '.gitignore', '.gitattributes']:
            self.assertTrue(protected(path))
            self.assertIn('/'+path+' @Redhollow999', owners)
        self.assertTrue(protected('.github/workflows/another.yml'))
        self.assertIn('/.github/workflows/ @Redhollow999', owners)


def main():
    assert not issues('src/example.c', b'int value = 1;\n')
    assert issues('data.bin', b'ordinary text')
    assert issues('renamed.txt', b'\x80\x37\x12\x40')
    assert issues('source.c', b'unsigned char wave[]={'+b','.join([b'1']*257)+b'};')
    assert issues('notes.txt', ('ghp_' + 'a'*36).encode())
    assert issues('notes.txt', b'MZsynthetic')
    assert issues('data.txt', b'zero\0byte')
    assert issues('checkpoints/notes.md', b'data')
    assert issues('.env', b'example')
    assert not issues('.env.example', b'EXAMPLE=replace-locally')
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        path = root/'source.txt'; path.write_bytes(b'control')
        records = [{'path': 'source.txt', 'sha256': hashlib.sha256(b'control').hexdigest()}]
        assert not verify(root, records)
        path.write_bytes(b'different'); assert verify(root, records)[0][1] == 'hash differs'
        path.unlink(); assert verify(root, records)[0][1] == 'missing'
        assert verify(root, [{'path': '../outside.txt', 'sha256': ''}])[0][1] == 'unsafe path'
    print('PASS 14 publication/preflight positive and negative controls')


if __name__ == '__main__':
    main()
    unittest.main()
