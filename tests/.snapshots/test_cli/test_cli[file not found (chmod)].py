{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!missing.py %644->755\n',
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
          content='!missing.py %644->755\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}