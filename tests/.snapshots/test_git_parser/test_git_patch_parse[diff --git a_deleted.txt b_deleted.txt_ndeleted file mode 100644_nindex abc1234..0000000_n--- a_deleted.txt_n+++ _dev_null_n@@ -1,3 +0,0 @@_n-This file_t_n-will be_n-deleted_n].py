{
  'patch_text': 'diff --git a/deleted.txt b/deleted.txt\n'
    'deleted file mode 100644\n'
    'index abc1234..0000000\n'
    '--- a/deleted.txt\n'
    '+++ /dev/null\n'
    '@@ -1,3 +0,0 @@\n'
    '-This file\t\n'
    '-will be\n'
    '-deleted\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='deleted.txt',
        new_path=None,
        old_mode='100644',
        new_mode=None,
        old_index='abc1234',
        new_index='0000000',
        is_new_file=False,
        is_deleted_file=True,
        is_rename=False,
        is_binary=False,
        similarity_index=None,
        hunks=[
          GitHunk(
            old_start=1,
            old_count=3,
            new_start=0,
            new_count=0,
            context='',
            lines=[
              GitRemovedLine(
                content='This file\t',
              ),
              GitRemovedLine(
                content='will be',
              ),
              GitRemovedLine(
                content='deleted',
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