{
  'patch_text': 'diff --git a/only_deletions.txt b/only_deletions.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/only_deletions.txt\n'
    '+++ b/only_deletions.txt\n'
    '@@ -1,7 +1,3 @@\n'
    ' keep line 1\n'
    '-delete line 1\n'
    '-delete line 2\n'
    '-delete line 3\n'
    ' keep line 2\n'
    '-delete line 4\n'
    ' keep line 3\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='only_deletions.txt',
        new_path='only_deletions.txt',
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
            old_count=7,
            new_start=1,
            new_count=3,
            context='',
            lines=[
              GitContextLine(
                content='keep line 1',
              ),
              GitRemovedLine(
                content='delete line 1',
              ),
              GitRemovedLine(
                content='delete line 2',
              ),
              GitRemovedLine(
                content='delete line 3',
              ),
              GitContextLine(
                content='keep line 2',
              ),
              GitRemovedLine(
                content='delete line 4',
              ),
              GitContextLine(
                content='keep line 3',
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