import logging
from asyncio import AbstractEventLoop
from functools import partial
from typing import NamedTuple

from aiohttp.hdrs import METH_POST
from aiohttp.web import Application

from . import (handlers,
               middlewares)


class Route(NamedTuple):
    method: str
    path: str


PostRoute = partial(Route, METH_POST)

routes = {
    handlers.generate_key: PostRoute('/generate-key'),
    handlers.add_key: PostRoute('/add-key'),
    handlers.encrypt: PostRoute('/encrypt'),
    handlers.decrypt: PostRoute('/decrypt'),
}


def create(*,
           logger: logging.Logger,
           instance_name: str,
           loop: AbstractEventLoop) -> Application:
    app = Application(logger=logger,
                      loop=loop,
                      middlewares=[middlewares.factory])
    app['instance'] = instance_name
    for handler, route in routes.items():
        app.router.add_route(*route,
                             handler=handler)
    return app
