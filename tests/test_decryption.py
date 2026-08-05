"""
Unit tests for FileDecryptor round-trip streaming decryption and original filename restoration.
"""

import hashlib
from pathlib import Path

import pytest

from encryption.aes_decrypt import FileDecryptor
from encryption.aes_encrypt import FileEncryptor


def compute_sha256(file_path: Path) -> str:
    """Helper computing SHA-256 hex digest of target file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_encryption_decryption_roundtrip(tmp_path: Path):
    """Verify that file encrypted and then decrypted yields identical content (SHA-256 match)."""
    input_file = tmp_path / "financial_report_2026.xlsx"
    binary_content = b"\x50\x4b\x03\x04" + b"ExcelDataPayloadSimulation" * 500
    input_file.write_bytes(binary_content)

    original_hash = compute_sha256(input_file)
    password = "ComplexPassword987#"

    # Encrypt
    encrypted_file = FileEncryptor.encrypt_file(
        input_path=input_file,
        password=password,
        output_path=tmp_path / "enc_out.enc",
    )
    assert encrypted_file.exists()

    # Decrypt to separate output dir
    restored_dir = tmp_path / "restored_dir"
    decrypted_file = FileDecryptor.decrypt_file(
        encrypted_path=encrypted_file,
        password=password,
        output_dir=restored_dir,
    )

    assert decrypted_file.exists()
    assert decrypted_file.name == "financial_report_2026.xlsx"

    restored_hash = compute_sha256(decrypted_file)
    assert restored_hash == original_hash
