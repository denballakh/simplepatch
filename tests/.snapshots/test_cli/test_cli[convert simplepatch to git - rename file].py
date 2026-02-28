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
        content='!oldname.txt -> newname.txt\n',
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
      'diff --git a/oldname.txt b/newname.txt\n'
      'similarity index 100%\n'
      'rename from oldname.txt\n'
      'rename to newname.txt\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='!oldname.txt -> newname.txt\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}