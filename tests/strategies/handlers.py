from Cryptodome.PublicKey import RSA
from hypothesis import strategies

from .keys import (sizes_in_bits,
                   exponents,
                   secrets,
                   public_keys)
from .utils import names

generate_key_jsons = strategies.one_of(
        strategies.none(),
        strategies.fixed_dictionaries({'size': sizes_in_bits,
                                       'exponent': exponents,
                                       'secret': secrets}))
public_keys_strings = public_keys.map(RSA.RsaKey.exportKey).map(bytes.decode)
add_key_jsons = strategies.fixed_dictionaries({'name': names,
                                               'key': public_keys_strings})
