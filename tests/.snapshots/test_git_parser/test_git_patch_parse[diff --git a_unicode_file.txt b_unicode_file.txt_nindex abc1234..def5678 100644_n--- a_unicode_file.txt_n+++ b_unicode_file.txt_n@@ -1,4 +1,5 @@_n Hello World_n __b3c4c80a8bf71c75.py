{
  'patch_text': 'diff --git a/unicode_file.txt b/unicode_file.txt\n'
    'index abc1234..def5678 100644\n'
    '--- a/unicode_file.txt\n'
    '+++ b/unicode_file.txt\n'
    '@@ -1,4 +1,5 @@\n'
    ' Hello World\n'
    ' Привет мир\n'
    '+日本語テキスト\n'
    ' مرحبا بالعالم\n'
    ' 🎉 emoji test 🚀\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='unicode_file.txt',
        new_path='unicode_file.txt',
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
                content='Hello World',
              ),
              GitContextLine(
                content='Привет мир',
              ),
              GitAddedLine(
                content='日本語テキスト',
              ),
              GitContextLine(
                content='مرحبا بالعالم',
              ),
              GitContextLine(
                content='🎉 emoji test 🚀',
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