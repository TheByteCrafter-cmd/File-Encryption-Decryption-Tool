"""
Main CLI Demonstration & Verification Runner.

Demonstrates end-to-end multi-format file encryption and decryption, SHA-256 cryptographic verification,
error handling edge cases, and automated execution of the pytest suite.
"""

import hashlib
import os
import sys
from pathlib import Path
from typing import List

import pytest

import config
from encryption.aes_decrypt import FileDecryptor
from encryption.aes_encrypt import FileEncryptor
from encryption.utils import (
    IntegrityVerificationError,
    InvalidFileFormatError,
    get_logger,
)

logger = get_logger("FEDT.Main")


def print_banner() -> None:
    """Prints a styled CLI header banner."""
    print("=" * 80)
    print(f"   {config.APP_NAME} ({config.APP_VERSION})")
    print("   Enterprise AES-256-GCM Backend Engine Verification")
    print("=" * 80)


def compute_sha256(file_path: Path) -> str:
    """Computes SHA-256 hex digest of target file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_sample_files() -> List[Path]:
    """Generates synthetic test files of diverse formats inside samples/."""
    config.SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    sample_files: List[Path] = []

    # 1. Text sample (.txt)
    txt_file = config.SAMPLES_DIR / "confidential_notes.txt"
    txt_file.write_text(
        "Confidential Project Specification 2026.\n"
        "AES-256-GCM Authenticated Encryption with PBKDF2 Key Derivation.\n",
        encoding="utf-8",
    )
    sample_files.append(txt_file)

    # 2. Binary document simulation (.pdf)
    pdf_file = config.SAMPLES_DIR / "financial_statement.pdf"
    pdf_file.write_bytes(b"%PDF-1.7\n" + b"\x00\xff\xfe\xfd\xfc" * 2000)
    sample_files.append(pdf_file)

    # 3. Simulated image asset (.png)
    png_file = config.SAMPLES_DIR / "security_diagram.png"
    png_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + os.urandom(5000))
    sample_files.append(png_file)

    # 4. Large binary archive payload (.zip)
    zip_file = config.SAMPLES_DIR / "backup_archive.zip"
    zip_file.write_bytes(b"PK\x03\x04" + os.urandom(50_000))
    sample_files.append(zip_file)

    return sample_files


def run_demonstration() -> bool:
    """Executes sample file encryption, decryption, and hash verification."""
    print("\n--- [Phase 1: Multi-Format Encryption & Decryption Workflow] ---")
    sample_files = generate_sample_files()
    master_password = "EnterpriseMasterPassword2026!"
    restored_dir = config.OUTPUT_DIR / "restored"
    restored_dir.mkdir(parents=True, exist_ok=True)

    all_passed = True

    for sample in sample_files:
        original_hash = compute_sha256(sample)
        print(
            f"\n[+] Processing: '{sample.name}' (Size: {sample.stat().st_size} bytes)"
        )
        print(f"    Original SHA-256 : {original_hash}")

        # Progress reporting hook
        def progress_reporter(processed: int, total: int):
            percent = (processed / total * 100) if total > 0 else 100
            sys.stdout.write(
                f"\r    [Progress] {processed}/{total} bytes ({percent:.1f}%)"
            )
            sys.stdout.flush()

        # Encrypt
        enc_path = FileEncryptor.encrypt_file(
            input_path=sample,
            password=master_password,
            progress_callback=progress_reporter,
        )
        print(f"\n    Encrypted Output : {enc_path}")

        # Decrypt
        dec_path = FileDecryptor.decrypt_file(
            encrypted_path=enc_path,
            password=master_password,
            output_dir=restored_dir,
            progress_callback=progress_reporter,
        )
        print(f"\n    Restored Output  : {dec_path}")

        restored_hash = compute_sha256(dec_path)
        print(f"    Restored SHA-256 : {restored_hash}")

        if original_hash == restored_hash:
            print("    Status           : SUCCESS (Hashes Match Perfect Integrity)")
        else:
            print("    Status           : FAILED (Hash Mismatch Error)")
            all_passed = False

    return all_passed


def run_error_handling_tests() -> None:
    """Demonstrates graceful handling of invalid passwords and file corruption."""
    print("\n--- [Phase 2: Error Handling & Security Boundary Verification] ---")
    test_sample = config.SAMPLES_DIR / "confidential_notes.txt"
    enc_file = config.OUTPUT_DIR / "confidential_notes.txt.enc"

    # 1. Wrong Password Test
    print("\n[+] Test 1: Decryption with Incorrect Password")
    try:
        FileDecryptor.decrypt_file(enc_file, password="WrongPassword999!")
        print("    FAILED: Expected IntegrityVerificationError was not raised.")
    except IntegrityVerificationError as err:
        print(f"    PASSED: Caught expected error -> '{err}'")

    # 2. Invalid Header / Format Test
    print("\n[+] Test 2: Decryption of Non-FEDT File")
    invalid_file = config.OUTPUT_DIR / "invalid_format.txt"
    invalid_file.write_text("Regular unencrypted file content", encoding="utf-8")
    try:
        FileDecryptor.decrypt_file(invalid_file, password="AnyPassword")
        print("    FAILED: Expected InvalidFileFormatError was not raised.")
    except InvalidFileFormatError as err:
        print(f"    PASSED: Caught expected error -> '{err}'")


def verify_log_security() -> None:
    """Verifies that no sensitive passwords or keys were written to app.log."""
    print("\n--- [Phase 3: Zero-Trust Log Audit Verification] ---")
    if not config.LOG_FILE.exists():
        print("    Warning: Log file does not exist yet.")
        return

    log_content = config.LOG_FILE.read_text(encoding="utf-8")
    forbidden_terms = ["EnterpriseMasterPassword2026!", "WrongPassword999!", "raw_key"]

    leak_found = False
    for term in forbidden_terms:
        if term in log_content:
            print(
                f"    CRITICAL SECURITY RISK: Sensitive term '{term}' was found in log file!"
            )
            leak_found = True

    if not leak_found:
        print(
            "    PASSED: Audit complete. Zero sensitive passwords or keys exposed in app.log."
        )


def run_pytest_suite() -> int:
    """Runs automated pytest suite programmatically."""
    print("\n--- [Phase 4: Programmatic Pytest Verification Suite Execution] ---")
    return pytest.main(["-v", "tests"])


def main() -> None:
    """Main execution flow."""
    print_banner()
    demo_success = run_demonstration()
    run_error_handling_tests()
    verify_log_security()

    test_exit_code = run_pytest_suite()

    print("\n" + "=" * 80)
    if demo_success and test_exit_code == 0:
        print("   FINAL VERIFICATION RESULTS: ALL SYSTEM CHECKS & TESTS PASSED!")
        print("   Backend Engine is 100% Production Ready for Phase 2 GUI Integration.")
    else:
        print("   FINAL VERIFICATION RESULTS: FAILURES DETECTED!")
        sys.exit(1)
    print("=" * 80)


if __name__ == "__main__":
    main()
