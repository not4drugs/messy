from Cryptodome.PublicKey import RSA

from messy.messages import (MAC_TAG_LENGTH,
                            NONCE_LENGTH,
                            decrypt,
                            encrypt)


def test_encrypt(public_key: RSA.RsaKey,
                 message: bytes) -> None:
    result = encrypt(message,
                     public_key=public_key)

    assert isinstance(result, bytes)
    assert len(result) == (public_key.size_in_bytes()
                           + NONCE_LENGTH + MAC_TAG_LENGTH
                           + len(message))


def test_decrypt(private_key: RSA.RsaKey,
                 public_key: RSA.RsaKey,
                 message: bytes) -> None:
    encrypted = encrypt(message,
                        public_key=public_key)
    result = decrypt(encrypted,
                     private_key=private_key)

    assert isinstance(result, bytes)
    assert result == message
