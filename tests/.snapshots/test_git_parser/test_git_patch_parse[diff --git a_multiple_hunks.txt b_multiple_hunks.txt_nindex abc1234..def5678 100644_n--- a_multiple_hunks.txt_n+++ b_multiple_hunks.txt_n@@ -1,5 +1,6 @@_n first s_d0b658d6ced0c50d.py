{
  'patch_text': 'diff --git a/multiple_hunks.txt b/multiple_hunks.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/multiple_hunks.txt\n'
    '+++ b/multiple_hunks.txt\n'
    '@@ -1,5 +1,6 @@\n'
    ' first section\n'
    ' line 2\n'
    '+added in first hunk\n'
    ' line 3\n'
    ' line 4\n'
    ' line 5\n'
    '@@ -10,6 +11,7 @@ line 9\n'
    ' line 10\n'
    ' second section\n'
    ' line 12\n'
    '+added in second hunk\n'
    ' line 13\n'
    ' line 14\n'
    ' line 15\n'
    '@@ -20,5 +22,6 @@ line 19\n'
    ' line 20\n'
    ' third section\n'
    ' line 22\n'
    '+added in third hunk\n'
    ' line 23\n'
    ' line 24\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='multiple_hunks.txt',
        new_path='multiple_hunks.txt',
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
                content='first section',
              ),
              GitContextLine(
                content='line 2',
              ),
              GitAddedLine(
                content='added in first hunk',
              ),
              GitContextLine(
                content='line 3',
              ),
              GitContextLine(
                content='line 4',
              ),
              GitContextLine(
                content='line 5',
              ),
            ],
          ),
          GitHunk(
            old_start=10,
            old_count=6,
            new_start=11,
            new_count=7,
            context='line 9',
            lines=[
              GitContextLine(
                content='line 10',
              ),
              GitContextLine(
                content='second section',
              ),
              GitContextLine(
                content='line 12',
              ),
              GitAddedLine(
                content='added in second hunk',
              ),
              GitContextLine(
                content='line 13',
              ),
              GitContextLine(
                content='line 14',
              ),
              GitContextLine(
                content='line 15',
              ),
            ],
          ),
          GitHunk(
            old_start=20,
            old_count=5,
            new_start=22,
            new_count=6,
            context='line 19',
            lines=[
              GitContextLine(
                content='line 20',
              ),
              GitContextLine(
                content='third section',
              ),
              GitContextLine(
                content='line 22',
              ),
              GitAddedLine(
                content='added in third hunk',
              ),
              GitContextLine(
                content='line 23',
              ),
              GitContextLine(
                content='line 24',
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