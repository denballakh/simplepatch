{
  'args': [
    'apply',
    'p2.patch',
    'p1.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'p1.patch': File(
        content='!file\n'
          '-a\n'
          '+b\n',
        permissions=420,
      ),
      'p2.patch': File(
        content='!file\n'
          '-b\n'
          '+c\n',
        permissions=420,
      ),
      'file': File(
        content='a\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: Could not find match in file\n'
      "Looking for: ['b\\n']\n",
    'final_fs': Dir(
      children={
        'file': File(
          content='a\n',
          permissions=420,
        ),
        'p1.patch': File(
          content='!file\n'
            '-a\n'
            '+b\n',
          permissions=420,
        ),
        'p2.patch': File(
          content='!file\n'
            '-b\n'
            '+c\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}