{
  'patch_text': '!file\n'
    '#c\n'
    '+a\n',
  'result': PatchFile(
    chunks=[
      EditOperation(
        path='file',
        line_hint=(
          None,
          None,
        ),
        lines=[
          AddedLine(
            content='a\n',
          ),
        ],
      ),
    ],
  ),
}