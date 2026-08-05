"""
Unit tests for large file chunk-based streaming and progress callbacks.
"""

import os
from pathlib import Path

import pytest

import config
from encryption.aes_decrypt import FileDecryptor
from encryption.aes_encrypt import FileEncryptor
from tests.test_decryption import compute_sha256


def test_large_payload_streaming(tmp_path: Path):
    """
    Verify chunked streaming encryption and decryption on a 10 MB payload
    using small custom chunk size (16 KB) to ensure multiple streaming updates.
    """
    payload_size = 10 * 1024 * 1024  # 10 MB
    large_file = tmp_path / "dataset_large_2026.bin"

    # Write pseudo-random 10 MB payload
    chunk_data = os.urandom(64 * 1024)
    with open(large_file, "wb") as f:
        written = 0
        while written < payload_size:
            to_write = min(len(chunk_data), payload_size - written)
            f.write(chunk_data[:to_write])
            written += to_write

    original_digest = compute_sha256(large_file)
    password = "StreamingTestPassword2026!"
    small_chunk = 16 * 1024  # 16 KB chunk size

    enc_progress_calls = []

    def enc_callback(processed: int, total: int):
        enc_progress_calls.append((processed, total))

    # Encrypt
    encrypted_file = FileEncryptor.encrypt_file(
        input_path=large_file,
        password=password,
        output_path=tmp_path / "dataset_large.enc",
        progress_callback=enc_callback,
        chunk_size=small_chunk,
    )

    assert encrypted_file.exists()
    # 10 MB / 16 KB = ~640 chunk iterations
    assert len(enc_progress_calls) > 500
    assert enc_progress_calls[-1][0] == payload_size

    dec_progress_calls = []

    def dec_callback(processed: int, total: int):
        dec_progress_calls.append((processed, total))

    # Decrypt
    restored_dir = tmp_path / "streaming_out"
    decrypted_file = FileDecryptor.decrypt_file(
        encrypted_path=encrypted_file,
        password=password,
        output_dir=restored_dir,
        progress_callback=dec_callback,
        chunk_size=small_chunk,
    )

    assert decrypted_file.exists()
    assert decrypted_file.name == "dataset_large_2026.bin"
    assert len(dec_progress_calls) > 500

    restored_digest = compute_sha256(decrypted_file)
    assert restored_digest == original_digest
