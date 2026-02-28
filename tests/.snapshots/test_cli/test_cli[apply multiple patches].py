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
        content='!file1\n'
          '-old1\n'
          '+new1\n',
        permissions=420,
      ),
      'p2.patch': File(
        content='!file2\n'
          '-old2\n'
          '+new2\n',
        permissions=420,
      ),
      'file1': File(
        content='old1\n',
        permissions=420,
      ),
      'file2': File(
        content='old2\n',
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
        'file1': File(
          content='new1\n',
          permissions=420,
        ),
        'file2': File(
          content='new2\n',
          permissions=420,
        ),
        'p1.patch': File(
          content='!file1\n'
            '-old1\n'
            '+new1\n',
          permissions=420,
        ),
        'p2.patch': File(
          content='!file2\n'
            '-old2\n'
            '+new2\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}