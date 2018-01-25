from Cryptodome.PublicKey import RSA
from hypothesis import strategies

rsa_keys_lengths_in_bits = strategies.sampled_from([1024, 2048, 3072])


def to_odd(number: int) -> int:
    return 2 * number + 1


rsa_public_keys_exponents = strategies.integers(min_value=1).map(to_odd)
private_keys = strategies.builds(RSA.generate,
                                 bits=rsa_keys_lengths_in_bits,
                                 e=rsa_public_keys_exponents)
