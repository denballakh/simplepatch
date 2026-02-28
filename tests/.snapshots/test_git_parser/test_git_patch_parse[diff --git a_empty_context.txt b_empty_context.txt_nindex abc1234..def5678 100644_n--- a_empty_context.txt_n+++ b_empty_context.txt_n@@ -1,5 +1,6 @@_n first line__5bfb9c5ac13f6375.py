{
  'patch_text': 'diff --git a/empty_context.txt b/empty_context.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/empty_context.txt\n'
    '+++ b/empty_context.txt\n'
    '@@ -1,5 +1,6 @@\n'
    ' first line\n'
    ' \n'
    '+added after empty line\n'
    ' \n'
    ' last line\n'
    ' \n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='empty_context.txt',
        new_path='empty_context.txt',
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
            old_count=5,
            new_start=1,
            new_count=6,
            context='',
            lines=[
              GitContextLine(
                content='first line',
              ),
              GitContextLine(
                content='',
              ),
              GitAddedLine(
                content='added after empty line',
              ),
              GitContextLine(
                content='',
              ),
              GitContextLine(
                content='last line',
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