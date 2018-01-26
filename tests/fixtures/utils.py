import pytest

from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def message() -> bytes:
    return example(strategies.messages)
