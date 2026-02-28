{
  'patch_text': 'diff --git a/deep/nested/path/file.txt b/deep/nested/path/file.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/deep/nested/path/file.txt\n'
    '+++ b/deep/nested/path/file.txt\n'
    '@@ -1,3 +1,4 @@\n'
    ' content in\n'
    '+new content\n'
    ' deeply nested\n'
    ' file\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='deep/nested/path/file.txt',
        new_path='deep/nested/path/file.txt',
        old_mode=None,
        new_mode='100644',
        old_index='abc1234',
        new_index='def5678',
        is_new_file=False,
        is_deleted_file=False,
        is_rename=False,
        is_binary=False,
        similarity_index=None,
        hunks=[
          GitHunk(
            old_start=1,
            old_count=3,
            new_start=1,
            new_count=4,
            context='',
            lines=[
              GitContextLine(
                content='content in',
              ),
              GitAddedLine(
                content='new content',
              ),
              GitContextLine(
                content='deeply nested',
              ),
              GitContextLine(
                content='file',
              ),
            ],
          ),
        ],
        binary_patch=None,
      ),
    ],
    submodules=[],
    preamble=None,
  ),
}