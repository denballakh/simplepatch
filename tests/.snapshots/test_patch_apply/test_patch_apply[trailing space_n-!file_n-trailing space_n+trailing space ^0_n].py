{
  'before': 'trailing space\n',
  'patch_text': '!file\n'
    '-trailing space\n'
    '+trailing space ^0\n',
  'result': Dir(
    children={
      'file': File(
        content='trailing space \n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}