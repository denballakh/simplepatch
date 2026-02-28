{
  'patch_text': 'diff --git a/no_newline.txt b/no_newline.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/no_newline.txt\n'
    '+++ b/no_newline.txt\n'
    '@@ -1,3 +1,3 @@\n'
    ' line 1\n'
    ' line 2\n'
    '-line 3\n'
    '\\ No newline at end of file\n'
    '+line 3 modified\n'
    '\\ No newline at end of file\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='no_newline.txt',
        new_path='no_newline.txt',
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
            new_count=3,
            context='',
            lines=[
              GitContextLine(
                content='line 1',
              ),
              GitContextLine(
                content='line 2',
              ),
              GitRemovedLine(
                content='line 3',
              ),
              GitNoNewlineMarker(),
              GitAddedLine(
                content='line 3 modified',
              ),
              GitNoNewlineMarker(),
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