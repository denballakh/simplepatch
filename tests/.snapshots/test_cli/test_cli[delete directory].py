{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='\n'
          '!dir/file ->\n'
          '!dir/ ->\n',
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
    'exit_code': 0,
    'stdout': 'Applied test.patch to .\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'test.patch': File(
          content='\n'
            '!dir/file ->\n'
            '!dir/ ->\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}