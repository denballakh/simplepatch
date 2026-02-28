{
  'before': 'a\n'
    'b\n',
  'patch_text': '!file @2\n'
    '=a\n'
    '-b\n'
    '+c\n',
  'result': Dir(
    children={
      'file': File(
        content='a\n'
          'c\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}