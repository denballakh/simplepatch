{
  'patch_text': 'diff --git a/file.with.dots.txt b/file.with.dots.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/file.with.dots.txt\n'
    '+++ b/file.with.dots.txt\n'
    '@@ -1,3 +1,4 @@\n'
    ' line 1\n'
    '+added\n'
    ' line 2\n'
    ' line 3\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='file.with.dots.txt',
        new_path='file.with.dots.txt',
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
                content='line 1',
              ),
              GitAddedLine(
                content='added',
              ),
              GitContextLine(
                content='line 2',
              ),
              GitContextLine(
                content='line 3',
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