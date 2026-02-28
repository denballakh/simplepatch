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
        content='!deleted.txt ->\n',
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
      'diff --git a/deleted.txt b/deleted.txt\n'
      'deleted file mode 100644\n'
      'index 0000000..0000000\n'
      '--- a/deleted.txt\n'
      '+++ /dev/null\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='!deleted.txt ->\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}