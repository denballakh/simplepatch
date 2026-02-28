{
  'patch_text': '!-> file\n'
    '-b\n'
    '+a\n',
  'result': PatchFile(
    chunks=[
      CreateOperation(
        path='file',
        lines=[
          RemovedLine(
            content='b\n',
          ),
          AddedLine(
            content='a\n',
          ),
        ],
      ),
    ],
  ),
}