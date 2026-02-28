{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!missing.py\n'
          '-old\n'
          '+new\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: missing.py\n',
    'final_fs': Dir(
      children={
        'test.patch': File(
          content='!missing.py\n'
            '-old\n'
            '+new\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}