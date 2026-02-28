{
  'before': 'line1\n'
    'line2\n'
    'line3\n'
    'line4\n',
  'patch_text': '!file @3\n'
    '-line3\n'
    '+new3\n'
    '\n'
    '!file @1\n'
    '-line1\n'
    '+new1\n',
  'result': Dir(
    children={
      'file': File(
        content='new1\n'
          'line2\n'
          'new3\n'
          'line4\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}