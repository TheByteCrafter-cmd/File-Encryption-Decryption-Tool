"""
Low-Level Cipher AES-256-GCM Streaming File Encryption Engine.

Implements true chunk-based streaming file encryption using low-level Cipher(algorithms.AES, modes.GCM).
Supports configurable chunk sizes, non-blocking progress callbacks, extensible binary header metadata,
and memory zeroing of derived keys.
"""

from pathlib import Path
from typing import Callable, Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import config
from encryption.key_manager import KeyDerivationManager
from encryption.utils import (
    TAG_OFFSET_IN_HEADER,
    EncryptionError,
    FileAccessError,
    logger,
    pack_header,
    validate_input_file,
    validate_password,
)


class FileEncryptor:
    """
    Production-ready streaming file encryptor using low-level AES-256-GCM.
    """

    @staticmethod
    def encrypt_file(
        input_path: Path | str,
        password: str,
        output_path: Optional[Path | str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        chunk_size: int = config.CHUNK_SIZE,
    ) -> Path:
        """
        Encrypts any input file using AES-256-GCM streaming with a low-level Cipher API.

        Args:
            input_path: Absolute or relative path to the input file.
            password: User secret password for PBKDF2 key derivation.
            output_path: Optional destination path. Defaults to output/filename.ext.enc.
            progress_callback: Optional callback accepting (processed_bytes, total_bytes).
            chunk_size: Processing chunk size in bytes (default 64 KB).

        Returns:
            Path: Path to the generated .enc file.

        Raises:
            FileAccessError: If input file is missing or unreadable.
            ValueError: If password is empty.
            EncryptionError: If an unrecoverable streaming or encryption error occurs.
        """
        validated_input = validate_input_file(input_path)
        validate_password(password)

        if output_path is None:
            config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            destination = config.OUTPUT_DIR / f"{validated_input.name}.enc"
        else:
            destination = Path(output_path).resolve()
            destination.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Encryption started for file: '{validated_input.name}'")

        raw_key: bytearray = bytearray()
        try:
            # 1. Cryptographic Parameter Generation & Key Derivation
            salt = KeyDerivationManager.generate_salt()
            nonce = KeyDerivationManager.generate_nonce()
            raw_key = bytearray(KeyDerivationManager.derive_key(password, salt))

            # 2. Low-Level AES-256-GCM Cipher Setup
            cipher = Cipher(
                algorithms.AES(bytes(raw_key)),
                modes.GCM(nonce),
            )
            encryptor = cipher.encryptor()

            # 3. Header Packaging with Tag Placeholder (16 Zero Bytes)
            tag_placeholder = b"\x00" * config.TAG_SIZE
            header_bytes = pack_header(
                salt=salt,
                nonce=nonce,
                tag=tag_placeholder,
                original_filename=validated_input.name,
            )

            total_bytes = validated_input.stat().st_size
            processed_bytes = 0

            # Initial progress notification
            if progress_callback:
                progress_callback(0, total_bytes)

            # 4. Streaming Encryption Write Loop
            with open(validated_input, "rb") as in_file, open(
                destination, "wb+"
            ) as out_file:
                # Write contiguous binary header
                out_file.write(header_bytes)

                # Process payload in configurable chunks
                while chunk := in_file.read(chunk_size):
                    cipher_chunk = encryptor.update(chunk)
                    if cipher_chunk:
                        out_file.write(cipher_chunk)

                    processed_bytes += len(chunk)
                    if progress_callback:
                        progress_callback(processed_bytes, total_bytes)

                # Finalize GCM stream
                final_cipher_chunk = encryptor.finalize()
                if final_cipher_chunk:
                    out_file.write(final_cipher_chunk)

                # 5. Extract Authentication Tag & Write into Binary Header Tag Offset
                auth_tag = encryptor.tag
                out_file.seek(TAG_OFFSET_IN_HEADER)
                out_file.write(auth_tag)

            logger.info(
                f"Encryption completed successfully: '{destination.name}' "
                f"({processed_bytes} bytes processed)"
            )
            return destination

        except Exception as err:
            logger.error(f"Encryption failed for '{validated_input.name}': {err}")
            # Cleanup incomplete file on failure
            if destination.exists():
                try:
                    destination.unlink()
                except Exception:
                    pass
            if isinstance(err, (FileAccessError, ValueError)):
                raise
            raise EncryptionError(f"Encryption operation failed: {err}") from err

        finally:
            # Secure memory cleanup
            if raw_key:
                KeyDerivationManager.wipe_memory(raw_key)
