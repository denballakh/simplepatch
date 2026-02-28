{
  'args': [
    'convert',
    '--to=simplepatch',
    'input.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'input.patch': File(
        content='diff --git a/file.txt b/file.txt\n'
          'index abc1234..def5678 100644\n'
          '--- a/file.txt\n'
          '+++ b/file.txt\n'
          '@@ -1,3 +1,3 @@\n'
          ' line 1\n'
          '-old line\n'
          '+new line\n'
          ' line 3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': '!file.txt @1\n'
      '=line 1\n'
      '-old line\n'
      '+new line\n'
      '=line 3\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='diff --git a/file.txt b/file.txt\n'
            'index abc1234..def5678 100644\n'
            '--- a/file.txt\n'
            '+++ b/file.txt\n'
            '@@ -1,3 +1,3 @@\n'
            ' line 1\n'
            '-old line\n'
            '+new line\n'
            ' line 3\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}