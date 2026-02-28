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
        content='!-> newfile.txt\n'
          '+line 1\n'
          '+line 2\n'
          '+line 3\n',
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
      'diff --git a/newfile.txt b/newfile.txt\n'
      'new file mode 100644\n'
      'index 0000000..0000000\n'
      '--- /dev/null\n'
      '+++ b/newfile.txt\n'
      '@@ -0,0 +1,3 @@\n'
      '+line 1\n'
      '+line 2\n'
      '+line 3\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='!-> newfile.txt\n'
            '+line 1\n'
            '+line 2\n'
            '+line 3\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}