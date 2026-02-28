{
  'args': [
    '--help',
  ],
  'stdin': None,
  'fs': Dir(
    children={},
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'usage: simplepatch [-h] [-V] {apply,convert,diff} ...\n'
      '\n'
      'SimplePatch - Human-friendly patch format and tool\n'
      '\n'
      'positional arguments:\n'
      '  {apply,convert,diff}  Available commands\n'
      '    apply               Apply one or more patches to a directory\n'
      '    convert             Convert between patch formats\n'
      '    diff                Generate a simplepatch from two files\n'
      '\n'
      'options:\n'
      '  -h, --help            show this help message and exit\n'
      "  -V, --version         show program's version number and exit\n",
    'stderr': '',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}