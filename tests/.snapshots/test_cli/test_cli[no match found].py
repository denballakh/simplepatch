{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='!file\n'
          '-nonexistent line\n'
          '+new line\n',
        permissions=420,
      ),
      'file': File(
        content='line1\n'
          'line2\n'
          'line3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: Could not find match in file\n'
      "Looking for: ['nonexistent line\\n']\n",
    'final_fs': Dir(
      children={
        'file': File(
          content='line1\n'
            'line2\n'
            'line3\n',
          permissions=420,
        ),
        'test.patch': File(
          content='!file\n'
            '-nonexistent line\n'
            '+new line\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}