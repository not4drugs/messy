from typing import Optional

import pytest
from Cryptodome.PublicKey import RSA
from _pytest.monkeypatch import MonkeyPatch
from aiohttp.test_utils import TestClient

from messy import keys
from messy.app import routes
from messy.handlers import (JsonType,
                            generate_key,
                            add_key,
                            encrypt,
                            decrypt)
from messy.utils import Status


@pytest.mark.asyncio
async def test_generate_key(instance_name: str,
                            client: TestClient,
                            generate_key_json: Optional[JsonType],
                            directory_path: str,
                            monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(keys, 'directory_path', directory_path)
    response = await client.request(*routes[generate_key],
                                    json=generate_key_json)
    response_json = await response.json()

    assert response_json['instance'] == instance_name
    assert response_json['status'] == Status.ok


@pytest.mark.asyncio
async def test_add_key(instance_name: str,
                       client: TestClient,
                       add_key_json: JsonType,
                       directory_path: str,
                       monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(keys, 'directory_path', directory_path)
    response = await client.request(*routes[add_key],
                                    json=add_key_json)
    response_json = await response.json()

    assert response_json['instance'] == instance_name
    assert response_json['status'] == Status.ok


@pytest.mark.asyncio
async def test_encrypt(instance_name: str,
                       client: TestClient,
                       encrypt_json: JsonType,
                       name: str,
                       public_key: RSA.RsaKey,
                       monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(keys, 'cache', {name: public_key})
    response = await client.request(*routes[encrypt],
                                    json=encrypt_json)
    response_json = await response.json()

    assert response_json['instance'] == instance_name
    assert response_json['status'] == Status.ok


@pytest.mark.asyncio
async def test_decrypt(instance_name: str,
                       client: TestClient,
                       decrypt_json: JsonType,
                       private_key: RSA.RsaKey,
                       monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(keys, 'cache', {instance_name: private_key})
    response = await client.request(*routes[decrypt],
                                    json=decrypt_json)
    response_json = await response.json()

    assert response_json['instance'] == instance_name
    assert response_json['status'] == Status.ok
