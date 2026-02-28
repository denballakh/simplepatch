"""Converter module for converting between git patch and simplepatch formats."""

from .models import (
    # Git patch models
    GitPatch,
    GitFileDiff,
    GitHunk,
    GitContextLine,
    GitAddedLine,
    GitRemovedLine,
    GitNoNewlineMarker,
    GitSubmoduleDiff,
    # SimplePatch models
    PatchFile,
    EditOperation,
    CreateOperation,
    DeleteOperation,
    RenameOperation,
    ChmodOperation,
    ContextLine,
    AddedLine,
    RemovedLine,
    HunkLine,
)
from .parser import parse_git_patch


def _escape_simplepatch_content(content: str) -> str:
    """Escape special characters for simplepatch format.

    SimplePatch uses ^ as escape character:
    - ^0 - removed completely (for trailing space preservation)
    - ^r - carriage return
    - ^t - tab character
    - ^x - no newline at end
    - ^^ - literal ^ character
    """
    result = []
    for char in content:
        if char == '^':
            result.append('^^')
        elif char == '\r':
            result.append('^r')
        elif char == '\t':
            result.append('^t')
        else:
            result.append(char)
    return ''.join(result)


def _format_simplepatch_line(prefix: str, content: str, no_newline: bool = False) -> str:
    """Format a line for simplepatch output.

    Args:
        prefix: The line prefix ('+', '-', '=')
        content: The line content (without newline)
        no_newline: Whether this line has no newline at end of file
    """
    escaped = _escape_simplepatch_content(content)
    if no_newline:
        return f'{prefix}{escaped}^x\n'
    # Handle trailing spaces by adding ^0 marker
    if escaped.endswith(' '):
        return f'{prefix}{escaped}^0\n'
    return f'{prefix}{escaped}\n'


def convert_git_to_simplepatch(git_patch: GitPatch) -> str:
    """Convert a GitPatch object to simplepatch format string.

    Args:
        git_patch: Parsed git patch object

    Returns:
        SimplePatch format string
    """
    lines: list[str] = []

    # Add preamble (commit header, message, etc.) as comments if present
    if git_patch.preamble:
        for preamble_line in git_patch.preamble.split('\n'):
            lines.append(f'# {preamble_line}\n')
        lines.append('\n')

    for diff in git_patch.diffs:
        lines.extend(_convert_file_diff_to_simplepatch(diff))

    # Handle submodule diffs
    for submodule in git_patch.submodules:
        lines.extend(_convert_submodule_diff_to_simplepatch(submodule))

    return ''.join(lines)


def _convert_submodule_diff_to_simplepatch(submodule: GitSubmoduleDiff) -> list[str]:
    """Convert a submodule diff to simplepatch format lines."""
    lines: list[str] = []

    # Add a comment indicating this is a submodule change
    lines.append(f'# Submodule {submodule.path} ({submodule.old_commit}..{submodule.new_commit})\n')

    # Convert each file diff within the submodule
    for diff in submodule.diffs:
        # Prepend the submodule path to file paths
        submodule_lines = _convert_file_diff_to_simplepatch(diff, path_prefix=submodule.path + '/')
        lines.extend(submodule_lines)

    return lines


def _convert_file_diff_to_simplepatch(diff: GitFileDiff, path_prefix: str = '') -> list[str]:
    """Convert a single file diff to simplepatch format lines.

    Args:
        diff: The file diff to convert
        path_prefix: Optional prefix to prepend to file paths (for submodules)
    """
    lines: list[str] = []

    # Handle different types of file operations
    if diff.is_rename and not diff.hunks:
        # Pure rename without content changes
        old_path = path_prefix + (diff.old_path or '')
        new_path = path_prefix + (diff.new_path or '')
        lines.append(f'!{old_path} -> {new_path}\n')
        return lines

    if diff.is_new_file:
        # File creation
        new_path = path_prefix + (diff.new_path or '')
        lines.append(f'!-> {new_path}\n')
        # Add content from hunks
        for hunk in diff.hunks:
            lines.extend(_convert_hunk_lines_for_create(hunk))
        return lines

    if diff.is_deleted_file:
        # File deletion
        old_path = path_prefix + (diff.old_path or '')
        lines.append(f'!{old_path} ->\n')
        return lines

    if diff.is_binary:
        # Binary files - we can't convert these meaningfully
        # Just add a comment
        path = path_prefix + (diff.new_path or diff.old_path or '')
        lines.append(f'# Binary file: {path}\n')
        return lines

    # Handle mode changes
    if diff.old_mode and diff.new_mode and diff.old_mode != diff.new_mode:
        path = path_prefix + (diff.new_path or diff.old_path or '')
        # Convert mode strings to octal integers for display
        old_mode_int = int(diff.old_mode, 8) & 0o777
        new_mode_int = int(diff.new_mode, 8) & 0o777
        lines.append(f'!{path} %{old_mode_int:03o}->{new_mode_int:03o}\n')

    # Regular file edit with hunks
    if diff.hunks:
        path = path_prefix + (diff.new_path or diff.old_path or '')

        # Handle rename with changes
        if diff.is_rename and diff.old_path and diff.new_path and diff.old_path != diff.new_path:
            old_path = path_prefix + diff.old_path
            new_path = path_prefix + diff.new_path
            lines.append(f'!{old_path} -> {new_path}\n')

        for hunk in diff.hunks:
            # Add header with line hint
            lines.append(f'!{path} @{hunk.old_start}\n')
            lines.extend(_convert_hunk_lines(hunk))

    return lines


def _convert_hunk_lines(hunk: GitHunk) -> list[str]:
    """Convert hunk lines to simplepatch format."""
    lines: list[str] = []
    hunk_lines = hunk.lines
    i = 0

    while i < len(hunk_lines):
        line = hunk_lines[i]
        # Check if next line is a no-newline marker
        no_newline = i + 1 < len(hunk_lines) and isinstance(hunk_lines[i + 1], GitNoNewlineMarker)

        if isinstance(line, GitContextLine):
            lines.append(_format_simplepatch_line('=', line.content, no_newline))
        elif isinstance(line, GitAddedLine):
            lines.append(_format_simplepatch_line('+', line.content, no_newline))
        elif isinstance(line, GitRemovedLine):
            lines.append(_format_simplepatch_line('-', line.content, no_newline))
        elif isinstance(line, GitNoNewlineMarker):
            # Skip, handled above
            pass

        i += 1

    return lines


def _convert_hunk_lines_for_create(hunk: GitHunk) -> list[str]:
    """Convert hunk lines for file creation (only added lines)."""
    lines: list[str] = []
    hunk_lines = hunk.lines
    i = 0

    while i < len(hunk_lines):
        line = hunk_lines[i]
        # Check if next line is a no-newline marker
        no_newline = i + 1 < len(hunk_lines) and isinstance(hunk_lines[i + 1], GitNoNewlineMarker)

        if isinstance(line, GitAddedLine):
            lines.append(_format_simplepatch_line('+', line.content, no_newline))
        elif isinstance(line, GitNoNewlineMarker):
            # Skip, handled above
            pass

        i += 1

    return lines


def convert_from_git(git_text: str) -> str:
    """Convert git diff text to SimplePatch format.

    Args:
        git_text: Git unified diff format text

    Returns:
        SimplePatch format string
    """
    git_patch = parse_git_patch(git_text)
    return convert_git_to_simplepatch(git_patch)


def _unescape_simplepatch_content(content: str) -> tuple[str, bool]:
    """Unescape simplepatch content and detect no-newline marker.

    Returns:
        Tuple of (unescaped content, has_no_newline_marker)
    """
    result = []
    no_newline = False
    i = 0

    while i < len(content):
        if content[i] == '^':
            i += 1
            if i >= len(content):
                break
            next_char = content[i]
            if next_char == '0':
                pass  # Remove ^0 marker
            elif next_char == 'r':
                result.append('\r')
            elif next_char == 't':
                result.append('\t')
            elif next_char == 'x':
                no_newline = True
            elif next_char == '^':
                result.append('^')
        else:
            result.append(content[i])
        i += 1

    return ''.join(result), no_newline


def convert_simplepatch_to_git(patch: PatchFile) -> str:
    """Convert a PatchFile object to git diff format string.

    Args:
        patch: Parsed simplepatch object

    Returns:
        Git unified diff format string
    """
    lines: list[str] = []

    lines.append('From 0000000\n')
    lines.append('From: unknown author <noname@example.com>\n')
    lines.append('Date: Mon, 01 Jan 1970 00:00:00 +0000\n')
    lines.append('Subject: <subject>\n')

    for operation in patch.chunks:
        lines.extend(_convert_operation_to_git(operation))

    return ''.join(lines)


def _convert_operation_to_git(
    operation: EditOperation | CreateOperation | DeleteOperation | RenameOperation | ChmodOperation,
) -> list[str]:
    """Convert a single operation to git diff format lines."""
    lines: list[str] = []

    if isinstance(operation, CreateOperation):
        path = operation.path
        lines.append(f'diff --git a/{path} b/{path}\n')
        lines.append('new file mode 100644\n')
        lines.append('index 0000000..0000000\n')
        lines.append('--- /dev/null\n')
        lines.append(f'+++ b/{path}\n')

        # Convert lines to git format
        added_lines = [line for line in operation.lines if isinstance(line, AddedLine)]
        if added_lines:
            lines.append(f'@@ -0,0 +1,{len(added_lines)} @@\n')
            for i, line in enumerate(added_lines):
                content = line.content
                # Remove trailing newline for git format
                if content.endswith('\n'):
                    content = content[:-1]
                    lines.append(f'+{content}\n')
                else:
                    # No newline at end of file
                    lines.append(f'+{content}\n')
                    if i == len(added_lines) - 1:
                        lines.append('\\ No newline at end of file\n')

    elif isinstance(operation, DeleteOperation):
        path = operation.path
        lines.append(f'diff --git a/{path} b/{path}\n')
        lines.append('deleted file mode 100644\n')
        lines.append('index 0000000..0000000\n')
        lines.append(f'--- a/{path}\n')
        lines.append('+++ /dev/null\n')
        # Note: We don't have the original content, so we can't generate the hunk
        # This is a limitation - we'd need the original file content

    elif isinstance(operation, RenameOperation):
        old_path = operation.old_path
        new_path = operation.new_path
        lines.append(f'diff --git a/{old_path} b/{new_path}\n')
        lines.append('similarity index 100%\n')
        lines.append(f'rename from {old_path}\n')
        lines.append(f'rename to {new_path}\n')

    elif isinstance(operation, ChmodOperation):
        path = operation.path
        old_mode = operation.old_perms
        new_mode = operation.new_perms
        lines.append(f'diff --git a/{path} b/{path}\n')
        lines.append(f'old mode 100{old_mode:03o}\n')
        lines.append(f'new mode 100{new_mode:03o}\n')

    elif isinstance(operation, EditOperation):
        path = operation.path
        lines.append(f'diff --git a/{path} b/{path}\n')
        lines.append('index 0000000..0000000 100644\n')
        lines.append(f'--- a/{path}\n')
        lines.append(f'+++ b/{path}\n')

        # Calculate hunk header
        old_start = operation.line_hint[0] or 1
        old_count = 0
        new_count = 0

        hunk_lines: list[str] = []
        last_line_no_newline = False

        for line in operation.lines:
            if isinstance(line, ContextLine):
                content = line.content
                if content.endswith('\n'):
                    content = content[:-1]
                    hunk_lines.append(f' {content}\n')
                else:
                    hunk_lines.append(f' {content}\n')
                    last_line_no_newline = True
                old_count += 1
                new_count += 1
            elif isinstance(line, RemovedLine):
                content = line.content
                if content.endswith('\n'):
                    content = content[:-1]
                    hunk_lines.append(f'-{content}\n')
                else:
                    hunk_lines.append(f'-{content}\n')
                    last_line_no_newline = True
                old_count += 1
            elif isinstance(line, AddedLine):
                content = line.content
                if content.endswith('\n'):
                    content = content[:-1]
                    hunk_lines.append(f'+{content}\n')
                else:
                    hunk_lines.append(f'+{content}\n')
                    last_line_no_newline = True
                new_count += 1

        if last_line_no_newline:
            hunk_lines.append('\\ No newline at end of file\n')

        # Add hunk header
        new_start = old_start  # Simplified - in reality this might differ
        lines.append(f'@@ -{old_start},{old_count} +{new_start},{new_count} @@\n')
        lines.extend(hunk_lines)

    return lines


def convert_to_git(patch: PatchFile) -> str:
    """Convert SimplePatch to git diff format.

    Args:
        patch: Parsed simplepatch object

    Returns:
        Git unified diff format string
    """
    return convert_simplepatch_to_git(patch)
