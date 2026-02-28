{
  'patch_text': '!-> file\n'
    '=c\n'
    '+a\n'
    '=c\n',
  'result': PatchFile(
    chunks=[
      CreateOperation(
        path='file',
        lines=[
          ContextLine(
            content='c\n',
          ),
          AddedLine(
            content='a\n',
          ),
          ContextLine(
            content='c\n',
          ),
        ],
      ),
    ],
  ),
}