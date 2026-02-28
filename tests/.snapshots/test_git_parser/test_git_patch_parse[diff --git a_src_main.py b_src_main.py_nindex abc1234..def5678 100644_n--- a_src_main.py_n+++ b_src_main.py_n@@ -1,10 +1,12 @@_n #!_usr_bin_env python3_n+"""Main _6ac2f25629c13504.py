{
  'patch_text': 'diff --git a/src/main.py b/src/main.py\n'
    'index abc1234..def5678 100644\n'
    '--- a/src/main.py\n'
    '+++ b/src/main.py\n'
    '@@ -1,10 +1,12 @@\n'
    ' #!/usr/bin/env python3\n'
    '+"""Main module docstring."""\n'
    ' \n'
    ' import os\n'
    ' import sys\n'
    '+from typing import Optional\n'
    ' \n'
    ' \n'
    '-def main():\n'
    '+def main() -> None:\n'
    '     """Main function."""\n'
    '     print("Hello, World!")\n'
    ' \n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='src/main.py',
        new_path='src/main.py',
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
            old_count=10,
            new_start=1,
            new_count=12,
            context='',
            lines=[
              GitContextLine(
                content='#!/usr/bin/env python3',
              ),
              GitAddedLine(
                content='"""Main module docstring."""',
              ),
              GitContextLine(
                content='',
              ),
              GitContextLine(
                content='import os',
              ),
              GitContextLine(
                content='import sys',
              ),
              GitAddedLine(
                content='from typing import Optional',
              ),
              GitContextLine(
                content='',
              ),
              GitContextLine(
                content='',
              ),
              GitRemovedLine(
                content='def main():',
              ),
              GitAddedLine(
                content='def main() -> None:',
              ),
              GitContextLine(
                content='    """Main function."""',
              ),
              GitContextLine(
                content='    print("Hello, World!")',
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