{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!-> newfile\n'
          '+content\n',
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
        'newfile': File(
          content='content\n',
          permissions=420,
        ),
        'test.patch': File(
          content='!-> newfile\n'
            '+content\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}