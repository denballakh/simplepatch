{
  'before': 'def  foo():\n'
    '    pass\n',
  'patch_text': '!file\n'
    '-def  foo():\n'
    '-    pass\n'
    '+def  foo():\n'
    '+    return 42\n',
  'result': Dir(
    children={
      'file': File(
        content='def  foo():\n'
          '    return 42\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}