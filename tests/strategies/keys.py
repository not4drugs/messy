import operator

from Cryptodome.PublicKey import RSA
from hypothesis import strategies

sizes_in_bits = strategies.sampled_from([1024, 2048, 3072])


def to_odd(number: int) -> int:
    return 2 * number + 1


exponents = strategies.integers(min_value=1).map(to_odd)
private_keys = strategies.builds(RSA.generate,
                                 bits=sizes_in_bits,
                                 e=exponents)
public_keys = (private_keys
               .map(operator.methodcaller(RSA.RsaKey.publickey.__name__)))
keys = strategies.one_of(private_keys,
                         public_keys)
names = strategies.text(min_size=1)
secrets = strategies.one_of(strategies.none(),
                            strategies.text(min_size=1))
