{
  'before': 'line1\n'
    'line2\n'
    'line3\n',
  'patch_text': '!file\n'
    '-line1\n'
    '-line2\n'
    '-line3\n',
  'result': Dir(
    children={
      'file': File(
        content='',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}