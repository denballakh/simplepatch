from collections.abc import Callable

import pytest

from .snapshots import Snapshotter


@pytest.fixture
def snapshot(request: pytest.FixtureRequest) -> Snapshotter:
    return Snapshotter.from_request(request)
