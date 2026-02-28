{
  'args': [
    'convert',
    '--from=git',
    '--to=simplepatch',
    'input.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'input.patch': File(
        content='diff --git a/script.sh b/script.sh\n'
          'old mode 100644\n'
          'new mode 100755\n'
          'index abc1234..abc1234\n'
          '--- a/script.sh\n'
          '+++ b/script.sh\n'
          '@@ -1 +1 @@\n'
          '-echo "not executable"\n'
          '+echo "now executable"\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': '!script.sh %644->755\n'
      '!script.sh @1\n'
      '-echo "not executable"\n'
      '+echo "now executable"\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='diff --git a/script.sh b/script.sh\n'
            'old mode 100644\n'
            'new mode 100755\n'
            'index abc1234..abc1234\n'
            '--- a/script.sh\n'
            '+++ b/script.sh\n'
            '@@ -1 +1 @@\n'
            '-echo "not executable"\n'
            '+echo "now executable"\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}