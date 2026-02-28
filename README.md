# simplepatch

`simplepatch` is both a patch file format and tool for applying them.
It is designed to be easily read and written by humans.

## Format Overview

### TLDR
```diff
# Edit file:
!dir/file
=context
-remove
+add
=context
# Note: `^` character has special meaning, see below for details

# Creation:
!-> dir/file
+content
!-> dir/subdir/

# Deletion:
!dir/file ->
!dir/subdir/ ->

# Renaming:
!dir/file -> dir/newfile
!dir/subdir/ -> dir/newdir/
```

### More elaborate example
```diff
# Comment lines start with # and are allowed everywhere and are ignored.
# Empty lines are also ignored:

# Headers start with ! and specify what operation to perform.
# Edit file:
!dir/file
-remove this
+replace with that

# Edit file with optional line number hint:
!dir/file @10
-remove this
+replace with that
!dir/file @50
-remove something else
# ^ to edit file in two different places, two chunks are used

# If line number changes - you can specify that too:
!dir/file @10
+add some lines in the beginning
+line numbers after that will increase by 2
!dir/file @50->52
-remove this
+replace with that

# Context lines:
!dir/file
=context before
-remove this
+replace with that
=context after

!dir/file
=context before
-delete this
=context in the middle
+add that
=context after

# If hunk is ambiguos - the first match is replaced:
!dir/file
+a
+b
+a
+c
!dir/file
-a
+x
!dir/file
-x
-b
-a
-c

# Add context lines to disambiguate:
!dir/file
+a
+b
+a
+c
!dir/file
-a
+x
=c
!dir/file
-a
-b
-x
-c


# It is completely fine to have comments and empty lines inside a patch.
# As promised, they are simply ignored:
!dir/file
=context before

-delete this
# <very useful comment describing the patch>
+add that

=context after
# thats an empty context line:
=

# Editing binary files is done by fully replacing their contents.
# Binary data is Z85 encoded, and each line is prefixed with `z`:
!dir/file
z0rJuas7(>4vrb{4D
z2E*FA+eV&x(mMaBz
zb98klah(aARKAv}V
z#$A::3gaPIGx00

# Character `^` has special meaning in context, added and removed lines:
#   ^0 - removed completely, you can put it on lines with trailing space to prevent code editors from trimming it automatically
#   ^r - replaced with carriage return character
#   ^t - replaced with tab character
#   ^x - means that the current line has no newline character at the end
#   ^^ - replaced with `^` character

# TODO: add examples of ^ usage

# File creation:
!-> dir/file
+content
# Directory creation:
!-> dir/subdir/
# Directories are distinguished by trailing /
# By default, files are created with 644 permissions, and directories with 755 permissions.

# Changing permissions:
!dir/file %644->750
!dir/subdir/ %755->750

# File deletion:
!dir/file ->
# Directory deletion (it is allowed to be nonempty):
!dir/subdir/ ->

# File renaming:
!dir/file -> dir/newfile
# Directory renaming:
!dir/ -> newdir/

```


### CLI

```bash
# Apply a patch
simplepatch apply changes.patch

# Apply multiple patches
simplepatch apply p1.patch p2.patch ./project

# Apply from stdin
cat changes.patch | simplepatch apply -

# Create a patch from git diff
git diff | simplepatch convert --from=unified > changes.patch

# Convert simplepatch to unified diff
simplepatch convert --to=unified changes.patch > changes.diff

# Generate a patch from two files
simplepatch diff old.py new.py > changes.patch
```