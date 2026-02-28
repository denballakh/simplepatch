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
        content='diff --git a/oldname.txt b/newname.txt\n'
          'similarity index 100%\n'
          'rename from oldname.txt\n'
          'rename to newname.txt\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': '!oldname.txt -> newname.txt\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='diff --git a/oldname.txt b/newname.txt\n'
            'similarity index 100%\n'
            'rename from oldname.txt\n'
            'rename to newname.txt\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}