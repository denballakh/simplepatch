{
  'patch_text': '!file %644->755\n',
  'result': PatchFile(
    chunks=[
      ChmodOperation(
        path='file',
        old_perms=420,
        new_perms=493,
      ),
    ],
  ),
}