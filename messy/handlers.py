from http import HTTPStatus
from typing import (Union,
                    Dict)

from Cryptodome.PublicKey import RSA
from aiohttp.web_request import Request
from aiohttp.web_response import (Response,
                                  json_response)

from . import (messages,
               keys)
from .utils import Status

JsonType = Dict[str, Union[int, str]]


async def to_json(request: Request) -> JsonType:
    return await request.json()


async def generate_key(request: Request) -> Response:
    request_json = await to_json(request) if request.body_exists else {}

    try:
        size = request_json.get('size', 2_048)
        exponent = request_json.get('exponent', 65_537)
        secret = request_json.get('secret')
    except KeyError:
        data = {'status': Status.invalid_json,
                'reason': 'Invalid JSON.'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    private_key = keys.create(size=size,
                              exponent=exponent)
    instance_name = request.app['instance']
    keys.save(private_key,
              name=instance_name,
              secret=secret)
    data = {'status': Status.ok}
    return json_response(data)


async def add_key(request: Request) -> Response:
    request_json = await to_json(request) if request.body_exists else {}

    try:
        name = request_json['name']
        raw_public_key = request_json['key']
    except KeyError:
        data = {'status': Status.invalid_json,
                'reason': 'Invalid JSON.'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    instance_name = request.app['instance']
    attempt_to_add_instance_key = name == instance_name
    if attempt_to_add_instance_key:
        data = {'status': Status.invalid_method,
                'reason': 'Trying to set instance key which is not allowed, '
                          f'use "{generate_key.__qualname__}" method '
                          'for generating it.'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    public_key = RSA.import_key(raw_public_key)
    attempt_to_add_private_key = public_key.has_private()
    if attempt_to_add_private_key:
        data = {'status': Status.private_key_received,
                'reason': 'Expected public key '
                          'but private key received '
                          f'for "{name}".'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    keys.save(public_key,
              name=name)
    data = {'status': Status.ok,
            'name': name}
    return json_response(data)


async def encrypt(request: Request) -> Response:
    request_json = await to_json(request)

    try:
        name = request_json['name']
        message = request_json['message']
    except KeyError:
        data = {'status': Status.invalid_json,
                'reason': 'Invalid JSON.'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    try:
        public_key = keys.search(name)
    except (FileNotFoundError, ValueError):
        data = {'status': Status.key_not_found,
                'reason': 'Failed to found valid key '
                          f'for "{name}".'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    result = messages.encrypt(message.encode(),
                              public_key=public_key)
    data = {'status': Status.ok,
            'result': messages.encode(result).decode(),
            'name': name}
    return json_response(data)


async def decrypt(request: Request) -> Response:
    request_json = await to_json(request)

    try:
        message = request_json['message']
        secret = request_json.get('secret')
    except KeyError:
        data = {'status': Status.invalid_json,
                'reason': 'Invalid JSON.'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    instance_name = request.app['instance']
    try:
        private_key = keys.search(instance_name,
                                  secret=secret)
    except (FileNotFoundError, ValueError):
        data = {'status': Status.key_not_found,
                'reason': 'Failed to found valid instance key.'}
        return json_response(data,
                             status=HTTPStatus.BAD_REQUEST)

    result = messages.decrypt(messages.decode(message.encode()),
                              private_key=private_key)
    data = {'status': Status.ok,
            'result': result.decode()}
    return json_response(data)
