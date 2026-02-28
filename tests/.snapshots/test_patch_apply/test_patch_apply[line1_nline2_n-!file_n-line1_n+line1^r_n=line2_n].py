{
  'before': 'line1\n'
    'line2\n',
  'patch_text': '!file\n'
    '-line1\n'
    '+line1^r\n'
    '=line2\n',
  'result': Dir(
    children={
      'file': File(
        content='line1\n'
          'line2\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}