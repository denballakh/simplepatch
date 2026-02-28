{
  'args': [
    'convert',
    '-h',
  ],
  'stdin': None,
  'fs': Dir(
    children={},
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'usage: simplepatch convert [-h] [--from {git,simplepatch}]\n'
      '                           [--to {git,simplepatch}]\n'
      '                           [input_file]\n'
      '\n'
      'positional arguments:\n'
      '  input_file            Input file (default: stdin)\n'
      '\n'
      'options:\n'
      '  -h, --help            show this help message and exit\n'
      '  --from {git,simplepatch}\n'
      '                        Source format (auto-detected if omitted)\n'
      '  --to {git,simplepatch}\n'
      '                        Target format (default: simplepatch)\n',
    'stderr': '',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}