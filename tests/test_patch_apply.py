from __future__ import annotations
from pathlib import Path

import pytest

from simplepatch import apply_patch, parse_patch
from .snapshots import Snapshotter
from .fsutils import File, write_fs, read_fs, Dir
from . import DATA_DIR

PATCH_APPLY_TESTCASES_FILENAME = DATA_DIR / 'apply.patch'


def parse_onefile_test_cases(file: Path) -> list[tuple[str | None, str]]:
    DELETED = 'DELETED'  # special string that means that there is no file at all

    text = file.read_text()
    cases = text.split('=' * 50 + '\n')
    ret = []
    for case in cases:
        if not case.strip():
            continue

        parts = case.split('-' * 50 + '\n')
        if len(parts) != 2:
            continue
        before, patch = parts

        # Remove trailing separator from after if present
        if before.strip() == DELETED:
            before = None
        else:
            before = before

        ret.append((before, patch))
    return ret


PATCH_APPLY_TESTCASES = parse_onefile_test_cases(PATCH_APPLY_TESTCASES_FILENAME)


@pytest.mark.parametrize(
    [
        'before',
        'patch_text',
    ],
    PATCH_APPLY_TESTCASES,
)
def test_patch_apply(
    before: str | None,
    patch_text: str,
    tmp_path: Path,
    snapshot: Snapshotter,
):
    fs_before = Dir({'file': File(before)} if before is not None else {})
    write_fs(tmp_path, fs_before)

    with snapshot:
        patch = parse_patch(patch_text)
        apply_patch(patch, base_dir=tmp_path)
        fs_actual = read_fs(tmp_path)
        snapshot(fs_actual)
