import logging
from asyncio import AbstractEventLoop

from aiohttp.web import Application

from . import (handlers,
               middlewares)


def create(*,
           logger: logging.Logger,
           instance_name: str,
           loop: AbstractEventLoop) -> Application:
    app = Application(logger=logger,
                      loop=loop,
                      middlewares=[middlewares.factory])
    app['instance'] = instance_name
    app.router.add_post('/generate-key', handlers.generate_key)
    app.router.add_post('/add-key', handlers.add_key)
    app.router.add_post('/encrypt', handlers.encrypt)
    app.router.add_post('/decrypt', handlers.decrypt)
    return app
