{
  'patch_text': '!file ->\n'
    '-b\n',
  'result': PatchFile(
    chunks=[
      DeleteOperation(
        path='file',
      ),
    ],
  ),
}