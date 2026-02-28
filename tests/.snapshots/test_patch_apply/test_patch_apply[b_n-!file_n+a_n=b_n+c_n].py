{
  'before': 'b\n',
  'patch_text': '!file\n'
    '+a\n'
    '=b\n'
    '+c\n',
  'result': Dir(
    children={
      'file': File(
        content='a\n'
          'b\n'
          'c\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}