"""
Unit tests for FileEncryptor streaming encryption engine.
"""

from pathlib import Path

import pytest

import config
from encryption.aes_encrypt import FileEncryptor
from encryption.utils import unpack_header


@pytest.fixture
def sample_text_file(tmp_path: Path) -> Path:
    """Fixture creating a temporary sample text file."""
    file_path = tmp_path / "secret_document.txt"
    file_path.write_text(
        "Top Secret Content for Encryption Testing 2026!", encoding="utf-8"
    )
    return file_path


def test_encrypt_file_success(sample_text_file: Path, tmp_path: Path):
    """Verify file encrypts successfully, creates .enc file, and formats valid header."""
    output_path = tmp_path / "secret_document.txt.enc"
    password = "StrongPassword123!"

    progress_updates = []

    def callback(processed: int, total: int):
        progress_updates.append((processed, total))

    result_path = FileEncryptor.encrypt_file(
        input_path=sample_text_file,
        password=password,
        output_path=output_path,
        progress_callback=callback,
    )

    assert result_path.exists()
    assert result_path == output_path
    assert len(progress_updates) >= 2  # Start and finish updates

    # Inspect packed binary header
    with open(result_path, "rb") as stream:
        version, salt, nonce, tag, orig_filename, header_size = unpack_header(stream)

    assert version == config.HEADER_VERSION
    assert len(salt) == config.SALT_SIZE
    assert len(nonce) == config.NONCE_SIZE
    assert len(tag) == config.TAG_SIZE
    assert tag != b"\x00" * 16  # Tag must be overwritten with real GCM tag
    assert orig_filename == "secret_document.txt"


def test_encrypt_nonexistent_file(tmp_path: Path):
    """Verify encrypting nonexistent file raises FileAccessError."""
    fake_file = tmp_path / "missing.txt"
    with pytest.raises(Exception, match="Target file does not exist"):
        FileEncryptor.encrypt_file(fake_file, "password")


def test_encrypt_empty_password(sample_text_file: Path):
    """Verify empty password raises ValueError."""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        FileEncryptor.encrypt_file(sample_text_file, "")
