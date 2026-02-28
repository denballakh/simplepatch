{
  'args': [
    'apply',
    '-h',
  ],
  'stdin': None,
  'fs': Dir(
    children={},
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'usage: simplepatch apply [-h] patches [patches ...] [target_dir]\n'
      '\n'
      'positional arguments:\n'
      '  patches     Patch files to apply (use "-" for stdin)\n'
      '  target_dir  Target directory (default: current directory)\n'
      '\n'
      'options:\n'
      '  -h, --help  show this help message and exit\n',
    'stderr': '',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}