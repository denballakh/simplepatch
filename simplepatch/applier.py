from typing import assert_never
import re
from pathlib import Path

from .models import (
    AddedLine,
    BinaryLine,
    ChmodOperation,
    ContextLine,
    CreateOperation,
    DeleteOperation,
    EditOperation,
    HunkLine,
    PatchFile,
    RemovedLine,
    RenameOperation,
    Operation,
    PathSpec,
)


def is_dir(path: PathSpec) -> bool:
    return path.endswith('/')


class PatchApplicationError(Exception):
    """Base exception for patch application errors."""


class AmbiguousMatchError(PatchApplicationError):
    """Raised when multiple matches are found and cannot be disambiguated."""


class NoMatchFoundError(PatchApplicationError):
    """Raised when no match is found for the patch."""


def apply_patch(
    patch: PatchFile,
    base_dir: Path | None = None,
) -> None:
    """Apply a patch to the filesystem.

    Args:
        patch: The parsed patch file to apply
        base_dir: Base directory for relative paths (default: current directory)

    Raises:
        FileNotFoundError: If a required file doesn't exist
        FileExistsError: If trying to create a file that already exists
        ValueError: If the patch cannot be applied (ambiguous match, etc.)
    """
    if base_dir is None:
        base_dir = Path.cwd()

    for chunk in patch.chunks:
        apply_chunk(chunk, base_dir)


def apply_chunk(operation: Operation, base_dir: Path) -> None:
    """Apply a single patch chunk."""
    if isinstance(operation, CreateOperation):
        apply_create(operation, base_dir)
    elif isinstance(operation, DeleteOperation):
        apply_delete(operation, base_dir)
    elif isinstance(operation, RenameOperation):
        apply_rename(operation, base_dir)
    elif isinstance(operation, ChmodOperation):
        apply_chmod(operation, base_dir)
    elif isinstance(operation, EditOperation):
        apply_edit(operation, base_dir)
    else:
        assert_never(operation)


def apply_create(operation: CreateOperation, base_dir: Path) -> None:
    """Create a new file or directory."""
    target_path = base_dir / operation.path

    if target_path.exists():
        raise FileExistsError(str(operation.path))

    # Check if it's a directory
    if is_dir(operation.path):
        target_path.mkdir(parents=True, exist_ok=False)
        target_path.chmod(0o755)  # Default for directories
    else:
        # Create parent directories if needed
        if target_path.parent != base_dir and not target_path.parent.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if we have binary content
        has_binary = any(isinstance(line, BinaryLine) for line in operation.lines)

        if has_binary:
            # Decode binary content
            binary_lines = [line for line in operation.lines if isinstance(line, BinaryLine)]
            content = decode_binary_lines(binary_lines)
            target_path.write_bytes(content)
        else:
            # Text content
            if operation.lines:
                parts = []
                for line in operation.lines:
                    if isinstance(line, AddedLine):
                        parts.append(line.content)
                content = ''.join(parts)
            else:
                content = ''
            target_path.write_text(content, encoding='utf-8')

        # Set default permissions for files
        target_path.chmod(0o644)


def apply_delete(operation: DeleteOperation, base_dir: Path) -> None:
    """Delete a file or directory."""
    target_path = base_dir / operation.path

    if not target_path.exists():
        raise FileNotFoundError(str(operation.path))

    if target_path.is_dir():
        target_path.rmdir()  # Only removes empty directories
    else:
        target_path.unlink()


def apply_rename(operation: RenameOperation, base_dir: Path) -> None:
    """Rename or move a file or directory."""
    old_path = base_dir / operation.old_path
    new_path = base_dir / operation.new_path

    if not old_path.exists():
        raise FileNotFoundError(str(operation.old_path))

    if new_path.exists():
        raise FileExistsError(str(operation.new_path))

    # Create parent directory for new path if needed
    new_path.parent.mkdir(parents=True, exist_ok=True)

    old_path.rename(new_path)


def apply_chmod(operation: ChmodOperation, base_dir: Path) -> None:
    """Change file permissions."""
    target_path = base_dir / operation.path

    if not target_path.exists():
        raise FileNotFoundError(str(operation.path))

    if (perms := target_path.stat().st_mode & 0o777) != operation.old_perms:
        raise OSError(f'expected permissions {operation.old_perms:#o}, but got {perms:#o}')

    target_path.chmod(operation.new_perms)


def apply_edit(operation: EditOperation, base_dir: Path) -> None:
    """Apply an edit operation to a file."""
    target_path = base_dir / operation.path

    if not target_path.exists():
        raise FileNotFoundError(str(operation.path))

    # Read the file
    content = target_path.read_text(encoding='utf-8')
    file_lines = content.splitlines(keepends=True)

    patch_lines = operation.lines

    if not patch_lines:
        # Nothing to do
        return

    # Extract the pattern to match (context + removed lines)
    match_pattern: list[ContextLine | RemovedLine] = [
        line for line in patch_lines if isinstance(line, ContextLine | RemovedLine)
    ]

    if not match_pattern:
        # Only added lines - need to find position based on context
        # For now, append at end if no context
        for line in patch_lines:
            if isinstance(line, AddedLine):
                file_lines.append(line.content)
        new_content = ''.join(file_lines)
        target_path.write_text(new_content, encoding='utf-8')
        return

    # Find all candidate positions
    candidates = find_pattern_matches(file_lines, match_pattern, normalize_line)

    if len(candidates) == 0:
        # Try fuzzy matching
        candidates = find_pattern_matches(file_lines, match_pattern, fuzzy_normalize_line)

    if len(candidates) == 0:
        raise NoMatchFoundError(
            f'Could not find match in {operation.path}\n'
            f'Looking for: {[line.content for line in match_pattern]}'
        )

    if len(candidates) > 1:
        if len(candidates) > 1:
            raise AmbiguousMatchError(
                f'Ambiguous match in {operation.path}\n'
                f'Found {len(candidates)} occurrences at lines: {candidates}\n'
                f'Add context lines to disambiguate.'
            )

    # Apply the patch at the found position
    match_start = candidates[0]

    # Build new content by applying the patch
    new_lines = []

    # Add lines before the match
    new_lines.extend(file_lines[:match_start])

    # Apply the patch: walk through patch_lines and file simultaneously
    file_idx = match_start
    for patch_line in patch_lines:
        if isinstance(patch_line, ContextLine):
            # Context line - keep the original file line
            if file_idx < len(file_lines):
                new_lines.append(file_lines[file_idx])
                file_idx += 1
        elif isinstance(patch_line, RemovedLine):
            # Removed line - skip the file line
            file_idx += 1
        elif isinstance(patch_line, AddedLine):
            # Added line - insert new content
            new_lines.append(patch_line.content)

    # Add remaining lines after the match
    new_lines.extend(file_lines[file_idx:])

    # Write back
    new_content = ''.join(new_lines)
    target_path.write_text(new_content, encoding='utf-8')


def find_pattern_matches(
    file_lines: list[str],
    pattern: list[ContextLine | RemovedLine],
    normalize_fn,
) -> list[int]:
    """Find all positions where the pattern (context + removed lines) matches.

    The pattern is a sequence of ContextLine and RemovedLine objects.
    Both context and removed lines must match the file content at the position.

    Returns list of line numbers (0-based) where the match starts.
    """
    if not pattern:
        return []

    pattern_len = len(pattern)
    candidates = []

    # Search through file
    for i in range(len(file_lines) - pattern_len + 1):
        # Check if all pattern lines match
        match = True
        for j, patch_line in enumerate(pattern):
            patch_content = normalize_fn(patch_line.content)
            file_content = normalize_fn(file_lines[i + j])
            if patch_content != file_content:
                match = False
                break

        if match:
            candidates.append(i)

    return candidates


def find_fuzzy_matches(
    file_lines: list[str],
    pattern: list[ContextLine | RemovedLine],
) -> list[int]:
    """Find matches allowing minor whitespace differences.

    Returns list of line numbers (0-based) where the match starts.
    """
    return find_pattern_matches(file_lines, pattern, fuzzy_normalize_line)


def disambiguate_with_hint(candidates: list[int], line_hint: int) -> list[int]:
    """Use line hint to prefer candidates near the hint.

    Returns candidates sorted by distance from hint, keeping only the closest.
    """
    # Convert to 0-based
    hint_line = line_hint - 1

    # Calculate distances
    distances = [(abs(candidate - hint_line), candidate) for candidate in candidates]
    distances.sort()

    # Return only the closest candidate
    if distances:
        return [distances[0][1]]

    return candidates


def normalize_line(line: str) -> str:
    """Normalize a line for exact matching (strip line endings)."""
    return line.rstrip('\r\n')


def fuzzy_normalize_line(line: str) -> str:
    """Normalize a line for fuzzy matching (normalize whitespace)."""
    # Strip line endings and normalize whitespace
    line = line.rstrip('\r\n')
    line = re.sub(r'\s+', ' ', line)
    return line.strip()


def decode_binary_lines(binary_lines: list) -> bytes:
    """Decode binary lines from base85 encoding."""
    # This is a placeholder - actual implementation would decode Z85 or Git base85
    # For now, just raise an error
    raise NotImplementedError('Binary file support not yet implemented')
