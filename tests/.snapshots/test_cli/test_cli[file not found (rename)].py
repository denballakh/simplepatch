{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!old.py -> new.py\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: old.py\n',
    'final_fs': Dir(
      children={
        'test.patch': File(
          content='!old.py -> new.py\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}