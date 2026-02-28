{
  'args': [
    'apply',
    'p1.patch',
    'p2.patch',
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
    'exit_code': 0,
    'stdout': 'Applied p1.patch to .\n'
      'Applied p2.patch to .\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'file': File(
          content='c\n',
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