from asyncio import AbstractEventLoop
from logging import Logger

import pytest
from aiohttp.test_utils import (TestServer,
                                TestClient)
from aiohttp.web import Application

from messy.app import create
from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def logger() -> Logger:
    return example(strategies.loggers)


@pytest.fixture(scope='function')
def instance_name() -> str:
    return example(strategies.instances_names)


@pytest.fixture(scope='function')
def app(logger: Logger,
        instance_name: str,
        event_loop: AbstractEventLoop) -> Application:
    return create(logger=logger,
                  instance_name=instance_name,
                  loop=event_loop)


@pytest.fixture(scope='function')
def server(app: Application,
           event_loop: AbstractEventLoop) -> TestServer:
    return TestServer(app,
                      loop=event_loop)


@pytest.fixture(scope='function')
def client(server: TestServer,
           event_loop: AbstractEventLoop) -> TestClient:
    with TestClient(server,
                    loop=event_loop) as result:
        yield result
