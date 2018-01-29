import os
from pathlib import Path

from Cryptodome.PublicKey import RSA

cache = {}


def search(name: str,
           *,
           secret: str = None) -> RSA.RsaKey:
    try:
        return cache[name]
    except KeyError:
        if secret is not None:
            secret = secret.encode()
        path = to_file_path(name)
        with open(path, mode='rb') as file:
            content = file.read()
        key = RSA.import_key(content,
                             passphrase=secret)
        return cache.setdefault(name, key)


def save(key: RSA.RsaKey,
         *,
         name: str,
         secret: str = None) -> None:
    if secret is not None:
        secret = secret.encode()
    path = to_file_path(name)
    content = key.exportKey(passphrase=secret)
    with open(path, mode='wb') as file:
        file.write(content)
    cache[name] = key


def create(*,
           size: int,
           exponent: int) -> RSA.RsaKey:
    return RSA.generate(size,
                        e=exponent)


directory_path = os.path.join(Path.home(), '.ssh')


def to_file_path(name: str) -> str:
    return os.path.join(directory_path,
                        to_file_name(name))


def to_file_name(name: str) -> str:
    return name.encode().hex()
