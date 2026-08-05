"""
Secure File Encryption & Decryption Engine Package.

Exposes core classes, exceptions, and key derivation primitives.
"""

from encryption.aes_decrypt import FileDecryptor
from encryption.aes_encrypt import FileEncryptor
from encryption.key_manager import KeyDerivationManager
from encryption.utils import (
    CorruptedFileError,
    DecryptionError,
    EncryptionError,
    FEDTError,
    FileAccessError,
    InvalidFileFormatError,
    InvalidPasswordError,
    IntegrityVerificationError,
    get_logger,
)

__all__ = [
    "FileEncryptor",
    "FileDecryptor",
    "KeyDerivationManager",
    "FEDTError",
    "EncryptionError",
    "DecryptionError",
    "InvalidPasswordError",
    "CorruptedFileError",
    "InvalidFileFormatError",
    "FileAccessError",
    "IntegrityVerificationError",
    "get_logger",
]
