# Simple Patch

`simplepatch` is both a patch file format and tool for applying them.

## Examples

```diff
# Comments start with `#` symbol and last until the end of the line.
# Comment lines are completely ignored, as if they were not in the patch file in the first place.

# Patch chunk looks like this:
!<header specifying the file being patched>
 context line start with space
# comments might appear here as well
- removed lines start with -
+ added lines start with +
 more context here
 but context is not mandatory and can be omitted
# for binary patches the entire new blob is specified
# patch body is a sequence of Z85-encoded lines (prefixed with `x`)
# or base85-encoded lines (prefixed with `z`)
# Z85 spec: https://rfc.zeromq.org/spec/32/
xxK#0@zY<mxA+]m
zXk~0{Zy<MXa%^M

# Header might look like this:
!file
# with a line number for human to read
!file:123
# line number was changed
!file:123->456
# file was renamed
!file1 -> file2
# file got deleted
!file ->
# file got created
! -> file

# If patch line ends with a whitespace, it should have a `$0` to the end of a line,
#   so that code editors dont strip trailing whitespace automatically.
# If patch line has \r\n endings, it should have a `$r` to the end of a line.
# If last line of a file does not end with a newline, it should have a `$x` to the end of a line.

```
