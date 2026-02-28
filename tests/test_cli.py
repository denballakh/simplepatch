"""Tests for the SimplePatch CLI."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from .fsutils import File, Dir, read_fs, write_fs
from .snapshots import Snapshotter


def run_cli(
    args: list[str],
    stdin: str | None = None,
    cwd: Path | None = None,
) -> tuple[int, str, str]:
    """Run the simplepatch CLI and return (exit_code, stdout, stderr)."""
    # Get the project root directory (parent of tests directory)
    project_root = Path(__file__).parent.parent

    cmd = [
        sys.executable,
        '-m',
        'simplepatch',
        *args,
    ]

    # Set PYTHONPATH to include the project root
    env = dict(os.environ)
    env_pythonpath = str(project_root)
    if 'PYTHONPATH' in env:
        env_pythonpath = f'{env_pythonpath}:{env["PYTHONPATH"]}'
    env['PYTHONPATH'] = env_pythonpath

    result = subprocess.run(
        cmd,
        input=stdin,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )

    return result.returncode, result.stdout, result.stderr


def case(
    name: str = '',
    /,
    *,
    args: list[str],
    stdin: str | None = None,
    fs: Dir = Dir({}),
) -> tuple[str, list[str], str | None, Dir]:
    if not name:
        name = ' '.join(args)
    return name, args, stdin, fs


CLI_TEST_CASES = [
    # Help and version
    case(args=[]),
    case(args=['-h']),
    case(args=['--help']),
    case(args=['-V']),
    case(args=['--version']),
    case(args=['diff']),
    case(args=['diff', '-h']),
    case(args=['diff', '--help']),
    case(args=['convert']),
    case(args=['convert', '-h']),
    case(args=['convert', '--help']),
    # Apply command - basic
    case(args=['apply']),
    case(args=['apply', '-h']),
    case(args=['apply', '--help']),
    case(
        'apply basic',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!file\n-old line\n+new line\n'),
                'file': File('old line\n'),
            }
        ),
    ),
    case(
        'apply stdin',
        args=['apply', '-'],
        stdin='!file\n-old line\n+new line\n',
        fs=Dir(
            {
                'file': File('old line\n'),
            }
        ),
    ),
    case(
        'apply multiple patches',
        args=['apply', 'p1.patch', 'p2.patch'],
        fs=Dir(
            {
                'p1.patch': File('!file1\n-old1\n+new1\n'),
                'p2.patch': File('!file2\n-old2\n+new2\n'),
                'file1': File('old1\n'),
                'file2': File('old2\n'),
            }
        ),
    ),
    case(
        'apply chained patches',
        args=['apply', 'p1.patch', 'p2.patch'],
        fs=Dir(
            {
                'p1.patch': File('!file\n-a\n+b\n'),
                'p2.patch': File('!file\n-b\n+c\n'),
                'file': File('a\n'),
            }
        ),
    ),
    case(
        'apply chained patches reverse order',
        args=['apply', 'p2.patch', 'p1.patch'],
        fs=Dir(
            {
                'p1.patch': File('!file\n-a\n+b\n'),
                'p2.patch': File('!file\n-b\n+c\n'),
                'file': File('a\n'),
            }
        ),
    ),
    case(
        'apply with subdir',
        args=['apply', 'test.patch', 'subdir'],
        fs=Dir(
            {
                'test.patch': File('!file\n-old\n+new\n'),
                'subdir': Dir(
                    {
                        'file': File('old\n'),
                    }
                ),
            }
        ),
    ),
    case(
        'apply missing patch file',
        args=['apply', 'missing.patch'],
        fs=Dir({}),
    ),
    # Apply command - file operations
    case(
        'create file',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!-> newfile\n+content\n'),
            }
        ),
    ),
    case(
        'delete file',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!oldfile ->\n'),
                'oldfile': File('content\n'),
            }
        ),
    ),
    case(
        'rename file',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!old -> new\n'),
                'old': File('content\n'),
            }
        ),
    ),
    # Error cases
    case(
        'edit missing file',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!missing\n-old\n+new\n'),
            }
        ),
    ),
    case(
        'ambiguous match',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!file\n-x = 1\n+x = 10\n'),
                'file': File('x = 1\ny = 2\nx = 1\nz = 3\n'),
            }
        ),
    ),
    # Create directory
    case(
        'create directory and file',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!-> dir/\n!-> dir/file\n+content\n'),
            }
        ),
    ),
    # Delete directory
    case(
        'delete directory',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!dir/file ->\n!dir/ ->\n'),
                'dir': Dir(
                    {
                        'file': File('content\n'),
                    }
                ),
            }
        ),
    ),
    # Rename file
    case(
        'rename file with comment',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('# Reorganize project structure\n!old -> new\n'),
                'old': File('content\n'),
            }
        ),
    ),
    # Change permissions
    case(
        'change permissions',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!file.sh %644->755\n'),
                'file.sh': File(b'#!/bin/bash\necho "Hello"\n', permissions=0o644),
            }
        ),
    ),
    # Rename directory
    case(
        'rename directory',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!olddir/ -> newdir/\n'),
                'olddir': Dir(
                    {
                        'file': File('content\n'),
                    }
                ),
            }
        ),
    ),
    # UTF-8 content
    case(
        'utf-8 content',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!file\n-Hello 世界\n+Goodbye 世界\n'),
                'file': File('Hello 世界\nПривет мир\n'),
            }
        ),
    ),
    # Line hint disambiguation - first occurrence
    case(
        'line hint disambiguation',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!file @1\n-x = 1\n+x = 10\n'),
                'file': File('x = 1\ny = 2\nx = 1\nz = 3\n'),
            }
        ),
    ),
    # Chmod with informational old perms
    case(
        'chmod with old perms info',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('\n!file %755->600\n'),
                'file': File(b'content', permissions=0o644),
            }
        ),
    ),
    # Error cases from test_apply_patch_errors
    # File not found (edit)
    case(
        'file not found (edit)',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!missing.py\n-old\n+new\n'),
            }
        ),
    ),
    # File not found (delete)
    case(
        'file not found (delete)',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!missing.py ->\n'),
            }
        ),
    ),
    # File not found (chmod)
    case(
        'file not found (chmod)',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!missing.py %644->755\n'),
            }
        ),
    ),
    # File not found (rename source)
    case(
        'file not found (rename)',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!old.py -> new.py\n'),
            }
        ),
    ),
    # File already exists (create)
    case(
        'file already exists (create)',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!-> existing.py\n+new content\n'),
                'existing.py': File('content\n'),
            }
        ),
    ),
    # File already exists (rename target)
    case(
        'file already exists (rename)',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!old.py -> new.py\n'),
                'old.py': File('old\n'),
                'new.py': File('new\n'),
            }
        ),
    ),
    # Delete non-empty directory fails
    case(
        'delete non-empty directory',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!dir/ ->\n'),
                'dir': Dir(
                    {
                        'file': File('content\n'),
                    }
                ),
            }
        ),
    ),
    # Ambiguous match error
    case(
        'ambiguous match',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!file\n-x = 1\n+x = 10\n'),
                'file': File('x = 1\ny = 2\nx = 1\nz = 3\n'),
            }
        ),
    ),
    # No match found error
    case(
        'no match found',
        args=['apply', 'test.patch'],
        fs=Dir(
            {
                'test.patch': File('!file\n-nonexistent line\n+new line\n'),
                'file': File('line1\nline2\nline3\n'),
            }
        ),
    ),
    # Convert command tests
    case(
        'convert git to simplepatch - simple edit',
        args=['convert', '--from=git', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File(
                    'diff --git a/file.txt b/file.txt\n'
                    'index abc1234..def5678 100644\n'
                    '--- a/file.txt\n'
                    '+++ b/file.txt\n'
                    '@@ -1,3 +1,3 @@\n'
                    ' line 1\n'
                    '-old line\n'
                    '+new line\n'
                    ' line 3\n'
                ),
            }
        ),
    ),
    case(
        'convert git to simplepatch - new file',
        args=['convert', '--from=git', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File(
                    'diff --git a/newfile.txt b/newfile.txt\n'
                    'new file mode 100644\n'
                    'index 0000000..abc1234\n'
                    '--- /dev/null\n'
                    '+++ b/newfile.txt\n'
                    '@@ -0,0 +1,3 @@\n'
                    '+line 1\n'
                    '+line 2\n'
                    '+line 3\n'
                ),
            }
        ),
    ),
    case(
        'convert git to simplepatch - delete file',
        args=['convert', '--from=git', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File(
                    'diff --git a/deleted.txt b/deleted.txt\n'
                    'deleted file mode 100644\n'
                    'index abc1234..0000000\n'
                    '--- a/deleted.txt\n'
                    '+++ /dev/null\n'
                    '@@ -1,3 +0,0 @@\n'
                    '-line 1\n'
                    '-line 2\n'
                    '-line 3\n'
                ),
            }
        ),
    ),
    case(
        'convert git to simplepatch - rename file',
        args=['convert', '--from=git', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File(
                    'diff --git a/oldname.txt b/newname.txt\n'
                    'similarity index 100%\n'
                    'rename from oldname.txt\n'
                    'rename to newname.txt\n'
                ),
            }
        ),
    ),
    case(
        'convert git to simplepatch - mode change',
        args=['convert', '--from=git', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File(
                    'diff --git a/script.sh b/script.sh\n'
                    'old mode 100644\n'
                    'new mode 100755\n'
                    'index abc1234..abc1234\n'
                    '--- a/script.sh\n'
                    '+++ b/script.sh\n'
                    '@@ -1 +1 @@\n'
                    '-echo "not executable"\n'
                    '+echo "now executable"\n'
                ),
            }
        ),
    ),
    case(
        'convert git to simplepatch - stdin',
        args=['convert', '--from=git', '--to=simplepatch'],
        stdin=(
            'diff --git a/file.txt b/file.txt\n'
            'index abc1234..def5678 100644\n'
            '--- a/file.txt\n'
            '+++ b/file.txt\n'
            '@@ -1,3 +1,3 @@\n'
            ' line 1\n'
            '-old line\n'
            '+new line\n'
            ' line 3\n'
        ),
        fs=Dir({}),
    ),
    case(
        'convert simplepatch to git - simple edit',
        args=['convert', '--from=simplepatch', '--to=git', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!file.txt @1\n=line 1\n-old line\n+new line\n=line 3\n'),
            }
        ),
    ),
    case(
        'convert simplepatch to git - new file',
        args=['convert', '--from=simplepatch', '--to=git', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!-> newfile.txt\n+line 1\n+line 2\n+line 3\n'),
            }
        ),
    ),
    case(
        'convert simplepatch to git - delete file',
        args=['convert', '--from=simplepatch', '--to=git', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!deleted.txt ->\n'),
            }
        ),
    ),
    case(
        'convert simplepatch to git - rename file',
        args=['convert', '--from=simplepatch', '--to=git', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!oldname.txt -> newname.txt\n'),
            }
        ),
    ),
    case(
        'convert simplepatch to git - chmod',
        args=['convert', '--from=simplepatch', '--to=git', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!script.sh %644->755\n'),
            }
        ),
    ),
    case(
        'convert auto-detect git format',
        args=['convert', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File(
                    'diff --git a/file.txt b/file.txt\n'
                    'index abc1234..def5678 100644\n'
                    '--- a/file.txt\n'
                    '+++ b/file.txt\n'
                    '@@ -1,3 +1,3 @@\n'
                    ' line 1\n'
                    '-old line\n'
                    '+new line\n'
                    ' line 3\n'
                ),
            }
        ),
    ),
    case(
        'convert auto-detect simplepatch format',
        args=['convert', '--to=git', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!file.txt @1\n=line 1\n-old line\n+new line\n=line 3\n'),
            }
        ),
    ),
    case(
        'convert same format passthrough',
        args=['convert', '--from=simplepatch', '--to=simplepatch', 'input.patch'],
        fs=Dir(
            {
                'input.patch': File('!file.txt\n-old\n+new\n'),
            }
        ),
    ),
    case(
        'convert missing input file',
        args=['convert', '--from=git', '--to=simplepatch', 'missing.patch'],
        fs=Dir({}),
    ),
]


@pytest.mark.parametrize(
    ['args', 'stdin', 'fs'],
    [case[1:] for case in CLI_TEST_CASES],
    ids=[case[0] for case in CLI_TEST_CASES],
)
def test_cli(
    args: list[str],
    stdin: str | None,
    fs: Dir,
    tmp_path: Path,
    snapshot: Snapshotter,
) -> None:
    write_fs(tmp_path, fs)

    exit_code, stdout, stderr = run_cli(args, stdin=stdin, cwd=tmp_path)

    final_fs = read_fs(tmp_path)

    result = {
        'exit_code': exit_code,
        'stdout': stdout,
        'stderr': stderr,
        'final_fs': final_fs,
    }

    snapshot(result)
