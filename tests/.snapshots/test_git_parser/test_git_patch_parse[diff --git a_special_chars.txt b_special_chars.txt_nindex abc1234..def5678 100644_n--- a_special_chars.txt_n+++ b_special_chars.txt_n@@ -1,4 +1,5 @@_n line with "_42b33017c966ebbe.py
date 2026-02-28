{
  'patch_text': 'diff --git a/special_chars.txt b/special_chars.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/special_chars.txt\n'
    '+++ b/special_chars.txt\n'
    '@@ -1,4 +1,5 @@\n'
    ' line with "quotes"\n'
    " line with 'single quotes'\n"
    '+line with $variable and ${braces}\n'
    ' line with `backticks`\n'
    ' line with \\backslash\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='special_chars.txt',
        new_path='special_chars.txt',
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
                content='line with "quotes"',
              ),
              GitContextLine(
                content="line with 'single quotes'",
              ),
              GitAddedLine(
                content='line with $variable and ${braces}',
              ),
              GitContextLine(
                content='line with `backticks`',
              ),
              GitContextLine(
                content='line with \\backslash',
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