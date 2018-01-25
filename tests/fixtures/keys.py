import pytest
from Cryptodome.PublicKey import RSA

from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def private_key() -> RSA.RsaKey:
    return example(strategies.private_keys)


@pytest.fixture(scope='function')
def public_key(private_key: RSA.RsaKey) -> RSA.RsaKey:
    return private_key.publickey()
