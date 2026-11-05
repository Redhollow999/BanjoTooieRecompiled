"""Positive and negative controls without ROMs, game assets or network access."""
import hashlib
import tempfile
from pathlib import Path
from alpha_preflight import verify
from validate_public_additions import issues


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
