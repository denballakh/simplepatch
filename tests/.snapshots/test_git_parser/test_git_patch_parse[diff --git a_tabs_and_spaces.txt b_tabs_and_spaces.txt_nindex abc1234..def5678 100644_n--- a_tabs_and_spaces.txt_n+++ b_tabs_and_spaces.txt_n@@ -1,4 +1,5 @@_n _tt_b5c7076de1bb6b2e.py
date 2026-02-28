{
  'patch_text': 'diff --git a/tabs_and_spaces.txt b/tabs_and_spaces.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/tabs_and_spaces.txt\n'
    '+++ b/tabs_and_spaces.txt\n'
    '@@ -1,4 +1,5 @@\n'
    ' \ttab indented\n'
    '     space indented\n'
    '+\tmixed\ttabs\tand spaces\n'
    '   two spaces\n'
    ' \t\tdouble tab\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='tabs_and_spaces.txt',
        new_path='tabs_and_spaces.txt',
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
            old_count=4,
            new_start=1,
            new_count=5,
            context='',
            lines=[
              GitContextLine(
                content='\ttab indented',
              ),
              GitContextLine(
                content='    space indented',
              ),
              GitAddedLine(
                content='\tmixed\ttabs\tand spaces',
              ),
              GitContextLine(
                content='  two spaces',
              ),
              GitContextLine(
                content='\t\tdouble tab',
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