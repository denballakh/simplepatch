{
  'args': [
    'apply',
    'test.patch',
  ],
  'stdin': None,
  'fs': Dir(
    children={
      'test.patch': File(
        content='\n'
          '!file.sh %644->755\n',
        permissions=420,
      ),
      'file.sh': File(
        content=b'#!/bin/bash\n'
          b'echo "Hello"\n',
        permissions=420,
      ),
    },
    permissions=493,
  ),
  'result': {
    'exit_code': 0,
    'stdout': 'Applied test.patch to .\n',
    'stderr': '',
    'final_fs': Dir(
      children={
        'file.sh': File(
          content='#!/bin/bash\n'
            'echo "Hello"\n',
          permissions=493,
        ),
        'test.patch': File(
          content='\n'
            '!file.sh %644->755\n',
          permissions=420,
        ),
      },
      permissions=493,
    ),
  },
}