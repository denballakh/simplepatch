{
  'before': 'line1\n'
    'line2\n',
  'patch_text': '!file\n'
    '=line1\n'
    '-line2\n'
    '+line2^x\n',
  'result': Dir(
    children={
      'file': File(
        content='line1\n'
          'line2',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}