{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!dir/ ->\n',
        permissions=420,
      ),
      'dir': Dir(
        children={
          'file': File(
            content='content\n',
            permissions=420,
          ),
        },
        permissions=493,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': "Error: [Errno 39] Directory not empty: 'dir'\n",
    'final_fs': Dir(
      children={
        'dir': Dir(
          children={
            'file': File(
              content='content\n',
              permissions=420,
            ),
          },
          permissions=493,
        ),
        'test.patch': File(
          content='!dir/ ->\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}