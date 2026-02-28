{
  'before': None,
  'patch_text': '!-> file\n'
    '+content\n',
  'result': Dir(
    children={
      'file': File(
        content='content\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}