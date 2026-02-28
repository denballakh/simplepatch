{
  'before': 'x = 1\n'
    'y = 2\n'
    'x = 1\n'
    'z = 3\n',
  'patch_text': '!file\n'
    '=y = 2\n'
    '-x = 1\n'
    '+x = 10\n'
    '=z = 3\n',
  'result': Dir(
    children={
      'file': File(
        content='x = 1\n'
          'y = 2\n'
          'x = 10\n'
          'z = 3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}