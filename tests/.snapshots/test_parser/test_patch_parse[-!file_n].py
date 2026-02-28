{
  'patch_text': '-!file\n',
  'result': (
    lark.exceptions.UnexpectedToken,
    lark.exceptions.UnexpectedToken(
      "Unexpected token Token('LINE_CONTENT', '-!file') at line 1, column 1.\n"
      'Expected one of: \n'
      '\t* $END\n'
      '\t* BANG\n'
      '\t* HASH\n'
      '\t* _NEWLINE\n'
      'Previous tokens: [None]\n'),
  ),
}