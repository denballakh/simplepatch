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
          '!file\n'
          '-Hello 世界\n'
          '+Goodbye 世界\n',
        permissions=420,
      ),
      'file': File(
        content='Hello 世界\n'
          'Привет мир\n',
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
        'file': File(
          content='Goodbye 世界\n'
            'Привет мир\n',
          permissions=420,
        ),
        'test.patch': File(
          content='\n'
            '!file\n'
            '-Hello 世界\n'
            '+Goodbye 世界\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}