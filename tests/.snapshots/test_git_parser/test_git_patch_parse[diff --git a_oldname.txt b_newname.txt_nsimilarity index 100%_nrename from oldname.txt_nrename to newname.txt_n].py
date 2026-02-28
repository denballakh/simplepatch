{
  'patch_text': 'diff --git a/oldname.txt b/newname.txt\n'
    'similarity index 100%\n'
    'rename from oldname.txt\n'
    'rename to newname.txt\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='oldname.txt',
        new_path='newname.txt',
        old_mode=None,
        new_mode=None,
        old_index=None,
        new_index=None,
        is_new_file=False,
        is_deleted_file=False,
        is_rename=True,
        is_binary=False,
        similarity_index=100,
        hunks=[],
        binary_patch=None,
      ),
    ],
    submodules=[],
    preamble=None,
  ),
}