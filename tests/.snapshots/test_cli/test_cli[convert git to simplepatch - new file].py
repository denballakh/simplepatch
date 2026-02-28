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
        content='diff --git a/newfile.txt b/newfile.txt\n'
          'new file mode 100644\n'
          'index 0000000..abc1234\n'
          '--- /dev/null\n'
          '+++ b/newfile.txt\n'
          '@@ -0,0 +1,3 @@\n'
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
    'stdout': '!-> newfile.txt\n'
      '+line 1\n'
      '+line 2\n'
      '+line 3\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='diff --git a/newfile.txt b/newfile.txt\n'
            'new file mode 100644\n'
            'index 0000000..abc1234\n'
            '--- /dev/null\n'
            '+++ b/newfile.txt\n'
            '@@ -0,0 +1,3 @@\n'
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