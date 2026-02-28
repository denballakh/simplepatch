{
  'patch_text': '!file ->\n'
    '=c\n',
  'result': PatchFile(
    chunks=[
      DeleteOperation(
        path='file',
      ),
    ],
  ),
}