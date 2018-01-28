import codecs
import json
import traceback
from http import HTTPStatus
from typing import (Callable,
                    Coroutine)

from aiohttp.web import (Application,
                         json_response)
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from .utils import Status

HandlerType = Callable[[Request], Coroutine[None, None, Response]]


async def factory(app: Application,
                  handler: HandlerType) -> HandlerType:
    logger = app.logger
    instance_name = app['instance']

    async def middlewared(request: Request) -> Response:
        logger.debug(f'Received "{request.method}" request '
                     f'to "{request.path}".')
        try:
            response = await handler(request)
        except Exception:
            logger.exception('')
            err_msg = ('Something unexpected happened, '
                       'contact with administrator '
                       'and provide following traceback:\n'
                       f'{traceback.format_exc()}')
            data = {'status': Status.unknown_error,
                    'reason': err_msg,
                    'instance': instance_name}
            return json_response(data,
                                 status=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            response_encoding = response.charset
            response_body = response.body
            if not isinstance(response_body, bytes):
                response_encoding = response_body.encoding
                response_body = response_body._value
            response_text = codecs.decode(response_body,
                                          encoding=response_encoding)
            data = json.loads(response_text)
            logger.debug(json.dumps(data,
                                    ensure_ascii=False,
                                    indent=2))
            data['instance'] = instance_name
            return json_response(data,
                                 status=response.status)

    return middlewared
