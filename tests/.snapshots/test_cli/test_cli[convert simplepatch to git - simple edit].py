{
  'args': [
    'convert',
    '--from=simplepatch',
    '--to=git',
    'input.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'input.patch': File(
        content='!file.txt @1\n'
          '=line 1\n'
          '-old line\n'
          '+new line\n'
          '=line 3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'From 0000000\n'
      'From: unknown author <noname@example.com>\n'
      'Date: Mon, 01 Jan 1970 00:00:00 +0000\n'
      'Subject: <subject>\n'
      'diff --git a/file.txt b/file.txt\n'
      'index 0000000..0000000 100644\n'
      '--- a/file.txt\n'
      '+++ b/file.txt\n'
      '@@ -1,3 +1,3 @@\n'
      ' line 1\n'
      '-old line\n'
      '+new line\n'
      ' line 3\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='!file.txt @1\n'
            '=line 1\n'
            '-old line\n'
            '+new line\n'
            '=line 3\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}