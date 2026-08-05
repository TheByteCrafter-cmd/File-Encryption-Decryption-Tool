"""
Cryptographic Utilities, Binary Header Protocol, Logging, and Custom Exception Hierarchy.

Provides structured header packing/unpacking, file and password validation, zero-trust logging,
and domain-specific exception types for the Secure File Encryption & Decryption Tool.
"""

import logging
import os
import struct
from pathlib import Path
from typing import BinaryIO, Tuple

import config

# ==============================================================================
# Custom Exception Hierarchy
# ==============================================================================


class FEDTError(Exception):
    """Base exception class for all Secure File Encryption & Decryption Tool errors."""

    pass


class EncryptionError(FEDTError):
    """Raised when file encryption encounters an unrecoverable failure."""

    pass


class DecryptionError(FEDTError):
    """Raised when file decryption encounters an unrecoverable failure."""

    pass


class InvalidPasswordError(DecryptionError):
    """Raised when decryption fails due to an incorrect password."""

    pass


class CorruptedFileError(DecryptionError):
    """Raised when an encrypted file is tampered with or truncated."""

    pass


class InvalidFileFormatError(DecryptionError):
    """Raised when a file does not contain a valid FEDT header signature."""

    pass


class FileAccessError(FEDTError):
    """Raised when input/output file cannot be read or written due to permissions or missing paths."""

    pass


class IntegrityVerificationError(DecryptionError):
    """Raised when authentication tag check fails during decryption."""

    pass


# ==============================================================================
# Zero-Trust Logging Subsystem
# ==============================================================================


def get_logger(name: str = "FEDT") -> logging.Logger:
    """
    Retrieves and configures the application logger.
    Configures file output to logs/app.log and console output without exposing sensitive key material.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

        # Formatter including timestamp, level, module name, and message
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File Handler
        try:
            config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
        except Exception as err:
            print(f"Warning: Unable to initialize file log handler: {err}")

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    return logger


# Initialize global logger instance
logger = get_logger("FEDT.Utils")


# ==============================================================================
# Binary File Header Protocol
# ==============================================================================

# Fixed header prefix: MAGIC(4B) + VER(2B) + SALT(32B) + NONCE(12B) + TAG(16B) + FNAME_LEN(2B) = 68 Bytes
HEADER_PREFIX_FORMAT: str = ">4sH32s12s16sH"
HEADER_PREFIX_SIZE: int = struct.calcsize(HEADER_PREFIX_FORMAT)
TAG_OFFSET_IN_HEADER: int = 4 + 2 + 32 + 12  # Byte index 50 (Tag size = 16)


def pack_header(
    salt: bytes,
    nonce: bytes,
    tag: bytes,
    original_filename: str,
    version: int = config.HEADER_VERSION,
) -> bytes:
    """
    Packs cryptographic parameters and metadata into a contiguous binary header.

    Header Structure:
    [MAGIC: 4B][VERSION: 2B][SALT: 32B][NONCE: 12B][TAG: 16B][FILENAME_LEN: 2B][FILENAME: UTF-8]
    """
    if len(salt) != config.SALT_SIZE:
        raise ValueError(f"Salt size must be exactly {config.SALT_SIZE} bytes.")
    if len(nonce) != config.NONCE_SIZE:
        raise ValueError(f"Nonce size must be exactly {config.NONCE_SIZE} bytes.")
    if len(tag) != config.TAG_SIZE:
        raise ValueError(f"Tag size must be exactly {config.TAG_SIZE} bytes.")

    filename_bytes = original_filename.encode("utf-8")
    filename_len = len(filename_bytes)
    if filename_len > 65535:
        raise ValueError("Filename is too long to encode in binary header.")

    prefix = struct.pack(
        HEADER_PREFIX_FORMAT,
        config.MAGIC_HEADER,
        version,
        salt,
        nonce,
        tag,
        filename_len,
    )
    return prefix + filename_bytes


def unpack_header(stream: BinaryIO) -> Tuple[int, bytes, bytes, bytes, str, int]:
    """
    Unpacks binary header from input file stream.

    Returns:
        Tuple containing (version, salt, nonce, tag, original_filename, total_header_size)

    Raises:
        InvalidFileFormatError: If file is too small or magic bytes do not match.
    """
    prefix_data = stream.read(HEADER_PREFIX_SIZE)
    if len(prefix_data) < HEADER_PREFIX_SIZE:
        raise InvalidFileFormatError(
            "File is corrupted or too small to contain a valid FEDT header."
        )

    try:
        magic, version, salt, nonce, tag, filename_len = struct.unpack(
            HEADER_PREFIX_FORMAT, prefix_data
        )
    except struct.error as err:
        raise InvalidFileFormatError(
            f"Failed to unpack header structure: {err}"
        ) from err

    if magic != config.MAGIC_HEADER:
        raise InvalidFileFormatError(
            f"Invalid file format signature. Expected {config.MAGIC_HEADER!r}, got {magic!r}."
        )

    filename_bytes = stream.read(filename_len)
    if len(filename_bytes) < filename_len:
        raise InvalidFileFormatError(
            "Header truncated: unable to read full original filename."
        )

    try:
        original_filename = filename_bytes.decode("utf-8")
    except UnicodeDecodeError as err:
        raise InvalidFileFormatError(
            f"Corrupted filename encoding in header: {err}"
        ) from err

    total_header_size = HEADER_PREFIX_SIZE + filename_len
    return version, salt, nonce, tag, original_filename, total_header_size


# ==============================================================================
# Validation Helpers
# ==============================================================================


def validate_input_file(file_path: Path | str) -> Path:
    """Validates that target input file exists, is a file, and is readable."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileAccessError(f"Target file does not exist: {path}")
    if not path.is_file():
        raise FileAccessError(f"Target path is a directory, not a file: {path}")
    if not os.access(path, os.R_OK):
        raise FileAccessError(f"Permission denied: cannot read target file: {path}")
    return path


def validate_password(password: str) -> None:
    """Validates that password is provided and non-empty."""
    if not password:
        raise ValueError("Password cannot be empty.")
