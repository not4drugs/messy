import pytest
from Cryptodome.PublicKey import RSA
from _pytest.tmpdir import TempdirFactory

from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def private_key() -> RSA.RsaKey:
    return example(strategies.private_keys)


@pytest.fixture(scope='function')
def public_key(private_key: RSA.RsaKey) -> RSA.RsaKey:
    return private_key.publickey()


@pytest.fixture(scope='function')
def key() -> RSA.RsaKey:
    return example(strategies.keys)


@pytest.fixture(scope='function')
def name() -> str:
    return example(strategies.names)


@pytest.fixture(scope='function')
def secret() -> str:
    return example(strategies.secrets)


@pytest.fixture(scope='function')
def size_in_bits() -> int:
    return example(strategies.sizes_in_bits)


@pytest.fixture(scope='function')
def exponent() -> int:
    return example(strategies.exponents)


@pytest.fixture(scope='function')
def directory_path(tmpdir_factory: TempdirFactory) -> str:
    return str(tmpdir_factory.mktemp('.ssh'))
