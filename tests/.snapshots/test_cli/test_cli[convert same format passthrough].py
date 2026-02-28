{
  'args': [
    'convert',
    '--from=simplepatch',
    '--to=simplepatch',
    'input.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'input.patch': File(
        content='!file.txt\n'
          '-old\n'
          '+new\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': '!file.txt\n'
      '-old\n'
      '+new\n'
      '\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'input.patch': File(
          content='!file.txt\n'
            '-old\n'
            '+new\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}