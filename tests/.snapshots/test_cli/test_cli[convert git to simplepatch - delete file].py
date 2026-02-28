{
  'args': [
    'convert',
    '--from=git',
    '--to=simplepatch',
    'input.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'input.patch': File(
        content='diff --git a/deleted.txt b/deleted.txt\n'
          'deleted file mode 100644\n'
          'index abc1234..0000000\n'
          '--- a/deleted.txt\n'
          '+++ /dev/null\n'
          '@@ -1,3 +0,0 @@\n'
          '-line 1\n'
          '-line 2\n'
          '-line 3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': '!deleted.txt ->\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='diff --git a/deleted.txt b/deleted.txt\n'
            'deleted file mode 100644\n'
            'index abc1234..0000000\n'
            '--- a/deleted.txt\n'
            '+++ /dev/null\n'
            '@@ -1,3 +0,0 @@\n'
            '-line 1\n'
            '-line 2\n'
            '-line 3\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}