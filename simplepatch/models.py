from typing import Self
from dataclasses import dataclass, field
from enum import Enum


type PathSpec = str


# =============================================================================
# Git Patch Models
# =============================================================================


@dataclass
class GitContextLine:
    """A context line in a git diff (unchanged line)."""

    content: str


@dataclass
class GitAddedLine:
    """An added line in a git diff."""

    content: str


@dataclass
class GitRemovedLine:
    """A removed line in a git diff."""

    content: str


@dataclass
class GitNoNewlineMarker:
    """Marker indicating no newline at end of file."""

    pass


type GitHunkLine = GitContextLine | GitAddedLine | GitRemovedLine | GitNoNewlineMarker


@dataclass
class GitHunk:
    """A hunk in a git diff, representing a contiguous change."""

    old_start: int
    old_count: int
    new_start: int
    new_count: int
    context: str  # Optional context after @@ line
    lines: list[GitHunkLine] = field(default_factory=list)


@dataclass
class GitBinaryPatchData:
    """Data for a single binary patch section (literal or delta)."""

    patch_type: str  # 'literal' or 'delta'
    size: int
    data: str  # Base85-encoded data


@dataclass
class GitBinaryPatch:
    """A git binary patch with forward and optional reverse patches."""

    forward: GitBinaryPatchData
    reverse: GitBinaryPatchData | None = None


@dataclass
class GitFileDiff:
    """A single file diff in a git patch."""

    old_path: str | None  # None for new files
    new_path: str | None  # None for deleted files
    old_mode: str | None
    new_mode: str | None
    old_index: str | None
    new_index: str | None
    is_new_file: bool = False
    is_deleted_file: bool = False
    is_rename: bool = False
    is_binary: bool = False
    similarity_index: int | None = None
    hunks: list[GitHunk] = field(default_factory=list)
    binary_patch: GitBinaryPatch | None = None


@dataclass
class GitCommitHeader:
    """Optional commit header information."""

    commit_hash: str | None = None
    author: str | None = None
    date: str | None = None
    subject: str | None = None


@dataclass
class GitSubmoduleDiff:
    """A submodule diff containing changes within a git submodule."""

    path: str
    old_commit: str
    new_commit: str
    diffs: list[GitFileDiff] = field(default_factory=list)


@dataclass
class GitPatch:
    """A complete git patch, potentially containing multiple file diffs."""

    header: GitCommitHeader | None = None
    diffs: list[GitFileDiff] = field(default_factory=list)
    submodules: list[GitSubmoduleDiff] = field(default_factory=list)
    preamble: str | None = None  # Text before the first diff (commit message, etc.)


# =============================================================================
# SimplePatch Models
# =============================================================================


@dataclass
class TextLine:
    content: str

    @classmethod
    def from_raw_content(cls, content: str) -> Self:
        # ^0 - removed completely (for trailing space preservation)
        # ^r - carriage return (CRLF line ending)
        # ^t - tab character
        # ^x - no newline at end
        # ^^ - literal ^ character
        result = ''

        no_newline_marker = False
        i = 0
        while i < len(content):
            if content[i] == '^':
                i += 1
                if i >= len(content):
                    raise ValueError('Unexpected end of string')

                next_char = content[i]
                match next_char:
                    case '0':
                        pass
                    case 'r':
                        result += '\r'
                    case 't':
                        result += '\t'
                    case 'x':
                        no_newline_marker = True
                    case '^':
                        result += '^'
                    case _:
                        raise ValueError(f'Unknown escape sequence: {next_char}')

            else:
                result += content[i]

            i += 1
        if not no_newline_marker:
            result += '\n'

        return cls(content=result)


@dataclass
class ContextLine(TextLine):
    pass


@dataclass
class RemovedLine(TextLine):
    pass


@dataclass
class AddedLine(TextLine):
    pass


class BinaryLineEncoding(Enum):
    Z85 = 'z85'


@dataclass
class BinaryLine:
    encoding: BinaryLineEncoding
    data: str


type HunkLine = ContextLine | RemovedLine | AddedLine | BinaryLine


@dataclass
class EditOperation:
    path: PathSpec
    line_hint: tuple[int | None, int | None]
    lines: list[HunkLine] = field(default_factory=list)


@dataclass
class CreateOperation:
    path: PathSpec
    lines: list[HunkLine] = field(default_factory=list)


@dataclass
class DeleteOperation:
    path: PathSpec


@dataclass
class RenameOperation:
    old_path: PathSpec
    new_path: PathSpec


@dataclass
class ChmodOperation:
    path: PathSpec
    old_perms: int
    new_perms: int


type Operation = (
    EditOperation | CreateOperation | DeleteOperation | RenameOperation | ChmodOperation
)


@dataclass
class PatchFile:
    chunks: list[Operation]
