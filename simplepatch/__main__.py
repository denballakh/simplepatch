import argparse
import sys
from pathlib import Path
from typing import Never

from . import __version__
from .parser import parse_patch
from .applier import apply_patch
from .models import PatchFile
from .converter import convert_from_git, convert_to_git


class HelpfulArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that prints full help on error."""

    def error(self, message: str) -> Never:
        self.print_help(sys.stderr)
        sys.stderr.write(f'\nerror: {message}\n')
        sys.exit(2)


def main() -> None:
    parser = HelpfulArgumentParser(
        prog='simplepatch',
        description='SimplePatch - Human-friendly patch format and tool',
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
    )

    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
    )

    # Apply command
    apply_parser = subparsers.add_parser(
        'apply',
        help='Apply one or more patches to a directory',
    )
    apply_parser.add_argument(
        'patches',
        nargs='+',
        help='Patch files to apply (use "-" for stdin)',
    )
    apply_parser.add_argument(
        'target_dir',
        nargs='?',
        default='.',
        help='Target directory (default: current directory)',
    )

    # Convert command
    convert_parser = subparsers.add_parser(
        'convert',
        help='Convert between patch formats',
    )
    convert_parser.add_argument(
        '--from',
        dest='from_format',
        choices=['git', 'simplepatch'],
        help='Source format (auto-detected if omitted)',
    )
    convert_parser.add_argument(
        '--to',
        dest='to_format',
        choices=['git', 'simplepatch'],
        default='simplepatch',
        help='Target format (default: simplepatch)',
    )
    convert_parser.add_argument(
        'input_file',
        nargs='?',
        help='Input file (default: stdin)',
    )

    # Diff command
    diff_parser = subparsers.add_parser(
        'diff',
        help='Generate a simplepatch from two files',
    )
    diff_parser.add_argument(
        'old_file',
        help='Original file',
    )
    diff_parser.add_argument(
        'new_file',
        help='Modified file',
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)  # Exit with error code when no command provided

    try:
        if args.command == 'apply':
            cmd_apply(args)
        elif args.command == 'convert':
            cmd_convert(args)
        elif args.command == 'diff':
            cmd_diff(args)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


def cmd_apply(args: argparse.Namespace) -> None:
    """Apply patches to a directory."""
    patches = list(args.patches)
    target_dir = Path(args.target_dir)

    # Handle case where last patch argument is actually the target directory
    # This supports: simplepatch apply patch1.patch patch2.patch /target/dir
    if len(patches) > 1 and patches[-1] != '-':
        last_path = Path(patches[-1])
        if last_path.is_dir():
            target_dir = last_path
            patches = patches[:-1]

    # Read and apply each patch
    for patch_file in patches:
        if patch_file == '-':
            # Read from stdin
            patch_text = sys.stdin.read()
        else:
            patch_path = Path(patch_file)
            if not patch_path.exists():
                raise FileNotFoundError(f'Patch file not found: {patch_file}')
            patch_text = patch_path.read_text(encoding='utf-8')

        # Parse the patch
        patch = parse_patch(patch_text)

        # Apply the patch
        apply_patch(patch, base_dir=target_dir)

        print(f'Applied {patch_file} to {target_dir}')


def cmd_convert(args: argparse.Namespace) -> None:
    """Convert between patch formats."""
    # Read input
    if args.input_file:
        if args.input_file == '-':
            input_text = sys.stdin.read()
        else:
            input_path = Path(args.input_file)
            if not input_path.exists():
                raise FileNotFoundError(f'Input file not found: {args.input_file}')
            input_text = input_path.read_text(encoding='utf-8')
    else:
        input_text = sys.stdin.read()

    # Auto-detect format if not specified
    from_format = args.from_format
    if not from_format:
        # Simple heuristic: if it starts with '!', it's simplepatch
        if input_text.lstrip().startswith('!') or input_text.lstrip().startswith('#'):
            from_format = 'simplepatch'
        else:
            from_format = 'git'

    # Convert
    if from_format == 'simplepatch' and args.to_format == 'git':
        # Parse simplepatch and convert to git
        patch = parse_patch(input_text)
        output = convert_to_git(patch)
        print(output)
    elif from_format == 'git' and args.to_format == 'simplepatch':
        # Parse git and convert to simplepatch
        output = convert_from_git(input_text)
        print(output)
    elif from_format == args.to_format:
        # No conversion needed
        print(input_text)
    else:
        raise ValueError(f'Unsupported conversion: {from_format} -> {args.to_format}')


def cmd_diff(args: argparse.Namespace) -> None:
    """Generate a simplepatch from two files."""
    old_path = Path(args.old_file)
    if not old_path.exists():
        raise FileNotFoundError(f'File not found: {args.old_file}')
    old_content = old_path.read_text(encoding='utf-8')

    new_path = Path(args.new_file)
    if not new_path.exists():
        raise FileNotFoundError(f'File not found: {args.new_file}')
    new_content = new_path.read_text(encoding='utf-8')

    # Generate simplepatch
    patch = generate_simplepatch(old_path, old_content, new_content)
    print(patch)


def generate_simplepatch(filepath: Path, old_content: str, new_content: str) -> str:
    """Generate a simplepatch from two file contents."""
    # TODO: Implement diff generation
    raise NotImplementedError('Diff generation not yet implemented')


if __name__ == '__main__':
    main()
