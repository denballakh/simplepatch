{
  'patch_text': '!dir/dir/./dir/file\n',
  'result': PatchFile(
    chunks=[
      EditOperation(
        path='dir/dir/./dir/file',
        line_hint=(
          None,
          None,
        ),
        lines=[],
      ),
    ],
  ),
}