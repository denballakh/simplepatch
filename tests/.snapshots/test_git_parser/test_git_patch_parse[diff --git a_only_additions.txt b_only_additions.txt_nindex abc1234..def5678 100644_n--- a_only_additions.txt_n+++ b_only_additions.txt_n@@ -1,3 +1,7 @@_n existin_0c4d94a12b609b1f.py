{
  'patch_text': 'diff --git a/only_additions.txt b/only_additions.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/only_additions.txt\n'
    '+++ b/only_additions.txt\n'
    '@@ -1,3 +1,7 @@\n'
    ' existing line 1\n'
    '+new line 1\n'
    '+new line 2\n'
    '+new line 3\n'
    ' existing line 2\n'
    '+new line 4\n'
    ' existing line 3\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='only_additions.txt',
        new_path='only_additions.txt',
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
            new_count=7,
            context='',
            lines=[
              GitContextLine(
                content='existing line 1',
              ),
              GitAddedLine(
                content='new line 1',
              ),
              GitAddedLine(
                content='new line 2',
              ),
              GitAddedLine(
                content='new line 3',
              ),
              GitContextLine(
                content='existing line 2',
              ),
              GitAddedLine(
                content='new line 4',
              ),
              GitContextLine(
                content='existing line 3',
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