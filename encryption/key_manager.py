"""
Key Derivation and Memory Security Management.

Handles cryptographically secure PBKDF2-HMAC-SHA256 key derivation, random byte generation,
and secure in-memory key buffer wiping.
"""

import secrets
from typing import Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import config
from encryption.utils import logger, validate_password


class KeyDerivationManager:
    """
    Manages key derivation using PBKDF2-HMAC-SHA256 and cryptographically secure random values.
    """

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """
        Derives a 256-bit (32-byte) AES key from a password and salt using PBKDF2-HMAC-SHA256.

        Args:
            password: User supplied password.
            salt: Cryptographically secure random salt (32 bytes).

        Returns:
            bytes: Derived 32-byte key.

        Raises:
            ValueError: If password is empty or salt is invalid.
        """
        validate_password(password)

        if not salt or len(salt) != config.SALT_SIZE:
            raise ValueError(f"Salt must be exactly {config.SALT_SIZE} bytes.")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=config.KEY_SIZE,
            salt=salt,
            iterations=config.PBKDF2_ITERATIONS,
            backend=default_backend(),
        )

        return kdf.derive(password.encode("utf-8"))

    @staticmethod
    def generate_salt() -> bytes:
        """Generates a cryptographically secure random salt of config.SALT_SIZE bytes."""
        return secrets.token_bytes(config.SALT_SIZE)

    @staticmethod
    def generate_nonce() -> bytes:
        """Generates a cryptographically secure random IV/Nonce of config.NONCE_SIZE bytes."""
        return secrets.token_bytes(config.NONCE_SIZE)

    @staticmethod
    def wipe_memory(buffer: Union[bytearray, memoryview]) -> None:
        """
        Overwrites mutable byte buffer in memory with zero bytes to prevent memory disclosure.

        Args:
            buffer: Target bytearray or writable memoryview.
        """
        try:
            if isinstance(buffer, bytearray):
                for i in range(len(buffer)):
                    buffer[i] = 0
            elif isinstance(buffer, memoryview) and not buffer.readonly:
                buffer[:] = b"\x00" * len(buffer)
        except Exception as err:
            logger.warning(f"Memory wipe encountered non-fatal error: {err}")
