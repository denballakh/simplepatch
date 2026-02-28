{
  'patch_text': '!-> file\n'
    '+a\n',
  'result': PatchFile(
    chunks=[
      CreateOperation(
        path='file',
        lines=[
          AddedLine(
            content='a\n',
          ),
        ],
      ),
    ],
  ),
}