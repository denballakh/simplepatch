{
  'before': 'line1\n'
    'line2\n'
    'line3\n',
  'patch_text': '!file\n'
    '-line2\n'
    '+new_line2\n',
  'result': Dir(
    children={
      'file': File(
        content='line1\n'
          'new_line2\n'
          'line3\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}