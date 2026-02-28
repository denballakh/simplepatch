{
  'patch_text': '!file @x\n',
  'result': (
    lark.exceptions.UnexpectedToken,
    lark.exceptions.UnexpectedToken(
      "Unexpected token Token('PATH', 'x') at line 1, column 8.\n"
      'Expected one of: \n'
      '\t* NUMBER\n'
      "Previous tokens: [Token('AT', '@')]\n"),
  ),
}