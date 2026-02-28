from pathlib import Path

import pytest

from simplepatch import parse_patch
from .snapshots import Snapshotter
from .fsutils import File, write_fs, read_fs, Dir
from . import DATA_DIR

PARSER_TESTCASES_FILENAME = DATA_DIR / 'parser.patch'


def parse_parser_test_cases(file: Path) -> list[str]:
    text = file.read_text()
    return text.split('=' * 50 + '\n')


PARSER_TEST_CASES = []
PARSER_TEST_CASES += parse_parser_test_cases(PARSER_TESTCASES_FILENAME)


@pytest.mark.parametrize('patch_text', PARSER_TEST_CASES)
def test_patch_parse(patch_text: str, snapshot: Snapshotter) -> None:
    with snapshot:
        snapshot(parse_patch(patch_text))
