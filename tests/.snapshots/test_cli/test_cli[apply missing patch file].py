{
  'args': [
    'apply',
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
    'stderr': 'Error: Patch file not found: missing.patch\n',
    'final_fs': Dir(
      children={},
      permissions=493,
    ),
  },
}