{
  'patch_text': 'diff --git a/mode_change.sh b/mode_change.sh\n'
    'old mode 100644\n'
    'new mode 100755\n'
    'index abc1234..abc1234\n'
    '--- a/mode_change.sh\n'
    '+++ b/mode_change.sh\n'
    '@@ -1 +1 @@\n'
    '-echo "not executable"\n'
    '+echo "now executable"\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='mode_change.sh',
        new_path='mode_change.sh',
        old_mode='100644',
        new_mode='100755',
        old_index='abc1234',
        new_index='abc1234',
        is_new_file=False,
        is_deleted_file=False,
        is_rename=False,
        is_binary=False,
        similarity_index=None,
        hunks=[
          GitHunk(
            old_start=1,
            old_count=1,
            new_start=1,
            new_count=1,
            context='',
            lines=[
              GitRemovedLine(
                content='echo "not executable"',
              ),
              GitAddedLine(
                content='echo "now executable"',
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