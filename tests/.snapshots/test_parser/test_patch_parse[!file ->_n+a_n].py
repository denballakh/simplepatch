{
  'patch_text': '!file ->\n'
    '+a\n',
  'result': PatchFile(
    chunks=[
      DeleteOperation(
        path='file',
      ),
    ],
  ),
}