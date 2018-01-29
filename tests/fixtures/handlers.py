from typing import (Union,
                    Optional,
                    Dict)

import pytest
from Cryptodome.PublicKey import RSA

from messy import messages
from messy.handlers import JsonType
from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def generate_key_json() -> Optional[JsonType]:
    return example(strategies.generate_key_jsons)


@pytest.fixture(scope='function')
def add_key_json() -> JsonType:
    return example(strategies.add_key_jsons)


@pytest.fixture(scope='function')
def encrypt_json(name: str,
                 message: bytes) -> JsonType:
    return {'name': name,
            'message': message.decode()}


@pytest.fixture(scope='function')
def decrypt_json(message: bytes,
                 public_key: RSA.RsaKey) -> JsonType:
    encrypted = messages.encrypt(message,
                                 public_key=public_key)
    return {'message': messages.encode(encrypted).decode()}
