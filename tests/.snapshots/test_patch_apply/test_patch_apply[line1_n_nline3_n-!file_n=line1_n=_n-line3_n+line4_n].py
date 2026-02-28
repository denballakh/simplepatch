{
  'before': 'line1\n'
    '\n'
    'line3\n',
  'patch_text': '!file\n'
    '=line1\n'
    '=\n'
    '-line3\n'
    '+line4\n',
  'result': Dir(
    children={
      'file': File(
        content='line1\n'
          '\n'
          'line4\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}