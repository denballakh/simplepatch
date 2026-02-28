from dataclasses import dataclass
from pathlib import Path
from typing import assert_never


@dataclass
class File:
    DEFAULT_PERMISSIONS = 0o644

    content: bytes | str
    permissions: int = DEFAULT_PERMISSIONS

    @property
    def binary_content(self) -> bytes:
        return self.content.encode('utf-8') if isinstance(self.content, str) else self.content


@dataclass
class Dir:
    DEFAULT_PERMISSIONS = 0o755

    children: dict[str, File | Dir]
    permissions: int = DEFAULT_PERMISSIONS


def write_fs(base_dir: Path, fs_tree: Dir) -> None:
    for name, item in fs_tree.children.items():
        path = base_dir / name
        match item:
            case File():
                path.write_bytes(item.binary_content)
                path.chmod(item.permissions)

            case Dir():
                path.mkdir(parents=True, exist_ok=True)
                write_fs(path, item)

            case _:
                assert_never(item)


def read_fs(base_dir: Path) -> Dir:
    result: Dir = Dir({})

    for path in sorted(base_dir.iterdir()):
        name = path.name
        if path.is_file():
            try:
                content = path.read_text()
            except Exception:
                content = path.read_bytes()

            permissions = path.stat().st_mode & 0o777
            result.children[name] = File(content, permissions)
        elif path.is_dir():
            result.children[name] = read_fs(path)

    return result
