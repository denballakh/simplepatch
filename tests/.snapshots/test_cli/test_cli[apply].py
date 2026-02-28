{
  'args': [
    'apply',
  ],
  'stdin': None,
  'fs': Dir(
    children={},
    permissions=493,
  ),
  'result': {
    'exit_code': 2,
    'stdout': '',
    'stderr': 'usage: simplepatch apply [-h] patches [patches ...] [target_dir]\n'
      '\n'
      'positional arguments:\n'
      '  patches     Patch files to apply (use "-" for stdin)\n'
      '  target_dir  Target directory (default: current directory)\n'
      '\n'
      'options:\n'
      '  -h, --help  show this help message and exit\n'
      '\n'
      'error: the following arguments are required: patches\n',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}