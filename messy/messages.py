import codecs
from itertools import accumulate

from Cryptodome.Cipher import (AES,
                               PKCS1_OAEP)
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

MAC_TAG_LENGTH = 16
NONCE_LENGTH = 16


def encrypt(message: bytes,
            *,
            public_key: RSA.RsaKey) -> bytes:
    session_key = get_random_bytes(16)
    encrypted_session_key = encrypt_rsa(session_key,
                                        public_key=public_key)
    cipher = AES.new(session_key,
                     mode=AES.MODE_EAX)
    encrypted, tag = cipher.encrypt_and_digest(message)
    return b''.join([encrypted_session_key,
                     cipher.nonce,
                     tag,
                     encrypted])


def decrypt(message: bytes,
            *,
            private_key: RSA.RsaKey) -> bytes:
    indexes_increments = [0, private_key.size_in_bytes(),
                          NONCE_LENGTH, MAC_TAG_LENGTH]
    indexes = list(accumulate(indexes_increments)) + [None]
    encrypted_session_key, nonce, tag, encrypted = [
        message[previous_index:index]
        for previous_index, index in zip(indexes, indexes[1:])]
    session_key = decrypt_rsa(encrypted_session_key,
                              private_key=private_key)
    cipher = AES.new(session_key,
                     mode=AES.MODE_EAX,
                     nonce=nonce)
    return cipher.decrypt_and_verify(encrypted,
                                     received_mac_tag=tag)


rsa_cipher = PKCS1_OAEP.new


def encrypt_rsa(message: bytes,
                *,
                public_key: RSA.RsaKey) -> bytes:
    cipher = rsa_cipher(public_key)
    return cipher.encrypt(message)


def decrypt_rsa(message: bytes,
                *,
                private_key: RSA.RsaKey) -> bytes:
    cipher = rsa_cipher(private_key)
    return cipher.decrypt(message)


def encode(message: bytes,
           *,
           encoding: str = 'hex') -> bytes:
    return codecs.encode(message,
                         encoding=encoding)


def decode(message: bytes,
           *,
           encoding: str = 'hex') -> bytes:
    return codecs.decode(message,
                         encoding=encoding)
