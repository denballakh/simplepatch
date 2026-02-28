{
  'patch_text': '!file\n'
    '-b\n',
  'result': PatchFile(
    chunks=[
      EditOperation(
        path='file',
        line_hint=(
          None,
          None,
        ),
        lines=[
          RemovedLine(
            content='b\n',
          ),
        ],
      ),
    ],
  ),
}