from pathlib import Path
from typing import Any, cast

import lark
from lark import Lark, Token, Transformer, v_args

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
    BinaryLineEncoding,
    Operation,
    PathSpec,
    # Git patch models
    GitContextLine,
    GitAddedLine,
    GitRemovedLine,
    GitNoNewlineMarker,
    GitHunkLine,
    GitHunk,
    GitFileDiff,
    GitCommitHeader,
    GitPatch,
    GitSubmoduleDiff,
    GitBinaryPatchData,
    GitBinaryPatch,
)


def _patch_lark() -> None:
    # fixed here: https://github.com/lark-parser/lark/pull/1575
    # TODO: remove this after upgrading lark

    # original _format_expected prints expected tokens in random order, so sort options here:
    def _format_expected(self, expected):
        return _format_expected_old(self, sorted(expected))

    _format_expected_old = lark.UnexpectedInput._format_expected
    lark.UnexpectedInput._format_expected = _format_expected  # type: ignore[invalid-assignment]


_patch_lark()

SIMPLEPATCH_GRAMMAR_FILE = Path(__file__).parent / 'simplepatch.lark'
with open(SIMPLEPATCH_GRAMMAR_FILE) as f:
    SIMPLEPATCH_GRAMMAR = f.read()


GIT_GRAMMAR_FILE = Path(__file__).parent / 'git.lark'
with open(GIT_GRAMMAR_FILE) as f:
    GIT_GRAMMAR = f.read()


class SimplePatchTransformer(Transformer):
    def path(self, items: list[Token]) -> PathSpec:
        return ''.join([str(item) for item in items])

    def NUMBER(self, s: Token) -> int:
        return int(str(s))

    def OCTAL_MODE(self, s: Token) -> int:
        return int(str(s), 8)

    def line_hint(self, items: list[int]) -> tuple[int, int | None]:
        start = items[0]
        end = items[1] if len(items) > 1 else None
        return start, end

    @v_args(inline=True)
    def edit_op(
        self,
        path: PathSpec,
        line_hint: tuple[int | None, int | None] | None = None,
    ) -> EditOperation:
        return EditOperation(path=path, line_hint=line_hint or (None, None))

    @v_args(inline=True)
    def create_op(self, path: PathSpec) -> CreateOperation:
        return CreateOperation(path=path)

    @v_args(inline=True)
    def delete_op(self, path: PathSpec) -> DeleteOperation:
        return DeleteOperation(path=path)

    @v_args(inline=True)
    def rename_op(self, old_filepath: PathSpec, new_filepath: PathSpec) -> RenameOperation:
        return RenameOperation(old_path=old_filepath, new_path=new_filepath)

    @v_args(inline=True)
    def chmod_op(self, path: PathSpec, old_perms: int, new_perms: int) -> ChmodOperation:
        return ChmodOperation(path=path, old_perms=old_perms, new_perms=new_perms)

    @v_args(inline=True)
    def context_line(self, content: Token | None = None) -> ContextLine:
        data = str(content) if content else ''
        return ContextLine.from_raw_content(data)

    @v_args(inline=True)
    def removed_line(self, content: Token | None = None) -> RemovedLine:
        data = str(content) if content else ''
        return RemovedLine.from_raw_content(data)

    @v_args(inline=True)
    def added_line(self, content: Token | None = None) -> AddedLine:
        data = str(content) if content else ''
        return AddedLine.from_raw_content(data)

    @v_args(inline=True)
    def binary_line(self, content: Token | None = None) -> BinaryLine:
        data = str(content) if content else ''
        return BinaryLine(encoding=BinaryLineEncoding.Z85, data=data)

    @v_args(inline=True)
    def comment_line(self, content: Token | None = None) -> None:
        return None

    @v_args(inline=True)
    def empty_line(self) -> None:
        return None

    def chunk(self, items: list[Any]) -> Operation:
        operation: Operation
        hunk_lines: list[HunkLine | None]
        operation, *hunk_lines = items

        operation.lines = [line for line in hunk_lines if line is not None]

        return operation

    def patch_file(self, items: list[Operation | None]) -> PatchFile:
        return PatchFile(chunks=[operation for operation in items if operation is not None])


def parse_patch(patch_text: str) -> PatchFile:
    parser = Lark(SIMPLEPATCH_GRAMMAR, parser='lalr', transformer=SimplePatchTransformer())

    result = parser.parse(patch_text)
    return cast(PatchFile, result)


class GitTransformer(Transformer):
    """Transformer for git unified diff format."""

    # Terminals
    def NUMBER(self, s: Token) -> int:
        return int(str(s))

    def SIGN(self, s: Token) -> str:
        return str(s)

    def FILE_MODE(self, s: Token) -> str:
        return str(s)

    def COMMIT_HASH(self, s: Token) -> str:
        return str(s)

    def INDEX_HASH(self, s: Token) -> str:
        return str(s)

    def PERCENTAGE(self, s: Token) -> int:
        return int(str(s))

    def FILE_PATH(self, s: Token) -> str:
        return str(s)

    def LINE_CONTENT(self, s: Token) -> str:
        return str(s)

    def REST_OF_LINE(self, s: Token) -> str:
        return str(s)

    def HUNK_CONTEXT(self, s: Token) -> str:
        return str(s)

    def GIT_PATH_PREFIX(self, s: Token) -> str:
        return str(s)

    def SUBMODULE_RANGE(self, s: Token) -> str:
        return str(s)

    # Git path
    @v_args(inline=True)
    def git_path(self, prefix: str, path: str) -> str:
        # Return just the path without the a/ or b/ prefix
        return path

    @v_args(inline=True)
    def dev_null(self) -> None:
        return None

    @v_args(inline=True)
    def file_path_spec(self, path: str | None) -> str | None:
        return path

    # Commit header
    @v_args(inline=True)
    def from_line(self, commit_hash: str, rest: str) -> str:
        return commit_hash

    @v_args(inline=True)
    def author_line(self, author: str) -> str:
        return author

    @v_args(inline=True)
    def date_line(self, date: str) -> str:
        return date

    @v_args(inline=True)
    def subject_line(self, subject: str) -> str:
        return subject

    def commit_header(self, items: list[Any]) -> GitCommitHeader:
        commit_hash = items[0] if len(items) > 0 else None
        author = items[1] if len(items) > 1 else None
        date = items[2] if len(items) > 2 else None
        subject = items[3] if len(items) > 3 else None
        return GitCommitHeader(
            commit_hash=commit_hash,
            author=author,
            date=date,
            subject=subject,
        )

    # Extended header lines
    @v_args(inline=True)
    def index_line(self, old_hash: str, new_hash: str, mode: str | None = None) -> dict[str, Any]:
        return {'type': 'index', 'old_hash': old_hash, 'new_hash': new_hash, 'mode': mode}

    @v_args(inline=True)
    def old_mode_line(self, mode: str) -> dict[str, Any]:
        return {'type': 'old_mode', 'mode': mode}

    @v_args(inline=True)
    def new_mode_line(self, mode: str) -> dict[str, Any]:
        return {'type': 'new_mode', 'mode': mode}

    @v_args(inline=True)
    def deleted_file_mode_line(self, mode: str) -> dict[str, Any]:
        return {'type': 'deleted_file_mode', 'mode': mode}

    @v_args(inline=True)
    def new_file_mode_line(self, mode: str) -> dict[str, Any]:
        return {'type': 'new_file_mode', 'mode': mode}

    @v_args(inline=True)
    def similarity_index_line(self, percentage: int) -> dict[str, Any]:
        return {'type': 'similarity_index', 'percentage': percentage}

    @v_args(inline=True)
    def rename_from_line(self, path: str) -> dict[str, Any]:
        return {'type': 'rename_from', 'path': path}

    @v_args(inline=True)
    def rename_to_line(self, path: str) -> dict[str, Any]:
        return {'type': 'rename_to', 'path': path}

    def empty_content(self, items: list[Any]) -> None:
        return None

    # Git binary patch
    def BINARY_PATCH_TYPE(self, s: Token) -> str:
        return str(s)

    def BINARY_DATA_LINE(self, s: Token) -> str:
        return str(s)

    def binary_data_line(self, items: list[Any]) -> str:
        return items[0]

    def binary_patch_header(self, items: list[Any]) -> dict[str, Any]:
        patch_type = items[0]
        size = items[1]
        return {'type': patch_type, 'size': size}

    def binary_data_lines(self, items: list[str]) -> str:
        return '\n'.join(items)

    def binary_patch_data(self, items: list[Any]) -> GitBinaryPatchData:
        header = items[0]
        data = items[1] if len(items) > 1 else ''
        return GitBinaryPatchData(
            patch_type=header['type'],
            size=header['size'],
            data=data,
        )

    def git_binary_patch(self, items: list[GitBinaryPatchData]) -> GitBinaryPatch:
        forward = items[0]
        reverse = items[1] if len(items) > 1 else None
        return GitBinaryPatch(forward=forward, reverse=reverse)

    def text_diff(self, items: list[Any]) -> tuple[tuple[str | None, str | None], list[GitHunk]]:
        file_header_data = items[0]
        hunks_data = items[1] if len(items) > 1 else []
        return (file_header_data, hunks_data)

    # File header
    @v_args(inline=True)
    def old_file_line(self, path: str | None) -> str | None:
        return path

    @v_args(inline=True)
    def new_file_line(self, path: str | None) -> str | None:
        return path

    @v_args(inline=True)
    def file_header(
        self, old_path: str | None, new_path: str | None
    ) -> tuple[str | None, str | None]:
        return (old_path, new_path)

    # Diff header
    @v_args(inline=True)
    def diff_header(self, old_path: str, new_path: str) -> tuple[str, str]:
        return (old_path, new_path)

    # Hunk range
    def hunk_range(self, items: list[Any]) -> tuple[int, int]:
        sign = items[0]
        start = items[1]
        count = items[2] if len(items) > 2 else 1
        return (start, count)

    # Hunk header
    def hunk_header(self, items: list[Any]) -> dict[str, Any]:
        old_range = items[0]
        new_range = items[1]
        context = items[2] if len(items) > 2 else ''
        return {
            'old_start': old_range[0],
            'old_count': old_range[1],
            'new_start': new_range[0],
            'new_count': new_range[1],
            'context': context.strip() if context else '',
        }

    # Hunk lines
    def context_line(self, items: list[Any]) -> GitContextLine:
        # items[0] is SPACE token, items[1] is optional LINE_CONTENT
        content = items[1] if len(items) > 1 else ''
        return GitContextLine(content=content or '')

    def added_line(self, items: list[Any]) -> GitAddedLine:
        # items[0] is PLUS token, items[1] is optional LINE_CONTENT
        content = items[1] if len(items) > 1 else ''
        return GitAddedLine(content=content or '')

    def removed_line(self, items: list[Any]) -> GitRemovedLine:
        # items[0] is MINUS token, items[1] is optional LINE_CONTENT
        content = items[1] if len(items) > 1 else ''
        return GitRemovedLine(content=content or '')

    @v_args(inline=True)
    def no_newline_line(self) -> GitNoNewlineMarker:
        return GitNoNewlineMarker()

    def hunk_lines(self, items: list[GitHunkLine]) -> list[GitHunkLine]:
        return items

    # Hunk
    def hunk(self, items: list[Any]) -> GitHunk:
        header = items[0]
        lines = items[1] if len(items) > 1 else []
        return GitHunk(
            old_start=header['old_start'],
            old_count=header['old_count'],
            new_start=header['new_start'],
            new_count=header['new_count'],
            context=header['context'],
            lines=lines,
        )

    def hunks(self, items: list[GitHunk]) -> list[GitHunk]:
        return items

    # File diff
    def file_diff(self, items: list[Any]) -> GitFileDiff:
        diff_header = items[0]
        old_path_from_header, new_path_from_header = diff_header

        # Process extended headers and file content
        extended_headers: list[dict[str, Any]] = []
        file_header_data: tuple[str | None, str | None] | None = None
        hunks_data: list[GitHunk] = []
        binary_patch_data: GitBinaryPatch | None = None

        for item in items[1:]:
            if isinstance(item, dict):
                extended_headers.append(item)
            elif isinstance(item, GitBinaryPatch):
                binary_patch_data = item
            elif isinstance(item, tuple) and len(item) == 2:
                # Could be text_diff result (file_header, hunks) or just file_header
                first, second = item
                if isinstance(first, tuple) and isinstance(second, list):
                    # text_diff result: ((old_path, new_path), hunks)
                    file_header_data = first
                    hunks_data = second
                elif isinstance(first, str) or first is None:
                    # Just file_header: (old_path, new_path)
                    file_header_data = item
            elif isinstance(item, list):
                hunks_data = item
            elif item is None:
                # empty_content
                pass

        # Extract information from extended headers
        old_mode: str | None = None
        new_mode: str | None = None
        old_index: str | None = None
        new_index: str | None = None
        is_new_file = False
        is_deleted_file = False
        is_rename = False
        is_binary = binary_patch_data is not None
        similarity_index: int | None = None

        for header in extended_headers:
            header_type = header.get('type')
            if header_type == 'index':
                old_index = header['old_hash']
                new_index = header['new_hash']
                if header.get('mode'):
                    new_mode = header['mode']
            elif header_type == 'old_mode':
                old_mode = header['mode']
            elif header_type == 'new_mode':
                new_mode = header['mode']
            elif header_type == 'deleted_file_mode':
                is_deleted_file = True
                old_mode = header['mode']
            elif header_type == 'new_file_mode':
                is_new_file = True
                new_mode = header['mode']
            elif header_type == 'similarity_index':
                similarity_index = header['percentage']
            elif header_type == 'rename_from':
                is_rename = True
            elif header_type == 'rename_to':
                is_rename = True

        # Get paths from file header if available
        old_path = file_header_data[0] if file_header_data else old_path_from_header
        new_path = file_header_data[1] if file_header_data else new_path_from_header

        return GitFileDiff(
            old_path=old_path,
            new_path=new_path,
            old_mode=old_mode,
            new_mode=new_mode,
            old_index=old_index,
            new_index=new_index,
            is_new_file=is_new_file,
            is_deleted_file=is_deleted_file,
            is_rename=is_rename,
            is_binary=is_binary,
            similarity_index=similarity_index,
            hunks=hunks_data,
            binary_patch=binary_patch_data,
        )

    # Submodule diff
    def submodule_header(self, items: list[Any]) -> dict[str, str]:
        path = items[0]
        range_str = items[1]
        # Parse the range "old_commit..new_commit"
        old_commit, new_commit = range_str.split('..')
        return {'path': path, 'old_commit': old_commit, 'new_commit': new_commit}

    def submodule_diff(self, items: list[Any]) -> GitSubmoduleDiff:
        header = items[0]
        diffs = [item for item in items[1:] if isinstance(item, GitFileDiff)]
        return GitSubmoduleDiff(
            path=header['path'],
            old_commit=header['old_commit'],
            new_commit=header['new_commit'],
            diffs=diffs,
        )

    # Git patch
    def git_patch(self, items: list[Any]) -> GitPatch:
        header: GitCommitHeader | None = None
        diffs: list[GitFileDiff] = []
        submodules: list[GitSubmoduleDiff] = []

        for item in items:
            if isinstance(item, GitCommitHeader):
                header = item
            elif isinstance(item, GitFileDiff):
                diffs.append(item)
            elif isinstance(item, GitSubmoduleDiff):
                submodules.append(item)

        return GitPatch(header=header, diffs=diffs, submodules=submodules)


def _preprocess_git_patch(patch_text: str) -> tuple[str, str | None]:
    """Preprocess git patch text to handle format-patch output.

    Git format-patch output includes additional content between the commit header
    and the first diff (like commit message body, ticket references, etc.).
    This function extracts the preamble and returns it separately.

    Returns:
        Tuple of (diff_text, preamble) where preamble is the text before the first diff.
    """
    # Find the first 'diff --git' line
    diff_marker = '\ndiff --git '
    diff_pos = patch_text.find(diff_marker)

    if diff_pos == -1:
        # Check if it starts with 'diff --git'
        if patch_text.startswith('diff --git '):
            return patch_text, None
        # No diff found, return as-is (will likely fail parsing)
        return patch_text, None

    # Extract preamble (everything before the first diff)
    preamble = patch_text[:diff_pos].strip() if diff_pos > 0 else None

    # Return from the first diff onwards (include the newline before it)
    diff_text = patch_text[diff_pos + 1 :]  # +1 to skip the leading newline

    return diff_text, preamble


def parse_git_patch(patch_text: str) -> GitPatch:
    # Preprocess to handle format-patch output with extra content
    diff_text, preamble = _preprocess_git_patch(patch_text)

    parser = Lark(GIT_GRAMMAR, parser='lalr', transformer=GitTransformer())

    result = parser.parse(diff_text)
    git_patch = cast(GitPatch, result)

    # Set the preamble if present
    if preamble:
        git_patch.preamble = preamble

    return git_patch
