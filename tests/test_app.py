import logging
from asyncio import AbstractEventLoop

from aiohttp.web import Application

from messy.app import create


def test_create(logger: logging.Logger,
                instance_name: str,
                event_loop: AbstractEventLoop) -> None:
    result = create(logger=logger,
                    instance_name=instance_name,
                    loop=event_loop)

    assert isinstance(result, Application)
    assert result.logger == logger
    assert result['instance'] == instance_name
