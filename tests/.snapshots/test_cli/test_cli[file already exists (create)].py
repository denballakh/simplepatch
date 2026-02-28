{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!-> existing.py\n'
          '+new content\n',
        permissions=420,
      ),
      'existing.py': File(
        content='content\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: existing.py\n',
    'final_fs': Dir(
      children={
        'existing.py': File(
          content='content\n',
          permissions=420,
        ),
        'test.patch': File(
          content='!-> existing.py\n'
            '+new content\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}