{
  'before': 'unix\n'
    'windows^r\n'
    'unix\n',
  'patch_text': '!file\n'
    '-unix\n'
    '+modified unix\n'
    '-windows^r\n'
    '+modified windows^r\n',
  'result': (
    simplepatch.applier.NoMatchFoundError,
    simplepatch.applier.NoMatchFoundError(
      'Could not find match in file\n'
        "Looking for: ['unix\\n', 'windows\\r\\n']",
    ),
  ),
}