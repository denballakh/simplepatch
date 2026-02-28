{
  'patch_text': '!file @1->2\n',
  'result': PatchFile(
    chunks=[
      EditOperation(
        path='file',
        line_hint=(
          1,
          2,
        ),
        lines=[],
      ),
    ],
  ),
}