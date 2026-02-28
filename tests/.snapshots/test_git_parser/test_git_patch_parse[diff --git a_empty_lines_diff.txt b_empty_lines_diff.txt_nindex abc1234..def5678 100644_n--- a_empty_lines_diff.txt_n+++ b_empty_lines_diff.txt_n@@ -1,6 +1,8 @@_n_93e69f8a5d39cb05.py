{
  'patch_text': 'diff --git a/empty_lines_diff.txt b/empty_lines_diff.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/empty_lines_diff.txt\n'
    '+++ b/empty_lines_diff.txt\n'
    '@@ -1,6 +1,8 @@\n'
    ' line 1\n'
    ' \n'
    '+\n'
    ' line 2\n'
    '+\n'
    ' \n'
    ' line 3\n'
    ' \n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='empty_lines_diff.txt',
        new_path='empty_lines_diff.txt',
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
            old_count=6,
            new_start=1,
            new_count=8,
            context='',
            lines=[
              GitContextLine(
                content='line 1',
              ),
              GitContextLine(
                content='',
              ),
              GitAddedLine(
                content='',
              ),
              GitContextLine(
                content='line 2',
              ),
              GitAddedLine(
                content='',
              ),
              GitContextLine(
                content='',
              ),
              GitContextLine(
                content='line 3',
              ),
              GitContextLine(
                content='',
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