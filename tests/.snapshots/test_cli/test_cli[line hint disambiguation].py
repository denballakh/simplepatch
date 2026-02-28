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
          '!file @1\n'
          '-x = 1\n'
          '+x = 10\n',
        permissions=420,
      ),
      'file': File(
        content='x = 1\n'
          'y = 2\n'
          'x = 1\n'
          'z = 3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: Ambiguous match in file\n'
      'Found 2 occurrences at lines: [0, 2]\n'
      'Add context lines to disambiguate.\n',
    'final_fs': Dir(
      children={
        'file': File(
          content='x = 1\n'
            'y = 2\n'
            'x = 1\n'
            'z = 3\n',
          permissions=420,
        ),
        'test.patch': File(
          content='\n'
            '!file @1\n'
            '-x = 1\n'
            '+x = 10\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}