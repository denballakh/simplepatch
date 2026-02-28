{
  'patch_text': 'From 0000000000000000000000000000000000000000 Mon Sep 17 00:00:00 2001\n'
    'From: noname <noname@example.com>\n'
    'Date: at some day\n'
    'Subject: [xxx] fix it\n'
    '\n'
    'Ticket: XXX-1234\n'
    '\n'
    'This is a commit message body that should be ignored.\n'
    'It can span multiple lines and contain various content.\n'
    '\n'
    'Signed-off-by: Someone <someone@example.com>\n'
    '\n'
    'diff --git a/xxx b/xxx\n'
    'index 0000000..0000000 100755\n'
    '--- a/xxx\n'
    '+++ b/xxx\n'
    '@@ -100,3 +100,4 @@\n'
    '     mount_partition\n'
    '+    echo "New line added"\n'
    ' fi\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='xxx',
        new_path='xxx',
        old_mode=None,
        new_mode='100755',
        old_index='0000000',
        new_index='0000000',
        is_new_file=False,
        is_deleted_file=False,
        is_rename=False,
        is_binary=False,
        similarity_index=None,
        hunks=[
          GitHunk(
            old_start=100,
            old_count=3,
            new_start=100,
            new_count=4,
            context='',
            lines=[
              GitContextLine(
                content='    mount_partition',
              ),
              GitAddedLine(
                content='    echo "New line added"',
              ),
              GitContextLine(
                content='fi',
              ),
            ],
          ),
        ],
        binary_patch=None,
      ),
    ],
    submodules=[],
    preamble='From 0000000000000000000000000000000000000000 Mon Sep 17 00:00:00 2001\n'
      'From: noname <noname@example.com>\n'
      'Date: at some day\n'
      'Subject: [xxx] fix it\n'
      '\n'
      'Ticket: XXX-1234\n'
      '\n'
      'This is a commit message body that should be ignored.\n'
      'It can span multiple lines and contain various content.\n'
      '\n'
      'Signed-off-by: Someone <someone@example.com>',
  ),
}