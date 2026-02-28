{
  'patch_text': '!file\n'
    '+^^\n'
    '-^^\n'
    '=^^\n'
    '+aaa^x\n'
    '+aaa^r\n'
    '+^raaa\n'
    '+^t   ^0\n'
    '+^0   ^t\n',
  'result': PatchFile(
    chunks=[
      EditOperation(
        path='file',
        line_hint=(
          None,
          None,
        ),
        lines=[
          AddedLine(
            content='^\n',
          ),
          RemovedLine(
            content='^\n',
          ),
          ContextLine(
            content='^\n',
          ),
          AddedLine(
            content='aaa',
          ),
          AddedLine(
            content='aaa\r\n',
          ),
          AddedLine(
            content='\r'
              'aaa\n',
          ),
          AddedLine(
            content='\t   \n',
          ),
          AddedLine(
            content='   \t\n',
          ),
        ],
      ),
    ],
  ),
}