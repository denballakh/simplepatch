{
  'before': 'def foo():\n'
    '    pass\n'
    '\n'
    'def bar():\n'
    '    pass\n',
  'patch_text': '!file @3\n'
    '-def bar():\n'
    '-    pass\n'
    '+def bar():\n'
    '+    return 42\n',
  'result': Dir(
    children={
      'file': File(
        content='def foo():\n'
          '    pass\n'
          '\n'
          'def bar():\n'
          '    return 42\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}