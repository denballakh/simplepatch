{
  'before': '^\n',
  'patch_text': '!file\n'
    '-^^\n'
    '+here is a single caret char: -> ^^ <-\n',
  'result': Dir(
    children={
      'file': File(
        content='here is a single caret char: -> ^ <-\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
}