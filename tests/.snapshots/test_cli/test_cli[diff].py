{
  'args': [
    'diff',
  ],
  'stdin': None,
  'fs': Dir(
    children={},
    permissions=493,
  ),
  'result': {
    'exit_code': 2,
    'stdout': '',
    'stderr': 'usage: simplepatch diff [-h] old_file new_file\n'
      '\n'
      'positional arguments:\n'
      '  old_file    Original file\n'
      '  new_file    Modified file\n'
      '\n'
      'options:\n'
      '  -h, --help  show this help message and exit\n'
      '\n'
      'error: the following arguments are required: old_file, new_file\n',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}