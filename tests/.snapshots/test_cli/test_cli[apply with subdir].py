{
  'args': [
    'apply',
    'test.patch',
    'subdir',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!file\n'
          '-old\n'
          '+new\n',
        permissions=420,
      ),
      'subdir': Dir(
        children={
          'file': File(
            content='old\n',
            permissions=420,
          ),
        },
        permissions=493,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'Applied test.patch to subdir\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'subdir': Dir(
          children={
            'file': File(
              content='new\n',
              permissions=420,
            ),
          },
          permissions=493,
        ),
        'test.patch': File(
          content='!file\n'
            '-old\n'
            '+new\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}