{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!oldfile ->\n',
        permissions=420,
      ),
      'oldfile': File(
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
        'test.patch': File(
          content='!oldfile ->\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}