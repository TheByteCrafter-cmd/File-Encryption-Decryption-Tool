"""
Real-World QA Test Suite for Phase 1 Backend Engine.

Verifies multi-format file encryption/decryption, SHA-256 round-trip integrity,
wrong password rejection, tampered ciphertext detection, empty password validation,
renamed .enc file restoration, long & Unicode filenames, 100 MB large file streaming,
and original file safety guarantees.
"""

import hashlib
import os
import shutil
from pathlib import Path

import pytest

from encryption.aes_decrypt import FileDecryptor
from encryption.aes_encrypt import FileEncryptor
from encryption.utils import IntegrityVerificationError, InvalidFileFormatError


def compute_sha256(file_path: Path) -> str:
    """Helper computing SHA-256 hex digest of target file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


# ==============================================================================
# 1. Multi-Format Real-World Round-Trip Verification
# ==============================================================================


@pytest.mark.parametrize(
    "extension, header, size_bytes",
    [
        (".txt", b"Plain text payload for encryption QA verification.\n" * 50, 2500),
        (".pdf", b"%PDF-1.7\n" + b"\x00\xff\xfe\xfd\xfc" * 500, 2500),
        (".png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x12\x34" * 1000, 2016),
        (".jpg", b"\xff\xd8\xff\xe0\x00\x10JFIF\x00" + b"\xab\xcd" * 1000, 2010),
        (".zip", b"PK\x03\x04\x14\x00\x00\x00" + b"\x55\xaa" * 1000, 2010),
        (".mp4", b"\x00\x00\x00\x18ftypmp42" + b"\x99\x88" * 1000, 2012),
        (".exe", b"MZ\x90\x00\x03\x00\x00\x00" + b"\x11\x22" * 1000, 2008),
        (".bin", b"\x00\x01\x02\x03\x04\x05" + os.urandom(4000), 4006),
    ],
)
def test_real_world_file_formats_roundtrip(
    tmp_path: Path, extension: str, header: bytes, size_bytes: int
):
    """
    Verifies encryption and decryption round-trip across realistic binary file types.
    Checks exact SHA-256 hash match before and after decryption.
    """
    filename = f"sample_realworld_file{extension}"
    sample_path = tmp_path / filename
    sample_path.write_bytes(header)

    original_hash = compute_sha256(sample_path)
    password = "QAPassword2026!Secure"

    # Encrypt
    enc_path = FileEncryptor.encrypt_file(
        input_path=sample_path,
        password=password,
        output_path=tmp_path / f"{filename}.enc",
    )
    assert enc_path.exists()
    assert enc_path.stat().st_size > sample_path.stat().st_size  # Header added

    # Decrypt
    out_dir = tmp_path / "restored_formats"
    restored_path = FileDecryptor.decrypt_file(
        encrypted_path=enc_path,
        password=password,
        output_dir=out_dir,
    )

    assert restored_path.exists()
    assert restored_path.name == filename
    restored_hash = compute_sha256(restored_path)
    assert restored_hash == original_hash


# ==============================================================================
# 2. Security Edge-Cases (Wrong Password, Corrupted Data, Empty Password)
# ==============================================================================


def test_wrong_password_security(tmp_path: Path):
    """Verifies that decryption with an incorrect password fails and leaves no partial output file."""
    sample = tmp_path / "confidential_vault.bin"
    sample.write_bytes(b"Confidential Payload Data " * 100)

    correct_pwd = "CorrectPassword@123"
    wrong_pwd = "WrongPassword@123"

    enc_path = FileEncryptor.encrypt_file(
        input_path=sample,
        password=correct_pwd,
        output_path=tmp_path / "vault.enc",
    )

    out_dir = tmp_path / "failed_out"
    with pytest.raises(
        IntegrityVerificationError, match="Incorrect password or corrupted"
    ):
        FileDecryptor.decrypt_file(
            encrypted_path=enc_path,
            password=wrong_pwd,
            output_dir=out_dir,
        )

    # Ensure no partial file exists
    assert not (out_dir / "confidential_vault.bin").exists()


def test_corrupted_encrypted_file_tamper_detection(tmp_path: Path):
    """
    Verifies that AES-GCM tag verification detects tampering, safely deletes partial output,
    and leaves the original .enc file untouched.
    """
    sample = tmp_path / "financial_records.pdf"
    sample.write_bytes(b"%PDF-1.7 Payload Content " * 200)

    password = "RobustPassword#2026"
    enc_path = FileEncryptor.encrypt_file(
        input_path=sample,
        password=password,
        output_path=tmp_path / "records.pdf.enc",
    )

    # Copy encrypted file
    copied_enc_path = tmp_path / "records_corrupted.pdf.enc"
    shutil.copy(enc_path, copied_enc_path)

    # Tamper with ciphertext bytes in copy
    raw_data = bytearray(copied_enc_path.read_bytes())
    tamper_index = len(raw_data) - 10
    raw_data[tamper_index] ^= 0xAA
    copied_enc_path.write_bytes(raw_data)

    original_enc_hash = compute_sha256(enc_path)

    out_dir = tmp_path / "tamper_out"
    with pytest.raises(IntegrityVerificationError):
        FileDecryptor.decrypt_file(
            encrypted_path=copied_enc_path,
            password=password,
            output_dir=out_dir,
        )

    # Verify original .enc file was not modified
    assert compute_sha256(enc_path) == original_enc_hash
    # Verify no partial output file remains
    assert not (out_dir / "financial_records.pdf").exists()


def test_empty_password_rejection(tmp_path: Path):
    """Verifies that empty passwords are rejected immediately for both encryption and decryption."""
    sample = tmp_path / "data.txt"
    sample.write_text("Secret Data", encoding="utf-8")

    with pytest.raises(ValueError, match="Password cannot be empty"):
        FileEncryptor.encrypt_file(sample, "")

    valid_enc = FileEncryptor.encrypt_file(
        sample, password="ValidPassword123", output_path=tmp_path / "data.txt.enc"
    )

    with pytest.raises(ValueError, match="Password cannot be empty"):
        FileDecryptor.decrypt_file(valid_enc, "")


# ==============================================================================
# 3. Filename Metadata & Extension Preservation Edge-Cases
# ==============================================================================


def test_renamed_enc_file_restoration(tmp_path: Path):
    """
    Verifies that renaming the .enc file does not impact automatic restoration
    of the original filename embedded inside binary header metadata.
    """
    sample = tmp_path / "important_contract.pdf"
    sample.write_bytes(b"%PDF-1.7 Executive Agreement Document Content" * 50)

    password = "MetadataPassword!2026"
    enc_path = FileEncryptor.encrypt_file(
        input_path=sample,
        password=password,
        output_path=tmp_path / "important_contract.pdf.enc",
    )

    # Rename .enc file to random_name.enc
    renamed_enc = tmp_path / "random_obfuscated_name.enc"
    enc_path.rename(renamed_enc)

    out_dir = tmp_path / "renamed_restored_dir"
    restored = FileDecryptor.decrypt_file(
        encrypted_path=renamed_enc,
        password=password,
        output_dir=out_dir,
    )

    # Should be restored with original name "important_contract.pdf"
    assert restored.exists()
    assert restored.name == "important_contract.pdf"
    assert compute_sha256(restored) == compute_sha256(sample)


def test_long_filename_support(tmp_path: Path):
    """Verifies encryption and decryption of files with long OS-valid filenames (150+ chars)."""
    long_name = (
        "project_specification_document_enterprise_security_compliance_audit_"
        "verification_report_final_version_2026_confidential_archive_draft.docx"
    )
    sample = tmp_path / long_name
    sample.write_text("Long Filename Test Payload", encoding="utf-8")

    password = "LongFilenamePassword123"
    enc_path = FileEncryptor.encrypt_file(
        input_path=sample,
        password=password,
        output_path=tmp_path / f"{long_name}.enc",
    )

    out_dir = tmp_path / "long_fname_out"
    restored = FileDecryptor.decrypt_file(
        encrypted_path=enc_path,
        password=password,
        output_dir=out_dir,
    )

    assert restored.name == long_name
    assert compute_sha256(restored) == compute_sha256(sample)


def test_unicode_filename_support(tmp_path: Path):
    """
    Verifies support for international UTF-8 Unicode filenames:
    - Hindi: हेलो.txt
    - Chinese: 测试.pdf
    - French/Spanish: résumé_información.txt
    """
    unicode_names = ["हेलो.txt", "测试.pdf", "résumé_información.txt"]
    password = "UnicodePassword!2026"

    for name in unicode_names:
        sample = tmp_path / name
        sample.write_bytes(f"Unicode Test Payload for {name}".encode("utf-8"))

        original_hash = compute_sha256(sample)

        enc_path = FileEncryptor.encrypt_file(
            input_path=sample,
            password=password,
            output_path=tmp_path / f"{name}.enc",
        )

        out_dir = tmp_path / "unicode_out"
        restored = FileDecryptor.decrypt_file(
            encrypted_path=enc_path,
            password=password,
            output_dir=out_dir,
        )

        assert restored.name == name
        assert compute_sha256(restored) == original_hash


# ==============================================================================
# 4. Large File Streaming Performance Test (100 MB Payload)
# ==============================================================================


def test_100mb_large_file_streaming(tmp_path: Path):
    """
    Generates a temporary 100 MB binary file in chunks.
    Encrypts and decrypts it using chunk-based streaming.
    Verifies SHA-256 exact match and cleans up artifacts afterwards.
    """
    large_file = tmp_path / "large_payload_100mb.bin"
    target_bytes = 100 * 1024 * 1024  # 100 MB

    # Write 100 MB binary file in 1 MB chunks
    chunk_pattern = os.urandom(1024 * 1024)
    written = 0
    with open(large_file, "wb") as f:
        while written < target_bytes:
            f.write(chunk_pattern)
            written += len(chunk_pattern)

    original_hash = compute_sha256(large_file)
    password = "LargeFile100MBPassword!"

    progress_history = []

    def progress_callback(processed: int, total: int):
        progress_history.append(processed)

    # Encrypt
    enc_path = FileEncryptor.encrypt_file(
        input_path=large_file,
        password=password,
        output_path=tmp_path / "large_payload_100mb.bin.enc",
        progress_callback=progress_callback,
    )

    assert enc_path.exists()
    assert len(progress_history) > 1000  # Multi-chunk streaming updates

    # Decrypt
    out_dir = tmp_path / "large_out"
    restored_path = FileDecryptor.decrypt_file(
        encrypted_path=enc_path,
        password=password,
        output_dir=out_dir,
    )

    assert restored_path.exists()
    assert restored_path.name == "large_payload_100mb.bin"

    restored_hash = compute_sha256(restored_path)
    assert restored_hash == original_hash

    # Cleanup temporary 100 MB test files to save disk space
    large_file.unlink()
    enc_path.unlink()
    restored_path.unlink()


# ==============================================================================
# 5. Original File Safety Guarantees
# ==============================================================================


def test_original_file_safety(tmp_path: Path):
    """
    Verifies that encryption never alters or deletes the source input file,
    and failed decryption never alters the source .enc file.
    """
    sample = tmp_path / "source_document.docx"
    sample.write_bytes(b"Original Document Payload Content " * 100)
    original_hash = compute_sha256(sample)

    password = "SafetyPassword123"
    enc_path = FileEncryptor.encrypt_file(
        input_path=sample,
        password=password,
        output_path=tmp_path / "source_document.docx.enc",
    )

    # Original file must remain untouched
    assert sample.exists()
    assert compute_sha256(sample) == original_hash

    enc_original_hash = compute_sha256(enc_path)

    # Attempt decryption with wrong password
    with pytest.raises(IntegrityVerificationError):
        FileDecryptor.decrypt_file(
            encrypted_path=enc_path,
            password="WrongPassword999",
            output_dir=tmp_path / "fail_dir",
        )

    # Encrypted file must remain completely untouched
    assert enc_path.exists()
    assert compute_sha256(enc_path) == enc_original_hash
