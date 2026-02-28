{
  'patch_text': 'diff --git a/binary_file.bin b/binary_file.bin\n'
    'new file mode 100644\n'
    'index 0000000000000000000000000000000000000000..ab993f17662b9b0868d97b08711b6c84446eabb9\n'
    'GIT binary patch\n'
    'literal 876\n'
    'zc${sLQAiU37{|ZwZo6%6L^C3lNJKxfOG`Yw5fKp(5fBNuAP5Kk0|Ntt0|WzuAP5Kk\n'
    '\n'
    'literal 0\n'
    'Hc$@<O00001\n'
    '\n',
  'result': GitPatch(
    header=None,
    diffs=[
      GitFileDiff(
        old_path='binary_file.bin',
        new_path='binary_file.bin',
        old_mode=None,
        new_mode='100644',
        old_index='0000000000000000000000000000000000000000',
        new_index='ab993f17662b9b0868d97b08711b6c84446eabb9',
        is_new_file=True,
        is_deleted_file=False,
        is_rename=False,
        is_binary=True,
        similarity_index=None,
        hunks=[],
        binary_patch=GitBinaryPatch(
          forward=GitBinaryPatchData(
            patch_type='literal',
            size=876,
            data='zc${sLQAiU37{|ZwZo6%6L^C3lNJKxfOG`Yw5fKp(5fBNuAP5Kk0|Ntt0|WzuAP5Kk',
          ),
          reverse=GitBinaryPatchData(
            patch_type='literal',
            size=0,
            data='Hc$@<O00001',
          ),
        ),
      ),
    ],
    submodules=[],
    preamble=None,
  ),
}