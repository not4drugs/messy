from logging import Logger

import pytest

from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def logger() -> Logger:
    return example(strategies.loggers)


@pytest.fixture(scope='function')
def instance_name() -> str:
    return example(strategies.instances_names)
