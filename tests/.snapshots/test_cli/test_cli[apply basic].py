{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!file\n'
          '-old line\n'
          '+new line\n',
        permissions=420,
      ),
      'file': File(
        content='old line\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'Applied test.patch to .\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'file': File(
          content='new line\n',
          permissions=420,
        ),
        'test.patch': File(
          content='!file\n'
            '-old line\n'
            '+new line\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}