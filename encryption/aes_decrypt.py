"""
Low-Level Cipher AES-256-GCM Streaming File Decryption Engine.

Implements true chunk-based streaming file decryption using low-level Cipher(algorithms.AES, modes.GCM).
Parses extensible binary headers, automatically restores original filenames, verifies GCM AEAD tags,
zeroes derived keys in memory, and converts tag failures into user-friendly integrity exceptions.
"""

from pathlib import Path
from typing import Callable, Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import config
from encryption.key_manager import KeyDerivationManager
from encryption.utils import (
    DecryptionError,
    FileAccessError,
    IntegrityVerificationError,
    InvalidFileFormatError,
    InvalidPasswordError,
    logger,
    unpack_header,
    validate_input_file,
    validate_password,
)


class FileDecryptor:
    """
    Production-ready streaming file decryptor using low-level AES-256-GCM.
    """

    @staticmethod
    def decrypt_file(
        encrypted_path: Path | str,
        password: str,
        output_dir: Optional[Path | str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        chunk_size: int = config.CHUNK_SIZE,
    ) -> Path:
        """
        Decrypts an encrypted file (.enc) using AES-256-GCM streaming with low-level Cipher API.

        Args:
            encrypted_path: Path to the encrypted .enc file.
            password: User password for key re-derivation.
            output_dir: Optional destination directory for restored file. Defaults to output/.
            progress_callback: Optional callback accepting (processed_bytes, total_bytes).
            chunk_size: Processing chunk size in bytes (default 64 KB).

        Returns:
            Path: Path to the restored original file.

        Raises:
            FileAccessError: If target encrypted file is missing or unreadable.
            InvalidFileFormatError: If file lacks a valid FEDT header signature.
            IntegrityVerificationError: If password is wrong or ciphertext is corrupted/tampered.
            DecryptionError: For unexpected stream or read failures.
        """
        validated_encrypted = validate_input_file(encrypted_path)
        validate_password(password)

        logger.info(
            f"Decryption started for encrypted file: '{validated_encrypted.name}'"
        )

        raw_key: bytearray = bytearray()
        destination: Optional[Path] = None

        try:
            with open(validated_encrypted, "rb") as in_file:
                # 1. Parse Contiguous Binary Header & Extract Cryptographic Parameters
                version, salt, nonce, tag, original_filename, header_size = (
                    unpack_header(in_file)
                )

                # Determine destination output path
                if output_dir is None:
                    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    destination = config.OUTPUT_DIR / original_filename
                else:
                    out_path = Path(output_dir).resolve()
                    out_path.mkdir(parents=True, exist_ok=True)
                    destination = out_path / original_filename

                total_file_size = validated_encrypted.stat().st_size
                total_ciphertext_bytes = max(0, total_file_size - header_size)

                # Initial progress notification
                if progress_callback:
                    progress_callback(0, total_ciphertext_bytes)

                # 2. Key Re-Derivation
                raw_key = bytearray(KeyDerivationManager.derive_key(password, salt))

                # 3. Low-Level AES-256-GCM Decipher Setup
                cipher = Cipher(
                    algorithms.AES(bytes(raw_key)),
                    modes.GCM(nonce, tag),
                )
                decryptor = cipher.decryptor()

                # 4. Streaming Decryption Read/Write Loop
                processed_bytes = 0
                with open(destination, "wb") as out_file:
                    while chunk := in_file.read(chunk_size):
                        plain_chunk = decryptor.update(chunk)
                        if plain_chunk:
                            out_file.write(plain_chunk)

                        processed_bytes += len(chunk)
                        if progress_callback:
                            progress_callback(processed_bytes, total_ciphertext_bytes)

                    # 5. Finalize Decryption & Verify Authentication Tag
                    try:
                        final_plain_chunk = decryptor.finalize()
                        if final_plain_chunk:
                            out_file.write(final_plain_chunk)
                    except InvalidTag as tag_err:
                        logger.error(
                            f"Decryption tag verification failed for '{validated_encrypted.name}': "
                            "Incorrect password or corrupted file."
                        )
                        raise IntegrityVerificationError(
                            "Decryption failed: Incorrect password or corrupted encrypted file."
                        ) from tag_err

            logger.info(
                f"Decryption completed successfully: Restored '{destination.name}' "
                f"({processed_bytes} bytes processed)"
            )
            return destination

        except (
            FileAccessError,
            InvalidFileFormatError,
            IntegrityVerificationError,
            ValueError,
        ):
            # Clean up partially written file on authentication failure
            if destination and destination.exists():
                try:
                    destination.unlink()
                except Exception:
                    pass
            raise

        except Exception as err:
            logger.error(
                f"Decryption failed unexpectedly for '{validated_encrypted.name}': {err}"
            )
            if destination and destination.exists():
                try:
                    destination.unlink()
                except Exception:
                    pass
            raise DecryptionError(
                f"Decryption operation encountered an error: {err}"
            ) from err

        finally:
            # Secure memory cleanup
            if raw_key:
                KeyDerivationManager.wipe_memory(raw_key)
