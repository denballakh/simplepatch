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
      'old.py': File(
        content='old\n',
        permissions=420,
      ),
      'new.py': File(
        content='new\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: new.py\n',
    'final_fs': Dir(
      children={
        'new.py': File(
          content='new\n',
          permissions=420,
        ),
        'old.py': File(
          content='old\n',
          permissions=420,
        ),
        'test.patch': File(
          content='!old.py -> new.py\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}