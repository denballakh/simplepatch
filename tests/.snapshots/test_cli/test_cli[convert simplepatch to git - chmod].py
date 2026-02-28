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
        content='!script.sh %644->755\n',
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
      'diff --git a/script.sh b/script.sh\n'
      'old mode 100644\n'
      'new mode 100755\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='!script.sh %644->755\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}