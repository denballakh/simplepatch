from typing import assert_never
import os
import textwrap
from collections.abc import Callable
from dataclasses import is_dataclass
from difflib import unified_diff
from pathlib import Path
from types import TracebackType

import pytest

SNAPSHOT_EXT = '.py'


def indent(
    text: str,
    prefix: str,
    first_prefix: str | None = None,
) -> str:
    if first_prefix is None:
        first_prefix = prefix
    ret = textwrap.indent(text, prefix)
    lines = ret.splitlines(keepends=True)
    if not lines:
        return first_prefix + ret

    lines[0] = first_prefix + lines[0].removeprefix(prefix)
    ret = ''.join(lines)
    return ret


def format_obj(obj: object) -> str:
    match obj:
        case int() | float() | None:
            return repr(obj)

        case str() if '\n' not in obj:
            return repr(obj)

        case str():
            return '\n'.join(
                '  ' * (i != 0) + repr(s) for i, s in enumerate(obj.splitlines(keepends=True))
            )
        case bytes() if b'\n' not in obj:
            return repr(obj)

        case bytes():
            return '\n'.join(
                '  ' * (i != 0) + repr(s) for i, s in enumerate(obj.splitlines(keepends=True))
            )

        case list():
            if not obj:
                return '[]'
            return '[\n' + ''.join(indent(format_obj(x), '  ') + ',\n' for x in obj) + ']'

        case tuple():
            if not obj:
                return '()'
            return '(\n' + ''.join(indent(format_obj(x), '  ') + ',\n' for x in obj) + ')'

        case BaseException():
            name = format_obj(obj.__class__)

            if obj.args:
                return (
                    f'{name}(\n'
                    + ''.join(indent(format_obj(x), '  ') + ',\n' for x in obj.args)
                    + ')'
                )

            if str(obj):
                if '\n' not in str(obj):
                    return f'{name}({str(obj)!r})'
                return (
                    f'{name}(\n'
                    + '\n'.join(
                        '  ' + repr(s) for i, s in enumerate(str(obj).splitlines(keepends=True))
                    )
                    + ')'
                )

            return f'{name}()'

        case type():
            name = obj.__qualname__
            if obj.__module__ not in ('builtins', '', '__main__'):
                name = f'{obj.__module__}.{name}'
            return name

        case _ if is_dataclass(obj):
            fields = {}
            for field_name in obj.__dataclass_fields__:
                value = getattr(obj, field_name)
                fields[field_name] = value

            class_name = obj.__class__.__qualname__
            if not fields:
                return f'{class_name}()'

            return (
                f'{class_name}(\n'
                + ''.join(indent(format_obj(v), '  ', f'  {k}=') + ',\n' for k, v in fields.items())
                + ')'
            )

            fields_str = ',\n'.join(fields)
            return f'{class_name}(\n{fields_str}\n{prefix})'

        case dict():
            if not obj:
                return '{}'

            return (
                '{\n'
                + ''.join(indent(format_obj(v), '  ', f'  {k!r}: ') + ',\n' for k, v in obj.items())
                + '}'
            )

            fields_str = ',\n'.join(fields)
            return f'{class_name}(\n{fields_str}\n{prefix})'

        case Path():
            return f'Path({str(obj)!r})'

        case _:
            return repr(obj)

    assert_never(obj)


class Snapshotter:
    def __init__(
        self,
        test_name: str,
        snapshot_dir: Path,
        should_update: bool,
        params: dict[str, object] | None = None,
    ) -> None:
        self.test_name = test_name
        self.snapshot_dir = snapshot_dir
        self.should_update = should_update
        self.fired = False
        self.params = params

    @classmethod
    def from_request(cls, request: pytest.FixtureRequest) -> Snapshotter:
        test_file = Path(request.path)

        test_name = request.node.name
        snapshot_dir = test_file.parent / '.snapshots' / test_file.stem
        should_update = os.environ.get('UPDATE_SNAPSHOTS', '0') == '1'

        if hasattr(request.node, 'callspec'):
            params = request.node.callspec.params
        else:
            params = None

        return Snapshotter(test_name, snapshot_dir, should_update, params)

    def check(self, obj: object) -> bool:
        import hashlib

        safe_name = (
            self.test_name.replace('/', '_')
            .replace('\\', '_')
            .replace('\n', '_')
            .replace('\r', '_')
        )

        # Truncate long filenames to avoid filesystem limits (typically 255 bytes)
        # Keep first 100 chars + hash of full name for uniqueness
        max_name_len = 200  # Leave room for extension and directory
        if len(safe_name) > max_name_len:
            name_hash = hashlib.sha256(safe_name.encode()).hexdigest()[:16]
            safe_name = f'{safe_name[: max_name_len - 17]}_{name_hash}'

        snapshot_path = self.snapshot_dir / f'{safe_name}{SNAPSHOT_EXT}'

        if self.params is not None:
            obj = {**self.params, 'result': obj}

        actual = format_obj(obj)

        if not snapshot_path.exists():
            expected = ''
        else:
            expected = snapshot_path.read_text(encoding='utf-8')

        if actual != expected:
            if self.should_update:
                self.snapshot_dir.mkdir(parents=True, exist_ok=True)
                snapshot_path.write_text(actual, encoding='utf-8')
                return True

            diff = '\n'.join(
                list(
                    unified_diff(
                        expected.splitlines(),
                        actual.splitlines(),
                        fromfile='expected',
                        tofile='actual',
                        lineterm='',
                    )
                )[3:]
            )

            self.fired = True
            pytest.fail(
                f'Snapshot mismatch for {self.test_name}\n'
                f'If you are ABSOLUTELY sure that the diff is expected and correct, \n'
                'run `just update-snapshots` to update the snapshot.\n\n'
                f'Diff:\n{diff}'
            )
            # unreachable
        return True

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self.fired:
            return False
        if exc_type is not None:
            ok = self.check((exc_type, exc_val))
            return ok  # suppress only if test passes
        return False

    def __call__(self, actual: object) -> bool:
        ok = self.check(actual)
        return ok
