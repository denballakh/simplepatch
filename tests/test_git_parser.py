from pathlib import Path

import pytest

from simplepatch import parse_git_patch
from .snapshots import Snapshotter
from .fsutils import File, write_fs, read_fs, Dir
from . import DATA_DIR

GIT_PARSER_TESTCASES_FILENAME = DATA_DIR / 'git.patch'


def parse_git_parser_test_cases(file: Path) -> list[str]:
    text = file.read_text()
    return [x for x in text.split('=' * 50 + '\n') if x.strip()]


GIT_PARSER_TEST_CASES = []
GIT_PARSER_TEST_CASES += parse_git_parser_test_cases(GIT_PARSER_TESTCASES_FILENAME)


@pytest.mark.parametrize('patch_text', GIT_PARSER_TEST_CASES)
def test_git_patch_parse(patch_text: str, snapshot: Snapshotter) -> None:
    with snapshot:
        snapshot(parse_git_patch(patch_text))
