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
          '!file %755->600\n',
        permissions=420,
      ),
      'file': File(
        content=b'content',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: expected permissions 0o755, but got 0o644\n',
    'final_fs': Dir(
      children={
        'file': File(
          content='content',
          permissions=420,
        ),
        'test.patch': File(
          content='\n'
            '!file %755->600\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}