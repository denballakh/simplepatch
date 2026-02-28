{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='# Reorganize project structure\n'
          '!old -> new\n',
        permissions=420,
      ),
      'old': File(
        content='content\n',
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
        'new': File(
          content='content\n',
          permissions=420,
        ),
        'test.patch': File(
          content='# Reorganize project structure\n'
            '!old -> new\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}