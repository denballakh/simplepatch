{
  'args': [
    'convert',
    '--from=git',
    '--to=simplepatch',
    'missing.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={},
    permissions=493,
  ),
  'result': {
    'exit_code': 1,
    'stdout': '',
    'stderr': 'Error: Input file not found: missing.patch\n',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}