{
  'patch_text': '!file -> file2\n',
  'result': PatchFile(
    chunks=[
      RenameOperation(
        old_path='file',
        new_path='file2',
      ),
    ],
  ),
}