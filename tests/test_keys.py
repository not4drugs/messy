import os

import pytest
from Cryptodome.PublicKey import RSA
from _pytest.monkeypatch import MonkeyPatch

from messy import keys
from messy.keys import (create,
                        save,
                        search,
                        to_file_path)


def test_search(key: RSA.RsaKey,
                name: str,
                secret: str,
                directory_path: str,
                monkeypatch: MonkeyPatch) -> None:
    with pytest.raises(FileNotFoundError):
        search(name,
               secret=secret)

    monkeypatch.setattr(keys, 'directory_path', directory_path)
    save(key,
         name=name,
         secret=secret)
    key_from_cache = search(name=name,
                            secret=secret)
    monkeypatch.setattr(keys, 'cache', {})
    key_from_file = search(name=name,
                           secret=secret)

    assert isinstance(key_from_file, RSA.RsaKey)
    assert isinstance(key_from_cache, RSA.RsaKey)
    assert key_from_file == key_from_cache == key


def test_save(key: RSA.RsaKey,
              name: str,
              secret: str,
              directory_path: str,
              monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(keys, 'directory_path', directory_path)
    file_path = to_file_path(name)
    file_path_existed_before = os.path.exists(file_path)
    save(key,
         name=name,
         secret=secret)
    file_path_exists_after = os.path.exists(file_path)

    assert not file_path_existed_before
    assert file_path_exists_after


def test_create(size_in_bits: int,
                exponent: int) -> None:
    result = create(size=size_in_bits,
                    exponent=exponent)

    assert isinstance(result, RSA.RsaKey)
    assert result.size_in_bits() == size_in_bits
    assert result.e == exponent


def test_to_file_path(name: str) -> None:
    result = to_file_path(name)

    assert isinstance(result, str)
    assert name in result
