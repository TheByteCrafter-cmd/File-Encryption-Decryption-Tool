"""
Unit tests for authentication tag integrity verification, wrong password handling, and tampering detection.
"""

from pathlib import Path

import pytest

from encryption.aes_decrypt import FileDecryptor
from encryption.aes_encrypt import FileEncryptor
from encryption.utils import IntegrityVerificationError, InvalidFileFormatError


def test_wrong_password_raises_integrity_error(tmp_path: Path):
    """Verify decryption with wrong password raises IntegrityVerificationError and cleans up output."""
    sample_file = tmp_path / "sensitive.docx"
    sample_file.write_bytes(b"DocxContent" * 100)

    encrypted_path = FileEncryptor.encrypt_file(
        input_path=sample_file,
        password="CorrectPassword123",
        output_path=tmp_path / "sensitive.docx.enc",
    )

    out_dir = tmp_path / "decrypted_out"

    with pytest.raises(
        IntegrityVerificationError, match="Incorrect password or corrupted"
    ):
        FileDecryptor.decrypt_file(
            encrypted_path=encrypted_path,
            password="WrongPassword456",
            output_dir=out_dir,
        )

    # Verify partially written file was cleaned up
    expected_restored = out_dir / "sensitive.docx"
    assert not expected_restored.exists()


def test_tampered_ciphertext_raises_integrity_error(tmp_path: Path):
    """Verify modifying a byte in ciphertext causes tag verification failure."""
    sample_file = tmp_path / "data.csv"
    sample_file.write_text("id,name,val\n1,Alice,100\n2,Bob,200\n", encoding="utf-8")

    password = "MySecurePassword"
    encrypted_path = FileEncryptor.encrypt_file(
        input_path=sample_file,
        password=password,
        output_path=tmp_path / "data.csv.enc",
    )

    # Corrupt a byte in the encrypted file (after header offset)
    raw_data = bytearray(encrypted_path.read_bytes())
    corrupt_offset = len(raw_data) - 5
    raw_data[corrupt_offset] ^= 0xFF
    encrypted_path.write_bytes(raw_data)

    with pytest.raises(IntegrityVerificationError):
        FileDecryptor.decrypt_file(
            encrypted_path=encrypted_path,
            password=password,
            output_dir=tmp_path / "decrypted_corrupt",
        )


def test_non_fedt_file_raises_invalid_format(tmp_path: Path):
    """Verify attempting to decrypt a non-FEDT file raises InvalidFileFormatError."""
    random_file = tmp_path / "random.bin"
    random_file.write_bytes(b"NotAFEDTHeaderData" * 10)

    with pytest.raises(InvalidFileFormatError, match="Invalid file format signature"):
        FileDecryptor.decrypt_file(
            encrypted_path=random_file,
            password="AnyPassword",
            output_dir=tmp_path / "out",
        )
