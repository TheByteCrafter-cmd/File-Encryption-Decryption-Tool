"""
Unit tests for KeyDerivationManager, binary header packing/unpacking, and memory wiping.
"""

import io
import pytest
import config
from encryption.key_manager import KeyDerivationManager
from encryption.utils import (
    InvalidFileFormatError,
    pack_header,
    unpack_header,
    validate_password,
)


def test_key_derivation_deterministic():
    """Verify that same password and salt produce identical derived keys."""
    password = "SuperSecretPassword123!"
    salt = KeyDerivationManager.generate_salt()

    key1 = KeyDerivationManager.derive_key(password, salt)
    key2 = KeyDerivationManager.derive_key(password, salt)

    assert len(key1) == config.KEY_SIZE
    assert key1 == key2


def test_key_derivation_different_salts():
    """Verify that different salts produce distinct derived keys for the same password."""
    password = "SuperSecretPassword123!"
    salt1 = KeyDerivationManager.generate_salt()
    salt2 = KeyDerivationManager.generate_salt()

    key1 = KeyDerivationManager.derive_key(password, salt1)
    key2 = KeyDerivationManager.derive_key(password, salt2)

    assert key1 != key2


def test_empty_password_validation():
    """Verify empty password raises ValueError."""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        validate_password("")


def test_header_packing_unpacking_roundtrip():
    """Verify header packing and unpacking correctly restores metadata and original filename."""
    salt = KeyDerivationManager.generate_salt()
    nonce = KeyDerivationManager.generate_nonce()
    tag = b"0123456789abcdef"  # 16 bytes
    original_fname = "document_confidential_2026.pdf"

    packed = pack_header(salt, nonce, tag, original_fname)
    stream = io.BytesIO(packed)

    (
        version,
        unpacked_salt,
        unpacked_nonce,
        unpacked_tag,
        unpacked_fname,
        header_size,
    ) = unpack_header(stream)

    assert version == config.HEADER_VERSION
    assert unpacked_salt == salt
    assert unpacked_nonce == nonce
    assert unpacked_tag == tag
    assert unpacked_fname == original_fname
    assert header_size == len(packed)


def test_unpack_invalid_magic_header():
    """Verify unpacking invalid magic header raises InvalidFileFormatError."""
    bad_header = b"BADH\x00\x01" + b"\x00" * 62
    stream = io.BytesIO(bad_header)

    with pytest.raises(InvalidFileFormatError, match="Invalid file format signature"):
        unpack_header(stream)


def test_memory_wipe():
    """Verify memory wiping zeroes out bytearray buffer."""
    buf = bytearray(b"SecretKeyMaterial123456789012345")
    KeyDerivationManager.wipe_memory(buf)

    assert buf == bytearray(b"\x00" * 32)
