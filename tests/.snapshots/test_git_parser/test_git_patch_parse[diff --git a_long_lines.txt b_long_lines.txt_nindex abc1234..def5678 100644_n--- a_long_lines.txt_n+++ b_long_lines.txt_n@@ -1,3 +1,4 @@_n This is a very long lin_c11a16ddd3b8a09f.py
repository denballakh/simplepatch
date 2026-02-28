{
  'patch_text': 'diff --git a/long_lines.txt b/long_lines.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/long_lines.txt\n'
    '+++ b/long_lines.txt\n'
    '@@ -1,3 +1,4 @@\n'
    ' This is a very long line that exceeds typical terminal width and should be handled correctly by the parser without any issues whatsoever even if it goes on and on and on\n'
    "+Another very long line added here that also exceeds typical terminal width and contains lots of text to test the parser's ability to handle long content\n"
    ' Short line\n'
    ' End\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='long_lines.txt',
        new_path='long_lines.txt',
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
                content='This is a very long line that exceeds typical terminal width and should be handled correctly by the parser without any issues whatsoever even if it goes on and on and on',
              ),
              GitAddedLine(
                content="Another very long line added here that also exceeds typical terminal width and contains lots of text to test the parser's ability to handle long content",
              ),
              GitContextLine(
                content='Short line',
              ),
              GitContextLine(
                content='End',
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