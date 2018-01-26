from Cryptodome.PublicKey import RSA

from messy.messages import (MAC_TAG_LENGTH,
                            NONCE_LENGTH,
                            decrypt,
                            encrypt,
                            encode,
                            decode)


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


def test_encode(message: bytes) -> None:
    result = encode(message)

    assert isinstance(result, bytes)
    assert len(result) >= len(message)


def test_decode(message: bytes) -> None:
    encoded = encode(message)
    result = decode(encoded)

    assert isinstance(result, bytes)
    assert result == message
