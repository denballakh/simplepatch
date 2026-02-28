{
  'patch_text': 'diff --git a/renamed_with_changes.txt b/renamed_modified.txt\n'
    'similarity index 85%\n'
    'rename from renamed_with_changes.txt\n'
    'rename to renamed_modified.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/renamed_with_changes.txt\n'
    '+++ b/renamed_modified.txt\n'
    '@@ -1,3 +1,4 @@\n'
    ' line 1\n'
    '+added line\n'
    ' line 2\n'
    ' line 3\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='renamed_with_changes.txt',
        new_path='renamed_modified.txt',
        old_mode=None,
        new_mode='100644',
        old_index='abc1234',
        new_index='def5678',
        is_new_file=False,
        is_deleted_file=False,
        is_rename=True,
        is_binary=False,
        similarity_index=85,
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
                content='added line',
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