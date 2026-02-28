{
  'patch_text': 'diff --git a/simple.txt b/simple.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/simple.txt\n'
    '+++ b/simple.txt\n'
    '@@ -1,3 +1,4 @@\n'
    ' \tline 1\n'
    '+new line\n'
    ' \tline 2\n'
    ' line 3\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='simple.txt',
        new_path='simple.txt',
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
                content='\tline 1',
              ),
              GitAddedLine(
                content='new line',
              ),
              GitContextLine(
                content='\tline 2',
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