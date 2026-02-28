{
  'patch_text': 'diff --git a/newfile.txt b/newfile.txt\n'
    'new file mode 100644\n'
    'index 0000000..abc1234\n'
    '--- /dev/null\n'
    '+++ b/newfile.txt\n'
    '@@ -0,0 +1,3 @@\n'
    '+\tThis is a new file\n'
    '+with multiple lines\n'
    '+of content\t\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path=None,
        new_path='newfile.txt',
        old_mode=None,
        new_mode='100644',
        old_index='0000000',
        new_index='abc1234',
        is_new_file=True,
        is_deleted_file=False,
        is_rename=False,
        is_binary=False,
        similarity_index=None,
        hunks=[
          GitHunk(
            old_start=0,
            old_count=0,
            new_start=1,
            new_count=3,
            context='',
            lines=[
              GitAddedLine(
                content='\tThis is a new file',
              ),
              GitAddedLine(
                content='with multiple lines',
              ),
              GitAddedLine(
                content='of content\t',
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