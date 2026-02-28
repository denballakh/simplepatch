{
  'args': [
    'apply',
    '-',
  ],
  'stdin': '!file\n'
    '-old line\n'
    '+new line\n',
  'fs': Dir(
    children={
      'file': File(
        content='old line\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'Applied - to .\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'file': File(
          content='new line\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}